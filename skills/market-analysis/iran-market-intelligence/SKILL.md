---
name: iran-market-intelligence
description: "Monitor Iran gold/currency/crypto/oil + war intel via cron."
tags: [iran, market, gold, currency, crypto, oil, war, intel, cron, monitoring]
---

# Iran Market Intelligence — Class-Level Umbrella

Unified methodology for real-time Iranian financial market monitoring and geopolitical intelligence.

## When to Use
- User asks for live gold/currency/crypto/oil prices in Iran
- Need to set up automated market monitoring with alerts
- Need war/conflict intelligence from Iranian Telegram channels
- Building cron jobs for market data collection

---

## Core Principles (User-Mandated)

### 1. Language & Currency
- **All output in Persian** — User is Iranian, speaks Persian only
- **Prices in Toman** — 1 Toman = 10 Rial. NEVER mix units. Convert Rial→Toman (÷10) on ingestion
- **Persian calendar dates** — Current: مرداد ۱۴۰۵ (July 2026)

### 2. Price Search Methodology
| Rule | Detail |
|------|--------|
| **Category-first** | Detect category → search ONLY relevant sites |
| **Min 10 sites** | Digikala, Basalam, Sheypoor, Divar, Bama, Emalls, Torob, Snapp, ParsianComputer, Zoomit, SodaMarket, Technolife, Digistyle, Khodro45, KhodroBank, Hamrah-Mechanic |
| **Direct links mandatory** | Every price entry MUST include clickable source link |
| **Min/Avg/Max + Quality** | Report range, average, quality eval, recommendation |
| **Used/stock focus** | User buys used/stock hardware (GPU, CPU, motherboard) |

### 3. Cron Job Patterns (Proven Working)
| Job | Schedule | Script | Mode |
|-----|----------|--------|------|
| Tehran Time Sync | Every 5 min | `tehran_time_sync.py` | `no_agent=true` |
| Market Monitor (Full) | Every 3h | `market_monitor.py` | `no_agent=true` |
| Gold/Telegram Alert | Every 30m | `gold_alert_telegram.py` | `no_agent=true` |
| War Intel | Every 3h | `war_intel_monitor.py` | `no_agent=true` |
| Tech News Digest | Daily 13:00 Tehran | `tech_news_digest.py` | `no_agent=true` |
| Backup to GitHub | Every 12h | `backup.sh` | `no_agent=true` |

> **Critical**: All cron jobs converted to `no_agent=true` direct Python scripts to avoid LLM+Playwright Provider timeouts (21s+ failures).

---

## Primary Data Sources

