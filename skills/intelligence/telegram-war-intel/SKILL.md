---
name: telegram-war-intel
description: "Monitor Iranian Telegram channels for war/conflict alerts."
tags: [war, iran, telegram, intel, conflict, middle-east]
---

# Telegram War Intelligence — Iranian Conflict Monitoring

Monitor Iranian Telegram channels for real-time war/conflict alerts, missile strikes, proxy escalations, US base attacks.

## When to Use
- Need real-time alerts on Iran-Israel-US tensions
- Monitoring missile/drone attacks, proxy fronts (Hezbollah, Houthis, PMF)
- Track Middle East escalation indicators
- Daily/weekly threat assessment reports

## Source Channels (10+ Verified)

| Channel | Handle | Focus | Reliability |
|---------|--------|-------|-------------|
| Iran International TV | @iranintltv | Breaking Iran news, military | ⭐⭐⭐⭐⭐ |
| Khamenei.ir (Persian) | @km_ap | Supreme Leader statements | ⭐⭐⭐⭐⭐ |
| Tasnim News | @tasnimnews | IRGC, military, foreign policy | ⭐⭐⭐⭐ |
| Fars News | @farsna | IRGC, defense, nuclear | ⭐⭐⭐⭐ |
| Tabnak | @tabzlive | Political/military analysis | ⭐⭐⭐ |
| Alibk3 | @alibk3 | Military hardware, strikes | ⭐⭐⭐ |
| Khabari 18 | @khabari_18 | Breaking alerts | ⭐⭐⭐ |
| Ne_Wg | @ne_wg | Geopolitical analysis | ⭐⭐⭐ |

## Keyword Triggers (Auto-Alert)

### Direct Attacks
- موشک، راکت، پهپاد، درون، حمله، درگیری، جنگ، تهدید
- missile, rocket, drone, uav, attack, strike, war, threat
- شهید، کمان، دفاع، air defense، س-۳۰۰، باور-۳۷۳

### Proxy Fronts
- حزب‌الله،حوثی، حماس، جهاد اسلامی، هاشدم شعبی
- Hezbollah, Houthi, Hamas, PIJ, PMF, Hashd al-Shaabi
- لبنان، سوریه، عراق، یمن، غزه
- Lebanon, Syria, Iraq, Yemen, Gaza

### Strategic Assets
- نطنز، فردو، بوشهر، خارک، خلیج فارس، هرمز
- Natanz, Fordow, Bushehr, Kharg, Persian Gulf, Hormuz
- تسلیحات هسته‌ای، غنی‌سازی، centrifuges
- nuclear, enrichment, centrifuge

### US/Israel Presence
- آمریکا، اسرائیل، پایگاه، عین‌الاسد، اربیل، بغداد
- USA, Israel, base, Ain al-Asad, Erbil, Baghdad
- پنتاگون، سنتکم، ناو، حامل هواپیما
- Pentagon, CENTCOM, carrier, destroyer

## Alert Thresholds

| Level | Trigger | Action |
|-------|---------|--------|
| 🔴 CRITICAL | Direct Iran/Israel/US kinetic action | Immediate Telegram alert |
| 🟠 HIGH | Proxy attack on US/Israel assets | Alert within 5 min |
| 🟡 MEDIUM | Threat rhetoric, mobilization | Daily digest |
| 🟢 LOW | Routine exercises, statements | Weekly summary |

## Extraction Script (Python)

```python
import asyncio
import aiohttp
import re
from datetime import datetime, timezone, timedelta

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))

CHANNELS = [
    "iranintltv", "km_ap", "tasnimnews", "farsna",
    "tabzlive", "alibk3", "khabari_18", "ne_wg",
]

KEYWORDS = {
    "critical": ["موشک", "پهپاد", "حمله", "درگیری", "شهید", "کمان", "نطنز", "فردو"],
    "high": ["حزب‌الله", "حوثی", "حماس", "پنتاگون", "اربیل", "عین‌الاسد", "حامل‌هواپیما"],
    "medium": ["تهدید", "مناور", "تسلیح", "غنی‌سازی", "صهیونیست", "استکبار"],
}

async def fetch_channel(session, channel):
    url = f"https://t.me/s/{channel}"
    try:
        async with session.get(url, timeout=15) as resp:
            html = await resp.text()
            return html
    except Exception as e:
        return None

def parse_messages(html, channel):
    messages = []
    pattern = r'data-post="[^"]*"[^>]*>.*?<div class="tgme_widget_message_text[^"]*">(.*?)</div>'
    for match in re.finditer(pattern, html, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1))
        text = text.replace('&nbsp;', ' ').strip()
        if len(text) > 20:
            messages.append({
                "channel": channel,
                "text": text[:500],
                "time": datetime.now(TEHRAN_TZ).isoformat(),
            })
    return messages

def classify_alert(text):
    text_lower = text.lower()
    for level, kws in KEYWORDS.items():
        for kw in kws:
            if kw in text_lower:
                return level
    return "low"

async def monitor_war_channels():
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [fetch_channel(session, ch) for ch in CHANNELS]
        results = await asyncio.gather(*tasks)
        
        all_alerts = []
        for channel, html in zip(CHANNELS, results):
            if html:
                msgs = parse_messages(html, channel)
                for msg in msgs[:10]:
                    level = classify_alert(msg["text"])
                    if level in ["critical", "high"]:
                        all_alerts.append({**msg, "level": level})
        
        return all_alerts
```

## Cron Integration
```bash
# Every 30 minutes for critical alerts
*/30 * * * * python3 /path/to/war_monitor.py --alert-only

# Every 3 hours for full digest
0 */3 * * * python3 /path/to/war_monitor.py --digest
```

## Output Format (JSON)
```json
{
  "alerts": [
    {
      "level": "critical",
      "channel": "@iranintltv",
      "text": "IRGC launches missiles at US base in Erbil...",
      "time": "2026-07-27T14:30:00+03:30",
      "keywords_matched": ["موشک", "اربیل", "پایگاه"]
    }
  ],
  "summary": "2 critical, 1 high alerts in last 3h"
}
```

## References
- Telegram web preview: https://t.me/s/<channel>
- No API key needed for public channels
- Rate limit: ~30 req/min per IP