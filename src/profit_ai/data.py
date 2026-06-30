from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import requests
import yfinance as yf


@dataclass(frozen=True)
class MarketRequest:
    asset_type: str
    symbol: str
    period: str = "6mo"
    days: int = 180


def load_market_data(request: MarketRequest) -> pd.DataFrame:
    """Load OHLCV market data for a stock or crypto asset.

    Stocks use Yahoo Finance via yfinance. Example symbol: AAPL, MSFT, TSLA.
    Crypto uses CoinGecko public API. Example symbol: bitcoin, ethereum, solana.
    """
    if request.asset_type == "stock":
        return load_stock_data(request.symbol, request.period)

    if request.asset_type == "crypto":
        return load_crypto_data(request.symbol, request.days)

    raise ValueError("asset_type must be either 'stock' or 'crypto'")


def load_stock_data(symbol: str, period: str = "6mo") -> pd.DataFrame:
    df = yf.download(
        symbol, period=period, interval="1d", progress=False, auto_adjust=True
    )

    if df.empty:
        raise ValueError(f"No stock data found for symbol: {symbol}")

    # yfinance can return multi-index columns in some versions.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [column[0] for column in df.columns]

    df = df.rename(columns=str.lower)
    df.index.name = "date"
    return df[["open", "high", "low", "close", "volume"]].dropna()


def load_crypto_data(coin_id: str, days: int = 180) -> pd.DataFrame:
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    response = requests.get(
        url,
        params={"vs_currency": "usd", "days": days, "interval": "daily"},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()

    prices = payload.get("prices", [])
    volumes = payload.get("total_volumes", [])

    if not prices:
        raise ValueError(f"No crypto data found for CoinGecko coin id: {coin_id}")

    price_df = pd.DataFrame(prices, columns=["timestamp", "close"])
    volume_df = pd.DataFrame(volumes, columns=["timestamp", "volume"])

    df = price_df.merge(volume_df, on="timestamp", how="left")
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
    df = df.drop(columns=["timestamp"])
    df = df.groupby("date", as_index=True).agg({"close": "last", "volume": "last"})

    # CoinGecko market_chart does not provide daily OHLC in this endpoint.
    # For indicators/backtests here, using close as open/high/low is enough for a beginner project.
    df["open"] = df["close"]
    df["high"] = df["close"]
    df["low"] = df["close"]
    return df[["open", "high", "low", "close", "volume"]].dropna()
