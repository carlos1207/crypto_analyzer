# Crypto Market Analyzer

Advanced cryptocurrency market cycle analysis tool with multiple technical indicators designed to help identify market tops and bottoms.

## Features

### Indicators Implemented

1. **Pi Cycle Top Indicator** - Compares 111-day MA with 350-day MA × 2 to identify market tops
2. **2-Year MA Multiplier** - Shows position relative to 2-year moving average (5× historically marks tops)
3. **RSI (Relative Strength Index)** - Momentum indicator showing overbought/oversold conditions
4. **Rainbow Chart** - Multiple MA bands creating a visual spectrum of market cycle position
5. **Mayer Multiple** - Price / 200-day MA ratio (values > 2.4 indicate tops)
6. **Golden Ratio Multiplier** - Fibonacci ratios applied to 350-day MA
7. **Fear & Greed Index** - Market sentiment indicator combining multiple data sources

### Supported Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)

*More coins can be easily added by updating `config.py`*

### AI-Generated Interpretations

Each indicator comes with detailed, context-aware interpretations that explain:
- What the indicator means
- Current market status
- Historical context
- Suggested actions based on the signal

## Installation

### 1. Install Dependencies

```bash
cd crypto_analyzer
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python cli.py --help
```

## Usage

### Command-Line Interface (CLI)

#### Analyze a Single Cryptocurrency

```bash
# Basic analysis
python cli.py analyze BTC

# Detailed analysis with full interpretations
python cli.py analyze BTC --detailed

# Analyze with custom data range
python cli.py analyze ETH --detailed --days 365
```

#### Check Fear & Greed Index

```bash
# Quick view
python cli.py feargreed

# Detailed interpretation
python cli.py feargreed --detailed
```

#### Compare Multiple Coins

```bash
python cli.py compare
```

#### List Supported Coins

```bash
python cli.py list-coins
```

### Web Dashboard

#### Start the Web Server

```bash
python web_app.py
```

Then open your browser to: **http://localhost:5000**

#### Features:
- Interactive charts powered by Plotly
- Real-time data fetching
- Side-by-side comparison of BTC, ETH, SOL
- Beautiful dark-themed UI
- Detailed indicator interpretations
- Fear & Greed gauge

## How to Interpret the Signals

### Top Signals (RED)
- **EXTREME_TOP** - Strong sell signal, historically marks major tops
- **TOP** - Approaching dangerous territory, consider taking profits
- **WARNING** - Caution warranted, monitor closely

### Bottom Signals (GREEN)
- **EXTREME_BOTTOM** - Strong buy signal, historically marks major bottoms
- **BOTTOM** - Good accumulation zone
- **NEAR_BOTTOM** - Risk/reward favoring buyers

### Neutral Signals (BLUE/YELLOW)
- **NEUTRAL** - No extreme conditions
- **BULLISH** - Healthy bull market territory
- **SAFE** - No immediate concerns

## Example Workflows

### For Long-Term Investors

1. Run comparison: `python cli.py compare`
2. Look for coins with multiple "BOTTOM" signals
3. Check Fear & Greed: `python cli.py feargreed --detailed`
4. If Fear & Greed < 25 and multiple indicators show BOTTOM → Accumulate
5. Set alerts for when indicators flip to TOP signals

### For Traders

1. Analyze your target: `python cli.py analyze BTC --detailed`
2. Check RSI for overbought/oversold conditions
3. Use Pi Cycle and Mayer Multiple for macro context
4. Open web dashboard for visual confirmation
5. Plan entries/exits based on signal confluence

### For Market Monitoring

1. Start web dashboard: `python web_app.py`
2. Keep it open in a browser tab
3. Refresh periodically (or add auto-refresh)
4. Watch for signal changes
5. Use comparison view to spot divergences between coins

## Understanding Each Indicator

### Pi Cycle Top Indicator
- **Best for:** Identifying Bitcoin tops
- **Signal:** When 111-day MA crosses above 350-day MA × 2
- **Historical accuracy:** Very high for BTC cycle tops (2013, 2017, 2021)

