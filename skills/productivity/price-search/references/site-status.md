# Site Status & Notes (Updated July 2026)

## Working Sites

### E-commerce
| Site | URL | Status | Notes |
|------|-----|--------|-------|
| Digikala | digikala.com | ✅ Works | Best for electronics, JS-heavy rendering |
| Basalam | basalam.com | ✅ API | Fastest method, direct API call |
| Technolife | technolife.com | ✅ Works | Slower, good for electronics |
| Digistyle | digistyle.com | ✅ Works | Fashion/beauty focused |
| Sodamarket | sodamarket.com | ✅ Works | General products |
| Modiseh | modiseh.com | ✅ Works | Fashion/clothing |

### Cars & Motorcycles
| Site | URL | Status | Notes |
|------|-----|--------|-------|
| Divar | divar.ir | ✅ Works | Best for used cars/motorcycles, city-specific URLs |
| Bama | bama.ir | ✅ Works | Largest car marketplace |
| Khodro45 | khodro45.com | ✅ Works | Car listings |
| Khodrobank | khodrobank.com | ✅ Works | Car prices & reviews |
| Hamrah Mechanic | hamrah-mechanic.com | ✅ Works | Car marketplace |

### Blocked / Deprecated
| Site | URL | Status | Issue |
|------|-----|--------|-------|
| Torob | torob.com | ❌ CAPTCHA | Anti-bot protection from cloud IPs |
| Emalls | emalls.ir | ❌ SSL Error | Certificate expired |
| Bamilo | bamilo.com | ❌ SSL Error | Certificate issues |
| Bigmart | bigmart.co | ❌ Access Denied | Anti-bot protection |
| Shenoto | shenoto.com | ❌ Wrong site | Now a podcast platform, not classifieds |

## URL Patterns

### E-commerce Search
- Digikala: `https://www.digikala.com/search/?q={query}`
- Basalam API: `https://services.basalam.com/web/v1/search/product/search?from=0&q={encoded}&size=10`
- Technolife: `https://www.technolife.com/search?q={query}`
- Digistyle: `https://www.digistyle.com/search?q={query}`
- Sodamarket: `https://www.sodamarket.com/search?q={query}`
- Modiseh: `https://modiseh.com/search?q={query}`

### Car/Motorcycle
- Divar Cars: `https://divar.ir/s/tehran/car` (change city as needed)
- Divar Motorcycles: `https://divar.ir/s/tehran/motorcycle`
- Bama: Requires search input interaction (no direct URL)
- Khodrobank: `https://khodrobank.com/search?q={query}`
- Hamrah Mechanic: `https://hamrah-mechanic.com/search?q={query}`

## Persian Numeral Conversion

```python
PERSIAN_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
text.translate(PERSIAN_DIGITS)
```

## Price Format Patterns

### E-commerce
Product name on one line, price on a nearby line (within 15 lines).

### Divar
Format: `car name | mileage | price تومان`
Example: `پراید ۱۳۲ | ۲۳۰ کیلومتر | ۵۲۰,۰۰۰,۰۰۰ تومان`

### Basalam API
JSON response with `price` field (integer, in Toman).
