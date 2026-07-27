# TGJU.org — Verified Extraction Patterns (Session 2026-07-27)

## Verified Working Endpoints & Patterns

### HTML Structure (Profile Pages)
Each profile page (e.g., `/profile/geram18`) contains the price in multiple formats:

```html
<!-- Primary: data-price attribute on table row -->
<tr id="geram18" data-price="181565000" data-time="14:30:00" ...>
  <td class="price">۱۸,۱۵۶,۵۰۰</td>
</tr>

<!-- Alternative: span with price class -->
<span class="price" data-price="181565000">۱۸,۱۵۶,۵۰۰</span>

<!-- Alternative: td with price class -->
<td class="price">۱۸,۱۵۶,۵۰۰</td>
```

### Working Regex Patterns (Priority Order)
```python
PATTERNS = [
    r'data-price["\s:=]+([\d,]+)',      # Most reliable: data-price="181565000"
    r'class="price"[^>]*>([\d,]+)',     # <td class="price">18,156,500</td>
    r'<span[^>]*price[^>]*>([\d,]+)',   # <span class="price">18,156,500</span>
    r'<td[^>]*price[^>]*>([\d,]+)',     # <td class="price">18,156,500</td>
]
```

### Verified Profile URLs & Price Keys
| Asset | Profile URL | Price Key | Unit (TGJU) | Unit (Display) |
|-------|-------------|-----------|-------------|----------------|
| Gold 18k/gram | `/profile/geram18` | `gold_18k` | Rial | Toman (÷10) |
| Gold 24k/gram | `/profile/geram24` | `gold_24k` | Rial | Toman (÷10) |
| Mesghal | `/profile/mesghal` | `mesghal` | Rial | Toman (÷10) |
| Gold Ounce | `/profile/ons` | `gold_ounce` | USD | USD |
| Coin Full (New) | `/profile/sekee` | `coin_full` | Rial | Toman (÷10) |
| Half Coin | `/profile/nim` | `coin_half` | Rial | Toman (÷10) |
| Quarter Coin | `/profile/rob` | `coin_quarter` | Rial | Toman (÷10) |
| 1g Coin | `/profile/geram_sekee` | `coin_1g` | Rial | Toman (÷10) |
| USD Remittance | `/profile/price_dollar_rl` | `usd_remittance` | Rial | Toman (÷10) |
| EUR Remittance | `/profile/price_eur` | `eur` | Rial | Toman (÷10) |
| AED Remittance | `/profile/price_aed` | `aed` | Rial | Toman (÷10) |
| USDT | `/profile/usdt` | `usdt` | Toman | Toman |
| BTC | `/profile/btc` | `btc` | USD | USD |
| Brent Oil | `/profile/brent` | `brent` | USD | USD |
| WTI Oil | `/profile/wti` | `wti` | USD | USD |

### Verified Prices (2026-07-27 10:31 Tehran)
| Asset | TGJU Price (Rial) | Display (Toman) |
|-------|-------------------|-----------------|
| Gold 18k | 181,565,000 | **18,156,500** |
| Gold 24k | 242,060,000 | **24,206,000** |
| Mesghal | 786,500,000 | **78,650,000** |
| Coin Full (New) | 1,823,000,000 | **182,300,000** |
| Half Coin | 935,000,000 | **93,500,000** |
| Quarter Coin | 525,000,000 | **52,500,000** |
| USD Remittance | 15,156,900 | **1,515,690** |
| EUR | 17,240,430 | **1,724,043** |
| USDT | 188,088 | **188,088** |
| BTC | 65,363 | **$65,363** |
| Brent | 89.94 | **$89.94** |
| WTI | 83.51 | **$83.51** |

### Cron Integration (Production)
```python
#!/usr/bin/env python3
# /data/.hermes/scripts/tgju_monitor.py
import asyncio, aiohttp, re, json
from datetime import datetime, timezone, timedelta

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))
STATE_FILE = "/data/.hermes/tgju_prices.json"
THRESHOLD = 5.0  # 5%

TGJU_URLS = { ... }  # As above

async def fetch_all(session):
    tasks = [fetch_one(session, k, v) for k, v in TGJU_URLS.items()]
    results = await asyncio.gather(*tasks)
    return {k: v for r in results for k, v in r.items() if v is not None}

def check_alerts(old, new):
    alerts = []
    for k, new_price in new.items():
        if k in old and old[k] > 0:
            change = abs(new_price - old[k]) / old[k] * 100
            if change > THRESHOLD:
                alerts.append({
                    "asset": k,
                    "old": old[k],
                    "new": new_price,
                    "change_pct": round(change, 2),
                    "direction": "up" if new_price > old[k] else "down"
                })
    return alerts

async def main():
    state = load_json(STATE_FILE) or {}
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        prices = await fetch_all(session)
    
    # Convert Rial to Toman for display assets
    display_prices = {k: v // 10 if k not in ["gold_ounce", "btc", "brent", "wti", "usdt"] else v 
                      for k, v in prices.items()}
    
    alerts = check_alerts(state.get("prices", {}), display_prices)
    
    save_json(STATE_FILE, {"prices": display_prices, "last_update": datetime.now(TEHRAN_TZ).isoformat()})
    
    if alerts:
        print("---ALERTS---")
        print(json.dumps(alerts, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
```

### Common Pitfalls Fixed
| Pitfall | Fix |
|---------|-----|
| Prices in Rial not Toman | Always ÷10 for gold/currency/coin; USDT/BTC/Oil already in correct unit |
| `data-price` missing | Fallback to `class="price"` patterns |
| Persian numerals in HTML | HTML shows Arabic-Indic (۱۸,۱۵۶,۵۰۰) but `data-price` has ASCII digits |
| Rate limiting | Add 1-2s delay between requests; TGJU allows ~30 req/min |
| Stale cache | Add `?t={timestamp}` or `Cache-Control: no-cache` header |

### Comparison with IranJib
| Feature | TGJU | IranJib |
|---------|------|---------|
| Update frequency | Real-time (seconds) | Near real-time |
| Parsing | HTML (multiple patterns) | HTML (fixed IDs) |
| Reliability | High (official exchange) | High (aggregator) |
| Oil prices | Yes (Brent/WTI) | Yes |
| Crypto | Yes (USDT, BTC) | Yes |
| TSE index | Yes (`tesix`, `teda`) | No |
| Best for | Gold/Currency primary | Cross-reference |