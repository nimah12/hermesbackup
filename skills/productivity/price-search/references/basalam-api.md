# Basalam API Reference

## Search Products

```
GET https://services.basalam.com/web/v1/search/product/search
```

### Parameters
- `q` (string, required): Search query (URL-encoded)
- `from` (int): Offset for pagination (default: 0)
- `size` (int): Results per page (default: 12)
- `dynamicFacets` (bool): Include dynamic facets

### Required Headers
```
User-Agent: Mozilla/5.0
Origin: https://basalam.com
Referer: https://basalam.com/
```

### Response Structure
```json
{
  "products": [
    {
      "id": 39245071,
      "name": "product name",
      "price": 250000,
      "primaryPrice": 250000,
      "IsAvailable": true,
      "vendor": { "name": "seller name" },
      "categoryTitle": "دسته‌بندی",
      "rating": 4.5,
      "photo": "url..."
    }
  ],
  "facets": { ... },
  "meta": { ... }
}
```

### Notes
- `price` is in Toman (تومان), not Rial
- No authentication required
- API is public and stable
- Returns up to `size` products per request
- Products include parts, accessories, and full vehicles

## Spell Correct

```
GET https://services.basalam.com/web/v1/nlp/spell-correct/?query=<encoded>
```

## Vendor Search

```
GET https://services.basalam.com/web/v1/vendor-search/vendors/suggestion?q=<encoded>
```
