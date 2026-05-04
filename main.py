import os
from dotenv import load_dotenv
load_dotenv()

import requests
import feedparser
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from agents.news_fetcher import fetch_market_news
from agents.signal_filter import filter_market_news, run_signal_filter
from agents.narrative_engine import detect_dominant_narratives
from agents.macro_agent import run_macro_agent
from agents.sector_agent import run_sector_agent
from agents.stock_agent import run_stock_agent
from agents.creator_agent import run_creator_agent
from agents.contrarian_agent import run_contrarian_agent
from agents.memory_agent import (
    save_daily_memory,
    load_recent_memories
)
from agents.confidence_agent import run_confidence_agent
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
#
# def analyze_with_ai(news, market_data):
#     # ✅ CLEAN NEWS (simple + powerful)
#     all_news = news
#
#     # convert everything to text
#     clean_news = [str(article).lower() for article in all_news]
#
#     # remove duplicates (optional but good)
#     clean_news = list(set(clean_news))
#
#     # take top 8 headlines (important)
#     news_data = "\n".join(clean_news[:8])
#
#     # debug print (keep this for now)
#     print("DEBUG NEWS DATA:\n", news_data)
#
#     # 🔽 PROMPT
#     prompt = f"""
# You are a global macro strategist and finance content creator.
#
# Your task is NOT to summarize news.
#
# Your task is to CONNECT the news into one powerful market narrative.
#
# You must think like:
# - a hedge fund analyst
# - a macro investor
# - a finance YouTube creator
#
# ---
#
# NEWS:
# {news_data}
#
# MARKET DATA:
# {market_data}
#
# ---
#
# STEP 1: IDENTIFY THE CORE STORY
#
# Identify the SINGLE biggest narrative connecting:
# - geopolitics
# - AI / technology
# - economy
# - markets
#
# Do NOT discuss unrelated stories separately.
#
# Connect them into ONE big picture.
#
# ---
#
# STEP 2: EXPLAIN THE REAL INSIGHT
#
# Explain:
# - what is happening
# - why it matters
# - what changed compared to before
# - what second-order effects may happen next
# - where institutional money may flow
#
# Focus heavily on:
# - US markets
# - India markets
# - sectors
# - currencies
# - AI economy
# - rates
# - oil
# - tech infrastructure
#
# ---
#
# STEP 3: MARKET IMPACT
#
# Explain:
# - US market impact
# - India market impact
# - sectors that benefit
# - sectors at risk
# - stock watchlist ideas
#
# ---
#
# STEP 4: WHAT MOST PEOPLE ARE MISSING
#
# Explain:
# - what retail investors are not noticing
# - what smart money is likely doing
# - hidden implications
#
# ---
#
# STEP 5: CONTENT CREATOR MODE
#
# Now switch into finance creator mode.
#
# Do NOT sound like a research report.
#
# Sound like:
# - a sharp macro creator
# - someone explaining hidden market signals
# - conversational but intelligent
#
# Avoid:
# - textbook explanations
# - boring summaries
# - generic advice
#
# ---
#
# OUTPUT FORMAT:
#
# 1. BIGGEST INSIGHT OF THE DAY
#
# 2. WHAT MOST PEOPLE ARE MISSING
#
# 3. SMART MONEY POSITIONING
#
# 4. US vs INDIA IMPACT
#
# 5. 3 VIRAL VIDEO HOOKS
#
# Hooks should feel like:
# - "Everyone thinks..."
# - "But the real story is..."
# - "Nobody is noticing..."
# - "This changes everything because..."
#
# ---
#
# 6. 2 FULL REEL SCRIPTS
#
# IMPORTANT:
# - 400–500 words EACH
# - Speak like I am talking on camera
# - Conversational
# - Insight-heavy
# - Explain cause → effect → market impact
# - Connect geopolitics + AI + economy together
# - Strong hook in first 2 lines
# - Deep but simple
# """
#
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )
#
#
#     return response.choices[0].message.content

