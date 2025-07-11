=== main.py ===

import pandas as pd import numpy as np import requests import pandas_ta as ta from datetime import datetime import pytz

=== Telegram Setup ===

TELEGRAM_TOKEN = "38172768175:AAGe_4nBGJthZYdN3UQr3VL97x8-5I5bNng" CHAT_ID = "1644693247"

def send_telegram_alert(message): url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" data = {"chat_id": CHAT_ID, "text": message} requests.post(url, data=data)

=== Price Data Fetching (Mocked for now) ===

def fetch_price_data(): # Example OHLC structure; replace with live XAUUSD data source later data = { "time": pd.date_range(end=datetime.now(), periods=100, freq="5min"), "open": np.random.uniform(3300, 3350, 100), "high": np.random.uniform(3350, 3380, 100), "low": np.random.uniform(3280, 3320, 100), "close": np.random.uniform(3300, 3360, 100), } return pd.DataFrame(data)

=== Signal Logic ===

def check_for_signals(df): df.ta.ema(length=50, append=True) df.ta.ema(length=200, append=True) df.ta.rsi(length=14, append=True) df.ta.macd(append=True) df.ta.atr(length=14, append=True)

last = df.iloc[-1]

signal = None
reason = []

if last["RSI_14"] > 50:
    if last["EMA_50"] > last["EMA_200"]:
        signal = "BUY"
        reason.append("Trend Up (50 > 200 EMA)")
elif last["RSI_14"] < 50:
    if last["EMA_50"] < last["EMA_200"]:
        signal = "SELL"
        reason.append("Trend Down (50 < 200 EMA)")

if signal:
    confidence = 75
    message = (
        f"XAUUSD {signal} Signal\n"
        f"Confidence: {confidence}%\n"
        f"Reason: {'; '.join(reason)}\n"
        f"Price: {last['close']:.2f}\nTime: {datetime.now(pytz.timezone('Africa/Nairobi')).strftime('%H:%M:%S')}"
    )
    send_telegram_alert(message)
else:
    print("No valid signal this round.")

=== Main Execution ===

if name == "main": df = fetch_price_data() check_for_signals(df)


