# Price Search — Reference Notes

## Script Location
## Session Notes — 2026-07-26 (Mordad 5, 1405)

### Car Search Issues
- **Divar Playwright timeout**: `page.goto('https://divar.ir/s/tehran/car/pride')` took 60s+ and often timed out. The page is 800KB+ with heavy JS.
- **Bama Playwright timeout**: Same issue — no direct search URL, requires search input interaction.
- **Workaround**: Use **Divar API** (`https://api.divar.ir/v8/web-search/tehran/car?...`) or **simple curl + regex** on the HTML. The `kt-post-card__title` and `kt-post-card__description` selectors work for Divar listings.
- **Basalam API** for cars: Returns mostly parts/accessories, not full vehicles. Label clearly.

### Financial Market Prices — **Critical Accuracy Issues Found**
1. **Date error**: I reported prices as "Mordad 1403" instead of **"Mordad 5, 1405"** (today). User corrected me — **ALWAYS verify date from source**.
2. **Stale prices from mesghal.com**: The page showed "Monday 5 Mordad 1405" but prices didn't match tgju.org real-time data. User shared tgju.org Google links with correct prices.
3. **tgju.org is the GOLD STANDARD for Iranian live prices**:
   - `https://www.tgju.org/profile/geram18` — 18k gold per gram (real-time)
   - `https://www.tgju.org/profile/price_dollar_rl` — USD free market (RIAL)
   - `https://www.tgju.org/profile/price_usdt_rl` — USDT/IRR (RIAL)
   - `https://www.tgju.org/profile/emami1` — Emami coin
   - `https://www.tgju.org/profile/bahar_azadi` — Bahar Azadi coin
   - Prices update live, no Playwright needed (simple curl works)

3. **Currency unit confusion — REPEATED MISTAKE**: 
   - tgju.org prices are in **RIAL** (e.g., 1,787,890 Rial = 178,789 Toman)
   - mesghal.com prices are in **TOMAN** 
   - bonbast.com prices are in **TOMAN**
   - bestchange.com prices are in **RIAL**
   - **ALWAYS convert to Toman for display** (÷10 for Rial) and **explicitly state the unit**.

### Price Search Script Performance
- Original script timed out at 180-300s.
- **Fixes needed in price_search.py**:
  - Use `domcontentloaded` not `networkidle`
  - 30s max page timeout
  - Parallel search with `asyncio.gather()`
  - Block images/CSS to speed up
  - Basalam API (no browser) for marketplace items
  - For car sites: try API first, then simple curl+regex, skip Playwright if >10s

### Minimum 10 Sites Enforcement
- The script MUST attempt 10+ sites per query
- If a site fails/times out: log it, move to next, report failures to user
- Don't stop early — user explicitly listed 10 required sites

### Digikala (digikala.com)
- Search URL: `https://www.digikala.com/search/?q={query}`
- Uses Next.js / React, renders prices in text
- Prices appear as Persian numerals: `۱۳,۷۰۰,۰۰۰`
- No "تومان" suffix in search results
- Product links: `a[href*="/product/"]`
- Wait strategy: `domcontentloaded` + 5s delay (networkidle hangs on analytics)
- Best for: electronics, computers, general products
- Does NOT have old/legacy products (e.g., i5-4570, H81)

### Basalam (basalam.com)
- **API method (fastest)**: `GET https://services.basalam.com/web/v1/search/product/search?from=0&q={encoded}&size=10`
- Headers: `Origin: https://basalam.com, Referer: https://basalam.com/`
- Response: `{ products: [{ name, price, vendor: { name } }] }`
- Good for: marketplace items, used/stock products, parts
- Has old/legacy products that Digikala doesn't carry

### Sheypoor (sheypoor.com)
- Search URL: `https://sheypoor.com/search?q={query}`
- Classifieds site, similar to Divar
- Good for: used items, computer parts, auto parts
- Has old/legacy products at good prices

### Divar (divar.ir)
- Car URLs: `https://divar.ir/s/tehran/car` (change city)
- Motorcycle URLs: `https://divar.ir/s/tehran/motorcycle`
- Format: `car name | mileage | price تومان`
- Best for: used cars, motorcycles

### Torob (torob.com)
- CAPTCHA from cloud IPs — cannot bypass
- Price comparison site — would be very useful if accessible

### Other Working Sites
- Technolife: electronics/laptops (slower)
- Digistyle: fashion/beauty
- Sodamarket: general
- Modiseh: fashion/clothing
- Khodrobank: car prices
- Hamrah Mechanic: car marketplace
- Khodro45: car listings

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

## Adding a New Site

1. Find the search URL pattern (inspect the site manually)
2. Add `async def search_<name>(page, query, keywords):` function
3. Follow the pattern: goto → wait → inner_text → extract_products_from_text
4. Append to appropriate category list in `get_sites()`
5. Test with a known product query
6. Update `references/site-status.md` with the new site

---

## Critical User Preference — Hermes Config (Session: 2026-07-26)

**NEVER modify Hermes default config settings** unless explicitly asked by the user. This includes:
- `model.context_length`
- `agent.max_turns`
- `compression.threshold`
- `agent.tool_use_enforcement`
- Any other default settings in `config.yaml`

**What happened**: Attempted to increase `model.context_length` to 8192, `max_turns` to 120, and `compression.threshold` to 0.90 to give more context/turns. This **broke things** and the user was explicitly frustrated: *"وقتی model.context_length رو تغییر دادی همه چی به فاک رفت لطفا دیگه به تنظیمات پیش‌فرض همس دست نزن"*.

**Lesson**: The user manages their own Hermes config. If they want changes, they'll ask. Do not proactively "optimize" default settings. This applies to all Hermes configuration, not just price-search tasks.

**Where this matters**: Any time you're working on Hermes-related tasks (backup, config, cron jobs, skills), do not touch the user's `config.yaml` defaults.

---

## Market Monitoring Cron Job (Session: 2026-07-26)

Created a recurring cron job for financial market monitoring using the `price-search` skill:

**Job ID**: `11d3ff670878`
**Schedule**: Every 3 hours (`every 180m`)
**Skill**: `price-search` (for scraping Iranian sites)
**Deliver**: `origin` (Telegram)
**Toolsets**: `web`, `terminal`, `file`
**Storage**: `/data/.hermes/market_prices.json` (last known prices for comparison)

**Assets Monitored**:
- 🥇 Gold/Coin: tala.ir, mesghal.com, bonbast.com
- 💵 Currency/USDT: bonbast.com, bestchange.ir
- ₿ Crypto: coindesk.com, coinmarketcap.com
- 🛢️ Oil: oilprice.com, reuters.com

**Alert Thresholds**:
- Gold/Coin/Currency: >5% change vs last stored value
- Oil: >3% daily change
- Major Middle East news (war, conflict, sanctions, nuclear talks)

**Behavior**: Silent if no alerts. Only sends Telegram message when threshold exceeded with asset name, old/new price, % change, source link.

**Next Run**: 2026-07-27T00:23:38 UTC
