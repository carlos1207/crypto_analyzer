#!/usr/bin/env python3
"""
Crypto Analyzer CLI - Command-line interface for cryptocurrency market analysis
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from rich.text import Text
from datetime import datetime
import sys

from data_fetcher import CryptoDataFetcher
from indicators import MarketCycleIndicators
from interpreter import IndicatorInterpreter
from config import SUPPORTED_COINS

console = Console()


def get_signal_color(signal: str) -> str:
    """Map signal to color"""
    if 'TOP' in signal or 'OVERBOUGHT' in signal or 'GREED' in signal:
        return 'red'
    elif 'BOTTOM' in signal or 'OVERSOLD' in signal or 'FEAR' in signal:
        return 'green'
    elif 'WARNING' in signal or 'BULLISH' in signal:
        return 'yellow'
    else:
        return 'blue'


def format_price(price: float) -> str:
    """Format price with appropriate decimals"""
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.2f}"
    else:
        return f"${price:.6f}"


def display_coin_header(coin_data: dict):
    """Display coin header with current price info"""
    price_change_24h = coin_data.get('price_change_24h', 0)
    change_color = 'green' if price_change_24h >= 0 else 'red'
    change_symbol = '+' if price_change_24h >= 0 else ''

    header_text = f"""
[bold cyan]{coin_data['name']} ({coin_data['symbol']})[/bold cyan]
Current Price: [bold]{format_price(coin_data['current_price'])}[/bold]
24h Change: [{change_color}]{change_symbol}{price_change_24h:.2f}%[/{change_color}]
7d Change: {coin_data.get('price_change_7d', 0):.2f}%
Market Cap: ${coin_data['market_cap']:,.0f}
"""
    console.print(Panel(header_text, border_style="cyan", box=box.DOUBLE))


def display_indicator_summary(results: dict):
    """Display summary table of all indicators"""
    table = Table(title="Market Cycle Indicators Summary", box=box.ROUNDED, show_header=True, header_style="bold magenta")

    table.add_column("Indicator", style="cyan", width=25)
    table.add_column("Signal", width=20)
    table.add_column("Quick Interpretation", width=50)

    for key, data in results.items():
        if key == 'overall_assessment':
            continue

        signal = data.get('signal', 'N/A')
        signal_color = get_signal_color(signal)
        name = data.get('name', key)
        interpretation = data.get('interpretation', 'N/A')

        table.add_row(
            name,
            f"[{signal_color}]{signal}[/{signal_color}]",
            interpretation[:80] + "..." if len(interpretation) > 80 else interpretation
        )

    console.print("\n")
    console.print(table)


def display_detailed_interpretation(indicator_name: str, data: dict):
    """Display detailed interpretation for an indicator"""
    interpretation = IndicatorInterpreter.get_interpretation(indicator_name, data)

    title = f"📊 {data.get('name', indicator_name)}"
    console.print("\n")
    console.print(Panel(interpretation, title=title, border_style=get_signal_color(data.get('signal', '')), box=box.DOUBLE, padding=(1, 2)))


def display_overall_assessment(assessment: str):
    """Display overall market assessment"""
    console.print("\n")
    console.print(Panel(
        f"[bold yellow]{assessment}[/bold yellow]",
        title="🎯 Overall Market Assessment",
        border_style="yellow",
        box=box.DOUBLE
    ))


def display_fear_greed(fg_data: dict):
    """Display Fear & Greed Index"""
    value = fg_data['value']
    classification = fg_data['classification']

    # Create visual gauge
    gauge = "█" * (value // 5) + "░" * (20 - (value // 5))
    color = 'red' if value > 75 else 'green' if value < 25 else 'yellow'

    text = f"""
Fear & Greed Index: [{color}]{value}/100[/{color}] - {classification.upper()}

[{color}]{gauge}[/{color}]
0 (Fear) {'':>40} 100 (Greed)

