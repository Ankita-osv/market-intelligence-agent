from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

def run_macro_agent(news, market_data):
    if not client:
        return "Error: OPENAI_API_KEY not set in environment"

    prompt = f"""
You are a senior global macro strategist.

Your task is to identify the SINGLE most important global market narrative.

Focus on:
- Federal Reserve
- inflation
- oil
- geopolitics
- AI economy
- liquidity
- currencies
- global capital flows

NEWS:
{news}

MARKET DATA:
{market_data}

IMPORTANT:
- Think like a hedge fund macro analyst
- Connect events together
- Identify second-order effects
- Explain where institutional money may flow

Return your answer STRICTLY in this format:

MACRO THEME:
MARKET REGIME:
KEY DRIVERS:
BULLISH FOR:
BEARISH FOR:
CONFIDENCE:
WHY CONFIDENCE:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content