# Cron Job Configurations — iran-market-monitoring

## Active Cron Jobs (as of 2026-07-26)

### 1. Market Price Monitoring
- **Job ID:** `11d3ff670878`
- **Name:** Market Price Monitoring
- **Schedule:** `every 3h` (every 180 minutes)
- **Skill:** `price-search`
- **Next Run:** 2026-07-27T00:23:38.608542+00:00
- **Status:** scheduled/enabled

**Sources (Web):**
- https://www.iranjib.ir/showgroup/23/realtime_price/ (primary)
- https://talasea.ir/
- https://mesghal.com/
- https://www.tgju.org/profile/price_gold_18
- https://www.tgju.org/profile/price_gold_24
- https://bonbast.com/
- https://www.tgju.org/profile/price_dollar_rl
- https://www.tgju.org/profile/price_usdt_rl
- https://bestchange.com/
- https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=20&sortBy=market_cap&sortType=desc&convert=USD
- https://api.coindesk.com/v1/bpi/currentprice.json
- https://www.oilprice.com/
- https://www.reuters.com/markets/commodities/

**Sources (Telegram - Market Analysis):**
- @talasea_ir → https://t.me/talasea_ir
- @ecoshariff → https://t.me/ecoshariff
- @se_pz → https://t.me/se_pz
- @eco_roozbeh → https://t.me/eco_roozbeh

**Sources (News for Alerts):**
- https://www.reuters.com/world/middle-east/
- https://www.aljazeera.net/where/middle-east

**Alert Conditions:**
- Gold/Coin/Currency: >5% change vs last stored
- Oil: >3% daily change
- Middle East war/conflict news
- Telegram channels signal major move

**State File:** `/data/.hermes/market_prices.json`

---

### 2. Gold Price Alert — talasea.ir
- **Job ID:** `eba28df13194`
- **Name:** Gold Price Alert - talasea.ir
- **Schedule:** `every 30m`
- **Skill:** `price-search`
- **Next Run:** 2026-07-26T23:18:56.849187+00:00
- **Status:** scheduled/enabled

**Source:** https://talasea.ir/ (Playwright scraping)

**Monitors:**
- 18k gold per gram
- 24k gold per gram
- Mesghal gold
- Ounce gold
- Coin prices (if available)

**Alert Threshold:** >5% change on ANY gold price

**State File:** `/data/.hermes/talasea_gold_prices.json`

---

### 3. Middle East War/Conflict Alert
- **Job ID:** `3eaeabca4dae`
- **Name:** Middle East War/Conflict Alert - Telegram Channels
- **Schedule:** `every 3h`
- **Skill:** `price-search`
- **Next Run:** 2026-07-27T02:00:09.870128+00:00
- **Status:** scheduled/enabled

**Telegram Channels (8):**
1. @iranintltv → https://t.me/iranintltv
2. @km_ap → https://t.me/km_ap
3. @ne_wg → https://t.me/ne_wg
4. @tasnimnews → https://t.me/tasnimnews
5. @tabzlive → https://t.me/tabzlive
6. @alibk3 → https://t.me/alibk3
7. @farsna → https://t.me/farsna
8. @khabari_18 → https://t.me/khabari_18

**High-Confidence Keywords:**
- Missile/Attack: موشک، راکت، پهپاد، درون، حملات، هدف‌گذاری
- Military: درگیری، جنگ، تهاجم، عملیات نظامی
- Iran-Direct: ایران، تسه‌های هسته‌ای، نیروها، سپاه، ارتش
- Escalation: اخطار، هشدار، هوانوردی، حاملات جنگی، تنش بالا
- Regional: اسرائیل، آمریکا، حزب‌الله، حوفی‌ها، سوریه، لبنان، عراق، یمن

**State File:** `/data/.hermes/telegram_alert_state.json`

---

### 4. Hermes Backup to GitHub (Existing)
- **Schedule:** Every 12h
- **Script:** `/data/.hermes/scripts/backup.sh`
- **Repo:** https://github.com/nimah12/hermesbackup
- **Excludes:** state.db (contains GitHub PATs)

---

## Management Commands

```bash
# List all cron jobs
hermes cronjob list

# View specific job
hermes cronjob list --job-id 11d3ff670878

# Run job manually
hermes cronjob run --job-id 11d3ff670878

# Pause/Resume
hermes cronjob pause --job-id 11d3ff670878
hermes cronjob resume --job-id 11d3ff670878

# Update job
hermes cronjob update --job-id 11d3ff670878 --prompt "new prompt"

# Remove job
hermes cronjob remove --job-id 11d3ff670878
```

---

## Playwright Setup (Required)

```bash
pip install playwright
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers playwright install chromium
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers playwright install-deps chromium
```

**CRITICAL:** Browser cache MUST go to `/tmp/pw-browsers/` — `/data` partition is only 434MB.