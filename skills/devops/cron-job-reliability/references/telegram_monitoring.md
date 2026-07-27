# Telegram Monitoring Patterns Reference

## Overview
This document captures the verified patterns for monitoring Iranian Telegram channels via `t.me/s/` public preview pages.

## Channel List (Verified Working)

### Market Price Channels
| Channel | URL | Purpose | Frequency |
|---------|-----|---------|-----------|
| @se_pz | https://t.me/s/se_pz | Gold, coin, USD, USDT prices | 30 min |
| @talasea_ir | https://t.me/s/talasea_ir | Gold, coin, USD prices | 30 min |

### War/Conflict Intelligence Channels
| Channel | URL | Purpose | Frequency |
|---------|-----|---------|-----------|
| @iranintltv | https://t.me/s/iranintltv | Breaking Iran news, military | 30 min / 3h |
| @km_ap | https://t.me/s/km_ap | Khamenei statements | 30 min / 3h |
| @tasnimnews | https://t.me/s/tasnimnews | IRGC, military, foreign policy | 30 min / 3h |
| @farsna | https://t.me/s/farsna | Defense, nuclear | 30 min / 3h |
| @tabzlive | https://t.me/s/tabzlive | Political/military analysis | 30 min / 3h |
| @alibk3 | https://t.me/s/alibk3 | Military hardware, strikes | 30 min / 3h |
| @khabari_18 | https://t.me/s/khabari_18 | Flash alerts | 30 min / 3h |
| @ne_wg | https://t.me/s/ne_wg | Geopolitical analysis | 30 min / 3h |

## HTML Structure (t.me/s/ pages)

```html
<div class="tgme_widget_message_wrap js-widget_message_wrap">
  <div class="tgme_widget_message text_not_supported_wrap js-widget_message" 
       data-post="channel_name/349775" 
       data-view="...">
    <div class="tgme_widget_message_user">...</div>
    <div class="tgme_widget_message_bubble">
      <div class="tgme_widget_message_author accent_color">...</div>
      <div class="tgme_widget_message_text js-message_text" dir="auto">
        <!-- MESSAGE TEXT HERE -->
        طلا ۱۸ عیار: ۱۸,۱۵۶,۵۰۰ تومان
        سکه تمام: ۱۸۲,۳۰۰,۰۰۰ تومان
      </div>
      <div class="tgme_widget_message_footer compact js-message_footer">
        <span class="tgme_widget_message_views">40.1K</span>
        <a class="tgme_widget_message_date" href="https://t.me/channel/349775">
          <time datetime="2026-07-27T06:07:29+00:00" class="time">06:07</time>
        </a>
      </div>
    </div>
  </div>
</div>
```

## Regex Patterns

### Message Extraction (Primary - Verified)
```python
# Extracts text from tgme_widget_message_text divs
MESSAGE_PATTERN = r'<div class="tgme_widget_message_text[^"]*"[^>]*dir="auto">(.*?)</div>'
```

### Data-Post ID Extraction (for deduplication)
```python
DATA_POST_PATTERN = r'data-post="([^"]+)"'
```

