"""
Configuration for Crypto Analyzer
"""

# Supported cryptocurrencies
SUPPORTED_COINS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana'
}

# CoinGecko API configuration
COINGECKO_API_BASE = 'https://api.coingecko.com/api/v3'

# Historical data parameters
DEFAULT_DAYS = 730  # 2 years of data for comprehensive analysis

# Indicator thresholds
THRESHOLDS = {
    'rsi': {
        'oversold': 30,
        'overbought': 70
    },
    'fear_greed': {
        'extreme_fear': 25,
        'extreme_greed': 75
    }
}

# Color scheme for terminal output
COLORS = {
    'bullish': 'green',
    'bearish': 'red',
    'neutral': 'yellow',
    'info': 'blue'
}
