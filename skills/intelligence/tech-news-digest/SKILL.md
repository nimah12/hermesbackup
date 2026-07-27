---
name: tech-news-digest
description: "Daily AI/gaming/space tech news digest at 13:00 Tehran."
tags: [tech, news, ai, gaming, spacex, digest, daily]
---

# Tech News Digest — Daily AI, Gaming, SpaceX Summary

Curated daily digest of technology news: AI breakthroughs, gaming releases, SpaceX/space industry, cybersecurity.

## When to Use
- Daily briefing at 13:00 Tehran (09:30 UTC)
- Weekly trend analysis for tech sectors
- Tracking specific topics: LLMs, GPUs, Starship, console wars

## Source Categories

### AI & Machine Learning
| Source | Type | Frequency |
|--------|------|-----------|
| arXiv (cs.AI, cs.LG, cs.CL) | Papers | Daily |
| Papers With Code | Trending | Daily |
| Hugging Face Blog | Models | Weekly |
| OpenAI/Anthropic/Google Blogs | Announcements | As released |
| The Gradient / LWN / Import AI | Newsletters | Weekly |
| Twitter/X: @karpathy, @ylecun, @AndrewYNg | Expert takes | Real-time |

### Gaming
| Source | Type | Frequency |
|--------|------|-----------|
| SteamDB / SteamCharts | Player counts | Daily |
| PlayStation Blog / Xbox Wire | Official | Weekly |
| Nintendo Direct / eShop | Releases | Monthly |
| IGN / GameSpot / Eurogamer | Reviews/News | Daily |
| Reddit: r/Games, r/pcgaming | Community | Daily |
| Metacritic / OpenCritic | Scores | On release |

### SpaceX / Space Industry
| Source | Type | Frequency |
|--------|------|-----------|
| SpaceX.com / @SpaceX | Official | Per launch |
| NASASpaceFlight.com / Forum | Technical | Daily |
| Everyday Astronaut | Analysis | Per event |
| Rocket Lab / ULA / Blue Origin | Competitors | Weekly |
| SpaceNews / Ars Technica Space | Industry | Daily |

### Cybersecurity
| Source | Type | Frequency |
|--------|------|-----------|
| The Hacker News / BleepingComputer | Breaking | Daily |
| Krebs on Security | Deep dives | Weekly |
| CISA / NVD | CVEs | Real-time |
| Google Project Zero / MSRC | 0-days | Monthly |

## Digest Structure (Telegram Format)

```
🗞 **گزارش تکنولوژی روزانه — ۱۳:۰۰ تهران**
📅 ۶ مرداد ۱۴۰۵

🤖 **هوش مصنوعی**
• GPT-5 luônدرآمد: OpenAI انتشار داد...
• Llama 3.1 405B: مدل باز سورس جدید متا...
• पेپر هفته: "Scaling Laws for Neural Operators" (arXiv)

🎮 **گیمینگ**
• Black Myth: Wukong منتشر شد — ۲.۲م بازیکنی همزمان در استیم
• PS5 Pro شایعات: معرفی احتمالی سپتامبر
• Steam Deck OLED موجودی 돌아왔다

🚀 **فضا / SpaceX**
• Starship IFT-5: استاتیک فایر موفقیت‌آمیز، پرتاب هفته depan
• Starlink: ۶۰۰۰+ ساتلیک در مدار، سرویس در ایران فعال نیست
• NASA Artemis III تأخیر به ۲۰۲۷

🔐 **سایبرامنیت**
• CVE-2026-XXXX: Zero-day در Windows Kernel (پچ شده)
• LockBit 3.0 رانسومور: حملات جدید در خاورمیانه

📊 **ترندها**
• AI Agents: AutoGPT v2، Devin، SWE-agent
• Local LLMs: llama.cpp، Ollama، LM Studio
• GPU Prices: RTX 4090 در ایران ~۱۸۰م تومان
```

## Automation Script

```python
import asyncio
import aiohttp
import feedparser
from datetime import datetime, timezone, timedelta

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))

RSS_FEEDS = {
    "ai": [
        "https://arxiv.org/rss/cs.AI",
        "https://arxiv.org/rss/cs.LG", 
        "https://arxiv.org/rss/cs.CL",
        "https://huggingface.co/blog/feed.xml",
        "https://openai.com/blog/rss/",
        "https://www.anthropic.com/news/feed.xml",
    ],
    "gaming": [
        "https://www.ign.com/rss.xml",
        "https://www.gamespot.com/feeds/mashup/",
        "https://steamcommunity.com/games/593110/rss/",
    ],
    "space": [
        "https://www.nasaspaceflight.com/feed/",
        "https://spacenews.com/feed/",
        "https://www.spacex.com/feed/",
    ],
    "security": [
        "https://thehackernews.com/feeds/posts/default",
        "https://krebsonsecurity.com/feed/",
        "https://feeds.feedburner.com/eset/blog",
    ],
}

async def fetch_feed(session, url, category):
    try:
        async with session.get(url, timeout=10) as resp:
            content = await resp.text()
            feed = feedparser.parse(content)
            items = []
            for entry in feed.entries[:5]:
                items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", "")[:200],
                    "published": entry.get("published", ""),
                    "category": category,
                })
            return items
    except Exception as e:
        return []

async def build_daily_digest():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_feed(session, url, cat) 
                 for cat, urls in RSS_FEEDS.items() 
                 for url in urls]
        results = await asyncio.gather(*tasks)
    
    # Flatten and organize by category
    digest = {"ai": [], "gaming": [], "space": [], "security": []}
    for items in results:
        for item in items:
            digest[item["category"]].append(item)
    
    return digest

def format_telegram_message(digest):
    date_str = datetime.now(TEHRAN_TZ).strftime("%d %B %Y / %d %B %Y")
    msg = f"🗞 **گزارش تکنولوژی روزانه — ۱۳:۰۰ تهران**\n📅 {date_str}\n\n"
    
    icons = {"ai": "🤖", "gaming": "🎮", "space": "🚀", "security": "🔐"}
    labels = {"ai": "هوش مصنوعی", "gaming": "گیمینگ", "space": "فضا / SpaceX", "security": "سایبرامنیت"}
    
    for cat, items in digest.items():
        if items:
            msg += f"{icons[cat]} **{labels[cat]}**\n"
            for item in items[:3]:
                msg += f"• [{item['title']}]({item['link']})\n"
            msg += "\n"
    
    return msg
```

## Cron Schedule
```bash
# Daily at 13:00 Tehran (09:30 UTC)
30 9 * * * python3 /path/to/tech_digest.py --send-telegram

# Weekly deep-dive Sunday 10:00 Tehran
0 6 * * 0 python3 /path/to/tech_digest.py --weekly
```

## Telegram Delivery
- Target: User's chat (origin)
- Format: Markdown with clickable links
- Length: ~500-800 chars (fits in one message)
- Silent: No notification for weekly, notify for daily

## Keywords to Track (Auto-tag)
| Topic | Keywords |
|-------|----------|
| LLMs | GPT, Llama, Claude, Gemini, Mistral, fine-tune, RAG, agent |
| GPUs | RTX 4090, 5090, H100, A100, Blackwell, ROCm, CUDA |
| SpaceX | Starship, Starlink, Falcon, Raptor, IFT, Boca Chica |
| Consoles | PS5, Xbox Series, Switch 2, Steam Deck, handheld |
| Cyber | ransomware, zero-day, CVE, APT, supply chain, vulnerability |

## References
- RSS feeds: No API key needed
- arXiv API: https://arxiv.org/help/api
- Telegram Bot API for delivery
- Rate limits: Respectful polling (30s between feeds)