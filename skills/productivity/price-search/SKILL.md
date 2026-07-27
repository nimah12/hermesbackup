---
name: price-search
description: "Search Iranian e-commerce for product prices via Playwright."
tags: [price, search, shopping, iran, digikala, basalam, car, motorcycle]
---

# Price Search — Iranian E-Commerce & Marketplaces

Search Iranian e-commerce sites, car markets, and motorcycle listings for prices.
Uses Playwright for browser-based sites + direct API for Basalam.

## When to Use

- User asks for the price of a product (any category)
- User asks to compare prices across Iranian stores
- User says "قیمت X رو پیدا کن" or "X رو بگرد"
- User asks about car, motorcycle, or auto part prices

## User's Price-Search Rules (MANDATORY)

The user (Nima) has explicitly requested these rules. Follow ALL of them every time:

1. **NEVER limit to one site** — Search ALL available sites in the correct category, not just the first result. Present results from every site that returns data. The user was VERY frustrated when I kept showing only Basalam results.
2. **CATEGORY-FIRST approach** — Detect the product category FIRST, then ONLY search sites in that category. Never search car sites for computer parts or vice versa. See "Site Categorization" below.
3. **Always compare prices** — Show: lowest price, average price, highest price. Make the comparison visual.
4. **Evaluate quality & trust** — For each result, note: product condition (new/used/stock), warranty status, seller reliability/reputation.
5. **Give personal recommendations** — Always end with YOUR recommendation: which option offers the best value, considering price + quality + trust. Don't just list — advise.
6. **Price is #1 priority** — The user cares most about getting the best deal. Always highlight the cheapest viable option.
7. **Always provide links** — The user wants clickable links to the products/pages found. Include URLs in results.
8. **Don't stop at one search** — If the first query doesn't find enough results, try alternative search terms (e.g., "i5-4570" vs "اینتل 4570" vs "پردازنده 4570").
9. **Language** — User prefers Persian (Farsi). Respond in Persian.
10. **CRITICAL: Currency units** — 1 Toman = 10 Rial. Most Iranian sites show prices in Toman. NEVER mix up Toman and Rial. If a site shows Rial, convert to Toman for display (divide by 10). Always verify the unit before reporting to the user.
11. **MINIMUM 10 sites per product** — The user explicitly requested at least 10 sites per product search. If one site blocks you, move to the next. Don't stop early. The user listed required sites: Digikala, Emalls, Sheypoor, Divar, Snapp, Tapsi, Torob, eSAm, Computer Parsian, Zoomit.
12. **Show results from ALL sites** — Don't default to just Basalam. Present results from EVERY site that returns data. The user was very frustrated when only Basalam results were shown.

## Setup (one-time)

```bash
pip install playwright
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers playwright install chromium
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers playwright install-deps chromium
```

**CRITICAL**: Browser cache MUST go to `/tmp/pw-browsers/` — `/data` is only 434MB.

## Usage

```bash
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers python3 /data/.hermes/scripts/price_search.py "<search query>"
```

Output: JSON with `category` (car/motorcycle/general), `query`, and `results` sorted by price.

## Optimizations Learned (Session Notes)

### Performance Fixes for Playwright Script
- **Timeout issues**: The original script timed out at 180-300s. Fixes applied:
  - Use `wait_until="domcontentloaded"` instead of `"networkidle"` (much faster)
  - Set page timeout to 30s max, not 60s+
  - Add `ignore_https_errors=True` to browser context
  - Disable images: `context = await browser.new_context(ignore_https_errors=True)` then block image loading via route
- **Parallelize**: Search multiple sites concurrently using `asyncio.gather()` — don't wait for each sequentially
- **Basalam API**: Use direct API (no browser needed) — 10x faster, no timeouts
- **Divar**: New class-based selectors (`kt-post-card__title`, `kt-post-card__description`) work reliably
- **Bama/Khodro45**: These block cloud IPs. Use API endpoints if available, else skip gracefully

### Category-First Search Pattern (MANDATORY)
```python
# 1. DETECT category from query
category = detect_category(query)  # car / motorcycle / general

# 2. SELECT sites for that category ONLY
sites = CATEGORY_SITES[category]  # Never mix categories

# 3. SEARCH all sites in parallel
results = await asyncio.gather(*[search_site(site, query) for site in sites])

# 4. FILTER: keep only valid results (price > 0, has link)
# 5. SORT by price, show min/avg/max, recommend best value
```

### Currency Detection — Hard Rules
- **Basalam API**: Always Toman (explicit in docs)
- **Divar**: Always shows "تومان" explicitly
- **Sheypoor**: NO unit shown — MUST check product page or flag uncertainty
- **Digikala**: NO unit shown — assume Toman (modern Iranian e-commerce standard)
- **Default**: If no unit visible, assume Toman but FLAG: "⚠️ واحد پول نمایش داده نشده — احتمالاً تومان"

