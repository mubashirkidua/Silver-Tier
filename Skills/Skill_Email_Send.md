# 📧 Skill: Email Send
**Skill ID:** `silver.email_send`
**Status:** 🟢 Active

## Description
Capability to compose and send emails via the Gmail MCP server.

## Workflow
1. Identify recipient, subject, and body.
2. Route draft to `Pending_Approval/`.
3. Upon approval, execute `send_email` tool via `mcp/gmail_server.py`.
4. Log Message ID in activity logs.

## Constraints
- **HITL Required:** Always.
- **Limit:** Max 50 emails per day to prevent rate limiting.
