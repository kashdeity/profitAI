"""
menu.py — Interactive menu for Profit AI.

The entry point is run_menu(). It:
  1. Asks the user to choose a language (English or Turkish).
  2. Shows a numbered main menu in that language.
  3. Routes each choice to the correct feature.
  4. Loops back to the menu after each result.

run_menu() is called by __main__.py when the program is run with no arguments.
"""

from __future__ import annotations

import sys

from profit_ai.backtest import run_backtest
from profit_ai.data import MarketRequest, load_market_data
from profit_ai.i18n import Lang, select_language
from profit_ai.indicators import add_indicators
from profit_ai.insights import build_insights
from profit_ai.recommendation import build_recommendation
from profit_ai.scanner import DEFAULT_CRYPTO, DEFAULT_STOCKS, scan_symbols

SEP = "=" * 52
sep = "-" * 52


def run_menu() -> None:
    """Language selection → main menu loop."""
    lang = select_language()

    while True:
        choice = _show_main_menu(lang)

        if choice == "1":
            _run_analyze(lang)
        elif choice == "2":
            _run_scan(lang)
        elif choice == "3":
            _run_backtest(lang)
        elif choice == "4":
            _show_help(lang)
        elif choice == "5":
            print("\n  Güle güle! / Goodbye!\n")
            sys.exit(0)
        else:
            print(f"\n  {lang.t('invalid_choice')}\n")


# ── Main menu ──────────────────────────────────────────────────────────────────


def _show_main_menu(lang: Lang) -> str:
    print(f"\n{SEP}")
    print(f"  {lang.t('app_name')}  —  {lang.t('menu_title')}")
    print(SEP)
    print(f"  1.  {lang.t('menu_1')}")
    print(f"  2.  {lang.t('menu_2')}")
    print(f"  3.  {lang.t('menu_3')}")
    print(f"  4.  {lang.t('menu_4')}")
    print(f"  5.  {lang.t('menu_5')}")
    print(SEP)
    return input(f"  {lang.t('menu_prompt')}: ").strip()


# ── Analyze ────────────────────────────────────────────────────────────────────


def _run_analyze(lang: Lang) -> None:
    print(f"\n{sep}")
    asset_type = _ask_type(lang)
    if asset_type is None:
        return

    symbol = _ask_symbol(lang, asset_type)

    if asset_type == "stock":
        period = input(f"  {lang.t('enter_period')}: ").strip() or "6mo"
        days = 180
    else:
        period = "6mo"
        raw_days = input(f"  {lang.t('enter_days')}: ").strip()
        days = int(raw_days) if raw_days.isdigit() else 180

    print(f"\n  {lang.t('fetching', symbol=symbol.upper())}")
    try:
        request = MarketRequest(
            asset_type=asset_type, symbol=symbol, period=period, days=days
        )
        raw = load_market_data(request)
        data = add_indicators(raw)
        insight = build_insights(data)
        rec = build_recommendation(insight, lang)
        _print_analysis(symbol, asset_type, insight, rec, lang)
    except Exception as exc:
        print(f"\n  {lang.t('error_prefix')}: {exc}\n")

    input(f"\n  {lang.t('press_enter')}")


# ── Scan ───────────────────────────────────────────────────────────────────────


def _run_scan(lang: Lang) -> None:
    print(f"\n{sep}")
    asset_type = _ask_type(lang)
    if asset_type is None:
        return

    symbols = DEFAULT_STOCKS if asset_type == "stock" else DEFAULT_CRYPTO
    print(f"\n  {lang.t('scanning', n=len(symbols), asset_type=asset_type)}")

    results = scan_symbols(symbols, asset_type)
    _print_scan(results, lang)

    input(f"\n  {lang.t('press_enter')}")


# ── Backtest ───────────────────────────────────────────────────────────────────


def _run_backtest(lang: Lang) -> None:
    print(f"\n{sep}")
    asset_type = _ask_type(lang)
    if asset_type is None:
        return

    symbol = _ask_symbol(lang, asset_type)

    if asset_type == "stock":
        period = input(f"  {lang.t('enter_period')}: ").strip() or "6mo"
        days = 180
    else:
        period = "6mo"
        raw_days = input(f"  {lang.t('enter_days')}: ").strip()
        days = int(raw_days) if raw_days.isdigit() else 180

    raw_cash = input(f"  {lang.t('enter_cash')}: ").strip()
    cash = float(raw_cash) if raw_cash.replace(".", "").isdigit() else 1000.0

    print(f"\n  {lang.t('fetching', symbol=symbol.upper())}")
    try:
        request = MarketRequest(
            asset_type=asset_type, symbol=symbol, period=period, days=days
        )
        raw = load_market_data(request)
        data = add_indicators(raw)
        result = run_backtest(data, initial_cash=cash)
        _print_backtest(symbol, asset_type, result, lang)
    except Exception as exc:
        print(f"\n  {lang.t('error_prefix')}: {exc}\n")

    input(f"\n  {lang.t('press_enter')}")


