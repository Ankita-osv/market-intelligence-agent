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
    "iran", "oil", "crude", "hormuz",
    "war", "attack", "geopolitics",
    "fed", "inflation", "interest rate"
]

for article in all_news:
    title = str(article).lower()
    
    # only keep strong macro signals
    if any(k in title for k in keywords):
        filtered_news.append(title)

# remove duplicates
filtered_news = list(set(filtered_news))

# 🚨 HARD LIMIT
news_data = "\n".join(filtered_news[:3])

  prompt = f"""
You are a macro analyst.

You must follow instructions EXACTLY.

---

INPUT:

NEWS:
{news_data}

MARKET DATA:
{market_data}

---

STEP 1: SELECT ONE THEME

From the NEWS, choose ONLY ONE dominant theme.

RULES:
- All output must be based on this ONE theme
- Ignore all unrelated news
- Do not mix multiple topics

---

STEP 2: ANALYSIS

Explain clearly:

- What happened
- Why it matters
- Impact on US markets (specific sectors)
- Impact on India markets (INR, sectors)
- Where money will flow

---

STEP 3: OUTPUT FORMAT

THEME:
(one line)

ANALYSIS:
(5–6 lines, clear cause → effect)

---

STEP 4: REEL SCRIPTS

REEL SCRIPTS (IMPORTANT):

Write like I am speaking on camera.

No titles. No descriptions. No formal tone.

---

SCRIPT 1:

"Listen, if this Iran situation escalates, don’t just think about war.

The real impact is oil.

If oil prices go up, inflation in the US goes up again.

That means Fed will delay rate cuts.

And when that happens, markets don’t like it.

Now for India, it’s even bigger.

We import oil, so higher crude means pressure on INR and markets.

So smart money is watching oil, not headlines.

That’s the real signal here."

---

SCRIPT 2:

"Everyone is focusing on the conflict itself.

But the bigger story is supply disruption.

If shipping through Hormuz gets affected, oil supply tightens.

That pushes global prices up.

US markets react through inflation fears.

India reacts through currency pressure.

So if you’re investing, don’t track the war.

Track oil prices.

That’s where the real opportunity is."
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




