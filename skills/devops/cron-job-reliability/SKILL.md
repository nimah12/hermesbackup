---
name: cron-job-reliability
description: "Use no_agent Python scripts for cron; LLM agents timeout."
category: devops
triggers:
  - "cron job timeout"
  - "provider timeout"
  - "LLM agent cron failure"
  - "reliable scheduled scraping"
  - "market data cron"
  - "Telegram channel monitoring cron"
---

# Cron Job Reliability Patterns

## Core Principle

**LLM Agents + Playwright in cron jobs = unreliable**. Use `no_agent=true` with direct Python scripts instead.

## When to Use Each Approach

| Scenario | Approach | Why |
|----------|----------|-----|
| Scheduled scraping (every 5m-3h) | `no_agent=true` + Python script | No LLM latency, no provider timeout, deterministic |
| One-off complex analysis | LLM Agent + tools | Needs reasoning, not just data fetch |
| Conditional logic based on content | LLM Agent | Requires interpretation |
| Simple threshold alerts | `no_agent=true` + Python | Pure numeric comparison |

## Reliable Cron Job Template

```yaml
# cronjob create
action: create
no_agent: true
script: my_script.py          # Place in ~/.hermes/scripts/
enabled_toolsets: ["terminal", "file"]
schedule: "every 3h"
deliver: "origin"              # or "local" for silent
```

## Direct Python Script Pattern

```python
#!/usr/bin/env python3
import asyncio
import aiohttp
import json
from datetime import datetime, timezone, timedelta

STATE_FILE = "/data/.hermes/my_state.json"
THRESHOLD = 5.0

def load_state(): ...
def save_state(data): ...
async def fetch(session, url): ...
async def main():
    old = load_state()
    async with aiohttp.ClientSession() as session:
        data = await fetch_source(session)
    alerts = check_thresholds(old, data)
    save_state({"data": data, "last": now()})
    if alerts:
        print("---ALERTS_JSON_START---")
        print(json.dumps(alerts))
        print("---ALERTS_JSON_END---")
```

## Iran Market Data Sources (Verified Working)

| Source | Method | Key Data | Notes |
|--------|--------|----------|-------|
| **IranJib** | HTML parse (specific IDs) | Gold, coins, USD, EUR, USDT, BTC, Brent, WTI | IDs: `f_85_63_pr` (18k), `f_87_63_pr` (coin new), `f_19054_127_pr` (USDT), `f_6371_127_pr` (Brent) |
| **Tala.ir API** | JSON API | Gold 18k/24k, mesghal, coins | `https://www.tala.ir/api/v1/live-price` |
| **CoinGecko** | JSON API | BTC, ETH, USDT, BNB, SOL, XRP in USD | Free, no key, include_24hr_change |
| **Telegram channels** | t.me/s/ HTML parse | @se_pz, @talasea_ir prices | Parse `tgme_widget_message_text` divs |

## IranJib ID Mapping (Critical)

```python
ID_MAP = {
    "f_83_63_pr": ("gold_ounce_usd", 1),
    "f_84_63_pr": ("mesghal_toman", 10),      # Rial -> Toman
    "f_85_63_pr": ("gold_18k_toman", 10),
    "f_127_63_pr": ("gold_24k_toman", 10),
    "f_86_63_pr": ("silver_ounce_usd", 1),
    "f_87_63_pr": ("coin_full_new_toman", 10),
    "f_88_63_pr": ("coin_full_old_toman", 10),
    "f_89_63_pr": ("coin_half_toman", 10),
    "f_90_63_pr": ("coin_quarter_toman", 10),
    "f_92_63_pr": ("coin_1gram_toman", 10),
    "f_19054_127_pr": ("usdt_toman", 1),
    "f_8652_68_pr": ("usd_remittance_toman", 1),
    "f_8653_68_pr": ("eur_remittance_toman", 1),
    "f_17624_68_pr": ("aed_remittance_toman", 1),
    "f_8277_127_pr": ("btc_usd", 1),
    "f_6371_127_pr": ("brent_usd", 1),
    "f_6372_127_pr": ("wti_usd", 1),
}
```

## State Persistence Pattern

```python
STATE_FILE = "/data/.hermes/market_prices.json"

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

## Alert Output Format (for cron delivery)

```python
if alerts:
    print("---ALERTS_JSON_START---")
    print(json.dumps(alerts, ensure_ascii=False))
    print("---ALERTS_JSON_END---")