### 2-Year MA Multiplier
- **Best for:** Long-term cycle position
- **Key levels:**
  - Below 1.0 = accumulation zone
  - Above 5.0 = distribution zone
- **Use case:** Macro perspective, ignore short-term noise

### RSI
- **Best for:** Short to medium-term momentum
- **Key levels:**
  - < 30 = oversold
  - > 70 = overbought
- **Note:** Can stay extreme during strong trends

### Rainbow Chart
- **Best for:** Visual representation of market cycle
- **Colors:** Blue (buy) → Green (hold) → Yellow (caution) → Orange/Red (sell)
- **Use case:** Simple, intuitive assessment

### Mayer Multiple
- **Best for:** Bitcoin valuation
- **Key levels:**
  - < 0.8 = undervalued
  - > 2.4 = overvalued
- **Historical average:** ~1.4

### Golden Ratio Multiplier
- **Best for:** Mathematical precision seekers
- **Based on:** Fibonacci ratios (1.618, 2.618, 3.618)
- **Use case:** Confluence with other indicators

### Fear & Greed Index
- **Best for:** Sentiment analysis
- **Contrarian indicator:**
  - Extreme Fear (< 25) = buy opportunity
  - Extreme Greed (> 75) = sell opportunity
- **Updated:** Daily

## API Endpoints (Web Dashboard)

- `GET /api/analyze/<symbol>` - Full analysis for a coin
- `GET /api/feargreed` - Fear & Greed Index
- `GET /api/compare` - Compare all supported coins

## Customization

### Add More Cryptocurrencies

Edit `config.py`:

```python
SUPPORTED_COINS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'ADA': 'cardano',  # Add new coin
    'DOT': 'polkadot'  # Add another
}
```

### Adjust Indicator Parameters

Each indicator in `indicators.py` can be customized with different periods or thresholds.

### Customize Interpretations

Edit `interpreter.py` to modify the AI-generated interpretations to match your strategy.

## Data Sources

- **Price Data:** Yahoo Finance via yfinance (free, no API key required)
- **Fear & Greed:** Alternative.me API
- **Update Frequency:** Real-time on demand

## Tips for Power Users

1. **Combine Signals:** Don't rely on a single indicator. Look for confluence of 3+ signals.

2. **Context Matters:** A "TOP" signal in a bear market bounce is different from one in a 2-year bull run.

3. **Time Frames:** Use 2-Year MA and Golden Ratio for macro, RSI for micro.

4. **Backtesting:** Check historical data to see how indicators performed in past cycles.

5. **Dollar-Cost Average:** Even with perfect indicators, timing is hard. DCA reduces risk.

6. **Risk Management:** No indicator is 100% accurate. Always use stop losses and position sizing.

## Troubleshooting

### "Error fetching data"
- Check your internet connection
- CoinGecko API might be rate-limited (wait a few minutes)
- Verify the coin symbol is correct

### "Insufficient data"
- Some indicators need 2+ years of data
- Newer coins may not have enough history
- Try reducing `--days` parameter

### Charts not displaying
- Ensure Flask is running: `python web_app.py`
- Check browser console for JavaScript errors
- Try clearing browser cache

## Future Enhancements (Ideas for You)

- [ ] Add email/SMS alerts when signals trigger
- [ ] Integrate on-chain metrics (Glassnode API)
- [ ] Add more coins (top 20 by market cap)
- [ ] Historical backtesting module
- [ ] Export data to CSV/Excel
- [ ] Mobile-responsive dashboard improvements
- [ ] Real-time websocket updates
- [ ] Portfolio tracking integration

## Disclaimer

**This tool is for educational and informational purposes only. It is NOT financial advice.**

- Cryptocurrency investing is highly risky
- Past performance does not guarantee future results
- Always do your own research (DYOR)
- Never invest more than you can afford to lose
- Consult a licensed financial advisor before making investment decisions

## License

MIT License - Feel free to modify and use for your own purposes.

## Contributing

Found a bug? Have an idea? This is your personal tool - modify it however you like!

---

**Built with:** Python, Flask, Plotly, Rich, CoinGecko API

**Happy Analyzing! 🚀📊**
