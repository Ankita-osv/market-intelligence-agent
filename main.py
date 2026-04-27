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
You are a global macro analyst and content creator.

Your job is NOT to summarize news.
Your job is to extract ONE strong market insight.

---

INPUT:

NEWS:
{news_data}

MARKET DATA:
{market_data}

---

STEP 1: FIND ONE DOMINANT THEME

Pick ONLY ONE theme that impacts markets.
Examples:
- Oil / geopolitics
- Interest rates / inflation
- Capital flows

Ignore all unrelated news.

---

STEP 2: BUILD A CLEAR LOGIC

Explain:

- What happened (simple)
- Why it matters
- Impact on US markets
- Impact on India markets
- What smart money will do

---

STEP 3: OUTPUT FORMAT

1. THEME
2. US IMPACT
3. INDIA IMPACT
4. MONEY FLOW
5. ACTIONABLE INSIGHT

---

STEP 4: REEL CONTENT

Write 2 FULL REEL SCRIPTS (1–2 min each)

STRICT RULES:

- Write like speaking on camera
- Use simple conversational tone
- No titles, no captions
- No “explore”, “stay tuned”, “markets may fluctuate”

---

STRUCTURE:

HOOK:
Strong opening line

BODY:
Explain clearly step-by-step

INSIGHT:
What most people are missing

CLOSING:
Clear takeaway

---

IMPORTANT:
- Stick ONLY to given news
- Do NOT introduce outside topics
- Focus on ONE idea only
"""---

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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