{IndicatorInterpreter.interpret_fear_greed(value, classification)}
"""
    console.print("\n")
    console.print(Panel(text, title="😱 Fear & Greed Index", border_style=color, box=box.DOUBLE))


@click.group()
def cli():
    """Crypto Analyzer - Market Cycle Analysis Tool"""
    pass


@cli.command()
@click.argument('symbol', type=click.Choice(['BTC', 'ETH', 'SOL'], case_sensitive=False))
@click.option('--detailed', '-d', is_flag=True, help='Show detailed interpretations for all indicators')
@click.option('--days', default=730, help='Number of days of historical data (default: 730)')
def analyze(symbol: str, detailed: bool, days: int):
    """
    Analyze a cryptocurrency with market cycle indicators

    Example: crypto-analyzer analyze BTC --detailed
    """
    symbol = symbol.upper()

    try:
        with console.status(f"[bold cyan]Fetching data for {symbol}...", spinner="dots"):
            fetcher = CryptoDataFetcher()

            # Fetch current price data
            current_data = fetcher.get_current_price(symbol)

            # Fetch historical data
            historical_data = fetcher.get_historical_data(symbol, days=days)

        # Display coin header
        display_coin_header(current_data)

        with console.status(f"[bold cyan]Calculating indicators...", spinner="dots"):
            # Calculate all indicators
            indicators = MarketCycleIndicators()
            results = indicators.analyze_all(historical_data)

        # Display summary
        display_indicator_summary(results)

        # Display overall assessment
        display_overall_assessment(results['overall_assessment'])

        # Display detailed interpretations if requested
        if detailed:
            console.print("\n[bold cyan]═" * 50 + "[/bold cyan]")
            console.print("[bold cyan]Detailed Indicator Interpretations[/bold cyan]")
            console.print("[bold cyan]═" * 50 + "[/bold cyan]\n")

            for key, data in results.items():
                if key != 'overall_assessment':
                    display_detailed_interpretation(key, data)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@cli.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed interpretation')
def feargreed(detailed: bool):
    """
    Show the current Crypto Fear & Greed Index

    Example: crypto-analyzer feargreed --detailed
    """
    try:
        with console.status("[bold cyan]Fetching Fear & Greed Index...", spinner="dots"):
            fetcher = CryptoDataFetcher()
            fg_data = fetcher.get_fear_greed_index()

        if detailed:
            display_fear_greed(fg_data)
        else:
            value = fg_data['value']
            classification = fg_data['classification']
            color = 'red' if value > 75 else 'green' if value < 25 else 'yellow'

            console.print(f"\nFear & Greed Index: [{color}]{value}/100[/{color}] - {classification.upper()}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@cli.command()
def compare():
    """
    Compare BTC, ETH, and SOL side by side

    Example: crypto-analyzer compare
    """
    try:
        with console.status("[bold cyan]Fetching data for all coins...", spinner="dots"):
            fetcher = CryptoDataFetcher()
            indicators_calc = MarketCycleIndicators()

            comparison_data = {}

            for symbol in ['BTC', 'ETH', 'SOL']:
                current_data = fetcher.get_current_price(symbol)
                historical_data = fetcher.get_historical_data(symbol, days=730)
                results = indicators_calc.analyze_all(historical_data)

                comparison_data[symbol] = {
                    'current': current_data,
                    'indicators': results
                }

        # Create comparison table
        table = Table(title="Multi-Coin Comparison", box=box.ROUNDED, show_header=True, header_style="bold magenta")

        table.add_column("Metric", style="cyan", width=25)
        table.add_column("BTC", width=20)
        table.add_column("ETH", width=20)
        table.add_column("SOL", width=20)

        # Add price row
        table.add_row(
            "Current Price",
            format_price(comparison_data['BTC']['current']['current_price']),
            format_price(comparison_data['ETH']['current']['current_price']),
            format_price(comparison_data['SOL']['current']['current_price'])
        )

        # Add 24h change
        def format_change(change):
            color = 'green' if change >= 0 else 'red'
            symbol = '+' if change >= 0 else ''
            return f"[{color}]{symbol}{change:.2f}%[/{color}]"

        table.add_row(
            "24h Change",
            format_change(comparison_data['BTC']['current']['price_change_24h']),
            format_change(comparison_data['ETH']['current']['price_change_24h']),
            format_change(comparison_data['SOL']['current']['price_change_24h'])
        )

        # Add separator
        table.add_row("", "", "", "")

        # Add indicator signals
        indicator_names = {
            'pi_cycle': 'Pi Cycle',
            'two_year_ma': '2Y MA Multiplier',
            'rsi': 'RSI',
            'rainbow': 'Rainbow Chart',
            'mayer': 'Mayer Multiple',
            'golden_ratio': 'Golden Ratio'
        }

        for key, name in indicator_names.items():
            btc_signal = comparison_data['BTC']['indicators'][key]['signal']
            eth_signal = comparison_data['ETH']['indicators'][key]['signal']
            sol_signal = comparison_data['SOL']['indicators'][key]['signal']

            btc_color = get_signal_color(btc_signal)
            eth_color = get_signal_color(eth_signal)
            sol_color = get_signal_color(sol_signal)

            table.add_row(
                name,
                f"[{btc_color}]{btc_signal}[/{btc_color}]",
                f"[{eth_color}]{eth_signal}[/{eth_color}]",
                f"[{sol_color}]{sol_signal}[/{sol_color}]"
            )

        console.print("\n")
        console.print(table)

        # Overall assessments
        console.print("\n[bold cyan]Overall Assessments:[/bold cyan]")
        for symbol in ['BTC', 'ETH', 'SOL']:
            assessment = comparison_data[symbol]['indicators']['overall_assessment']
            console.print(f"\n[bold]{symbol}:[/bold] {assessment}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@cli.command()
def list_coins():
    """List all supported cryptocurrencies"""
    console.print("\n[bold cyan]Supported Cryptocurrencies:[/bold cyan]\n")
    for symbol, name in SUPPORTED_COINS.items():
        console.print(f"  • {symbol} - {name.capitalize()}")
    console.print()


if __name__ == '__main__':
    cli()
