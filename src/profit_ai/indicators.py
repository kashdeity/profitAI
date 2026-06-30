from __future__ import annotations

import pandas as pd

# The minimum number of rows we need after all indicators are calculated.
# Below this, analysis results are too unreliable to show.
MIN_ROWS_REQUIRED = 10


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the market dataframe with all technical indicators attached.

    Why min_periods matters:
    Without it, rolling(window=50).mean() produces NaN for the first 49 rows.
    If your period is only 1-2 months (~21-42 trading days), every single row
    becomes NaN for sma_50, and dropna() wipes the whole dataframe.

    With min_periods, the calculation starts as soon as enough rows are available.
    For example, rolling(window=50, min_periods=10) will compute a valid average
    once it has at least 10 data points instead of requiring all 50.
    The values are less statistically ideal but far better than crashing.
    """
    result = df.copy()

    # ── Trend: SMA ─────────────────────────────────────────────────────────────
    # min_periods = half the window so short datasets still produce values.
    result["sma_20"] = result["close"].rolling(window=20, min_periods=5).mean()
    result["sma_50"] = result["close"].rolling(window=50, min_periods=10).mean()
    result["ema_12"] = result["close"].ewm(span=12, adjust=False, min_periods=3).mean()
    result["ema_26"] = result["close"].ewm(span=26, adjust=False, min_periods=5).mean()

    # ── RSI ────────────────────────────────────────────────────────────────────
    result["rsi_14"] = calculate_rsi(result["close"], window=14, min_periods=5)

    # ── MACD ───────────────────────────────────────────────────────────────────
    macd, macd_signal, macd_histogram = calculate_macd(result["close"])
    result["macd"] = macd
    result["macd_signal"] = macd_signal
    result["macd_histogram"] = macd_histogram

    # ── Bollinger Bands ────────────────────────────────────────────────────────
    result["bb_middle"] = result["close"].rolling(window=20, min_periods=5).mean()
    bb_std = result["close"].rolling(window=20, min_periods=5).std()
    result["bb_upper"] = result["bb_middle"] + 2 * bb_std
    result["bb_lower"] = result["bb_middle"] - 2 * bb_std
    bb_range = (result["bb_upper"] - result["bb_lower"]).replace(0, pd.NA)
    result["bb_position"] = (result["close"] - result["bb_lower"]) / bb_range

    # ── Volume ─────────────────────────────────────────────────────────────────
    result["volume_sma_20"] = result["volume"].rolling(window=20, min_periods=5).mean()
    result["volume_ratio"] = result["volume"] / result["volume_sma_20"].replace(
        0, pd.NA
    )

    # ── 52-week price position ─────────────────────────────────────────────────
    # min_periods=1 → always produces a value (uses whatever history is available).
    window_52w = min(252, len(result))
    result["high_52w"] = result["close"].rolling(window=window_52w, min_periods=1).max()
    result["low_52w"] = result["close"].rolling(window=window_52w, min_periods=1).min()
    range_52w = (result["high_52w"] - result["low_52w"]).replace(0, pd.NA)
    result["price_position_52w"] = (result["close"] - result["low_52w"]) / range_52w

    # Drop rows where any of the core indicators are still NaN.
    # With min_periods set above, this only removes the very first few rows
    # instead of wiping out everything when the period is short.
    core_columns = [
        "sma_20",
        "sma_50",
        "rsi_14",
        "macd",
        "macd_signal",
        "macd_histogram",
        "bb_upper",
        "bb_lower",
        "bb_position",
        "volume_ratio",
    ]
    result = result.dropna(subset=core_columns)

    return result


def calculate_rsi(
    close: pd.Series, window: int = 14, min_periods: int = 5
) -> pd.Series:
    delta = close.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    avg_gain = gains.rolling(window=window, min_periods=min_periods).mean()
    avg_loss = losses.rolling(window=window, min_periods=min_periods).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def calculate_macd(close: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series]:
    ema_12 = close.ewm(span=12, adjust=False, min_periods=3).mean()
    ema_26 = close.ewm(span=26, adjust=False, min_periods=5).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False, min_periods=3).mean()
    histogram = macd - signal
    return macd, signal, histogram
