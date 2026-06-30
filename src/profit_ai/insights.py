from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class MarketInsight:
    # Core price info
    close: float
    change_1d_pct: float
    change_7d_pct: float

    # Trend
    trend: str  # "UPTREND" | "DOWNTREND" | "RECOVERING" | "WEAKENING" | "SIDEWAYS"

    # Key price levels (used by the recommendation engine)
    sma_20: float
    sma_50: float
    bb_upper: float
    bb_lower: float

    # Price location
    price_position_label: (
        str  # code: "near_low" | "near_high" | "lower_third" | "upper_third" | "middle"
    )
    high_52w: float
    low_52w: float
    pct_from_high: float
    pct_from_low: float

    # Bollinger Bands
    bb_position_label: (
        str  # code: "below_lower_bb" | "near_lower_bb" | "inside_bb" | etc.
    )

    # RSI
    rsi_14: float
    rsi_label: str  # code: "extreme_oversold" | "oversold" | "slight_oversold" | "neutral" | etc.

    # Volume
    volume_ratio: float
    volume_label: str  # code: "huge_spike" | "high" | "very_low" | "low" | "normal"

    # Events — list of (event_key, params_dict) tuples.
    # The i18n module translates these into display text.
    # Example: ("rsi_oversold", {"rsi": 28.5})
    events: list[tuple[str, dict]] = field(default_factory=list)

    # Overall signal and score
    signal: str = "HOLD"
    opportunity_score: int = 0


