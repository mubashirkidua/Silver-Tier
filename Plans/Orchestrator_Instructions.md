# Orchestrator Instructions

**Tier:** Silver  
**Version:** 2.0  
**Updated:** 2026-04-30

---

## Core Orchestration Rule (Silver)

> **For every new file in `Needs_Action/`, automatically generate a `Plan.md` in `Plans/`, execute local tasks, and route all external actions (Email, LinkedIn, WhatsApp) through `Pending_Approval/`.**

---

## Silver Workflow steps

### Step 1: Auto-Detect & Plan
- Monitor `Needs_Action/`
- Immediately create `Plans/Plan_YYYYMMDD_<desc>.md` with checkboxes for every step.
- Identify Silver skills required (`silver.email_mcp`, `silver.linkedin_post`).

### Step 2: Processing & HITL Gate
- **Local Tasks:** Execute automatically using Bronze skills.
- **External Actions (HITL):** 
  - If the plan involves sending an email or posting to LinkedIn:
  - Create a file in `Pending_Approval/` (e.g., `LINKEDIN_POST_...md`).
  - DO NOT execute until a human moves the file to `Approved/`.

### Step 3: Execution of Approved Tasks
- Monitor `Approved/` folder.
- Once an item is approved, use the relevant Silver skill to send/post.
- Move approved file to `Done/` after successful execution.

### Step 4: Finalize
- Move the original `Needs_Action` trigger file to `Done/`.
- Log the activity and update `Dashboard.md`.

---

## File Naming Conventions

| Folder | Format |
|--------|--------|
| Plans | `Plan_YYYYMMDD_<desc>.md` |
| Pending | `[TYPE]_YYYYMMDD_<desc>.md` |
| Logs | `activity_YYYYMMDD.md` |
