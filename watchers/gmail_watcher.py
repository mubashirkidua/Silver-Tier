from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import os
import time

class GmailWatcher:
    def __init__(self, vault_path: str, credentials_path: str = "credentials.json", check_interval: int = 180):
        self.vault_path = vault_path
        self.creds_path = credentials_path
        self.check_interval = check_interval  # 3 minutes
        self.processed_ids = set()

    def check_for_updates(self):
        # First time OAuth flow
        if not os.path.exists("token.json"):
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                self.creds_path, ["https://www.googleapis.com/auth/gmail.modify"]
            )
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        else:
            creds = Credentials.from_authorized_user_file("token.json")

        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q='is:unread is:inbox').execute()
        messages = results.get('messages', [])
        return [m for m in messages if m['id'] not in self.processed_ids]

    def create_action_file(self, message):
        # Create action file in Needs_Action folder
        needs_action_path = os.path.join(self.vault_path, "Needs_Action")
        
        # Get email details
        msg_id = message['id']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_only = datetime.now().strftime("%Y-%m-%d")
        
        # Create action file
        action_file_name = f"GMAIL_{msg_id}_{date_only}.md"
        action_file_path = os.path.join(needs_action_path, action_file_name)
        
        # Create markdown content
        content = f"""# Gmail Action Required

**Received:** {timestamp}
**Message ID:** {msg_id}
**Status:** Unread

---

## Suggested Actions

- [ ] Review email content
- [ ] Determine priority level
- [ ] Respond or delegate as needed
- [ ] Move to appropriate folder (Approved/Pending/Rejected)

---

## Notes

_Add your notes here_

"""
        
        with open(action_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update log
        logs_path = os.path.join(self.vault_path, "Logs")
        log_file = os.path.join(logs_path, f"activity_{date_only}.md")
        
        # Create log file if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Activity Log - {date_only}\n\n| Time | Action | Status |\n|------|--------|--------|\n")
        
        # Append log entry
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"| {timestamp} | Gmail detected: {msg_id} → {action_file_name} | ✅ |\n")
        
        print(f"[{timestamp}] ✅ New Gmail message detected → Needs_Action mein daal diya")
        self.processed_ids.add(msg_id)

    def run(self):
        """Main loop to continuously check for new emails"""
        print("🚀 Gmail Watcher started... (Checking every 3 minutes)")
        try:
            while True:
                new_messages = self.check_for_updates()
                for msg in new_messages:
                    self.create_action_file(msg)
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n⏹️ Gmail Watcher stopped.")

if __name__ == "__main__":
    vault = os.path.join(os.path.dirname(__file__), "..")  # Silver-Tier root
    watcher = GmailWatcher(vault)
    watcher.run()