def build_insights(df: pd.DataFrame) -> MarketInsight:
    """Build a rich MarketInsight from a fully-indicatored dataframe.

    Each section is a scoring rule with a named code so the i18n layer
    can translate labels and events into any language without changing this logic.
    """
    if len(df) < 2:
        raise ValueError("Need at least 2 rows to compute insights")

    latest = df.iloc[-1]
    prev = df.iloc[-2]
    week_ago = df.iloc[-7] if len(df) >= 7 else df.iloc[0]

    events: list[tuple[str, dict]] = []
    score = 0

    # ── Price changes ──────────────────────────────────────────────────────────
    close = float(latest["close"])
    change_1d_pct = (close - float(prev["close"])) / float(prev["close"]) * 100
    change_7d_pct = (close - float(week_ago["close"])) / float(week_ago["close"]) * 100

    # ── Trend ──────────────────────────────────────────────────────────────────
    sma_20 = float(latest["sma_20"])
    sma_50 = float(latest["sma_50"])

    if close > sma_20 > sma_50:
        trend = "UPTREND"
        score += 2
    elif close > sma_20 and sma_20 < sma_50:
        trend = "RECOVERING"
        score += 1
    elif close < sma_20 < sma_50:
        trend = "DOWNTREND"
        score -= 2
    elif close < sma_20 and sma_20 > sma_50:
        trend = "WEAKENING"
        score -= 1
    else:
        trend = "SIDEWAYS"

    # Golden Cross / Death Cross
    prev_sma_20 = float(prev["sma_20"])
    prev_sma_50 = float(prev["sma_50"])
    if prev_sma_20 < prev_sma_50 and sma_20 > sma_50:
        events.append(("golden_cross", {}))
        score += 3
    if prev_sma_20 > prev_sma_50 and sma_20 < sma_50:
        events.append(("death_cross", {}))
        score -= 3

    # ── 52-week position ───────────────────────────────────────────────────────
    high_52w = float(latest["high_52w"])
    low_52w = float(latest["low_52w"])
    pct_from_high = (close - high_52w) / high_52w * 100
    pct_from_low = (close - low_52w) / low_52w * 100
    pos_52w = float(latest["price_position_52w"])

    if pos_52w <= 0.10:
        price_position_label = "near_low"
        events.append(("near_52w_low", {"pct": pct_from_low}))
        score += 1
    elif pos_52w >= 0.90:
        price_position_label = "near_high"
        events.append(("near_52w_high", {"pct": abs(pct_from_high)}))
        score += 1
    elif pos_52w <= 0.30:
        price_position_label = "lower_third"
    elif pos_52w >= 0.70:
        price_position_label = "upper_third"
    else:
        price_position_label = "middle"

    # ── Bollinger Bands ────────────────────────────────────────────────────────
    bb_pos = float(latest["bb_position"])
    bb_upper_val = float(latest["bb_upper"])
    bb_lower_val = float(latest["bb_lower"])

    if bb_pos < 0:
        bb_position_label = "below_lower_bb"
        events.append(("below_bb_lower", {}))
        score += 2
    elif bb_pos > 1:
        bb_position_label = "above_upper_bb"
        events.append(("above_bb_upper", {}))
        score -= 2
    elif bb_pos < 0.20:
        bb_position_label = "near_lower_bb"
        score += 1
    elif bb_pos > 0.80:
        bb_position_label = "near_upper_bb"
        score -= 1
    else:
        bb_position_label = "inside_bb"

    # ── RSI ────────────────────────────────────────────────────────────────────
    rsi = float(latest["rsi_14"])
    prev_rsi = float(prev["rsi_14"])

    if rsi < 25:
        rsi_label = "extreme_oversold"
        events.append(("rsi_extreme_oversold", {"rsi": rsi}))
        score += 3
    elif rsi < 35:
        rsi_label = "oversold"
        events.append(("rsi_oversold", {"rsi": rsi}))
        score += 2
    elif rsi < 45:
        rsi_label = "slight_oversold"
        score += 1
    elif rsi > 80:
        rsi_label = "extreme_overbought"
        events.append(("rsi_extreme_overbought", {"rsi": rsi}))
        score -= 3
    elif rsi > 70:
        rsi_label = "overbought"
        events.append(("rsi_overbought", {"rsi": rsi}))
        score -= 2
    elif rsi > 60:
        rsi_label = "slight_overbought"
        score -= 1
    else:
        rsi_label = "neutral"

    # Bullish RSI divergence: price falling but RSI rising
    if change_7d_pct < -3 and rsi > prev_rsi:
        events.append(("rsi_bullish_divergence", {}))
        score += 2

    # ── MACD ───────────────────────────────────────────────────────────────────
    macd = float(latest["macd"])
    macd_signal_val = float(latest["macd_signal"])
    macd_hist = float(latest["macd_histogram"])
    prev_macd_hist = float(prev["macd_histogram"])

    if prev_macd_hist < 0 < macd_hist:
        events.append(("macd_bullish_cross", {}))
        score += 2
    elif prev_macd_hist > 0 > macd_hist:
        events.append(("macd_bearish_cross", {}))
        score -= 2
    elif macd > macd_signal_val:
        score += 1
    else:
        score -= 1

    # ── Volume ─────────────────────────────────────────────────────────────────
    volume_ratio = float(latest["volume_ratio"])

    if volume_ratio > 3.0:
        volume_label = "huge_spike"
        events.append(("volume_huge_spike", {"ratio": volume_ratio}))
    elif volume_ratio > 2.0:
        volume_label = "high"
        events.append(("volume_high", {"ratio": volume_ratio}))
        score += 1 if trend in ("UPTREND", "RECOVERING") else -1
    elif volume_ratio < 0.5:
        volume_label = "very_low"
        events.append(("volume_very_low", {}))
    elif volume_ratio < 0.7:
        volume_label = "low"
    else:
        volume_label = "normal"

    # ── Overall signal ─────────────────────────────────────────────────────────
    if score >= 4:
        signal = "STRONG BUY"
    elif score >= 2:
        signal = "BUY"
    elif score <= -4:
        signal = "STRONG SELL"
    elif score <= -2:
        signal = "SELL"
    else:
        signal = "HOLD"

    opportunity_score = max(0, min(100, 50 + score * 8))

    return MarketInsight(
        close=close,
        change_1d_pct=change_1d_pct,
        change_7d_pct=change_7d_pct,
        trend=trend,
        sma_20=sma_20,
        sma_50=sma_50,
        bb_upper=bb_upper_val,
        bb_lower=bb_lower_val,
        price_position_label=price_position_label,
        high_52w=high_52w,
        low_52w=low_52w,
        pct_from_high=pct_from_high,
        pct_from_low=pct_from_low,
        bb_position_label=bb_position_label,
        rsi_14=rsi,
        rsi_label=rsi_label,
        volume_ratio=volume_ratio,
        volume_label=volume_label,
        events=events,
        signal=signal,
        opportunity_score=opportunity_score,
    )
