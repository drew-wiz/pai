import os.path
import datetime
import argparse
import json
from google import genai

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/drive"]
TEMPLATE_ID = "1jAs8WnaqvW8x4WEqcZgVxPqL3kPZdwdw7gV-iR1-2F0"

def get_creds():
    creds = None
    creds_dir = os.path.expanduser("~/.pai_credentials/google")
    creds_path = os.path.join(creds_dir, "credentials.json")
    token_path = os.path.join(creds_dir, "token_slides.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds

def generate_content_from_notes(notes, api_key, additional_instructions=None):
    client = genai.Client(api_key=api_key)
    
    user_guidance = ""
    if additional_instructions:
        user_guidance = f"\n\nUSER INSTRUCTIONS (HIGHEST PRIORITY): {additional_instructions}\nFollow these instructions strictly when determining the Priorities and Themes."

    prompt = f"""
    You are a solution engineering assistant creating an executive readout deck.
    Based on the following notes and user instructions, extract the key information to populate a slide deck.
    
    Notes:
    {notes}
    {user_guidance}

    You need to identify:
    1. A concise summary of the engagement (timeline, key events) for the 'Our engagement to date' slide.
    2. The Top 3 Business Priorities/Themes identified during the PoV.
    3. For EACH Priority, identify:
       - 3 specific findings, wins, or goals achieved ('findings').
       - A list of challenges/pain points ('challenges').
       - A list of downstream mission impacts ('impacts').
    4. A list of 3-5 concrete Next Steps.

    Output MUST be valid JSON with this exact structure:
    {{
      "engagement_summary": "Concise summary text...",
      "priorities": [
        {{
          "title": "Priority 1 Title",
          "findings": ["Finding 1", "Finding 2", "Finding 3"],
          "challenges": ["Challenge 1", "Challenge 2", "Challenge 3"],
          "impacts": ["Impact 1", "Impact 2", "Impact 3"]
        }},
        {{
          "title": "Priority 2 Title",
          "findings": ["Finding 1", "Finding 2", "Finding 3"],
          "challenges": ["Challenge 1", "Challenge 2", "Challenge 3"],
          "impacts": ["Impact 1", "Impact 2", "Impact 3"]
        }},
        {{
          "title": "Priority 3 Title",
          "findings": ["Finding 1", "Finding 2", "Finding 3"],
          "challenges": ["Challenge 1", "Challenge 2", "Challenge 3"],
          "impacts": ["Impact 1", "Impact 2", "Impact 3"]
        }}
      ],
      "next_steps": ["Step 1", "Step 2", "Step 3"],
      "timeline_use_cases": ["Use Case 1", "Use Case 2", "Use Case 3", "Use Case 4"]
    }}
    """

    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt,
        config={'response_mime_type': 'application/json'}
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Error decoding JSON from Gemini response. Raw response:")
        print(response.text)
        return None

def create_replacement_request(text_to_find, replacement_text, page_object_ids=None):
    if not replacement_text:
        replacement_text = "" 
        
    req = {
        "replaceAllText": {
            "containsText": {"text": text_to_find, "matchCase": True},
            "replaceText": replacement_text,
        }
    }
    if page_object_ids:
        req["replaceAllText"]["pageObjectIds"] = page_object_ids
    return req

def format_list(items):
    return "\n".join([f"• {item}" for item in items])

def main(customer_name, ae_name, region, notes_file, additional_instructions):
    creds = get_creds()
    
    try:
        # 1. Copy Template
        drive_service = build("drive", "v3", credentials=creds)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        copy_title = f"{customer_name} - Executive Readout - {timestamp}"
        
        # Folder ID for 'templates/ai-workspace'
        TARGET_FOLDER_ID = "1pWnLJ6FlLmpgaYmMjnHpQEru1su7OTO9" 
        
        body = {"name": copy_title, "parents": [TARGET_FOLDER_ID]}
        drive_response = drive_service.files().copy(fileId=TEMPLATE_ID, body=body).execute()
        presentation_copy_id = drive_response.get("id")
        print(f"Created presentation copy: {presentation_copy_id}")
        print(f"Presentation located in folder ID: {TARGET_FOLDER_ID}")

        # 2. Get Presentation Structure
        slides_service = build("slides", "v1", credentials=creds)
        presentation = slides_service.presentations().get(presentationId=presentation_copy_id).execute()
        slides = presentation.get('slides')
        
        # 3. Generate Content
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        with open(notes_file, "r") as f:
            notes = f.read()
            
        content = generate_content_from_notes(notes, api_key, additional_instructions)
        if not content:
            return

        # 4. Prepare Batch Update Requests
        requests = []

        # Global Static Replacements
        requests.append(create_replacement_request("{{customer_name}}", customer_name))
        requests.append(create_replacement_request("{{stakeholder}}", customer_name))
        requests.append(create_replacement_request("{{AE}}", ae_name))
        requests.append(create_replacement_request("{{REGION}}", region))
        requests.append(create_replacement_request("<REP>", ae_name))
        requests.append(create_replacement_request("<REGION>", region))

        # Slide 3: Timeline Replacements
        requests.append(create_replacement_request("{{pov_started_details}}", content.get("engagement_summary", "")))
        
        timeline_use_cases = content.get("timeline_use_cases", [])
        for i in range(4):
            placeholder = f"{{{{use_case_0{i+1}}}}}"
            val = timeline_use_cases[i] if i < len(timeline_use_cases) else ""
            requests.append(create_replacement_request(placeholder, val))

        # Priority Deep Dives
        priorities = content.get("priorities", [])
        
        # Priority 1
        if len(priorities) > 0:
            p = priorities[0]
            requests.append(create_replacement_request("{{priority_01}}", p["title"]))
            requests.append(create_replacement_request("{{challenge_list_01}}", format_list(p.get("challenges", []))))
            requests.append(create_replacement_request("{{impact_list_01}}", format_list(p.get("impacts", []))))
            
            if len(slides) > 8:
                requests.append(create_replacement_request("PRIORITY 1", p["title"], [slides[8].get('objectId')]))
            if len(slides) > 10:
                p_goals_id = slides[10].get('objectId')
                requests.append(create_replacement_request("PRIORITY 1", p["title"], [p_goals_id]))
                findings = p.get("findings", [])
                for i in range(3):
                    finding_text = f"• {findings[i]}" if i < len(findings) else ""
                    requests.append(create_replacement_request(f"Goal {i+1}", finding_text, [p_goals_id]))

        # Priority 2
        if len(priorities) > 1:
            p = priorities[1]
            requests.append(create_replacement_request("{{priority_02}}", p["title"]))
            requests.append(create_replacement_request("{{challenge_list_02}}", format_list(p.get("challenges", []))))
            requests.append(create_replacement_request("{{impact_list_02}}", format_list(p.get("impacts", []))))
            
            if len(slides) > 11:
                requests.append(create_replacement_request("PRIORITY 2", p["title"], [slides[11].get('objectId')]))
            if len(slides) > 13:
                p_goals_id = slides[13].get('objectId')
                requests.append(create_replacement_request("PRIORITY 2", p["title"], [p_goals_id]))
                findings = p.get("findings", [])
                for i in range(3):
                    finding_text = f"• {findings[i]}" if i < len(findings) else ""
                    requests.append(create_replacement_request(f"Goal {i+1}", finding_text, [p_goals_id]))

        # Priority 3
        if len(priorities) > 2:
            p = priorities[2]
            requests.append(create_replacement_request("{{priority_03}}", p["title"]))
            requests.append(create_replacement_request("{{challenge_list_03}}", format_list(p.get("challenges", []))))
            requests.append(create_replacement_request("{{impact_list_03}}", format_list(p.get("impacts", []))))
            
            if len(slides) > 14:
                requests.append(create_replacement_request("PRIORITY 3", p["title"], [slides[14].get('objectId')]))
            if len(slides) > 16:
                p_goals_id = slides[16].get('objectId')
                requests.append(create_replacement_request("PRIORITY 3", p["title"], [p_goals_id]))
                findings = p.get("findings", [])
                for i in range(3):
                    finding_text = f"• {findings[i]}" if i < len(findings) else ""
                    requests.append(create_replacement_request(f"Goal {i+1}", finding_text, [p_goals_id]))

        # Next Steps (Slide 20)
        if len(slides) > 19:
            steps = content.get("next_steps", [])
            if steps:
                next_steps_text = "Next Steps\n" + "\n".join([f"• {step}" for step in steps])
                requests.append(create_replacement_request("Next Steps", next_steps_text, [slides[19].get('objectId')]))

        # Execute Batch Update
        requests = [r for r in requests if r is not None]
        if requests:
            update_body = {"requests": requests}
            slides_service.presentations().batchUpdate(presentationId=presentation_copy_id, body=update_body).execute()
            print(f"Updated presentation with {len(requests)} replacements.")

        # Final Summary
        print("\n--- PoV Deck Creation Summary ---")
        print(f"Presentation ID: {presentation_copy_id}")
        print(f"Folder:          templates/ai-workspace ({TARGET_FOLDER_ID})")
        print(f"Customer Name:   {customer_name}")
        print(f"Account Exec:    {ae_name}")
        print(f"Region:          {region}")
        print(f"Notes File:      {notes_file}")
        print("---------------------------------")

    except HttpError as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Google Slides presentation.")
    parser.add_argument("--customer-name", type=str, required=True, help="The name of the customer.")
    parser.add_argument("--ae-name", type=str, required=True, help="The name of the Account Executive.")
    parser.add_argument("--region", type=str, required=True, help="The geographic region.")
    parser.add_argument("--notes-file", type=str, required=True, help="The path to the text file containing the presentation notes.")
    parser.add_argument("--additional-instructions", type=str, help="Specific user instructions or priorities to guide content generation.")
    args = parser.parse_args()
    main(args.customer_name, args.ae_name, args.region, args.notes_file, args.additional_instructions)
