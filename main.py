import pandas as pd
import pandas as pd
import pandas_ta.overlap as overlap
import pandas_ta.momentum as momentum
import pandas_ta.trend as trend
def add_indicators(df):
    df['EMA50'] = ta.ema(df['close'], length=50)
    df['EMA200'] = ta.ema(df['close'], length=200)
    macd = ta.macd(df['close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    df['RSI'] = ta.rsi(df['close'], length=14)
    df.dropna(inplace=True)
    return df
import requests
import time
import datetime
import pytz
from telegram import Bot
import numpy as np

# === Setup ===
BOT_TOKEN = "38172768175:AAGe_4nBGJthZYdN3UQr3VL97x8-5I5bNng"
CHAT_ID = "1644693247"
bot = Bot(token=BOT_TOKEN)

# === Config ===
CONFIDENCE_THRESHOLD = 70
CHECK_INTERVAL = 300  # 5 minutes

# === Fetch Price (Simulated with random values, replace with real API later) ===
def get_price():
    try:
        # 🔁 Replace this with your real XAUUSD price fetch (e.g., from a broker or API)
        price = np.random.randint(3250, 3450)  # Example random price
        return price
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# === RSI Calculation ===
def calculate_rsi(prices, period=14):
    if len(prices) < period:
        return 50  # neutral
    deltas = np.diff(prices)
    ups = deltas[deltas > 0].sum() / period
    downs = -deltas[deltas < 0].sum() / period
    rs = ups / downs if downs != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

# === Signal Generator ===
def generate_signal(rsi, price):
    confidence = 60 + abs(rsi - 50)  # simplistic confidence
    signal = None
    if rsi > 55:
        signal = f"🔼 BUY XAUUSD at {price} | RSI: {rsi:.2f} | Confidence: {confidence:.1f}%"
    elif rsi < 45:
        signal = f"🔽 SELL XAUUSD at {price} | RSI: {rsi:.2f} | Confidence: {confidence:.1f}%"
    return signal if confidence >= CONFIDENCE_THRESHOLD else None

# === Kenya Time Filter ===
def is_within_trading_hours():
    kenya = pytz.timezone("Africa/Nairobi")
    now = datetime.datetime.now(kenya)
    return now.hour >= 9 and now.hour < 17  # 9AM–5PM Kenya time

# === Main Loop ===
price_history = []

print("📡 XAUUSD Bot started...")

while True:
    if is_within_trading_hours():
        price = get_price()
        if price:
            price_history.append(price)
            if len(price_history) > 100:
                price_history.pop(0)

            rsi = calculate_rsi(price_history)
            signal = generate_signal(rsi, price)

            if signal:
                print(f"✅ Signal: {signal}")
                try:
                    bot.send_message(chat_id=CHAT_ID, text=signal)
                except Exception as e:
                    print(f"Telegram Error: {e}")
            else:
                print(f"ℹ️ No strong signal | RSI: {rsi:.2f}")
        else:
            print("⚠️ Price fetch failed")
    else:
        print("⏳ Outside Kenya trading hours (9AM–5PM). Waiting...")

    time.sleep(CHECK_INTERVAL)