# ── Help ───────────────────────────────────────────────────────────────────────


def _show_help(lang: Lang) -> None:
    print(f"\n{SEP}")
    print(f"  {lang.t('help_header')}")
    print(SEP)
    print(lang.t("help_body"))
    input(f"  {lang.t('press_enter')}")


# ── Input helpers ──────────────────────────────────────────────────────────────


def _ask_type(lang: Lang) -> str | None:
    raw = input(f"  {lang.t('enter_type')}: ").strip().lower()
    if raw not in ("stock", "crypto"):
        print(f"  {lang.t('type_error')}")
        return None
    return raw


def _ask_symbol(lang: Lang, asset_type: str) -> str:
    key = "enter_symbol_stock" if asset_type == "stock" else "enter_symbol_crypto"
    return input(f"  {lang.t(key)}: ").strip()


# ── Print functions ────────────────────────────────────────────────────────────


def _print_analysis(
    symbol: str,
    asset_type: str,
    insight,
    rec,
    lang: Lang,
) -> None:
    arrow_1d = "▲" if insight.change_1d_pct >= 0 else "▼"
    arrow_7d = "▲" if insight.change_7d_pct >= 0 else "▼"

    print(f"\n{SEP}")
    print(f"  {symbol.upper()}  ({asset_type.upper()})  —  {lang.t('analysis_title')}")
    print(SEP)

    print(f"\n  {lang.t('price_label'):<14}: {insight.close:,.2f}")
    print(f"  {lang.t('change_1d'):<14}: {arrow_1d} {insight.change_1d_pct:+.2f}%")
    print(f"  {lang.t('change_7d'):<14}: {arrow_7d} {insight.change_7d_pct:+.2f}%")
    print(
        f"  {lang.t('week52_high'):<14}: {insight.high_52w:,.2f}  "
        f"({insight.pct_from_high:.1f}% {lang.t('pct_from_here')})"
    )
    print(
        f"  {lang.t('week52_low'):<14}: {insight.low_52w:,.2f}  "
        f"({insight.pct_from_low:.1f}% {lang.t('pct_above_low')})"
    )

    print(f"\n{sep}")
    print(f"  {lang.t('signal_header'):<14}: *** {lang.signal(insight.signal)} ***")
    print(f"  {lang.t('opportunity_label'):<14}: {insight.opportunity_score}/100")
    print(sep)

    print(f"\n  {lang.t('trend_label'):<14}: {lang.trend(insight.trend)}")
    print(f"  {lang.t('detail_label'):<14}: {lang.trend_detail(insight.trend)}")
    print(
        f"  {lang.t('rsi_label'):<14}: {insight.rsi_14:.1f}  [{lang.rsi_lbl(insight.rsi_label)}]"
    )
    print(
        f"  {lang.t('bollinger_label'):<14}: {lang.bb_lbl(insight.bb_position_label)}"
    )
    print(
        f"  {lang.t('volume_label'):<14}: {insight.volume_ratio:.1f}x {lang.t('vol_avg')}"
        f"  [{lang.volume_lbl(insight.volume_label)}]"
    )
    print(
        f"  {lang.t('position52w_label'):<14}: {lang.position_lbl(insight.price_position_label)}"
    )

    if insight.events:
        print(f"\n{sep}")
        print(f"  {lang.t('events_header')}:")
        for event_key, event_params in insight.events:
            print(f"    • {lang.event(event_key, event_params)}")

    print(f"\n{sep}")
    print(f"  {lang.t('summary_label')}: {lang.summary(insight.signal)}")
    print(sep)
    print(f"\n  {lang.t('disclaimer').capitalize()}.")
    print(SEP)
    _print_recommendation(rec, lang)
    print(SEP)
    print(f"  {lang.t('final_disclaimer_label')}: {lang.t('final_disclaimer')}")
    print(SEP)


