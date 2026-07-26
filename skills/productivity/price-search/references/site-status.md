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
| Divar | divar.ir | ⚠️ Slow/Timeout | Best for used cars/motorcycles, city-specific URLs. **Playwright times out (60s+)**. Use API or simple curl + regex instead. |
| Bama | bama.ir | ⚠️ Slow/Timeout | Largest car marketplace. **No direct search URL** — requires search input interaction. Playwright often times out. |
| Khodro45 | khodro45.com | ✅ Works | Car listings, simpler HTML |
| Khodrobank | khodrobank.com | ✅ Works | Car prices & reviews |
| Hamrah Mechanic | hamrah-mechanic.com | ✅ Works | Car marketplace |

### Financial Markets (Gold/Currency/Crypto) — **Primary Sources**
| Site | URL | Status | Notes |
|------|-----|--------|-------|
| **tgju.org** | tgju.org | ✅ **Best for live prices** | **Tehran Gold & Currency Exchange — PRIMARY SOURCE**. Profiles: `geram18` (18k gold/gram), `price_dollar_rl` (USD), `price_usdt_rl` (USDT), `emami1` (Emami coin), `bahar_azadi` (Bahar Azadi coin). **Real-time, no Playwright needed** (simple curl works). All prices in RIAL (÷10 = Toman). |
| mesghal.com | mesghal.com | ✅ Works | Good for gold/coin, but prices may be daily not live. HTML is clean. |
| bonbast.com | bonbast.com | ⚠️ Needs Playwright | Gold + currency combined. IDs: #usd1, #usd2, #gol18_top, #emami1_top. |
| tala.ir | tala.ir | ✅ Works | News + prices, daily updates. |
| bestchange.com | bestchange.com | ✅ Works | USDT/exchanger rates. Simple HTML tables. |
| tala.ir | tala.ir | ✅ Works | News + prices, daily updates. |

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
**List View Format**: `car name | mileage` (NO price in list — must visit detail page)
Example: `پراید ۱۳۲ | ۲۳۰ کیلومتر`
**Detail Page**: Price appears with "تومان" suffix

**Working Selectors (July 2026)**:
- Container: `article.kt-post-card` or `class="kt-post-card kt-post-card--outlined"`
- Title: `class="kt-post-card__title"`
- Description/Mileage: `class="kt-post-card__description"`
- Link: `href="/v/{token}"`

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
