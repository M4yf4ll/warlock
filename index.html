import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

RSS_URL = "https://worldofwarcraft.blizzard.com/en-gb/news/rss"
OUTPUT_FILE = "warlock_patches.json"

def fetch_and_filter_warlock_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WoWForeverWarlockBot/2.0'
    }
    
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Fel vid hämtning av RSS: {e}")
        return

    root = ET.fromstring(response.content)
    channel = root.find('channel')
    
    warlock_keywords = ['warlock', 'forever', 'class change', 'hotfix', 'patch', 'voidwalker', 'succubus', 'soul siphon', 'felsteed', 'buff', 'nerf']
    filtered_articles = []
    guide_status = "Optimerad för aktuell Patch"

    if channel is not None:
        for item in channel.findall('item'):
            title = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            description = item.find('description').text if item.find('description') is not None else ""

            content_to_check = (title + " " + description).lower()
            
            if any(keyword in content_to_check for keyword in warlock_keywords):
                # Om en större patch nämns, flagga guiden för översyn
                if "patch" in content_to_check or "hotfix" in content_to_check:
                    guide_status = "⚠️ Ny patch detekterad – Se över ändringar nedan!"

                filtered_articles.append({
                    "title": title,
                    "link": link,
                    "date": pub_date,
                    "summary": description[:250] + "..." if len(description) > 250 else description
                })

    output_data = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "guide_status": guide_status,
        "total_updates": len(filtered_articles),
        "articles": filtered_articles
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Skanning klar! Hittade {len(filtered_articles)} relevanta Forever-ändringar.")

if __name__ == "__main__":
    fetch_and_filter_warlock_news()
