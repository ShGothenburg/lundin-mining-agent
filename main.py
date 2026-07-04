import yfinance as yf
import requests
from datetime import datetime

# --- CONFIG ---
TICKER = "LUMI.ST"  # Lundin Mining på Stockholmsbörsen

def get_stock_price():
    stock = yf.Ticker(TICKER)
    data = stock.history(period="1d")
    if data.empty:
        return None
    return data["Close"].iloc[-1]

def get_copper_price():
    # enkel proxy (kan förbättras senare)
    url = "https://www.lme.com/api/prices"
    try:
        r = requests.get(url, timeout=10)
        return "OK (placeholder)"
    except:
        return "Ej tillgänglig"

def create_report():
    price = get_stock_price()
    copper = get_copper_price()

    report = f"""
📊 Lundin Mining Daglig Rapport
Datum: {datetime.now().strftime('%Y-%m-%d')}

💰 Aktie
- Pris: {price} SEK

🪙 Koppar
- Status: {copper}

🤖 AI-analys
- Systemet är igång (version 1)
"""
    return report

if __name__ == "__main__":
    print(create_report())
