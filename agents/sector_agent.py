from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

def run_sector_agent(macro_analysis, market_data):

    prompt = f"""
You are a senior cross-asset sector strategist.

Your task is to identify:
- which sectors benefit,
- which sectors are at risk,
- where institutional capital may rotate.

MACRO ANALYSIS:
{macro_analysis}

MARKET DATA:
{market_data}

IMPORTANT:
- Think like a hedge fund sector strategist
- Focus on capital flows
- Explain second-order effects
- Identify both winners and losers
- Include US and Indian market sectors

Return STRICTLY in this format:

BULLISH SECTORS:
- sector name → why

BEARISH SECTORS:
- sector name → why

INSTITUTIONAL FLOWS:
- where smart money may rotate

US MARKET IMPACT:

INDIA MARKET IMPACT:

CONFIDENCE:

WHY CONFIDENCE:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content