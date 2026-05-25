# Silver Tier Skills

**Tier Status:** Active (Upgrading)  
**Last Updated:** 2026-04-30

---

## Enabled Skills

### 1. Email Management (MCP)
**Skill ID:** `silver.email_mcp`  
**Permissions:** Send emails via Gmail API  
**HITL Required:** Yes (Always require approval for sending)

**Capabilities:**
- `send_email(to, subject, body)`: Sends a plain text email using configured Gmail credentials.

**Use Cases:**
- Responding to inquiries detected in `Needs_Action`
- Sending automated notifications to the user
- Distributing briefings

---

### 2. LinkedIn Auto-Post
**Skill ID:** `silver.linkedin_auto_post`  
**Status:** Active  
**HITL Required:** Yes

**Capabilities:**
- Generate professional business posts based on vault activity or user prompts.
- Schedule/Move to `Pending_Approval` for review.
- Post to LinkedIn via `watchers/linkedin_poster.py`.

---

### 3. WhatsApp Monitoring
**Skill ID:** `silver.whatsapp_watch`  
**Status:** Active
**HITL Required:** Yes

---

## MCP Configuration
The Email MCP server is located at `mcp/mcp.json`.
