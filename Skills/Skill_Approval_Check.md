# 🔍 Skill: Approval Check
**Skill ID:** `silver.approval_check`
**Status:** 🟢 Active

## Description
Monitoring the `Approved/` and `Rejected/` folders to trigger final execution or archival.

## Workflow
1. Watch `Approved/` folder for new files.
2. Identify the source task/plan associated with the approved item.
3. Execute the pending action (e.g., Post to LinkedIn, Send Email).
4. Move the approved file to `Done/` after execution.

## Constraints
- Actions are only triggered by file movements, not manual command overrides.
