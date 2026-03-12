import ccxt
import pandas as pd
import time
import requests
# टेलीग्राम टोकन और आईडी को सुरक्षित तरीके से यहाँ से उठाएं
# सेटिंग्स
TELEGRAM_TOKEN = '8799540972:AAHyxXfLq8CNti1Th83XX8X-l6mbcoEvrYo'
CHAT_ID = '8781065824'
SYMBOL = 'BTC/USDT'
exchange = ccxt.binance()

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.get(url, params={'chat_id': CHAT_ID, 'text': message})

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

print("Bot analysis shuru ho gaya hai...")

# लूप को यहाँ से शुरू करें
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