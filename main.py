
# === main.py ===
from flask import Flask
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    return 'XAUUSD Signal Bot is running.'

@app.route('/signal')
def signal():
    # Simulated example of price data
    df = pd.DataFrame({
        'close': [3320, 3325, 3322, 3330, 3340, 3350]
    })
    
    # Calculate simple RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    last_rsi = rsi.iloc[-1]
    now = datetime.now(pytz.timezone("Africa/Nairobi")).strftime("%H:%M:%S")
    
    if last_rsi > 70:
        signal = "🔴 SELL - RSI Overbought"
    elif last_rsi < 30:
        signal = "🟢 BUY - RSI Oversold"
    else:
        signal = "⚠️ No strong signal (RSI = {:.2f})".format(last_rsi)

    return f"Time: {now} | RSI: {last_rsi:.2f} | Signal: {signal}"

if __name__ == '__main__':
    app.run(debug=True)

