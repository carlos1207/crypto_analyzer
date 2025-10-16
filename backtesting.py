"""
Historical backtesting for market cycle indicators
Analyzes indicator accuracy at predicting tops and bottoms
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from indicators import MarketCycleIndicators


class Backtester:
    """
    Backtest market cycle indicators against historical data
    """

    def __init__(self):
        self.indicators = MarketCycleIndicators()

    def find_price_peaks_and_troughs(self, df: pd.DataFrame, window: int = 30) -> Dict:
        """
        Identify actual price peaks (tops) and troughs (bottoms)

        Args:
            df: DataFrame with price data
            window: Days to look back/forward for peaks/troughs

        Returns:
            Dictionary with peaks and troughs data
        """
        prices = df['price']

        # Find local maxima (peaks/tops)
        peaks = []
        for i in range(window, len(prices) - window):
            if prices.iloc[i] == prices.iloc[i-window:i+window+1].max():
                peaks.append({
                    'date': prices.index[i],
                    'price': prices.iloc[i],
                    'type': 'peak'
                })

        # Find local minima (troughs/bottoms)
        troughs = []
        for i in range(window, len(prices) - window):
            if prices.iloc[i] == prices.iloc[i-window:i+window+1].min():
                troughs.append({
                    'date': prices.index[i],
                    'price': prices.iloc[i],
                    'type': 'trough'
                })

        return {
            'peaks': peaks,
            'troughs': troughs
        }

    def backtest_pi_cycle(self, df: pd.DataFrame) -> Dict:
        """
        Backtest Pi Cycle Top Indicator

        Returns:
            Dict with signals and accuracy metrics
        """
        ma_111 = df['price'].rolling(window=111).mean()
        ma_350_x2 = df['price'].rolling(window=350).mean() * 2

        # Find crossover points (when 111 MA crosses above 350 MA x2)
        signals = []
        for i in range(1, len(df)):
            if pd.notna(ma_111.iloc[i]) and pd.notna(ma_350_x2.iloc[i]):
                prev_below = ma_111.iloc[i-1] < ma_350_x2.iloc[i-1]
                curr_above = ma_111.iloc[i] >= ma_350_x2.iloc[i]

                if prev_below and curr_above:
                    # Signal triggered
                    signal_date = df.index[i]
                    signal_price = df['price'].iloc[i]

                    # Check price movement after signal (30, 60, 90 days)
                    future_returns = {}
                    for days in [30, 60, 90]:
                        future_idx = i + days
                        if future_idx < len(df):
                            future_price = df['price'].iloc[future_idx]
                            returns = ((future_price - signal_price) / signal_price) * 100
                            future_returns[f'{days}d'] = returns

                    signals.append({
                        'date': signal_date,
                        'price': signal_price,
                        'type': 'TOP',
                        'future_returns': future_returns
                    })

        # Calculate accuracy (how many times price dropped within 90 days)
        accurate_signals = sum(1 for s in signals if s['future_returns'].get('90d', 0) < 0)
        accuracy = (accurate_signals / len(signals) * 100) if signals else 0

        # Average return after signal
        avg_30d = np.mean([s['future_returns'].get('30d', 0) for s in signals]) if signals else 0
        avg_60d = np.mean([s['future_returns'].get('60d', 0) for s in signals]) if signals else 0
        avg_90d = np.mean([s['future_returns'].get('90d', 0) for s in signals]) if signals else 0

        return {
            'indicator': 'Pi Cycle Top',
            'signals': signals,
            'total_signals': len(signals),
            'accuracy': accuracy,
            'avg_return_30d': avg_30d,
            'avg_return_60d': avg_60d,
            'avg_return_90d': avg_90d,
            'interpretation': self._interpret_backtest_results('top', accuracy, avg_90d)
        }

    def backtest_mayer_multiple(self, df: pd.DataFrame) -> Dict:
        """
        Backtest Mayer Multiple indicator

        Returns:
            Dict with signals and accuracy metrics
        """
        ma_200 = df['price'].rolling(window=200).mean()
        mayer = df['price'] / ma_200

        # Find signals when Mayer > 2.4 (top) or < 0.8 (bottom)
        top_signals = []
        bottom_signals = []

        for i in range(1, len(df)):
            if pd.notna(mayer.iloc[i]):
                # Top signal
                if mayer.iloc[i-1] < 2.4 and mayer.iloc[i] >= 2.4:
                    signal_date = df.index[i]
                    signal_price = df['price'].iloc[i]

                    future_returns = self._calculate_future_returns(df, i, signal_price)

                    top_signals.append({
                        'date': signal_date,
                        'price': signal_price,
                        'mayer_value': mayer.iloc[i],
                        'type': 'TOP',
                        'future_returns': future_returns
                    })

                # Bottom signal
                if mayer.iloc[i-1] > 0.8 and mayer.iloc[i] <= 0.8:
                    signal_date = df.index[i]
                    signal_price = df['price'].iloc[i]

                    future_returns = self._calculate_future_returns(df, i, signal_price)

                    bottom_signals.append({
                        'date': signal_date,
                        'price': signal_price,
                        'mayer_value': mayer.iloc[i],
                        'type': 'BOTTOM',
                        'future_returns': future_returns
                    })

        # Calculate accuracy
        top_accuracy = self._calculate_accuracy(top_signals, 'top')
        bottom_accuracy = self._calculate_accuracy(bottom_signals, 'bottom')

        return {
            'indicator': 'Mayer Multiple',
            'top_signals': top_signals,
            'bottom_signals': bottom_signals,
            'top_accuracy': top_accuracy['accuracy'],
            'bottom_accuracy': bottom_accuracy['accuracy'],
            'avg_top_return_90d': top_accuracy['avg_90d'],
            'avg_bottom_return_90d': bottom_accuracy['avg_90d'],
            'interpretation': self._interpret_dual_backtest(top_accuracy, bottom_accuracy)
        }

    def backtest_rsi(self, df: pd.DataFrame) -> Dict:
        """
        Backtest RSI indicator

        Returns:
            Dict with signals and accuracy metrics
        """
        # Calculate RSI
        period = 14
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        # Find oversold (RSI < 30) and overbought (RSI > 70) signals
        oversold_signals = []
        overbought_signals = []

        for i in range(1, len(df)):
            if pd.notna(rsi.iloc[i]):
                # Oversold (bottom signal)
                if rsi.iloc[i-1] > 30 and rsi.iloc[i] <= 30:
                    signal_date = df.index[i]
                    signal_price = df['price'].iloc[i]
                    future_returns = self._calculate_future_returns(df, i, signal_price)

                    oversold_signals.append({
                        'date': signal_date,
                        'price': signal_price,
                        'rsi_value': rsi.iloc[i],
                        'type': 'OVERSOLD',
                        'future_returns': future_returns
                    })

                # Overbought (top signal)
                if rsi.iloc[i-1] < 70 and rsi.iloc[i] >= 70:
                    signal_date = df.index[i]
                    signal_price = df['price'].iloc[i]
                    future_returns = self._calculate_future_returns(df, i, signal_price)

                    overbought_signals.append({
                        'date': signal_date,
                        'price': signal_price,
                        'rsi_value': rsi.iloc[i],
                        'type': 'OVERBOUGHT',
                        'future_returns': future_returns
                    })

        oversold_accuracy = self._calculate_accuracy(oversold_signals, 'bottom')
        overbought_accuracy = self._calculate_accuracy(overbought_signals, 'top')

        return {
            'indicator': 'RSI',
            'oversold_signals': oversold_signals,
            'overbought_signals': overbought_signals,
            'oversold_accuracy': oversold_accuracy['accuracy'],
            'overbought_accuracy': overbought_accuracy['accuracy'],
            'avg_oversold_return_90d': oversold_accuracy['avg_90d'],
            'avg_overbought_return_90d': overbought_accuracy['avg_90d'],
            'interpretation': self._interpret_dual_backtest(overbought_accuracy, oversold_accuracy)
        }

    def _calculate_future_returns(self, df: pd.DataFrame, idx: int, signal_price: float) -> Dict:
        """Calculate returns 30, 60, 90 days after signal"""
        future_returns = {}
        for days in [30, 60, 90]:
            future_idx = idx + days
            if future_idx < len(df):
                future_price = df['price'].iloc[future_idx]
                returns = ((future_price - signal_price) / signal_price) * 100
                future_returns[f'{days}d'] = returns
        return future_returns

    def _calculate_accuracy(self, signals: List[Dict], signal_type: str) -> Dict:
        """Calculate accuracy and average returns for signals"""
        if not signals:
            return {'accuracy': 0, 'avg_30d': 0, 'avg_60d': 0, 'avg_90d': 0}

        # For top signals, accuracy = price went down
        # For bottom signals, accuracy = price went up
        if signal_type == 'top':
            accurate = sum(1 for s in signals if s['future_returns'].get('90d', 0) < 0)
        else:
            accurate = sum(1 for s in signals if s['future_returns'].get('90d', 0) > 0)

        accuracy = (accurate / len(signals) * 100) if signals else 0

        avg_30d = np.mean([s['future_returns'].get('30d', 0) for s in signals])
        avg_60d = np.mean([s['future_returns'].get('60d', 0) for s in signals])
        avg_90d = np.mean([s['future_returns'].get('90d', 0) for s in signals])

        return {
            'accuracy': accuracy,
            'avg_30d': avg_30d,
            'avg_60d': avg_60d,
            'avg_90d': avg_90d
        }

    def _interpret_backtest_results(self, signal_type: str, accuracy: float, avg_return: float) -> str:
        """Generate interpretation for backtest results"""
        if accuracy >= 75:
            reliability = "highly reliable"
        elif accuracy >= 60:
            reliability = "moderately reliable"
        elif accuracy >= 50:
            reliability = "somewhat reliable"
        else:
            reliability = "not reliable"

        return (
            f"This indicator is {reliability} ({accuracy:.1f}% accuracy). "
            f"On average, price moved {abs(avg_return):.1f}% {'down' if avg_return < 0 else 'up'} "
            f"within 90 days after signal."
        )

    def _interpret_dual_backtest(self, top_accuracy: Dict, bottom_accuracy: Dict) -> str:
        """Generate interpretation for indicators with both top and bottom signals"""
        top_acc = top_accuracy['accuracy']
        bottom_acc = bottom_accuracy['accuracy']
        top_ret = top_accuracy['avg_90d']
        bottom_ret = bottom_accuracy['avg_90d']

        interpretation = []

        # Top signals
        if top_acc >= 60:
            interpretation.append(f"Top signals are reliable ({top_acc:.1f}% accurate, avg {abs(top_ret):.1f}% decline).")
        else:
            interpretation.append(f"Top signals are less reliable ({top_acc:.1f}% accurate).")

        # Bottom signals
        if bottom_acc >= 60:
            interpretation.append(f"Bottom signals are reliable ({bottom_acc:.1f}% accurate, avg {abs(bottom_ret):.1f}% gain).")
        else:
            interpretation.append(f"Bottom signals are less reliable ({bottom_acc:.1f}% accurate).")

        return " ".join(interpretation)

    def run_full_backtest(self, df: pd.DataFrame) -> Dict:
        """
        Run backtest on all major indicators

        Args:
            df: DataFrame with historical price data

        Returns:
            Dictionary with backtest results for all indicators
        """
        results = {
            'pi_cycle': self.backtest_pi_cycle(df),
            'mayer_multiple': self.backtest_mayer_multiple(df),
            'rsi': self.backtest_rsi(df),
            'data_period': {
                'start': str(df.index[0]),
                'end': str(df.index[-1]),
                'days': len(df)
            }
        }

        return results


if __name__ == "__main__":
    # Test backtesting
    print("Backtesting module created successfully!")
    print("Use run_full_backtest() to analyze historical indicator performance.")
