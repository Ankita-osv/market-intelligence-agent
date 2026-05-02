from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

def run_contrarian_agent(
    macro_analysis,
    sector_analysis,
    stock_analysis
):

    prompt = f"""
You are a contrarian hedge fund strategist.

Your task is NOT to agree with the main narrative.

Your task is to:
- challenge assumptions,
- identify weak logic,
- detect crowded trades,
- identify hidden risks,
- explain what could go wrong.

INPUTS:

MACRO ANALYSIS:
{macro_analysis}

SECTOR ANALYSIS:
{sector_analysis}

STOCK ANALYSIS:
{stock_analysis}

IMPORTANT:
- Think independently
- Be skeptical
- Avoid consensus thinking
- Look for hidden risks
- Focus on second-order effects
- Identify overconfidence
- Identify fragile narratives

Return STRICTLY in this format:

MAIN NARRATIVE BEING PRICED:
- what markets currently believe

WHY THIS NARRATIVE MAY FAIL:
- weaknesses in the logic

POSSIBLE MARKET REVERSALS:
- what could suddenly change

CROWDED TRADES:
- what looks overcrowded

UNDERAPPRECIATED RISKS:
- what investors may be ignoring

CONTRARIAN OPPORTUNITIES:
- areas the market may be underestimating

CONFIDENCE:

WHY CONFIDENCE:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content