import os.path
import datetime
import argparse
from google import genai

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/drive"]
TEMPLATE_ID = "1jAs8WnaqvW8x4WEqcZgVxPqL3kPZdwdw7gV-iR1-2F0"

def main(customer_name, ae_name, region, notes_file):
  """Copies a presentation and prints the new presentation ID.
  """
  creds = None
  creds_dir = os.path.expanduser("~/.pai_credentials/google")
  creds_path = os.path.join(creds_dir, "credentials.json")
  token_path = os.path.join(creds_dir, "token.json")

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          creds_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, "w") as token:
      token.write(creds.to_json())

  try:
    drive_service = build("drive", "v3", credentials=creds)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    copy_title = f"{customer_name} - Executive Readout - {timestamp}"
    body = {"name": copy_title, "parents": ["1pWnLJ6FlLmpgaYmMjnHpQEru1su7OTO9"]}
    drive_response = (
        drive_service.files()
        .copy(fileId=TEMPLATE_ID, body=body)
        .execute()
    )
    presentation_copy_id = drive_response.get("id")
    print(f"Created a copy of the presentation with ID: {presentation_copy_id}")

    slides_service = build("slides", "v1", credentials=creds)
    requests = [
        {
            "replaceAllText": {
                "containsText": {"text": "{{customer_name}}", "matchCase": True},
                "replaceText": customer_name,
            }
        },
        {
            "replaceAllText": {
                "containsText": {"text": "{{AE}}", "matchCase": True},
                "replaceText": ae_name,
            }
        },
        {
            "replaceAllText": {
                "containsText": {"text": "{{REGION}}", "matchCase": True},
                "replaceText": region,
            }
        }
    ]
    body = {"requests": requests}
    response = (
        slides_service.presentations()
        .batchUpdate(presentationId=presentation_copy_id, body=body)
        .execute()
    )
    print("Replaced text in the presentation.")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    client = genai.Client(api_key=api_key)

    with open(notes_file, "r") as f:
        notes = f.read()
    
    prompt = f"""
    Based on the following notes, extract the required information and format it as a JSON object.

    Notes:
    {notes}

    JSON format:
    {{
      "pov_started_details": "A very concise summary of the cloud connection and time taken (e.g., 'Connected to Azure - 20 minutes').",
      "use_case_01": "A terse, 2-3 word topic for the first use case.",
      "use_case_02": "A terse, 2-3 word topic for the second use case.",
      "use_case_03": "A terse, 2-3 word topic for the third use case.",
      "use_case_04": "A terse, 2-3 word topic for the fourth use case."
    }}
    """

    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt
    )
    import json
    
    # Clean the response to extract only the JSON
    cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
    slide_3_content = json.loads(cleaned_response)

    requests = [
        {
            "replaceAllText": {
                "containsText": {"text": "{{pov_started_details}}", "matchCase": True},
                "replaceText": slide_3_content["pov_started_details"],
            }
        },
        {
            "replaceAllText": {
                "containsText": {"text": "{{use_case_01}}", "matchCase": True},
                "replaceText": slide_3_content["use_case_01"],
            }
        },
        {
            "replaceAllText": {
                "containsText": {"text": "{{use_case_02}}", "matchCase": True},
                "replaceText": slide_3_content["use_case_02"],
            }
        },
        {
            "replaceAllText": {
                "containsText": {"text": "{{use_case_03}}", "matchCase": True},
                "replaceText": slide_3_content["use_case_03"],
            }
        },
        {
            "replaceAllText": {
                "containsText": {"text": "{{use_case_04}}", "matchCase": True},
                "replaceText": slide_3_content["use_case_04"],
            }
        }
    ]
    body = {"requests": requests}
    slides_service.presentations().batchUpdate(presentationId=presentation_copy_id, body=body).execute()
    print("Successfully populated Slide 3 with generated content.")

  except HttpError as err:
    print(err)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Generate a Google Slides presentation.")
  parser.add_argument("--customer-name", type=str, required=True, help="The name of the customer.")
  parser.add_argument("--ae-name", type=str, required=True, help="The name of the Account Executive.")
  parser.add_argument("--region", type=str, required=True, help="The geographic region.")
  parser.add_argument("--notes-file", type=str, required=True, help="The path to the text file containing the presentation notes.")
  args = parser.parse_args()
  main(args.customer_name, args.ae_name, args.region, args.notes_file)
