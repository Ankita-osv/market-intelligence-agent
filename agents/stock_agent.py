from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

def run_stock_agent(sector_analysis):

    prompt = f"""
You are a senior equity strategist at a global hedge fund.

Your task is to identify:
- stocks likely to benefit,
- stocks likely at risk,
- sector leaders,
- second-order beneficiaries,
- India and US opportunities.

SECTOR ANALYSIS:
{sector_analysis}

IMPORTANT:
- Think like institutional capital allocators
- Focus on WHY a company benefits
- Include both US and Indian companies
- Avoid generic answers
- Include risks and contrarian concerns

Return STRICTLY in this format:

TOP BULLISH STOCKS:

US STOCKS:
- Stock → why it benefits

INDIA STOCKS:
- Stock → why it benefits

TOP BEARISH STOCKS:
- Stock → why it may struggle

SECOND-ORDER BENEFICIARIES:
- companies indirectly benefiting

KEY RISKS:
- what could invalidate the thesis

CONFIDENCE:

WHY CONFIDENCE:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content