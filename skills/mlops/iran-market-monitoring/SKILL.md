---
name: iran-market-monitoring
description: "Multi-source Iranian market monitoring + war alerts."
tags: [iran, market, monitoring, gold, currency, crypto, oil, cron, telegram, alerts]
---

# Iran Market Monitoring — Multi-Source Financial Alerts

Comprehensive financial market monitoring for Iranian markets with automated cron jobs. Covers gold, currency, crypto, oil prices, and geopolitical alerts from multiple web sources and Telegram channels.

## When to Use

- User wants automated market price monitoring with alerts
- User asks for "قیمت بازار", "مانیتورینگ طلا/دلار", "هشدار قیمت"
- Setting up cron jobs for financial monitoring
- Need multi-source price aggregation (not single-site)
- Monitoring Telegram channels for breaking news/analysis

## Core Principles (MANDATORY)

### 1. MULTI-SOURCE ONLY — Never rely on a single site
- **Gold/Coin:** iranijib.ir (primary), talasea.ir, mesghal.com, tgju.org
- **Currency/USDT:** bonbast.com, tgju.org, bestchange.com
- **Crypto:** CoinMarketCap API, CoinDesk API
- **Oil:** oilprice.com, reuters.com
- **War/Conflict:** 8 Telegram channels via t.me web interface
- **Market Analysis:** 4 Telegram channels (@talasea_ir, @ecoshariff, @se_pz, @eco_roozbeh)

### 2. AGGREGATE & MEDIAN — Take median/average of available sources
- More reliable than any single source
- Handles site outages, stale data, or outliers

### 3. PLAYWRIGHT FOR JS-HEAVY IRANIAN SITES
- iranijib.ir, tgju.org, bonbast.com, talasea.ir require Playwright
- Use `/tmp/pw-browsers/` for browser cache (disk space)
- `wait_until="domcontentloaded"` not `"networkidle"`

### 4. DIRECT API WHERE AVAILABLE
- CoinMarketCap, CoinDesk, Basalam API — no browser needed
- Faster and more reliable

### 5. CURRENCY UNITS — CRITICAL
- 1 Toman = 10 Rial
- Most Iranian sites show **Toman** but some show **Rial**
- ALWAYS verify unit before reporting
- Convert Rial → Toman (divide by 10) for display
- Default assumption: Toman, but FLAG uncertainty

### 6. ALERT THRESHOLDS
- Gold/Coin/Currency: >5% change vs last stored value
- Oil: >3% daily change
- War/Conflict: Missile strikes, military engagement, Iran-direct threats
- Only alert on threshold breach — SILENT otherwise

### 7. TELEGRAM CHANNEL MONITORING
- Use t.me/channelname web interface with Playwright
- Fetch last ~20 messages per channel
- Track message IDs to avoid duplicates
- Filter for SERIOUS content only (not routine political news)

### 8. PERSISTENT STATE
- Save last prices to `/data/.hermes/market_prices.json`
- Save last Telegram message IDs to `/data/.hermes/telegram_alert_state.json`
- Save talasea gold prices to `/data/.hermes/talasea_gold_prices.json`

## Cron Job Architecture

| Job ID | Name | Schedule | Sources |
|--------|------|----------|---------|
| `11d3ff670878` | Market Price Monitoring | Every 3h | 8 web sources + 4 Telegram analysis channels |
| `eba28df13194` | Gold Alert - talasea.ir | Every 30m | talasea.ir (gold only, 5% threshold) |
| `3eaeabca4dae` | Middle East War Alert | Every 3h | 8 Telegram war/news channels |

## Telegram Channels by Category

### War/Conflict (8 channels)
- @iranintltv, @km_ap, @ne_wg, @tasnimnews
- @tabzlive, @alibk3, @farsna, @khabari_18

### Market Analysis (4 channels)
- @talasea_ir, @ecoshariff, @se_pz, @eco_roozbeh

## Keywords for War Alerts (High Confidence Only)
- **Missile/Attack:** موشک، راکت، پهپاد، درون، حملات، هدف‌گذاری
- **Military Engagement:** درگیری، جنگ، تهاجم، عملیات نظامی
- **Iran-Direct:** ایران، تسه‌های هسته‌ای، نیروها، سپاه، ارتش
- **Escalation:** اخطار، هشدار، هوانوردی، حاملات جنگی، تنش بالا
- **Regional Powers:** اسرائیل، آمریکا، حزب‌الله، حوفی‌ها، سوریه، لبنان، عراق، یمن

## Pitfalls & Lessons Learned

1. **DON'T modify Hermes default config** (model.context_length, agent.max_turns, compression.threshold, etc.) unless explicitly asked. User explicitly forbids this.

2. **Date accuracy matters** — User caught 1403 vs 1405 error. Always use current Persian date.

3. **Price unit verification** — Mesghal.com shows prices in Rial per gram but labels "تومان". Always cross-check.

4. **Single-source failure** — User frustrated when only Basalam results shown. ALWAYS search all sites in category.

5. **Category-first** — Detect product category FIRST, then search ONLY relevant sites. Never search car sites for computer parts.

6. **Telegram web interface** — t.me/channelname works with Playwright for public channels. No API token needed.

7. **Silent mode default** — Cron jobs should only message on alerts. No "nothing to report" messages.

8. **Playwright timeouts** — Iranian sites slow. Use 60s timeout, domcontentloaded, 5s wait after load.

## Related Skills

- `price-search` — For product-specific price searches (shopping)
- `hermes-agent` — For cron job management commands