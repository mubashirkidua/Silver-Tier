# 👤 Skill: HITL Approval
**Skill ID:** `silver.hitl_gate`
**Status:** 🟢 Active

## Description
The Human-in-the-Loop (HITL) safety mechanism that prevents autonomous execution of sensitive actions.

## Governance Rules
- **Financial:** Any transaction >$100.
- **External:** Any communication (Email, LinkedIn, WhatsApp).
- **Destructive:** Any file deletion or handbook modification.

## Workflow
1. AI creates a metadata-rich file in `Pending_Approval/`.
2. AI pauses execution on that specific task.
3. User moves file to `Approved/` or `Rejected/`.
