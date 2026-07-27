---
name: tgju-market-api
description: "Get Iranian gold, currency, crypto, oil prices from TGJU."
tags: [market, gold, currency, tgju, iran, real-time]
---

# TGJU Market API — Real-time Iranian Financial Data

Direct API access to Tehran Gold & Currency Exchange (TGJU) for live prices.

## When to Use
- Need real-time gold (18k, 24k, mesghal, ounce), coin, USD/USDT, crypto, oil, metals prices
- Market monitoring cron jobs (every 30min-3h)
- Alerting on >5% price changes

## API Endpoints (No Auth Required)

### Main Price Profiles
| Asset | TGJU Profile URL | Key Selector |
|-------|------------------|--------------|
| Gold 18k/gram | https://www.tgju.org/profile/geram18 | `#geram18 .price` |
| Gold 24k/gram | https://www.tgju.org/profile/geram24 | `#geram24 .price` |
| Mesghal | https://www.tgju.org/profile/mesghal | `#mesghal .price` |
| Gold Ounce | https://www.tgju.org/profile/ons | `#ons .price` |
| Coin (Bahri Azadi) | https://www.tgju.org/profile/sekee | `#sekee .price` |
| Half Coin | https://www.tgju.org/profile/nim | `#nim .price` |
| Quarter Coin | https://www.tgju.org/profile/rob | `#rob .price` |
| USD (Remittance) | https://www.tgju.org/profile/price_dollar_rl | `#price_dollar_rl .price` |
| EUR | https://www.tgju.org/profile/price_eur | `#price_eur .price` |
| BTC | https://www.tgju.org/profile/btc | `#btc .price` |
| USDT | https://www.tgju.org/profile/usdt | `#usdt .price` |

### Oil & Energy
| Asset | TGJU Profile URL |
|-------|------------------|
| Brent | https://www.tgju.org/profile/brent |
| WTI | https://www.tgju.org/profile/wti |
| Gasoline | https://www.tgju.org/profile/gasoline |
| Gas Oil | https://www.tgju.org/profile/gas_oil |

### Metals
| Asset | TGJU Profile URL |
|-------|------------------|
| Copper | https://www.tgju.org/profile/copper |
| Silver | https://www.tgju.org/profile/silver |
| Platinum | https://www.tgju.org/profile/platinum |

## Quick Fetch Script (Python)

```python
import asyncio
import aiohttp
import re

TGJU_URLS = {
    "gold_18k": "https://www.tgju.org/profile/geram18",
    "gold_24k": "https://www.tgju.org/profile/geram24",
    "mesghal": "https://www.tgju.org/profile/mesghal",
    "coin_full": "https://www.tgju.org/profile/sekee",
    "coin_half": "https://www.tgju.org/profile/nim",
    "coin_quarter": "https://www.tgju.org/profile/rob",
    "usd": "https://www.tgju.org/profile/price_dollar_rl",
    "eur": "https://www.tgju.org/profile/price_eur",
    "btc": "https://www.tgju.org/profile/btc",
    "usdt": "https://www.tgju.org/profile/usdt",
    "brent": "https://www.tgju.org/profile/brent",
    "wti": "https://www.tgju.org/profile/wti",
}

async def fetch_tgju_price(session, name, url):
    try:
        async with session.get(url, timeout=10) as resp:
            html = await resp.text()
            patterns = [
                r'data-price["\s:=]+([\d,]+)',
                r'class="price"[^>]*>([\d,]+)',
                r'<span[^>]*price[^>]*>([\d,]+)',
                r'<td[^>]*price[^>]*>([\d,]+)',
            ]
            for pattern in patterns:
                m = re.search(pattern, html)
                if m:
                    return {name: int(m.group(1).replace(",", ""))}
    except Exception as e:
        return {name: None}
    return {name: None}

async def get_all_tgju_prices():
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [fetch_tgju_price(session, k, v) for k, v in TGJU_URLS.items()]
        results = await asyncio.gather(*tasks)
        merged = {}
        for r in results:
            merged.update(r)
        return merged
```

## Currency Unit
- **All TGJU prices are in Rial**
- Convert to Toman: `price // 10`
- Display in Toman (standard Iranian convention)

## Cron Integration
```bash
# Every 30 minutes for gold/currency alerts
*/30 * * * * python3 /path/to/tgju_monitor.py

# Every 3 hours for full market snapshot
0 */3 * * * python3 /path/to/market_snapshot.py
```

## Alert Thresholds
- Gold/Currency: >5% change
- Oil: >3% change
- Crypto: >10% change

## References
- TGJU.org - Tehran Gold & Currency Exchange
- Updates every few seconds during market hours
- Most reliable source for Iranian market prices