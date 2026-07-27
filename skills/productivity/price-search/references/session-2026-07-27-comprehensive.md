# Comprehensive Session Learnings — 27 July 2026 (6 Mordad 1405)

This document captures all critical learnings, user preferences, and operational patterns from the extended session on 2026-07-27 (6 Mordad 1405).

---

## 🎯 **User Profile (Nima)**

- **Language**: Persian (Farsi) only — always respond in Persian
- **Interests**: Computer hardware (GPU, CPU, motherboard) — used/stock items in Iran
- **GitHub backup**: `nimah12/hermesbackup` — cron every 12h
- **Communication style**: Direct, frustrated by repeated mistakes, uses angry emojis when things go wrong

---

## 📅 **CRITICAL: Date Verification Protocol**

**ALWAYS verify current date before reporting ANY price or news.**

| Check | Method |
|-------|--------|
| System date | `date` command / `TZ=Asia/Tehran date` |
| Source page timestamp | Check "آخرین به‌روزرسانی" on source pages |
| Jalali conversion | Use `jdatetime` or manual calc (March 21 = 1 Farvardin) |
| Reference API | `https://api.aladhan.com/v1/gToH?date=DD-MM-YYYY&calendar=persian` |

**Session failure**: Reported mesghal.com data as "5 Mordad 1403" when actual was "5 Mordad 1405". User was furious (😡😡😡).

**Current date at session start**: 2026-07-26 UTC / 2026-07-27 03:06 +0330 = **6 Mordad 1405, Monday**

---

## 💰 **Currency Rules (Hard)**

| Rule | Detail |
|------|--------|
| **1 Toman = 10 Rial** | Never mix up |
| **Most Iranian sites** | Show prices in **Toman** (no unit shown = assume Toman) |
| **Sheypoor** | NO unit shown — MUST verify or flag uncertainty |
| **Digikala** | NO unit shown — assume Toman (modern standard) |
| **Divar** | Explicitly shows "تومان" |
| **Basalam API** | Always Toman (documented) |
| **When uncertain** | Flag: "⚠️ واحد پول نمایش داده نشده — احتمالاً تومان" |
| **If Rial detected** | Convert to Toman (÷10) for display |

**Session failure**: Repeatedly reported Rial as Toman. User extremely frustrated.

---

## 🏪 **Site Categorization (Updated)**

### Removed from Electronics/Mobile
| Site | Reason |
|------|--------|
| **Digistyle** | Fashion/beauty ONLY — never search for phones, laptops, computer parts |

### Added to Electronics/Mobile
| Site | URL Pattern | Notes |
|------|-------------|-------|
| **Snapp Shop** | `https://snapp.shop/search?q={query}` | Snapp's e-commerce, growing electronics |
| **Tapsi Shop** | `https://tapsi.shop/search?q={query}` | Tapsi's e-commerce, newer player |

### Mobile/Tablet Category Sites (Updated)
```
digikala, basalam, mobile.ir, technolife, sodamarket, snapp.shop, tapsi.shop
```

### Computer/Laptop Category Sites (Updated)
```
digikala, basalam, sheypoor, sodamarket, technolife, torob
```

---

## 🔍 **Search Strategy (Mandatory)**

### Category-First Pattern
```python
# 1. DETECT category from query
category = detect_category(query)  # car / motorcycle / mobile / computer / general

# 2. SELECT sites for that category ONLY
sites = CATEGORY_SITES[category]

# 3. SEARCH all sites in parallel (asyncio.gather)
results = await asyncio.gather(*[search_site(site, query) for site in sites])

# 4. FILTER valid results (price > 0, has link)
# 5. SORT by price, show min/avg/max, recommend best value
```

### Minimum 10 Sites Enforcement
- Attempt ≥10 sites per query
- If site fails/times out → log failure → move to next immediately
- Continue until 10+ successful OR all exhausted
- Report failed sites to user

### Multiple Search Terms
- Try variations: "i5-4570" vs "اینتل 4570" vs "پردازنده 4570"
- English model numbers + Persian descriptions yield different results

---

## ⚡ **Playwright Optimizations (Critical)**

| Issue | Fix |
|-------|-----|
| **Timeouts (180-300s)** | Use `wait_until="domcontentloaded"` not `"networkidle"` |
| **Page timeout** | 30s max, not 60s+ |
| **HTTPS errors** | `ignore_https_errors=True` in browser context |
| **Images** | Block image loading via route interception |
| **Parallelization** | `asyncio.gather()` for concurrent site searches |
| **Basalam** | Use direct API — 10x faster, no browser needed |
| **Divar selectors (Jul 2026)** | `kt-post-card__title`, `kt-post-card__description`, `href="/v/{token}"` |

### Basalam API (No Browser)
```
GET https://services.basalam.com/web/v1/search/product/search?from=0&q={encoded}&size=10
Headers: Origin: https://basalam.com, Referer: https://basalam.com/
Response: { products: [{ name, price, vendor: { name }, url }] }
```

---

## 🥇 **Primary Market Data Sources**

