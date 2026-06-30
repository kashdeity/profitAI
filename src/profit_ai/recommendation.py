from __future__ import annotations

from dataclasses import dataclass, field

from profit_ai.i18n import Lang
from profit_ai.insights import MarketInsight


@dataclass
class Recommendation:
    action: str
    reasoning: str
    entry_plan: str
    key_levels: list[str]
    what_to_watch: list[str]
    risks: list[str]
    exit_guide: list[str]


def build_recommendation(insight: MarketInsight, lang: Lang) -> Recommendation:
    """Build a Recommendation in the given language from a MarketInsight.

    All text is generated through the Lang object so you can get English or
    Turkish output by swapping the lang argument — no logic changes needed.
    """
    signal = insight.signal
    close = insight.close
    sma_20 = insight.sma_20
    sma_50 = insight.sma_50
    bb_lower = insight.bb_lower
    bb_upper = insight.bb_upper
    low_52w = insight.low_52w
    high_52w = insight.high_52w
    rsi = insight.rsi_14

    # ── Nearest support and resistance ────────────────────────────────────────
    supports: list[float] = sorted(
        {
            round(v, 2)
            for v in [bb_lower, min(sma_20, sma_50), max(sma_20, sma_50), low_52w]
            if v < close
        },
        reverse=True,
    )
    resistances: list[float] = sorted(
        {
            round(v, 2)
            for v in [bb_upper, max(sma_20, sma_50), min(sma_20, sma_50), high_52w]
            if v > close
        },
    )
    nearest_support = supports[0] if supports else low_52w
    nearest_resistance = resistances[0] if resistances else high_52w

    # ── Stop loss and take profit ──────────────────────────────────────────────
    stop_loss = round(nearest_support * 0.97, 2)
    take_profit_1 = round(nearest_resistance, 2)
    take_profit_2 = round(nearest_resistance * 1.05, 2)
    risk_per_unit = close - stop_loss
    reward_per_unit = take_profit_1 - close
    rr_ratio = round(reward_per_unit / risk_per_unit, 1) if risk_per_unit > 0 else 0.0

    # ── Determine risk flags ───────────────────────────────────────────────────
    # These codes tell the Lang object which risk paragraphs to include.
    risk_flags: list[str] = []

    if insight.trend in ("DOWNTREND", "WEAKENING"):
        risk_flags.append("downtrend")

    if insight.volume_ratio < 0.7:
        risk_flags.append("low_volume")

    if rsi < 30 and insight.trend == "DOWNTREND":
        risk_flags.append("falling_knife")

    if insight.pct_from_high > -15:
        risk_flags.append("near_high")

    if rr_ratio < 1.5:
        risk_flags.append("low_rr")

    if signal in ("STRONG BUY", "BUY") and insight.trend == "DOWNTREND":
        risk_flags.append("contrarian")

    risk_flags.append("always")

    # ── Build sections through the Lang object ─────────────────────────────────
    action = lang.rec_action(signal)

    reasoning = lang.rec_reasoning(
        signal,
        close=f"{close:,.2f}",
        rsi=f"{rsi:.1f}",
    )

    entry_plan = lang.rec_entry(
        signal,
        close=f"{close:,.2f}",
        nearest_support=f"{nearest_support:,.2f}",
        sma_20=f"{sma_20:,.2f}",
        nearest_resistance=f"{nearest_resistance:,.2f}",
        stop_loss=f"{stop_loss:,.2f}",
        low_52w=f"{low_52w:,.2f}",
    )

    key_levels = lang.rec_key_levels(
        close=close,
        sma_20=sma_20,
        sma_50=sma_50,
        nearest_support=nearest_support,
        nearest_resistance=nearest_resistance,
        bb_lower=bb_lower,
        bb_upper=bb_upper,
        low_52w=low_52w,
        high_52w=high_52w,
        risk_per_unit=risk_per_unit,
        reward_per_unit=reward_per_unit,
        rr_ratio=rr_ratio,
    )

    what_to_watch = lang.rec_watch(
        sma_20=f"{sma_20:,.2f}",
        sma_50=f"{sma_50:,.2f}",
        bb_upper=f"{bb_upper:,.2f}",
        nearest_support=f"{nearest_support:,.2f}",
        low_52w=f"{low_52w:,.2f}",
    )

    risks = lang.rec_risks(risk_flags, rr_ratio)

    exit_guide = lang.rec_exit(
        stop_loss=f"{stop_loss:,.2f}",
        take_profit_1=f"{take_profit_1:,.2f}",
        take_profit_2=f"{take_profit_2:,.2f}",
    )

    return Recommendation(
        action=action,
        reasoning=reasoning,
        entry_plan=entry_plan,
        key_levels=key_levels,
        what_to_watch=what_to_watch,
        risks=risks,
        exit_guide=exit_guide,
    )