### IranJib — PRIMARY for Market Prices
| Asset | URL | **Exact HTML ID** |
|-------|-----|-------------------|
| Gold 18k | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_83_63_pr` |
| Gold 24k | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_84_63_pr` |
| Mesghal | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_86_63_pr` |
| Coin Full | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_87_63_pr` |
| Half Coin | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_88_63_pr` |
| Quarter Coin | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_89_63_pr` |
| USD | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_90_63_pr` |
| EUR | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_91_63_pr` |
| USDT | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_92_63_pr` |
| BTC | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_93_63_pr` |
| Brent | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_94_63_pr` |
| WTI | https://www.iranjib.ir/showgroup/23/realtime_price/ | `f_95_63_pr` |

**Extraction Pattern**: `id="f_XX_63_pr"[^>]*>([\d,]+)`

### TGJU — Backup/Validation
- https://www.tgju.org/profile/geram18 (Gold 18k)
- https://www.tgju.org/profile/sekee (Coin)
- https://www.tgju.org/profile/price_dollar_rl (USD)
- All TGJU prices in **Rial** → convert to Toman

### CoinGecko — Crypto
- BTC, USDT, ETH global prices in USD

### Telegram Channels — War Intel
```python
WAR_CHANNELS = [
    "iranintltv", "km_ap", "tasnimnews", "farsna",
    "tabzlive", "alibk3", "khabari_18", "ne_wg"
]
```

### Worldometer — Tehran Time
- https://www.worldometers.info/time/tehran-iran/

---

## Alert Thresholds

| Asset Class | Warning | Critical | Action |
|-------------|---------|----------|--------|
| Gold (18k, 24k, Coin) | >3% daily | >5% daily | Buy physical / coin |
| Currency (USD, EUR, USDT) | >2% daily | >5% daily | Buy USDT / crypto |
| Oil (Brent, WTI) | >$3/day | >$10/day | Hedge / short stocks |
| Tehran Stock Index | >-2% | >-5% | Reduce exposure |
| BTC Iran Premium | >10% | >20% | Sell premium / buy dip |

---

## Price Search Categories & Approved Sites

| Category | Sites (Min 10) |
|----------|----------------|
| **Computer Hardware** | Digikala, Basalam, Sheypoor, SodaMarket, Technolife, Torob, Snapp.shop, Tapsi.shop, ParsianComputer, Zoomit |
| **Vehicles** | Divar, Bama, KhodroBank, Hamrah-Mechanic, Khodro45 |
| **Mobile** | Digikala, Basalam, Mobile.ir, Technolife, SodaMarket, Snapp.shop, Tapsi.shop |
| **Fashion** | Modiseh, Digistyle (NOT electronics) |
| **Motorcycle Parts** | Divar, Sheypoor, Bama, Khodro45, Basalam, MotorIran, Digikala |

---

## Proven Extraction Scripts

### Market Monitor (`market_monitor.py`)
```python
# Extracts 24 prices from IranJib + Tala.ir + CoinGecko
# Saves to /data/.hermes/market_prices.json
# Alerts on >5% gold/currency, >3% oil
# Runs every 3h via cron 11d3ff670878 (no_agent=true)
```

### Gold Telegram Alert (`gold_alert_telegram.py`)
```python
# Monitors @se_pz and @talasea_ir only (user-specified)
# Checks last 20 messages each
# Alerts on >5% price change for gold/coin/dollar/USDT
# Silent otherwise
# Runs every 30m via cron eba28df13194 (no_agent=true)
```

### War Intel Monitor (`war_intel_monitor.py`)
```python
# Fetches 8 Telegram channels via t.me/s/ public preview
# Parses tgme_widget_message_text class
# Keyword classification: Critical/High/Medium
# Runs every 3h via cron 3eaeabca4dae (no_agent=true)
```

### Tehran Time Sync (`tehran_time_sync.py`)
```python
# Fetches Worldometer Tehran time
# Saves to /data/.hermes/current_date.json
# Runs every 5m via cron 82ebc249d760 (no_agent=true)
```

---

## Backup Strategy
- **Repo**: `nimah12/hermesbackup`
- **Schedule**: Every 12h
- **Script**: `/data/.hermes/scripts/backup.sh`
- **Excludes**: `state.db` (too large, not needed)
- **Files**: skills/, cron/, memories/, scripts/, *.json, *.md

---

## Anti-Patterns to Avoid
| ❌ Don't | ✅ Do |
|----------|-------|
| Use LLM+Playwright in cron | Use `no_agent=true` direct Python |
| Mix Rial/Toman | Convert all to Toman on ingest |
| Search all sites for every query | Category-first → relevant sites only |
| Skip direct links | **Mandatory** clickable link per price |
| Modify Hermes default config | Never touch config unless explicitly asked |

---

## References
- `references/iranjib-ids.md` — Exact HTML ID mappings
- `references/cron-patterns.md` — Proven cron job configurations
- `references/extraction-scripts/` — Ready-to-deploy Python scripts
- `references/alert-thresholds.md` — Threshold matrix with rationale

---

## Related Skills (Sub-skills)
- `price-search/motorcycle-parts-price` — Motorcycle parts pricing
- `market-analysis/tgju-market-api` — TGJU API details
- `market-analysis/iran-sanctions-war-impact` — Geopolitical impact analysis
- `intelligence/telegram-war-intel` — Telegram war intelligence
- `intelligence/tech-news-digest` — Daily tech news at 13:00 Tehran