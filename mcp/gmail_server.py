import os
import base64
import json
import sys
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def send_email(to, subject, body):
    try:
        if not os.path.exists("token.json"):
            return "Error: token.json not found. Please run gmail_watcher.py first to authenticate."
        
        creds = Credentials.from_authorized_user_file("token.json")
        service = build('gmail', 'v1', credentials=creds)
        
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['Subject'] = subject
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        send_result = service.users().messages().send(userId="me", body=create_message).execute()
        return f"Email sent successfully! Message ID: {send_result['id']}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

def get_email_details(message_id):
    try:
        if not os.path.exists("token.json"):
            return {"error": "token.json not found"}
        
        creds = Credentials.from_authorized_user_file("token.json")
        service = build('gmail', 'v1', credentials=creds)
        
        message = service.users().messages().get(userId='me', id=message_id).execute()
        headers = message.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown Sender")
        snippet = message.get('snippet', '')
        
        return {
            "id": message_id,
            "subject": subject,
            "from": sender,
            "snippet": snippet
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    # Simple JSON-RPC-like interface for MCP
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "send_email":
                result = send_email(params.get("to"), params.get("subject"), params.get("body"))
                print(json.dumps({"result": result}))
            elif method == "get_email_details":
                result = get_email_details(params.get("message_id"))
                print(json.dumps({"result": result}))
            else:
                print(json.dumps({"error": "Method not found"}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        # Direct CLI execution for testing
        print(send_email(sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        main()
