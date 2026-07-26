# Price Search — Reference Notes

## Script Location
`/data/.hermes/scripts/price_search.py`

## Playwright Setup on This System

```bash
# Install
pip install playwright
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers playwright install chromium
PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers playwright install-deps chromium

# System deps that were missing initially:
# libglib-2.0.so.0 and other GTK/GLib libraries
# Fixed by: playwright install-deps chromium
```

**Why /tmp?** The `/data` partition is 434MB. Chromium alone is ~300MB. `/tmp` lives on the root overlay with 1.8TB free.

## Site-Specific Notes

### Digikala (digikala.com)
- Search URL: `https://www.digikala.com/search/?q={query}`
- Uses Next.js / React, renders prices in text
- Prices appear as Persian numerals: `۱۳,۷۰۰,۰۰۰`
- No "تومان" suffix in search results
- Product links: `a[href*="/product/"]`
- Wait strategy: `domcontentloaded` + 5s delay (networkidle hangs on analytics)
- Tested 2026-07-26: working, 968 results for "RX 580 8GB"

### Torob (torob.com)
- Search URL: `https://torob.com/search/?query={query}`
- Uses ar captcha (arcaptcha.ir) for bot detection
- Returns captcha page on first visit from new IP
- Cannot be bypassed with headless Playwright
- API endpoint (`api.torob.com`) also blocked by captcha

### Emalls (emalls.ir)
- Search URL: `https://www.emalls.ir/search?query={query}`
- SSL certificate often expired/invalid
- Use `ignore_https_errors=True`
- Sometimes returns empty page

### Technolife (technolife.com)
- Search URL: `https://www.technolife.com/search?q={query}`
- Redirects from .ir to .com
- More laptops than standalone GPUs
- Working as of 2026-07-26

### Sodamarket (sodamarket.com)
- Search URL: `https://www.sodamarket.com/search?q={query}`
- General electronics store
- Working as of 2026-07-26

### Galaxy-M (galaxy-m.com)
- Search URL: `https://www.galaxy-m.com/search?q={query}`
- Mobile-focused store
- Working as of 2026-07-26

### Digistyle (digistyle.com)
- Search URL: `https://www.digistyle.com/search?q={query}`
- Fashion-focused, limited electronics
- Working as of 2026-07-26

## Persian Numeral Conversion

```python
PERSIAN_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
text_en = text.translate(PERSIAN_DIGITS)
```

## Price Regex Pattern

Iranian prices use commas as thousand separators:
- `۱۳,۷۰۰,۰۰۰` → `13,700,000`
- Regex: `([\d,]{7,})` — matches 7+ digit numbers with commas
- After converting Persian digits, strip commas and check length ≥ 6

## Test Results (2026-07-26)

Query: "RX 580 8GB"
- Digikala: 3 RX 580 results (13.7M - 26.6M Toman) + related GPUs
- Technolife: laptops with 8GB RAM (not GPU matches)
- Digistyle: no GPU matches
- Torob: captcha blocked
- Emalls: no results

Query: "هوندا 125"
- Digikala: Honda 125 motorcycles (234M - 544M Toman) + parts
- Basalam API: Parts and accessories (250K - 26.7M Toman)
- Divar: Honda listings available

Query: "Intel i5-4570"
- Basalam: i5-4570 stock (44.5M - 90.7M Toman)
- Digikala: No direct 4570 listings (only newer CPUs)
- Found bundle: CPU + H81 motherboard + fan for 108M Toman

## New Sites Discovered (July 2026)

### Sheypoor (sheypoor.com)
- Classifieds site, similar to Divar
- URL: `https://sheypoor.com/search?q={query}`
- Status: Working, has search + prices

### Modiseh (modiseh.com)
- Fashion/clothing e-commerce
- URL: `https://modiseh.com/search?q={query}`
- Status: Working, prices in body text

### Hamrah Mechanic (hamrah-mechanic.com)
- Car marketplace, similar to Bama
- URL: `https://hamrah-mechanic.com/search?q={query}`
- Status: Working, has search + prices

## Adding a New Site

1. Find the search URL pattern (inspect the site manually)
2. Add `async def search_<name>(page, query, keywords):` function
3. Follow the pattern: goto → wait → inner_text → extract_products_from_text
4. Append to appropriate category list in `get_sites()`
5. Test with a known product query
6. Update `references/site-status.md` with the new site
