# Market Monitoring — Reference Patterns (Session 2026-07-26)

## Cron Job Created

**Job ID**: `11d3ff670878`
**Name**: "Market Price Monitoring"
**Schedule**: Every 3 hours (`every 180m`)
**Skill**: `price-search` (for Iranian site scraping)
**Toolsets**: `web`, `terminal`, `file`
**Deliver**: `origin` (Telegram)
**Storage**: `/data/.hermes/market_prices.json` (last known prices for comparison)

## Assets Monitored & Sources

### 🥇 Gold/Coin (طلا/سکه)
| Source | Method | Notes |
|--------|--------|-------|
| **tgju.org** | **Playwright / curl** | **Primary — real-time Tehran Gold & Currency Exchange**. Profiles: `geram18` (18k gold/gram), `emami1` (Emami coin), `bahar_azadi` (Bahar Azadi coin). Most reliable for live Iranian prices. |
| mesghal.com | Playwright | Good backup, clean HTML, prices in Toman. May be daily not live. |
| tala.ir | Playwright | News + prices, daily updates. |
| bonbast.com | Playwright | Gold + currency combined, needs JS rendering. |

### 💵 Currency/USDT (ارز/دلار/تتر)
| Source | Method | Notes |
|--------|--------|-------|
| **tgju.org** | **Playwright / curl** | **Primary — real-time**. Profiles: `price_dollar_rl` (USD free market), `price_usdt_rl` (USDT/IRR), `price_eur_rl`, `price_gbp_rl`. |
| bonbast.com | Playwright | USD, EUR, GBP, USDT. Needs JS rendering. IDs: #usd1, #usd2, #gol18_top, #emami1_top. |
| bestchange.com | Playwright/curl | USDT rates via exchangers. Simple HTML tables. |

### ₿ Crypto (ارز دیجیتال)
| Source | Method | Notes |
|--------|--------|-------|
| coinmarketcap.com | API | REST API, free tier. `https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10&sortBy=market_cap&sortType=desc&convert=USD` |
| coindesk.com | Playwright | News + prices. |

### 🛢️ Oil (نفت)
| Source | Method | Notes |
|--------|--------|-------|
| oilprice.com | Playwright | Brent, WTI prices. |
| reuters.com | Playwright | Authoritative, news + prices. |

### 📰 Middle East News (اخبار خاورمیانه)
Monitor for: war/conflict escalation, new sanctions, nuclear talks, major geopolitical events
Sources: reuters.com, aljazeera.com, irna.ir, tasnimnews.com

## Alert Thresholds

| Asset Class | Threshold | Action |
|-------------|-----------|--------|
| Gold/Coin (طلا/سکه) | >5% change vs last stored | Send Telegram alert |
| Currency/USDT (دلار/تتر) | >5% change vs last stored | Send Telegram alert |
| Oil (نفت) | >3% daily change | Send Telegram alert |
| Major ME News | Any breaking event | Send Telegram alert |

## Storage Format (`/data/.hermes/market_prices.json`)

```json
{
  "gold": {
    "18k_gram_buy": 7557000,
    "18k_gram_sell": 7572000,
    "bahar_azadi_buy": 62650000,
    "bahar_azadi_sell": 63150000,
    "last_updated": "2026-07-26T22:30:00Z"
  },
  "currency": {
    "usd_rial": 1051700,
    "usdt_trc20_rial": 1051739,
    "eur_rial": 1135000,
    "last_updated": "2026-07-26T22:30:00Z"
  },
  "crypto": {
    "btc_usd": 58342,
    "eth_usd": 2618,
    "last_updated": "2026-07-26T22:30:00Z"
  },
  "oil": {
    "brent_usd": 81.50,
    "wti_usd": 77.80,
    "last_updated": "2026-07-26T22:30:00Z"
  }
}
```

## Scraping Patterns (Working July 2026)

### mesghal.com (Best for Gold/Coin)
```bash
curl -sL "https://mesghal.com" -H "User-Agent: Mozilla/5.0"
# Parse: ONS, GRAM 18, SHEKE BAHAR, NIM, ROB, GERMI
# Prices in Toman, format: 14,800,000
```

### bonbast.com
```bash
# Main page has IDs: #usd1, #usd2, #eur1, #eur2, #gol18_top, #emami1_top
# Requires JS rendering — use Playwright
```

### bestchange.com (USDT)
```bash
curl -sL "https://bestchange.com/usd-to-usdt-trc20.html"
# Parse exchanger rates table
```

### coinmarketcap.com API
```bash
curl -sL "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10&sortBy=market_cap&sortType=desc&convert=USD"
# Returns BTC, ETH, USDT, BNB, SOL, etc.
```

## Alert Message Format (Persian)

```
⚠️ **هشدار بازار: طلا/سکه**
📉 سکه بهار آزادی: ۶۳,۱۵۰,۰۰۰ تومان (۲.۸٪ کاهش)
🔗 منبع: mesghal.com
```

## Key Lessons

1. **mesghal.com is the most reliable for Iranian gold/coin prices** — clean HTML, prices in Toman
2. **bonbast.com needs Playwright** — prices rendered via JS
3. **bestchange.com gives real USDT market rates** — exchanger-based
4. **Store last values in JSON** — compare on each run, alert on threshold
5. **Silent mode** — only alert when threshold exceeded, no "all clear" messages
6. **Language**: All alerts in Persian (Farsi)