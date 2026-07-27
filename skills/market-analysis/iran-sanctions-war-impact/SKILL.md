---
name: iran-sanctions-war-impact
description: "Analyze war/sanctions impact on Iran gold, currency, oil."
tags: [iran, sanctions, war, gold, currency, oil, market-impact, geopolitics]
---

# Iran Sanctions & War Impact Analysis

Analyze how Middle East conflicts, US sanctions, and geopolitical events affect Iranian markets: gold, currency (USD/USDT), oil, crypto, stocks.

## When to Use
- User asks "جنگ چطور روی قیمت طلا/دلار اثر می‌گذارد؟"
- Need to correlate geopolitical events with price movements
- Risk assessment for Iranian market positions
- Scenario planning for escalation/de-escalation

## Key Impact Channels

### 1. Direct Military Conflict
| Event | Gold | USD/USDT | Oil (Brent) | Tehran Stocks | Crypto |
|-------|------|----------|-------------|---------------|--------|
| Iran-Israel direct exchange | 🔺🔺🔺 (+15-30%) | 🔺🔺 (+10-20%) | 🔺🔺🔺 (+$20-50/bbl) | 🔻🔻 (-15-30%) | 🔺 (+20-50%) |
| Proxy attack on US base | 🔺🔺 (+10-20%) | 🔺🔺 (+8-15%) | 🔺🔺 (+$10-30/bbl) | 🔻🔻 (-10-20%) | 🔺 (+15-30%) |
| Strait of Hormuz threat | 🔺 (+5-10%) | 🔺 (+5-10%) | 🔺🔺🔺 (+$30-100/bbl) | 🔻🔻 (-15-25%) | 🔺 (+10-20%) |
| Nuclear facility strike | 🔺🔺🔺 (+20-40%) | 🔺🔺🔺 (+20-40%) | 🔺🔺 (+$20-50/bbl) | 🔻🔻🔻 (-30-50%) | 🔺🔺 (+30-60%) |

### 2. Sanctions Escalation
| Sanction Type | Gold | USD/USDT | Oil Export | Inflation | Crypto Usage |
|---------------|------|----------|------------|-----------|--------------|
| Oil export ban | 🔺🔺 | 🔺🔺 | 🔻🔻🔻 | 🔺🔺🔺 | 🔺🔺 |
| Banking disconnect (SWIFT) | 🔺🔺 | 🔺🔺🔺 | 🔻🔻 | 🔺🔺 | 🔺🔺🔺 |
| Central bank assets freeze | 🔺🔺 | 🔺🔺 | 🔻 | 🔺🔺 | 🔺🔺 |
| Secondary sanctions on buyers | 🔺 | 🔺 | 🔻🔻 | 🔺 | 🔺 |

### 3. Diplomatic/De-escalation
| Event | Gold | USD/USDT | Oil | Stocks | Crypto |
|-------|------|----------|-----|--------|--------|
| JCPOA revival hope | 🔻🔻 | 🔻🔻 | 🔻 | 🔺🔺 | 🔻 |
| Prisoner swap / talks | 🔻 | 🔻 | 🔻 | 🔺 | 🔻 |
| Regional normalization | 🔻 | 🔻 | 🔻 | 🔺🔺 | 🔻 |

## Real-time Monitoring Dashboard

### Primary Indicators (Check Every 30min)
```python
INDICATORS = {
    "gold_18k_tgju": "https://www.tgju.org/profile/geram18",
    "gold_24k_tgju": "https://www.tgju.org/profile/geram24",
    "coin_bahri_tgju": "https://www.tgju.org/profile/sekee",
    "usd_remittance_tgju": "https://www.tgju.org/profile/price_dollar_rl",
    "usdt_tgju": "https://www.tgju.org/profile/usdt",
    "brent_oil": "https://www.tgju.org/profile/brent",
    "wti_oil": "https://www.tgju.org/profile/wti",
    "btc_tgju": "https://www.tgju.org/profile/btc",
    "tesix": "https://www.tgju.org/profile/tesix",  # Tehran Stock Exchange
    "teda": "https://www.tgju.org/profile/teda",    # ETF
}
```

### Telegram Alert Channels
```python
WAR_CHANNELS = [
    "@iranintltv",      # Breaking military news
    "@km_ap",           # Khamenei statements
    "@tasnimnews",      # IRGC / military
    "@farsna",          # Defense / nuclear
    "@tabzlive",        # Political/military analysis
    "@alibk3",          # Military hardware
    "@khabari_18",      # Flash alerts
    "@ne_wg",           # Geopolitical
]
```

### Keyword-to-Asset Mapping
```python
KEYWORD_IMPACT = {
    # Critical - immediate gold/USD spike
    "موشک بالستیک": {"gold": +15, "usd": +12, "oil": +25, "stocks": -20},
    "حمله پهپادی": {"gold": +10, "usd": +8, "oil": +15, "stocks": -12},
    "نطنز": {"gold": +25, "usd": +20, "oil": +20, "stocks": -30},
    "فردو": {"gold": +25, "usd": +20, "oil": +20, "stocks": -30},
    "خلیج فارس": {"gold": +8, "usd": +6, "oil": +40, "stocks": -15},
    "هرمز": {"gold": +8, "usd": +6, "oil": +40, "stocks": -15},
    "صهیونیست": {"gold": +5, "usd": +4, "oil": +10, "stocks": -5},
    
    # High - proxy fronts
    "حزب‌الله": {"gold": +8, "usd": +6, "oil": +15, "stocks": -10},
    "حوثی": {"gold": +5, "usd": +4, "oil": +12, "stocks": -8},
    "عراق": {"gold": +5, "usd": +4, "oil": +10, "stocks": -5},
    "اربیل": {"gold": +10, "usd": +8, "oil": +15, "stocks": -12},
    "عین‌الاسد": {"gold": +12, "usd": +10, "oil": +18, "stocks": -15},
    
    # Diplomatic - de-escalation
    "مذاکره": {"gold": -5, "usd": -4, "oil": -8, "stocks": +8},
    "جایگزینی": {"gold": -8, "usd": -6, "oil": -10, "stocks": +10},
    "آسیب‌پذیری": {"gold": +3, "usd": +2, "oil": +5, "stocks": -3},
}
```

