import os

# Disable Flask from loading .env automatically
os.environ["FLASK_SKIP_DOTENV"] = "1"

from flask import Flask ,render_template,request
import feedparser

app = Flask(__name__)

RSS_FEEDS = {
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
    'Hacker News': 'https://news.ycombinator.com/rss',
    'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'CNBC': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069'
}

@app.route("/")
def index():
    articales = []
    for source , feed in RSS_FEEDS.items():
        parse_feed = feedparser.parse(feed)
        entries = [(source,entry) for entry in parse_feed.entries]
        articales.extend(entries)

    articales = sorted(articales, key=lambda x: x[1].published_parsed, reverse=True)

    page = request.args.get("page", 1,type=int)
    per_page = 10 
    total_articales = len(articales)
    start = (page - 1) * per_page 
    end = start + per_page
    paginated_articales = articales[start:end]

    return render_template(template_name_or_list="index.html", articales=paginated_articales, page=page , total_pages = total_articales // per_page + 1)

@app.route("/search")
def search():
    query = request.args.get("q")

    articales = []
    for source , feed in RSS_FEEDS.items():
        parse_feed = feedparser.parse(feed)
        entries = [(source,entry) for entry in parse_feed.entries]
        articales.extend(entries)

    results = [articales for article in articales if query.lower() in articales[1].title.lower()]

    return render_template(template_name_or_list="search.html",articales=results,query=query)

if __name__ == "__main__":
    app.run(debug=True)

    