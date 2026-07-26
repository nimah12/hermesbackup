# Car Search Patterns — Session 2026-07-26 (Updated Mordad 5, 1405)

## What Worked for "پراید 111" (Pride 111)

### Basalam API (✅ Fast, No Browser)
```bash
curl -sL "https://services.basalam.com/web/v1/search/product/search?from=0&q=%D9%BE%D8%B1%D8%A7%DB%8C%D8%AF%20111&size=15" \
  -H "Origin: https://basalam.com" -H "Referer: https://basalam.com/" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
```
- Returns JSON with `price` in **Toman**, `name`, `vendor.name`, `web_url`
- **Got 15 results** — mostly parts/accessories/whatnots, not full cars
- Label results clearly: "قطعات/لوازم جانبی" vs "خودروی کامل"

### Divar via Playwright (✅ Works with New Selectors)
```python
# Working selectors (July 2026)
cards:      'article.kt-post-card'  or  class="kt-post-card kt-post-card--outlined"
title:      class="kt-post-card__title"
price/desc: class="kt-post-card__description"  (shows "۳۰۰,۰۰۰ کیلومتر" — mileage, NOT price!)
link:       href="/v/{token}"

# NOTE: Divar cards show MILEAGE not PRICE in the list view!
# Price only appears on detail page. Must visit each link for price.
```

### Divar API (✅ Alternative - Works!)
```bash
# This pattern works for car searches
curl -sL "https://api.divar.ir/v8/web-search/tehran/car?json_schema=%7B%22category%22%3A%7B%22value%22%3A%22car%22%7D%7D&per_page=20" \
  -H "User-Agent: Mozilla/5.0" -H "Accept: application/json"
```
- Returns `widget_list` with `title`, `middle_description_text` (price), `token`, `location`
- **Filter locally** for "پراید" or "111" in title
- **Much faster than Playwright** — use this as primary, Playwright as fallback

### Bama (❌ Blocked Cloud IPs)
- Direct page load: Heavy JS, anti-bot
- API `https://api.bama.ir/v1/vehicle/list?vehicle=pride,111` — empty response from cloud IP
- **Recommendation**: Tell user to check https://bama.ir/car/pride/111 directly

### Khodro45 (❌ Blocked/Empty)
- Page loads but no parseable listings from cloud IP

## Working Pattern for Car Searches

```python
async def search_car(query: str):
    # 1. Divar API (primary - fast, no browser)
    divar_results = await fetch_divar_api(query)
    
    # 2. Basalam API (instant, parts/accessories)
    basalam = await fetch_basalam_api(query)
    
    # 3. Try Bama API (may fail from cloud)
    bama = await try_bama_api(query)
    
    # 4. Combine, deduplicate, sort by price
    return format_results(divar_results, basalam, bama)
```

## Selectors to Use (July 2026)

| Site | Container | Title | Price/Mileage | Link |
|------|-----------|-------|---------------|------|
| Divar | `article.kt-post-card` | `.kt-post-card__title` | `.kt-post-card__description` | `href="/v/..."` |
| Bama | Need JS interaction | N/A | N/A | N/A |

## Key Lessons

1. **Divar list view shows MILEAGE not PRICE** — must visit detail page for actual price
2. **Basalam = parts/accessories mostly** — not full vehicles
3. **Cloud IPs blocked by Bama/Khodro45** — be honest with user, give direct links
4. **Parallel execution essential** — don't await each site sequentially
5. **Timeout at 30s per site max** — use `wait_until="domcontentloaded"`
6. **Disable images** to speed up: `await page.route("**/*.{png,jpg,jpeg,webp}", lambda r: r.abort())`

## Session Update — Mordad 5, 1405 (2026-07-27)

### Divar API Working Pattern (Verified)
```python
import urllib.request, json

def search_divar_car(query, city="tehran", per_page=20):
    url = f"https://api.divar.ir/v8/web-search/{city}/car?json_schema=%7B%22category%22%3A%7B%22value%22%3A%22car%22%7D%7D&per_page={per_page}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    data = json.load(urllib.request.urlopen(req, timeout=10))
    
    results = []
    for w in data.get('widget_list', []):
        d = w.get('data', {})
        title = d.get('title', '')
        if query.lower() in title.lower() or '111' in title:
            results.append({
                'title': title,
                'price': d.get('middle_description_text', ''),  # This IS the price in Divar API!
                'location': d.get('location', ''),
                'url': f"https://divar.ir/v/{d.get('token', '')}"
            })
    return results
```

### Price Extraction from Divar API
- `middle_description_text` contains the price (e.g., "۴۵۰,۰۰۰,۰۰۰ تومان") — **NOT mileage!**
- The Playwright list view shows mileage; the API shows price. Use API for price.

### Date Accuracy — CRITICAL
- **ALWAYS verify the date from the source** (not assume current year)
- User caught me reporting "1403" instead of "1405" — shameful error
- tgju.org shows live timestamp in `last-update` span
- mesghal.com article header shows date (e.g., "دوشنبه ۵ مرداد ۱۴۰۵")

### Currency Unit Handling
- **tgju.org**: All prices in **RIAL** → divide by 10 for Toman
- **mesghal.com**: Prices in **TOMAN** (explicitly labeled)
- **bonbast.com**: Prices in **TOMAN**
- **bestchange.com**: Prices in **RIAL**
- **Divar API**: Prices in **TOMAN** (explicit "تومان" suffix)
- **Basalam API**: Prices in **TOMAN** (per docs)

### tgju.org as Primary Financial Source
- Added `references/tgju-api.md` with full patterns
- Simple curl, no Playwright, live prices
- Profiles: `geram18`, `price_dollar_rl`, `price_usdt_rl`, `emami1`, `bahar_azadi`, etc.