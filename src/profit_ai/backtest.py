from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from profit_ai.strategy import signal_for_row


@dataclass(frozen=True)
class BacktestResult:
    initial_cash: float
    final_value: float
    profit: float
    profit_percent: float
    trades: int
    buy_and_hold_value: float


def run_backtest(df: pd.DataFrame, initial_cash: float = 1000.0) -> BacktestResult:
    """Run a simple all-in/all-out paper backtest.

    Rules:
    - BUY means convert all cash into the asset.
    - SELL means convert all asset units back into cash.
    - HOLD means do nothing.

    This intentionally ignores fees, slippage, taxes, spread, and liquidity.
    """
    if df.empty or len(df) < 10:
        raise ValueError(
            f"Not enough data to backtest ({len(df)} rows after indicator calculation). "
            "Try a longer period — use 6mo or 1y for stocks, 180+ days for crypto. "
            "/ Yeterli veri yok. Stoklar için 6mo veya 1y, kripto için 180+ gün deneyin."
        )

    cash = initial_cash
    units = 0.0
    trades = 0

    for _, row in df.iterrows():
        signal = signal_for_row(row)
        price = float(row["close"])

        if signal == "BUY" and cash > 0:
            units = cash / price
            cash = 0.0
            trades += 1
        elif signal == "SELL" and units > 0:
            cash = units * price
            units = 0.0
            trades += 1

    last_price = float(df.iloc[-1]["close"])
    final_value = cash + units * last_price
    profit = final_value - initial_cash
    profit_percent = (profit / initial_cash) * 100

    first_price = float(df.iloc[0]["close"])
    buy_and_hold_units = initial_cash / first_price
    buy_and_hold_value = buy_and_hold_units * last_price

    return BacktestResult(
        initial_cash=initial_cash,
        final_value=final_value,
        profit=profit,
        profit_percent=profit_percent,
        trades=trades,
        buy_and_hold_value=buy_and_hold_value,
    )