### Minimum 10 Sites Enforcement
The script MUST attempt at least 10 sites per query. If a site fails/times out:
1. Log the failure
2. Move to next site immediately
3. Continue until 10+ successful results or all sites exhausted
4. Report which sites failed to the user

### Car/Motorcycle Specific
- **Divar**: Use city-specific URLs: `https://divar.ir/s/tehran/car` or `.../motorcycle`
- **Bama**: Requires search input interaction — no direct URL. Try API first.
- **Khodro45**: Try `https://khodro45.com/car/{brand}/{model}` pattern
- **Basalam**: Returns parts/accessories mostly, not full vehicles — label clearly

## Category Detection

The script auto-detects query category and selects appropriate sites:
- **car** keywords: پراید, پژو, سمند, تیبا, 206, 405, خودرو, etc.
- **motorcycle** keywords: موتور, هوندا, یاماها, CG125, ویو, etc.
- **general** (default): everything else

## Site Categorization (CRITICAL)

The user explicitly asked: "وقتی بهت میگم برو قیمت قطعات کامپیوتر دربیار دیگه تو سایت خودرو یا سایتایی که ربطی ندارن دنبال قیمت نگرد"

**Detect category FIRST, then search ONLY relevant sites:**

| Category | Sites to Search | DO NOT Search |
|----------|----------------|---------------|
| 🖥️ Computer/Laptop | digikala, basalam, sheypoor, sodamarket, technolife, torob | car sites |
| 🚗 Cars | divar, bama, khodrobank, hamrah-mechanic, khodro45 | shop sites |
| 🏍️ Motorcycles | divar, bama, khodro45 | shop sites |
| 📱 Mobile/Tablet | digikala, basalam, mobile.ir | car sites |
| 👗 Fashion | modiseh, digistyle | car sites |
| 🏠 Home/Kitchen | digikala, basalam | car sites |
| 💄 Cosmetics | digikala, basalam | car sites |
| 📚 Books | digikala, nashr.com | car sites |
| 🔧 Tools/Industrial | digikala, bazargan.com | car sites |
| 🚗 Auto Parts | khodro45, basalam, sheypoor | shop sites |
| 🎮 Gaming | digikala, basalam | car sites |
| 💎 Gold/Coin | tala.ir, mesghal.com, bonbast.com | — |
| 💵 Currency/USD | bonbast.com, bestchange.ir | — |
| ₿ Crypto | coindesk.com, coinmarketcap.com | — |
| 🛢️ Oil | oilprice.com, reuters.com | — |

**Auto-detect keywords:**
- car: پراید, پژو, سمند, تیبا, 206, 405, خودرو, BMW, etc.
- motorcycle: موتور, هوندا, یاماها, CG125, ویو, etc.
- computer: کارت گرافیک, مادربرد, پردازنده, RAM, SSD, CPU, GPU, etc.
- mobile: گوشی, آیفون, سامسونگ, etc.
- general: everything else → search ALL e-commerce sites

## Supported Sites

### E-commerce (general)
| Site | Method | Status |
|------|--------|--------|
| digikala.com | Playwright | ✅ Best coverage, JS-heavy |
| basalam.com | **API direct** | ✅ Fastest, no browser needed |
| sheypoor.com | Playwright | ✅ Classifieds, verify currency unit |
| divar.ir | Playwright | ✅ Classifieds, prices in Toman |
| technolife.com | Playwright | ✅ Electronics/laptops |
| sodamarket.com | Playwright | ✅ General |
| modiseh.com | Playwright | ✅ Fashion/clothing |
| bazargan.com | Playwright | ✅ Industrial/tools |
| nashr.com | Playwright | ✅ Books |
| mobile.ir | Playwright | ✅ Mobile phones |
| zoomit.ir | Playwright | ✅ Tech news/comparison |
| parsiancomputer.com | Playwright | ✅ Computer parts |
| esam.ir | Playwright | ✅ Electronics marketplace |
| torob.com | Playwright | ⚠️ CAPTCHA from cloud IPs |
| emalls.ir | Playwright | ⚠️ SSL issues, sometimes works |
| snapp.market | Playwright | ⚠️ Grocery, limited electronics |
| **snapp.shop** | Playwright | ⚠️ Snapp's shop platform, growing electronics |
| **tapsi.shop** | Playwright | ⚠️ Tapsi's shop platform, newer player |

