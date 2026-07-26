# Hermes Backup — Session Notes (2026-07-26)

## User Setup
- User: Nima
- Language: Farsi (فارسی)
- Repo: `https://github.com/nimah12/hermesbackup`
- Auth: Classic GitHub PAT embedded in HTTPS clone URL

## Files Backed Up
- `memories/` — user profile (USER.md)
- `SOUL.md` — personality/soul
- `config.yaml` — configuration
- `skills/` — all custom skills (550+ files)
- `sessions/sessions.json` — session database
- `kanban.db` — kanban database
- `cron/` — cron execution data (executions.db, heartbeats)
- `channel_directory.json` — channel mappings
- `gateway_state.json` — gateway state
- `BACKUP_MANIFEST.md` — generated manifest

## Files Excluded
- `state.db` — **CONTAINS GitHub PAT tokens in plaintext**. GitHub Push Protection detected them and blocked the push.

## Key Commands Used
```bash
# Clone with embedded token
git clone https://ghp_TOKEN@github.com/nimah12/hermesbackup.git /data/hermesbackup

# Undo a commit on an empty repo (only 1 commit, no HEAD~1)
git update-ref -d HEAD

# Script location
/data/.hermes/scripts/backup.sh

# Cron job: every 12h, no_agent, script-only
schedule: "every 12h"
script: "backup.sh"
no_agent: true
```

## Error Encountered
GitHub rejected push with: `GH013: Repository rule violations — Push cannot contain secrets`
- Path: `state.db:625`, `state.db:1334`, `state.db:1563`
- Type: GitHub Personal Access Token
- Fix: excluded `state.db` from backup, recreated commit
