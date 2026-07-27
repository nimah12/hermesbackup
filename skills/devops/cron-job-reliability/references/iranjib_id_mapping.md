# IranJib HTML ID Mapping Reference

## Gold & Coin Table (تابلو آنلاین قیمت طلا - ریال)

| HTML ID | Name | Our Key | Divisor | Unit |
|---------|------|---------|---------|------|
| `f_83_63_pr` | هر انس طلا | `gold_ounce_usd` | 1 | USD |
| `f_84_63_pr` | هر مثقال طلا در بازار تهران | `mesghal_toman` | 10 | Toman |
| `f_85_63_pr` | هر گرم طلای ۱۸ عیار | `gold_18k_toman` | 10 | Toman |
| `f_127_63_pr` | هر گرم طلای ۲۴ عیار | `gold_24k_toman` | 10 | Toman |
| `f_86_63_pr` | هر انس نقره | `silver_ounce_usd` | 1 | USD |

## Coin Table (تابلو آنلاین قیمت سکه - ریال)

| HTML ID | Name | Our Key | Divisor | Unit |
|---------|------|---------|---------|------|
| `f_87_63_pr` | طرح جدید | `coin_full_new_toman` | 10 | Toman |
| `f_88_63_pr` | طرح قدیم | `coin_full_old_toman` | 10 | Toman |
| `f_89_63_pr` | نیم سکه | `coin_half_toman` | 10 | Toman |
| `f_90_63_pr` | ربع سکه | `coin_quarter_toman` | 10 | Toman |
| `f_92_63_pr` | یک گرمی | `coin_1gram_toman` | 10 | Toman |

## Financial Markets (بازارها و شاخص‌های مالی مرتبط)

| HTML ID | Name | Our Key | Divisor | Unit |
|---------|------|---------|---------|------|
| `f_19054_127_pr` | تتر | `usdt_toman` | 1 | Toman |
| `f_6370_127_pr` | شاخص دلار | `usd_index` | 1 | Index |
| `f_8652_68_pr` | دلار / حواله | `usd_remittance_toman` | 1 | Toman |
| `f_8653_68_pr` | یورو / حواله | `eur_remittance_toman` | 1 | Toman |
| `f_17624_68_pr` | درهم / حواله | `aed_remittance_toman` | 1 | Toman |
| `f_8277_127_pr` | بیت کوین / Bitcoin | `btc_usd` | 1 | USD |

## Global Energy (نرخ جهانی انرژی)

| HTML ID | Name | Our Key | Divisor | Unit |
|---------|------|---------|---------|------|
| `f_6371_127_pr` | نفت برنت | `brent_usd` | 1 | USD |
| `f_6372_127_pr` | نفت سبک (WTI) | `wti_usd` | 1 | USD |

## Global Metals (نرخ جهانی فلزات)

| HTML ID | Name | Our Key | Divisor | Unit |
|---------|------|---------|---------|------|
| `f_8281_127_pr` | آلومینیوم | `aluminum` | 1 | USD/ton |
| `f_8282_127_pr` | مس | `copper` | 1 | USD/ton |
| `f_8283_127_pr` | سرب | `lead` | 1 | USD/ton |
| `f_8284_127_pr` | نیکل | `nickel` | 1 | USD/ton |
| `f_8285_127_pr` | قلع | `zinc` | 1 | USD/ton |
| `f_8286_127_pr` | روی | `tin` | 1 | USD/ton |
| `f_19058_127_pr` | فولاد | `steel` | 1 | USD/ton |
| `f_19057_127_pr` | سنگ آهن | `iron_ore` | 1 | USD/ton |
| `f_6373_127_pr` | پلاتین | `platinum` | 1 | USD/oz |

## Additional Energy Products

| HTML ID | Name | Our Key | Divisor | Unit |
|---------|------|---------|---------|------|
| `f_8287_127_pr` | بنزین | `gasoline` | 1 | USD/gal |
| `f_8288_127_pr` | گازوئیل | `gasoil` | 1 | USD/ton |
| `f_8289_127_pr` | گاز طبیعی | `natural_gas` | 1 | USD/MMBtu |

## Agriculture (نرخ جهانی نهاده‌های کشاورزی)

