#!/usr/bin/env python3
"""
Telegram Gold Alert - Monitors @se_pz and @talasea_ir for price changes
Runs every 30 minutes, alerts on >5% change
"""
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timezone, timedelta

THRESHOLD = 5.0  # 5% change triggers alert
CHANNELS = [
    ("se_pz", "https://t.me/s/se_pz"),
    ("talasea_ir", "https://t.me/s/talasea_ir"),
]

STATE_FILE = "/data/.hermes/telegram_gold_prices.json"

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

def extract_prices(text):
    """Extract gold/coin/currency prices from text"""
    prices = {}
    patterns = {
        "gold_18k_gram": [
            r'(?:طلای?\s*۱۸\s*عیار|گرم\s*طلای?\s*۱۸)\D*([\d,]{8,12})',
            r'(?:۱۸\s*عیار|18k)\D*([\d,]{8,12})',
            r'(?:geram.*?18|18.*?geram)\D*([\d,]{8,12})',
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
            r'(?:سکه\s*یک\s*گرم|۱\s*گرم\s*سکه)\D*([\d,]{9,12})',
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
                # Filter realistic ranges
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

async def fetch_channel(session, channel_id, url):
    try:
        async with session.get(url, timeout=15) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception as e:
        print(f"[{channel_id}] Fetch error: {e}")
    return None

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

async def main():
    print(f"=== Telegram Gold Alert: {tehran_now()} ===")

    old_state = load_state()
    old_prices = old_state.get("prices", {})

    new_prices = {}
    alerts = []

    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        for channel_id, url in CHANNELS:
            print(f"[{channel_id}] Fetching...")
            html = await fetch_channel(session, channel_id, url)
            if html:
                messages = parse_messages(html)
                print(f"[{channel_id}] Got {len(messages)} messages")

                for msg in messages:
                    prices = extract_prices(msg)
                    if prices:
                        for k, v in prices.items():
                            full_key = f"{channel_id}:{k}"
                            if full_key not in new_prices:
                                new_prices[full_key] = v

                            old_val = old_prices.get(full_key)
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

    save_state({"prices": new_prices, "last_check": tehran_now()})

    if alerts:
        print(f"\n=== {len(alerts)} ALERTS ===")
        for a in alerts:
            print(json.dumps(a, ensure_ascii=False))
        print("---ALERTS_JSON_START---")
        print(json.dumps(alerts, ensure_ascii=False))
        print("---ALERTS_JSON_END---")
    else:
        print(f"\n=== NO ALERTS (all changes < {THRESHOLD}%) ===")
        print(f"Tracked prices: {len(new_prices)}")
        for k, v in new_prices.items():
            print(f"  {k}: {v:,}")

if __name__ == "__main__":
    asyncio.run(main())