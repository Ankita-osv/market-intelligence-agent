from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

def run_creator_agent(
    macro_analysis,
    sector_analysis,
    stock_analysis,
    contrarian_analysis,
):

    prompt = f"""
You are a sharp Indian financial creator speaking to intelligent Indian retail investors.

Your job is NOT to summarize markets.

Your job is to:
- explain the hidden narrative,
- connect macro + sectors + stocks,
- sound conversational,
- sound insightful,
- sound human,
- sound like a smart market commentator.

IMPORTANT TONE:
- intelligent but simple
- conversational English
- NOT robotic
- NOT textbook style
- NOT corporate jargon
- sound like a finance creator on camera
- slightly provocative
- insight-heavy
- explain what most people are missing

You are speaking to:
- ambitious Indian investors
- startup people
- tech audience
- market enthusiasts

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

Create:
1. TWO SHORT REEL SCRIPT (~500-700 words)
2. TWO LONG VIDEO SCRIPT (~1200-1500 words)

For BOTH:
- start with a strong hook
- connect geopolitics + economy + AI + markets
- explain cause and effect
- mention sectors and stocks naturally
- explain where smart money may flow
- include India implications
- include contrarian thinking
- avoid generic motivation-style content

VERY IMPORTANT:
Do NOT sound AI-generated.

Avoid:
- bullet-point style narration
- repetitive wording
- textbook finance explanations

Instead:
- sound fluid
- natural
- intelligent
- emotionally engaging

OUTPUT FORMAT:

SHORT REEL SCRIPT:
...

LONG VIDEO SCRIPT:
...
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content