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

  prompt = prompt = f"""
You are a global macro strategist and content creator.

Your job is NOT to summarize news.
Your job is to extract SIGNAL from NOISE and explain market impact.

---

INPUT:

NEWS:
{news_data}

MARKET DATA:
{market_data}

---

STEP 1: IDENTIFY ONE DOMINANT MACRO THEME

From the news, identify ONLY ONE dominant theme that impacts global markets.

Examples:
- Oil / Middle East tension
- Interest rates / inflation
- AI / tech capital shift
- Geopolitical risk

RULES:
- All selected points MUST relate to the SAME theme
- If news is unrelated → IGNORE it completely
- Do NOT mix biotech + AI + geopolitics

Output ONE clear theme only.

---

STEP 2: DEEP ANALYSIS

For EACH selected event:

- What happened? (1 line)
- Why does it matter?
- What changes vs expectations?
- Market reaction path:
  Event → Asset → Sector → Stocks

---

STEP 3: GLOBAL LINKAGE

Explain clearly:

- US market impact (specific sectors + companies)
- India market impact (FPI, INR, sectors, companies)

---

STEP 4: MULTI-LAYER IMPACT

Break into:
- Immediate impact
- Short-term (days/weeks)
- Structural (long-term)

---

STEP 5: MONEY FLOW

Where is capital moving?
What will smart money (institutions) do?

---

STEP 6: FINAL OUTPUT FORMAT

1. KEY EVENTS (max 2–3, deeply explained)

2. US MARKET IMPACT
(mention sectors + example companies)

3. INDIA MARKET IMPACT
(include INR, FPI, sectors, stocks)

4. MULTI-LAYER IMPACT

5. WHERE MONEY IS FLOWING

6. ACTIONABLE INSIGHTS
(what should someone watch or do)

---

7. CONTENT CREATION

A. 3 STRONG HOOKS

---

B. 2 REEL SCRIPTS (1–2 MIN EACH)

Write EXACTLY like someone speaking on camera.

STRICT FORMAT:

Script must be in spoken Hinglish/English tone.

---

REEL 1:

HOOK:
(1 strong opening line)

BODY:
Explain step-by-step:
- What happened
- Why it matters
- Impact on US markets
- Impact on India

INSIGHT:
What most people are missing

CLOSING:
1 sharp takeaway

---

RULES:
- Write in short spoken sentences
- No titles, no descriptions
- No “explore”, “dive into”
- No narration tone
- It should feel like I can directly read this in a reel

---

Example tone:

“If oil prices go up from here, don’t just think petrol prices…  
this actually changes inflation, Fed decisions, and even Indian markets…”"""---

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