### Car & Motorcycle
| Site | Method | Status |
|------|--------|--------|
| divar.ir | Playwright | ✅ Cars + motorcycles (city-specific URLs) |
| bama.ir | Playwright | ✅ Iran's largest car marketplace |
| khodro45.com | Playwright | ✅ Car listings |
| khodrobank.com | Playwright | ✅ Car prices & reviews |
| hamrah-mechanic.com | Playwright | ✅ Car marketplace |
| **motoriran.com** | Playwright | ✅ Motorcycle parts/specifications |
| **iribike.com** | Playwright | ✅ Motorcycle marketplace |

### Blocked / Deprecated
| Site | Issue |
|------|-------|
| torob.com | CAPTCHA/timeout from cloud server IPs |
| emalls.ir | SSL certificate expired |
| bamilo.com | SSL issues |
| bigmart.co | Access Denied (anti-bot) |
| shenoto.com | Now a podcast site, no longer classifieds |

## Key Technical Details

### Basalam API (no browser needed!)
```
GET https://services.basalam.com/web/v1/search/product/search?from=0&q=<encoded>&size=10
Headers: Origin: https://basalam.com, Referer: https://basalam.com/
Response: { products: [{ name, price, vendor: { name } }] }
```
This is faster and more reliable than browser scraping.

### Persian Numerals
Prices use فارسی digits (۰۱۲۳۴۵۶۷۸۹). Auto-converted via:
```python
PERSIAN_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
```

### Price Extraction Patterns
- **Digikala**: prices as `۱۳,۷۰۰,۰۰۰` (no "تومان"). Regex: `([\d,]{7,})`
- **Divar**: format `نام | کیلومتر | قیمت تومان`. Regex: `([\d,]{7,})\s*تومان`
- **Basalam**: JSON `price` field in API response

## Pitfalls

- **CRITICAL: Currency unit confusion** — I repeatedly wrote Rial prices as Toman. The user was EXTREMELY frustrated (used angry emojis). 1 Toman = 10 Rial. Most Iranian sites use Toman, BUT some (especially Sheypoor, older classifieds) may use Rial without showing the unit. ALWAYS verify the unit before reporting. If uncertain, check the product page directly. Default to Toman but FLAG uncertainty.
- **CRITICAL: Never modify Hermes default config** — User explicitly forbids touching `model.context_length`, `agent.max_turns`, `compression.threshold`, etc. Changing `model.context_length` broke things previously. Only modify config when explicitly asked.
- **CRITICAL: Always verify current date before reporting prices** — I reported "1403" instead of actual "1405". ALWAYS check system date or page timestamp before writing any date in responses.
### Pitfalls

- **CRITICAL: Currency unit confusion** — I repeatedly wrote Rial prices as Toman. The user was EXTREMELY frustrated (used angry emojis). 1 Toman = 10 Rial. Most Iranian sites use Toman, BUT some (especially Sheypoor, older classifieds) may use Rial without showing the unit. ALWAYS verify the unit before reporting. If uncertain, check the product page directly. Default to Toman but FLAG uncertainty.
- **CRITICAL: Never modify Hermes default config** — User explicitly forbids touching `model.context_length`, `agent.max_turns`, `compression.threshold`, etc. Changing `model.context_length` broke things previously. Only modify config when explicitly asked.
- **CRITICAL: Always verify current date before reporting prices** — I reported "1403" instead of actual "1405". ALWAYS check system date or page timestamp before writing any date in responses.
- **CRITICAL: Use tgju.org as PRIMARY source for live market prices** — mesghal.com shows daily snapshots (may be stale). tgju.org updates in real-time (seconds). For market monitoring cron, use tgju.org profiles via curl (no JS needed).
- **CRITICAL: Minimum 10 sites per product search** — User explicitly listed required sites. If one site fails/times out, move to next immediately. Don't stop early. Report which sites failed.
- **USER FRUSTRATION: Only showing Basalam results** — Search ALL sites in category, present results from EVERY site that returns data.
- **USER FRUSTRATION: Wrong category searches** — Detect category FIRST, then ONLY search relevant sites.
- **USER FRUSTRATION: No clickable links** — The user wants clickable links to products. Always include URLs.
- **CRITICAL: Wrong dates in price reports** — Session 2026-07-26: I reported mesghal.com data as "5 Mordad 1403" when it was actually 1405. The user was furious (😡😡😡). ALWAYS verify the date on the source page before reporting. Use tgju.org which shows correct Jalali dates.
- **CRITICAL: Wrong price source** — mesghal.com showed stale/old prices (14,800,000 Rial = 1,480,000 Toman for 18k gold) while tala.ir showed correct 17,878,900 Toman. Cross-reference multiple sources. tgju.org and tala.ir are more reliable for gold/currency.
- **CRITICAL: Date verification** — Before reporting ANY price, check the page's displayed date. The share link https://share.google/5PuM49weUHtgTI3u6 showed "آخرین به روز رسانی در تاریخ دوشنبه، ۵ مرداد ۱۴۰۵" — always include this in reports.
- **Torob CAPTCHA/timeout**: From certain IPs (cloud servers), Torob blocks completely. Report as غیردسترس.
- **digikala timeouts**: Use `wait_until="domcontentloaded"` not `"networkidle"`.
- **Divar car URL**: Must use `https://divar.ir/s/tehran/car` (city-specific).
- **Bama search**: Needs to type into search input and press Enter, not direct URL.
- **Basalam**: Returns parts/accessories, not always the full vehicle. Digikala has new vehicle listings.
- **Emalls SSL**: Certificate expired, skip entirely.
- **Shenoto**: Now a podcast/audio platform, no longer classifieds. Skip.
- Use `ignore_https_errors=True` for all Playwright contexts.
- **Disk space**: Playwright browsers MUST go to `/tmp/pw-browsers/` — `/data` partition is only 434MB.
- **Search terms**: Try multiple variations — English model numbers + Persian descriptions yield different results.
- **Car sites**: Basalam returns parts, not full vehicles. For actual cars, use Divar/Bama/Khodro45.
- **Persian numerals**: All Iranian sites use فارسی digits. Always convert before price parsing.
- **Currency detection**: Check each price line for "تومان" or "ریال". Default assumption is Toman. Convert Rial to Toman (÷10) for display.
- **Market monitoring**: A cron job runs every 4 hours checking gold, coin, USD, oil prices and Middle East news. Alert user if >5% fluctuation or major news event.