| HTML ID | Name | Our Key | Divisor | Unit |
|---------|------|---------|---------|------|
| `f_19060_127_pr` | کاکائو | `cocoa` | 1 | USD/ton |
| `f_19061_127_pr` | قهوه | `coffee` | 1 | USD/ton |
| `f_19062_127_pr` | ذرت | `corn` | 1 | USD/ton |
| `f_19063_127_pr` | پنبه | `cotton` | 1 | USD/ton |
| `f_19064_127_pr` | برنج | `rice` | 1 | USD/ton |
| `f_19065_127_pr` | سویا | `soybean` | 1 | USD/ton |
| `f_19066_127_pr` | شکر | `sugar` | 1 | USD/ton |
| `f_19067_127_pr` | روغن آفتابگردان | `sunflower_oil` | 1 | USD/ton |
| `f_19068_127_pr` | چای | `tea` | 1 | USD/ton |
| `f_19069_127_pr` | گندم | `wheat` | 1 | USD/ton |

---

## Python ID_MAP Constant

```python
ID_MAP = {
    # Gold & Coin
    "f_83_63_pr": ("gold_ounce_usd", 1),
    "f_84_63_pr": ("mesghal_toman", 10),
    "f_85_63_pr": ("gold_18k_toman", 10),
    "f_127_63_pr": ("gold_24k_toman", 10),
    "f_86_63_pr": ("silver_ounce_usd", 1),
    "f_87_63_pr": ("coin_full_new_toman", 10),
    "f_88_63_pr": ("coin_full_old_toman", 10),
    "f_89_63_pr": ("coin_half_toman", 10),
    "f_90_63_pr": ("coin_quarter_toman", 10),
    "f_92_63_pr": ("coin_1gram_toman", 10),

    # Currency & Crypto
    "f_19054_127_pr": ("usdt_toman", 1),
    "f_6370_127_pr": ("usd_index", 1),
    "f_8652_68_pr": ("usd_remittance_toman", 1),
    "f_8653_68_pr": ("eur_remittance_toman", 1),
    "f_17624_68_pr": ("aed_remittance_toman", 1),
    "f_8277_127_pr": ("btc_usd", 1),

    # Oil
    "f_6371_127_pr": ("brent_usd", 1),
    "f_6372_127_pr": ("wti_usd", 1),

    # Metals (optional)
    "f_8281_127_pr": ("aluminum", 1),
    "f_8282_127_pr": ("copper", 1),
    "f_8283_127_pr": ("lead", 1),
    "f_8284_127_pr": ("nickel", 1),
    "f_8285_127_pr": ("zinc", 1),
    "f_8286_127_pr": ("tin", 1),
    "f_19058_127_pr": ("steel", 1),
    "f_19057_127_pr": ("iron_ore", 1),
    "f_6373_127_pr": ("platinum", 1),

    # Energy (optional)
    "f_8287_127_pr": ("gasoline", 1),
    "f_8288_127_pr": ("gasoil", 1),
    "f_8289_127_pr": ("natural_gas", 1),

    # Agriculture (optional)
    "f_19060_127_pr": ("cocoa", 1),
    "f_19061_127_pr": ("coffee", 1),
    "f_19062_127_pr": ("corn", 1),
    "f_19063_127_pr": ("cotton", 1),
    "f_19064_127_pr": ("rice", 1),
    "f_19065_127_pr": ("soybean", 1),
    "f_19066_127_pr": ("sugar", 1),
    "f_19067_127_pr": ("sunflower_oil", 1),
    "f_19068_127_pr": ("tea", 1),
    "f_19069_127_pr": ("wheat", 1),
}
```

---

## Regex Pattern for Extraction

```python
# Pattern: id="f_85_63_pr"><span class="lastprice">۱۸۱,۵۶۵,۰۰۰
pattern = rf'id="{id_str}"[^>]*><span class="lastprice">([^<]+)'
```

---

## Notes

- **All prices in "ریال" tables are in Rial** → Divide by 10 for Toman
- **USD/EUR/AED remittance prices already in Toman** → Divisor 1
- **Brent/WTI/BTC/Gold ounce already in USD** → Divisor 1
- **Update frequency**: IranJib updates every 60 seconds (see `refreshtime` counter)
- **Page encoding**: Persian numbers (۰-۹) may appear - use `.replace("،", "").replace(",", "")` for parsing

---

## Example HTML Snippet

```html
<tr>
  <td class="entryrtl"><a class="tts" href="#" onclick="return!1">هر گرم طلای ۱۸ عیار</a></td>
  <td id="f_85_63_pr"><span class="lastprice">۱۸۱,۵۶۵,۰۰۰</span></td>
  <td id="f_85_64"><span class="change">...</span></td>
  ...
</tr>
```