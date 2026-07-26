# Session Lessons — July 26, 2026 (5 Mordad 1405)

## Critical Failures & Fixes

### 1. Wrong Date in Report (User Furious 😡😡😡)
- **What happened**: Reported mesghal.com data as "5 Mordad 1403" when actual date was 1405
- **Fix**: ALWAYS verify system date AND page timestamp before writing dates
- **Working source**: tgju.org share link showed "آخرین به روز رسانی در تاریخ دوشنبه، ۵ مرداد ۱۴۰۵" — include this in reports

### 2. Stale/Incorrect Prices from Wrong Source
- **mesghal.com** showed: 18k Gold = 14,800,000 Rial (1,480,000 Toman) — WRONG (stale)
- **tala.ir / tgju.org** showed: 18k Gold = 17,878,900 Toman — CORRECT (real-time)
- **Fix**: tgju.org is PRIMARY for live prices. mesghal.com is backup only.

### 3. Not Searching Enough Sites
- User demanded minimum 10 sites per product
- Only showed Basalam for Pride 111 car search
- **Fix**: Run Playwright searches on ALL category-relevant sites sequentially

### 4. Touched Hermes Config Without Permission
- Changed `model.context_length` from default to 8192
- User explicitly forbids this
- **Fix**: NEVER modify `model.context_length`, `agent.max_turns`, `compression.threshold`, etc. unless user explicitly asks

### 5. Missing Clickable Links
- User wants direct URLs for every price
- **Fix**: Include source URLs in all price reports

## Working Patterns Discovered

### tgju.org — Best for Live Market Prices
```bash
# 18k Gold per gram (RIAL)
curl -s "https://www.tgju.org/profile/geram18" | grep -oP 'class="price-value"[^>]*>\K[0-9,]+'

# USD Free Market (RIAL)
curl -s "https://www.tgju.org/profile/price_dollar_rl" | grep -oP 'class="price-value"[^>]*>\K[0-9,]+'

# USDT (RIAL)
curl -s "https://www.tgju.org/profile/price_usdt_rl" | grep -oP 'class="price-value"[^>]*>\K[0-9,]+'
```
- All prices in **RIAL** — divide by 10 for Toman
- No JS rendering needed
- Updates in real-time (seconds)

### Iranjib (iranjib.ir) — Playwright for Live Tables
```python
# Works with Playwright (chromium)
# Tables have class="items_table"
# Price rows have class="price-value" with data-price attribute
# Categories: Gold, Coin, Currency, Crypto, Oil, Metals
```

### Divar Car Search — Playwright Selectors (July 2026)
```python
# Post cards: class="kt-post-card kt-post-card--outlined"
# Title: class="kt-post-card__title"
# Description/Price: class="kt-post-card__description"
# Link: href="/v/TOKEN"
```

### Basalam API (No Browser Needed)
```bash
curl "https://services.basalam.com/web/v1/search/product/search?from=0&q=QUERY&size=15" \
  -H "Origin: https://basalam.com" -H "Referer: https://basalam.com/"
# Returns JSON with products array
```

## Market Monitoring Cron (Job ID: 11d3ff670878)
- Runs every 3 hours
- Storage: `/data/.hermes/market_prices.json`
- Sources: tgju.org (gold/currency), bestchange.com (USDT), coinmarketcap API (crypto), oilprice.com (oil)
- Alert thresholds: >5% gold/currency, >3% oil, major ME news
- Silent mode: only alert on threshold breach