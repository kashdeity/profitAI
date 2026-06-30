"""
app.py — Profit AI Web Dashboard
Çalıştır / Run:  streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# src/ klasörünü Python yoluna ekle
sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from profit_ai.backtest import run_backtest
from profit_ai.data import MarketRequest, load_market_data
from profit_ai.i18n import Lang
from profit_ai.indicators import add_indicators
from profit_ai.insights import build_insights
from profit_ai.recommendation import build_recommendation
from profit_ai.scanner import (
    CRYPTO_CATALOG,
    DEFAULT_CRYPTO,
    DEFAULT_STOCKS,
    STOCK_CATALOG,
    scan_symbols,
)
from profit_ai.strategy import signal_for_row

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA AYARLARI / PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Profit AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CUSTOM CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    """
<style>
.signal-pill {
    display:inline-block; padding:6px 22px; border-radius:30px;
    font-size:1.5rem; font-weight:900; letter-spacing:2px; margin-bottom:4px;
}
.sig-STRONG-BUY,  .sig-GÜÇLÜ-AL   { background:#00C853; color:#fff; }
.sig-BUY,         .sig-AL          { background:#4CAF50; color:#fff; }
.sig-HOLD,        .sig-BEKLE       { background:#FF9800; color:#fff; }
.sig-SELL,        .sig-SAT         { background:#e53935; color:#fff; }
.sig-STRONG-SELL, .sig-GÜÇLÜ-SAT  { background:#b71c1c; color:#fff; }

.big-signal { text-align:center; padding:20px 10px; }
.big-emoji  { font-size:4rem; line-height:1.2; }
.big-text   { font-size:2.2rem; font-weight:900; margin:6px 0; }

.card {
    background:#1e2130; border-radius:14px; padding:18px 20px;
    margin:6px 0; border-left:4px solid #444;
}
.card-green { border-left-color:#4CAF50; }
.card-red   { border-left-color:#e53935; }
.card-orange{ border-left-color:#FF9800; }
.card-blue  { border-left-color:#42a5f5; }

.card-title { font-size:.75rem; text-transform:uppercase;
              letter-spacing:1px; color:#888; margin-bottom:4px; }
.card-value { font-size:1.5rem; font-weight:700; color:#f0f0f0; }
.card-sub   { font-size:.82rem; color:#aaa; margin-top:3px; }

.step { background:#232640; border-radius:10px; padding:12px 16px;
        margin:5px 0; display:flex; align-items:flex-start; gap:12px; }
.step-icon { font-size:1.4rem; flex-shrink:0; }
.step-body { font-size:.92rem; color:#ddd; line-height:1.5; }
.step-body b { color:#fff; }

.bull-card { background:linear-gradient(135deg,#1b4332,#2d6a4f);
             border:1px solid #40916c; border-radius:12px; padding:16px; }
.bear-card { background:linear-gradient(135deg,#3d0000,#7b1a1a);
             border:1px solid #c1121f; border-radius:12px; padding:16px; }
.scenario-title { font-weight:700; font-size:1rem; margin-bottom:8px; }
.scenario-row   { font-size:.85rem; color:#ddd; margin:4px 0; }

.ind-table { width:100%; border-collapse:collapse; }
.ind-table td { padding:8px 12px; border-bottom:1px solid #2a2a40;
                font-size:.88rem; }
.ind-table td:first-child { color:#999; width:40%; }
.ind-table td:last-child  { color:#f0f0f0; font-weight:600; }

.disclaimer { font-size:.72rem; color:#555; font-style:italic;
              border-left:2px solid #333; padding-left:8px; margin-top:16px; }

.gauge-wrap { margin:14px 0; }
.gauge-label { display:flex; justify-content:space-between;
               font-size:.75rem; color:#777; margin-bottom:4px; }
.gauge-bar { height:12px; border-radius:6px;
             background:linear-gradient(90deg,#e53935,#FF9800,#4CAF50); position:relative; }
.gauge-dot { width:14px; height:14px; background:#fff; border:2px solid #333;
             border-radius:50%; position:absolute; top:-1px;
             transform:translateX(-50%); }
</style>
""",
    unsafe_allow_html=True,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SİNYAL YARDIMCıLARı / SIGNAL HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIGNAL_COLORS = {
    "STRONG BUY": "#00C853",
    "GÜÇLÜ AL": "#00C853",
    "BUY": "#4CAF50",
    "AL": "#4CAF50",
    "HOLD": "#FF9800",
    "BEKLE": "#FF9800",
    "SELL": "#e53935",
    "SAT": "#e53935",
    "STRONG SELL": "#b71c1c",
    "GÜÇLÜ SAT": "#b71c1c",
}

SIGNAL_EMOJIS = {
    "STRONG BUY": "🟢",
    "GÜÇLÜ AL": "🟢",
    "BUY": "🟢",
    "AL": "🟢",
    "HOLD": "🟡",
    "BEKLE": "🟡",
    "SELL": "🔴",
    "SAT": "🔴",
    "STRONG SELL": "🔴",
    "GÜÇLÜ SAT": "🔴",
}

# Başlangıç sekme içeriği / Beginner tab content
BEGINNER = {
    "en": {
        "STRONG BUY": {
            "headline": "Rare buying opportunity! 🎯",
            "explain": (
                "The price has dropped a lot and multiple indicators agree: "
                "it looks very cheap right now. RSI is extremely low, meaning too "
                "many people sold too fast. Think of it like a rubber band stretched "
                "too far — it tends to snap back. This setup is rare and worth attention."
            ),
            "bull_title": "🟢 If it goes up (Bull scenario)",
            "bear_title": "🔴 If it keeps falling (Bear scenario)",
            "steps_title": "What should you do?",
            "steps": [
                (
                    "1️⃣",
                    "Enter with <b>1/3 of your planned amount</b> now while the signal is strong.",
                ),
                (
                    "2️⃣",
                    "If price drops to <b>Support level</b>, add another 1/3. Buy cheaper.",
                ),
                (
                    "3️⃣",
                    "Set your <b>Stop Loss</b>. If it drops below that, exit — no hesitation.",
                ),
            ],
        },
        "BUY": {
            "headline": "Looks interesting — cautious entry possible",
            "explain": (
                "More good signals than bad ones. The price isn't at a perfect low "
                "but it leans bullish. Don't go all-in. Start small, watch what happens, "
                "and only add more when you see confirmation."
            ),
            "bull_title": "🟢 If it goes up",
            "bear_title": "🔴 If it falls",
            "steps_title": "What should you do?",
            "steps": [
                (
                    "1️⃣",
                    "Start with a <b>small position</b> (25-33% of what you'd normally invest).",
                ),
                (
                    "2️⃣",
                    "Wait for RSI to climb above 45 or price to close above <b>SMA20</b> before adding more.",
                ),
                (
                    "3️⃣",
                    "Set your <b>Stop Loss</b> below the nearest support. Protect yourself first.",
                ),
            ],
        },
        "HOLD": {
            "headline": "Wait — not a clear moment yet",
            "explain": (
                "The signals are fighting each other — some say up, some say down. "
                "The market is undecided. Entering now is like driving in thick fog. "
                "Smart traders wait for clarity. Set alerts and check back later."
            ),
            "bull_title": "🟢 When to consider buying",
            "bear_title": "🔴 What could push it lower",
            "steps_title": "What should you do?",
            "steps": [
                (
                    "⏳",
                    "Do <b>not enter</b> a new position right now. Cash is a position too.",
                ),
                (
                    "🔔",
                    "Set a <b>price alert</b> at the Support level (potential discount entry).",
                ),
                (
                    "👀",
                    "Watch for RSI to drop below 30 or MACD to cross — then reassess.",
                ),
            ],
        },
        "SELL": {
            "headline": "Bearish — avoid new entries",
            "explain": (
                "More bad signals than good. The price is showing weakness. "
                "This is not a good time to buy. If you already hold this asset, "
                "think about whether you still believe in it — or protect your gains."
            ),
            "bull_title": "🟢 When could it recover?",
            "bear_title": "🔴 The risk right now",
            "steps_title": "What should you do?",
            "steps": [
                (
                    "🚫",
                    "Do <b>not open new positions</b> here. Wait for the trend to change.",
                ),
                (
                    "🛡️",
                    "If you already hold it, consider <b>selling 30-50%</b> to reduce exposure.",
                ),
                ("⚠️", "Move your stop loss closer. <b>Protect what you have</b>."),
            ],
        },
        "STRONG SELL": {
            "headline": "High risk — strong bearish signals",
            "explain": (
                "Almost every indicator is flashing red at the same time. "
                "Staying in a strong downtrend hoping for a recovery usually "
                "leads to bigger losses. Professional traders cut losses early. "
                "Cash is safe — you can always buy back lower."
            ),
            "bull_title": "🟢 Recovery would need...",
            "bear_title": "🔴 The risk right now",
            "steps_title": "What should you do?",
            "steps": [
                ("🚨", "<b>Do not buy</b> under any circumstances right now."),
                (
                    "💼",
                    "If you hold this, seriously consider <b>exiting most or all</b> of your position.",
                ),
                (
                    "📉",
                    "If you stay, set a <b>strict stop loss</b>. The next key level is the 52-week low.",
                ),
            ],
        },
    },
    "tr": {
        "STRONG BUY": {
            "headline": "Nadir bir alım fırsatı! 🎯",
            "explain": (
                "Fiyat çok düştü ve birden fazla gösterge aynı anda aynı şeyi söylüyor: "
                "şu an çok ucuz görünüyor. RSI aşırı düşük — yani çok fazla insan çok hızlı sattı. "
                "Bir lastik gibi düşün: çok gerdikçe geri fırlar. Bu tür kurulum nadirdir, dikkat et."
            ),
            "bull_title": "🟢 Eğer yükselirse (Yükseliş senaryosu)",
            "bear_title": "🔴 Eğer düşmeye devam ederse (Düşüş senaryosu)",
            "steps_title": "Ne yapmalısın?",
            "steps": [
                (
                    "1️⃣",
                    "Sinyal güçlü olduğu için <b>planladığının 1/3'ü kadar</b> şimdi gir.",
                ),
                (
                    "2️⃣",
                    "Fiyat <b>Destek seviyesine</b> düşerse bir 1/3 daha ekle. Daha ucuza al.",
                ),
                (
                    "3️⃣",
                    "<b>Zarar Kes</b> seviyeni belirle. O seviyenin altına düşerse tereddütsüz çık.",
                ),
            ],
        },
        "BUY": {
            "headline": "İlgi çekici görünüyor — temkinli giriş olabilir",
            "explain": (
                "İyi sinyaller kötüden fazla. Fiyat mükemmel bir dip noktasında değil "
                "ama yükselen yönde eğilimli. Hepsini bir anda yatırma. Küçük başla, "
                "ne olduğunu gözlemle, doğrulama gördüğünde daha fazlasını ekle."
            ),
            "bull_title": "🟢 Yükseliş senaryosu",
            "bear_title": "🔴 Düşüş senaryosu",
            "steps_title": "Ne yapmalısın?",
            "steps": [
                (
                    "1️⃣",
                    "<b>Küçük bir pozisyon</b> aç (normalde yatıracağının %25-33'ü kadar).",
                ),
                (
                    "2️⃣",
                    "RSI 45'in üzerine çıkana ya da fiyat <b>SMA20'nin</b> üzerinde kapanana kadar bekle.",
                ),
                (
                    "3️⃣",
                    "En yakın destek seviyesinin altına <b>Zarar Kes</b> koy. Önce kendini koru.",
                ),
            ],
        },
        "HOLD": {
            "headline": "Bekle — henüz net bir an değil",
            "explain": (
                "Sinyaller birbirine karşı çalışıyor — bazıları yukarı, bazıları aşağı diyor. "
                "Piyasa kararsız. Şu an girmek yoğun siste araba kullanmak gibi. "
                "Akıllı yatırımcılar netlik bekler. Alarm kur, sonra tekrar bak."
            ),
            "bull_title": "🟢 Ne zaman almayı düşünebilirsin?",
            "bear_title": "🔴 Ne düşürür?",
            "steps_title": "Ne yapmalısın?",
            "steps": [
                ("⏳", "Şu an <b>yeni pozisyon açma</b>. Nakit de bir pozisyondur."),
                (
                    "🔔",
                    "Destek seviyesine <b>fiyat alarmı</b> kur (indirimli giriş fırsatı olabilir).",
                ),
                (
                    "👀",
                    "RSI 30'un altına düşerse veya MACD çapraz yaparsa tekrar değerlendir.",
                ),
            ],
        },
        "SELL": {
            "headline": "Düşüş — yeni giriş yapma",
            "explain": (
                "Kötü sinyaller iyi sinyalden fazla. Fiyat zayıflık gösteriyor. "
                "Şu an almak için iyi bir zaman değil. Bu varlığı zaten tutuyorsan, "
                "hâlâ inanıyor musun? Yoksa kazancını koru."
            ),
            "bull_title": "🟢 Ne zaman toparlanabilir?",
            "bear_title": "🔴 Şu anki risk",
            "steps_title": "Ne yapmalısın?",
            "steps": [
                (
                    "🚫",
                    "Buradan <b>yeni pozisyon açma</b>. Trend değişene kadar bekle.",
                ),
                ("🛡️", "Zaten tutuyorsan, maruziyeti azaltmak için <b>%30-50 sat</b>."),
                ("⚠️", "Zarar kesini yaklaştır. <b>Elindekini koru</b>."),
            ],
        },
        "STRONG SELL": {
            "headline": "Yüksek risk — güçlü düşüş sinyalleri",
            "explain": (
                "Neredeyse her gösterge aynı anda kırmızı yanıyor. "
                "Güçlü bir düşüş trendinde toparlanma umuduyla kalmak "
                "genellikle daha büyük kayıplara yol açar. Profesyoneller zararı erken keser. "
                "Nakit güvenlidir — daha aşağıdan her zaman geri alabilirsin."
            ),
            "bull_title": "🟢 Toparlanma için ne gerekir?",
            "bear_title": "🔴 Şu anki risk",
            "steps_title": "Ne yapmalısın?",
            "steps": [
                ("🚨", "Şu an <b>kesinlikle alma</b>."),
                (
                    "💼",
                    "Bu varlığı tutuyorsan, <b>büyük bölümünü satmayı</b> ciddi olarak düşün.",
                ),
                (
                    "📉",
                    "Kalırsan <b>katı bir zarar kes</b> belirle. Bir sonraki kilit seviye 52 haftalık dip.",
                ),
            ],
        },
    },
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  VERİ YÜKLEME / DATA LOADING  (cache: 15 dk)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data(ttl=900, show_spinner=False)
def fetch_and_process(asset_type: str, symbol: str, period: str, days: int):
    """Veriyi indir, göstergeleri hesapla ve önbelleğe al."""
    request = MarketRequest(
        asset_type=asset_type, symbol=symbol, period=period, days=days
    )
    raw = load_market_data(request)
    data = add_indicators(raw)
    return raw, data


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GRAFİK OLUŞTURUCU / CHART BUILDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _show_not_found_error(
    err: str, symbol: str, asset_type: str, lang_code: str
) -> None:
    """Sembol bulunamadiğında dil destekli, yönlendirici hata mesajı göster."""
    e_low = err.lower()
    is_tr = lang_code == "tr"

    # Bulunamadı hatası mı?
    not_found = any(
        x in e_low
        for x in [
            "no stock data found",
            "no crypto data found",
            "no data found",
            "404",
            "not found",
            "invalid",
            "yfinance",
            "coingecko",
        ]
    )

    if not_found and asset_type == "stock":
        if is_tr:
            st.error(
                f"❌  **'{symbol}' bulunamadı.**\n\n"
                "Bu sembol Yahoo Finance'de mevcut değil. Kontrol et:\n"
                "- ABD hisseleri büyük harf: `AAPL`, `MSFT`, `TSLA`\n"
                "- **Borsa İstanbul** için sona `.IS` ekle: `THYAO.IS`, `GARAN.IS`, `KCHOL.IS`\n"
                "- Yazımın doğru olduğundan emin ol\n\n"
                "Sol menüden hazır listeden seçim yapabilir ya da 'Manuel sembol gir' seçeneğini kullanabilirsin."
            )
        else:
            st.error(
                f"❌  **'{symbol}' not found.**\n\n"
                "This ticker doesn't exist on Yahoo Finance. Check:\n"
                "- US stocks use uppercase: `AAPL`, `MSFT`, `TSLA`\n"
                "- **Turkish stocks** add `.IS` suffix: `THYAO.IS`, `GARAN.IS`, `KCHOL.IS`\n"
                "- Double-check the spelling\n\n"
                "You can pick from the ready-made list in the sidebar instead."
            )

    elif not_found and asset_type == "crypto":
        if is_tr:
            st.error(
                f"❌  **'{symbol}' kripto bulunamadı.**\n\n"
                "Bu coin CoinGecko'da mevcut değil. Kontrol et:\n"
                "- Tam, küçük harfli isim kullan: `bitcoin`, `ethereum`, `solana`\n"
                "- Kısaltma değil tam isim: `dogecoin` (DOGE değil), `ripple` (XRP değil)\n"
                "- Doğru ID için: coingecko.com'da aratabilirsin\n\n"
                "Sol menüden hazır kripto listesinden seçim yapabilirsin."
            )
        else:
            st.error(
                f"❌  **'{symbol}' crypto not found.**\n\n"
                "This coin ID doesn't exist on CoinGecko. Check:\n"
                "- Use the full lowercase name: `bitcoin`, `ethereum`, `solana`\n"
                "- Not the ticker symbol: `dogecoin` not `DOGE`, `ripple` not `XRP`\n"
                "- Search coingecko.com for the exact coin ID\n\n"
                "You can pick from the ready-made list in the sidebar instead."
            )
    else:
        # Genel hata
        if is_tr:
            st.error(f"❌  Bir hata oluştu: {err}")
        else:
            st.error(f"❌  An error occurred: {err}")


def _render_welcome(lang: Lang, lang_code: str) -> None:
    """Full-screen welcome page shown before the first analysis."""

    is_tr = lang_code == "tr"

    st.markdown(
        """
    <style>
    @keyframes fadeUp {
        from { opacity:0; transform:translateY(24px); }
        to   { opacity:1; transform:translateY(0);    }
    }
    .hero {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-radius: 20px;
        padding: 56px 40px 48px;
        text-align: center;
        margin-bottom: 32px;
        animation: fadeUp .6s ease both;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(66,165,245,.18);
        color: #42a5f5;
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 5px 16px;
        border-radius: 20px;
        border: 1px solid rgba(66,165,245,.35);
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: clamp(2.2rem, 5vw, 3.4rem);
        font-weight: 900;
        background: linear-gradient(90deg, #42a5f5, #4CAF50, #FF9800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.15;
        margin-bottom: 16px;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #b0bec5;
        max-width: 560px;
        margin: 0 auto 32px;
        line-height: 1.65;
    }
    .hero-arrow {
        font-size: 1rem;
        color: #42a5f5;
        animation: fadeUp .8s ease .4s both;
    }

    .feat-grid {
        display: grid;
        grid-template-columns: repeat(3,1fr);
        gap: 16px;
        margin-bottom: 28px;
        animation: fadeUp .6s ease .2s both;
    }
    @media(max-width:720px){ .feat-grid{ grid-template-columns:1fr; } }
    .feat-card {
        background: #161b2e;
        border: 1px solid #1e2740;
        border-radius: 16px;
        padding: 24px 20px;
        transition: border-color .25s, transform .2s;
        text-align: center;
    }
    .feat-card:hover { border-color:#42a5f5; transform:translateY(-3px); }
    .feat-icon  { font-size: 2.4rem; margin-bottom: 12px; }
    .feat-title { font-size: 1rem;   font-weight: 700; color: #e0e0e0; margin-bottom: 8px; }
    .feat-desc  { font-size: .83rem; color: #90a4ae; line-height: 1.55; }

    .steps-wrap {
        background: #161b2e;
        border: 1px solid #1e2740;
        border-radius: 16px;
        padding: 28px 24px;
        animation: fadeUp .6s ease .35s both;
    }
    .steps-title { font-size: 1rem; font-weight:700; color:#e0e0e0;
                   text-transform:uppercase; letter-spacing:1px; margin-bottom:18px; }
    .step-row {
        display:flex; align-items:flex-start; gap:14px;
        padding: 10px 0; border-bottom:1px solid #1e2740;
    }
    .step-row:last-child { border-bottom:none; }
    .step-num-circle {
        width:30px; height:30px; border-radius:50%;
        background: linear-gradient(135deg,#1565c0,#42a5f5);
        display:flex; align-items:center; justify-content:center;
        font-size:.85rem; font-weight:800; color:#fff; flex-shrink:0;
    }
    .step-row-text { font-size:.9rem; color:#b0bec5; line-height:1.5; padding-top:4px; }
    .step-row-text b { color:#e0e0e0; }

    .ticker-strip {
        display: flex; gap: 24px; overflow-x: auto;
        padding: 14px 4px; margin-bottom: 28px;
        animation: fadeUp .6s ease .15s both;
        scrollbar-width: none;
    }
    .ticker-strip::-webkit-scrollbar { display:none; }
    .ticker-item {
        background: #161b2e; border:1px solid #1e2740;
        border-radius:12px; padding:12px 20px;
        text-align:center; flex-shrink:0; min-width:110px;
    }
    .ticker-sym  { font-size:.75rem; color:#888; letter-spacing:1px; }
    .ticker-name { font-size:.95rem; font-weight:700; color:#e0e0e0; margin:2px 0; }
    .ticker-note { font-size:.72rem; color:#42a5f5; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # ── Hero bölümü ─────────────────────────────────────────────────────────
    badge = (
        "Educational Market Analysis" if not is_tr else "Eğitim Amaçlı Piyasa Analizi"
    )
    title = "Profit AI"
    sub_en = (
        "Real market data. AI-powered signals. Plain language you can actually understand — "
        "whether you're a complete beginner or an experienced trader."
    )
    sub_tr = (
        "Gerçek piyasa verisi. Yapay zeka destekli sinyaller. "
        "İster yeni başlayan ister deneyimli olun, herkesin anlayacağı sade bir analiz."
    )
    sub = sub_tr if is_tr else sub_en
    arrow = (
        "← Select a symbol in the sidebar to begin"
        if not is_tr
        else "← Başlamak için sol kenar çubuğundan sembol seç"
    )

    st.markdown(
        f"""
    <div class="hero">
        <div class="hero-badge">{badge}</div>
        <div class="hero-title">📈 {title}</div>
        <div class="hero-sub">{sub}</div>
        <div class="hero-arrow">{arrow}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Popüler semboller şeridi ─────────────────────────────────────────────
    tickers = [
        ("AAPL", "Apple", "Stock"),
        ("NVDA", "NVIDIA", "Stock"),
        ("TSLA", "Tesla", "Stock"),
        ("MSFT", "Microsoft", "Stock"),
        ("BTC", "Bitcoin", "Crypto"),
        ("ETH", "Ethereum", "Crypto"),
        ("SOL", "Solana", "Crypto"),
    ]
    items_html = "".join(
        f'<div class="ticker-item">'
        f'<div class="ticker-sym">{sym}</div>'
        f'<div class="ticker-name">{name}</div>'
        f'<div class="ticker-note">{kind}</div>'
        f"</div>"
        for sym, name, kind in tickers
    )
    st.markdown(
        f'<div class="ticker-strip">{items_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Özellik kartları ─────────────────────────────────────────────────────
    if not is_tr:
        feats = [
            (
                "🔍",
                "Deep Analysis",
                "Full chart with price, Bollinger Bands, RSI and MACD. "
                "Beginner and professional views side by side.",
            ),
            (
                "📡",
                "Market Scanner",
                "Scan 8 stocks or 5 cryptos at once, ranked by opportunity score. "
                "Spot the best setups fast.",
            ),
            (
                "📜",
                "Strategy Backtest",
                "See how the strategy would have performed historically. "
                "Equity curve vs Buy & Hold.",
            ),
        ]
    else:
        feats = [
            (
                "🔍",
                "Derin Analiz",
                "Fiyat, Bollinger Bantları, RSI ve MACD ile tam grafik. "
                "Başlangıç ve profesyonel görünümü yan yana.",
            ),
            (
                "📡",
                "Piyasa Taraması",
                "8 hisse veya 5 kripto parayı aynı anda tara, fırsat puanına göre sırala. "
                "En iyi kurulumları hızla bul.",
            ),
            (
                "📜",
                "Strateji Testi",
                "Stratejinin geçmişte nasıl performans gösterdiğini gör. "
                "Eşitlik eğrisi vs Al ve Tut.",
            ),
        ]

    cards_html = "".join(
        f'<div class="feat-card">'
        f'<div class="feat-icon">{icon}</div>'
        f'<div class="feat-title">{title_}</div>'
        f'<div class="feat-desc">{desc}</div>'
        f"</div>"
        for icon, title_, desc in feats
    )
    st.markdown(
        f'<div class="feat-grid">{cards_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Hızlı başlangıç adımları ─────────────────────────────────────────────
    if not is_tr:
        steps_title = "How to get started"
        steps = [
            ("1", "Choose <b>Stock</b> or <b>Crypto</b> in the sidebar."),
            ("2", "Type a symbol — e.g. <b>AAPL</b>, <b>NVDA</b>, or <b>bitcoin</b>."),
            ("3", "Select a time period (6mo recommended for best signals)."),
            (
                "4",
                "Click <b>ANALYZE</b> and switch between Beginner and Professional tabs.",
            ),
        ]
    else:
        steps_title = "Nasıl başlanır"
        steps = [
            ("1", "Sol kenar çubuğundan <b>Stock</b> (Hisse) veya <b>Crypto</b> seç."),
            ("2", "Sembol yaz — örn. <b>AAPL</b>, <b>NVDA</b> veya <b>bitcoin</b>."),
            ("3", "Bir dönem seç (en iyi sinyaller için 6mo önerilir)."),
            (
                "4",
                "<b>ANALİZ ET</b>'e tıkla, Başlangıç ve Profesyonel sekmeleri arasında geç.",
            ),
        ]

    rows_html = "".join(
        f'<div class="step-row">'
        f'<div class="step-num-circle">{n}</div>'
        f'<div class="step-row-text">{text}</div>'
        f"</div>"
        for n, text in steps
    )
    st.markdown(
        f'<div class="steps-wrap"><div class="steps-title">{steps_title}</div>{rows_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Uyarı notu ───────────────────────────────────────────────────────────
    note = (
        "⚠️ This tool is for **educational purposes only**. "
        "Nothing here is financial advice."
        if not is_tr
        else "⚠️ Bu araç yalnızca **eğitim amaçlıdır**. "
        "Buradaki hiçbir şey yatırım tavsiyesi değildir."
    )
    st.markdown(f"")
    st.caption(note)


def build_chart(
    data: pd.DataFrame,
    insight,
    rec,
    symbol: str,
    asset_type: str,
    lang: Lang,
) -> go.Figure:
    """
    4 bölümlü interaktif grafik:
      Bölüm 1: Fiyat (mum/çizgi) + SMA20 + SMA50 + Bollinger + sinyal markırları + hedef çizgiler
      Bölüm 2: Hacim
      Bölüm 3: RSI (30/70 çizgileri ile)
      Bölüm 4: MACD (histogram + çizgiler)
    """
    is_crypto = asset_type == "crypto"

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.025,
        row_heights=[0.52, 0.14, 0.17, 0.17],
        subplot_titles=(
            f"{symbol.upper()} — {lang.t('price_label')}",
            lang.t("volume_label"),
            "RSI 14",
            "MACD",
        ),
    )

    dates = data.index

    # ── Bölüm 1: Fiyat grafiği ────────────────────────────────────────────
    if is_crypto:
        # Kripto: sadece kapanış fiyatı var
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=data["close"],
                name=symbol.upper(),
                line=dict(color="#42a5f5", width=2),
                fill="tozeroy",
                fillcolor="rgba(66,165,245,0.07)",
            ),
            row=1,
            col=1,
        )
    else:
        # Hisse: OHLC mum grafiği
        fig.add_trace(
            go.Candlestick(
                x=dates,
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["close"],
                name=symbol.upper(),
                increasing_line_color="#4CAF50",
                decreasing_line_color="#e53935",
            ),
            row=1,
            col=1,
        )

    # SMA 20
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["sma_20"],
            name="SMA 20",
            line=dict(color="#FF9800", width=1.5, dash="solid"),
        ),
        row=1,
        col=1,
    )

    # SMA 50
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["sma_50"],
            name="SMA 50",
            line=dict(color="#ab47bc", width=1.5, dash="solid"),
        ),
        row=1,
        col=1,
    )

    # Bollinger üst bant
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["bb_upper"],
            name="BB Üst/Upper",
            line=dict(color="rgba(180,180,180,0.5)", width=1, dash="dot"),
            showlegend=True,
        ),
        row=1,
        col=1,
    )

    # Bollinger alt bant + doldurma
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["bb_lower"],
            name="BB Alt/Lower",
            line=dict(color="rgba(180,180,180,0.5)", width=1, dash="dot"),
            fill="tonexty",
            fillcolor="rgba(180,180,180,0.06)",
        ),
        row=1,
        col=1,
    )

    # ── Sinyal markırları ─────────────────────────────────────────────────
    # Her gün için sinyali hesapla, BUY/SELL noktalarını işaretle
    buy_x, buy_y, sell_x, sell_y = [], [], [], []
    for date, row in data.iterrows():
        sig = signal_for_row(row)
        price = float(row["close"])
        if sig == "BUY":
            buy_x.append(date)
            buy_y.append(price * 0.985)
        elif sig == "SELL":
            sell_x.append(date)
            sell_y.append(price * 1.015)

    if buy_x:
        fig.add_trace(
            go.Scatter(
                x=buy_x,
                y=buy_y,
                mode="markers",
                name="AL/BUY",
                marker=dict(symbol="triangle-up", size=10, color="#4CAF50"),
            ),
            row=1,
            col=1,
        )
    if sell_x:
        fig.add_trace(
            go.Scatter(
                x=sell_x,
                y=sell_y,
                mode="markers",
                name="SAT/SELL",
                marker=dict(symbol="triangle-down", size=10, color="#e53935"),
            ),
            row=1,
            col=1,
        )

    # ── Senaryo çizgileri: Zarar Kes, Hedef 1, Hedef 2 ───────────────────
    # Recommendation'dan stop loss ve take profit seviyelerini al
    stop_loss_val = _parse_price(rec.exit_guide[0])
    tp1_val = _parse_price(rec.exit_guide[1])
    tp2_val = _parse_price(rec.exit_guide[2])

    _add_hline(fig, stop_loss_val, "🛑 Stop Loss", "#e53935", "dash")
    _add_hline(fig, tp1_val, "🎯 Hedef 1/TP1", "#4CAF50", "dot")
    _add_hline(fig, tp2_val, "🎯 Hedef 2/TP2", "#00C853", "dot")

    # ── Bölüm 2: Hacim ───────────────────────────────────────────────────
    vol_colors = [
        "#4CAF50" if c >= o else "#e53935" for c, o in zip(data["close"], data["open"])
    ]
    fig.add_trace(
        go.Bar(
            x=dates,
            y=data["volume"],
            name=lang.t("volume_label"),
            marker_color=vol_colors,
            opacity=0.7,
        ),
        row=2,
        col=1,
    )

    # Hacim ortalaması
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["volume_sma_20"],
            name="Vol MA20",
            line=dict(color="#FF9800", width=1),
        ),
        row=2,
        col=1,
    )

    # ── Bölüm 3: RSI ─────────────────────────────────────────────────────
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["rsi_14"],
            name="RSI 14",
            line=dict(color="#42a5f5", width=2),
            fill="tozeroy",
            fillcolor="rgba(66,165,245,0.05)",
        ),
        row=3,
        col=1,
    )

    # RSI 70 çizgisi (aşırı alınmış)
    fig.add_hline(
        y=70,
        line_dash="dot",
        line_color="#e53935",
        annotation_text="70",
        annotation_position="left",
        row=3,
        col=1,
    )
    # RSI 50 orta çizgi
    fig.add_hline(y=50, line_dash="dot", line_color="#888", row=3, col=1)
    # RSI 30 çizgisi (aşırı satılmış)
    fig.add_hline(
        y=30,
        line_dash="dot",
        line_color="#4CAF50",
        annotation_text="30",
        annotation_position="left",
        row=3,
        col=1,
    )

    # RSI bölge renklendirme
    fig.add_hrect(
        y0=70, y1=100, fillcolor="rgba(229,57,53,0.08)", line_width=0, row=3, col=1
    )
    fig.add_hrect(
        y0=0, y1=30, fillcolor="rgba(76,175,80,0.08)", line_width=0, row=3, col=1
    )

    # ── Bölüm 4: MACD ────────────────────────────────────────────────────
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["macd"],
            name="MACD",
            line=dict(color="#42a5f5", width=1.5),
        ),
        row=4,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=data["macd_signal"],
            name="MACD Signal",
            line=dict(color="#FF9800", width=1.5),
        ),
        row=4,
        col=1,
    )

    hist_colors = ["#4CAF50" if v >= 0 else "#e53935" for v in data["macd_histogram"]]
    fig.add_trace(
        go.Bar(
            x=dates,
            y=data["macd_histogram"],
            name="MACD Hist",
            marker_color=hist_colors,
            opacity=0.8,
        ),
        row=4,
        col=1,
    )

    fig.add_hline(y=0, line_color="#555", line_width=1, row=4, col=1)

    # ── Genel düzen ───────────────────────────────────────────────────────
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#ccc", size=11),
        legend=dict(
            orientation="h",
            x=0,
            y=1.02,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10),
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        height=750,
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
    )

    # Y eksen etiketleri
    fig.update_yaxes(
        title_text=lang.t("price_label"), row=1, col=1, gridcolor="#1a1a2e"
    )
    fig.update_yaxes(
        title_text=lang.t("volume_label"), row=2, col=1, gridcolor="#1a1a2e"
    )
    fig.update_yaxes(
        title_text="RSI", row=3, col=1, range=[0, 100], gridcolor="#1a1a2e"
    )
    fig.update_yaxes(title_text="MACD", row=4, col=1, gridcolor="#1a1a2e")
    fig.update_xaxes(gridcolor="#1a1a2e", showgrid=True)

    return fig


def _add_hline(fig, value: float | None, label: str, color: str, dash: str) -> None:
    """Grafik üzerine etiketli yatay çizgi ekle."""
    if value is None or value <= 0:
        return
    fig.add_hline(
        y=value,
        line_dash=dash,
        line_color=color,
        line_width=1.2,
        annotation_text=f" {label}: {value:,.2f}",
        annotation_font=dict(color=color, size=10),
        annotation_position="right",
        row=1,
        col=1,
    )


def _parse_price(exit_line: str) -> float | None:
    """
    Exit guide satırından fiyat değerini ayıkla.
    Örnek: "Stop loss : 268.24 — exit..."  →  268.24
    """
    try:
        for part in exit_line.split():
            cleaned = part.replace(",", "").replace("$", "")
            val = float(cleaned)
            if val > 0:
                return val
    except Exception:
        pass
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GERİYE DÖNÜK TEST EKİTİ EĞRİSİ / BACKTEST EQUITY CURVE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def compute_equity_curve(
    data: pd.DataFrame, initial_cash: float = 1000.0
) -> pd.DataFrame:
    """Strateji ve Al&Tut portföy değerlerini zaman içinde hesapla."""
    cash, units = initial_cash, 0.0
    first_price = float(data.iloc[0]["close"])
    bnh_units = initial_cash / first_price

    rows = []
    for date, row in data.iterrows():
        sig = signal_for_row(row)
        price = float(row["close"])
        trade = None

        if sig == "BUY" and cash > 0:
            units = cash / price
            cash = 0.0
            trade = "BUY"
        elif sig == "SELL" and units > 0:
            cash = units * price
            units = 0.0
            trade = "SELL"

        rows.append(
            {
                "date": date,
                "strategy": cash + units * price,
                "buy_and_hold": bnh_units * price,
                "trade": trade,
                "price": price,
            }
        )
    return pd.DataFrame(rows).set_index("date")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KENAR ÇUBUĞU / SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("# 📈 Profit AI")
    st.divider()

    lang_code = st.radio(
        "🌐 Language / Dil",
        ["en", "tr"],
        format_func=lambda x: "English" if x == "en" else "Türkçe",
        horizontal=True,
    )
    lang = Lang(lang_code)

    st.divider()

    page_labels = {
        "analysis": "🔍 " + ("Analysis" if lang_code == "en" else "Analiz"),
        "scan": "📡 " + ("Market Scan" if lang_code == "en" else "Piyasa Taraması"),
        "backtest": "📜 " + ("Backtest" if lang_code == "en" else "Geriye Dönük Test"),
    }
    page_key = st.radio(
        "📄 " + ("Page" if lang_code == "en" else "Sayfa"),
        list(page_labels.keys()),
        format_func=lambda k: page_labels[k],
    )

    st.divider()

    asset_type = st.radio(
        "💹 " + ("Market Type" if lang_code == "en" else "Piyasa Türü"),
        ["stock", "crypto"],
        format_func=lambda x: (
            ("Stock 📈" if lang_code == "en" else "Hisse Senedi 📈")
            if x == "stock"
            else ("Crypto 🪙" if lang_code == "en" else "Kripto Para 🪙")
        ),
        horizontal=True,
    )

    # ── Sembol seçici ──────────────────────────────────────────────────────
    CUSTOM_KEY = "__custom__"
    custom_label = "✏️  " + (
        "Custom symbol / Manuel giriş" if lang_code == "en" else "Manuel sembol gir"
    )

    if asset_type == "stock":
        catalog = STOCK_CATALOG
        custom_placeholder = "e.g. ORCL, IBM, SHOP, THYAO.IS"
        custom_help = (
            "Yahoo Finance ticker. Turkish stocks: add .IS suffix (e.g. THYAO.IS)"
            if lang_code == "en"
            else "Yahoo Finance kodu. Türk hisseleri için .IS ekle (örn. THYAO.IS)"
        )
    else:
        catalog = CRYPTO_CATALOG
        custom_placeholder = "e.g. bitcoin, ethereum, solana"
        custom_help = (
            "CoinGecko coin ID — full lowercase name, not the ticker"
            if lang_code == "en"
            else "CoinGecko coin ID — küçük harfle tam isim, kısaltma değil"
        )

    options_map = {k: f"{k.replace('.IS', '')}  —  {v}" for k, v in catalog.items()}
    options_map[CUSTOM_KEY] = custom_label
    sel_label = "🔎 " + ("Symbol" if lang_code == "en" else "Sembol")

    selected_key = st.selectbox(
        sel_label,
        list(options_map.keys()),
        format_func=lambda k: options_map[k],
    )

    if selected_key == CUSTOM_KEY:
        symbol = st.text_input(
            "🔎 " + ("Enter symbol" if lang_code == "en" else "Sembol gir"),
            placeholder=custom_placeholder,
            help=custom_help,
        ).strip()
    else:
        symbol = selected_key
        st.caption(f"📌 {catalog[selected_key]}")

    if asset_type == "stock":
        period_opts = {
            "1 ay / 1mo": "1mo",
            "3 ay / 3mo": "3mo",
            "6 ay / 6mo": "6mo",
            "1 yıl / 1y": "1y",
            "2 yıl / 2y": "2y",
        }
        period_label = st.selectbox(
            "📅 " + ("Period" if lang_code == "en" else "Dönem"),
            list(period_opts.keys()),
            index=2,
        )
        period = period_opts[period_label]
        days = 180
    else:
        period = "6mo"
        days_opt = {
            "30 " + ("days" if lang_code == "en" else "gün"): 30,
            "90 " + ("days" if lang_code == "en" else "gün"): 90,
            "180 " + ("days" if lang_code == "en" else "gün"): 180,
            "365 " + ("days" if lang_code == "en" else "gün"): 365,
        }
        days_label = st.selectbox(
            "📅 " + ("History" if lang_code == "en" else "Geçmiş"),
            list(days_opt.keys()),
            index=2,
        )
        days = days_opt[days_label]

    st.divider()
    analyze_btn = st.button(
        "🔍 " + ("ANALYZE" if lang_code == "en" else "ANALİZ ET"),
        use_container_width=True,
        type="primary",
    )

    st.divider()
    st.markdown(
        f"<div class='disclaimer'>{lang.t('disclaimer').capitalize()}.</div>",
        unsafe_allow_html=True,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SESSION STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "result" not in st.session_state:
    st.session_state.result = None

if analyze_btn and symbol:
    # Hisseleri büyük harf, kriptoları küçük harf yap
    sym_normalized = symbol.upper() if asset_type == "stock" else symbol.lower()

    with st.spinner(
        f"⏳ {'Fetching' if lang_code == 'en' else 'Veri alınıyor'}: {sym_normalized}..."
    ):
        try:
            raw, data = fetch_and_process(asset_type, sym_normalized, period, days)
            insight = build_insights(data)
            rec = build_recommendation(insight, lang)
            st.session_state.result = {
                "raw": raw,
                "data": data,
                "insight": insight,
                "rec": rec,
                "symbol": sym_normalized,
                "asset_type": asset_type,
                "lang_code": lang_code,
            }
        except Exception as e:
            _show_not_found_error(str(e), sym_normalized, asset_type, lang_code)
            st.session_state.result = None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA: ANALİZ / ANALYSIS PAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if page_key == "analysis":
    if st.session_state.result is None:
        _render_welcome(lang, lang_code)
        st.stop()

    R = st.session_state.result
    insight = R["insight"]
    rec = R["rec"]
    data = R["data"]
    sym = R["symbol"].upper()
    atype = R["asset_type"]

    translated_signal = lang.signal(insight.signal)
    sig_color = SIGNAL_COLORS.get(translated_signal, "#888")
    sig_cls = translated_signal.replace(" ", "-")

    # ── Başlık satırı ─────────────────────────────────────────────────────
    arrow = "▲" if insight.change_1d_pct >= 0 else "▼"
    chg_color = "#4CAF50" if insight.change_1d_pct >= 0 else "#e53935"
    st.markdown(
        f"## {sym} "
        f"<span style='font-size:1rem;color:#888;'>({atype.upper()})</span>"
        f"&nbsp;&nbsp;<span style='font-size:1.2rem;font-weight:700;'>"
        f"{insight.close:,.2f}</span>"
        f"&nbsp;<span style='color:{chg_color};font-size:1rem;'>"
        f"{arrow} {insight.change_1d_pct:+.2f}%</span>",
        unsafe_allow_html=True,
    )

    # ── 4 metrik kartı ────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
        <div class="card card-blue">
            <div class="card-title">{lang.t("price_label")}</div>
            <div class="card-value">{insight.close:,.2f}</div>
            <div class="card-sub">{arrow} {insight.change_1d_pct:+.2f}% (24h) &nbsp;|&nbsp;
                {("▲" if insight.change_7d_pct >= 0 else "▼")} {insight.change_7d_pct:+.2f}% (7d)</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
        <div class="card" style="border-left-color:{sig_color}">
            <div class="card-title">{lang.t("signal_header")}</div>
            <div class="card-value">
                <span class="signal-pill sig-{sig_cls}">{translated_signal}</span>
            </div>
            <div class="card-sub">{lang.t("opportunity_label")}: {insight.opportunity_score}/100</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with c3:
        rsi_color = (
            "#e53935"
            if insight.rsi_14 > 70
            else "#4CAF50"
            if insight.rsi_14 < 30
            else "#FF9800"
        )
        st.markdown(
            f"""
        <div class="card" style="border-left-color:{rsi_color}">
            <div class="card-title">RSI 14</div>
            <div class="card-value">{insight.rsi_14:.1f}</div>
            <div class="card-sub">{lang.rsi_lbl(insight.rsi_label)}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
        <div class="card card-orange">
            <div class="card-title">{lang.t("volume_label")}</div>
            <div class="card-value">{insight.volume_ratio:.1f}x</div>
            <div class="card-sub">{lang.volume_lbl(insight.volume_label)}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ── Ana grafik ─────────────────────────────────────────────────────────
    chart = build_chart(data, insight, rec, sym, atype, lang)
    st.plotly_chart(chart, use_container_width=True)

    # ── Sekmeler: Başlangıç / Profesyonel ────────────────────────────────
    beg_lbl = "🟢 " + ("Beginner" if lang_code == "en" else "Başlangıç")
    pro_lbl = "📊 " + ("Professional" if lang_code == "en" else "Profesyonel")
    tab_beg, tab_pro = st.tabs([beg_lbl, pro_lbl])

    # ══════════════════════════════════════════════════════════════════════
    #  BAŞLANGIÇ SEKMESİ
    # ══════════════════════════════════════════════════════════════════════
    with tab_beg:
        bdata = BEGINNER[lang_code][insight.signal]
        sig_emoji = SIGNAL_EMOJIS.get(translated_signal, "⚪")

        # Büyük sinyal göstergesi
        st.markdown(
            f"""
        <div class="big-signal">
            <div class="big-emoji">{sig_emoji}</div>
            <div class="big-text" style="color:{sig_color};">{translated_signal}</div>
            <div style="font-size:1rem;color:#aaa;">{bdata["headline"]}</div>
        </div>""",
            unsafe_allow_html=True,
        )

        st.divider()

        # Açıklama
        explain_lbl = (
            "What does this mean?" if lang_code == "en" else "Bu ne anlama geliyor?"
        )
        st.markdown(f"**{explain_lbl}**")
        st.markdown(bdata["explain"])

        st.divider()

        # ── Senaryolar ────────────────────────────────────────────────────
        # Recommendation'dan değerleri al
        stop_loss_val = _parse_price(rec.exit_guide[0]) or 0
        tp1_val = _parse_price(rec.exit_guide[1]) or 0
        tp2_val = _parse_price(rec.exit_guide[2]) or 0

        tp1_pct = (tp1_val - insight.close) / insight.close * 100 if tp1_val else 0
        sl_pct = (
            (insight.close - stop_loss_val) / insight.close * 100
            if stop_loss_val
            else 0
        )

        sc_lbl = (
            "Scenarios — What Could Happen?"
            if lang_code == "en"
            else "Senaryolar — Neler Olabilir?"
        )
        st.markdown(f"**{sc_lbl}**")
        col_bull, col_bear = st.columns(2)

        with col_bull:
            bull_items = [
                f"• {'Price bounces from' if lang_code == 'en' else 'Fiyat destek seviyesinden'} {insight.sma_20:,.0f} {'and rises' if lang_code == 'en' else 'seker'}",
                f"• {'Target 1' if lang_code == 'en' else 'Hedef 1'}: <b>{tp1_val:,.2f}</b> (+{tp1_pct:.1f}%)",
                f"• {'Target 2' if lang_code == 'en' else 'Hedef 2'}: <b>{tp2_val:,.2f}</b>",
            ]
            st.markdown(
                f"""
            <div class="bull-card">
                <div class="scenario-title">{bdata["bull_title"]}</div>
                {"".join(f'<div class="scenario-row">{i}</div>' for i in bull_items)}
            </div>""",
                unsafe_allow_html=True,
            )

        with col_bear:
            bear_items = [
                f"• {'Price breaks below' if lang_code == 'en' else 'Fiyat destek kırar'}: {insight.bb_lower:,.0f}",
                f"• {'Stop Loss activates' if lang_code == 'en' else 'Zarar Kes devreye girer'}: <b>{stop_loss_val:,.2f}</b>",
                f"• {'Max loss' if lang_code == 'en' else 'Maksimum kayıp'}: <b>-{sl_pct:.1f}%</b>",
            ]
            st.markdown(
                f"""
            <div class="bear-card">
                <div class="scenario-title">{bdata["bear_title"]}</div>
                {"".join(f'<div class="scenario-row">{i}</div>' for i in bear_items)}
            </div>""",
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Adımlar ───────────────────────────────────────────────────────
        st.markdown(f"**{bdata['steps_title']}**")
        for icon, text in bdata["steps"]:
            st.markdown(
                f"""
            <div class="step">
                <span class="step-icon">{icon}</span>
                <span class="step-body">{text}</span>
            </div>""",
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Fiyat konumu göstergesi ────────────────────────────────────────
        pos = float(data.iloc[-1].get("price_position_52w", 0.5))
        pos_pct = max(2, min(98, int(pos * 100)))
        pos_lbl = (
            "Price Position (52-week range)"
            if lang_code == "en"
            else "Fiyat Konumu (52 haftalık aralık)"
        )
        st.markdown(f"**{pos_lbl}**")
        st.markdown(
            f"""
        <div class="gauge-wrap">
            <div class="gauge-label">
                <span>📉 {insight.low_52w:,.0f} (Low)</span>
                <span>📈 {insight.high_52w:,.0f} (High)</span>
            </div>
            <div class="gauge-bar">
                <div class="gauge-dot" style="left:{pos_pct}%;"></div>
            </div>
            <div style="text-align:center;font-size:.8rem;color:#aaa;margin-top:6px;">
                ↑ {"Current" if lang_code == "en" else "Şu an"}: {insight.close:,.2f} ({pos_pct}%)
            </div>
        </div>""",
            unsafe_allow_html=True,
        )

        # Önemli olaylar
        if insight.events:
            st.divider()
            events_lbl = (
                "Key Events Detected"
                if lang_code == "en"
                else "Tespit Edilen Önemli Olaylar"
            )
            st.markdown(f"**{events_lbl}**")
            for key, params in insight.events:
                st.info(f"⚡ {lang.event(key, params)}")

        st.markdown(
            f"<div class='disclaimer'>{lang.t('disclaimer').capitalize()}.</div>",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════
    #  PROFESYONEL SEKMESİ
    # ══════════════════════════════════════════════════════════════════════
    with tab_pro:
        pcol1, pcol2 = st.columns([1, 1])

        # ── Sol: Tüm göstergeler tablosu ─────────────────────────────────
        with pcol1:
            ind_lbl = (
                "Indicator Readings" if lang_code == "en" else "Gösterge Değerleri"
            )
            st.markdown(f"**{ind_lbl}**")

            rows_html = [
                (lang.t("price_label"), f"{insight.close:,.2f}"),
                (lang.t("change_1d"), f"{insight.change_1d_pct:+.2f}%"),
                (lang.t("change_7d"), f"{insight.change_7d_pct:+.2f}%"),
                (
                    lang.t("week52_high"),
                    f"{insight.high_52w:,.2f}  ({insight.pct_from_high:.1f}%)",
                ),
                (lang.t("week52_low"), f"{insight.low_52w:,.2f}"),
                (lang.t("trend_label"), f"{lang.trend(insight.trend)}"),
                ("SMA 20", f"{insight.sma_20:,.2f}"),
                ("SMA 50", f"{insight.sma_50:,.2f}"),
                (
                    "RSI 14",
                    f"{insight.rsi_14:.1f}  [{lang.rsi_lbl(insight.rsi_label)}]",
                ),
                (lang.t("bollinger_label"), lang.bb_lbl(insight.bb_position_label)),
                (
                    lang.t("volume_label"),
                    f"{insight.volume_ratio:.1f}x  [{lang.volume_lbl(insight.volume_label)}]",
                ),
                (
                    lang.t("position52w_label"),
                    lang.position_lbl(insight.price_position_label),
                ),
                (lang.t("signal_header"), lang.signal(insight.signal)),
                (lang.t("opportunity_label"), f"{insight.opportunity_score}/100"),
            ]

            trs = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows_html)
            st.markdown(
                f'<table class="ind-table">{trs}</table>',
                unsafe_allow_html=True,
            )

        # ── Sağ: Öneri özeti ──────────────────────────────────────────────
        with pcol2:
            rec_lbl = lang.t("rec_header")
            st.markdown(f"**{rec_lbl}**")

            st.markdown(
                f"""
            <div class="card" style="border-left-color:{sig_color}">
                <div class="card-title">{lang.t("rec_action_label")}</div>
                <div class="card-value" style="font-size:1rem;">{rec.action}</div>
            </div>""",
                unsafe_allow_html=True,
            )

            st.caption(rec.reasoning)

        st.divider()

        # ── Anahtar fiyat seviyeleri ───────────────────────────────────────
        kl_lbl = lang.t("rec_levels_label")
        st.markdown(f"**{kl_lbl}**")
        kl_cols = st.columns(2)
        for i, level in enumerate(rec.key_levels):
            with kl_cols[i % 2]:
                st.markdown(f"• {level}")

        st.divider()

        # ── Giriş planı ───────────────────────────────────────────────────
        ep_lbl = lang.t("rec_entry_label")
        st.markdown(f"**{ep_lbl}**")
        for line in rec.entry_plan.split("\n"):
            if line.strip():
                st.markdown(f"  {line}")

        st.divider()

        # ── Çıkış rehberi ─────────────────────────────────────────────────
        ex_lbl = lang.t("rec_exit_label")
        st.markdown(f"**{ex_lbl}**")
        ec1, ec2 = st.columns(2)
        for i, line in enumerate(rec.exit_guide):
            with ec1 if i % 2 == 0 else ec2:
                if line.strip():
                    st.markdown(f"• {line}")

        st.divider()

        # ── Dikkat edilecekler ────────────────────────────────────────────
        ww_lbl = lang.t("rec_watch_label")
        st.markdown(f"**{ww_lbl}**")
        wc1, wc2 = st.columns(2)
        for i, item in enumerate(rec.what_to_watch):
            with wc1 if i % 2 == 0 else wc2:
                st.markdown(f"• {item}")

        st.divider()

        # ── Riskler ───────────────────────────────────────────────────────
        risk_lbl = lang.t("rec_risks_label")
        st.markdown(f"**{risk_lbl}**")
        for risk in rec.risks:
            st.warning(f"⚠️ {risk}")

        st.markdown(
            f"<div class='disclaimer'>{lang.t('final_disclaimer')}</div>",
            unsafe_allow_html=True,
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA: PİYASA TARAMASI / MARKET SCAN PAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page_key == "scan":
    title = "📡 Market Scan" if lang_code == "en" else "📡 Piyasa Taraması"
    st.markdown(f"## {title}")
    desc = (
        "Scans your watchlist and ranks by opportunity score."
        if lang_code == "en"
        else "İzleme listenizdeki tüm sembolleri tarar ve fırsat puanına göre sıralar."
    )
    st.markdown(desc)

    scan_btn = st.button(
        "🚀 " + ("Scan Now" if lang_code == "en" else "Şimdi Tara"),
        type="primary",
    )

    if scan_btn:
        symbols = DEFAULT_STOCKS if asset_type == "stock" else DEFAULT_CRYPTO
        progress = st.progress(
            0, text="Scanning..." if lang_code == "en" else "Taranıyor..."
        )

        results = []
        for i, sym_s in enumerate(symbols):
            progress.progress(
                (i + 1) / len(symbols),
                text=f"{'Scanning' if lang_code == 'en' else 'Tarıyor'}: {sym_s.upper()}",
            )
            try:
                _, d = fetch_and_process(asset_type, sym_s.lower(), "6mo", 180)
                ins = build_insights(d)
                results.append({"symbol": sym_s.upper(), "insight": ins})
            except Exception:
                pass

        progress.empty()

        if not results:
            st.error("No data returned." if lang_code == "en" else "Veri alınamadı.")
            st.stop()

        # Tablo oluştur
        table_rows = []
        for r in results:
            ins = r["insight"]
            sig_tr = lang.signal(ins.signal)
            table_rows.append(
                {
                    lang.t("scan_col_symbol"): r["symbol"],
                    lang.t("scan_col_signal"): sig_tr,
                    lang.t("scan_col_score"): ins.opportunity_score,
                    lang.t("scan_col_price"): ins.close,
                    lang.t("scan_col_24h"): round(ins.change_1d_pct, 2),
                    "RSI": round(ins.rsi_14, 1),
                    lang.t("scan_col_trend"): lang.trend(ins.trend),
                }
            )

        # Fırsat puanına göre sırala
        df_scan = pd.DataFrame(table_rows).sort_values(
            lang.t("scan_col_score"), ascending=False
        )

        # Sinyal sütununu renkli göster
        def color_signal(val: str):
            c = SIGNAL_COLORS.get(val, "#888")
            return f"background-color:{c}22; color:{c}; font-weight:700;"

        styled = df_scan.style.map(color_signal, subset=[lang.t("scan_col_signal")])
        st.dataframe(styled, use_container_width=True, hide_index=True)

        # En iyi fırsatlar
        top = [r for r in results if r["insight"].signal in ("STRONG BUY", "BUY")]
        if top:
            top_lbl = f"🏆 {lang.t('scan_top')} ({len(top)})"
            st.markdown(f"### {top_lbl}")
            for r in top:
                ins = r["insight"]
                sig_c = SIGNAL_COLORS.get(lang.signal(ins.signal), "#4CAF50")
                sig_tr = lang.signal(ins.signal)
                with st.expander(
                    f"{r['symbol']}  —  {sig_tr}  ({ins.opportunity_score}/100)"
                ):
                    st.markdown(
                        f"<span class='signal-pill sig-{sig_tr.replace(' ', '-')}'>"
                        f"{sig_tr}</span>",
                        unsafe_allow_html=True,
                    )
                    for key, params in ins.events[:4]:
                        st.markdown(f"• {lang.event(key, params)}")
        else:
            st.info(lang.t("scan_none"))

        st.markdown(
            f"<div class='disclaimer'>{lang.t('disclaimer').capitalize()}.</div>",
            unsafe_allow_html=True,
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SAYFA: GERİYE DÖNÜK TEST / BACKTEST PAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page_key == "backtest":
    title = "📜 Backtest" if lang_code == "en" else "📜 Geriye Dönük Test"
    st.markdown(f"## {title}")
    desc = (
        "See how this strategy would have performed on historical data. "
        "**Does not guarantee future results.**"
        if lang_code == "en"
        else "Bu stratejinin geçmiş verilerde nasıl performans gösterdiğini gör. "
        "**Gelecekteki sonuçları garanti etmez.**"
    )
    st.markdown(desc)

    cash_label = "Starting cash ($)" if lang_code == "en" else "Başlangıç parası ($)"
    initial_cash = st.number_input(
        cash_label, min_value=100.0, value=1000.0, step=100.0
    )

    run_btn = st.button(
        "▶️ " + ("Run Backtest" if lang_code == "en" else "Testi Başlat"),
        type="primary",
    )

    if run_btn:
        if not symbol:
            st.warning(
                "Please enter a symbol." if lang_code == "en" else "Lütfen sembol gir."
            )
            st.stop()

        with st.spinner("⏳"):
            try:
                _, data_bt = fetch_and_process(asset_type, symbol.lower(), period, days)
                bt_result = run_backtest(data_bt, initial_cash=initial_cash)
                equity_df = compute_equity_curve(data_bt, initial_cash)
            except Exception as e:
                st.error(f"❌ {e}")
                st.stop()

        bnh_ret = (bt_result.buy_and_hold_value - initial_cash) / initial_cash * 100

        # Metrikler
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(lang.t("bt_starting_cash"), f"${initial_cash:,.0f}")
        m2.metric(
            lang.t("bt_strategy_value"),
            f"${bt_result.final_value:,.2f}",
            f"{bt_result.profit_percent:+.2f}%",
        )
        m3.metric(
            lang.t("bt_bnh_value"),
            f"${bt_result.buy_and_hold_value:,.2f}",
            f"{bnh_ret:+.2f}%",
        )
        m4.metric(lang.t("bt_trades"), str(bt_result.trades))

        # Eşitlik eğrisi grafiği
        fig_bt = go.Figure()

        fig_bt.add_trace(
            go.Scatter(
                x=equity_df.index,
                y=equity_df["strategy"],
                name="Strategy" if lang_code == "en" else "Strateji",
                line=dict(color="#4CAF50", width=2.5),
                fill="tozeroy",
                fillcolor="rgba(76,175,80,0.08)",
            )
        )

        fig_bt.add_trace(
            go.Scatter(
                x=equity_df.index,
                y=equity_df["buy_and_hold"],
                name="Buy & Hold" if lang_code == "en" else "Al ve Tut",
                line=dict(color="#42a5f5", width=2, dash="dot"),
            )
        )

        # Alım/Satım işaretleri
        buys = equity_df[equity_df["trade"] == "BUY"]
        sells = equity_df[equity_df["trade"] == "SELL"]

        if not buys.empty:
            fig_bt.add_trace(
                go.Scatter(
                    x=buys.index,
                    y=buys["strategy"],
                    mode="markers",
                    name="BUY",
                    marker=dict(symbol="triangle-up", size=12, color="#4CAF50"),
                )
            )
        if not sells.empty:
            fig_bt.add_trace(
                go.Scatter(
                    x=sells.index,
                    y=sells["strategy"],
                    mode="markers",
                    name="SELL",
                    marker=dict(symbol="triangle-down", size=12, color="#e53935"),
                )
            )

        fig_bt.add_hline(
            y=initial_cash,
            line_dash="dot",
            line_color="#888",
            annotation_text="Starting capital" if lang_code == "en" else "Başlangıç",
            annotation_position="left",
        )

        fig_bt.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            height=420,
            hovermode="x unified",
            legend=dict(orientation="h", x=0, y=1.02, bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=30, b=10),
            yaxis_title="Portfolio Value ($)",
            font=dict(color="#ccc"),
        )
        st.plotly_chart(fig_bt, use_container_width=True)

        # Kazanan kim?
        if bt_result.final_value > bt_result.buy_and_hold_value:
            diff = bt_result.final_value - bt_result.buy_and_hold_value
            msg = (
                f"✅ Strategy beat Buy & Hold by **${diff:,.2f}**"
                if lang_code == "en"
                else f"✅ Strateji, Al ve Tut'u **${diff:,.2f}** farkla geçti"
            )
            st.success(msg)
        else:
            diff = bt_result.buy_and_hold_value - bt_result.final_value
            msg = (
                f"ℹ️ Buy & Hold was better by **${diff:,.2f}**"
                if lang_code == "en"
                else f"ℹ️ Al ve Tut, stratejiyi **${diff:,.2f}** farkla geçti"
            )
            st.info(msg)

        st.caption(lang.t("bt_note"))
