# Telegram Channel Quick Reference

## War/Conflict Alert Channels (8)

| Channel | URL | Focus |
|---------|-----|-------|
| @iranintltv | https://t.me/iranintltv | Iran International TV — breaking news, military |
| @km_ap | https://t.me/km_ap | Khabar Melli / AP — official news, alerts |
| @ne_wg | https://t.me/ne_wg | News/World/Geopolitics — regional conflict |
| @tasnimnews | https://t.me/tasnimnews | Tasnim News Agency — IRGC-linked, military |
| @tabzlive | https://t.me/tabzlive | Live updates, breaking news |
| @alibk3 | https://t.me/alibk3 | Military analysis, strategic |
| @farsna | https://t.me/farsna | Fars News Agency — official, military |
| @khabari_18 | https://t.me/khabari_18 | News 18 — breaking, alerts |

## Market Analysis Channels (4)

| Channel | URL | Focus |
|---------|-----|-------|
| @talasea_ir | https://t.me/talasea_ir | Gold, coin, technical analysis |
| @ecoshariff | https://t.me/ecoshariff | Economy, currency, market views |
| @se_pz | https://t.me/se_pz | Market signals, technical |
| @eco_roozbeh | https://t.me/eco_roozbeh | Daily economy, prices, news |

---

## Playwright Selectors for t.me/channelname

```python
# Basic pattern for public channel pages
await page.goto(f"https://t.me/{channel_name}", wait_until="domcontentloaded")
await page.wait_for_timeout(3000)

# Messages are in:
# - .tgme_widget_message_wrap (each message)
# - .tgme_widget_message_text (message text)
# - .tgme_widget_message_date (timestamp link)
# - .tgme_widget_message_photo_wrap (images)

# Get last ~20 messages:
messages = await page.query_selector_all('.tgme_widget_message_wrap')
for msg in messages[-20:]:
    text = await msg.query_selector('.tgme_widget_message_text')
    date_link = await msg.query_selector('.tgme_widget_message_date a')
    # Extract message_id from date_link href: https://t.me/channel/12345
```

---

## High-Confidence War Keywords (Persian)

### Must-Alert (Immediate)
- موشک، راکت، پهپاد، درون → Missile/Drone
- حمله، هدف‌گذاری، انفجار → Attack/Explosion
- درگیری، جنگ، تهاجم → Combat/War/Invasion
- opérations نظامی → Military Operation
- اخطار، هشدار فوری → Alert/Urgent Warning
- هوانوردی، حاملات جنگی → Air Force/Carriers
- حالت جنگ → War Status

### Iran-Direct (Higher Priority)
- ایران، تسه‌های هسته‌ای → Iran, Nuclear Sites
- سپاه، ارتش، بسیج → IRGC, Army, Basij
- موشک بالستیک → Ballistic Missile

### Regional Escalation
- اسرائیل، اسرائیل → Israel
- حزب‌الله، حوفی‌ها → Hezbollah, Houthis
- سوریه، لبنان، عراق، یمن → Syria, Lebanon, Iraq, Yemen
- آمریکا، نیروی دریایی آمریکا → US, US Navy

---

## Filtering Logic (Pseudo-code)

```python
WAR_KEYWORDS = [
    'موشک', 'راکت', 'پهپاد', 'درون', 'حمله', 'هدف‌گذاری', 'انفجار',
    'درگیری', 'جنگ', 'تهاجم', 'عملیات نظامی', 'اخطار', 'هشدار',
    'هوانوردی', 'حاملات', 'حالت جنگ', 'موشک بالستیک',
    'ایران', 'تسه هسته', 'سپاه', 'ارتش', 'بسیج',
    'اسرائیل', 'حزب‌الله', 'حوفی', 'سوریه', 'لبنان', 'عراق', 'یمن',
    'آمریکا', 'نیروی دریایی'
]

def is_war_alert(text: str) -> bool:
    text_lower = text.lower()
    # Must have at least 2 high-confidence keywords
    # OR 1 very high-confidence keyword
    high_conf = ['موشک', 'جنگ', 'درگیری', 'حمله', 'تهاجم', 'اخطار']
    matches = sum(1 for kw in WAR_KEYWORDS if kw in text_lower)
    high_matches = sum(1 for kw in high_conf if kw in text_lower)
    return high_matches >= 1 or matches >= 2
```

---

## Message ID Tracking

Store in `/data/.hermes/telegram_alert_state.json`:

```json
{
  "iranintltv": 123456,
  "km_ap": 789012,
  "ne_wg": 345678,
  "tasnimnews": 901234,
  "tabzlive": 567890,
  "alibk3": 234567,
  "farsna": 890123,
  "khabari_18": 456789,
  "talasea_ir": 111111,
  "ecoshariff": 222222,
  "se_pz": 333333,
  "eco_roozbeh": 444444
}
```

Only process messages with ID > stored ID for each channel.