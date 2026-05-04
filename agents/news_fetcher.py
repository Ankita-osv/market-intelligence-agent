import os
import requests

from datetime import datetime
from dotenv import load_dotenv

# LOAD ENV VARIABLES
load_dotenv()

# NEWS API CONFIG
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

URL = "https://newsapi.org/v2/everything"

# SOURCE QUALITY WEIGHTS
SOURCE_WEIGHTS = {
    "Reuters": 5,
    "Bloomberg": 5,
    "Financial Times": 5,
    "Wall Street Journal": 4,
    "CNBC": 4,
    "Economic Times": 4,
    "Moneycontrol": 4,
    "Twitter": 3,
    "Unknown": 1
}


# GET SOURCE SCORE
def get_source_score(source):

    return SOURCE_WEIGHTS.get(source, 1)


# STRUCTURE ARTICLE
def structure_article(
    title,
    summary,
    source,
    published,
    url,
    category="general"
):

    return {

        "title": title,

        "summary": summary,

        "source": source,

        "source_score": get_source_score(source),

        "published": published,

        "url": url,

        "category": category,

        "fetched_at": datetime.now().isoformat()
    }


# FETCH LIVE MARKET NEWS
def fetch_market_news():

    query = (
        "stock market OR inflation OR Federal Reserve "
        "OR oil OR AI OR geopolitics OR commodities "
        "OR China OR liquidity OR recession "
        "OR earnings OR bond yields"
    )

    params = {

        "q": query,

        "language": "en",

        "sortBy": "publishedAt",

        "pageSize": 20,

        "apiKey": NEWS_API_KEY
    }

    try:

        response = requests.get(
            URL,
            params=params,
            timeout=10
        )

        data = response.json()

        articles = data.get("articles", [])

        structured_news = []

        for article in articles:

            source_name = (
                article.get("source", {})
                .get("name", "Unknown")
            )

            structured_news.append(

                structure_article(

                    title=article.get("title", ""),

                    summary=article.get(
                        "description",
                        ""
                    ),

                    source=source_name,

                    published=article.get(
                        "publishedAt",
                        ""
                    ),

                    url=article.get("url", ""),

                    category="macro"
                )
            )

        return structured_news

    except Exception as e:

        print(f"News Fetch Error: {e}")

        return []