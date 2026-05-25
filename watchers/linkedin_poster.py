# watchers/linkedin_poster.py
from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import logging
import sys

class LinkedInPoster:
    def __init__(self, session_path: str = "linkedin_session"):
        self.session_path = Path(session_path)
        self.session_path.mkdir(exist_ok=True)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("LinkedInPoster")

    def post(self, post_text: str, post_file_path: str = None):
        """Approved post ko LinkedIn pe post karta hai"""
        try:
            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_path),
                    headless=False,
                    viewport={'width': 1400, 'height': 900},
                    slow_mo=800
                )
                
                page = context.pages[0] if context.pages else context.new_page()
                self.logger.info("Opening LinkedIn Feed...")
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded')
                
                # Check if we need to log in
                if "login" in page.url or "checkpoint" in page.url or not page.is_visible('button:has-text("Start a post")'):
                    print("\n" + "="*60)
                    print("🚨 ACTION REQUIRED: LOGIN TO LINKEDIN")
                    print("1. A browser window has opened.")
                    print("2. Please enter your email/password and log in manually.")
                    print("3. Solve any CAPTCHAs or enter 2FA codes if asked.")
                    print("4. ONCE YOU SEE YOUR FEED AND THE 'Start a post' BUTTON...")
                    input("👉 PRESS ENTER HERE IN THE TERMINAL TO CONTINUE...")
                    print("="*60 + "\n")

                # Robust detection for "Start a post" button
                self.logger.info("Waiting for 'Start a post' button to become interactable...")
                
                # Extended list of selectors for various LinkedIn UI versions
                post_trigger_selectors = [
                    'button:has-text("Start a post")',
                    'button:has-text("Share an update")',
                    '.share-box-feed-entry__trigger',
                    'button[aria-label="Start a post"]',
                    '.artdeco-card .share-box-feed-entry__trigger',
                    'text=Start a post',
                    'xpath=//button[contains(., "Start a post")]',
                    'xpath=//span[contains(text(), "Start a post")]/ancestor::button'
                ]
                
                found_trigger = False
                # Wait for the page to be stable
                page.wait_for_load_state("networkidle", timeout=30000)
                
                for selector in post_trigger_selectors:
                    try:
                        # Try to find and click the element
                        element = page.wait_for_selector(selector, state="visible", timeout=3000)
                        if element:
                            self.logger.info(f"✅ Found post trigger: {selector}")
                            element.click()
                            found_trigger = True
                            break
                    except:
                        continue
                
                if not found_trigger:
                    self.logger.error("❌ Could not find 'Start a post' button. Saving page source for diagnostic...")
                    with open("linkedin_debug_page.html", "w", encoding="utf-8") as f:
                        f.write(page.content())
                    
                    buttons = page.query_selector_all('button')
                    for i, btn in enumerate(buttons[:20]):
                        try:
                            text = btn.inner_text().strip()
                            if text:
                                self.logger.info(f"Button {i}: '{text}'")
                        except:
                            continue
                    
                    self.logger.error("❌ Diagnostic saved to linkedin_debug_page.html. Check the file to find the correct selector.")
                    context.close()
                    return False

                # Type the post in the editor
                self.logger.info("Waiting for editor...")
                page.wait_for_selector('.ql-editor', timeout=15000)
                editor = page.locator('.ql-editor')
                editor.fill(post_text)
                self.logger.info("Post text entered.")
                page.wait_for_timeout(2000)
                
                # Click Post button
                self.logger.info("Looking for 'Post' button...")
                post_btn_selectors = [
                    'button.share-actions__post-action',
                    'button:has-text("Post")',
                    '.share-box-footer__primary-btn'
                ]
                
                for selector in post_btn_selectors:
                    if page.is_visible(selector):
                        page.click(selector)
                        self.logger.info(f"✅ Clicked Post button.")
                        break
                
                page.wait_for_timeout(5000)
                self.logger.info("✅ Post successfully published!")
                context.close()
                return True
                
        except Exception as e:
            self.logger.error(f"LinkedIn posting failed: {e}")
            return False

if __name__ == "__main__":
    poster = LinkedInPoster()
    post_content = sys.argv[1] if len(sys.argv) > 1 else "Hello LinkedIn! #AI"
    print(f"Executing LinkedIn Post: {post_content}")
    poster.post(post_content)
