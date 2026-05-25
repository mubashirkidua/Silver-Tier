# 📱 LinkedIn Professional Posting Skill

**Skill ID:** `silver.linkedin_auto_post`
**Status:** 🟢 Active
**HITL:** Required (Always)

## Workflow
1. **Generation:** Daily at 09:00 AM, the AI scans `Done/` and `Logs/` for notable achievements.
2. **Drafting:** A professional business post is generated and saved to `Pending_Approval/LINKEDIN_DRAFT_YYYYMMDD.md`.
3. **Review:** User reviews and edits the draft.
4. **Approval:** Once moved to `Approved/`, the `watchers/linkedin_poster.py` script executes the post using Playwright.

## Post Guidelines
- **Tone:** Professional, insightful, and growth-oriented.
- **Content:** AI trends, project updates, or productivity tips.
- **Tags:** 3-5 relevant industry hashtags.
