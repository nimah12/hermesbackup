# Telegram Channel Monitoring Reference

## Channels Used

| Channel | URL | Purpose |
|---------|-----|---------|
| @se_pz | https://t.me/s/se_pz | Gold, coin, USD, USDT prices |
| @talasea_ir | https://t.me/s/talasea_ir | Gold, coin, USD prices |

## t.me/s/ HTML Structure

The `t.me/s/` public preview pages contain messages in this structure:

```html
<div class="tgme_widget_message_wrap" data-post="channel_name/12345">
  <div class="tgme_widget_message_text js-message_text" dir="auto">
    <!-- Message text with prices -->
    طلا ۱۸ عیار: ۱۸,۱۵۶,۵۰۰ تومان
    سکه تمام: ۱۸۲,۳۰۰,۰۰۰ تومان
    دلار: ۱,۵۱۵,۶۹۰ تومان
  </div>
</div>
```

## Regex Patterns for Extraction

### Message Container
```python
# Main pattern for t.me/s/ pages
MESSAGE_PATTERN = r'data-post="[^"]+"[^>]*>.*?<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>'
```

### Price Extraction Patterns (Persian)

```python
PRICE_PATTERNS = {
    "gold_18k": [
        r'(?:طلای?\s*۱۸\s*عیار|گرم\s*طلای?\s*۱۸)\D*([\d,]{8,12})',
        r'(?:۱۸\s*عیار|18k)\D*([\d,]{8,12})',
        r'(?:geram.*?18|18.*?geram)\D*([\d,]{8,12})',
    ],
    "gold_24k": [
        r'(?:طلای?\s*۲۴\s*عیار|گرم\s*طلای?\s*۲۴)\D*([\d,]{8,12})',
        r'(?:۲۴\s*عیار|24k)\D*([\d,]{8,12})',
    ],
    "mesghal": [
        r'(?:مثقال\s*طلا|mesghal)\D*([\d,]{9,12})',
    ],
    "coin_full": [
        r'(?:سکه\s*(?:تمام|بهر|آزادی|کامل)|full\s*coin)\D*([\d,]{9,12})',
        r'(?:سکه\s*یک\s*گرم|۱\s*گرم\s*سکه)\D*([\d,]{9,12})',
    ],
    "coin_half": [
        r'(?:نیم\s*سکه|half\s*coin)\D*([\d,]{9,12})',
    ],
    "coin_quarter": [
        r'(?:ربع\s*سکه|quarter\s*coin)\D*([\d,]{8,12})',
    ],
    "usd": [
        r'(?:دلار|dollar|usd)\D*([\d,]{5,7})',
    ],
    "usdt": [
        r'(?:تتر|usdt|tether)\D*([\d,]{5,7})',
    ],
}
```

## Realistic Price Ranges (for validation)

| Item | Min | Max | Unit |
|------|-----|-----|------|
| Gold 18k/24k per gram | 10,000,000 | 50,000,000 | Toman |
| Mesghal | 50,000,000 | 100,000,000 | Toman |
| Coin Full | 50,000,000 | 300,000,000 | Toman |
| Coin Half | 20,000,000 | 150,000,000 | Toman |
| Coin Quarter | 10,000,000 | 80,000,000 | Toman |
| USD/USDT | 50,000 | 200,000 | Toman |

## Alert Threshold

- **Gold/Currency**: > 5% change
- **Oil**: > 3% change

## State File Format

```json
{
  "prices": {
    "se_pz:gold_18k": 18156500,
    "se_pz:usd": 1515690,
    "talasea_ir:coin_full": 182300000,
    ...
  },
  "last_check": "2026-07-27 10:42:23"
}
```

## Python Extraction Helper

```python
import re

def extract_prices(text):
    """Extract all recognized prices from message text"""
    prices = {}
    for key, pat_list in PRICE_PATTERNS.items():
        for pattern in pat_list:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                val = int(matches[-1].replace(",", ""))
                # Validate realistic range
                if key in ["gold_18k", "gold_24k"] and 10_000_000 < val < 50_000_000:
                    prices[key] = val
                    break
                elif key == "mesghal" and 50_000_000 < val < 100_000_000:
                    prices[key] = val
                    break
                elif key == "coin_full" and 50_000_000 < val < 300_000_000:
                    prices[key] = val
                    break
                elif key == "coin_half" and 20_000_000 < val < 150_000_000:
                    prices[key] = val
                    break
                elif key == "coin_quarter" and 10_000_000 < val < 80_000_000:
                    prices[key] = val
                    break
                elif key in ["usd", "usdt"] and 50_000 < val < 200_000:
                    prices[key] = val
                    break
    return prices
```

## Cron Job Configuration

```yaml
# Gold/Currency Alert - every 30 minutes
cronjob create:
  action: create
  no_agent: true
  script: gold_alert_telegram.py
  schedule: "every 30m"
  deliver: "origin"
  enabled_toolsets: ["terminal", "file"]
```

## Notes

- Use `t.me/s/channelname` (not `t.me/channelname`) for public HTML preview
- Messages may contain multiple prices - extract all and validate ranges
- Persian numbers (۰-۹) may appear - normalize with `.replace("،", "").replace(",", "")`
- Skip metadata fields like "24h_change" - they trigger false alerts
- State file stores prices keyed by `channel:item` for cross-channel comparison