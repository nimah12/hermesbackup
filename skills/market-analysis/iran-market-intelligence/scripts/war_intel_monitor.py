#!/usr/bin/env python3
"""
War Intelligence Monitor - Fetches 8 Iranian Telegram channels for war/conflict alerts
Runs every 3 hours via cron (no_agent=true)
"""
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timezone, timedelta

WAR_CHANNELS = [
    "iranintltv", "km_ap", "tasnimnews", "farsna",
    "tabzlive", "alibk3", "khabari_18", "ne_wg"
]

STATE_FILE = "/data/.hermes/war_intel_state.json"

KEYWORDS = {
    "critical": [
        "جنگ", "درگیری", "موشک", "حمله", "انفجار", "شلیک", "هدف",
        "war", "attack", "missile", "strike", "explosion", "conflict"
    ],
    "high": [
        "هشدار", "احتیاط", "خطر", "فرار", "تخلیه", "ممانعت",
        "alert", "warning", "danger", "evacuation", "interception"
    ],
    "medium": [
        "تنش", "تهدید", "قدرت", "نیرو", "شلیک", "دفاع",
        "tension", "threat", "force", "defense"
    ]
}

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

def classify_message(text):
    text_lower = text.lower()
    for level, words in KEYWORDS.items():
        for w in words:
            if w in text_lower:
                return level
    return None

async def fetch_channel(session, channel_id):
    url = f"https://t.me/s/{channel_id}"
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
    print(f"=== War Intel Monitor: {tehran_now()} ===")

    old_state = load_state()
    seen_ids = set(old_state.get("seen_messages", []))

    all_alerts = []

    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        for channel_id in WAR_CHANNELS:
            print(f"[{channel_id}] Fetching...")
            html = await fetch_channel(session, channel_id)
            if not html:
                continue

            messages = parse_messages(html)
            print(f"[{channel_id}] Got {len(messages)} messages")

            for msg in messages:
                # Simple dedup by hash
                msg_hash = hash(msg[:200])
                if msg_hash in seen_ids:
                    continue
                seen_ids.add(msg_hash)

                level = classify_message(msg)
                if level:
                    alert = {
                        "channel": channel_id,
                        "level": level,
                        "text": msg[:500],
                        "time": tehran_now(),
                    }
                    all_alerts.append(alert)
                    print(f"  [{level.upper()}] {msg[:100]}...")

    # Keep last 1000 message hashes
    seen_list = list(seen_ids)[-1000:]
    save_state({"seen_messages": seen_list, "last_check": tehran_now()})

    if all_alerts:
        print(f"\n=== {len(all_alerts)} WAR ALERTS ===")
        for a in all_alerts:
            print(json.dumps(a, ensure_ascii=False))
        print("---ALERTS_JSON_START---")
        print(json.dumps(all_alerts, ensure_ascii=False))
        print("---ALERTS_JSON_END---")
    else:
        print(f"\n=== NO WAR ALERTS ===")

if __name__ == "__main__":
    asyncio.run(main())