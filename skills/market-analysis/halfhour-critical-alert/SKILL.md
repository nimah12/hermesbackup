---
name: halfhour-critical-alert
description: Alert on Iran market changes >5% every 30min.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
      - Market
      - Iran
      - Alert
      - Cron
---

# Half-Hour Critical Market Alert

Monitor Iranian market prices every 30 minutes and alert only when any asset changes >5%. Uses emoji indicators (🔴 >5%, 🟠 >3%, 🟡 >1%, 🟢 ≤1%) with Iranian color convention (red=up=bad, green=down=good). Integrates with iran-market-intelligence and telegram-persian-formatter.

## When to Use
- Automated 30-minute cron job for critical market moves
- User wants silent monitoring — only alerts on significant changes
- Telegram channel delivery with formatted Persian output

## Prerequisites
- iran-market-intelligence skill (data sources, thresholds)
- telegram-persian-formatter skill (output styling)
- market_monitor.py script at /data/.hermes/scripts/
- market_prices.json state file at /data/.hermes/
- Python 3.10+, aiohttp

## How to Run
Create cron job with `cronjob` tool:
```yaml
action: create
schedule: "every 30m"
skills: ["halfhour-critical-alert", "telegram-persian-formatter"]
prompt: "Run market_monitor.py, deliver formatted alert if any change >5%"
deliver: origin
```

## Quick Reference
| Change | Indicator | Meaning |
|--------|-----------|---------|
| >5% | 🔴 | Critical — immediate alert |
| >3% | 🟠 | Warning — monitor closely |
| >1% | 🟡 | Moderate — notable |
| ≤1% | 🟢 | Stable — no alert |

## Procedure
1. **Fetch prices** from IranJib + CoinGecko via market_monitor.py
2. **Compare** each price with previous state (market_prices.json)
3. **Calculate** percentage change and direction
4. **Apply indicator** using get_change_indicator() logic
5. **If ANY change >5%**: format full report with all prices + indicators, deliver to Telegram
6. **If ALL changes ≤5%**: silent — update state file only, no delivery
7. **Save** new prices as baseline for next run

## Indicator Logic (Python)
```python
def get_change_indicator(change_pct: float) -> str:
    abs_change = abs(change_pct)
    if abs_change > 5.0: return "🔴"
    elif abs_change > 3.0: return "🟠"
    elif abs_change > 1.0: return "🟡"
    else: return "🟢"
```

## Pitfalls
- **Silent mode**: No output when stable — cron must use `no_agent=true` or handle empty stdout
- **State file**: Must persist between runs — /data/.hermes/market_prices.json
- **Iranian convention**: Red=price increase (bad for buyers), Green=decrease (good)
- **Threshold**: Alert triggers on ANY single asset >5%, not average
- **Timezone**: All times in Tehran (UTC+3:30)

## Verification
1. Create cron job with 30min schedule
2. Run manually: `python3 /data/.hermes/scripts/market_monitor.py`
3. Verify: No output when stable, formatted alert when >5% change
4. Check state file updated: `read_file /data/.hermes/market_prices.json`