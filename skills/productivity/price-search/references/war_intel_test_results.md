# Telegram War Intelligence — Test Results (2026-07-27)

## Test Run Summary
- **Date**: 2026-07-27 11:58 Tehran
- **Channels Monitored**: 8/8 (7 successful, 1 empty)
- **Total Messages**: ~135
- **Critical Alerts**: 29
- **High Alerts**: 2
- **Execution Time**: ~15 seconds

## Channel-by-Channel Results

| Channel | Messages | Critical | High | Key Findings |
|---------|----------|----------|------|--------------|
| @iranintltv | 20 | 4 | 0 | Trump AI images, Erbil missiles, Hormuz threat |
| @km_ap | 20 | 12 | 2 | Pentagon casualties (18 KIA/624 WIA), CENTCOM, Erbil drones |
| @tasnimnews | 0 | 0 | 0 | Empty/error |
| @farsna | 20 | 5 | 0 | Yemen blockade (11 ships), 3 Saudi tankers hit |
| @tabzlive | 20 | 0 | 0 | English content, low Persian keyword match |
| @alibk3 | 20 | 0 | 0 | English content |
| @khabari_18 | 15 | 3 | 0 | Erbil drone strike, Yemen proxy attacks |
| @ne_wg | 20 | 5 | 2 | Ahvaz→Erbil missiles, Zelensky Iran/NK claims |

## Verified Actionable Alerts

### 🔴 CRITICAL (Immediate)
1. **Pentagon confirms 18 US KIA / 624 WIA in Iran war** (140+ new casualties, 4 deleted from database) — @km_ap
2. **IRGC suicide drones hit US base in Erbil** — @khabari_18, @ne_wg
3. **Missiles launched from Ahvaz toward Erbil** — @ne_wg
4. **Yemen/Houthi blockade of Bab el-Mandeb: only 11 ships crossing** (Reuters data) — @farsna
5. **Trump posts AI-generated attack images on Kharg Island** — @iranintltv
6. **Zelensky: Iran & North Korea attacked Ukraine before** — @km_ap, @ne_wg
7. **Iranian sailor killed in Ukrainian attack on Iranian ship in Caspian** — @ne_wg

### 🟠 HIGH
1. **CENTCOM commander recommends halt to US bombing near Hormuz** — @km_ap
2. **Explosions heard in Erbil, Iraq** — @ne_wg

## Keyword Effectiveness
| Keyword | Matches | Level |
|---------|---------|-------|
| "درگیری" (engagement) | 8 | Critical |
| "حمله" (attack) | 12 | Critical |
| "پهپاد" (drone) | 7 | Critical |
| "موشک" (missile) | 6 | Critical |
| "اربیل" (Erbil) | 4 | High/Critical |
| "نطنز" (Natanz) | 0 | Critical |
| "فردو" (Fordow) | 0 | Critical |
| "هرمز" (Hormuz) | 2 | Critical |
| "سنتکام" (CENTCOM) | 2 | High |
| "حزب‌الله" (Hezbollah) | 1 | High |
| "حوثی" (Houthi) | 3 | High |

## Parser Performance
- **Pattern**: `<div class="tgme_widget_message_text[^"]*"[^>]*dir="auto">(.*?)</div>`
- **Channels working**: 7/8
- **Average messages/channel**: 15-20
- **False positives**: Low (Persian keywords specific)
- **English channels (@tabzlive, @alibk3)**: 0 matches (keywords Persian-only)

## Cron Integration Status
- **Script**: `war_intel_monitor.py` (direct Python, `no_agent=true`)
- **Schedule**: Every 3 hours (`every 180m`)
- **Cron Job ID**: `3eaeabca4dae`
- **Toolsets**: `["terminal", "file"]`
- **State Persistence**: `/data/.hermes/war_intel_state.json`
- **Deduplication**: Hash-based (first 200 chars of message)

## Files Generated
- Test script: `/data/test_war_intel.py`
- Production script: `/data/.hermes/scripts/war_intel_monitor.py`
- State file: `/data/.hermes/war_intel_state.json`
- Test output: `/data/.hermes/war_intel_test.json`