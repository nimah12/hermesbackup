---
name: motorcycle-parts-price
description: "Find motorcycle tire, tube, part prices on Iranian sites."
tags: [motorcycle, tire, tube, parts, iran, price, honda, cg125]
---

# Motorcycle Parts Price Search — Iranian Market

Search Iranian motorcycle parts marketplaces for tires, tubes, chains, sprockets, batteries, filters.

## When to Use
- User asks for motorcycle tire/tube/part prices
- Specific model queries (Honda CG125, Yamaha RX135, Suzuki GSXR, etc.)
- Comparing prices across Divar, Sheypoor, Bama, Khodro45, Basalam

## Category-First Approach
**MOTORCYCLE PARTS ONLY** — Do NOT search car sites or general e-commerce.

### Approved Sites
| Site | Category | Method |
|------|----------|--------|
| Divar | Classifieds | Playwright (t.me/s/divar search) |
| Sheypoor | Classifieds | Playwright |
| Bama | Classifieds | Playwright |
| Khodro45 | Motorcycle parts | Playwright |
| Basalam | E-commerce | API direct |
| MotorIran | Parts shop | Playwright |
| Digikala (moto section) | E-commerce | Playwright |

## Search Patterns by Part

### Tires (تیوب / لاستیک)
| Query Variants | Brands |
|----------------|--------|
| `تیوب عقب هوندا 125` / `لاستیک عقب CG125` | یزد (Yazd), ساهی (Sahi), ملات (Mitas),ancio (Ancio), Pirelli, Michelin |
| `تیوب جلو هوندا 125` / `لاستیک جلو CG125` | سایزهای رایج: 2.75-18, 3.00-18, 90/90-18 |
| `تیوب موتور 125` / `لاستیک موتورسیکلت 125` | برندهای چینی ارزان، برندهای اصلی |

### Tubes (تیوب داخلی)
| Query | Sizes |
|-------|-------|
| `تیوب داخلی هوندا 125` | 2.75/3.00-18, 90/90-18 |
| `تیوب لاستیک عقب 125` | برند: یزد، ساهی، چینی |

### Chains & Sprockets (زنجیر و دنده)
| Part | Queries |
|------|---------|
| زنجیر | `زنجیر هوندا 125`, `زنجیر 428`, `زنجیر DID`, `زنجیر RK` |
| دنده عقب | `دنده عقب هوندا 125`, `دنده 42 ت`, `دنده 45 ت` |
| دنده موتور | `دنده موتور هوندا 125`, `دنده 14 ت`, `دنده 15 ت` |

### Other Common Parts
| Part | Persian Queries |
|------|-----------------|
| Battery | `باتری هوندا 125`, `باتری موتور 125`, `باتری یuasa`, `باتری والتا` |
| Oil Filter | `فیلتر روغن هوندا 125`, `فیلتر روغن CG125` |
| Air Filter | `فیلتر هوا هوندا 125`, `فیلتر هوا CG125` |
| Brake Pads | `کفیت ترمز هوندا 125`, `کفیت ترمز عقب CG125` |
| Spark Plug | `شمع هوندا 125`, `شمع NGK`, `شمع Denso` |

## Price Extraction Patterns

```python
# Prices in Toman (most Iranian sites)
patterns = [
    r'([\d,]{7,12})\s*تومان',      # 1,500,000 تومان
    r'([\d,]{7,12})\s*ت',          # 1,500,000 ت
    r'قیمت[^:\d]*([\d,]{7,12})',   # قیمت: 1,500,000
    r'([\d,]{7,12})\s*ریال',       # Convert: /10 for Toman
]
```

## CG125 Specific Specs

| Part | Spec | Common Brands |
|------|------|---------------|
| Rear Tire | 3.00-18 or 90/90-18 | Yazd, Sahi, Mitas, Pirelli MT60 |
| Front Tire | 2.75-18 or 80/90-18 | Same as rear |
| Tube (Rear) | 3.00-18 / 90/90-18 | Yazd, Sahi |
| Tube (Front) | 2.75-18 / 80/90-18 | Yazd, Sahi |
| Chain | 428H / 428X - 112/114 links | DID, RK, EK, Chinese |
| Rear Sprocket | 42T / 43T / 45T (steel or 46T for wheelie) | JT, Renthal, Chinese |
| Front Sprocket | 14T / 15T | Same |
| Battery | 12V 6Ah / 7Ah (YTX7A-BS) | Yuasa, Varta, Chinese |
| Oil Filter | M20x1.5 spin-on | Honda OEM, Hiflofiltro |
| Air Filter | Panel type | Honda OEM, Uni, Twin Air |

