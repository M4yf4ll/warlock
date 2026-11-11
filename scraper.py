import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

RSS_URL = "https://www.wowhead.com/classic/news/rss"
OUTPUT_FILE = "warlock_patches.json"

def fetch_and_filter_warlock_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WarlockScanner/1.0'
    }
    
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Fel vid hämtning av RSS: {e}")
        return

    # Parsea RSS (XML)
    root = ET.fromstring(response.content)
    channel = root.find('channel')
    
    warlock_keywords = ['warlock', 'succubus', 'voidwalker', 'imp', 'felhunter', 'corruption', 'drain life', 'soul siphon', 'felsteed']
    filtered_articles = []

    for item in channel.findall('item'):
        title = item.find('title').text if item.find('title') is not None else ""
        link = item.find('link').text if item.find('link') is not None else ""
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
        description = item.find('description').text if item.find('description') is not None else ""

        # Kontrollera om artikeln nämner Warlock eller relevanta spells/pets
        content_to_check = (title + " " + description).lower()
        if any(keyword in content_to_check for keyword in warlock_keywords):
            filtered_articles.append({
                "title": title,
                "link": link,
                "date": pub_date,
                "summary": description[:200] + "..." if len(description) > 200 else description
            })

    # Skapa slutgiltig JSON-struktur
    output_data = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "total_updates": len(filtered_articles),
        "articles": filtered_articles
    }

    # Spara till fil
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Skanning klar! Hittade {len(filtered_articles)} Warlock-relaterade uppdateringar.")

if __name__ == "__main__":
    fetch_and_filter_warlock_news()
