---
name: backup-automation
description: "Automated cron backups to Git repos with secret filtering."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [backup, cron, git, github, automation, secrets]
related_skills: [github-repo-management, github-auth]
---

# Backup Automation

Set up scheduled, automated backups of local data to remote Git repositories. Covers file selection, secret filtering, script authoring, and cron job creation.

## When to Use

- User asks to back up config, data, or state files to a Git repo on a schedule
- User wants periodic snapshots of application data (Hermes, databases, configs)
- User asks for disaster-recovery or offsite backup of local resources

## Workflow

### 1. Identify Files to Back Up

Survey the source directory. Categorize files into:
- **Include**: configs, memories, custom data, JSON/YAML/MD files
- **Exclude**: tokens, credentials, secrets, large binary caches

### 2. Check for Secrets in Binary Files

**CRITICAL PITFALL**: GitHub Push Protection scans ALL file types — including SQLite `.db`, `.sqlite`, `.bin` files — for tokens and will block the push.

Before backing up any binary file:
```bash
# Check if a .db file contains token-like strings
strings somefile.db | grep -iE 'ghp_|gho_|github_pat_|sk-|token|secret|password' | head -5
```

If matches are found, **exclude that file** from the backup. Common offenders:
- `state.db` (Hermes state — contains GitHub PATs in plaintext)
- Any SQLite DB that stores API keys, sessions with embedded tokens

### 3. Write the Backup Script

Place scripts in `~/.hermes/scripts/`. Template:

```bash
#!/bin/bash
set -euo pipefail

SOURCE_DIR="/path/to/source"
BACKUP_DIR="/path/to/clone"
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
REPO_URL="https://<token>@github.com/user/repo.git"

# Clone if needed
if [ ! -d "$BACKUP_DIR/.git" ]; then
    git clone "$REPO_URL" "$BACKUP_DIR" 2>/dev/null || true
fi

cd "$BACKUP_DIR"
git config user.email "backup-bot@hermes"
git config user.name "Backup Bot"

# Clean previous snapshot
find . -maxdepth 1 -not -name '.git' -not -name '.' -not -name '..' -exec rm -rf {} +

# Copy files (exclude sensitive ones)
# cp -r "$SOURCE_DIR/important_files/" ./
# DO NOT copy state.db, credentials, tokens

# Commit and push
git add -A
if git diff --cached --quiet; then
    echo "No changes."
else
    git commit -m "Backup: $TIMESTAMP"
    git push origin main 2>&1
fi
```

### 4. Undo a Failed Push

If a push is rejected (e.g., secret detected), undo the local commit:
```bash
# If it's the only commit (empty repo):
git update-ref -d HEAD

# If there are prior commits:
git reset HEAD~1
```

Then fix the exclusion list and re-commit.

### 5. Create the Cron Job

Use `cronjob` tool with `no_agent=true` and `script=<filename>`:
```
schedule: "every 12h"  (or "every 6h", "0 9 * * *", etc.)
script: "backup.sh"     (relative to ~/.hermes/scripts/)
no_agent: true          (script-only, no LLM overhead)
```

### 6. Verify

Run the script manually first, confirm the push succeeds, then create the cron job.

## Pitfalls

- **GitHub Push Protection**: scans binary files for tokens. Exclude any `.db` that might contain secrets.
- **Token in repo URL**: embed the PAT in the clone URL for HTTPS pushes when SSH port 22 is blocked. Format: `https://ghp_TOKEN@github.com/user/repo.git`
- **Empty repo first push**: use `git update-ref -d HEAD` (not `git reset HEAD~1`) when the repo has no prior commits.
- **Script path for cron**: must be a bare filename relative to `~/.hermes/scripts/`, not an absolute path.
