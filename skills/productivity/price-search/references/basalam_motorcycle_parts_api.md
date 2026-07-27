# Basalam API — Motorcycle Parts Search

## API Endpoint
```
GET https://services.basalam.com/web/v1/search/product/search
```

## Required Headers
```
Origin: https://basalam.com
Referer: https://basalam.com/
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
```

## Parameters
| Param | Description | Example |
|-------|-------------|---------|
| `q` | Search query (URL encoded) | `%D8%AA%DB%8C%D9%88%D8%A8%20%D8%B9%D9%82%D8%A8%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125` |
| `from` | Pagination offset | `0` |
| `size` | Results per page | `20` |

## Sample Query: Honda CG125 Rear Tube
```
https://services.basalam.com/web/v1/search/product/search?from=0&q=%D8%AA%DB%8C%D9%88%D8%A8%20%D8%B9%D9%82%D8%A8%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125&size=20
```

## Response Structure
```json
{
  "products": [
    {
      "id": 33119763,
      "name": "تیوب عقب و جلو موتور هوندا",
      "price": 5300000,
      "primaryPrice": 5300000,
      "vendor": {
        "name": "سیکلت پارت (شکیبا)",
        "city": "آزادشهر",
        "username": "مهران روحانی"
      },
      "stock": 3,
      "sales_count": 15,
      "rating": { "average": 4.6, "count": 5 },
      "photos": [
        { "MEDIUM": "https://statics.basalam.com/...jpg_512X512X70.jpg" }
      ],
      "tags": [{ "title": "مرجوعی بدون شرط" }]
    }
  ],
  "meta": { "count": 10000 }
}
```

## Price Extraction
- `price` / `primaryPrice` = **Toman** (always)
- No conversion needed
- All Basalam prices are in Toman

## CG125 Specific Search Terms
| Part | Persian Query | URL Encoded |
|------|---------------|-------------|
| Rear tire | `تیوب عقب هوندا 125` | `%D8%AA%DB%8C%D9%88%D8%A8%20%D8%B9%D9%82%D8%A8%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125` |
| Front tire | `تیوب جلو هوندا 125` | `%D8%AA%DB%8C%D9%88%D8%A8%20%D8%AC%D9%84%D9%88%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125` |
| Chain | `زنجیر هوندا 125` | `%D8%B2%D9%86%D8%AC%DB%8C%D8%B1%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125` |
| Rear sprocket | `دنده عقب هوندا 125` | `%D8%AF%D9%86%D8%AF%D9%87%20%D8%B9%D9%82%D8%A8%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125` |
| Battery | `باتری هوندا 125` | `%D8%A8%D8%A7%D8%AA%D8%B1%DB%8C%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125` |
| Oil filter | `فیلتر روغن هوندا 125` | `%D9%81%DB%8C%D9%84%D8%AA%D8%B1%20%D8%B1%D9%88%D8%BA%D9%86%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125` |

## Verified Results (Mordad 1405 / July 2026)
| Part | Brand | Price (Toman) | Seller | City |
|------|-------|---------------|--------|------|
| Rear+Front tube | Generic | 5,300,000 | سیکلت پارت | آزادشهر |
| Rear tube | Yas | 8,120,000 | اسدالله پور | تایباد |
| Rear tube | Yazd Tire 300-17 | 6,130,350 | یدکی موتور ماهان | رشت |
| Rear+Front tube | Click (not CG125) | 4,000,000 | خیرآبادی | سبزوار |
| Rear tube | Yazd 300/17 | 5,700,000 | یدک سیکلت فرامرز | ورامین |
| Rear tube | Yazd 300-17 | 8,739,800 | فرمونی | قم |
| Rear tube | Yas 18-250 | 5,700,000 | سلیم زاده | خواجه |
| Rear tube | Yas 17-300 | 5,900,000 | سلیم زاده | خواجه |

## Notes
- Results include new, used, and Chinese copy parts
- Always verify size (3.00-17 vs 3.00-18) before purchase
- Seller ratings (4.5+) and sales_count indicate reliability
- "مرجوعی بدون شرط" = no-questions-asked return policy