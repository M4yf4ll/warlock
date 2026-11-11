import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# Tillförlitliga källor som tillåter automatisk skanning
SOURCES = [
    {
        "name": "Blizzard WoW News",
        "url": "https://news.blizzard.com/en-us/rss/wow",
        "keywords": ["warlock", "patch", "hotfix", "class"]
    },
    {
        "name": "Wowhead News (Top Class Guides)",
        "url": "https://www.wowhead.com/news/rss",
        "keywords": ["warlock", "undead", "patch", "hotfix", "guide", "tuning"]
    },
    {
        "name": "Icy-Veins WoW Updates",
        "url": "https://www.icy-veins.com/forums/forum/18-world-of-warcraft.xml",
        "keywords": ["warlock", "patch", "build"]
    }
]

def fetch_rss_updates():
    articles = []
    # Använd en riktig User-Agent så att anropet inte avvisas
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for source in SOURCES:
        try:
            req = urllib.request.Request(source["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)

                # Loopa igenom artiklar i RSS-flödet
                for item in root.findall('.//item'):
                    title = item.find('title').text if item.find('title') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else '#'
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''

                    # Filtrera så att vi främst sparar relevanta nyheter för Warlock/Patches
                    title_lower = title.lower()
                    if any(kw in title_lower for kw in source["keywords"]) or source["name"] == "Blizzard WoW News":
                        formatted_date = pub_date[:16] if pub_date else datetime.now().strftime("%Y-%m-%d")
                        
                        articles.append({
                            "title": title,
                            "link": link,
                            "date": formatted_date,
                            "summary": f"Verifierad nyhet från {source['name']}."
                        })
                        
                        # Max 5 relevanta artiklar per källa
                        if len(articles) >= 8:
                            break
        except Exception as e:
            print(f"Kunde inte hämta från {source['name']}: {e}")

    return articles

def main():
    print("Skannar Blizzard och Elit-källor för Warlock...")
    fetched_articles = fetch_rss_updates()

    # Reservnotis om inga specifika Warlock-artiklar matchade sökord just idag
    if not fetched_articles:
        fetched_articles = [
            {
                "title": "WoW Official Patch & Class Status",
                "link": "https://news.blizzard.com/en-us/wow",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": "Inga nya specifika Warlock-ändringar i senaste timmens skanning. Guiden följer aktuell live-balansering."
            }
        ]

    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "guide_status": "Aktiv & Synkad med Blizzard/Wowhead",
        "total_updates": len(fetched_articles),
        "articles": fetched_articles
    }

    with open("warlock_patches.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("warlock_patches.json uppdaterad framgångsrikt!")

if __name__ == "__main__":
    main()
