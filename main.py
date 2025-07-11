from flask import Flask
import pandas as pd
import requests
import pandas_ta.overlap as overlap
import pandas_ta.momentum as momentum
import pandas_ta.trend as trend

# Telegram setup
TELEGRAM_TOKEN = "38172768175:AAGe_4nBGJthZYdN3UQr3VL97x8-5I5bNng"
CHAT_ID = "1644693247"

app = Flask(__name__)

@app.route('/')
def home():
    return "🔁 XAUUSD bot is running."

@app.route('/check_signal')
def check_signal():
    # Sample price data (use live price or historical CSV)
    df = pd.read_csv("https://raw.githubusercontent.com/argwingsmakuto/XAUUSD-bot/main/xauusd_clean.csv")

    # Apply indicators
    df['EMA50'] = overlap.ema(df['close'], length=50)
    df['EMA200'] = overlap.ema(df['close'], length=200)
    df['RSI'] = momentum.rsi(df['close'], length=14)
    macd = trend.macd(df['close'])
    df['MACD'], df['MACD_signal'], _ = macd
    df['ATR'] = trend.atr(df['high'], df['low'], df['close'])

    # Last row values
    last = df.iloc[-1]
    signal = ""

    # Signal Logic Example
    if last['EMA50'] > last['EMA200'] and last['MACD'] > last['MACD_signal'] and last['RSI'] > 55:
        signal = f"🔔 BUY Signal\nRSI: {round(last['RSI'], 2)}\nPrice: {last['close']}"
    elif last['EMA50'] < last['EMA200'] and last['MACD'] < last['MACD_signal'] and last['RSI'] < 45:
        signal = f"🔻 SELL Signal\nRSI: {round(last['RSI'], 2)}\nPrice: {last['close']}"

    if signal:
        send_telegram(signal)
        return f"✅ Sent: {signal}"
    else:
        return "⚠️ No strong signal right now."

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
