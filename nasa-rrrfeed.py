import feedparser

# Beispiel-RSS-Feed (NASA News Feed)
rss_url = "https://www.nasa.gov/rss/dyn/breaking_news.rss"

# Feed abrufen
feed = feedparser.parse(rss_url)

# Durch die Feed-Einträge iterieren
for entry in feed.entries:
    print("Titel:", entry.title)
    print("Link:", entry.link)
    print("Zusammenfassung:", entry.summary)
    print("---")