### Price Patterns (Persian)
```python
PRICE_PATTERNS = {
    "gold_18k": [
        r'(?:طلای?\s*۱۸\s*عیار|گرم\s*طلای?\s*۱۸)\D*([\d,]{8,12})',
        r'(?:۱۸\s*عیار|18k)\D*([\d,]{8,12})',
    ],
    "gold_24k": [
        r'(?:طلای?\s*۲۴\s*عیار|گرم\s*طلای?\s*۲۴)\D*([\d,]{8,12})',
    ],
    "mesghal": [
        r'(?:مثقال\s*طلا|mesghal)\D*([\d,]{9,12})',
    ],
    "coin_full": [
        r'(?:سکه\s*(?:تمام|بهر|آزادی|کامل)|full\s*coin)\D*([\d,]{9,12})',
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

### War/Conflict Keywords
```python
WAR_KEYWORDS = {
    "critical": [
        "موشک", "موشک بالستیک", "پهپاد", "حمله", "درگیری", 
        "شهید", "کمان", "نطنز", "فردو", "خلیج فارس", "هرمز"
    ],
    "high": [
        "حزب‌الله", "حوثی", "حماس", "پنتاگون", "اربیل", 
        "عین‌الاسد", "حامل‌هواپیما", "سنتکام", "ایران", "اسرائیل"
    ],
    "medium": [
        "تهدید", "مناور", "تسلیح", "غنی‌سازی", "صهیونیست", 
        "استکبار", "آمریکا", "نیروی دریایی", "سپاه"
    ],
}
```

## Text Cleaning Pipeline

```python
def clean_telegram_text(text):
    """Clean HTML and entities from t.me/s/ message text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&zwj;', '')
    text = text.replace('&#8204;', '')  # ZWJ
    text = text.replace('\u200c', '')   # ZWJ char
    # Normalize Persian digits
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    ascii_digits = '0123456789'
    trans = str.maketrans(persian_digits, ascii_digits)
    text = text.translate(trans)
    # Normalize commas
    text = text.replace('،', ',')
    return text.strip()
```

## Validation Rules

### Price Ranges (Mordad 1405)
| Item | Min | Max | Unit |
|------|-----|-----|------|
| Gold 18k/24k per gram | 10,000,000 | 50,000,000 | Toman |
| Mesghal | 50,000,000 | 100,000,000 | Toman |
| Coin Full | 50,000,000 | 300,000,000 | Toman |
| Coin Half | 20,000,000 | 150,000,000 | Toman |
| Coin Quarter | 10,000,000 | 80,000,000 | Toman |
| USD/USDT | 50,000 | 200,000 | Toman |

### Alert Thresholds
- **Gold/Currency**: > 5% change
- **Oil**: > 3% change
- **War Intel**: Any CRITICAL or HIGH keyword match

## State Persistence

### Market Prices State
```json
{
  "prices": {
    "se_pz:gold_18k": 18156500,
    "se_pz:coin_full": 182300000,
    "talasea_ir:usd": 1515690
  },
  "last_check": "2026-07-27 10:42:23"
}
```

### War Intel State
```json
{
  "last_messages": {
    "iranintltv": "data-post-id-349775",
    "km_ap": "data-post-id-123456"
  },
  "last_alerts": [
    {"channel": "@iranintltv", "level": "critical", "keyword": "موشک", "time": "2026-07-27T06:07:29+03:30"}
  ],
  "last_check": "2026-07-27 10:42:23"
}
```

## Test Results (2026-07-27)

### Market Channels
| Channel | Messages | Prices Found |
|---------|----------|--------------|
| @se_pz | 20 | 5-8 per run |
| @talasea_ir | 20 | 5-8 per run |

### War Intel Channels
| Channel | Messages | Alerts (CRITICAL/HIGH) |
|---------|----------|------------------------|
| @iranintltv | 20 | 4 |
| @km_ap | 20 | 14 |
| @tasnimnews | 0 | 0 |
| @farsna | 20 | 5 |
| @tabzlive | 20 | 0 |
| @alibk3 | 20 | 0 |
| @khabari_18 | 15 | 3 |
| @ne_wg | 20 | 7 |

**Total**: 135 messages, 29 actionable alerts in single run

## Performance Notes

- **Fetch time**: ~2-5 seconds per channel
- **Total 8 channels**: ~15-20 seconds
- **Rate limit**: t.me/s/ allows ~30 req/min per IP
- **Recommendation**: Batch requests with async, add 0.5s delay between channels

## Common Issues

1. **Persian digits**: Messages use ۰-۹ → must translate
2. **ZWJ characters**: `&#8204;` and `\u200c` → strip
3. **HTML entities**: `&nbsp;`, `&zwj;` → decode
4. **Empty channels**: @tasnimnews returned 0 messages (may be rate-limited or structure changed)
5. **Video-only messages**: No text content, skip
6. **Duplicate messages**: Use `data-post` for dedup

## Cron Job Configuration

```yaml
# Market prices - every 30 min
schedule: "*/30 * * * *"
script: gold_alert_telegram.py
no_agent: true
enabled_toolsets: ["terminal", "file"]

# War intel - every 3 hours (or 30 min for critical)
schedule: "0 */3 * * *"
script: war_intel_monitor.py
no_agent: true
enabled_toolsets: ["terminal", "file"]
```