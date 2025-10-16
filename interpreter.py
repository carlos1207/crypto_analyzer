"""
AI-powered interpretation generator for market indicators
Provides detailed, contextual explanations for each metric
"""


class IndicatorInterpreter:
    """Generates detailed interpretations for market indicators"""

    @staticmethod
    def interpret_pi_cycle(data: dict) -> str:
        """Generate detailed interpretation for Pi Cycle Indicator"""
        signal = data['signal']
        distance_pct = data.get('distance_pct', 0)

        base_explanation = (
            "The Pi Cycle Top Indicator compares the 111-day moving average with "
            "the 350-day moving average multiplied by 2. When the shorter 111-day MA "
            "crosses above the longer 350-day MA×2, it has historically signaled market tops "
            "with remarkable accuracy."
        )

        if signal == "TOP" or signal == "WARNING":
            return (
                f"{base_explanation}\n\n"
                f"⚠️ CURRENT STATUS: The 111-day MA is {'very close to' if signal == 'WARNING' else 'above'} "
                f"the 350-day MA×2 (distance: {abs(distance_pct):.1f}%).\n\n"
                f"WHAT THIS MEANS: Historically, this configuration has preceded major price peaks. "
                f"Past examples include the 2017 and 2021 Bitcoin tops. This doesn't guarantee an "
                f"immediate reversal, but suggests elevated risk.\n\n"
                f"SUGGESTED ACTION: Consider taking profits, tightening stop losses, or reducing position "
                f"size. This is NOT a signal to panic sell, but rather to be more defensive with "
                f"your allocations."
            )
        else:
            return (
                f"{base_explanation}\n\n"
                f"✅ CURRENT STATUS: The 111-day MA is below the 350-day MA×2 (distance: {abs(distance_pct):.1f}%).\n\n"
                f"WHAT THIS MEANS: The indicator is not currently signaling a market top. The market "
                f"may still have room to grow, though other indicators should be consulted.\n\n"
                f"SUGGESTED ACTION: Monitor this indicator as price rises. When the gap narrows to "
                f"less than 5%, begin considering risk management strategies."
            )

    @staticmethod
    def interpret_two_year_ma(data: dict) -> str:
        """Generate detailed interpretation for 2-Year MA Multiplier"""
        if data['signal'] == 'INSUFFICIENT_DATA':
            return data['interpretation']

        multiplier = data['multiplier']
        signal = data['signal']

        base_explanation = (
            "The 2-Year Moving Average Multiplier shows where price sits relative to the "
            "2-year (730-day) moving average. This long-term indicator smooths out short-term "
            "volatility and helps identify macro market cycles. A multiplier of 5× the 2-year MA "
            "has historically marked cycle tops."
        )

        if signal == "EXTREME_TOP":
            return (
                f"{base_explanation}\n\n"
                f"🔴 CURRENT STATUS: Price is {multiplier:.2f}× the 2-year MA - EXTREME OVERVALUATION!\n\n"
                f"WHAT THIS MEANS: Price is in the red zone above 5× the 2-year MA. Historically, "
                f"this has been an exceptional time to sell and lock in profits. Previous cycles "
                f"have seen 70-85% drawdowns from these levels.\n\n"
                f"SUGGESTED ACTION: Strongly consider taking significant profits. This is rare air "
                f"that doesn't last long. Set aside emotions and follow your predetermined exit strategy."
            )
        elif signal == "TOP":
            return (
                f"{base_explanation}\n\n"
                f"🟠 CURRENT STATUS: Price is {multiplier:.2f}× the 2-year MA - approaching danger zone.\n\n"
                f"WHAT THIS MEANS: Price is elevated and approaching historical top territory (5×). "
                f"Risk is increasing, though there may still be upside potential.\n\n"
                f"SUGGESTED ACTION: Begin taking profits systematically. Consider a staged exit "
                f"strategy (e.g., sell 20% now, 20% at 4×, 30% at 5×, keep 30% for moonshot)."
            )
        elif signal == "BOTTOM" or signal == "NEAR_BOTTOM":
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: Price is {multiplier:.2f}× the 2-year MA - {signal.replace('_', ' ')}.\n\n"
                f"WHAT THIS MEANS: Price is {'below' if multiplier < 1 else 'just above'} the 2-year MA. "
                f"Historically, this has been an excellent accumulation zone. The 2-year MA has acted "
                f"as strong support during bear markets.\n\n"
                f"SUGGESTED ACTION: High-conviction accumulation zone. Dollar-cost average or make "
                f"strategic buys. Historical data shows strong returns from this level over 12-24 month "
                f"timeframes."
            )
        else:
            return (
                f"{base_explanation}\n\n"
                f"🟡 CURRENT STATUS: Price is {multiplier:.2f}× the 2-year MA - normal range.\n\n"
                f"WHAT THIS MEANS: Price is in a typical range relative to the long-term average. "
                f"The market is neither extremely overheated nor oversold.\n\n"
                f"SUGGESTED ACTION: Continue monitoring. Consider your personal strategy - DCA if "
                f"accumulating, or hold if already positioned. Not an urgent signal either way."
            )

    @staticmethod
    def interpret_rsi(data: dict) -> str:
        """Generate detailed interpretation for RSI"""
        value = data['value']
        signal = data['signal']

        base_explanation = (
            f"The Relative Strength Index (RSI) measures momentum on a scale of 0-100. "
            f"Current RSI: {value:.1f}. "
            f"Traditional levels: below 30 = oversold, above 70 = overbought."
        )

        if signal == "EXTREME_OVERBOUGHT":
            return (
                f"{base_explanation}\n\n"
                f"🔴 CURRENT STATUS: RSI above 80 - EXTREME overbought conditions.\n\n"
                f"WHAT THIS MEANS: Buying pressure has reached extreme levels. While crypto can "
                f"stay overbought during parabolic rallies, this often precedes short-term pullbacks "
                f"or consolidation. In bull markets, RSI can remain elevated for weeks.\n\n"
                f"SUGGESTED ACTION: Avoid FOMO buying at these levels. If holding, consider taking "
                f"partial profits. If waiting to enter, be patient for a pullback to RSI 50-60 range. "
                f"Watch for bearish divergence (price making new highs while RSI makes lower highs)."
            )
        elif signal == "OVERBOUGHT":
            return (
                f"{base_explanation}\n\n"
                f"🟠 CURRENT STATUS: RSI 70-80 - overbought territory.\n\n"
                f"WHAT THIS MEANS: Momentum is strong but potentially overextended. In strong bull "
                f"markets, RSI can remain above 70 for extended periods, but pullbacks are common.\n\n"
                f"SUGGESTED ACTION: Not a sell signal alone, but caution is warranted. Avoid adding "
                f"aggressively at these levels. Good time to review your profit-taking strategy."
            )
        elif signal == "EXTREME_OVERSOLD":
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: RSI below 20 - EXTREME oversold conditions.\n\n"
                f"WHAT THIS MEANS: Selling pressure has reached extreme levels. While further downside "
                f"is possible, these levels often mark short-term bottoms and bounce opportunities. "
                f"Panic selling dominates at these extremes.\n\n"
                f"SUGGESTED ACTION: High-probability bounce zone for traders. For long-term investors, "
                f"this is typically an excellent accumulation opportunity. Consider staged entries as "
                f"RSI recovers back above 30. Watch for bullish divergence (price making new lows while "
                f"RSI makes higher lows)."
            )
        elif signal == "OVERSOLD":
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: RSI 20-30 - oversold territory.\n\n"
                f"WHAT THIS MEANS: Selling pressure is elevated and momentum is weak. While further "
                f"decline is possible, risk/reward is improving for buyers.\n\n"
                f"SUGGESTED ACTION: Start watching for entry opportunities. Wait for RSI to curl back "
                f"above 30 for confirmation of momentum shift. Good risk/reward for patient buyers."
            )
        else:
            return (
                f"{base_explanation}\n\n"
                f"🟡 CURRENT STATUS: RSI 30-70 - neutral momentum.\n\n"
                f"WHAT THIS MEANS: Momentum is balanced without extreme conditions. The market is "
                f"in a relatively healthy state without clear overbought or oversold signals.\n\n"
                f"SUGGESTED ACTION: No urgent action required based on RSI alone. Continue monitoring "
                f"and rely on other indicators for decision-making."
            )

    @staticmethod
    def interpret_rainbow(data: dict) -> str:
        """Generate detailed interpretation for Rainbow Chart"""
        if data['signal'] == 'INSUFFICIENT_DATA':
            return data['interpretation']

        position = data['position_ratio']
        signal = data['signal']

        base_explanation = (
            "The Rainbow Chart uses multiple moving averages to create colored bands that "
            "visualize market cycle position. Blue = accumulation, Green/Yellow = hold, "
            "Orange/Red = distribution. Position ratio: {:.2f}".format(position)
        )

        if signal == "EXTREME_TOP":
            return (
                f"{base_explanation}\n\n"
                f"🔴 CURRENT STATUS: Deep in the RED zone - bubble territory!\n\n"
                f"WHAT THIS MEANS: Price is far above all moving averages in the 'maximum bubble' "
                f"zone. This is historically where euphoria peaks and smart money exits. These "
                f"levels are unsustainable and don't last long.\n\n"
                f"SUGGESTED ACTION: Sell signal. Take profits aggressively. If you haven't already "
                f"taken gains, do it now. The red zone is for selling, not buying."
            )
        elif signal == "TOP":
            return (
                f"{base_explanation}\n\n"
                f"🟠 CURRENT STATUS: In the ORANGE zone - approaching euphoria.\n\n"
                f"WHAT THIS MEANS: Price is well above most moving averages. Market is hot but "
                f"not yet at extreme bubble levels. Risk is elevated.\n\n"
                f"SUGGESTED ACTION: Begin taking profits systematically. The orange zone is where "
                f"you should be de-risking, not adding exposure. Keep some for further upside, but "
                f"secure gains while you can."
            )
        elif signal == "EXTREME_BOTTOM":
            return (
                f"{base_explanation}\n\n"
                f"🔵 CURRENT STATUS: Deep in the BLUE zone - fire sale!\n\n"
                f"WHAT THIS MEANS: Price is well below the moving average spectrum in the 'maximum "
                f"discount' zone. This is historically where patient investors accumulate for "
                f"exceptional long-term returns.\n\n"
                f"SUGGESTED ACTION: Buy signal for long-term investors. Deep blue is the accumulation "
                f"zone. Fear is high, prices are low - classic contrarian opportunity. DCA heavily "
                f"at these levels."
            )
        elif signal == "BOTTOM":
            return (
                f"{base_explanation}\n\n"
                f"🔵 CURRENT STATUS: In the BLUE zone - accumulation territory.\n\n"
                f"WHAT THIS MEANS: Price is below most moving averages in the accumulation zone. "
                f"Market sentiment is typically poor, creating good buying opportunities.\n\n"
                f"SUGGESTED ACTION: Good zone for accumulation. Start building positions or increase "
                f"DCA amounts. Risk/reward is favorable for medium to long-term holds."
            )
        else:
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: GREEN/YELLOW zone - normal range.\n\n"
                f"WHAT THIS MEANS: Price is in a healthy middle range. Not undervalued enough to "
                f"be a screaming buy, not overvalued enough to be an urgent sell.\n\n"
                f"SUGGESTED ACTION: Hold mode. If you're accumulating, continue your DCA strategy. "
                f"If you're holding, stay patient. No extreme action required."
            )

    @staticmethod
    def interpret_mayer(data: dict) -> str:
        """Generate detailed interpretation for Mayer Multiple"""
        if data['signal'] == 'INSUFFICIENT_DATA':
            return data['interpretation']

        value = data['value']
        signal = data['signal']

        base_explanation = (
            f"The Mayer Multiple is the ratio of current price to the 200-day moving average. "
            f"Current value: {value:.2f}×. "
            f"Historical data shows values above 2.4 have marked major tops, while values below "
            f"0.8 have marked major bottoms."
        )

        if signal == "EXTREME_TOP":
            return (
                f"{base_explanation}\n\n"
                f"🔴 CURRENT STATUS: Mayer Multiple above 2.4 - EXTREME overvaluation!\n\n"
                f"WHAT THIS MEANS: Price is more than 2.4× the 200-day MA. Historically, this level "
                f"has preceded major corrections. The market is in euphoric territory.\n\n"
                f"SUGGESTED ACTION: Strong sell signal. Take profits. This level has marked tops "
                f"in previous cycles with high reliability. Don't get greedy at these extremes."
            )
        elif signal == "TOP":
            return (
                f"{base_explanation}\n\n"
                f"🟠 CURRENT STATUS: Mayer Multiple 1.8-2.4 - approaching danger zone.\n\n"
                f"WHAT THIS MEANS: Price is significantly above the 200-day MA and approaching "
                f"historically dangerous levels. Risk is increasing.\n\n"
                f"SUGGESTED ACTION: Begin profit-taking. Tighten stop losses. Be prepared for "
                f"increased volatility. Start moving toward more conservative positioning."
            )
        elif signal == "BOTTOM":
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: Mayer Multiple below 0.8 - historical bottom zone!\n\n"
                f"WHAT THIS MEANS: Price is more than 20% below the 200-day MA. This has historically "
                f"marked excellent long-term buying opportunities. Fear dominates at these levels.\n\n"
                f"SUGGESTED ACTION: Strong buy signal for long-term investors. These levels don't "
                f"last long and have historically provided exceptional risk/reward. Accumulate "
                f"aggressively with a 12+ month time horizon."
            )
        elif signal == "NEAR_BOTTOM":
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: Mayer Multiple 0.8-1.0 - below 200-day MA.\n\n"
                f"WHAT THIS MEANS: Price is below its 200-day MA, suggesting market weakness but "
                f"improving value. This is typically a good accumulation zone.\n\n"
                f"SUGGESTED ACTION: Good buying opportunity. DCA at these levels has historically "
                f"worked well. Risk/reward favors buyers with patience."
            )
        else:
            return (
                f"{base_explanation}\n\n"
                f"🟡 CURRENT STATUS: Mayer Multiple 1.0-1.8 - normal range.\n\n"
                f"WHAT THIS MEANS: Price is within a typical range relative to the 200-day MA. "
                f"Market is neither extremely over nor undervalued.\n\n"
                f"SUGGESTED ACTION: No extreme signal. Continue with your existing strategy. Monitor "
                f"for movement toward extreme zones (below 0.8 or above 2.4)."
            )

    @staticmethod
    def interpret_golden_ratio(data: dict) -> str:
        """Generate detailed interpretation for Golden Ratio Multiplier"""
        if data['signal'] == 'INSUFFICIENT_DATA':
            return data['interpretation']

        signal = data['signal']
        current_price = data['current_price']
        fib_levels = data.get('fib_levels', {})

        base_explanation = (
            "The Golden Ratio Multiplier uses Fibonacci ratios applied to the 350-day moving average "
            "to identify market cycle phases. These mathematically-derived levels have shown remarkable "
            "confluence with major market turning points."
        )

        if signal == "EXTREME_TOP":
            return (
                f"{base_explanation}\n\n"
                f"🔴 CURRENT STATUS: Beyond the 3.618 Fibonacci level - EXTREME bubble territory!\n\n"
                f"WHAT THIS MEANS: Price has exceeded even the highest Fibonacci projection. This is "
                f"'irrational exuberance' territory where fundamentals are ignored. These levels mark "
                f"the final parabolic phase before major corrections.\n\n"
                f"SUGGESTED ACTION: SELL. This is exceptionally rare air. History shows these levels "
                f"precede 70-90% drawdowns. Take profits now and ask questions later. Fear of missing "
                f"out is your enemy at this level."
            )
        elif signal == "TOP":
            return (
                f"{base_explanation}\n\n"
                f"🟠 CURRENT STATUS: Above 2.618 Fibonacci level - euphoria zone.\n\n"
                f"WHAT THIS MEANS: Price is in the euphoria band between 2.618 and 3.618. Market "
                f"sentiment is very bullish, but risk is high. Tops often form in this zone.\n\n"
                f"SUGGESTED ACTION: Take substantial profits. The 2.618-3.618 zone is where cycles "
                f"often peak. Keep some exposure for potential blow-off tops, but secure most gains."
            )
        elif signal == "BULLISH":
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: Above 1.618 Fibonacci level - bull market zone.\n\n"
                f"WHAT THIS MEANS: Price is in healthy bull market territory between 1.618 and 2.618. "
                f"This is where sustainable bull runs typically trade. Risk is moderate.\n\n"
                f"SUGGESTED ACTION: Hold and monitor. This is where bull markets spend most of their "
                f"time. Consider taking small profits to reduce cost basis, but maintain core position. "
                f"Start preparing profit-taking plan for 2.618+ levels."
            )
        elif signal == "EXTREME_BOTTOM":
            return (
                f"{base_explanation}\n\n"
                f"🔵 CURRENT STATUS: Below 0.5 Fibonacci level - DEEP bear territory!\n\n"
                f"WHAT THIS MEANS: Price is below half the 350-day MA. This represents extreme "
                f"bearishness and maximum pain. These levels have historically marked generational "
                f"buying opportunities.\n\n"
                f"SUGGESTED ACTION: BUY AGGRESSIVELY. This is where fortunes are made. Deploy "
                f"significant capital with a multi-year time horizon. Fear is maximum, opportunity "
                f"is maximum. These levels don't last long."
            )
        elif signal == "BOTTOM":
            return (
                f"{base_explanation}\n\n"
                f"🔵 CURRENT STATUS: Below or near the 350-day MA - accumulation zone.\n\n"
                f"WHAT THIS MEANS: Price is in bear market/accumulation territory. Market sentiment "
                f"is poor, but value is building. Patient accumulators are rewarded from these levels.\n\n"
                f"SUGGESTED ACTION: Accumulate. DCA at these levels. Risk/reward strongly favors "
                f"buyers with 6+ month time horizon. This is where wealth is built."
            )
        else:
            return (
                f"{base_explanation}\n\n"
                f"🟡 CURRENT STATUS: Near 350-day MA - neutral/transition zone.\n\n"
                f"WHAT THIS MEANS: Price is hovering around the long-term average. Market is in "
                f"transition between bear and bull phases.\n\n"
                f"SUGGESTED ACTION: Monitor closely. Wait for clear breakout above 1.618 (bullish) "
                f"or breakdown below 1.0 (bearish) before making major allocation changes."
            )

    @staticmethod
    def interpret_fear_greed(value: int, classification: str) -> str:
        """Generate detailed interpretation for Fear & Greed Index"""
        base_explanation = (
            f"The Crypto Fear & Greed Index combines multiple data sources (volatility, momentum, "
            f"social media, surveys, dominance, trends) into a single sentiment indicator. "
            f"Current value: {value}/100 ({classification})."
        )

        if value >= 75:
            return (
                f"{base_explanation}\n\n"
                f"🔴 CURRENT STATUS: EXTREME GREED - Market euphoria!\n\n"
                f"WHAT THIS MEANS: The market is in extreme greed territory. Participants are "
                f"overly optimistic, FOMO is prevalent, and risk-taking is high. Contrarian "
                f"indicator suggests caution.\n\n"
                f"SUGGESTED ACTION: Be fearful when others are greedy. Consider taking profits or "
                f"reducing exposure. Extreme greed often precedes corrections. This is when you "
                f"should be SELLING, not buying."
            )
        elif value >= 55:
            return (
                f"{base_explanation}\n\n"
                f"🟡 CURRENT STATUS: GREED - Positive sentiment, but not extreme.\n\n"
                f"WHAT THIS MEANS: Market sentiment is bullish. Optimism is present but not yet "
                f"at danger levels. Bull market psychology is developing.\n\n"
                f"SUGGESTED ACTION: Hold positions but monitor for further increases in greed. "
                f"Consider trimming if index approaches 75+. Don't chase aggressively at these levels."
            )
        elif value <= 25:
            return (
                f"{base_explanation}\n\n"
                f"🟢 CURRENT STATUS: EXTREME FEAR - Market panic!\n\n"
                f"WHAT THIS MEANS: The market is in extreme fear. Participants are overly pessimistic, "
                f"panic selling is common, and opportunities are emerging. Warren Buffett: 'Be greedy "
                f"when others are fearful.'\n\n"
                f"SUGGESTED ACTION: Excellent buying opportunity for long-term investors. Extreme "
                f"fear has historically marked excellent entry points. Deploy capital systematically. "
                f"This is when you should be BUYING, not selling."
            )
        elif value <= 45:
            return (
                f"{base_explanation}\n\n"
                f"🟡 CURRENT STATUS: FEAR - Negative sentiment, but not panic.\n\n"
                f"WHAT THIS MEANS: Market sentiment is bearish. Pessimism is present but not at "
                f"extreme levels. Good risk/reward is emerging.\n\n"
                f"SUGGESTED ACTION: Start accumulating. Fear levels (25-45) are typically good "
                f"buying zones. Consider increasing DCA amounts or making strategic purchases."
            )
        else:
            return (
                f"{base_explanation}\n\n"
                f"🟡 CURRENT STATUS: NEUTRAL - Balanced sentiment.\n\n"
                f"WHAT THIS MEANS: Market sentiment is relatively balanced between fear and greed. "
                f"No extreme emotions driving the market currently.\n\n"
                f"SUGGESTED ACTION: No strong signal from sentiment alone. Continue with your "
                f"existing strategy. Monitor for moves toward extremes (below 25 or above 75)."
            )

    @staticmethod
    def get_interpretation(indicator_name: str, data: dict) -> str:
        """
        Get detailed interpretation for any indicator

        Args:
            indicator_name: Name of the indicator
            data: Indicator data dictionary

        Returns:
            Detailed interpretation string
        """
        interpreters = {
            'pi_cycle': IndicatorInterpreter.interpret_pi_cycle,
            'two_year_ma': IndicatorInterpreter.interpret_two_year_ma,
            'rsi': IndicatorInterpreter.interpret_rsi,
            'rainbow': IndicatorInterpreter.interpret_rainbow,
            'mayer': IndicatorInterpreter.interpret_mayer,
            'golden_ratio': IndicatorInterpreter.interpret_golden_ratio
        }

        interpreter = interpreters.get(indicator_name)
        if interpreter:
            return interpreter(data)
        else:
            return data.get('interpretation', 'No interpretation available')
