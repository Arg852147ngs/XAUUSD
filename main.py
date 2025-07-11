from flask import Flask
import pandas as pd
import requests
import pandas_ta.overlap as ta_overlap
import pandas_ta.momentum as ta_momentum
import pandas_ta.trend as ta_trend

app = Flask(__name__)

TELEGRAM_TOKEN = "38172768175:AAGe_4nBGJthZYdN3UQr3VL97x8-5I5bNng"
CHAT_ID = "1644693247"

@app.route('/')
def home():
    return "✅ Bot is live."

@app.route('/check_signal')
def check_signal():
    # Load price data
    url = "https://raw.githubusercontent.com/argwingsmakuto/XAUUSD-bot/main/xauusd_clean.csv"
    df = pd.read_csv(url)

    # Indicators
    df['EMA50'] = ta_overlap.ema(df['close'], length=50)
    df['EMA200'] = ta_overlap.ema(df['close'], length=200)
    df['RSI'] = ta_momentum.rsi(df['close'], length=14)
    macd_df = ta_trend.macd(df['close'])
    df['MACD'] = macd_df['MACD_12_26_9']
    df['MACD_signal'] = macd_df['MACDs_12_26_9']
    df['ATR'] = ta_trend.atr(df['high'], df['low'], df['close'])

    # Signal Logic
    last = df.iloc[-1]
    signal = ""

    if last['EMA50'] > last['EMA200'] and last['MACD'] > last['MACD_signal'] and last['RSI'] > 55:
        signal = f"📈 BUY Signal\nRSI: {round(last['RSI'],2)}\nPrice: {last['close']}"
    elif last['EMA50'] < last['EMA200'] and last['MACD'] < last['MACD_signal'] and last['RSI'] < 45:
        signal = f"📉 SELL Signal\nRSI: {round(last['RSI'],2)}\nPrice: {last['close']}"

    if signal:
        send_telegram(signal)
        return f"✅ Sent: {signal}"
    else:
        return "⚠️ No valid signal found."

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
