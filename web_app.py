"""
Crypto Analyzer Web Dashboard
Flask app with interactive visualizations
"""

from flask import Flask, render_template, jsonify, request
import plotly.graph_objs as go
import plotly.utils
import json
from datetime import datetime

from data_fetcher import CryptoDataFetcher
from indicators import MarketCycleIndicators
from interpreter import IndicatorInterpreter
from config import SUPPORTED_COINS

app = Flask(__name__)


def create_price_chart(df, symbol):
    """Create price chart with moving averages"""
    fig = go.Figure()

    # Add price line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['price'],
        mode='lines',
        name='Price',
        line=dict(color='#3b82f6', width=2)
    ))

    # Add moving averages
    ma_111 = df['price'].rolling(window=111).mean()
    ma_350 = df['price'].rolling(window=350).mean()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=ma_111,
        mode='lines',
        name='111-day MA',
        line=dict(color='#f59e0b', width=1, dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=ma_350,
        mode='lines',
        name='350-day MA',
        line=dict(color='#8b5cf6', width=1, dash='dash')
    ))

    fig.update_layout(
        title=f'{symbol} Price History',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        template='plotly_dark',
        height=500
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_pi_cycle_chart(df, indicator_data):
    """Create Pi Cycle indicator chart"""
    fig = go.Figure()

    ma_111 = indicator_data['historical_data']['ma_111']
    ma_350_x2 = indicator_data['historical_data']['ma_350_x2']

    # Add price
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['price'],
        mode='lines',
        name='Price',
        line=dict(color='#3b82f6', width=2)
    ))

    # Add 111-day MA
    fig.add_trace(go.Scatter(
        x=ma_111.index,
        y=ma_111,
        mode='lines',
        name='111-day MA',
        line=dict(color='#10b981', width=2)
    ))

    # Add 350-day MA x 2
    fig.add_trace(go.Scatter(
        x=ma_350_x2.index,
        y=ma_350_x2,
        mode='lines',
        name='350-day MA × 2',
        line=dict(color='#ef4444', width=2)
    ))

    fig.update_layout(
        title='Pi Cycle Top Indicator',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        template='plotly_dark',
        height=400
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_rainbow_chart(df, rainbow_data):
    """Create Rainbow chart with MA bands"""
    fig = go.Figure()

    bands = rainbow_data['historical_data']
    colors = ['#1e3a8a', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd',
              '#fde047', '#facc15', '#f59e0b', '#f97316', '#dc2626']

    # Add bands in reverse order so they stack properly
    periods = [150, 120, 90, 70, 56, 42, 35, 28, 21, 14, 7]

    for i, period in enumerate(periods):
        key = f'ma_{period}'
        if key in bands:
            fig.add_trace(go.Scatter(
                x=bands[key].index,
                y=bands[key],
                mode='lines',
                name=f'{period}-day MA',
                line=dict(color=colors[i % len(colors)], width=1),
                fill='tonexty' if i > 0 else None,
                fillcolor=colors[i % len(colors)],
                opacity=0.3
            ))

    # Add price on top
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['price'],
        mode='lines',
        name='Price',
        line=dict(color='white', width=3)
    ))

    fig.update_layout(
        title='Rainbow Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        template='plotly_dark',
        height=500,
        showlegend=True
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_rsi_chart(rsi_data):
    """Create RSI chart"""
    fig = go.Figure()

    rsi_values = rsi_data['historical_data']

    # Add RSI line
    fig.add_trace(go.Scatter(
        x=rsi_values.index,
        y=rsi_values,
        mode='lines',
        name='RSI',
        line=dict(color='#3b82f6', width=2)
    ))

    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")

    # Add extreme lines
    fig.add_hline(y=80, line_dash="dot", line_color="darkred", annotation_text="Extreme OB (80)")
    fig.add_hline(y=20, line_dash="dot", line_color="darkgreen", annotation_text="Extreme OS (20)")

    # Add colored background zones
    fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, line_width=0)
    fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, line_width=0)

    fig.update_layout(
        title='RSI (Relative Strength Index)',
        xaxis_title='Date',
        yaxis_title='RSI',
        hovermode='x unified',
        template='plotly_dark',
        height=300,
        yaxis=dict(range=[0, 100])
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_fear_greed_gauge(fg_data):
    """Create Fear & Greed gauge chart"""
    value = fg_data['value']

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Fear & Greed Index", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': '#10b981'},
                {'range': [25, 45], 'color': '#84cc16'},
                {'range': [45, 55], 'color': '#eab308'},
                {'range': [55, 75], 'color': '#f97316'},
                {'range': [75, 100], 'color': '#ef4444'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        template='plotly_dark',
        height=400,
        font={'color': "white", 'family': "Arial"}
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', coins=list(SUPPORTED_COINS.keys()))


@app.route('/api/analyze/<symbol>')
def api_analyze(symbol):
    """API endpoint for cryptocurrency analysis"""
    symbol = symbol.upper()

    if symbol not in SUPPORTED_COINS:
        return jsonify({'error': 'Unsupported cryptocurrency'}), 400

    try:
        fetcher = CryptoDataFetcher()
        indicators_calc = MarketCycleIndicators()

        # Fetch data
        current_data = fetcher.get_current_price(symbol)
        historical_data = fetcher.get_historical_data(symbol, days=730)

        # Calculate indicators
        results = indicators_calc.analyze_all(historical_data)

        # Add interpretations
        for key, data in results.items():
            if key != 'overall_assessment':
                data['detailed_interpretation'] = IndicatorInterpreter.get_interpretation(key, data)

        # Create charts
        charts = {
            'price_chart': create_price_chart(historical_data, symbol),
            'pi_cycle_chart': create_pi_cycle_chart(historical_data, results['pi_cycle']),
            'rainbow_chart': create_rainbow_chart(historical_data, results['rainbow']),
            'rsi_chart': create_rsi_chart(results['rsi'])
        }

        # Clean up data for JSON serialization
        clean_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                clean_value = {k: v for k, v in value.items() if k != 'historical_data'}
                clean_results[key] = clean_value
            else:
                clean_results[key] = value

        return jsonify({
            'current_data': current_data,
            'indicators': clean_results,
            'charts': charts,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/feargreed')
def api_feargreed():
    """API endpoint for Fear & Greed Index"""
    try:
        fetcher = CryptoDataFetcher()
        fg_data = fetcher.get_fear_greed_index()

        chart = create_fear_greed_gauge(fg_data)
        interpretation = IndicatorInterpreter.interpret_fear_greed(fg_data['value'], fg_data['classification'])

        return jsonify({
            'data': fg_data,
            'chart': chart,
            'interpretation': interpretation,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare')
def api_compare():
    """API endpoint for comparing multiple coins"""
    try:
        fetcher = CryptoDataFetcher()
        indicators_calc = MarketCycleIndicators()

        comparison_data = {}

        for symbol in ['BTC', 'ETH', 'SOL']:
            current_data = fetcher.get_current_price(symbol)
            historical_data = fetcher.get_historical_data(symbol, days=730)
            results = indicators_calc.analyze_all(historical_data)

            # Clean results
            clean_results = {}
            for key, value in results.items():
                if isinstance(value, dict):
                    clean_value = {k: v for k, v in value.items() if k != 'historical_data'}
                    clean_results[key] = clean_value
                else:
                    clean_results[key] = value

            comparison_data[symbol] = {
                'current': current_data,
                'indicators': clean_results
            }

        return jsonify({
            'data': comparison_data,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
