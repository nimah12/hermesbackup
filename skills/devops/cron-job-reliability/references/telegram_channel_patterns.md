# Telegram Channel Monitoring Reference

## Channels Used

| Channel | URL | Purpose |
|---------|-----|---------|
| @se_pz | https://t.me/s/se_pz | Gold, coin, USD, USDT prices |
| @talasea_ir | https://t.me/s/talasea_ir | Gold, coin, USD prices |

## t.me/s/ HTML Structure (Verified 2026-07-27)

The `t.me/s/` public preview pages contain messages in this structure:

```html
<div class="tgme_widget_message_wrap js-widget_message_wrap">
  <div class="tgme_widget_message text_not_supported_wrap js-widget_message" data-post="channel_name/349775" data-view="...">
    <div class="tgme_widget_message_user">...</div>
    <div class="tgme_widget_message_bubble">
      <div class="tgme_widget_message_author accent_color">...</div>
      <div class="tgme_widget_message_text js-message_text" dir="auto">
        <!-- Message text with prices/war intel -->
        طلا ۱۸ عیار: ۱۸,۱۵۶,۵۰۰ تومان
        سکه تمام: ۱۸۲,۳۰۰,۰۰۰ تومان
        دلار: ۱,۵۱۵,۶۹۰ تومان
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

## Regex Patterns for Extraction

### Message Container (Verified Working)

```python
# Main pattern for t.me/s/ pages - extracts text from js-message_text divs
MESSAGE_PATTERN = r'<div class="tgme_widget_message_text[^"]*"[^>]*dir="auto">(.*?)</div>'

# Alternative: data-post based
DATA_POST_PATTERN = r'data-post="[^"]*"[^>]*>.*?<div class="tgme_widget_message_text[^"]*"[^>]*dir="auto">(.*?)</div>'
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

## War/Conflict Keywords (For Alert Classification)

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

## Channel-Specific Notes

### @se_pz
- Posts frequent price updates
- Uses format: "طلا ۱۸ عیار: ۱۸,۱۵۶,۵۰۰ تومان"
- Also posts USD, USDT, coin prices

### @talasea_ir
- Focuses on gold and coin prices
- Format: "سکه تمام بهار آزادی: ۱۸۲,۳۰۰,۰۰۰ تومان"
- Posts Mesghal, half/quarter coin prices

## Common Issues

1. **Persian digits**: Messages use Persian numerals (۰-۹) - must convert
2. **ZWJ characters**: `&#8204;` (zero-width joiner) appears in text - strip with `.replace('\u200c', '')`
3. **HTML entities**: `&nbsp;`, `&zwj;` - decode before parsing
4. **Message deduplication**: Use `data-post` attribute for unique message IDs
5. **Rate limiting**: t.me/s/ allows frequent requests, but add small delay if needed

## Python Helpers

```python
def normalize_persian_digits(text):
    """Convert Persian digits to ASCII"""
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    ascii_digits = '0123456789'
    trans = str.maketrans(persian_digits, ascii_digits)
    return text.translate(trans)

def clean_message(text):
    """Clean Telegram message text"""
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = text.replace('&nbsp;', ' ').replace('&zwj;', '').replace('\u200c', '')
    text = normalize_persian_digits(text)
    return text.strip()
```

---

## War Intel Channels (Additional)

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

## War Intel HTML Structure (Same as above)

Messages use same `tgme_widget_message_text js-message_text` class.