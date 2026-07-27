#!/usr/bin/env python3
"""
Tehran Time Sync - from Worldometer
Runs every 5 minutes, updates /data/.hermes/current_date.json
"""
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timezone, timedelta

OUTPUT_FILE = "/data/.hermes/current_date.json"
SOURCE_URL = "https://www.worldometers.info/time/tehran-iran/"

def load_state():
    try:
        with open(OUTPUT_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_state(data):
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def fetch(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception as e:
        print(f"[{url}] Error: {e}")
    return None

def extract_time(html):
    """Extract Tehran time from Worldometer page"""
    # Look for serverTime in the page props
    match = re.search(r'"serverTime"\s*:\s*(\d+)', html)
    if match:
        timestamp_ms = int(match.group(1))
        # Convert to Tehran timezone
        tehran_tz = timezone(timedelta(hours=3, minutes=30))
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=tehran_tz)
        return dt
    
    # Fallback: look for live clock display
    match = re.search(r'(\d{1,2}):(\d{2}):(\d{2})\s*(AM|PM)', html)
    if match:
        h, m, s, ampm = match.groups()
        h = int(h)
        if ampm == "PM" and h != 12:
            h += 12
        elif ampm == "AM" and h == 12:
            h = 0
        
        # Get date from page
        date_match = re.search(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+(July|August|September|October|November|December|January|February|March|April|May|June)\s+(\d{1,2}),?\s+(\d{4})', html)
        if date_match:
            _, month_str, day, year = date_match.groups()
            month_map = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            month = month_map.get(month_str, 1)
            day = int(day)
            year = int(year)
            
            tehran_tz = timezone(timedelta(hours=3, minutes=30))
            return datetime(year, month, day, h, int(m), int(s), tzinfo=tehran_tz)
    
    # Final fallback: system time with Tehran offset
    tehran_tz = timezone(timedelta(hours=3, minutes=30))
    return datetime.now(tehran_tz)

def gregorian_to_jalali(gy, gm, gd):
    """Convert Gregorian to Jalali (approximate)"""
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    gy2 = gy + 1 if (gm > 2) else gy
    days = (365 * gy) + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400 - 80 + gd + g_d_m[gm - 1]
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    jy += (days - 1) // 365 if days > 365 else 0
    if days > 365:
        days = (days - 1) % 365
    jm = 1 + (days // 31) if days < 186 else 7 + ((days - 186) // 30)
    jd = 1 + (days % 31) if days < 186 else 1 + ((days - 186) % 30)
    return jy, jm, jd

async def main():
    print(f"=== Tehran Time Sync ===")
    
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        html = await fetch(session, SOURCE_URL)
    
    if not html:
        print("Failed to fetch Worldometer")
        return
    
    tehran_dt = extract_time(html)
    
    # Convert to Jalali
    jy, jm, jd = gregorian_to_jalali(tehran_dt.year, tehran_dt.month, tehran_dt.day)
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_names_fa = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]
    
    data = {
        "gregorian": tehran_dt.strftime("%Y-%m-%d"),
        "jalali": f"{jy:04d}-{jm:02d}-{jd:02d}",
        "jalali_full": f"{jd} {['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند'][jm-1]} {jy}",
        "day_name": day_names[tehran_dt.weekday()],
        "day_name_fa": day_names_fa[tehran_dt.weekday()],
        "time_tehran": tehran_dt.strftime("%H:%M:%S"),
        "timezone": "Asia/Tehran",
        "updated_at": tehran_dt.isoformat(),
        "source": "worldometer"
    }
    
    save_state(data)
    print(f"Updated: {data['jalali_full']} {data['time_tehran']} ({data['day_name_fa']})")

if __name__ == "__main__":
    asyncio.run(main())