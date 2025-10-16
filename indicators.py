"""
Technical indicators for identifying market tops and bottoms
"""

import pandas as pd
import numpy as np
from datetime import datetime


class MarketCycleIndicators:
    """Calculate various indicators for identifying market cycle phases"""

    @staticmethod
    def calculate_moving_average(data: pd.Series, period: int) -> pd.Series:
        """Calculate simple moving average"""
        return data.rolling(window=period).mean()

    @staticmethod
    def pi_cycle_indicator(df: pd.DataFrame) -> dict:
        """
        Pi Cycle Top Indicator
        Compares 111-day MA with 350-day MA x 2
        When they cross, it historically indicates a market top

        Returns:
            Dictionary with indicator data and signal
        """
        ma_111 = df['price'].rolling(window=111).mean()
        ma_350_x2 = df['price'].rolling(window=350).mean() * 2

        current_ma_111 = ma_111.iloc[-1]
        current_ma_350_x2 = ma_350_x2.iloc[-1]
        current_price = df['price'].iloc[-1]

        # Check if lines are crossing
        distance = current_ma_111 - current_ma_350_x2
        distance_pct = (distance / current_price) * 100

        # Determine signal
        if current_ma_111 > current_ma_350_x2:
            if distance_pct < 5:  # Within 5% - approaching top
                signal = "WARNING"
                interpretation = "APPROACHING TOP"
            else:
                signal = "TOP"
                interpretation = "POTENTIAL TOP SIGNAL"
        else:
            signal = "SAFE"
            interpretation = "NO TOP SIGNAL"

        return {
            'name': 'Pi Cycle Top Indicator',
            'ma_111': current_ma_111,
            'ma_350_x2': current_ma_350_x2,
            'current_price': current_price,
            'distance_pct': distance_pct,
            'signal': signal,
            'interpretation': interpretation,
            'historical_data': {
                'ma_111': ma_111,
                'ma_350_x2': ma_350_x2
            }
        }

    @staticmethod
    def two_year_ma_multiplier(df: pd.DataFrame) -> dict:
        """
        2-Year MA Multiplier
        Price vs 2-year MA and 2-year MA x 5
        Helps identify market cycle extremes

        Returns:
            Dictionary with indicator data
        """
        ma_730 = df['price'].rolling(window=730).mean()  # 2-year MA
        ma_730_x5 = ma_730 * 5

        current_price = df['price'].iloc[-1]
        current_ma = ma_730.iloc[-1] if not pd.isna(ma_730.iloc[-1]) else None
        current_ma_x5 = ma_730_x5.iloc[-1] if not pd.isna(ma_730_x5.iloc[-1]) else None

        if current_ma is None:
            return {
                'name': '2-Year MA Multiplier',
                'signal': 'INSUFFICIENT_DATA',
                'interpretation': 'Need at least 2 years of data'
            }

        # Calculate multiplier
        multiplier = current_price / current_ma

        # Determine signal
        if multiplier > 5:
            signal = "EXTREME_TOP"
            interpretation = "EXTREME OVERVALUATION - Historical top zone"
        elif multiplier > 3:
            signal = "TOP"
            interpretation = "APPROACHING TOP - Consider taking profits"
        elif multiplier < 1:
            signal = "BOTTOM"
            interpretation = "BELOW 2Y MA - Historical accumulation zone"
        elif multiplier < 1.2:
            signal = "NEAR_BOTTOM"
            interpretation = "NEAR BOTTOM - Good accumulation zone"
        else:
            signal = "NEUTRAL"
            interpretation = "NORMAL RANGE - Market in transition"

        return {
            'name': '2-Year MA Multiplier',
            'current_price': current_price,
            'ma_730': current_ma,
            'ma_730_x5': current_ma_x5,
            'multiplier': multiplier,
            'signal': signal,
            'interpretation': interpretation,
            'historical_data': {
                'ma_730': ma_730,
                'ma_730_x5': ma_730_x5
            }
        }

    @staticmethod
    def rsi(df: pd.DataFrame, period: int = 14) -> dict:
        """
        Relative Strength Index
        Measures momentum, overbought/oversold conditions

        Returns:
            Dictionary with RSI data
        """
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi_values = 100 - (100 / (1 + rs))

        current_rsi = rsi_values.iloc[-1]

        # Determine signal
        if current_rsi > 80:
            signal = "EXTREME_OVERBOUGHT"
            interpretation = "EXTREME OVERBOUGHT - Potential top forming"
        elif current_rsi > 70:
            signal = "OVERBOUGHT"
            interpretation = "OVERBOUGHT - Momentum may slow"
        elif current_rsi < 20:
            signal = "EXTREME_OVERSOLD"
            interpretation = "EXTREME OVERSOLD - Potential bottom forming"
        elif current_rsi < 30:
            signal = "OVERSOLD"
            interpretation = "OVERSOLD - Potential bounce opportunity"
        else:
            signal = "NEUTRAL"
            interpretation = "NEUTRAL - No extreme momentum"

        return {
            'name': f'RSI ({period})',
            'value': current_rsi,
            'signal': signal,
            'interpretation': interpretation,
            'historical_data': rsi_values
        }

    @staticmethod
    def rainbow_chart(df: pd.DataFrame) -> dict:
        """
        Rainbow Chart / Moving Average Bands
        Multiple MAs create color bands showing market cycle position

        Returns:
            Dictionary with band data
        """
        # Calculate multiple MAs (weekly increments)
        bands = {}
        periods = [7, 14, 21, 28, 35, 42, 56, 70, 90, 120, 150]

        for period in periods:
            bands[f'ma_{period}'] = df['price'].rolling(window=period).mean()

        current_price = df['price'].iloc[-1]

        # Determine position in rainbow
        ma_7 = bands['ma_7'].iloc[-1]
        ma_150 = bands['ma_150'].iloc[-1]

        if pd.isna(ma_150):
            return {
                'name': 'Rainbow Chart',
                'signal': 'INSUFFICIENT_DATA',
                'interpretation': 'Need more historical data'
            }

        # Calculate position (0 = bottom of rainbow, 1 = top)
        rainbow_range = ma_7 - ma_150
        price_position = current_price - ma_150
        position_ratio = price_position / rainbow_range if rainbow_range != 0 else 0.5

        # Determine signal
        if position_ratio > 1.5:
            signal = "EXTREME_TOP"
            interpretation = "DEEP ORANGE/RED - Bubble territory"
        elif position_ratio > 1:
            signal = "TOP"
            interpretation = "ORANGE - Approaching overbought"
        elif position_ratio < 0:
            signal = "EXTREME_BOTTOM"
            interpretation = "DEEP BLUE - Fire sale zone"
        elif position_ratio < 0.3:
            signal = "BOTTOM"
            interpretation = "BLUE - Accumulation zone"
        else:
            signal = "NEUTRAL"
            interpretation = "GREEN/YELLOW - Normal range"

        return {
            'name': 'Rainbow Chart',
            'current_price': current_price,
            'position_ratio': position_ratio,
            'signal': signal,
            'interpretation': interpretation,
            'bands': {k: v.iloc[-1] for k, v in bands.items() if not pd.isna(v.iloc[-1])},
            'historical_data': bands
        }

    @staticmethod
    def mayer_multiple(df: pd.DataFrame) -> dict:
        """
        Mayer Multiple
        Current Price / 200-day MA
        Values > 2.4 historically indicate tops

        Returns:
            Dictionary with Mayer Multiple data
        """
        ma_200 = df['price'].rolling(window=200).mean()
        current_price = df['price'].iloc[-1]
        current_ma_200 = ma_200.iloc[-1]

        if pd.isna(current_ma_200):
            return {
                'name': 'Mayer Multiple',
                'signal': 'INSUFFICIENT_DATA',
                'interpretation': 'Need at least 200 days of data'
            }

        mayer_multiple = current_price / current_ma_200

        # Determine signal
        if mayer_multiple > 2.4:
            signal = "EXTREME_TOP"
            interpretation = "EXTREME OVERVALUATION - Historical top zone"
        elif mayer_multiple > 1.8:
            signal = "TOP"
            interpretation = "OVERVALUED - Approaching danger zone"
        elif mayer_multiple < 0.8:
            signal = "BOTTOM"
            interpretation = "UNDERVALUED - Historical bottom zone"
        elif mayer_multiple < 1:
            signal = "NEAR_BOTTOM"
            interpretation = "BELOW 200 MA - Accumulation opportunity"
        else:
            signal = "NEUTRAL"
            interpretation = "NORMAL RANGE"

        return {
            'name': 'Mayer Multiple',
            'value': mayer_multiple,
            'current_price': current_price,
            'ma_200': current_ma_200,
            'signal': signal,
            'interpretation': interpretation,
            'historical_data': current_price / ma_200
        }

    @staticmethod
    def golden_ratio_multiplier(df: pd.DataFrame) -> dict:
        """
        Golden Ratio Multiplier
        Uses Fibonacci ratios (350 MA as base) to identify cycle extremes

        Returns:
            Dictionary with Golden Ratio data
        """
        ma_350 = df['price'].rolling(window=350).mean()
        current_price = df['price'].iloc[-1]
        current_ma = ma_350.iloc[-1]

        if pd.isna(current_ma):
            return {
                'name': 'Golden Ratio Multiplier',
                'signal': 'INSUFFICIENT_DATA',
                'interpretation': 'Need at least 350 days of data'
            }

        # Fibonacci multiples
        fib_levels = {
            'bottom': current_ma * 0.5,
            'accumulation': current_ma * 1,
            'bullish': current_ma * 1.618,
            'euphoria': current_ma * 2.618,
            'extreme': current_ma * 3.618
        }

        # Determine current level
        if current_price > fib_levels['extreme']:
            signal = "EXTREME_TOP"
            interpretation = "BEYOND EXTREME - Bubble territory"
        elif current_price > fib_levels['euphoria']:
            signal = "TOP"
            interpretation = "EUPHORIA ZONE - High risk"
        elif current_price > fib_levels['bullish']:
            signal = "BULLISH"
            interpretation = "BULL MARKET - Still room to grow"
        elif current_price < fib_levels['bottom']:
            signal = "EXTREME_BOTTOM"
            interpretation = "DEEP BEAR - Maximum opportunity"
        elif current_price < fib_levels['accumulation']:
            signal = "BOTTOM"
            interpretation = "ACCUMULATION ZONE"
        else:
            signal = "NEUTRAL"
            interpretation = "NORMAL RANGE"

        return {
            'name': 'Golden Ratio Multiplier',
            'current_price': current_price,
            'ma_350': current_ma,
            'fib_levels': fib_levels,
            'signal': signal,
            'interpretation': interpretation
        }

    @staticmethod
    def analyze_all(df: pd.DataFrame) -> dict:
        """
        Run all indicators and return comprehensive analysis

        Args:
            df: DataFrame with price data

        Returns:
            Dictionary with all indicator results
        """
        indicators = MarketCycleIndicators()

        results = {
            'pi_cycle': indicators.pi_cycle_indicator(df),
            'two_year_ma': indicators.two_year_ma_multiplier(df),
            'rsi': indicators.rsi(df),
            'rainbow': indicators.rainbow_chart(df),
            'mayer': indicators.mayer_multiple(df),
            'golden_ratio': indicators.golden_ratio_multiplier(df)
        }

        # Count signals for overall assessment
        signals = [r['signal'] for r in results.values()]
        top_signals = sum(1 for s in signals if 'TOP' in s)
        bottom_signals = sum(1 for s in signals if 'BOTTOM' in s)

        if top_signals >= 3:
            overall = "APPROACHING TOP - Multiple indicators showing overvaluation"
        elif bottom_signals >= 3:
            overall = "APPROACHING BOTTOM - Multiple indicators showing undervaluation"
        else:
            overall = "MIXED SIGNALS - Market in transition"

        results['overall_assessment'] = overall

        return results


if __name__ == "__main__":
    # Test with sample data
    import random
    from datetime import timedelta

    dates = pd.date_range(start='2022-01-01', end='2024-10-15', freq='D')
    # Simulate price data
    prices = [30000 * (1 + 0.001 * i + random.uniform(-0.02, 0.02)) for i in range(len(dates))]

    df = pd.DataFrame({
        'price': prices
    }, index=dates)

    indicators = MarketCycleIndicators()
    results = indicators.analyze_all(df)

    print("Indicator Results:")
    for name, data in results.items():
        if name != 'overall_assessment':
            print(f"\n{data['name']}: {data['signal']}")
            print(f"  {data['interpretation']}")
