# 📥 Skill: Process Dropped File
**Skill ID:** `silver.file_process`
**Status:** 🟢 Active

## Description
The entry-point logic for the vault pipeline when a user drops a file into `Inbox/`.

## Workflow
1. `filesystem_watcher.py` detects file in `Inbox/`.
2. File is copied to `Needs_Action/` with `FILE_` or source prefix.
3. AI analyzes content and generates a corresponding `Plan.md` in `Plans/`.
4. Original file is moved to `Done/` or kept in `Needs_Action/` until plan completion.
