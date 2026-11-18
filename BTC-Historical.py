'''
import pandas as pd
import yfinance as yf

# Download historical data for BTC-USD
btc_data = yf.download('BTC-USD', start='2017-06-30', end='2024-10-17', interval='1H')

# Check if data was downloaded successfully
if btc_data.empty:
    print("No data found for the given date range.")
else:
    # Reset index to create a 'Date' column from the existing index
    btc_data.reset_index(inplace=True)

    # Display the DataFrame structure to understand available columns
    print(btc_data.head())  # Vypíšeme první řádky, abychom viděli strukturu DataFrame

    # Rename 'Datetime' to 'Date'
    btc_data.rename(columns={'Datetime': 'Date'}, inplace=True)

    # Localize the datetime column to remove timezone information (assuming it's present)
    btc_data['Date'] = btc_data['Date'].dt.tz_localize(None)

    # Select only the 'Date' and 'Close' columns for saving
    selected_data = btc_data[['Date', 'Open']]  # Use 'Close' for Price

    # Save to Excel
    selected_data.to_excel('BTC_Historical_Prices_New_Hourlyyy.xlsx', index=False)
    print("BTC Historical Prices saved to BTC_Historical_Prices_New_Hourly.xlsx")
'''

import requests
import pandas as pd
from datetime import datetime

def fetch_binance_klines(symbol="BTCUSDT", interval="1h", start_date="2018-01-03", end_date="2018-01-05"):
    url = "https://api.binance.com/api/v3/klines"
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
    klines = []
    
    while True:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_timestamp,
            "endTime": end_timestamp,
            "limit": 1000  # Maximum limit per request
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data:
            break
        
        klines.extend(data)
        start_timestamp = data[-1][6] + 1  # Move to the next timestamp
        
        if start_timestamp >= end_timestamp:
            break

    # Create DataFrame
    df = pd.DataFrame(klines, columns=[
        "Open time", "Open", "High", "Low", "Close", "Volume", 
        "Close time", "Quote asset volume", "Number of trades", 
        "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
    ])

    # Convert timestamps to readable dates
    df["Open time"] = pd.to_datetime(df["Open time"], unit='ms')
    
    # Select relevant columns and rename for export
    df = df[["Open time", "Open"]].rename(columns={"Open time": "Date", "Open": "Open Price"})
    df["Open Price"] = df["Open Price"].astype(float)

    return df

# Fetch BTC/USD data
df = fetch_binance_klines("BTCUSDT", "1h", "2018-01-03", "2018-01-05")

# Export to Excel
df.to_excel("BTC_USDT_1h-missing.xlsx", index=False)

print("Data successfully exported to BTC_USDT_1h-missing.xlsx")

'''
import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange
from datetime import datetime

# === Configuration ===
API_KEY = "JSBQLG7NR2JSLFIQ"
symbol = "EURUSD"  # EUR/USD
timeframe = "60min"  # 1-hour timeframe
output_excel = "EURUSD_Forex_1H_data.xlsx"

# === Fetch Data from Alpha Vantage ===
fx = ForeignExchange(key=API_KEY, output_format='pandas')
data, meta_data = fx.get_currency_exchange_intraday(
    from_symbol="EUR", to_symbol="USD", interval=timeframe
)

# === Process Data ===
data['Date'] = pd.to_datetime(data.index)
data['Open Price'] = data['1. open']
df = data[['Date', 'Open Price']]

# === Save to Excel ===
df.to_excel(output_excel, index=False)
print(f"Saved {len(df)} rows to {output_excel}")
'''



