# Market Change Indicators — Reference

## Emoji Indicators for Iranian Market

| Change % | Indicator | Meaning |
|----------|-----------|---------|
| **> 5%** | 🔴 | **Critical** — Immediate alert, bad for buyers (price up) |
| **3-5%** | 🟠 | **Warning** — Monitor closely |
| **1-3%** | 🟡 | **Moderate** — Notable movement |
| **≤ 1%** | 🟢 | **Stable** — Minimal change, good for buyers (price down) |

## Iranian Color Convention (CRITICAL)

**OPPOSITE of Western convention:**
- 🔴 **RED** = Price INCREASE (bad for buyers → "alert/warning")
- 🟢 **GREEN** = Price DECREASE (good for buyers → "relief")
- 🟡 **YELLOW/ORANGE** = High volatility / fluctuation

## Thresholds by Asset Class

| Asset Class | Warning | Critical | Action |
|-------------|---------|----------|--------|
| Gold (18k, 24k, Coin) | >3% daily | >5% daily | Buy physical / coin |
| Currency (USD, EUR, USDT) | >2% daily | >5% daily | Buy USDT / crypto |
| Oil (Brent, WTI) | >$3/day | >$10/day | Hedge / short stocks |
| Tehran Stock Index | >-2% | >-5% | Reduce exposure |
| BTC Iran Premium | >10% | >20% | Sell premium / buy dip |

## Implementation

```python
def get_change_indicator(change_pct: float) -> str:
    abs_change = abs(change_pct)
    if abs_change > 5.0:
        return "🔴"
    elif abs_change > 3.0:
        return "🟠"
    elif abs_change > 1.0:
        return "🟡"
    else:
        return "🟢"

def format_price_line(key: str, new_val: float, old_val: float = None) -> str:
    if old_val is None or old_val == 0:
        return f"  {key}: {new_val:,.2f}"
    change_pct = (new_val - old_val) / old_val * 100
    direction = "▲" if change_pct > 0 else "▼"
    indicator = get_change_indicator(change_pct)
    return f"  {indicator} {key}: {new_val:,.2f} ({direction}{abs(change_pct):.2f}%)"
```

## Cron Jobs Using This Logic

| Job | Schedule | Script | Alert Trigger |
|-----|----------|--------|---------------|
| Iran Market Intelligence | Every 3h | `market_monitor.py --silent` | Any 🔴 (>5%) or 🟠 oil (>3%) |
| Iran Market Critical Alert | Every 30m | `market_monitor.py --silent` | Any 🔴 (>5%) or 🟠 oil (>3%) |
| Gold Telegram Alert | Every 30m | `gold_alert_telegram.py` | >5% from @se_pz, @talasea_ir |