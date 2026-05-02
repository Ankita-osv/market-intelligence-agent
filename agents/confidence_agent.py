from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

def run_confidence_agent(
    macro_analysis,
    sector_analysis,
    stock_analysis,
    contrarian_analysis
):

    prompt = f"""
You are a hedge fund risk and confidence analyst.

Your task is to evaluate:
- which conclusions are strongly supported,
- which conclusions are speculative,
- where evidence is weak,
- where narrative is overpowering facts.

INPUTS:

MACRO ANALYSIS:
{macro_analysis}

SECTOR ANALYSIS:
{sector_analysis}

STOCK ANALYSIS:
{stock_analysis}

CONTRARIAN ANALYSIS:
{contrarian_analysis}

IMPORTANT:
- Think probabilistically
- Separate evidence from narrative
- Identify weak assumptions
- Evaluate confidence honestly
- Avoid overconfidence
- Think like a risk committee member

Return STRICTLY in this format:

HIGH-CONFIDENCE SIGNALS:
- signal → why confidence is high

MEDIUM-CONFIDENCE SIGNALS:
- signal → uncertainty involved

LOW-CONFIDENCE / SPECULATIVE THEMES:
- theme → why evidence is weak

NARRATIVES DOMINATING MARKETS:
- where psychology may exceed fundamentals

MOST RELIABLE DATA POINTS:
- strongest evidence currently available

BIGGEST UNKNOWN VARIABLES:
- what markets cannot predict well

OVERALL MARKET CONFIDENCE:
- Low / Medium / High

WHY:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content