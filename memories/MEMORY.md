PRICE SEARCH: Always include direct links. Search ALL sites (digikala, basalam, sheypoor, divar, bama, emalls, torob, snapp, parsiancomputer, zoomit, sodamarket, technolife, digistyle, khodro45, khodrobank, hamrah-mechanic). Try multiple bypass methods for blocked sites. Don't worry about tokens. CURRENCY: 1 Toman = 10 Rial. Most shops use Toman. NEVER mix units. Detect category FIRST then search relevant sites only.

=== SESSION 2026-07-27 SUMMARY ===
1. DATE SYNC: Cron every 5min from Worldometer -> /data/.hermes/current_date.json
2. MARKET MONITOR: 2 cron jobs (3h/4h) using market_monitor.py script
   Sources: IranJib (18 items), Tala.ir API, CoinGecko
   Alerts: >5% gold/currency, >3% oil
3. TELEGRAM GOLD ALERT: 30min cron, @se_pz & @talasea_ir, gold_alert_telegram.py
4. WAR ALERT: 3h cron, 8 TG channels - WORKING
5. TECH NEWS: Daily 13:00 Tehran
6. BACKUP: 12h to nimah12/hermesbackup
7. IPHONE 17: Not released (Sept 2025), iPhone 16 is latest
FIXES: Converted failing LLM+Playwright crons to direct Python scripts (no_agent=true)
IranJib extraction fixed with exact HTML IDs
§
CONSOLIDATED RULES: User Nima, Persian only. Hardware buyer (used/stock Iran). Price search: min 10 sites, category-first, min/avg/max, quality eval, recommendation, links. Currency: 1 Toman=10 Rial. Sites: Computer: digikala, basalam, sheypoor, sodamarket, technolife, torob, snapp.shop, tapsi.shop. Cars: divar, bama, khodrobank, hamrah-mechanic, khodro45. Mobile: digikala, basalam, mobile.ir, technolife, sodamarket, snapp.shop, tapsi.shop. Fashion: modiseh, digistyle (NOT electronics). BEHAVIOR: NEVER touch Hermes config. Use tgju.org primary for live prices. Verify date always. Digistyle=fashion only. MONITORING: 1) Market 3h multi-source (iranijib, talasea, mesghal, tgju, bonbast, bestchange, cmc, oilprice, reuters + 4 TG channels) alert >5% gold/currency, >3% oil. 2) Gold talasea.ir 30m >5%. 3) ME War 3h 8 TG channels. 4) Tech News 13:00 Tehran. 5) Backup 12h. Default market: iranijib.ir (Playwright).