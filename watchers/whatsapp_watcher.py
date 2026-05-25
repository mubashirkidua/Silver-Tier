# watchers/whatsapp_watcher.py
from playwright.sync_api import sync_playwright
from base_watcher import BaseWatcher
from pathlib import Path
import time
import logging

class WhatsAppWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str = "whatsapp_session"):
        super().__init__(vault_path, check_interval=60)
        self.session_path = Path(session_path)
        self.session_path.mkdir(exist_ok=True)
        
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'due', 'bill', 'help', 'reply', 'price', 'quote']
        self.logger.info("WhatsApp Watcher initialized")

    def check_for_updates(self):
        detected = []
        try:
            with sync_playwright() as p:
                # Important changes for stability
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_path),
                    headless=False,           # Must be False for QR scan
                    viewport={'width': 1200, 'height': 800},
                    slow_mo=800,              # Thoda slow rakho
                    timeout=60000             # Zyada timeout
                )
                
                page = context.pages[0] if context.pages else context.new_page()
                
                self.logger.info("Opening WhatsApp Web...")
                page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=45000)
                
                # Extra wait for QR code to appear
                self.logger.info("Waiting for WhatsApp to load (QR code should appear)...")
                page.wait_for_timeout(8000)   # 8 seconds wait
                
                # Try to find chat list (means logged in) or just wait
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=15000)
                    self.logger.info("✅ WhatsApp loaded successfully (already logged in)")
                except:
                    self.logger.info("⏳ QR Code should be visible now. Please scan it quickly!")
                    page.wait_for_timeout(25000)   # Extra 25 seconds for scanning
                
                # Simple check for any unread (optional for first run)
                unread = page.query_selector_all('[aria-label*="unread"]')
                self.logger.info(f"Found {len(unread)} unread chats")
                
                context.close()   # Safe close only after everything
                
        except Exception as e:
            self.logger.error(f"WhatsApp error: {e}")
            # Do not close context aggressively if error
        
        return detected   # For first run we just want browser to stay open longer

    def create_action_file(self, item):
        # Placeholder (abhi sirf testing ke liye)
        filepath = self.needs_action / f"WHATSAPP_test_{int(time.time())}.md"
        content = "---\ntype: whatsapp\nstatus: testing\n---\nWhatsApp Watcher is working."
        filepath.write_text(content, encoding='utf-8')
        return filepath


# ==================== Run Watcher ====================
if __name__ == "__main__":
    vault_path = Path(__file__).parent.parent.absolute()
    watcher = WhatsAppWatcher(str(vault_path))
    
    print("🚀 WhatsApp Watcher Starting...")
    print("→ Browser khulega. QR Code scan karne ke liye ~30-40 seconds hain.")
    print("→ Agar QR nahi dikhta toh script ko Ctrl+C se stop karke dobara run karo.\n")
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n👋 Watcher stopped by user.")
