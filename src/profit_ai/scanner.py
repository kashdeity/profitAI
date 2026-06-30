from __future__ import annotations

from dataclasses import dataclass

from profit_ai.data import MarketRequest, load_market_data
from profit_ai.indicators import add_indicators
from profit_ai.insights import MarketInsight, build_insights

# ── Tam sembol katalogları (UI dropdown için) ──────────────────────────────────
# format:  { ticker/id : "Emoji  Görünen Ad" }

STOCK_CATALOG: dict[str, str] = {
    # ── ABD Teknoloji / US Technology ─────────────────────────────────────────
    "AAPL": "💻  Apple",
    "MSFT": "💻  Microsoft",
    "NVDA": "💻  NVIDIA",
    "GOOGL": "💻  Google (Alphabet)",
    "AMZN": "📦  Amazon",
    "TSLA": "⚡  Tesla",
    "META": "💬  Meta",
    "AMD": "💻  AMD",
    "INTC": "💻  Intel",
    "NFLX": "🎬  Netflix",
    "ORCL": "💻  Oracle",
    "CRM": "☁️  Salesforce",
    "PLTR": "🔐  Palantir",
    "SHOP": "🛒  Shopify",
    # ── ABD Finans / US Finance ────────────────────────────────────────────────
    "JPM": "🏦  JPMorgan Chase",
    "BAC": "🏦  Bank of America",
    "GS": "🏦  Goldman Sachs",
    "V": "💳  Visa",
    "MA": "💳  Mastercard",
    "PYPL": "💳  PayPal",
    # ── ABD Tüketici & Medya / US Consumer & Media ────────────────────────────
    "KO": "🥤  Coca-Cola",
    "DIS": "🎠  Disney",
    "NKE": "👟  Nike",
    "SBUX": "☕  Starbucks",
    "MCD": "🍔  McDonald's",
    "WMT": "🛒  Walmart",
    # ── ABD Enerji & Sanayi / US Energy & Industrial ──────────────────────────
    "XOM": "⛽  ExxonMobil",
    "BA": "✈️  Boeing",
    "BRK-B": "📊  Berkshire Hathaway",
    # ── Çin / China ──────────────────────────────────────────────────────────
    "BABA": "🇨🇳  Alibaba",
    "BIDU": "🇨🇳  Baidu",
    "JD": "🇨🇳  JD.com",
    # ── Borsa İstanbul / Turkish Stocks (ISE) ─────────────────────────────────
    "THYAO.IS": "🇹🇷  Türk Hava Yolları (THY)",
    "EREGL.IS": "🇹🇷  Ereğli Demir ve Çelik",
    "ASELS.IS": "🇹🇷  ASELSAN",
    "KCHOL.IS": "🇹🇷  Koç Holding",
    "BIMAS.IS": "🇹🇷  BİM",
    "GARAN.IS": "🇹🇷  Garanti BBVA",
    "AKBNK.IS": "🇹🇷  Akbank",
    "ISCTR.IS": "🇹🇷  İş Bankası (C)",
    "TUPRS.IS": "🇹🇷  Tüpraş",
    "SASA.IS": "🇹🇷  SASA Polyester",
    "TOASO.IS": "🇹🇷  Tofaş Otomobil",
    "SAHOL.IS": "🇹🇷  Sabancı Holding",
    "FROTO.IS": "🇹🇷  Ford Otosan",
    "PGSUS.IS": "🇹🇷  Pegasus",
    "MAVI.IS": "🇹🇷  Mavi Giyim",
}

CRYPTO_CATALOG: dict[str, str] = {
    "bitcoin": "₿   Bitcoin (BTC)",
    "ethereum": "Ξ   Ethereum (ETH)",
    "solana": "◎   Solana (SOL)",
    "binancecoin": "🟡  BNB",
    "ripple": "✦   XRP",
    "cardano": "♠   Cardano (ADA)",
    "dogecoin": "🐕  Dogecoin (DOGE)",
    "avalanche-2": "🔺  Avalanche (AVAX)",
    "polkadot": "•   Polkadot (DOT)",
    "chainlink": "⛓  Chainlink (LINK)",
    "uniswap": "🦄  Uniswap (UNI)",
    "litecoin": "Ł   Litecoin (LTC)",
    "stellar": "✦   Stellar (XLM)",
    "near": "Ⓝ   NEAR Protocol",
    "shiba-inu": "🐕  Shiba Inu (SHIB)",
    "pepe": "🐸  PEPE",
    "sui": "💧  Sui (SUI)",
    "the-open-network": "💎  Toncoin (TON)",
    "aptos": "◈   Aptos (APT)",
    "injective-protocol": "🔷  Injective (INJ)",
}

# ── Tarama listesi (scan komutu için, katalogdan seçilmiş alt küme) ────────────
DEFAULT_STOCKS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "TSLA",
    "META",
    "AMD",
    "JPM",
    "NFLX",
    "THYAO.IS",
    "EREGL.IS",
    "GARAN.IS",
    "KCHOL.IS",
]

DEFAULT_CRYPTO = [
    "bitcoin",
    "ethereum",
    "solana",
    "binancecoin",
    "ripple",
    "cardano",
    "dogecoin",
    "avalanche-2",
]


@dataclass
class ScanResult:
    symbol: str
    asset_type: str
    insight: MarketInsight
    error: str | None = None


def scan_symbols(
    symbols: list[str],
    asset_type: str,
    period: str = "6mo",
    days: int = 180,
) -> list[ScanResult]:
    """Scan a list of symbols and return their insights, sorted by opportunity score."""
    results: list[ScanResult] = []

    for symbol in symbols:
        request = MarketRequest(
            asset_type=asset_type,
            symbol=symbol,
            period=period,
            days=days,
        )
        try:
            raw = load_market_data(request)
            data = add_indicators(raw)
            insight = build_insights(data)
            results.append(
                ScanResult(symbol=symbol, asset_type=asset_type, insight=insight)
            )
        except Exception as exc:
            results.append(
                ScanResult(
                    symbol=symbol, asset_type=asset_type, insight=None, error=str(exc)
                )  # type: ignore[arg-type]
            )

    signal_order = {"STRONG BUY": 0, "BUY": 1, "HOLD": 2, "SELL": 3, "STRONG SELL": 4}
    successful = [r for r in results if r.error is None]
    failed = [r for r in results if r.error is not None]
    successful.sort(
        key=lambda r: (
            signal_order.get(r.insight.signal, 99),
            -r.insight.opportunity_score,
        )
    )

    return successful + failed