# Cron delivers this JSON as message
```

## Common Pitfalls Fixed

| Pitfall | Fix |
|---------|-----|
| LLM Agent timeout in cron | Use `no_agent=true` + direct script |
| Playwright browser startup slow | Use `aiohttp` for simple HTML/JSON |
| Provider chain exhausted | Remove LLM dependency entirely |
| State lost between runs | Persist to `/data/.hermes/*.json` |
| IranJib prices in Rial | Divide by 10 for Toman |
| False alerts on metadata | Skip keys with `24h_change`, `index` |
| Telegram t.me/s/ parsing breaks | Use `tgme_widget_message_text` class divs |
| Divar car listings no prices in list | Need individual post view or API |
| Bama API returns minified JSON | Extract from embedded JSON-LD schema.org |
| Basalam API needs Origin/Referer headers | Add `Origin: https://basalam.com`, `Referer: https://basalam.com/` |

## Scripts Reference

- `scripts/market_monitor.py` — Main 3-hour market monitor (IranJib + Tala.ir + CoinGecko)
- `scripts/gold_alert_telegram.py` — 30-min Telegram channel monitor (@se_pz, @talasea_ir)
- `scripts/tehran_time_sync.py` — 5-min time sync from Worldometer (see references)
- `scripts/war_intel_monitor.py` — 3-hour war intelligence monitor (8 Iranian Telegram channels)

## Iranian Market Site Patterns (Verified)

| Site | Category | Method | Key Pattern |
|------|----------|--------|-------------|
| **IranJib** | Gold/Currency/Oil/Crypto | HTML parse (IDs) | `f_85_63_pr` = 18k gold |
| **Tala.ir** | Gold/Coin | JSON API | `/api/v1/live-price` |
| **CoinGecko** | Crypto | JSON API | `/api/v3/simple/price` |
| **Telegram** | Gold/Currency alerts | HTML parse (t.me/s/) | `tgme_widget_message_text` |
| **Basalam** | Consumer goods | JSON API | `services.basalam.com/web/v1/search/product/search` + Origin/Referer |
| **Divar** | Cars/Real estate | HTML/JSON | `api.divar.ir/v8/web-search` + schema.org |
| **Bama** | Cars | HTML/JSON | JSON-LD in page + `/api/v1/vehicles` |
| **Sheypoor** | Cars/Parts | HTML | Schema.org microdata |
| **Digikala** | Electronics | HTML/API | SSR prices in HTML |

## Category-First Search Strategy (User Preference)

**ALWAYS detect category first, then search relevant sites only:**

| Category | Sites (min 10) |
|----------|----------------|
| **Computer Parts** | digikala, basalam, sheypoor, sodamarket, technolife, torob, snapp.shop, tapsi.shop |
| **Cars** | divar, bama, khodrobank, hamrah-mechanic, khodro45 |
| **Mobile** | digikala, basalam, mobile.ir, technolife, sodamarket, snapp.shop, tapsi.shop |
| **Motorcycle Parts** | divar, bama, sheypoor, khodro45, basalam, motoriran |
| **Fashion** | modiseh, digistyle (NOT electronics) |

## Price Search Requirements (User Mandated)

- **Language**: Persian only
- **Currency**: Toman (1 Toman = 10 Rial) — NEVER mix units
- **Output**: Min/avg/max, quality evaluation, recommendation, direct links
- **Links**: Direct link to EVERY listing
- **Sites**: Minimum 10 Iranian sites per search
- **Bypass**: Try multiple methods for blocked sites

## Time Sync Cron Job

```yaml
# Separate cron for time accuracy
schedule: "every 5m"
script: tehran_time_sync.py
source: "https://www.worldometers.info/time/tehran-iran/"
output: "/data/.hermes/current_date.json"
```

---

## Support Files

| File | Purpose |
|------|---------|
| `scripts/market_monitor.py` | Main 3-hour market monitor (IranJib + Tala.ir + CoinGecko) |
| `scripts/gold_alert_telegram.py` | 30-min Telegram channel monitor (@se_pz, @talasea_ir) |
| `scripts/tehran_time_sync.py` | 5-min time sync from Worldometer |
| `scripts/test_war_intel.py` | War intelligence test for 8 Iranian Telegram channels |
| `references/iranjib_id_mapping.md` | Complete IranJib HTML ID to price key mapping |
| `references/telegram_channel_patterns.md` | Telegram channel parsing patterns and price ranges |
| `references/telegram_monitoring.md` | Telegram monitoring setup and channel list |
| `references/war_intel_test_results.md` | Test results: 29 alerts from 8 channels (2026-07-27) |

---

**Key Lesson**: Cron jobs that scrape data should be pure Python scripts with `no_agent=true`. LLM agents add latency and failure modes unsuitable for scheduled tasks.