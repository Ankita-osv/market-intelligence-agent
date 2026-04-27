from openai import OpenAI
import requests
import feedparser
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
def fetch_newsapi():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "US economy OR Federal Reserve OR inflation OR stock market",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    
    print("NewsAPI status:", response.status_code)  # DEBUG
    
    data = response.json()

    articles = []
    for article in data.get("articles", []):
        articles.append(article["title"])

    return articles


def fetch_rss():
    feeds = [
        "http://feeds.reuters.com/reuters/businessNews",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    ]

    headlines = []

    for feed in feeds:
        parsed = feedparser.parse(feed)
        for entry in parsed.entries[:5]:
            headlines.append(entry.title)

    return headlines

def fetch_market_data():
    tickers = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Gold": "GC=F",
        "Oil": "CL=F",
        "USD/INR": "INR=X"
    }

    market_data = {}

    for name, ticker in tickers.items():
        data = yf.Ticker(ticker)
        hist = data.history(period="1d")

        if not hist.empty:
            price = hist["Close"].iloc[-1]
            market_data[name] = round(price, 2)
        else:
            market_data[name] = "N/A"

    return market_data

def analyze_with_ai(news, market_data):
     # 🔽 FILTERING
    all_news = news
    filtered_news = []

    keywords = [
        "fed", "interest rate", "inflation",
        "oil", "crude", "geopolitics",
        "earnings", "acquisition", "ipo",
        "ai", "technology", "china", "us",
        "india", "bond", "yield"
    ]

    for article in all_news:
        title = str(article).lower()
        if any(k in title for k in keywords):
            filtered_news.append(title)

    news_data = "\n".join(filtered_news[:10])

  prompt = f"""
You are not a news summarizer. You are a macro strategist.

You must think like:
1. A hedge fund manager
2. A macro economist
3. A retail trader
4. A long-term investor

Analyze the following news deeply:

{news_data}

---

STEP 1: FILTER SIGNAL FROM NOISE
- Ignore irrelevant news
- Pick only market-moving developments
- Explain WHY they matter

---

STEP 2: WHAT IS DIFFERENT THIS TIME?
- Compare with historical behavior
- Is this normal or unusual?
- What has changed vs past similar events?

---

STEP 3: MARKET INTERPRETATION (DEEP)

A. US MARKET
- Which sectors move FIRST and WHY
- Which companies specifically benefit/suffer
- What smart money is likely doing RIGHT NOW

B. INDIA MARKET (VERY IMPORTANT)
- Impact via FPI flows, INR, global cues
- Which Indian sectors/stocks get indirect impact
- What usually happens vs what may happen now

---

STEP 4: MULTI-ORDER EFFECTS

- First-order (immediate reaction)
- Second-order (next 1–2 weeks)
- Third-order (structural shift)

---

STEP 5: ASSET CLASS ROTATION

Impact on:
- Equities
- Bonds (yields)
- Gold
- Oil
- USD
- Crypto
- Volatility (VIX)

Explain FLOW OF MONEY (where money moves)

---

STEP 6: CONTRARIAN VIEW

- What could go WRONG in this narrative?
- Where market might be overreacting

---

STEP 7: CLEAR ACTIONABLE INSIGHTS

- If you were a hedge fund, what would you do?
- If you were a retail investor, what would you avoid?

---

STEP 8: CONTENT ENGINE (HIGH DEPTH)

Give:

1. 3 STRONG HOOKS (not clickbait, insight-driven)

2. 2 REEL SCRIPTS (1–2 MINUTES EACH)
B. 2 HIGH-QUALITY REEL SCRIPTS (1–2 MIN EACH)

Each reel MUST follow this structure:

1. HOOK (first 2–3 seconds)
- Bold, surprising, scroll-stopping

2. EXPLANATION
- Break down what happened in simple terms

3. CAUSE → EFFECT
- Explain WHY it matters
- Connect macro → markets → sectors

4. US → INDIA LINK
- Always explain impact on Indian markets

5. SMART INSIGHT
- What smart money / institutions will do

6. ACTIONABLE CLOSE
- What should viewer watch / think / do

---

TONE:
- Conversational (like explaining to a friend)
- Confident, sharp
- No news-anchor language
- No phrases like “stay tuned”, “markets may fluctuate”

---

This should feel like a finance creator explaining markets, not a reporter reading news.
3. 1 LONG-FORM VIDEO STRUCTURE
- Hook
- Build-up
- Insight
- Conclusion

---

IMPORTANT:
- Avoid generic statements
- Avoid repeating news
- Focus on reasoning, causality, and insight
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content  # Add return

def send_email(content):
    sender_email = "ankitasethi333@gmail.com"
    receiver_email = "ankitasethi333@gmail.com"
    app_password = "qtmg kxdr dqyz fxgw"

    msg = MIMEText(content)
    msg["Subject"] = "📊 Daily Market Intelligence"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("\n📧 Email sent successfully!")
    except TimeoutError:
        print("\n⚠️ Email failed: Gmail SMTP connection timed out. Check your internet connection.")
    except Exception as e:
        print(f"\n⚠️ Email failed: {str(e)}")

def save_analysis_to_file(content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analysis_{timestamp}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Analysis saved to {filename}")
        return filename
    except Exception as e:
        print(f"⚠️ Failed to save analysis: {str(e)}")

def main():
   
    print("🚀 Script started")

    newsapi_news = fetch_newsapi()
    rss_news = fetch_rss()

    all_news = newsapi_news + rss_news
    unique_news = list(set(all_news))

    market_data = fetch_market_data()

    print("\n📰 Collected News:\n")
    for i, news in enumerate(unique_news, 1):
        print(f"{i}. {news}")

    print("\n📊 Market Snapshot:\n")
    for key, value in market_data.items():
        print(f"{key}: {value}")

    analysis = analyze_with_ai(unique_news, market_data)

    print("\n🧠 AI Analysis:\n")
    print(analysis)
    send_email(analysis)
    save_analysis_to_file(analysis)

if __name__ == "__main__":
    main()




