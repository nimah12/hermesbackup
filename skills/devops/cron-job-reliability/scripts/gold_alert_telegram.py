#!/usr/bin/env python3
"""
Gold/Currency price alert from Telegram channels @se_pz and @talasea_ir
Runs every 30 minutes, alerts on >5% price change
"""
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timezone, timedelta

THRESHOLD = 5.0
STATE_FILE = "/data/.hermes/telegram_gold_prices.json"

CHANNELS = [
    ("se_pz", "https://t.me/s/se_pz"),
    ("talasea_ir", "https://t.me/s/talasea_ir"),
]

def tehran_now():
    tz = timezone(timedelta(hours=3, minutes=30))
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def fetch(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception as e:
        print(f"[{url}] Error: {e}")
    return None

def extract_prices(text):
    """Extract gold/coin/currency prices from Telegram message text"""
    prices = {}
    patterns = {
        "gold_18k_gram": [
            r'(?:طلای?\s*۱۸\s*عیار|گرم\s*طلای?\s*۱۸)\D*([\d,]{8,12})',
            r'(?:۱۸\s*عیار|18k)\D*([\d,]{8,12})',
        ],
        "gold_24k_gram": [
            r'(?:طلای?\s*۲۴\s*عیار|گرم\s*طلای?\s*۲۴)\D*([\d,]{8,12})',
            r'(?:۲۴\s*عیار|24k)\D*([\d,]{8,12})',
        ],
        "gold_mesghal": [
            r'(?:مثقال\s*طلا|mesghal)\D*([\d,]{9,12})',
        ],
        "coin_full": [
            r'(?:سکه\s*(?:تمام|بهر|آزادی|کامل)|full\s*coin)\D*([\d,]{9,12})',
        ],
        "coin_half": [
            r'(?:نیم\s*سکه|half\s*coin)\D*([\d,]{9,12})',
        ],
        "coin_quarter": [
            r'(?:ربع\s*سکه|quarter\s*coin)\D*([\d,]{8,12})',
        ],
        "usd": [
            r'(?:دلار|dollar|usd)\D*([\d,]{5,7})',
        ],
        "usdt": [
            r'(?:تتر|usdt|tether)\D*([\d,]{5,7})',
        ],
    }
    
    for key, pat_list in patterns.items():
        for pattern in pat_list:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                val = int(matches[-1].replace(",", ""))
                if key in ["gold_18k_gram", "gold_24k_gram"] and 10_000_000 < val < 50_000_000:
                    prices[key] = val
                    break
                elif key == "gold_mesghal" and 50_000_000 < val < 100_000_000:
                    prices[key] = val
                    break
                elif key == "coin_full" and 50_000_000 < val < 300_000_000:
                    prices[key] = val
                    break
                elif key == "coin_half" and 20_000_000 < val < 150_000_000:
                    prices[key] = val
                    break
                elif key == "coin_quarter" and 10_000_000 < val < 80_000_000:
                    prices[key] = val
                    break
                elif key in ["usd", "usdt"] and 50_000 < val < 200_000:
                    prices[key] = val
                    break
    return prices

def parse_messages(html):
    messages = []
    patterns = [
        r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
        r'data-post="[^"]*"[^>]*>.*?<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, html, re.DOTALL)
        for m in matches:
            text = re.sub(r'<[^>]+>', '', m)
            text = text.replace('&nbsp;', ' ').replace('&zwj;', '').strip()
            if text and len(text) > 10:
                messages.append(text)
    return messages[:20]

async def check_channel(session, channel_id, url, prev_prices):
    alerts = []
    html = await fetch(session, url)
    if not html:
        return alerts, prev_prices
    
    messages = parse_messages(html)
    print(f"[{channel_id}] Got {len(messages)} messages")
    
    for msg in messages:
        prices = extract_prices(msg)
        if not prices:
            continue
        
        for k, v in prices.items():
            full_key = f"{channel_id}:{k}"
            if full_key not in prev_prices:
                prev_prices[full_key] = v
            
            old_val = prev_prices.get(full_key)
            if old_val and old_val > 0:
                change = abs((v - old_val) / old_val * 100)
                if change >= THRESHOLD:
                    alerts.append({
                        "type": "price_change",
                        "channel": channel_id,
                        "item": k,
                        "old_price": old_val,
                        "new_price": v,
                        "change_percent": round(change, 2),
                        "direction": "up" if v > old_val else "down",
                        "message_preview": msg[:200],
                        "time": tehran_now(),
                    })
            prev_prices[full_key] = v
    
    return alerts, prev_prices

async def main():
    print(f"=== Telegram Gold Alert: {tehran_now()} ===")
    
    old_state = load_state()
    prev_prices = old_state.get("prices", {})
    
    all_alerts = []
    
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        for channel_id, url in CHANNELS:
            print(f"[{channel_id}] Fetching...")
            alerts, prev_prices = await check_channel(session, channel_id, url, prev_prices)
            all_alerts.extend(alerts)
    
    save_state({"prices": prev_prices, "last_check": tehran_now()})
    
    if all_alerts:
        print(f"\n=== {len(all_alerts)} ALERTS ===")
        for a in all_alerts:
            print(json.dumps(a, ensure_ascii=False))
        print("---ALERTS_JSON_START---")
        print(json.dumps(all_alerts, ensure_ascii=False))
        print("---ALERTS_JSON_END---")
    else:
        print(f"\n=== NO ALERTS (all changes < {THRESHOLD}%) ===")
        print(f"Tracked prices: {len(prev_prices)}")
        for k, v in sorted(prev_prices.items()):
            print(f"  {k}: {v:,}")

if __name__ == "__main__":
    asyncio.run(main())