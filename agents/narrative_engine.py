from collections import defaultdict

THEMES = {
    "oil_geopolitics": [
        "iran",
        "oil",
        "hormuz",
        "middle east",
        "crude",
        "blockade",
        "war"
    ],

    "fed_liquidity": [
        "federal reserve",
        "inflation",
        "rates",
        "liquidity",
        "bond yields",
        "interest rates"
    ],

    "ai_infrastructure": [
        "nvidia",
        "ai",
        "gpu",
        "datacenter",
        "semiconductor",
        "openai",
        "microsoft"
    ],

    "consumer_stress": [
        "consumer",
        "spending",
        "debt",
        "credit",
        "retail slowdown"
    ]
}

def detect_dominant_narratives(news):
    scores = defaultdict(int)

    for article in news:
        article_lower = article.lower()
        for theme, keywords in THEMES.items():
            for keyword in keywords:
                if keyword in article_lower:
                    scores[theme] += 1

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores
