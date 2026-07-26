# Site Status & Notes (Updated July 2026)

## Working Sites

### E-commerce (User-Required Sites)
| Site | URL | Status | Notes |
|------|-----|--------|-------|
| Digikala | digikala.com | ✅ Works | Best for electronics, JS-heavy rendering |
| Basalam | basalam.com | ✅ API | Fastest method, direct API call |
| Sheypoor | sheypoor.com | ✅ Works | Classifieds, prices may be in Rial — verify unit! |
| Divar | divar.ir | ✅ Works | Classifieds, prices in Toman |
| Torob | torob.com | ⚠️ CAPTCHA | Anti-bot from cloud IPs, sometimes works |
| Emalls | emalls.ir | ⚠️ Timeout | SSL issues, sometimes accessible |
| Zoomit | zoomit.it | ⚠️ Works | Tech news/comparison, limited product data |
| Computer Parsian | parsiancomputer.com | ⚠️ Works | Computer parts specialist |
| eSAm | esam.ir | ⚠️ Works | Electronics marketplace |
| Snapp Market | snapp.market | ⚠️ Works | Grocery/delivery, limited electronics |
| Tapsi | tapsi.ir | ❌ | Ride-hailing, not a shop |

### Additional E-commerce
| Site | URL | Status | Notes |
|------|-----|--------|-------|
| Technolife | technolife.com | ✅ Works | Slower, good for electronics |
| Digistyle | digistyle.com | ✅ Works | Fashion/beauty focused |
| Sodamarket | sodamarket.com | ✅ Works | General products |
| Modiseh | modiseh.com | ✅ Works | Fashion/clothing |
| Bazargan | bazargan.com | ✅ Works | Industrial/tools |
| Nashr | nashr.com | ✅ Works | Books |
| Mobile.ir | mobile.ir | ✅ Works | Mobile phones |

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
| Bamilo | bamilo.com | ❌ SSL Error | Certificate issues |
| Bigmart | bigmart.co | ❌ Access Denied | Anti-bot protection |
| Shenoto | shenoto.com | ❌ Wrong site | Now a podcast platform, not classifieds |

## URL Patterns

### E-commerce Search
- Digikala: `https://www.digikala.com/search/?q={query}`
- Basalam API: `https://services.basalam.com/web/v1/search/product/search?from=0&q={encoded}&size=10`
- Sheypoor: `https://sheypoor.com/search?q={query}`
- Divar: `https://divar.ir/s/tehran/computers` (change category/city as needed)
- Technolife: `https://www.technolife.com/search?q={query}`
- Digistyle: `https://www.digistyle.com/search?q={query}`
- Sodamarket: `https://www.sodamarket.com/search?q={query}`
- Modiseh: `https://modiseh.com/search?q={query}`
- Zoomit: `https://www.zoomit.ir/search?q={query}`
- Torob: `https://torob.com/search/?query={query}`

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

### Sheypoor
Format: product name, then price on next line. NO unit shown — verify manually.
Example: `مادربرد ایسوس H81 Plus` then `۴,۹۰۰,۰۰۰`

### Basalam API
JSON response with `price` field (integer, in Toman).

## Currency Detection Rules

1. **Divar**: Always shows "تومان" explicitly
2. **Basalam API**: Always in Toman
3. **Sheypoor**: NO unit shown — could be Rial OR Toman. Check product page.
4. **Digikala**: NO unit shown — assumed Toman (standard for modern Iranian e-commerce)
5. **Default assumption**: If no unit visible, assume Toman (most Iranian shops use Toman)
6. **When uncertain**: Flag it to the user: "قیمت بدون واحد نمایش داده شده — احتمالاً تومان"
