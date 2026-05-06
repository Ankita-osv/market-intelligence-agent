def fetch_twitter_signals():

    try:
        import snscrape.modules.twitter as sntwitter
    except Exception as e:
        print("snscrape not available or failed to import:", e)
        return []

    queries = [
        "stock market",
        "Federal Reserve",
        "AI stocks",
        "Nvidia",
        "oil prices",
        "inflation",
        "earnings"
    ]

    tweets = []

    for query in queries:

        try:

            for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(query).get_items()
            ):

                if i > 5:
                    break

                tweets.append({
                    "title": tweet.content,
                    "summary": tweet.content,
                    "source": "Twitter",
                    "published": str(tweet.date),
                    "url": tweet.url
                })

        except Exception as e:
            print("Twitter scrape failed:", e)

    return tweets