## Scenario Analysis Templates

### Scenario A: Limited Exchange (Current Baseline)
**Probability: 40%**
- Iran/Israel proxy strikes continue
- No Hormuz closure
- Sanctions status quo
- **Market Impact:** Gold +5-10%/month, USD +3-5%/month, Oil range-bound $80-95

### Scenario B: Major Escalation (Hormuz Threat)
**Probability: 25%**
- Mining/strikes in Strait of Hormuz
- Oil spikes to $120-150
- Iran uses proxies heavily
- **Market Impact:** Gold +30-50%, USD +25-40%, Oil +$40-70, Stocks -30-50%

### Scenario C: Direct Iran-US/Israel War
**Probability: 15%**
- Direct missile strikes on Iranian soil
- Nuclear facilities targeted
- Full mobilization
- **Market Impact:** Gold 2-3x, USD 2-3x, Oil $200+, Stocks -60-80%, Crypto 5-10x

### Scenario D: Diplomatic Breakthrough
**Probability: 20%**
- JCPOA revival or interim deal
- Sanctions relief phased
- **Market Impact:** Gold -20-30%, USD -15-25%, Oil -$15-25, Stocks +40-60%, Crypto -20%

## Positioning Strategies

| Scenario | Gold | USD/USDT | Oil | Stocks | Crypto | Cash (Toman) |
|----------|------|----------|-----|--------|--------|--------------|
| Current (A) | 25% | 25% | 10% | 20% | 10% | 10% |
| Escalation (B) | 40% | 30% | 15% | 5% | 5% | 5% |
| War (C) | 50% | 30% | 10% | 0% | 10% | 0% |
| Deal (D) | 10% | 10% | 5% | 40% | 5% | 30% |

## Alert Thresholds (Auto-Notify)

| Asset | Warning | Critical | Action |
|-------|---------|----------|--------|
| Gold 18k | >5% daily | >10% daily | Buy physical / coin |
| USD Remittance | >3% daily | >7% daily | Buy USDT / crypto |
| USDT | >2% premium | >5% premium | Arbitrage / exit |
| Brent Oil | >$5/day | >$15/day | Hedge / short stocks |
| Tehran Stock Index | >-3% | >-7% | Reduce exposure / hedge |
| BTC/USDT (Iran premium) | >10% | >20% | Sell premium / buy dip |

## Historical Correlations (2020-2024)

| Event | Date | Gold 18k Δ | USD Δ | Brent Δ | TSE Δ |
|-------|------|------------|-------|---------|-------|
| Soleimani strike | Jan 2020 | +18% | +12% | +8% | -15% |
| Ukraine war start | Feb 2022 | +22% | +15% | +45% | -20% |
| Mahsa Amini protests | Sep 2022 | +8% | +12% | +5% | -18% |
| Israel-Hamas war | Oct 2023 | +15% | +10% | +12% | -12% |
| Iran-Israel direct | Apr 2024 | +12% | +8% | +18% | -15% |
| Raisi helicopter crash | May 2024 | +5% | +3% | +3% | -5% |

## Quick Reference Card

```
🚨 WAR ALERT TRIGGERS (Auto-alert)
├── Critical: "موشک"، "نطنز"، "فردو"، "هرمز"، "اربیل"
├── High: "پهپاد"، "حزب‌الله"، "حوثی"، "عین‌الاسد"
├── Medium: "تهدید"، "مناور"، "تسلیح"
└── De-escalate: "مذاکره"، "توافق"، "جایگزینی"

📊 PORTFOLIO HEDGE RATIOS
├── Peace: Gold 20% / USD 20% / Stocks 40% / Crypto 10% / Cash 10%
├── Tension: Gold 30% / USD 30% / Stocks 20% / Crypto 10% / Cash 10%
├── Crisis: Gold 40% / USD 35% / Stocks 5% / Crypto 10% / Cash 10%
└── War: Gold 50% / USD 30% / Crypto 15% / Cash 5%

💡 RULE OF THUMB
• Gold leads USD by 2-6 hours in Iran
• USDT premium >5% = panic buying
• TSE drops 2x faster than it rises
• Crypto premium in Iran = 15-30% over global
• Physical gold/coin > paper/ETF in crisis
```

## Cron Jobs

```bash
# Market monitor every 30 min
*/30 * * * * python3 /scripts/market_monitor.py --check-alerts

# War intel every 30 min
*/30 * * * * python3 /scripts/war_intel.py --telegram-scan

# Full scenario update daily 08:00 Tehran
0 4 * * * python3 /scripts/scenario_update.py --all-scenarios

# Weekly deep-dive Friday 10:00 Tehran
0 6 * * 5 python3 /scripts/weekly_analysis.py --full-report
```

## References
- TGJU.org - Primary price source
- TSE.ir - Tehran Stock Exchange
- CBI.ir - Central Bank rates
- OPEC monthly reports
- IMF Iran country reports
- US Treasury sanctions lists
- UN Panel of Experts reports