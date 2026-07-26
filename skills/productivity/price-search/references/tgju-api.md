# tgju.org — Tehran Gold & Currency Exchange API Patterns

## Overview
**tgju.org** is the **primary source for real-time Iranian financial market prices**. It's the official Tehran Gold & Currency Exchange (Tala va Arz) website.

- Prices update **live** (seconds-level refresh)
- No Playwright needed — simple `curl` works
- All prices in **RIAL** (divide by 10 for Toman)
- Clean HTML with consistent `class="price-value"` selectors

## Key Profiles (URLs)

| Asset | Profile URL | Display Name |
|-------|-------------|--------------|
| **18k Gold (per gram)** | `https://www.tgju.org/profile/geram18` | گرم طلای ۱۸ عیار |
| **USD Free Market** | `https://www.tgju.org/profile/price_dollar_rl` | دلار آزاد |
| **USDT (Tether)** | `https://www.tgju.org/profile/price_usdt_rl` | تتر (USDT) |
| **Euro** | `https://www.tgju.org/profile/price_eur_rl` | یورو |
| **GBP** | `https://www.tgju.org/profile/price_gbp_rl` | پوند |
| **Emami Coin** | `https://www.tgju.org/profile/emami1` | سکه امامی |
| **Bahar Azadi Coin** | `https://www.tgju.org/profile/bahar_azadi` | سکه بهار آزادی |
| **Half Azadi** | `https://www.tgju.org/profile/half_azadi` | نیم سکه |
| **Quarter Azadi** | `https://www.tgju.org/profile/quarter_azadi` | ربع سکه |
| **Gold Gram** | `https://www.tgju.org/profile/gram_gold_18` | گرم طلا ۱۸ |

## HTML Structure (for parsing)

```html
<!-- Main price value -->
<div class="price-value" data-price="17878900">۱۷,۸۷۸,۹۰۰</div>

<!-- Change indicators -->
<span class="price-change positive">+۱۲۳,۴۵۶</span>  <!-- positive = green -->
<span class="price-change negative">-۱۲۳,۴۵۶</span>  <!-- negative = red -->

<!-- Last update timestamp -->
<span class="last-update">۲۰۲۶-۰۷-۲۷ ۰۶:۴۵:۱۲</span>
```

## Quick Extraction (curl + grep)

```bash
# 18k Gold (per gram) - in RIAL
curl -s "https://www.tgju.org/profile/geram18" -H "User-Agent: Mozilla/5.0" | \
  grep -oP 'class="price-value"[^>]*>\K[0-9,]+'

# USD Free Market - in RIAL
curl -s "https://www.tgju.org/profile/price_dollar_rl" -H "User-Agent: Mozilla/5.0" | \
  grep -oP 'class="price-value"[^>]*>\K[0-9,]+'

# USDT - in RIAL  
curl -s "https://www.tgju.org/profile/price_usdt_rl" -H "User-Agent: Mozilla/5.0" | \
  grep -oP 'class="price-value"[^>]*>\K[0-9,]+'
```

## Python Helper

```python
import urllib.request
import re

TGJU_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

def get_tgju_price(profile: str) -> int:
    """Get price in RIAL from tgju.org profile"""
    url = f"https://www.tgju.org/profile/{profile}"
    req = urllib.request.Request(url, headers=TGJU_HEADERS)
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    
    match = re.search(r'class="price-value"[^>]*>([0-9,]+)', html)
    if match:
        return int(match.group(1).replace(',', ''))
    return None

def rial_to_toman(rial: int) -> int:
    """Convert Rial to Toman (divide by 10)"""
    return rial // 10

# Usage
gold_rial = get_tgju_price('geram18')        # e.g., 17878900 Rial
usd_rial = get_tgju_price('price_dollar_rl')  # e.g., 1051700 Rial
usdt_rial = get_tgju_price('price_usdt_rl')   # e.g., 1051740 Rial

print(f"18k Gold: {rial_to_toman(gold_rial):,} Toman")
print(f"USD: {rial_to_toman(usd_rial):,} Toman")
print(f"USDT: {rial_to_toman(usdt_rial):,} Toman")
```

## Key Findings from Session (Mordad 5, 1405)

1. **Real-time vs Daily**: tgju.org updates live (seconds). mesghal.com shows "Monday 5 Mordad 1405" but prices were stale/different.
2. **Unit**: ALL tgju.org prices are in **RIAL** — must divide by 10 for Toman display.
3. **Reliability**: No JS rendering needed — works with simple HTTP GET.
4. **Date**: Always check the `last-update` span or the page timestamp to confirm freshness.

## Integration with Market Monitoring Cron

The cron job should:
1. Fetch from tgju.org profiles every 3 hours
2. Compare with stored `/data/.hermes/market_prices.json`
3. Alert if change > 5% (gold/currency) or > 3% (oil)
4. Save new values for next comparison

## Common Profiles for Cron Job

```python
TGJU_PROFILES = {
    'geram18': '18k Gold (gram)',
    'price_dollar_rl': 'USD Free Market',
    'price_usdt_rl': 'USDT (Tether)',
    'price_eur_rl': 'EUR',
    'price_gbp_rl': 'GBP',
    'emami1': 'Emami Coin',
    'bahar_azadi': 'Bahar Azadi Coin',
    'half_azadi': 'Half Azadi Coin',
    'quarter_azadi': 'Quarter Azadi Coin',
}
```

## Error Handling

- If tgju.org fails: fallback to `mesghal.com` (Playwright) or `bonbast.com`
- Timeout: 10 seconds max per request
- Rate limit: max 1 request/second per profile (respectful scraping)