#!/usr/bin/env python3
"""
Tehran Time Sync - Fetches current Tehran time from Worldometer
Runs every 5 minutes via cron (no_agent=true)
"""
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timezone, timedelta

STATE_FILE = "/data/.hermes/current_date.json"
URL = "https://www.worldometers.info/time/tehran-iran/"

def tehran_now():
    tz = timezone(timedelta(hours=3, minutes=30))
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

async def fetch_tehran_time():
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        try:
            async with session.get(URL, timeout=10) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    # Extract time from Worldometer page
                    patterns = [
                        r'<span id="ct"[^>]*>(\d{2}:\d{2}:\d{2})</span>',
                        r'<span id="clock"[^>]*>(\d{2}:\d{2}:\d{2})</span>',
                        r'Tehran.*?(\d{2}:\d{2}:\d{2})',
                    ]
                    for pattern in patterns:
                        m = re.search(pattern, html, re.IGNORECASE)
                        if m:
                            return m.group(1)
        except Exception as e:
            print(f"[Tehran Time] Fetch error: {e}")
    return None

def save_time(time_str):
    data = {
        "tehran_time": time_str,
        "fetched_at": tehran_now(),
        "source": "worldometer"
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def main():
    print(f"=== Tehran Time Sync: {tehran_now()} ===")
    time_str = await fetch_tehran_time()
    if time_str:
        save_time(time_str)
        print(f"Tehran time saved: {time_str}")
    else:
        # Fallback to local calculated time
        save_time(tehran_now())
        print(f"Fallback to local time: {tehran_now()}")

if __name__ == "__main__":
    asyncio.run(main())