### Gold/Currency (Real-time)
| Source | Method | Profiles |
|--------|--------|----------|
| **tgju.org** (PRIMARY) | `curl` + simple parsing | `geram18` (18k gold/g), `price_dollar_rl` (USD), `price_usdt_rl` (USDT), `emami1`, `bahar_azadi` |
| **mesghal.com** | Playwright/curl | Daily snapshots, may be stale |
| **bonbast.com** | Playwright | IDs: #usd1, #usd2, #gol18_top, #emami1_top |
| **tala.ir** | Playwright | News + prices, daily updates |

**Rule**: tgju.org = real-time (seconds), mesghal.com = daily snapshot. Always prefer tgju.org.

### Currency Units
- tgju.org prices in **RIAL** → convert to Toman (÷10) for display
- bonbast.com in **Toman**
- bestchange.com for USDT/exchanger rates

---

## 🤖 **Cron Jobs Created This Session**

| Job ID | Name | Schedule | Purpose |
|--------|------|----------|---------|
| `11d3ff670878` | Market Price Monitoring | Every 3h (09:30 UTC) | Multi-source: gold, currency, crypto, oil, ME news |
| `eba28df13194` | Gold Alert - talasea.ir | Every 30m | 5% threshold on gold prices |
| `3eaeabca4dae` | Middle East War Alert | Every 3h | 8 Telegram channels (iranintltv, km_ap, ne_wg, tasnimnews, tabzlive, alibk3, farsna, khabari_18) |
| `d039ecf80095` | Daily Tech News Digest | Daily 13:00 Tehran (09:30 UTC) | AI, Gaming, SpaceX, General Tech from 20+ sources + 4 Telegram channels |
| `6b4de282394e` | Date Sync | Daily 00:00 Tehran (20:30 UTC) | Sync Jalali/Gregorian date to `/data/.hermes/current_date.json` |

### Telegram Channels for Market Analysis (added to Market Price Monitoring)
- @talasea_ir → https://t.me/talasea_ir
- @ecoshariff → https://t.me/ecoshariff
- @se_pz → https://t.me/se_pz
- @eco_roozbeh → https://t.me/eco_roozbeh

### Telegram Channels for War/Conflict Alerts
- @iranintltv, @km_ap, @ne_wg, @tasnimnews, @tabzlive, @alibk3, @farsna, @khabari_18

---

## 📱 **iPhone 17 Research Result**

**Fact**: iPhone 17 **NOT YET RELEASED** (expected Sept 2025 / Shahrivar 1404)

**Iran market (Basalam) shows ONLY**:
- "فول کپی" (full copy/fake) — 80M to 300M Toman
- "مینی ۴.۵ اینچ" — non-existent model
- "طرح اصل" = still fake copy

**Latest genuine iPhone in Iran**: iPhone 16 series (~110M-210M Toman with warranty)

---

## 💾 **Backup System**
- **Repo**: `https://github.com/nimah12/hermesbackup`
- **Script**: `/data/.hermes/scripts/backup.sh`
- **Cron**: Every 12 hours
- **Excludes**: `state.db` (contains GitHub PATs — triggers Push Protection)
- **Last successful**: 2026-07-26_23-06-26

---

## 🚫 **Config Prohibition (User Explicit)**

**NEVER modify Hermes default config**:
- `model.context_length`
- `agent.max_turns`
- `compression.threshold`
- `agent.tool_use_enforcement`
- Any `model.*`, `agent.*`, `compression.*`, `terminal.*` settings

**Session failure**: Changed `model.context_length` → broke things. User explicitly forbids.

---

## 📋 **Reference Files to Maintain**

| File | Purpose |
|------|---------|
| `references/site-status.md` | Current status of all Iranian sites + URL patterns + selectors |
| `references/tgju-api.md` | tgju.org API patterns for real-time gold/currency |
| `references/basalam-api.md` | Basalam direct API documentation |
| `references/market-monitoring.md` | Financial market monitoring patterns |
| `references/session-2026-07-26-car-search-patterns.md` | Car search selectors, APIs, patterns |
| `references/session-2026-07-27-comprehensive.md` | **This file** |
| `references/session-2026-07-26-lessons.md` | Previous session lessons |

---

## ✅ **Session Summary**

**What was fixed/updated**:
1. ✅ Digistyle removed from electronics/mobile categories
2. ✅ Snapp Shop & Tapsi Shop added to site lists
3. ✅ Market monitoring cron updated for multi-source + Telegram channels
4. ✅ Gold alert cron created for talasea.ir (30min, 5% threshold)
5. ✅ War/conflict alert cron created for 8 Telegram channels
6. ✅ Daily tech news digest cron created (13:00 Tehran)
7. ✅ Date sync cron created (00:00 Tehran)
8. ✅ Current date saved to `/data/.hermes/current_date.json`
9. ✅ iPhone 17 researched — confirmed not released, only fakes in Iran
10. ✅ Backup verified working

**Key behavioral rules reinforced**:
- Date verification BEFORE every price report
- Currency unit verification (Toman vs Rial)
- Category-first search (never mix car/shop sites)
- Minimum 10 sites, parallel search, report failures
- Always provide clickable links
- Personal recommendation at end
- Never touch Hermes default config

---

*Last updated: 2026-07-27 03:30 UTC (Monday, 6 Mordad 1405, 07:00 Tehran)*