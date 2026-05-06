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


def detect_market_contradictions(market_data, narratives):

    contradictions = []

    oil = market_data.get("oil")
    spx = market_data.get("sp500")
    dollar = market_data.get("dollar")
    yields = market_data.get("bond_yields")

    # Oil up + equities up
    if oil == "up" and spx == "up":
        contradictions.append(
            "Oil and equities are rising together. Markets may be ignoring inflation risks due to excess liquidity or AI optimism."
        )

    # Dollar down + equities up
    if dollar == "down" and spx == "up":
        contradictions.append(
            "Weak dollar + rising equities suggests global liquidity is driving risk appetite."
        )

    # Yields up + tech up
    if yields == "up" and "ai" in narratives:
        contradictions.append(
            "Tech rally despite rising yields suggests AI momentum is overpowering macro tightening fears."
        )

    return contradictions


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


def detect_market_contradictions(market_data, narratives):

    contradictions = []

    oil = market_data.get("Oil")
    spx = market_data.get("S&P 500")
    dollar = market_data.get("USD/INR")
    yields = market_data.get("bond_yields")

    # Oil up + equities up
    if oil and oil > 100 and spx and spx > 5000:
        contradictions.append(
            "Oil and equities are rising together. Markets may be ignoring inflation risks due to excess liquidity or AI optimism."
        )

    # Dollar down + equities up
    if dollar and dollar < 85 and spx and spx > 5000:
        contradictions.append(
            "Weak dollar + rising equities suggests global liquidity is driving risk appetite."
        )

    # Yields up + tech up
    if yields and yields > 4 and "ai" in str(narratives).lower():
        contradictions.append(
            "Tech rally despite rising yields suggests AI momentum is overpowering macro tightening fears."
        )

    return contradictions
