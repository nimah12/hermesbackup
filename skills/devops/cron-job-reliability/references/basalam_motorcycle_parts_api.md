# Basalam API Response Patterns — Motorcycle Parts

**Endpoint:** `https://services.basalam.com/web/v1/search/product/search`
**Date:** 2026-07-27
**Query:** `تیوب عقب هوندا 125`

---

## Request Parameters

```bash
curl "https://services.basalam.com/web/v1/search/product/search?from=0&q=%D8%AA%DB%8C%D9%88%D8%A8%20%D8%B9%D9%82%D8%A8%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125&size=20" \
  -H "Origin: https://basalam.com" \
  -H "Referer: https://basalam.com/" \
  -H "User-Agent: Mozilla/5.0"
```

---

## Key Response Fields

```json
{
  "products": [
    {
      "id": 33119763,
      "name": "پژو 405 و پرشیا شوتی درب بازشو مای توی",
      "price": 5800000,           // Price in Toman
      "primaryPrice": 5800000,
      "photo": {
        "MEDIUM": "https://statics.basalam.com/.../image.jpg_512X512X70.jpg",
        "SMALL": "https://statics.basalam.com/.../image.jpg_256X256X70.jpg"
      },
      "vendor": {
        "id": 394789,
        "identifier": "toy_land2022",
        "name": "سرزمین اسباب بازی 2022",
        "city": "کرج",
        "provinceId": 7,
        "owner": {"hashId": "dLVeO1", "name": "مهران روحانی"}
      },
      "rating": {"average": 4.6, "count": 5},
      "sales_count": 15,
      "stock": 3,
      "status": {"id": 2976, "title": "در دسترس"},
      "tags": [{"badge_color": "gray", "title": "مرجوعی بدون شرط"}]
    }
  ],
  "facets": {
    "query_category": {
      "by_id": {
        "106": {"slug": "car-accessory-parts", "doc_count": 590},
        "110": {"slug": "car-spare-parts", "doc_count": 673}
      }
    }
  },
  "meta": {"count": 10000, "took": 33}
}
```

---

## Motorcycle Tube Results (Honda 125 Rear)

| # | Product Name | Brand/Size | Price (Toman) | Vendor | City | Stock |
|---|--------------|------------|---------------|--------|------|-------|
| 1 | تیوب عقب و جلو موتور هوندا | - | **5,300,000** | سیکلت پارت (شکیبا) | آزادشهر | 6 sold |
| 2 | تیوب عقب هوندا یاسا | - | **8,120,000** | لوازم یدکی اسدالله پور | تایباد | - |
| 3 | تیوب عقب هوندا یزد تایر | سایز ۳۰۰-۱۷ | **6,130,350** (disc: 6,453,000) | یدکی موتور ماهان | رشت | 20 |
| 4 | تیوب عقب و جلو انواع کلیک | - | **4,000,000** | قطعات موتورسیکلت خیرآبادی | سبزوار | 5 sold |
| 5 | تیوب عقب هوندا ۳۰۰/۱۷ (برند یزد) | - | **5,700,000** | یدک سیکلت فرامرز | ورامین | - |
| 6 | تیوب عقب موتورسیکلت هوندا یزد سایز ۳۰۰-۱۷ | - | **8,739,800** (disc: 9,820,000) | فرمونی | قم | 20 |
| 7 | تیوب یاسا شماره ۱۸-۲۵۰ هوندا | - | **5,700,000** | لوازم یدکی سلیم زاده | خواجه | 20 |
| 8 | تیوب یاسا شماره ۱۷-۳۰۰ هوندا | - | **5,900,000** | لوازم یدکی سلیم زاده | خواجه | 20 |
| 9 | تیوب جلو هوندا ۲۵۰/۱۸ (برند یزد تایر) | - | **5,700,000** | یدک سیکلت فرامرز | ورامین | - |
| 10 | تیوب عقب ۳۰۰/۱۸ یزد تایر | - | **5,000,000** | رود درخشان | بهارستان | - |

---

## Price Analysis

| Metric | Value (Toman) |
|--------|---------------|
| **Min** | 4,000,000 (تیوب کلیک - not specific to Honda 125) |
| **Min (Honda 125 specific)** | **5,000,000** (تیوب عقب ۳۰۰/۱۸ یزد تایر) |
| **Average** | ~6,200,000 |
| **Max** | 8,739,800 (تیوب یزد سایز ۳۰۰-۱۷ با تخفیف) |

---

## Recommended Options

| Option | Price | Reason |
|--------|-------|--------|
| **تیوب عقب ۳۰۰/۱۸ یزد تایر** | 5,000,000 | Cheapest reputable brand (Yazd), standard size |
| **تیوب عقب هوندا یزد تایر ۳۰۰-۱۷** | 6,130,350 | Yazd brand, 300-17 size, 20 in stock |
| **تیوب عقب و جلو هوندا** | 5,300,000 | Complete front+rear set, 6 sales, 5★ rating |

---

## Technical Notes

1. **Price field:** `price` and `primaryPrice` are in **Toman** (not Rial)
2. **Discounts:** Check `primaryPrice` vs `price` — if different, discount applied
3. **Images:** Use `photo.MEDIUM` for 512px, `photo.SMALL` for 256px
4. **Vendor info:** Nested in `vendor` object with `city`, `provinceId`, `owner.name`
5. **Availability:** `status.id` 2976 = "در دسترس" (in stock)
6. **Pagination:** Use `from` (offset) and `size` (page size, max 50)
7. **Categories:** Results include mixed categories (toys, parts) — filter by `categoryTitle` or vendor

---

## Parsing Code Snippet

```python
async def search_basalam_motorcycle(query: str, size: int = 20):
    url = "https://services.basalam.com/web/v1/search/product/search"
    params = {"from": 0, "q": query, "size": size}
    headers = {
        "Origin": "https://basalam.com",
        "Referer": "https://basalam.com/",
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            data = await resp.json()
    
    results = []
    for p in data.get("products", []):
        results.append({
            "name": p["name"],
            "price_toman": p["price"],
            "vendor": p["vendor"]["name"],
            "city": p["vendor"]["city"],
            "rating": p.get("rating", {}).get("average"),
            "sales": p.get("sales_count", 0),
            "stock": p.get("stock"),
            "image": p["photo"]["MEDIUM"],
            "url": f"https://basalam.com/p/{p['id']}"
        })
    return results
```