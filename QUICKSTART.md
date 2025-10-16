# Quick Start Guide

Get up and running with Crypto Market Analyzer in 2 minutes!

## Installation

```bash
cd crypto_analyzer
pip install -r requirements.txt
```

Done! You're ready to go.

## Usage

### Option 1: Interactive Menu (Easiest)

```bash
./run_cli.sh
```

Pick from the menu and go!

### Option 2: Web Dashboard (Most Visual)

```bash
./run_dashboard.sh
```

Then open: **http://localhost:5000**

### Option 3: Direct Commands (Most Flexible)

```bash
# Analyze Bitcoin with detailed interpretations
python cli.py analyze BTC --detailed

# Quick ETH check
python cli.py analyze ETH

# Compare all three coins
python cli.py compare

# Check Fear & Greed
python cli.py feargreed --detailed
```

## What to Look For

### 🟢 BUY SIGNALS
- Multiple indicators showing "BOTTOM" or "EXTREME_BOTTOM"
- Fear & Greed Index < 25 (Extreme Fear)
- RSI < 30 (Oversold)
- Mayer Multiple < 0.8
- 2-Year MA Multiplier < 1.0

### 🔴 SELL SIGNALS
- Multiple indicators showing "TOP" or "EXTREME_TOP"
- Fear & Greed Index > 75 (Extreme Greed)
- RSI > 70 (Overbought)
- Mayer Multiple > 2.4
- Pi Cycle indicator crosses

### 🟡 HOLD/MONITOR
- Mixed signals
- Neutral indicators (30 < RSI < 70)
- Fear & Greed in 25-75 range

## Example Workflow

### Daily Check (30 seconds)
```bash
python cli.py compare
```
Quick glance at all three coins and their signals.

### Weekly Deep Dive (5 minutes)
```bash
python cli.py analyze BTC --detailed
python cli.py feargreed --detailed
./run_dashboard.sh  # Visual confirmation
```

### Before Making a Trade
1. Run detailed analysis on your target coin
2. Check for signal confluence (3+ indicators agreeing)
3. Review Fear & Greed for sentiment
4. Check comparison to see if other coins show similar signals
5. Make decision based on YOUR strategy and risk tolerance

## Tips

1. **Don't rely on a single indicator** - Look for confluence
2. **Context matters** - A "top" signal at $30k is different than at $100k
3. **Use with other analysis** - These are tools, not crystal balls
4. **Set up a routine** - Check daily/weekly consistently
5. **Take notes** - Track what signals preceded major moves

## Troubleshooting

**"Command not found"**
```bash
python3 cli.py analyze BTC  # Try python3 instead
```

**"Module not found"**
```bash
pip install -r requirements.txt  # Reinstall dependencies
```

**"API Error" or "Rate Limited"**
- Wait 5 minutes and try again
- CoinGecko API has rate limits on free tier

## Next Steps

Read the full [README.md](README.md) for:
- Detailed indicator explanations
- Advanced customization
- API documentation
- Adding more coins

---

**Happy analyzing!** 📊🚀

Remember: This is a tool to inform decisions, not make them for you. Always DYOR!
