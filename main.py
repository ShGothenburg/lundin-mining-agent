import yfinance as yf
import requests
import os
from datetime import datetime
from openai import OpenAI

# --- CONFIG ---
TICKER = "LUMI.ST"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_stock_price():
    stock = yf.Ticker(TICKER)
    data = stock.history(period="2d")
    if data.empty:
        return None, None

    close = data["Close"].iloc[-1]
    prev = data["Close"].iloc[-2] if len(data) > 1 else None

    return close, prev


def get_copper_price():
    # enkel placeholder (kan uppgraderas senare med riktig API)
    try:
        r = requests.get("https://api.metals.live/v1/spot/copper", timeout=10)
        return r.json()[0]["price"]
    except:
        return None


def generate_ai_report(stock, prev_stock, copper):
    prompt = f"""
Du är en finansanalytiker.

Bolag: Lundin Mining
Aktiekurs idag: {stock}
Aktiekurs igår: {prev_stock}
Kopparpris: {copper}

Skriv en kort daglig investeringsrapport på svenska med:
- kort sammanfattning
- vad som driver kursen
- risker
- möjligheter
- dagens slutsats (positiv / neutral / negativ)
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def create_report():
    stock, prev_stock = get_stock_price()
    copper = get_copper_price()

    ai_text = generate_ai_report(stock, prev_stock, copper)

    report = f"""
📊 Lundin Mining Daglig Rapport
Datum: {datetime.now().strftime('%Y-%m-%d')}

💰 Aktie
- Idag: {stock}
- Igår: {prev_stock}

🪙 Koppar
- Pris: {copper}

🤖 AI-Analys
{ai_text}
"""

    return report


if __name__ == "__main__":
    print(create_report())
