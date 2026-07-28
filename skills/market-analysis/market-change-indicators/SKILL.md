---
name: market-change-indicators
description: Add emoji indicators for Iran market change percentages.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
      - Market
      - Iran
      - Formatting
      - Indicators
---

# Market Change Indicators

Add visual emoji circles to Iranian market price outputs based on percentage change thresholds. Designed for Persian Telegram channel formatting with iran-market-intelligence and telegram-persian-formatter skills.

## When to Use
- Formatting market price outputs for Telegram delivery
- Any Iranian financial data display needing quick visual change assessment
- Cron job alerts from market_monitor.py or gold_alert_telegram.py

## Prerequisites
- iran-market-intelligence skill (data source)
- telegram-persian-formatter skill (output style)
- Python 3.10+ with aiohttp (for cron scripts)

## How to Run
Apply indicator logic when formatting price changes in market reports. No standalone invocation — integrates into existing market monitoring workflow.

## Quick Reference
| Change % | Indicator | Meaning |
|----------|-----------|---------|
| > 5% | 🔴 | Critical change (red circle) |
| > 3% | 🟠 | Warning change (orange circle) |
| ≤ 1% | 🟢 | Stable/minimal (green circle) |
| 1-3% | 🟡 | Moderate (yellow circle) |

## Procedure
1. **Calculate percentage change** between current and previous price
2. **Apply indicator** based on thresholds above
3. **Prefix price line** with indicator emoji in formatted output
4. **Include direction arrow** (▲ for up, ▼ for down) for clarity
5. **Use Iranian convention**: RED = price increase (bad for buyers), GREEN = decrease (good)

## Indicator Logic (Python)
```python
def get_change_indicator(change_pct: float, direction: str) -> str:
    abs_change = abs(change_pct)
    if abs_change > 5.0:
        return "🔴"
    elif abs_change > 3.0:
        return "🟠"
    elif abs_change > 1.0:
        return "🟡"
    else:
        return "🟢"
```

## Pitfalls
- Thresholds are absolute values — direction handled separately
- Iranian market: red = up (bad), green = down (good) — opposite of Western
- Only applies to price change display, not static prices
- Requires previous price data (from market_prices.json state file)

## Verification
Run market_monitor.py and verify output includes emoji indicators:
```bash
python3 /data/.hermes/scripts/market_monitor.py
```
Check that price lines with changes show 🔴/🟠/🟡/🟢 prefixes.