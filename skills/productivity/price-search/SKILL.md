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

1. **NEVER limit to one site** — Search ALL available sites, not just the first result. Present results from every site that returns data.
2. **Always compare prices** — Show: lowest price, average price, highest price. Make the comparison visual.
3. **Evaluate quality & trust** — For each result, note: product condition (new/used/stock), warranty status, seller reliability/reputation.
4. **Give personal recommendations** — Always end with YOUR recommendation: which option offers the best value, considering price + quality + trust. Don't just list — advise.
5. **Price is #1 priority** — The user cares most about getting the best deal. Always highlight the cheapest viable option.
6. **Don't stop at one search** — If the first query doesn't find enough results, try alternative search terms (e.g., "i5-4570" vs "اینتل 4570" vs "پردازنده 4570").

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

## Category Detection

The script auto-detects query category and selects appropriate sites:
- **car** keywords: پراید, پژو, سمند, تیبا, 206, 405, خودرو, etc.
- **motorcycle** keywords: موتور, هوندا, یاماها, CG125, ویو, etc.
- **general** (default): everything else

## Supported Sites

### E-commerce (general)
| Site | Method | Status |
|------|--------|--------|
| digikala.com | Playwright | ✅ Best coverage, JS-heavy |
| basalam.com | **API direct** | ✅ Fastest, no browser needed |
| technolife.com | Playwright | ✅ Electronics/laptops |
| digistyle.com | Playwright | ✅ Fashion/beauty |
| sodamarket.com | Playwright | ✅ General |
| modiseh.com | Playwright | ✅ Fashion/clothing |
| torob.com | Playwright | ⚠️ CAPTCHA from cloud IPs |

### Car & Motorcycle
| Site | Method | Status |
|------|--------|--------|
| divar.ir | Playwright | ✅ Cars + motorcycles (city-specific URLs) |
| bama.ir | Playwright | ✅ Iran's largest car marketplace |
| khodro45.com | Playwright | ✅ Car listings |
| khodrobank.com | Playwright | ✅ Car prices & reviews |
| hamrah-mechanic.com | Playwright | ✅ Car marketplace |

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