def send_email(content):
    sender_email = "ankitasethi333@gmail.com"
    receiver_email = "ankitasethi333@gmail.com"
    app_password = "qtmg kxdr dqyz fxgw"

    msg = MIMEText(content)
    msg["Subject"] = "Daily Market Intelligence"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("\nEmail sent successfully!")
    except TimeoutError:
        print("\nEmail failed: Gmail SMTP connection timed out. Check your internet connection.")
    except Exception as e:
        print(f"\nEmail failed: {str(e)}")

def save_analysis_to_file(content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/analysis_{timestamp}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Analysis saved to {filename}")
        return filename
    except Exception as e:
        print(f"Failed to save analysis: {str(e)}")

def fetch_market_data():
    """Fetch current market data for key indices and commodities"""
    try:
        # Define tickers
        tickers = {
            "S&P 500": "^GSPC",
            "Nasdaq": "^IXIC", 
            "Gold": "GC=F",
            "Oil": "CL=F",
            "USD/INR": "INR=X"
        }
        
        market_data = {}
        for name, ticker in tickers.items():
            try:
                stock = yf.Ticker(ticker)
                # Get the most recent closing price
                hist = stock.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                    market_data[name] = round(price, 2)
                else:
                    market_data[name] = "N/A"
            except Exception as e:
                market_data[name] = f"Error: {str(e)}"
        
        return market_data
    except Exception as e:
        print(f"Failed to fetch market data: {str(e)}")
        return {
            "S&P 500": "N/A",
            "Nasdaq": "N/A", 
            "Gold": "N/A",
            "Oil": "N/A",
            "USD/INR": "N/A"
        }

def main():
   
    print("Script started")

    all_news = fetch_market_news()

    unique_news = list(set([item["title"] for item in all_news]))
    # FILTER IMPORTANT MARKET NEWS

    filtered_news = filter_market_news(all_news)

    filtered_headlines = [
        item["title"]
        for item in filtered_news
    ]
    
    dominant_narratives = detect_dominant_narratives(filtered_headlines)

    print("\n🔥 DOMINANT MARKET NARRATIVES:\n")
    print(dominant_narratives)

    signal_analysis = run_signal_filter(filtered_headlines)  
    print("\nSIGNAL FILTER OUTPUT:\n")
    print(signal_analysis)  


    market_data = fetch_market_data()
    recent_memory = load_recent_memories()

    print("\nCollected News:\n")
    for i, news in enumerate(filtered_headlines, 1):
        print(f"{i}. {news}")

    print("\nMarket Snapshot:\n")
    for key, value in market_data.items():
        print(f"{key}: {value}")

    macro_analysis = run_macro_agent(
        signal_analysis,
        market_data,
        dominant_narratives,
        recent_memory
    )
    sector_analysis = run_sector_agent(macro_analysis, market_data)
    stock_analysis = run_stock_agent(sector_analysis)
    contrarian_analysis = run_contrarian_agent(
        macro_analysis,
        sector_analysis,
        stock_analysis,
    )
    confidence_analysis = run_confidence_agent(
        macro_analysis,
        sector_analysis,
        stock_analysis,
        contrarian_analysis,
    )
    creator_content = run_creator_agent(
        macro_analysis,
        sector_analysis,
        stock_analysis,
        contrarian_analysis,
        confidence_analysis,
    )

    print("\nMACRO AGENT OUTPUT:\n")
    print(macro_analysis)
    print("\nSECTOR AGENT OUTPUT:\n")
    print(sector_analysis)
    print("\nSTOCK AGENT OUTPUT:\n")
    print(stock_analysis)
    print("\nCREATOR SCRIPT OUTPUT:\n")
    print(creator_content)
    print("\nCONTRARIAN AGENT OUTPUT:\n")
    print(contrarian_analysis)
    print("\nCONFIDENCE AGENT OUTPUT:\n")
    print(confidence_analysis)

    final_output = f"""
================ MACRO ANALYSIS ================

{macro_analysis}

================ SECTOR ANALYSIS ================

{sector_analysis}

================ STOCK ANALYSIS ================

{stock_analysis}
================ CONFIDENCE ANALYSIS ================

{confidence_analysis}

================ CREATOR CONTENT ================

{creator_content}


"""

    send_email(final_output)
    save_analysis_to_file(final_output)
    save_daily_memory(final_output)

if __name__ == "__main__":
    main()




