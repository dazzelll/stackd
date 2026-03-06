import math
import os
from dotenv import load_dotenv

import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- SCORING ENGINE ---
def calculate_health_score(portfolio, villain_events_count=0, streak_avg=0):
    assets = portfolio.get('assets', [])
    total = portfolio.get('total', 0)
    if total == 0: return {"overall": 0, "diversification": 0, "liquidity": 0, "behavioral_resilience": 0}

    # Diversification (Herfindahl-Hirschman Index)
    hhi = sum([(a['pct'] / 100)**2 for a in assets])
    diversification = min(100, round((1 - hhi) * 125))

    # Liquidity (Savings Blob)
    savings_pct = next((a['pct'] for a in assets if a['name'] == 'Savings'), 0)
    liquidity = min(100, savings_pct * 5)

    # Resilience
    villain_penalty = min(40, villain_events_count * 10)
    streak_bonus = min(20, (streak_avg or 0) * 2)
    resilience = max(0, min(100, 60 + streak_bonus - villain_penalty))

    # Crypto Penalty
    crypto_pct = next((a['pct'] for a in assets if a['name'] == 'Crypto'), 0)
    crypto_penalty = max(0, crypto_pct - 30)

    overall = round((diversification * 0.35) + (liquidity * 0.30) + 
                    (resilience * 0.25) + max(0, 10 - crypto_penalty))
    
    return {
        "overall": min(100, overall),
        "diversification": min(100, diversification),
        "liquidity": min(100, liquidity),
        "behavioral_resilience": resilience
    }

def calculate_wealth_age(total_wealth, real_age, health_score):
    benchmarks = {
        25: 15000, 30: 60000, 35: 130000, 40: 250000, 
        45: 400000, 50: 600000, 55: 900000, 60: 1300000
    }
    wealth_age = real_age
    for age, benchmark in sorted(benchmarks.items()):
        if total_wealth >= benchmark: wealth_age = age
    
    health_bonus = round((health_score - 50) / 10)
    return max(18, wealth_age + health_bonus)

# --- AI SERVICE ---
async def generate_prophecy_text(data):
    try:
        # Use flash for high-speed hackathon responses
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""You are the financial oracle of a Gen Z wealth app called Wealth Wellness Hub.
        Write a SHORT prophecy (2-3 sentences MAX) about this user's financial future.
        Data: Projected wealth: ${data['projectedWealth']}, Freedom year: {data['freedomYear']}, Health score: {data['healthScore']}/100.
        Rules: Sound like a mystical oracle meets a Gen Z bestie. Max 3 sentences. No bullet points."""
        
        # Use the async generation method to prevent blocking the backend
        response = await model.generate_content_async(prompt)
        return response.text.strip()
        
    except Exception as e:
        print("Gemini API Error:", e)
        return "The algorithm has spoken ✨ You are on your way to main character energy."
    
async def generate_villain_roast(assets_data):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a savage, Gen-Z financial advisor AI. 
        The user just ruined their portfolio. 
        Here is their current data: {assets_data}
        
        Write a 1-sentence warning telling them their savings are too low and their crypto is too high. 
        Rules:
        - Keep it strictly under 15 words.
        - Use lowercase letters only.
        - Use Gen-Z slang (e.g., bestie, cooked, wilding, caught in 4k).
        - Do not use hashtags.
        """
        
        # Using async generation to keep the server fast
        response = await model.generate_content_async(prompt)
        return response.text.strip()
        
    except Exception as e:
        print("Gemini API Error:", e)
        return "your savings are depleted and crypto is wilding bestie. we need to fix this."