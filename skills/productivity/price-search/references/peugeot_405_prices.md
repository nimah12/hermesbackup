# Peugeot 405 Price Search — Iranian Market (Divar)

## Source
- **Primary**: Divar (https://divar.ir/s/tehran/car?q=پژو+405)
- **API**: `https://api.divar.ir/v8/web-search/1/vehicles`
- **JSON-LD**: Schema.org `Car` markup in listing pages

## Search URL Pattern
```
https://divar.ir/s/tehran/car?q=%D9%BE%DA%98%D9%88%20405
```

## Divar JSON-LD Structure (Schema.org Car)
```json
{
  "@type": "Car",
  "name": "پژو ۴۰۵ مدل ۱۳۸۵ دوگانه شرکتی",
  "url": "https://divar.ir/v/پژو-۴۰۵-مدل-۱۳۸۵-دوگانه-شرکتی/ganRhIQ4",
  "image": "https://postimage01.divarcdn.com/...webp",
  "model": "Peugeot 405 GLX-petrol",
  "category": "light",
  "vehicleTransmission": "manual",
  "productionDate": "1385",
  "knownVehicleDamages": "some-paint",
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceCurrency": "IRR",
    "price": "6800000000"
  },
  "mileageFromOdometer": {
    "@type": "QuantitativeValue",
    "unitCode": "KMT",
    "value": "241000"
  },
  "color": "نقره‌ای",
  "web_info": {
    "title": "پژو ۴۰۵ مدل ۱۳۸۵ دوگانه شرکتی",
    "city_persian": "تهران",
    "district_persian": "وردآورد",
    "category_slug_persian": "سواری و وانت"
  }
}
```

## Key Fields
| Field | JSON Path | Notes |
|-------|-----------|-------|
| Title | `name` / `web_info.title` | Persian title |
| Price (Rial) | `offers.price` | **Convert: ÷10 = Toman** |
| Year | `productionDate` | Persian year (1385 = 2006) |
| Mileage (km) | `mileageFromOdometer.value` | Integer |
| Transmission | `vehicleTransmission` | manual/automatic |
| Color | `color` | Persian |
| Body Damage | `knownVehicleDamages` | intact/some-paint/half-paint/some-scratches |
| City/District | `web_info.city_persian` / `district_persian` | |
| Link | `url` | Full Divar URL |
| Image | `image` | Thumbnail URL |

## Price Conversion
```python
# Divar prices are in IRR (Rial)
price_toman = int(price_rial) // 10
# Example: "6800000000" -> 680,000,000 Toman
```

## Verified Listings (Mordad 1405 / July 2026)

| Model/Trim | Year | Mileage | Body | Price (Toman) | District | Link |
|------------|------|---------|------|---------------|----------|------|
| 405 2000 | 1379 | 111,110 | some-scratches | **265,000,000** | پیکان شهر | [View](https://divar.ir/v/پژو-۴۰۵-2000/ganRhLXz) |
| GLX CNG (دوگانه) | 1385 | 241,000 | some-paint | **680,000,000** | وردآورد | [View](https://divar.ir/v/پژو-۴۰۵-مدل-۱۳۸۵-دوگانه-شرکتی/gaMFvBcK) |
| GLX بنزینی | 1391 | 350,000 | half-paint | **620,000,000** | فردوس | [View](https://divar.ir/v/پژو-۴۰۵-بنزینی-جی-ال-ایکس-glx/gaHd8ZMv) |
| GLX دوگانه کارخانه | 1385 | 310,000 | half-paint | **580,000,000** | جیحون | [View](https://divar.ir/v/پژو-۴۰۵-glx-مدل-۱۳۸۵-نقره-ای/gantgFKc) |
| GLX 1800 | 1382 | 325,000 | half-paint | **545,000,000** | کیانشهر | [View](https://divar.ir/v/پژو-405-مدل-82-glx1800/gantQVa-) |
| مدل ۸۹ | 1389 | 280,000 | half-paint | **620,000,000** | نیروی هوایی | [View](https://divar.ir/v/پژو-۴۰۵-مدل-۸۹/gac5WnBR) |
| مدل ۸۹ (دیگه) | 1389 | 350,000 | half-paint | **640,000,000** | توحید | [View](https://divar.ir/v/پژو-۴۰۵-مدل-۸۹/ganlgLNt) |
| تک‌برگ سند، بدون رنگ | 1389 | 300,000 | intact | **750,000,000** | تهرانسر | [View](https://divar.ir/v/پژو-405تکglx-تک-برگ-سند-بدون-رنگ/gakJ_lFu) |
| GLX دوگانه کارخانه | 1396 | 250,000 | some-scratches | **870,000,000** | نیروی هوایی | [View](https://divar.ir/v/پژو-405-glx-دوگانه-کارخانه/gan1AMjC) |
| مدل ۸۵ تمیز، کم‌کار | 1385 | 241,000 | some-paint | **680,000,000** | وردآورد | [View](https://divar.ir/v/پژو-۴۰۵-مدل-۸۵-تمیز-و-سالم-کم-کار-۲۷۰/gaMFvBcK) |
| مدل ۸۲، فقط ۶۹ تا کار | 1382 | 69,000 | some-scratches | **1,200,000,000** | دردشت | [View](https://divar.ir/v/پژو-405-مدل-82-فقط-۶۹-تا-کار-به-شرط-در-حد-خشک/gaB50pJ0) |
| مدل ۹۳ بیرنگ، شاسی پلمب | 1393 | 170,000 | *no damage listed* | *call for price* | - | [View](https://divar.ir/v/پژو-۴۰۵-مدل-۹۳بیرنگ-شاسی-پلمب/ganlgLNt) |

## Price Analysis (Mordad 1405)

| Category | Range (Toman) | Median | Notes |
|----------|---------------|--------|-------|
| **GLX CNG (factory) 1385-1396** | 580M - 870M | ~680M | Most popular |
| **GLX Petrol 1385-1391** | 545M - 680M | ~620M | Cheaper than CNG |
| **Low mileage (<100k) / Mint** | 750M - 1,200M | ~900M | Premium for condition |
| **Older / High mileage (>300k)** | 265M - 545M | ~400M | Budget range |
| **No paint / Single owner / Clean title** | +100M - +300M premium | | |

## Search Tips
1. **Always filter by Tehran** for representative prices: `s/tehran/car`
2. **Try multiple queries**: `پژو 405`, `پژو ۴۰۵`, `Peugeot 405`, `405 GLX`
3. **Check body damage enum**: `intact` > `some-scratches` > `some-paint` > `half-paint`
4. **Verify mileage**: Common tampering on 405s — cross-check with service records
5. **CNG vs Petrol**: CNG (دوگانه) typically 50-100M more than petrol for same year

## Divar API Alternative
```
POST https://api.divar.ir/v8/web-search/1/vehicles
{
  "json_schema": {"category": {"value": "light"}},
  "last_post_date": 0
}
```
Returns structured data without HTML parsing.

## Bama Alternative
- URL: `https://bama.ir/car/peugeot/405`
- Extracts JSON-LD similar to Divar
- More dealer listings, fewer private sellers
- Prices typically 10-20% higher than Divar

## Sheypoor Alternative
- URL: `https://www.sheypoor.com/iran/car/peugeot/405`
- Schema.org markup similar
- Good for provincial listings outside Tehran