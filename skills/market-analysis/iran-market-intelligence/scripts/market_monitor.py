#!/usr/bin/env python3
"""
Market Monitor - Comprehensive Iranian Market Data
Runs every 3 hours, checks multiple sources, alerts on >5% changes
Supports --silent flag for cron jobs (only outputs on alerts)
"""
import asyncio
import aiohttp
import json
import re
import sys
import os
from datetime import datetime, timezone, timedelta

THRESHOLD = 5.0  # 5% for gold/currency
OIL_THRESHOLD = 3.0  # 3% for oil
STATE_FILE = "/data/.hermes/market_prices.json"

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

async def fetch(session, url, headers=None):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15), headers=headers or {}) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception as e:
        print(f"[{url}] Error: {e}")
    return None

async def fetch_json(session, url, headers=None):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15), headers=headers or {}) as resp:
            if resp.status == 200:
                return await resp.json()
    except Exception as e:
        print(f"[{url}] JSON Error: {e}")
    return None

# ==================== IRANJIB ====================
async def get_iranjib(session):
    url = "https://www.iranjib.ir/showgroup/23/realtime_price/"
    html = await fetch(session, url, headers={"Referer": "https://www.iranjib.ir/"})
    if not html:
        return {}

    prices = {}
    id_map = {
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

    for id_str, (key, divisor) in id_map.items():
        pattern = rf'id="{id_str}"[^>]*><span class="lastprice">([^<]+)'
        m = re.search(pattern, html)
        if m:
            try:
                val_str = m.group(1).replace(",", "").replace("،", "")
                val = float(val_str) / divisor
                prices[key] = val
            except Exception as e:
                print(f"[iranjib:{id_str}] Parse error: {e}")

    return prices

# ==================== TALA.IR API ====================
async def get_tala_ir_api(session):
    url = "https://www.tala.ir/api/v1/live-price"
    data = await fetch_json(session, url)
    if not data:
        return {}

    prices = {}
    for item in data.get("data", []):
        name = item.get("name", "").lower()
        price = item.get("price", 0)
        if "۱۸" in name and "عیار" in name:
            prices["gold_18k_toman_tala"] = price
        elif "۲۴" in name and "عیار" in name:
            prices["gold_24k_toman_tala"] = price
        elif "مثقال" in name:
            prices["mesghal_toman_tala"] = price
        elif "تمام" in name and "سکه" in name:
            prices["coin_full_toman_tala"] = price
        elif "نیم" in name:
            prices["coin_half_toman_tala"] = price
        elif "ربع" in name:
            prices["coin_quarter_toman_tala"] = price
    return prices

# ==================== COINGECKO (Crypto) ====================
async def get_crypto(session):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,binancecoin,solana,ripple&vs_currencies=usd&include_24hr_change=true"
    data = await fetch_json(session, url)
    if not data:
        return {}

    prices = {}
    for coin, info in data.items():
        prices[f"crypto_{coin}_usd"] = info.get("usd", 0)
    return prices

# ==================== MERGE & ALERT ====================
def merge_prices(all_sources):
    """Merge prices from multiple sources with priority"""
    priority = ["iranjib", "tala_ir_api"]
    merged = {}

    for src in priority:
        if src in all_sources:
            for k, v in all_sources[src].items():
                if k not in merged:
                    merged[k] = v

    if "crypto" in all_sources:
        merged.update(all_sources["crypto"])

    return merged

def get_change_indicator(change_pct: float) -> str:
    """Return emoji indicator based on absolute percentage change."""
    abs_change = abs(change_pct)
    if abs_change > 5.0:
        return "🔴"
    elif abs_change > 3.0:
        return "🟠"
    elif abs_change > 1.0:
        return "🟡"
    else:
        return "🟢"

def format_price_line(key: str, new_val: float, old_val: float = None) -> str:
    """Format a price line with change indicator and percentage."""
    if old_val is None or old_val == 0:
        return f"  {key}: {new_val:,.2f}"

    change_pct = (new_val - old_val) / old_val * 100
    direction = "▲" if change_pct > 0 else "▼"
    indicator = get_change_indicator(change_pct)
    return f"  {indicator} {key}: {new_val:,.2f} ({direction}{abs(change_pct):.2f}%)"

def check_alerts(old_prices, new_prices):
    alerts = []
    skip_keys = [k for k in new_prices if "24h_change" in k or "index" in k.lower()]

    for key, new_val in new_prices.items():
        if key in skip_keys:
            continue
        old_val = old_prices.get(key)
        if old_val and old_val > 0:
            change = abs((new_val - old_val) / old_val * 100)
            threshold = OIL_THRESHOLD if key in ["brent_usd", "wti_usd"] else THRESHOLD
            if change >= threshold:
                alerts.append({
                    "type": "price_change",
                    "item": key,
                    "old_price": old_val,
                    "new_price": new_val,
                    "change_percent": round(change, 2),
                    "direction": "up" if new_val > old_val else "down",
                    "threshold": threshold,
                    "time": tehran_now(),
                })
    return alerts

async def main(silent_if_no_alerts=False):
    if not silent_if_no_alerts:
        print(f"=== Market Monitor: {tehran_now()} ===")

    old_state = load_state()
    old_prices = old_state.get("prices", {})

    all_prices = {}

    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = {
            "iranjib": get_iranjib(session),
            "tala_ir_api": get_tala_ir_api(session),
            "crypto": get_crypto(session),
        }

        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        for (source, _), result in zip(tasks.items(), results):
            if isinstance(result, Exception):
                if not silent_if_no_alerts:
                    print(f"[{source}] Exception: {result}")
                continue
            if result:
                all_prices[source] = result
                if not silent_if_no_alerts:
                    print(f"[{source}] Got {len(result)} prices")

    merged = merge_prices(all_prices)
    all_prices["merged"] = merged

    alerts = check_alerts(old_prices, merged)

    save_state({"prices": merged, "all_sources": all_prices, "last_check": tehran_now()})

    if alerts:
        if not silent_if_no_alerts:
            print(f"\n=== {len(alerts)} ALERTS ===")
        for a in alerts:
            print(json.dumps(a, ensure_ascii=False))
        print("---ALERTS_JSON_START---")
        print(json.dumps(alerts, ensure_ascii=False))
        print("---ALERTS_JSON_END---")
    else:
        if not silent_if_no_alerts:
            print(f"\n=== NO ALERTS (gold/currency: {THRESHOLD}%, oil: {OIL_THRESHOLD}%) ===")
            for k, v in sorted(merged.items()):
                if "24h_change" not in k:
                    old_v = old_prices.get(k)
                    print(format_price_line(k, v, old_v))

if __name__ == "__main__":
    silent = "--silent" in sys.argv or "SILENT_MODE" in os.environ
    asyncio.run(main(silent_if_no_alerts=silent))