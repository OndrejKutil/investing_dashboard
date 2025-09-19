import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY: str = os.getenv('FAGI_API_KEY')

API_URL: str = 'https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical'

def fetch_fear_and_greed_crypto_index(offset: int = 1, limit: int = 100) -> pd.DataFrame:
    headers: dict = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    
    params = {
        'start': str(offset),
        'limit': str(limit)
        }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['data'])

        # Convert timestamp to readable datetime format
        # First convert to numeric to avoid FutureWarning
        df['timestamp'] = pd.to_numeric(df['timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.date
        df.rename(columns={'value': 'fear_greed_index', 'timestamp': 'date'}, inplace=True)


        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
