# Profit AI Starter

A beginner-friendly Python project for learning how stock/crypto analysis software works.

> Important: this project is for education and paper trading only. It does **not** guarantee profit and does **not** place real trades.

## What it does

- Downloads historical market prices for stocks or crypto
- Calculates basic indicators:
  - SMA 20 / SMA 50
  - RSI 14
  - MACD
- Produces a simple rule-based analysis signal:
  - `BUY`
  - `SELL`
  - `HOLD`
- Runs a simple backtest so you can see how a strategy would have performed historically

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
```

Windows Git Bash / sh:

```bash
. .venv/Scripts/activate
```

macOS/Linux:

```bash
. .venv/bin/activate
```

Install the project and dependencies:

```bash
pip install -e .
```

## Examples

Analyze Apple stock:

```bash
python -m profit_ai analyze --type stock --symbol AAPL --period 6mo
```

Analyze Bitcoin:

```bash
python -m profit_ai analyze --type crypto --symbol bitcoin --days 180
```

Backtest Apple:

```bash
python -m profit_ai backtest --type stock --symbol AAPL --period 1y
```

Backtest Bitcoin:

```bash
python -m profit_ai backtest --type crypto --symbol bitcoin --days 365
```

## How to learn from this project

Start by reading these files in order:

1. `src/profit_ai/__main__.py` - CLI commands
2. `src/profit_ai/data.py` - how prices are downloaded
3. `src/profit_ai/indicators.py` - how indicators are calculated
4. `src/profit_ai/strategy.py` - how BUY/SELL/HOLD is decided
5. `src/profit_ai/backtest.py` - how paper trading simulation works

## Next improvement ideas

- Add more indicators: Bollinger Bands, ATR, volume analysis
- Save results into MySQL
- Build a small web dashboard with PHP or Flask
- Add real news/sentiment analysis
- Add an LLM explanation layer using an API key
- Add risk controls: max position size, stop loss, take profit
- Add proper tests
