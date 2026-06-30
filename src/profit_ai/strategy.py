from __future__ import annotations

import pandas as pd


def signal_for_row(row: pd.Series) -> str:
    """Rule-based signal for a single candle row, used by the backtester.

    Returns BUY, SELL, or HOLD.
    """
    score = 0

    # Trend
    if row["sma_20"] > row["sma_50"]:
        score += 1
    else:
        score -= 1

    # RSI
    if row["rsi_14"] < 35:
        score += 1
    elif row["rsi_14"] > 70:
        score -= 1

    # MACD
    if row["macd"] > row["macd_signal"]:
        score += 1
    else:
        score -= 1

    # Bollinger Bands
    bb_pos = row.get("bb_position", 0.5)
    if bb_pos < 0.15:
        score += 1
    elif bb_pos > 0.85:
        score -= 1

    if score >= 2:
        return "BUY"
    if score <= -2:
        return "SELL"
    return "HOLD"
