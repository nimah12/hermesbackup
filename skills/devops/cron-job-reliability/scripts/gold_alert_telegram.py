#!/usr/bin/env python3
"""
Gold/Currency Price Alert from Telegram channels @se_pz and @talasea_ir
Runs every 30 minutes, alerts on >5% price change
"""
import asyncio
import aiohttp
import re
import json
from datetime import datetime, timezone, timedelta

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))
STATE_FILE = "/data/.hermes/telegram_gold_prices.json"
THRESHOLD = 5.0

CHANNELS = [
    ("se_pz", "https://t.me/s/se_pz"),
    ("talasea_ir", "https://t.me/s/talasea_ir"),
]

# Patterns to extract prices from Persian text
PRICE_PATTERNS = [
    # طلا ۱۸ عیار: ۱۸,۱۵۶,۵۰۰ تومان
    r'(طلای?\s*۱۸\s*عیار|طلا\s*۱۸|۱۸\s*عیار)[^0-9]{0,20}([\d,]{7,12})',
    # طلا ۲۴ عیار
    r'(طلای?\s*۲۴\s*عیار|طلا\s*۲۴|۲۴\s*عیار)[^0-9]{0,20}([\d,]{7,12})',
    # سکه تمام/بهار آزادی
    r'(سکه\s*(?:تمام|بهار\s*آزادی|جدید))[^0-9]{0,20}([\d,]{7,12})',
    # نیم سکه
    r'(نیم\s*سکه)[^0-9]{0,20}([\d,]{7,12})',
    # ربع سکه
    r'(ربع\s*سکه)[^0-9]{0,20}([\d,]{7,12})',
    # دلار/دلار حواله
    r'(دلار\s*(?:حواله|ریال)?|دلار)[^0-9]{0,20}([\d,]{7,12})',
    # تتر/USDT
    r'(تتر|USDT|usdt)[^0-9]{0,20}([\d,]{7,12})',
    # یورو
    r'(یورو|ارو)[^0-9]{0,20}([\d,]{7,12})',
]

KEYWORDS = {
    "gold_18k": ["طلا ۱۸", "طلای ۱۸", "۱۸ عیار"],
    "gold_24k": ["طلا ۲۴", "طلای ۲۴", "۲۴ عیار"],
    "coin_full": ["سکه تمام", "سکه بهار آزادی", "سکه جدید"],
    "coin_half": ["نیم سکه"],
    "coin_quarter": ["ربع سکه"],
    "usd": ["دلار حواله", "دلار"],
    "usdt": ["تتر", "USDT", "usdt"],
    "eur": ["یورو", "ارو"],
}

async def fetch_channel(session, channel_id, url):
    try:
        async with session.get(url, timeout=15) as resp:
            html = await resp.text()
        return html
    except Exception as e:
        return None

def parse_messages(html):
    """Extract messages from t.me/s/ channel page"""
    messages = []
    pattern = r'<div class="tgme_widget_message_text[^"]*"[^>]*dir="auto">(.*?)</div>'
    for match in re.finditer(pattern, html, re.DOTALL):
        text = match.group(1)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&nbsp;', ' ').replace('&#8204;', ' ').replace('&zwj;', '')
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 20:
            messages.append(text)
    return messages[:30]

def extract_prices(text):
    """Extract (item_key, price) pairs from message text"""
    results = []
    text_lower = text.lower()
    
    for item_key, keywords in KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                for pattern in PRICE_PATTERNS:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        price_str = match.group(2).replace(",", "").replace("،", "")
                        try:
                            price = int(price_str)
                            if price > 100000:
                                results.append((item_key, price))
                                break
                        except:
                            pass
                break
    return results

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"prices": {}, "last_update": None}

def save_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_alerts(old, new):
    alerts = []
    for key, new_price in new.items():
        if key in old and old[key] and new_price:
            change = ((new_price - old[key]) / old[key]) * 100
            if abs(change) >= THRESHOLD:
                alerts.append({
                    "item": key,
                    "old_price": old[key],
                    "new_price": new_price,
                    "change_pct": round(change, 2),
                    "threshold": THRESHOLD,
                    "time": datetime.now(TEHRAN_TZ).isoformat(),
                })
    return alerts

async def main():
    print(f"[{datetime.now(TEHRAN_TZ).strftime('%H:%M:%S')}] Gold Telegram Alert Check")
    
    old_state = load_state()
    old_prices = old_state.get("prices", {})
    
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [fetch_channel(session, cid, url) for cid, url in CHANNELS]
        results = await asyncio.gather(*tasks)
    
    new_prices = {}
    for (cid, _), html in zip(CHANNELS, results):
        if not html:
            print(f"[@{cid}] Failed to fetch")
            continue
        messages = parse_messages(html)
        print(f"[@{cid}] Got {len(messages)} messages")
        
        for msg in messages:
            prices = extract_prices(msg)
            for item_key, price in prices:
                if item_key not in new_prices or price < new_prices[item_key]:
                    new_prices[item_key] = price
                    print(f"  {item_key}: {price:,} Toman")
    
    alerts = check_alerts(old_prices, new_prices)
    
    save_state({"prices": new_prices, "last_update": datetime.now(TEHRAN_TZ).isoformat()})
    
    if alerts:
        print("\n---ALERTS_JSON_START---")
        print(json.dumps(alerts, ensure_ascii=False))
        print("---ALERTS_JSON_END---")
    else:
        print(f"\nNo alerts (threshold: {THRESHOLD}%)")

if __name__ == "__main__":
    asyncio.run(main())