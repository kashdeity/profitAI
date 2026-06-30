"""
__main__.py — Entry point for  python -m profit_ai

Two modes:
  Interactive  (no arguments)  — language selection → menu
  CLI          (with arguments)  — direct commands in English for power users

CLI usage:
  python -m profit_ai analyze  --type stock  --symbol AAPL
  python -m profit_ai analyze  --type crypto --symbol bitcoin
  python -m profit_ai scan     --type stock
  python -m profit_ai scan     --type crypto
  python -m profit_ai backtest --type stock  --symbol AAPL --period 1y
  python -m profit_ai help
"""

from __future__ import annotations

import sys


def _ensure_utf8() -> None:
    """Force stdout/stderr to UTF-8 on Windows so arrows and Turkish chars print correctly."""
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> None:
    _ensure_utf8()
    # No arguments → interactive menu (language selection + full menu)
    if len(sys.argv) == 1:
        from profit_ai.menu import run_menu

        run_menu()
        return

    # help / ?help → show English help and exit
    if sys.argv[1].lower() in ("help", "?help", "yardim", "?yardim"):
        from profit_ai.i18n import Lang
        from profit_ai.menu import _show_help

        _show_help(Lang("en"))
        return

    # Otherwise: parse CLI arguments (always English, for backward compatibility)
    _run_cli()


def _run_cli() -> None:
    """CLI mode — parses arguments and runs the requested command in English."""
    import argparse

    from profit_ai.backtest import run_backtest
    from profit_ai.data import MarketRequest, load_market_data
    from profit_ai.i18n import Lang
    from profit_ai.indicators import add_indicators
    from profit_ai.insights import build_insights
    from profit_ai.menu import (
        _print_analysis,
        _print_backtest,
        _print_scan,
    )
    from profit_ai.recommendation import build_recommendation
    from profit_ai.scanner import DEFAULT_CRYPTO, DEFAULT_STOCKS, scan_symbols

    lang = Lang("en")

    parser = argparse.ArgumentParser(
        prog="python -m profit_ai",
        description="Market insight analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Interactive mode (language selection + menu):
  python -m profit_ai

CLI examples:
  python -m profit_ai analyze  --type stock  --symbol AAPL
  python -m profit_ai analyze  --type crypto --symbol bitcoin
  python -m profit_ai scan     --type stock
  python -m profit_ai scan     --type crypto
  python -m profit_ai backtest --type stock  --symbol AAPL --period 1y
  python -m profit_ai help
""",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # analyze
    analyze_p = subparsers.add_parser("analyze", help="Deep analysis of one symbol")
    _add_market_args(analyze_p)

    # scan
    scan_p = subparsers.add_parser(
        "scan", help="Scan multiple symbols and rank by opportunity"
    )
    scan_p.add_argument("--type", choices=["stock", "crypto"], required=True)
    scan_p.add_argument("--period", default="6mo")
    scan_p.add_argument("--days", type=int, default=180)

    # backtest
    bt_p = subparsers.add_parser("backtest", help="Paper backtest a symbol")
    _add_market_args(bt_p)
    bt_p.add_argument("--cash", type=float, default=1000.0)

    args = parser.parse_args()

    if args.command == "analyze":
        request = MarketRequest(
            asset_type=args.type,
            symbol=args.symbol,
            period=args.period,
            days=args.days,
        )
        print(f"\n  {lang.t('fetching', symbol=args.symbol.upper())}")
        raw = load_market_data(request)
        data = add_indicators(raw)
        insight = build_insights(data)
        rec = build_recommendation(insight, lang)
        _print_analysis(args.symbol, args.type, insight, rec, lang)

    elif args.command == "scan":
        symbols = DEFAULT_STOCKS if args.type == "stock" else DEFAULT_CRYPTO
        print(f"\n  {lang.t('scanning', n=len(symbols), asset_type=args.type)}")
        results = scan_symbols(symbols, args.type, period=args.period, days=args.days)
        _print_scan(results, lang)

    elif args.command == "backtest":
        request = MarketRequest(
            asset_type=args.type,
            symbol=args.symbol,
            period=args.period,
            days=args.days,
        )
        print(f"\n  {lang.t('fetching', symbol=args.symbol.upper())}")
        raw = load_market_data(request)
        data = add_indicators(raw)
        result = run_backtest(data, initial_cash=args.cash)
        _print_backtest(args.symbol, args.type, result, lang)


def _add_market_args(parser) -> None:
    parser.add_argument("--type", choices=["stock", "crypto"], required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--period", default="6mo")
    parser.add_argument("--days", type=int, default=180)


if __name__ == "__main__":
    main()
