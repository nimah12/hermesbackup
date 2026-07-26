PRICE SEARCH: Always include direct links. Search ALL sites (digikala, basalam, sheypoor, divar, bama, emalls, torob, snapp, parsiancomputer, zoomit, sodamarket, technolife, digistyle, khodro45, khodrobank, hamrah-mechanic). Try multiple bypass methods for blocked sites. Don't worry about tokens. CURRENCY: 1 Toman = 10 Rial. Most shops use Toman. NEVER mix units. Detect category FIRST then search relevant sites only.
§
Site categorization - DO NOT mix categories:
- COMPUTER PARTS: digikala, basalam, sheypoor, sodamarket, technolife, digistyle, torob (NOT car sites)
- CARS: divar, bama, khodrobank, hamrah-mechanic, khodro45, shenoto (NOT shop sites)
- MOTORCYCLES: divar, bama, khodro45 (NOT shop sites)
- FASHION/CLOTHING: modiseh, digistyle
When user asks for a product, detect category FIRST, then only search relevant sites. Don't waste time on unrelated sites.
§
NEVER modify Hermes default config settings (model.context_length, agent.max_turns, compression.threshold, etc.) unless explicitly asked. Changing model.context_length broke things previously. User explicitly forbids touching default settings.
§
USER PREFERENCES (CRITICAL):
- User gets EXTREMELY frustrated when: prices wrong/old, dates wrong (1403 vs 1405), not searching enough sites, only showing Basalam, mixing Rial/Toman, touching Hermes config
- ALWAYS verify current date before reporting prices
- ALWAYS search minimum 10 sites per product
- ALWAYS show results from EVERY site that returns data
- ALWAYS convert to Toman (divide Rial by 10)
- NEVER modify Hermes default config unless explicitly asked
- Market monitoring: gold/coin (tala.ir, mesghal.com, bonbast.com), currency/USDT (bonbast.com, bestchange.ir), crypto (coindesk, coinmarketcap), oil (oilprice.com, reuters.com) with alerts >5% changes
§
DEFAULT MARKET MONITORING SOURCE: iranijib.ir (https://www.iranjib.ir/showgroup/23/realtime_price/) - Use Playwright to scrape live price tables. This is the user's preferred source for gold, coin, currency, crypto, oil prices. Use for both manual queries and cron job alerts.