### Performance Optimizations (Session 2026-07-27)

- **Playwright timeout issues**: Original script timed out at 180-300s. Fixes applied:
  - Use `wait_until="domcontentloaded"` instead of `"networkidle"` (much faster)
  - Set page timeout to 30s max, not 60s+
  - Add `ignore_https_errors=True` to browser context
  - Disable images: block image loading via route interception
- **Parallelize**: Search multiple sites concurrently using `asyncio.gather()` — don't wait for each sequentially
- **Basalam API**: Use direct API (no browser needed) — 10x faster, no timeouts
  - Endpoint: `https://services.basalam.com/web/v1/search/product/search?from=0&q=<encoded>&size=10`
  - Headers: `Origin: https://basalam.com`, `Referer: https://basalam.com/`
- **Divar selectors**: New class-based selectors work reliably: `kt-post-card__title`, `kt-post-card__description`
- **Bama/Khodro45**: These block cloud IPs. Try API endpoints if available, else skip gracefully
- **Cron job reliability**: Convert failing LLM+Playwright crons to direct Python scripts (`no_agent=true`) for reliability

### Key Technical Patterns (Session 2026-07-27)

- **IranJib price extraction**: Use specific HTML IDs (`f_83_63_pr`, `f_84_63_pr`, `f_85_63_pr`, `f_127_63_pr`, `f_87_63_pr`, `f_89_63_pr`, `f_90_63_pr`, `f_92_63_pr`, `f_19054_127_pr`, `f_6370_127_pr`, `f_8652_68_pr`, `f_8653_68_pr`, `f_17624_68_pr`, `f_8277_127_pr`, `f_6371_127_pr`, `f_6372_127_pr`) — prices are in Rial, divide by 10 for Toman
- **Tala.ir API**: `https://www.tala.ir/api/v1/live-price` returns structured JSON with gold/coin prices
- **CoinGecko API**: Free crypto prices — `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,binancecoin,solana,ripple&vs_currencies=usd&include_24hr_change=true`
- **Telegram channel monitoring**: Use `t.me/s/<channel>` for public channel scraping (no auth needed)
- **Worldometer for Tehran time**: `https://www.worldometers.info/time/tehran-iran/` — extract from `serverTime` prop in live clock component

## Reference Files

- `references/tgju-api.md` — **tgju.org API patterns** — Tehran Gold & Currency Exchange real-time prices (PRIMARY SOURCE for gold/currency)
- `references/session-notes.md` — Session notes including Playwright setup, user preferences, and critical config warning
- `references/session-2026-07-26-car-search-patterns.md` — Working selectors, API endpoints, and patterns for car searches (Divar, Basalam API, Bama, Khodro45). Includes July 2026 selectors for Divar (`kt-post-card__title`, `kt-post-card__description`).
- `references/site-status.md` — Current status of all Iranian e-commerce/car sites with URL patterns and selectors
- `references/market-monitoring.md` — Financial market monitoring patterns (gold, currency, crypto, oil, ME news)
- `references/basalam-api.md` — Basalam API documentation (direct API, no browser needed)
- `references/session-2026-07-26-lessons.md` — Lessons learned from car search session
- `references/session-2026-07-27-comprehensive.md` — **Comprehensive session learnings: date verification, currency rules, site categorization, cron jobs, Telegram channels, Playwright optimizations, iPhone 17 research, user preferences, pitfalls**
