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

---

## Conflict Resolution During Backup (Session: 2026-07-26, Second Run)

**Problem**: Push rejected with "fetch first" — remote had commits not present locally. The cron job had run and pushed changes while a manual backup was also attempted.

**Root cause**: Both cron (every 12h) and manual backup tried to push, creating divergent histories. `git pull --rebase` hit a conflict in `config.yaml` (both local and remote had different config changes).

**Resolution**:
```bash
cd /data/hermesbackup
git pull origin main --rebase
# Conflict in config.yaml → chose "ours" (local version)
git checkout --ours config.yaml
git add config.yaml
GIT_EDITOR=true git rebase --continue
git push origin main
```

**Lesson**: 
- Cron jobs and manual backups can race. Consider locking or accept that occasional manual conflict resolution is needed.
- For config.yaml specifically: the local version had user preferences (threshold: 0.90, context_length: 64000) that were overridden by the cron's backup. Using `--ours` preserved the intentional local config.
- `GIT_EDITOR=true` is a clean way to auto-continue rebase without opening an editor.
