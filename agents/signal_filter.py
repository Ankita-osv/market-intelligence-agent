IMPORTANT_CATEGORIES = {

    "macro": [
        "inflation",
        "fed",
        "rates",
        "yield",
        "bond",
        "treasury",
        "interest rates",
        "federal reserve",
        "liquidity",
        "bond yields",
        "recession",
        "economy",
        "gdp",
        "unemployment",
        "cpi"
    ],

    "earnings": [
        "earnings",
        "guidance",
        "forecast",
        "revenue",
        "profit",
        "forecast",
        "results",
        "eps",
        "ai spending",
        "capex",
        "margin",
        "beat",
        "miss",
        "quarterly"
    ],

    "market_positioning": [
        "institutional",
        "flows",
        "hedge fund",
        "rotation",
        "positioning",
        "risk appetite",
        "buyback"
    ],

    "consumer_stress": [
        "consumer spending",
        "credit card",
        "debt",
        "retail slowdown",
        "defaults",
        "housing"
    ],

    "geopolitics": [
        "war",
        "sanctions",
        "military",
        "crude",
        "trade restrictions",
        "china",
        "russia",
        "iran",
        "tariffs",
        "nato",
        "taiwan"
    ],

    "technology": [
        "ai",
        "AI",
        "semiconductors",
        "nvidia",
        "automation",
        "data centers",
        "robotics",
        "openai",
        "chips",
        "microsoft",
        "google",
        "cloud computing"
    ],

    "commodities": [
        "oil",
        "gold",
        "copper",
        "energy",
        "natural gas",
        "commodities",
        "uranium"
    ],

    "currencies": [
        "usd",
        "yuan",
        "rupee",
        "de-dollarization",
        "currency",
        "dollar"
        ],
    "market_behavior": [ 
        "stocks rise", 
        "market rally", 
        "equities surge", 
        "S&P 500", 
        "Nasdaq", 
        "risk-on", 
        "risk appetite", 
        "valuation", 
        "liquidity rally", 
        "all-time high", 
        "bull market" ],

    "institutional_flows": [
        "hedge funds",
        "etf inflows",
        "capital flows",
        "positioning",
        "rotation",
        "fund managers",
        "etf flows",
        "bond fund flows",
        "treasure yield",
       "institutional investors",
        "risk-on",
        "risk-off"
    ]
}


NEGATIVE_KEYWORDS = [

    "celebrity",
    "football",
    "movie",
    "hospitalized",
    "viral",
    "entertainment",
    "crime",
    "gossip",
    "sports",
    "fashion",
    "music",
    "tv show",
    "wedding"
]

CATEGORY_WEIGHTS = {

    "macro": 3,

    "earnings": 5,

    "market_positioning": 5,

    "consumer_stress": 4,

    "geopolitics": 2,

    "technology": 5,

    "commodities": 2,

    "currencies": 3,

    "market_behavior": 5,

    "institutional_flows": 5
}


def score_article(title, summary=""):

    text = f"{title} {summary}".lower()

    score = 0

    # POSITIVE SCORING
    for category, keywords in IMPORTANT_CATEGORIES.items():

        for keyword in keywords:

            if keyword in text:
                score += CATEGORY_WEIGHTS.get(category, 3)

    # NEGATIVE SCORING
    for keyword in NEGATIVE_KEYWORDS:

        if keyword in text:
            score -= 5

    return score



from datetime import datetime


def calculate_time_weight(published_time):

    try:

        # Handle ISO timestamps
        published_dt = datetime.fromisoformat(
            published_time.replace("Z", "")
        )

        hours_old = (
            datetime.utcnow() - published_dt
        ).total_seconds() / 3600

        # Freshness weighting
        if hours_old <= 3:
            return 1.0

        elif hours_old <= 12:
            return 0.8

        elif hours_old <= 24:
            return 0.6

        elif hours_old <= 48:
            return 0.4

        else:
            return 0.2

    except:
        # fallback if timestamp parsing fails
        return 0.5


def filter_market_news(news_items):

    scored_news = []

    for item in news_items:

        # Support dict + string headlines
        if isinstance(item, str):

            title = item
            summary = ""
            published = ""

        else:

            title = item.get("title", "")
            summary = item.get("summary", "")
            published = item.get("published", "")

        # Existing relevance score
        score = score_article(title, summary)

        # NEW: Time relevance
        time_weight = calculate_time_weight(published)

        # FINAL SCORE
        final_score = score * time_weight

        # Keep only relevant news
        if final_score > 0.5:

            scored_news.append({
                "title": title,
                "summary": summary,
                "score": round(final_score, 2),
                "published": published
            })

    # SORT BY FINAL SCORE
    scored_news = sorted(
        scored_news,
        key=lambda x: x["score"],
        reverse=True
    )

    # RETURN TOP 10
    return scored_news[:10]



def run_signal_filter(headlines):
    """
    Analyze filtered headlines and generate signal analysis
    """
    if not headlines:
        return "No significant market signals detected from recent news."
    
    # Count occurrences of important categories
    category_counts = {}
    for category in IMPORTANT_CATEGORIES.keys():
        category_counts[category] = 0
    
    for headline in headlines:
        text = headline.lower()
        for category, keywords in IMPORTANT_CATEGORIES.items():
            for keyword in keywords:
                if keyword in text:
                    category_counts[category] += 1
    
    # Generate analysis
    signals = []
    for category, count in category_counts.items():
        if count > 0:
            signals.append(f"{category.replace('_', ' ').title()}: {count} signals")
    
    if signals:
        analysis = "Market Signal Analysis:\n" + "\n".join(signals)
    else:
        analysis = "No strong market signals detected in current news cycle."
    
    return analysis