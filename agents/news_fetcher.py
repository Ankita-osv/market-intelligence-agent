
import requests
import feedparser
import os
from dotenv import load_dotenv
from datetime import datetime
from agents.twitter_signals import fetch_twitter_signals
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# -----------------------------------
# STANDARD ARTICLE STRUCTURE
# -----------------------------------

def structure_article(title, summary, source, published, url):

    return {
        "title": title,
        "summary": summary,
        "source": source,
        "published": published,
        "url": url
    }


# -----------------------------------
# NEWS API
# -----------------------------------

def fetch_newsapi():

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "Federal Reserve OR inflation OR oil OR AI OR geopolitics OR stock market",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 15,
        "apiKey": NEWS_API_KEY
    }

    news = []

    try:

        response = requests.get(url, params=params)
        data = response.json()

        for article in data.get("articles", []):

            news.append(
                structure_article(
                    title=article.get("title", ""),
                    summary=article.get("description", ""),
                    source=article.get("source", {}).get("name", ""),
                    published=article.get("publishedAt", ""),
                    url=article.get("url", "")
                )
            )

    except Exception as e:
        print("NewsAPI Error:", e)

    return news


# -----------------------------------
# RSS FEEDS
# -----------------------------------

def fetch_rss():

    feeds = [
        "http://feeds.reuters.com/reuters/businessNews",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    ]

    news = []

    for feed in feeds:

        try:

            parsed = feedparser.parse(feed)

            for entry in parsed.entries[:10]:

                news.append(
                    structure_article(
                        title=entry.get("title", ""),
                        summary=entry.get("summary", ""),
                        source=feed,
                        published=entry.get("published", ""),
                        url=entry.get("link", "")
                    )
                )

        except Exception as e:
            print("RSS Error:", e)

    return news


# -----------------------------------
# MAIN FETCH FUNCTION
# -----------------------------------

def fetch_market_news():

    newsapi_news = fetch_newsapi()

    rss_news = fetch_rss()

    twitter_news = fetch_twitter_signals()

    all_news = newsapi_news + rss_news + twitter_news

    return all_news