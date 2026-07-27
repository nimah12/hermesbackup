# Iranian Market Sources — Selectors & API Endpoints

## iranijib.ir (Primary — Playwright)

**URL:** `https://www.iranjib.ir/showgroup/23/realtime_price/`

**Tables (in order):**
1. Gold prices (طلا) — Table 1
2. Coin prices (سکه) — Table 2
3. Financial indices (بازارها و شاخص‌ها) — Table 3
4. Currency at Exchange Center (ارز در مرکز مبادله) — Table 5
5. Crypto (ارزهای دیجیتال) — Table 8
6. Global Metals (فلزات جهانی) — Table 9
7. Global Energy (انرژی جهانی) — Table 10

**Selectors:**
```python
tables = await page.query_selector_all('table')
# Table 0: Gold, Table 1: Coins, Table 2: Indices, etc.

rows = await table.query_selector_all('tr')
for row in rows:
    cells = await row.query_selector_all('td, th')
    cell_texts = [await cell.inner_text() for cell in cells]
```

**Key Rows to Extract:**
- Gold 18k: "هر گرم طلای ۱۸ عیار"
- Gold 24k: "هر گرم طلای ۲۴ عیار"
- Mesghal: "هر مثقال طلا در بازار تهران"
- Ounce: "هر انس طلا"
- Coin New: "طرح جدید"
- Coin Old: "طرح قدیم"
- Half Coin: "نیم سکه"
- Quarter Coin: "ربع سکه"
- USD (Exchange): "دلار / حواله"
- EUR: "یورو / حواله"
- USDT (Iranjib): "تتر"
- BTC: "بیت کوین / Bitcoin"
- Brent: "نفت برنت"
- WTI: "نفت سبک"

---

## talasea.ir (Gold Only — Playwright)

**URL:** `https://talasea.ir/`

**Playwright Approach:**
```python
await page.goto("https://talasea.ir/", wait_until="domcontentloaded")
await page.wait_for_timeout(5000)
content = await page.content()
# Parse for gold prices — structure varies
```

**Note:** Check for 18k, 24k, mesghal, ounce, coin prices

---

## mesghal.com (Playwright)

**URL:** `https://mesghal.com/`

**Warning:** Unit labeling issues — verify Rial vs Toman

**Selectors:**
```python
# Prices appear in text like:
# "گرم 18: 14,800,000"
# "سکه طلا(تومان): 64,111,000"
# Use regex to extract
```

---

## tgju.org (Playwright)

**URLs:**
- Gold 18k: `https://www.tgju.org/profile/price_gold_18`
- Gold 24k: `https://www.tgju.org/profile/price_gold_24`
- USD Free: `https://www.tgju.org/profile/price_dollar_rl`
- USDT: `https://www.tgju.org/profile/price_usdt_rl`

**Selectors:**
```python
# Price elements have class="price-value" or similar
# Look for: class="price-value", id="price", data-price
# Or search for large numbers near labels
```

---

## bonbast.com (Playwright)

**URL:** `https://bonbast.com/`

**Selectors:**
```python
# Elements have IDs like:
# usd1, usd2 (buy/sell)
# usdt1, usdt2
# eur1, eur2
# gbp1, gbp2
# gol18_top (gold 18k)
# mithqal_top (mesghal)
# emami1_top (emami coin)

# Pattern: id="usd1" then next sibling has price
```

---

## bestchange.com (Playwright or Direct HTML)

**URL:** `https://bestchange.com/usd-to-usdt-trc20.html`

**Parsing:**
```python
# Table rows with exchanger rates
# Look for: "USDT TRC20" + "USD Cash" / "USD Card"
# Extract rate numbers
```

---

## CoinMarketCap API (Direct — No Playwright)

**Endpoint:**
```
GET https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?
start=1&limit=20&sortBy=market_cap&sortType=desc&convert=USD
```

**Headers:** `User-Agent: Mozilla/5.0`

**Response:**
```json
{
  "data": {
    "cryptoCurrencyList": [
      {
        "name": "Bitcoin",
        "symbol": "BTC",
        "quotes": [{
          "price": 65168.45,
          "percentChange24h": 1.30
        }]
      }
    ]
  }
}
```

---

## CoinDesk API (Direct)

**Endpoint:**
```
GET https://api.coindesk.com/v1/bpi/currentprice.json
```

**Response:**
```json
{
  "bpi": {
    "USD": {"rate_float": 65168.45},
    "EUR": {...},
    "GBP": {...}
  }
}
```

---

## oilprice.com (Playwright)

**URL:** `https://www.oilprice.com/`

**Selectors:**
```python
# Look for: "Brent crude", "WTI", "Crude Oil"
# Price elements near these labels
```

---

## Reuters Commodities (Playwright)

**URL:** `https://www.reuters.com/markets/commodities/`

**Note:** May have paywall/blocking. Use as backup.

---

## Quick Verification Script

```python
# Run to verify all sources are accessible
import asyncio
from playwright.async_api import async_playwright

async def verify_sources():
    sources = [
        ("iranjib", "https://www.iranjib.ir/showgroup/23/realtime_price/"),
        ("talasea", "https://talasea.ir/"),
        ("mesghal", "https://mesghal.com/"),
        ("tgju_gold18", "https://www.tgju.org/profile/price_gold_18"),
        ("tgju_usd", "https://www.tgju.org/profile/price_dollar_rl"),
        ("tgju_usdt", "https://www.tgju.org/profile/price_usdt_rl"),
        ("bonbast", "https://bonbast.com/"),
        ("bestchange", "https://bestchange.com/usd-to-usdt-trc20.html"),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for name, url in sources:
            page = await browser.new_page()
            try:
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                print(f"✅ {name}: OK")
            except Exception as e:
                print(f"❌ {name}: {e}")
            finally:
                await page.close()
        await browser.close()

asyncio.run(verify_sources())
```

---

## Rate Limits & Best Practices

| Source | Rate Limit | Notes |
|--------|------------|-------|
| iranijib.ir | 1 req/3h (cron) | Heavy JS, needs 5s wait |
| talasea.ir | 1 req/30m (cron) | Light, fast |
| tgju.org | 1 req/3h | Medium JS |
| bonbast.com | 1 req/3h | Medium JS |
| CoinMarketCap | 30 req/min | API, no browser |
| CoinDesk | Unlimited | API, no browser |
| bestchange.com | 1 req/3h | Medium JS |
| oilprice.com | 1 req/3h | Light |
| t.me channels | 1 req/3h | Playwright, 3s wait |

**Always:**
- Use `/tmp/pw-browsers/` for Playwright cache
- `wait_until="domcontentloaded"` not `"networkidle"`
- 3-5 second wait after load for dynamic content
- Handle timeouts gracefully (60s max)
- Save state before and after each run