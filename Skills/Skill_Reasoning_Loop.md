# 🔁 Skill: Reasoning Loop
**Skill ID:** `silver.reasoning_loop`
**Status:** 🟢 Active

## Description
The core autonomous logic that drives the "Digital FTE" behavior.

## Loop Logic
1. **Understand:** Read files in `Needs_Action/` or `Approved/`.
2. **Plan:** Create/Update `Plan.md` with checkboxes.
3. **Act:** Use skills (file_mgmt, email_send, etc.) to perform tasks.
4. **Verify:** Check outputs and error logs.
5. **Persist:** If task is incomplete, return to step 1.

## Objective
Continuous operation until task completion or HITL required.
