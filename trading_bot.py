import ccxt
import pandas as pd
import time
import requests
import os

# Render या सर्वर के Environment Variables से टोकन उठाएं
TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
SYMBOL = 'BTC/USDT'

exchange = ccxt.binance()

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def send_telegram_msg(message):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url)

print("Bot analysis shuru ho gaya hai...")

while True:
    try:
        bars = exchange.fetch_ohlcv(SYMBOL, timeframe='15m', limit=50)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        df['RSI'] = calculate_rsi(df)
        current_rsi = df['RSI'].iloc[-1]
        price = df['close'].iloc[-1]
        
        msg = f"BTC Price: {price:.2f} | RSI: {current_rsi:.2f}"
        
        if current_rsi < 30:
            msg += "\n🟢 Signal: RSI kam hai, BUY ka mauka!"
        elif current_rsi > 70:
            msg += "\n🔴 Signal: RSI zyada hai, SELL ka mauka!"
        else:
            msg += "\n⚪ Signal: Wait karo."
        
        send_telegram_msg(msg)
        print(msg)
        
    except Exception as e:
        print(f"Error: {e}")
        
    time.sleep(900) # 15 मिनट का इंतज़ार