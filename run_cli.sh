#!/bin/bash
# Quick launcher for Crypto Analyzer CLI

cd "$(dirname "$0")"

echo "Crypto Analyzer CLI"
echo "==================="
echo ""
echo "Choose an option:"
echo "1. Analyze BTC"
echo "2. Analyze ETH"
echo "3. Analyze SOL"
echo "4. Compare all coins"
echo "5. Fear & Greed Index"
echo "6. Custom command"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        python cli.py analyze BTC --detailed
        ;;
    2)
        python cli.py analyze ETH --detailed
        ;;
    3)
        python cli.py analyze SOL --detailed
        ;;
    4)
        python cli.py compare
        ;;
    5)
        python cli.py feargreed --detailed
        ;;
    6)
        read -p "Enter command (e.g., analyze BTC): " cmd
        python cli.py $cmd
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
