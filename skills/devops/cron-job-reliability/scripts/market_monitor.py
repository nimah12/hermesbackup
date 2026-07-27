#!/usr/bin/env python3
"""
Market Monitor - Comprehensive Iranian Market Data
Runs every 3 hours, checks multiple sources, alerts on >5% changes
"""
import asyncio
import aiohttp
import json
import re
from datetime import datetime, timezone, timedelta

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))
STATE_FILE = "/data/.hermes/market_prices.json"
ALERT_THRESHOLD_GOLD = 5.0
ALERT_THRESHOLD_OIL = 3.0

# IranJib ID Mapping (verified working 2026-07-27)
ID_MAP = {
    "f_83_63_pr": ("gold_ounce_usd", 1),
    "f_84_63_pr": ("mesghal_toman", 10),
    "f_85_63_pr": ("gold_18k_toman", 10),
    "f_127_63_pr": ("gold_24k_toman", 10),
    "f_86_63_pr": ("silver_ounce_usd", 1),
    "f_87_63_pr": ("coin_full_new_toman", 10),
    "f_88_63_pr": ("coin_full_old_toman", 10),
    "f_89_63_pr": ("coin_half_toman", 10),
    "f_90_63_pr": ("coin_quarter_toman", 10),
    "f_92_63_pr": ("coin_1gram_toman", 10),
    "f_19054_127_pr": ("usdt_toman", 1),
    "f_6370_127_pr": ("usd_index", 1),
    "f_8652_68_pr": ("usd_remittance_toman", 1),
    "f_8653_68_pr": ("eur_remittance_toman", 1),
    "f_17624_68_pr": ("aed_remittance_toman", 1),
    "f_8277_127_pr": ("btc_usd", 1),
    "f_6371_127_pr": ("brent_usd", 1),
    "f_6372_127_pr": ("wti_usd", 1),
}

SOURCES = {
    "iranjib": "https://www.iranjib.ir/showgroup/23/realtime_price/",
    "tala_ir": "https://www.tala.ir/api/v1/live-price",
    "coingecko": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,binancecoin,solana,ripple&vs_currencies=usd&include_24hr_change=true",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Referer": "https://www.iranjib.ir/",
}

async def fetch_iranjib(session):
    try:
        async with session.get(SOURCES["iranjib"], headers=HEADERS, timeout=15) as resp:
            html = await resp.text()
        prices = {}
        for id_str, (key, divisor) in ID_MAP.items():
            pattern = rf'id="{id_str}"[^>]*><span class="lastprice">([^<]+)'
            m = re.search(pattern, html)
            if m:
                raw = m.group(1).replace(",", "").replace("،", "")
                try:
                    prices[key] = int(raw) // divisor
                except:
                    pass
        return prices
    except Exception as e:
        return {"error": f"iranjib: {e}"}

async def fetch_tala_ir(session):
    try:
        async with session.get(SOURCES["tala_ir"], timeout=10) as resp:
            data = await resp.json()
        prices = {}
        if data.get("success") and data.get("data"):
            for item in data["data"]:
                name = item.get("name", "").strip()
                price = item.get("price")
                if price:
                    if "طلای ۱۸" in name:
                        prices["gold_18k_toman"] = price // 10
                    elif "طلای ۲۴" in name:
                        prices["gold_24k_toman"] = price // 10
                    elif "مثقال" in name:
                        prices["mesghal_toman"] = price // 10
                    elif "سکه تمام" in name:
                        prices["coin_full_new_toman"] = price // 10
                    elif "نیم سکه" in name:
                        prices["coin_half_toman"] = price // 10
                    elif "ربع سکه" in name:
                        prices["coin_quarter_toman"] = price // 10
        return prices
    except Exception as e:
        return {"error": f"tala_ir: {e}"}

async def fetch_coingecko(session):
    try:
        async with session.get(SOURCES["coingecko"], timeout=10) as resp:
            data = await resp.json()
        prices = {}
        mapping = {
            "bitcoin": ("btc_usd", 1),
            "ethereum": ("eth_usd", 1),
            "tether": ("usdt_usd", 1),
            "binancecoin": ("bnb_usd", 1),
            "solana": ("sol_usd", 1),
            "ripple": ("xrp_usd", 1),
        }
        for coin, (key, mult) in mapping.items():
            if coin in data and "usd" in data[coin]:
                prices[key] = data[coin]["usd"] * mult
                if "usd_24h_change" in data[coin]:
                    prices[f"{key}_24h_change"] = data[coin]["usd_24h_change"]
        return prices
    except Exception as e:
        return {"error": f"coingecko: {e}"}

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
    for key, new_val in new.items():
        if key.endswith("_24h_change") or key in ["usd_index"]:
            continue
        if key in old and old[key] and new_val:
            try:
                change = ((new_val - old[key]) / old[key]) * 100
                threshold = ALERT_THRESHOLD_OIL if "oil" in key or "brent" in key or "wti" in key else ALERT_THRESHOLD_GOLD
                if abs(change) >= threshold:
                    alerts.append({
                        "asset": key,
                        "old": old[key],
                        "new": new_val,
                        "change_pct": round(change, 2),
                        "threshold": threshold,
                        "time": datetime.now(TEHRAN_TZ).isoformat(),
                    })
            except:
                pass
    return alerts

async def main():
    print(f"[{datetime.now(TEHRAN_TZ).strftime('%H:%M:%S')}] Market Monitor Started")
    
    old_state = load_state()
    old_prices = old_state.get("prices", {})
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_iranjib(session),
            fetch_tala_ir(session),
            fetch_coingecko(session),
        ]
        results = await asyncio.gather(*tasks)
    
    # Merge all prices
    new_prices = {}
    for r in results:
        new_prices.update(r)
    
    # Check alerts
    alerts = check_alerts(old_prices, new_prices)
    
    # Save state
    save_state({
        "prices": new_prices,
        "last_update": datetime.now(TEHRAN_TZ).isoformat(),
    })
    
    # Output
    if alerts:
        print("---ALERTS_JSON_START---")
        print(json.dumps(alerts, ensure_ascii=False))
        print("---ALERTS_JSON_END---")
    else:
        print(f"Prices updated: {len(new_prices)} items")
        for k, v in sorted(new_prices.items()):
            if not k.endswith("_24h_change"):
                print(f"  {k}: {v:,.0f}")

if __name__ == "__main__":
    asyncio.run(main())