## Output Format

```markdown
## 🏍️ قیمت قطعات هوندا CG125 (مرداد ۱۴۰۵)

### 🔧 تیوب/لاستیک عقب (۳.۰۰-۱۸ / ۹۰/۹۰-۱۸)
| برند | نوع | قیمت (تومان) | منبع | لینک |
|------|-----|-------------|------|------|
| یزد (Yazd) | تیوب | ۴۵۰,۰۰۰ | دیوار | [link] |
| ساهی (Sahi) | لاستیک | ۱,۲۰۰,۰۰۰ | شیپور | [link] |
| میتاس (Mitas) | لاستیک E-07 | ۲,۱۰۰,۰۰۰ | باما | [link] |
| چینی (Gen.) | تیوب | ۱۸۰,۰۰۰ | بسالم | [link] |

### 🔗 زنجیر و دنده
| قطعه | برند | سایز/توضیح | قیمت | منبع |
|------|------|-----------|------|------|
| زنجیر | DID | 428H 114L | ۱,۸۵۰,۰۰۰ | دیوار |
| دنده عقب | JT | ۴۲ ت | ۳۲۰,۰۰۰ | شیپور |
| دنده موتور | RK | ۱۴ ت | ۱۸۰,۰۰۰ | باما |

### 🔋 باتری و سایر
| قطعه | برند | مشخصات | قیمت | منبع |
|------|------|----------|------|------|
| باتری | Yuasa | YTX7A-BS 12V 6Ah | ۱,۴۵۰,۰۰۰ | دیوار |
| فیلتر روغن | Honda OEM | M20x1.5 | ۱۲۰,۰۰۰ | بسالم |
| شمع | NGK | CR7HSA | ۸۵,۰۰۰ | دیوار |

> **پیشنهاد**: برای استفاده شهری economia → تیوب یزد/ساهی + زنجیر چینی DID کپی
> برای تورینگ/شنی → لاستیک میتاس E-07 + زنجیر اصلی RK
```

## Price Ranges (Reference - Mordad 1405)

| Part | Budget (Chinese) | Mid (Iranian Brand) | Premium (Imported) |
|------|------------------|---------------------|-------------------|
| Rear Tire | 180k-300k | 600k-900k | 1.5M-2.5M |
| Front Tire | 150k-250k | 500k-800k | 1.2M-2M |
| Tube (Rear) | 80k-150k | 200k-350k | 400k-600k |
| Chain | 300k-500k | 800k-1.2M | 1.8M-2.5M |
| Rear Sprocket | 100k-200k | 250k-400k | 500k-800k |
| Battery | 400k-600k | 1M-1.5M | 1.5M-2.5M |
| Oil Filter | 50k-100k | 120k-180k | 200k-300k |
| Spark Plug | 40k-80k | 80k-120k | 150k-250k |

## Search Script Template

```bash
# Basalam API (fastest for new parts)
curl "https://services.basalam.com/web/v1/search/product/search?from=0&q=%D8%AA%DB%8C%D9%88%D8%A8%20%D8%B9%D9%82%D8%A8%20%D9%87%D9%88%D9%86%D8%AF%D8%A7%20125&size=20"

# Divar (classifieds - used/stock)
# Use Playwright: https://divar.ir/s/tehran/motorcycle-parts?q=تیوب+عقب+هوندا+125
```

## References
- Divar motorcycle parts: https://divar.ir/s/tehran/motorcycle-parts
- Sheypoor: https://www.sheypoor.com/ir/motorcycle-parts
- Bama: https://bama.ir/motorcycle/parts
- Khodro45: https://khodro45.com/motorcycle-parts
- Basalam API: https://services.basalam.com/