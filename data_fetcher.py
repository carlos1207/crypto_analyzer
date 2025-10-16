"""
Data fetching module for cryptocurrency price data
Uses yfinance (free, no API key required)
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
from config import SUPPORTED_COINS, DEFAULT_DAYS


class CryptoDataFetcher:
    """Fetches cryptocurrency price data using yfinance"""

    def __init__(self):
        self.ticker_map = {
            'BTC': 'BTC-USD',
            'ETH': 'ETH-USD',
            'SOL': 'SOL-USD'
        }

    def get_historical_data(self, symbol: str, days: int = DEFAULT_DAYS) -> pd.DataFrame:
        """
        Fetch historical price data for a cryptocurrency

        Args:
            symbol: Crypto symbol (BTC, ETH, SOL)
            days: Number of days of historical data

        Returns:
            DataFrame with columns: price, market_cap, volume
        """
        if symbol not in SUPPORTED_COINS:
            raise ValueError(f"Unsupported coin: {symbol}. Supported: {list(SUPPORTED_COINS.keys())}")

        ticker = self.ticker_map[symbol]

        try:
            # Calculate start date
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Fetch data from yfinance
            crypto = yf.Ticker(ticker)
            hist = crypto.history(start=start_date, end=end_date)

            if hist.empty:
                raise Exception(f"No data returned for {symbol}")

            # Rename columns to match expected format
            df = pd.DataFrame({
                'price': hist['Close'],
                'volume': hist['Volume'],
                'market_cap': hist['Close'] * hist['Volume']  # Approximation
            })

            return df

        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")

    def get_current_price(self, symbol: str) -> dict:
        """
        Get current price and market data

        Args:
            symbol: Crypto symbol (BTC, ETH, SOL)

        Returns:
            Dictionary with current price, market cap, volume, etc.
        """
        if symbol not in SUPPORTED_COINS:
            raise ValueError(f"Unsupported coin: {symbol}")

        ticker = self.ticker_map[symbol]

        try:
            crypto = yf.Ticker(ticker)

            # Get current info
            info = crypto.info

            # Get recent history for price changes
            hist = crypto.history(period='1mo')

            if hist.empty:
                raise Exception(f"No data available for {symbol}")

            current_price = hist['Close'].iloc[-1]

            # Calculate price changes
            price_24h_ago = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            price_7d_ago = hist['Close'].iloc[-7] if len(hist) > 7 else current_price
            price_30d_ago = hist['Close'].iloc[0] if len(hist) > 0 else current_price

            price_change_24h = ((current_price - price_24h_ago) / price_24h_ago) * 100
            price_change_7d = ((current_price - price_7d_ago) / price_7d_ago) * 100
            price_change_30d = ((current_price - price_30d_ago) / price_30d_ago) * 100

            # Get market cap if available
            market_cap = info.get('marketCap', 0)
            if market_cap == 0:
                # Fallback: approximate using volume
                market_cap = current_price * hist['Volume'].iloc[-1]

            return {
                'symbol': symbol,
                'name': SUPPORTED_COINS[symbol].capitalize(),
                'current_price': float(current_price),
                'market_cap': float(market_cap),
                'volume_24h': float(hist['Volume'].iloc[-1]),
                'price_change_24h': float(price_change_24h),
                'price_change_7d': float(price_change_7d),
                'price_change_30d': float(price_change_30d),
                'ath': float(hist['High'].max()),
                'ath_date': str(hist['High'].idxmax()),
                'atl': float(hist['Low'].min()),
                'atl_date': str(hist['Low'].idxmin())
            }

        except Exception as e:
            raise Exception(f"Error fetching current data for {symbol}: {str(e)}")

    def get_fear_greed_index(self) -> dict:
        """
        Fetch the Crypto Fear & Greed Index

        Returns:
            Dictionary with fear & greed data
        """
        url = "https://api.alternative.me/fng/"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            latest = data['data'][0]

            return {
                'value': int(latest['value']),
                'classification': latest['value_classification'],
                'timestamp': datetime.fromtimestamp(int(latest['timestamp']))
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching Fear & Greed Index: {str(e)}")


if __name__ == "__main__":
    # Test the data fetcher
    fetcher = CryptoDataFetcher()

    print("Fetching BTC data...")
    btc_data = fetcher.get_historical_data('BTC', days=365)
    print(f"Retrieved {len(btc_data)} days of BTC data")
    print(btc_data.head())

    print("\nFetching current BTC price...")
    current = fetcher.get_current_price('BTC')
    print(f"Current BTC price: ${current['current_price']:,.2f}")

    print("\nFetching Fear & Greed Index...")
    fg = fetcher.get_fear_greed_index()
    print(f"Fear & Greed: {fg['value']} ({fg['classification']})")
