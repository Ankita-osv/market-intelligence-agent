from openai import OpenAI
import requests
import feedparser
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

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
    # ✅ CLEAN NEWS (simple + powerful)
    all_news = news

    # convert everything to text
    clean_news = [str(article).lower() for article in all_news]

    # remove duplicates (optional but good)
    clean_news = list(set(clean_news))

    # take top 8 headlines (important)
    news_data = "\n".join(clean_news[:8])

    # debug print (keep this for now)
    print("DEBUG NEWS DATA:\n", news_data)

    # 🔽 PROMPT
    prompt = f"""
You are a global macro strategist and finance content creator.

Your task is NOT to summarize news.

Your task is to CONNECT the news into one powerful market narrative.

You must think like:
- a hedge fund analyst
- a macro investor
- a finance YouTube creator

---

NEWS:
{news_data}

MARKET DATA:
{market_data}

---

STEP 1: IDENTIFY THE CORE STORY

Identify the SINGLE biggest narrative connecting:
- geopolitics
- AI / technology
- economy
- markets

Do NOT discuss unrelated stories separately.

Connect them into ONE big picture.

---

STEP 2: EXPLAIN THE REAL INSIGHT

Explain:
- what is happening
- why it matters
- what changed compared to before
- what second-order effects may happen next
- where institutional money may flow

Focus heavily on:
- US markets
- India markets
- sectors
- currencies
- AI economy
- rates
- oil
- tech infrastructure

---

STEP 3: MARKET IMPACT

Explain:
- US market impact
- India market impact
- sectors that benefit
- sectors at risk
- stock watchlist ideas

---

STEP 4: WHAT MOST PEOPLE ARE MISSING

Explain:
- what retail investors are not noticing
- what smart money is likely doing
- hidden implications

---

STEP 5: CONTENT CREATOR MODE

Now switch into finance creator mode.

Do NOT sound like a research report.

Sound like:
- a sharp macro creator
- someone explaining hidden market signals
- conversational but intelligent

Avoid:
- textbook explanations
- boring summaries
- generic advice

---

OUTPUT FORMAT:

1. BIGGEST INSIGHT OF THE DAY

2. WHAT MOST PEOPLE ARE MISSING

3. SMART MONEY POSITIONING

4. US vs INDIA IMPACT

5. 3 VIRAL VIDEO HOOKS

Hooks should feel like:
- "Everyone thinks..."
- "But the real story is..."
- "Nobody is noticing..."
- "This changes everything because..."

---

6. 2 FULL REEL SCRIPTS

IMPORTANT:
- 400–500 words EACH
- Speak like I am talking on camera
- Conversational
- Insight-heavy
- Explain cause → effect → market impact
- Connect geopolitics + AI + economy together
- Strong hook in first 2 lines
- Deep but simple
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )


    return response.choices[0].message.content

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




