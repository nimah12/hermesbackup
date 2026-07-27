#!/usr/bin/env python3
"""
Test script for Telegram War Intelligence monitoring.
Fetches and parses messages from Iranian military/political Telegram channels.
Validates the t.me/s/ HTML parsing pattern for cron job use.
"""
import asyncio
import aiohttp
import re
import json
from datetime import datetime, timezone, timedelta

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))

# Verified working Iranian war/military channels
CHANNELS = [
    "iranintltv", "km_ap", "tasnimnews", "farsna",
    "tabzlive", "alibk3", "khabari_18", "ne_wg",
]

KEYWORDS = {
    "critical": ["موشک", "پهپاد", "حمله", "درگیری", "شهید", "کمان", "نطنز", "فردو", "موشک بالستیک"],
    "high": ["حزب‌الله", "حوثی", "حماس", "پنتاگون", "اربیل", "عین‌الاسد", "حامل‌هواپیما", "سنتکام"],
    "medium": ["تهدید", "مناور", "تسلیح", "غنی‌سازی", "صهیونیست", "استکبار", "آمریکا", "اسرائیل"],
}

async def fetch_channel(session, channel):
    url = f"https://t.me/s/{channel}"
    try:
        async with session.get(url, timeout=15) as resp:
            html = await resp.text()
            return html
    except Exception as e:
        return None

def parse_messages(html, channel):
    """Parse t.me/s/ channel page for message text."""
    messages = []
    # Text is in <div class="tgme_widget_message_text js-message_text" dir="auto">...</div>
    pattern = r'<div class="tgme_widget_message_text[^"]*"[^>]*dir="auto">(.*?)</div>'
    for match in re.finditer(pattern, html, re.DOTALL):
        text = match.group(1)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&nbsp;', ' ').replace('&#8204;', ' ').replace('&zwj;', '')
        text = text.replace('<', '<').replace('>', '>').replace('&', '&')
        text = text.strip()
        if len(text) > 30:
            messages.append(text)
    return messages[:20]

def classify_alert(text):
    text_lower = text.lower()
    for level, kws in KEYWORDS.items():
        for kw in kws:
            if kw in text_lower:
                return level, kw
    return "low", None

def tehran_now():
    return datetime.now(TEHRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")

async def main():
    print(f"=== War Intel Test: {tehran_now()} ===")
    print(f"Monitoring {len(CHANNELS)} channels...\n")
    
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [fetch_channel(session, ch) for ch in CHANNELS]
        results = await asyncio.gather(*tasks)
    
    all_alerts = []
    
    for channel, html in zip(CHANNELS, results):
        if not html:
            print(f"[@{channel}] ❌ Failed to fetch")
            continue
        
        messages = parse_messages(html, channel)
        print(f"[@{channel}] ✅ Got {len(messages)} messages")
        
        for msg in messages:
            level, keyword = classify_alert(msg)
            if level in ["critical", "high"]:
                all_alerts.append({
                    "level": level,
                    "channel": f"@{channel}",
                    "keyword": keyword,
                    "text": msg[:400],
                    "time": tehran_now(),
                })
                print(f"  🚨 [{level.upper()}] Keyword: '{keyword}'")
                print(f"     {msg[:200]}...")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total alerts: {len(all_alerts)}")
    for alert in all_alerts:
        print(f"  [{alert['level'].upper()}] {alert['channel']} - '{alert['keyword']}'")
        print(f"    {alert['text'][:150]}...")
    
    with open('/data/.hermes/war_intel_test.json', 'w') as f:
        json.dump(all_alerts, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to /data/.hermes/war_intel_test.json")

if __name__ == "__main__":
    asyncio.run(main())