def _print_recommendation(rec, lang: Lang) -> None:
    print(f"\n{SEP}")
    print(f"  {lang.t('rec_header')}")
    print(SEP)
    print(f"\n  {lang.t('rec_action_label')}: {rec.action}")
    print(f"\n  {lang.t('rec_why_label')}:")
    for line in _wrap(rec.reasoning, width=50):
        print(f"  {line}")

    print(f"\n{sep}")
    print(f"  {lang.t('rec_entry_label')}:")
    for line in rec.entry_plan.split("\n"):
        print(f"  {line}")

    print(f"\n{sep}")
    print(f"  {lang.t('rec_levels_label')}:")
    for level in rec.key_levels:
        print(f"    {level}")

    print(f"\n{sep}")
    print(f"  {lang.t('rec_exit_label')}:")
    for line in rec.exit_guide:
        print(f"    {line}")

    print(f"\n{sep}")
    print(f"  {lang.t('rec_watch_label')}:")
    for item in rec.what_to_watch:
        print(f"    • {item}")

    print(f"\n{sep}")
    print(f"  {lang.t('rec_risks_label')}:")
    for risk in rec.risks:
        for line in _wrap(risk, width=50):
            print(f"    {line}")
        print()


def _print_scan(results: list, lang: Lang) -> None:
    WIDTH = 72
    print(f"\n{'=' * WIDTH}")
    print(f"  {lang.t('scan_header')}")
    print("=" * WIDTH)

    header = (
        f"  {lang.t('scan_col_symbol'):<14} "
        f"{lang.t('scan_col_signal'):<14} "
        f"{lang.t('scan_col_score'):>5} "
        f"{lang.t('scan_col_price'):>10} "
        f"{lang.t('scan_col_24h'):>7} "
        f"{lang.t('scan_col_rsi'):>6}  "
        f"{lang.t('scan_col_trend')}"
    )
    print(header)
    print("-" * WIDTH)

    for r in results:
        if r.error:
            print(f"  {r.symbol:<14} {lang.t('error_prefix')}: {r.error[:40]}")
            continue
        i = r.insight
        arrow = "▲" if i.change_1d_pct >= 0 else "▼"
        print(
            f"  {r.symbol:<14} {lang.signal(i.signal):<14} {i.opportunity_score:>4}  "
            f"{i.close:>10,.2f} {arrow}{abs(i.change_1d_pct):>4.1f}% "
            f"{i.rsi_14:>6.1f}  {lang.trend(i.trend)}"
        )

    print("=" * WIDTH)

    top = [
        r
        for r in results
        if r.error is None and r.insight.signal in ("STRONG BUY", "BUY")
    ]
    if top:
        print(f"\n  {lang.t('scan_top')} ({len(top)} {lang.t('scan_symbols')}):")
        for r in top:
            print(f"\n  >>> {r.symbol}")
            for event_key, event_params in r.insight.events[:3]:
                print(f"      • {lang.event(event_key, event_params)}")
    else:
        print(f"\n  {lang.t('scan_none')}")

    print(f"\n{'=' * WIDTH}")
    print(f"  {lang.t('disclaimer').capitalize()}.")
    print("=" * WIDTH)


def _print_backtest(symbol: str, asset_type: str, result, lang: Lang) -> None:
    print(f"\n{SEP}")
    print(f"  {symbol.upper()}  —  {lang.t('backtest_title')}")
    print(SEP)
    print(f"\n  {lang.t('bt_starting_cash'):<22}: ${result.initial_cash:>10,.2f}")
    print(f"  {lang.t('bt_strategy_value'):<22}: ${result.final_value:>10,.2f}")
    print(f"  {lang.t('bt_profit_loss'):<22}: ${result.profit:>+10,.2f}")
    print(f"  {lang.t('bt_return'):<22}: {result.profit_percent:>+.2f}%")
    print(f"  {lang.t('bt_trades'):<22}: {result.trades}")
    print(f"\n{sep}")
    bnh_return = (
        (result.buy_and_hold_value - result.initial_cash) / result.initial_cash * 100
    )
    print(f"  {lang.t('bt_bnh_value'):<22}: ${result.buy_and_hold_value:>10,.2f}")
    print(f"  {lang.t('bt_bnh_return'):<22}: {bnh_return:>+.2f}%")

    print()
    if result.final_value > result.buy_and_hold_value:
        diff = result.final_value - result.buy_and_hold_value
        print(f"  {lang.t('bt_strategy_beat')} ${diff:,.2f}")
    else:
        diff = result.buy_and_hold_value - result.final_value
        print(f"  {lang.t('bt_bnh_beat')} ${diff:,.2f}")

    print(f"\n{sep}")
    print(f"  {lang.t('bt_note')}")
    print(SEP)


# ── Utility ────────────────────────────────────────────────────────────────────


def _wrap(text: str, width: int = 50) -> list[str]:
    """Simple word wrapper for terminal output."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
