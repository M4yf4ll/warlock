import json
import re
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urljoin

SOURCES = [
    {
        "name": "Blizzard WoW News",
        "url": "https://news.blizzard.com/en-us/feed/world-of-warcraft",
        "keywords": ["warlock", "patch", "hotfix", "class"]
    }
]

class BlizzardNewsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = []
        self.current_article = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "news-card-link" in attributes.get("class", "").split():
            self.current_article = {
                "link": urljoin("https://news.blizzard.com", attributes.get("href", "")),
                "title": ""
            }
        elif tag == "blz-image" and self.current_article:
            self.current_article["title"] = " ".join(attributes.get("alt", "").split())

    def handle_endtag(self, tag):
        if tag == "a" and self.current_article:
            if self.current_article["title"] and self.current_article["link"]:
                self.articles.append(self.current_article)
            self.current_article = None

def article_date(title):
    match = re.search(r"(?:-|:)\s*([A-Z][a-z]+ \d{1,2}, \d{4})$", title)
    if match:
        try:
            return datetime.strptime(match.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
    return datetime.now().strftime("%Y-%m-%d")

def fetch_updates():
    articles = []
    errors = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; WarlockGuideScanner/1.0)"}

    for source in SOURCES:
        try:
            request = urllib.request.Request(source["url"], headers=headers)
            with urllib.request.urlopen(request, timeout=20) as response:
                page = response.read().decode("utf-8", errors="replace")

            parser = BlizzardNewsParser()
            parser.feed(page)
            if not parser.articles:
                raise ValueError("No news cards found in Blizzard's response")

            seen_links = set()
            for article in parser.articles:
                title = article["title"]
                if article["link"] in seen_links or not any(keyword in title.lower() for keyword in source["keywords"]):
                    continue
                seen_links.add(article["link"])
                articles.append({
                    "title": title,
                    "link": article["link"],
                    "date": article_date(title),
                    "summary": f"Officiell WoW-nyhet från {source['name']}."
                })
                if len(articles) >= 8:
                    break
        except Exception as error:
            errors.append(f"{source['name']}: {error}")
            print(f"Kunde inte hämta från {source['name']}: {error}")

    return articles, errors

def main():
    print("Skannar officiella WoW-nyheter för Warlock och patchnotiser...")
    fetched_articles, source_errors = fetch_updates()
    guide_status = "Synkad med Blizzard WoW News" if not source_errors else "Fel vid skanning av Blizzard WoW News"

    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "guide_status": guide_status,
        "total_updates": len(fetched_articles),
        "source_errors": source_errors,
        "articles": fetched_articles
    }

    with open("warlock_patches.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("warlock_patches.json uppdaterad framgångsrikt!")

if __name__ == "__main__":
    main()
