#!/bin/bash
# Launcher for Crypto Analyzer Web Dashboard

cd "$(dirname "$0")"

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   Crypto Market Analyzer - Web Dashboard             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Starting web server..."
echo ""
echo "Once started, open your browser to:"
echo "  → http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "─────────────────────────────────────────────────────────"
echo ""

python web_app.py
