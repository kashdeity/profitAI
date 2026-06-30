"""
i18n.py — Internationalization (translation) module.

Supports English ("en") and Turkish ("tr").

How it works:
- All user-visible text lives here as dictionaries keyed by language code.
- The Lang class wraps these dicts and exposes helper methods.
- Call lang.t("some_key") for static strings.
- Call lang.signal("BUY"), lang.trend("UPTREND"), etc. for coded values.
- Call lang.event("golden_cross", {"rsi": 22.3}) for dynamic event messages.
- Call lang.rec_*() methods for recommendation section text.

To add a new language, copy the "en" block, translate the values, and add the
code to SUPPORTED_LANGS.
"""

from __future__ import annotations

SUPPORTED_LANGS = {"en": "English", "tr": "Türkçe"}

# ── Static UI strings ──────────────────────────────────────────────────────────

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        # App
        "app_name": "Profit AI",
        "disclaimer": "educational analysis only — not financial advice",
        "final_disclaimer": (
            "This is automated rule-based analysis, not financial advice.\n"
            "  Always do your own research and only risk what you can afford to lose."
        ),
        # Language prompt
        "choose_language": "Choose your language / Dilinizi seçin:",
        # Menu
        "menu_title": "MAIN MENU",
        "menu_1": "Analyze a stock or crypto",
        "menu_2": "Scan the market  (multiple symbols at once)",
        "menu_3": "Backtest a strategy",
        "menu_4": "Help  (?help)",
        "menu_5": "Exit",
        "menu_prompt": "Your choice",
        "invalid_choice": "Invalid choice — please enter a number from the menu.",
        # Input prompts
        "enter_type": "Market type  [stock / crypto]",
        "enter_symbol_stock": "Stock ticker  (e.g. AAPL, TSLA, NVDA, MSFT)",
        "enter_symbol_crypto": "Crypto name  (e.g. bitcoin, ethereum, solana)",
        "enter_period": "History period  [1mo / 3mo / 6mo / 1y / 2y]  (default: 6mo)",
        "enter_days": "Days of history  (default: 180)",
        "enter_cash": "Starting paper cash  (default: 1000)",
        "type_error": "Please type 'stock' or 'crypto'.",
        "fetching": "Fetching data for {symbol}...",
        "scanning": "Scanning {n} {asset_type} symbols. Please wait...",
        "press_enter": "Press Enter to return to the menu...",
        "error_prefix": "Error",
        # Analysis section headers
        "analysis_title": "Profit AI Analysis",
        "signal_header": "SIGNAL",
        "opportunity_label": "Opportunity",
        "events_header": "KEY EVENTS & OPPORTUNITIES",
        "summary_label": "SUMMARY",
        # Price row labels
        "price_label": "Price",
        "change_1d": "24h change",
        "change_7d": "7d change",
        "week52_high": "52w high",
        "week52_low": "52w low",
        "pct_from_here": "from here",
        "pct_above_low": "above low",
        "trend_label": "Trend",
        "detail_label": "Detail",
        "rsi_label": "RSI 14",
        "bollinger_label": "Bollinger",
        "volume_label": "Volume",
        "vol_avg": "avg",
        "position52w_label": "52w position",
        # Scan
        "scan_header": "MARKET SCAN — Ranked by Opportunity",
        "scan_col_symbol": "Symbol",
        "scan_col_signal": "Signal",
        "scan_col_score": "Score",
        "scan_col_price": "Price",
        "scan_col_24h": "24h",
        "scan_col_rsi": "RSI",
        "scan_col_trend": "Trend",
        "scan_top": "TOP OPPORTUNITIES",
        "scan_none": "No strong buy signals found at the moment.",
        "scan_symbols": "symbols",
        # Backtest
        "backtest_title": "Paper Backtest Results",
        "bt_starting_cash": "Starting cash",
        "bt_strategy_value": "Strategy end value",
        "bt_profit_loss": "Profit / Loss",
        "bt_return": "Return",
        "bt_trades": "Trades made",
        "bt_bnh_value": "Buy & Hold value",
        "bt_bnh_return": "Buy & Hold return",
        "bt_strategy_beat": "Strategy BEAT buy & hold by",
        "bt_bnh_beat": "Buy & hold was better by",
        "bt_note": (
            "Backtest ignores fees, taxes, slippage, and real-world execution.\n"
            "  A strategy that looks good historically may not work in the future."
        ),
        # Recommendation section headers
        "rec_header": "AI RECOMMENDATION",
        "rec_action_label": "ACTION",
        "rec_why_label": "WHY",
        "rec_entry_label": "ENTRY PLAN",
        "rec_levels_label": "KEY PRICE LEVELS",
        "rec_exit_label": "EXIT GUIDE  (stop loss & take profit)",
        "rec_watch_label": "WHAT TO WATCH",
        "rec_risks_label": "RISKS TO BE AWARE OF",
        "final_disclaimer_label": "FINAL DISCLAIMER",
        # Help
        "help_header": "HELP — Profit AI",
        "help_body": """
  This program downloads real market prices and analyzes them with
  technical indicators. It then gives you a plain-English recommendation
  for what you might do — but it does NOT trade for you.

  HOW TO USE:
  Run  python -m profit_ai  with no arguments to open this menu.

  MENU OPTIONS:
  1. Analyze   — Deep analysis of one stock or crypto symbol.
  2. Scan      — Scan all symbols on your watchlist and rank by opportunity.
  3. Backtest  — Simulate how the strategy would have performed in the past.
  4. Help      — This screen.
  5. Exit      — Close the program.

  WHAT THE SIGNALS MEAN:
  STRONG BUY  — Multiple strong bullish signals at once. Rare — pay attention.
  BUY         — More bullish than bearish signals. Cautious entry possible.
  HOLD        — Mixed signals. Better to wait for clarity.
  SELL        — More bearish than bullish. Avoid new entries.
  STRONG SELL — Multiple strong bearish signals. High downside risk.

  KEY TERMS:
  RSI         — Momentum indicator. Below 30 = oversold (possible bounce).
                Above 70 = overbought (possible pullback).
  SMA 20/50   — Moving averages showing the trend direction.
                Price above both = uptrend. Price below both = downtrend.
  MACD        — Momentum indicator. Crossover up = bullish, down = bearish.
  Bollinger   — Volatility bands. Lower band = oversold. Upper = overbought.
  Support     — Price floor where buyers tend to step in.
  Resistance  — Price ceiling where sellers tend to push back.
  Stop Loss   — The price where you exit to limit your losses.
  Take Profit — The price where you exit to lock in your gains.
  DCA         — Dollar Cost Averaging. Buying in multiple small portions
                instead of all at once. Reduces timing risk.
  Risk/Reward — How much you could gain vs. how much you risk.
                Aim for at least 2:1 (gain $2 for every $1 risked).

  IMPORTANT:
  This tool is for education only. Always do your own research.
  Never invest money you cannot afford to lose completely.
""",
    },
    "tr": {
        # App
        "app_name": "Kâr AI",
        "disclaimer": "yalnızca eğitim amaçlı — yatırım tavsiyesi değildir",
        "final_disclaimer": (
            "Bu otomatik kural tabanlı bir analizdir, yatırım tavsiyesi değildir.\n"
            "  Her zaman kendi araştırmanızı yapın ve kaybetmeyi göze alamayacağınız parayı riske atmayın."
        ),
        # Language prompt
        "choose_language": "Choose your language / Dilinizi seçin:",
        # Menu
        "menu_title": "ANA MENÜ",
        "menu_1": "Bir hisse senedi veya kripto analiz et",
        "menu_2": "Piyasayı tara  (birden fazla sembol aynı anda)",
        "menu_3": "Stratejiyi geriye dönük test et",
        "menu_4": "Yardım  (?yardım)",
        "menu_5": "Çıkış",
        "menu_prompt": "Seçiminiz",
        "invalid_choice": "Geçersiz seçim — lütfen menüden bir numara girin.",
        # Input prompts
        "enter_type": "Piyasa türü  [stock / crypto]",
        "enter_symbol_stock": "Hisse kodu  (örn. AAPL, TSLA, NVDA, MSFT)",
        "enter_symbol_crypto": "Kripto adı  (örn. bitcoin, ethereum, solana)",
        "enter_period": "Geçmiş dönemi  [1mo / 3mo / 6mo / 1y / 2y]  (varsayılan: 6mo)",
        "enter_days": "Geçmiş gün sayısı  (varsayılan: 180)",
        "enter_cash": "Başlangıç kağıt parası  (varsayılan: 1000)",
        "type_error": "Lütfen 'stock' veya 'crypto' yazın.",
        "fetching": "{symbol} için veri alınıyor...",
        "scanning": "{n} {asset_type} sembolü taranıyor. Lütfen bekleyin...",
        "press_enter": "Menüye dönmek için Enter'a basın...",
        "error_prefix": "Hata",
        # Analysis section headers
        "analysis_title": "Kâr AI Analizi",
        "signal_header": "SİNYAL",
        "opportunity_label": "Fırsat",
        "events_header": "ÖNEMLİ OLAYLAR & FIRSATLAR",
        "summary_label": "ÖZET",
        # Price row labels
        "price_label": "Fiyat",
        "change_1d": "24s değişim",
        "change_7d": "7g değişim",
        "week52_high": "52h yüksek",
        "week52_low": "52h düşük",
        "pct_from_here": "buradan",
        "pct_above_low": "düşük üstünde",
        "trend_label": "Trend",
        "detail_label": "Detay",
        "rsi_label": "RSI 14",
        "bollinger_label": "Bollinger",
        "volume_label": "Hacim",
        "vol_avg": "ort",
        "position52w_label": "52h konum",
        # Scan
        "scan_header": "PİYASA TARAMASI — Fırsata Göre Sıralı",
        "scan_col_symbol": "Sembol",
        "scan_col_signal": "Sinyal",
        "scan_col_score": "Puan",
        "scan_col_price": "Fiyat",
        "scan_col_24h": "24s",
        "scan_col_rsi": "RSI",
        "scan_col_trend": "Trend",
        "scan_top": "EN İYİ FIRSATLAR",
        "scan_none": "Şu an güçlü alım sinyali bulunamadı.",
        "scan_symbols": "sembol",
        # Backtest
        "backtest_title": "Geriye Dönük Kağıt Test Sonuçları",
        "bt_starting_cash": "Başlangıç parası",
        "bt_strategy_value": "Strateji son değeri",
        "bt_profit_loss": "Kâr / Zarar",
        "bt_return": "Getiri",
        "bt_trades": "Yapılan işlem sayısı",
        "bt_bnh_value": "Al ve Tut değeri",
        "bt_bnh_return": "Al ve Tut getirisi",
        "bt_strategy_beat": "Strateji Al ve Tut'u geçti:",
        "bt_bnh_beat": "Al ve Tut daha iyi oldu:",
        "bt_note": (
            "Geriye dönük test; komisyon, vergi, kayma ve gerçek piyasa koşullarını göz ardı eder.\n"
            "  Geçmişte iyi görünen bir strateji gelecekte çalışmayabilir."
        ),
        # Recommendation section headers
        "rec_header": "YAPAY ZEKA TAVSİYESİ",
        "rec_action_label": "EYLEM",
        "rec_why_label": "NEDEN",
        "rec_entry_label": "GİRİŞ PLANI",
        "rec_levels_label": "ÖNEMLİ FİYAT SEVİYELERİ",
        "rec_exit_label": "ÇIKIŞ REHBERİ  (zarar kes & kâr al)",
        "rec_watch_label": "NELERE DİKKAT ET",
        "rec_risks_label": "DİKKAT EDİLMESİ GEREKEN RİSKLER",
        "final_disclaimer_label": "SON UYARI",
        # Help
        "help_header": "YARDIM — Kâr AI",
        "help_body": """
  Bu program gerçek piyasa fiyatlarını indirir ve teknik göstergelerle
  analiz eder. Ardından size ne yapabileceğinize dair Türkçe bir tavsiye
  sunar — ancak sizin adınıza alım satım YAPMAZ.

  NASIL KULLANILIR:
  python -m profit_ai  komutunu argümansız çalıştırarak bu menüyü açın.

  MENÜ SEÇENEKLERİ:
  1. Analiz et  — Tek bir hisse senedi veya kripto için derin analiz.
  2. Tara       — İzleme listenizdeki tüm sembolleri tarayın ve sıralayın.
  3. Geriye dön — Stratejinin geçmişte nasıl performans gösterdiğini simüle edin.
  4. Yardım     — Bu ekran.
  5. Çıkış      — Programı kapat.

  SİNYALLER NE ANLAMA GELİR:
  GÜÇLÜ AL   — Aynı anda birden fazla güçlü yükselen sinyal. Nadir — dikkat edin.
  AL         — Yükselen sinyaller düşenden fazla. Temkinli giriş değerlendirilebilir.
  BEKLE      — Karışık sinyaller. Netlik için beklemeyi tercih edin.
  SAT        — Düşen sinyaller yükselen sinyalden fazla. Yeni giriş yapmayın.
  GÜÇLÜ SAT  — Birden fazla güçlü düşen sinyal. Yüksek aşağı yönlü risk.

  TEMEL KAVRAMLAR:
  RSI         — Momentum göstergesi. 30 altı = aşırı satılmış (olası toparlanma).
                70 üstü = aşırı alınmış (olası geri çekilme).
  SMA 20/50   — Trend yönünü gösteren hareketli ortalamalar.
                Fiyat ikisinin üstünde = yükselen trend. Altında = düşen trend.
  MACD        — Momentum göstergesi. Yukarı geçiş = yükselen, aşağı = düşen.
  Bollinger   — Volatilite bantları. Alt bant = aşırı satılmış. Üst = aşırı alınmış.
  Destek      — Alıcıların devreye girdiği fiyat tabanı.
  Direnç     — Satıcıların baskı yaptığı fiyat tavanı.
  Zarar Kes  — Zararı sınırlamak için çıkış fiyatı.
  Kâr Al     — Kazancı kilitlemek için çıkış fiyatı.
  DCA         — Düzenli Maliyet Ortalaması. Tüm parayı bir kerede değil,
                küçük porsiyonlarda yatırmak. Zamanlama riskini azaltır.
  Risk/Ödül   — Ne kadar kazanabileceğinizin ne kadar kaybedeceğinize oranı.
                En az 2:1 hedefleyin (1 lira riske karşı 2 lira kazanç).

  ÖNEMLİ:
  Bu araç yalnızca eğitim amaçlıdır. Her zaman kendi araştırmanızı yapın.
  Kaybetmeyi göze alamayacağınız para yatırmayın.
""",
    },
}

# ── Coded-value translations ───────────────────────────────────────────────────

SIGNAL_NAMES: dict[str, dict[str, str]] = {
    "en": {
        "STRONG BUY": "STRONG BUY",
        "BUY": "BUY",
        "HOLD": "HOLD",
        "SELL": "SELL",
        "STRONG SELL": "STRONG SELL",
    },
    "tr": {
        "STRONG BUY": "GÜÇLÜ AL",
        "BUY": "AL",
        "HOLD": "BEKLE",
        "SELL": "SAT",
        "STRONG SELL": "GÜÇLÜ SAT",
    },
}

TREND_NAMES: dict[str, dict[str, str]] = {
    "en": {
        "UPTREND": "UPTREND",
        "RECOVERING": "RECOVERING",
        "DOWNTREND": "DOWNTREND",
        "WEAKENING": "WEAKENING",
        "SIDEWAYS": "SIDEWAYS",
    },
    "tr": {
        "UPTREND": "YÜKSELİŞ",
        "RECOVERING": "TOPARLANMA",
        "DOWNTREND": "DÜŞÜŞ",
        "WEAKENING": "ZAYIFLAMA",
        "SIDEWAYS": "YATAY",
    },
}

TREND_DETAILS: dict[str, dict[str, str]] = {
    "en": {
        "UPTREND": "Price > SMA20 > SMA50 — solid uptrend",
        "RECOVERING": "Price above SMA20 but SMA20 still below SMA50 — early recovery",
        "DOWNTREND": "Price < SMA20 < SMA50 — solid downtrend",
        "WEAKENING": "Price below SMA20 but SMA20 still above SMA50 — trend weakening",
        "SIDEWAYS": "No clear directional trend",
    },
    "tr": {
        "UPTREND": "Fiyat > SMA20 > SMA50 — sağlam yükselen trend",
        "RECOVERING": "Fiyat SMA20 üzerinde ama SMA20 hâlâ SMA50 altında — erken toparlanma",
        "DOWNTREND": "Fiyat < SMA20 < SMA50 — sağlam düşen trend",
        "WEAKENING": "Fiyat SMA20 altında ama SMA20 hâlâ SMA50 üzerinde — trend zayıflıyor",
        "SIDEWAYS": "Net bir yön trendi yok",
    },
}

SUMMARIES: dict[str, dict[str, str]] = {
    "en": {
        "STRONG BUY": "Multiple strong bullish signals align. High-potential opportunity — do your own research before acting.",
        "BUY": "More bullish signals than bearish. Looks interesting — confirm with your own research.",
        "HOLD": "Mixed signals. Wait for a clearer setup before acting.",
        "SELL": "More bearish signals than bullish. Risky area to enter.",
        "STRONG SELL": "Multiple strong bearish signals. High risk area — caution advised.",
    },
    "tr": {
        "STRONG BUY": "Birden fazla güçlü yükselen sinyal bir arada. Yüksek potansiyelli fırsat — harekete geçmeden önce kendi araştırmanızı yapın.",
        "BUY": "Yükselen sinyaller düşenden fazla. İlgi çekici görünüyor — kendi araştırmanızla doğrulayın.",
        "HOLD": "Karışık sinyaller. Harekete geçmeden önce daha net bir kurulum bekleyin.",
        "SELL": "Düşen sinyaller yükselen sinyalden fazla. Giriş için riskli bölge.",
        "STRONG SELL": "Birden fazla güçlü düşen sinyal. Yüksek riskli bölge — dikkat edin.",
    },
}

RSI_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "extreme_oversold": "EXTREMELY OVERSOLD",
        "oversold": "OVERSOLD",
        "slight_oversold": "Slightly oversold",
        "neutral": "Neutral",
        "slight_overbought": "Slightly overbought",
        "overbought": "OVERBOUGHT",
        "extreme_overbought": "EXTREMELY OVERBOUGHT",
    },
    "tr": {
        "extreme_oversold": "AŞIRI SATILMIŞ (EKSTREM)",
        "oversold": "AŞIRI SATILMIŞ",
        "slight_oversold": "Hafif aşırı satılmış",
        "neutral": "Nötr",
        "slight_overbought": "Hafif aşırı alınmış",
        "overbought": "AŞIRI ALINMIŞ",
        "extreme_overbought": "AŞIRI ALINMIŞ (EKSTREM)",
    },
}

BB_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "below_lower_bb": "BELOW LOWER BAND — extremely oversold, high bounce potential",
        "above_upper_bb": "ABOVE UPPER BAND — extremely overbought, high pullback potential",
        "near_lower_bb": "Near lower Bollinger Band — slightly oversold",
        "near_upper_bb": "Near upper Bollinger Band — slightly overbought",
        "inside_bb": "Inside Bollinger Bands — normal range",
    },
    "tr": {
        "below_lower_bb": "ALT BANDA KIRDI — aşırı satılmış (ekstrem), güçlü toparlanma potansiyeli",
        "above_upper_bb": "ÜST BANDA KIRDI — aşırı alınmış (ekstrem), güçlü geri çekilme potansiyeli",
        "near_lower_bb": "Alt Bollinger Bandına yakın — hafif aşırı satılmış",
        "near_upper_bb": "Üst Bollinger Bandına yakın — hafif aşırı alınmış",
        "inside_bb": "Bollinger Bantları içinde — normal aralık",
    },
}

VOLUME_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "huge_spike": "HUGE VOLUME SPIKE",
        "high": "HIGH VOLUME",
        "very_low": "VERY LOW VOLUME",
        "low": "Low volume",
        "normal": "Normal volume",
    },
    "tr": {
        "huge_spike": "DEV HACİM ARTIŞI",
        "high": "YÜKSEK HACİM",
        "very_low": "ÇOK DÜŞÜK HACİM",
        "low": "Düşük hacim",
        "normal": "Normal hacim",
    },
}

POSITION_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "near_low": "NEAR 52-WEEK LOW",
        "near_high": "NEAR 52-WEEK HIGH",
        "lower_third": "Lower third of 52-week range",
        "upper_third": "Upper third of 52-week range",
        "middle": "Middle of 52-week range",
    },
    "tr": {
        "near_low": "52 HAFTALIK DÜŞÜĞE YAKIN",
        "near_high": "52 HAFTALIK YÜKSEĞE YAKIN",
        "lower_third": "52 haftalık aralığın alt üçte biri",
        "upper_third": "52 haftalık aralığın üst üçte biri",
        "middle": "52 haftalık aralığın ortası",
    },
}

# ── Event templates ────────────────────────────────────────────────────────────
# Each key maps to a format string; params are passed as keyword arguments.

EVENTS: dict[str, dict[str, str]] = {
    "en": {
        "golden_cross": "GOLDEN CROSS detected — SMA20 just crossed above SMA50, historically bullish",
        "death_cross": "DEATH CROSS detected — SMA20 just crossed below SMA50, historically bearish",
        "near_52w_low": "Price is near its 52-week low (only {pct:.1f}% above it) — potential deep value",
        "near_52w_high": "Price is near its 52-week high ({pct:.1f}% below it) — strong momentum but less upside",
        "below_bb_lower": "Price broke below the lower Bollinger Band — historically a strong buy zone",
        "above_bb_upper": "Price broke above the upper Bollinger Band — historically a caution zone",
        "rsi_extreme_oversold": "RSI is {rsi:.1f} — extremely oversold, high bounce probability",
        "rsi_oversold": "RSI is {rsi:.1f} — oversold territory, potential buying opportunity",
        "rsi_extreme_overbought": "RSI is {rsi:.1f} — extremely overbought, high pullback risk",
        "rsi_overbought": "RSI is {rsi:.1f} — overbought, consider taking some profit",
        "rsi_bullish_divergence": "Bullish RSI divergence — price falling but RSI rising, possible reversal",
        "macd_bullish_cross": "MACD bullish crossover — momentum just flipped positive",
        "macd_bearish_cross": "MACD bearish crossover — momentum just flipped negative",
        "volume_huge_spike": "Volume is {ratio:.1f}x average — massive activity, big players likely moving",
        "volume_high": "Volume is {ratio:.1f}x average — strong interest, confirms price moves",
        "volume_very_low": "Very low volume — weak move, may not be reliable",
    },
    "tr": {
        "golden_cross": "ALTIN ÇAPRAZ tespit edildi — SMA20, SMA50'nin üzerine geçti, tarihsel olarak yükselen",
        "death_cross": "ÖLÜM ÇAPRAZ tespit edildi — SMA20, SMA50'nin altına düştü, tarihsel olarak düşen",
        "near_52w_low": "Fiyat 52 haftalık düşüğüne yakın (yalnızca %{pct:.1f} yukarıda) — derin değer potansiyeli",
        "near_52w_high": "Fiyat 52 haftalık yüksek seviyesine yakın (%{pct:.1f} aşağıda) — güçlü momentum ama az yukarı alan",
        "below_bb_lower": "Fiyat alt Bollinger Bandını kırdı — tarihsel olarak güçlü alım bölgesi",
        "above_bb_upper": "Fiyat üst Bollinger Bandını kırdı — tarihsel olarak dikkat bölgesi",
        "rsi_extreme_oversold": "RSI {rsi:.1f} — aşırı satılmış (ekstrem), yüksek toparlanma olasılığı",
        "rsi_oversold": "RSI {rsi:.1f} — aşırı satılmış bölge, olası alım fırsatı",
        "rsi_extreme_overbought": "RSI {rsi:.1f} — aşırı alınmış (ekstrem), yüksek geri çekilme riski",
        "rsi_overbought": "RSI {rsi:.1f} — aşırı alınmış, kısmi kâr almayı düşünün",
        "rsi_bullish_divergence": "Yükselen RSI uyuşmazlığı — fiyat düşerken RSI yükseliyor, olası dönüş",
        "macd_bullish_cross": "MACD yükselen çaprazı — momentum pozitife döndü",
        "macd_bearish_cross": "MACD düşen çaprazı — momentum negatife döndü",
        "volume_huge_spike": "Hacim ortalamanın {ratio:.1f} katı — devasa aktivite, büyük yatırımcılar hareket ediyor olabilir",
        "volume_high": "Hacim ortalamanın {ratio:.1f} katı — güçlü ilgi, fiyat hareketini doğruluyor",
        "volume_very_low": "Çok düşük hacim — zayıf hareket, güvenilir olmayabilir",
    },
}

# ── Recommendation actions ─────────────────────────────────────────────────────

REC_ACTIONS: dict[str, dict[str, str]] = {
    "en": {
        "STRONG BUY": "Strong buying opportunity — consider entering",
        "BUY": "Cautious buying — signals lean bullish but not perfect",
        "HOLD": "Stay on the sidelines — wait for a clearer signal",
        "SELL": "Bearish conditions — avoid new entries, protect existing gains",
        "STRONG SELL": "Strong bearish signal — high risk, exit or avoid",
    },
    "tr": {
        "STRONG BUY": "Güçlü alım fırsatı — giriş yapmayı düşünün",
        "BUY": "Temkinli alım — sinyaller yükselen ama mükemmel değil",
        "HOLD": "Kenarda bekleyin — daha net sinyal bekleyin",
        "SELL": "Düşüş koşulları — yeni giriş yapmayın, mevcut kazancı koruyun",
        "STRONG SELL": "Güçlü düşüş sinyali — yüksek risk, çıkın veya kaçının",
    },
}

# ── Recommendation reasoning templates ────────────────────────────────────────
# Placeholders: {close} {rsi} (both pre-formatted strings)

REC_REASONING: dict[str, dict[str, str]] = {
    "en": {
        "STRONG BUY": (
            "Multiple indicators align bullishly at the same time. "
            "The price ({close}) is showing oversold conditions (RSI {rsi}) and is positioned "
            "at a historically attractive level. This kind of multi-signal confluence is rare "
            "and worth paying attention to. That said, strong buy signals can still fail — "
            "never risk money you cannot afford to lose."
        ),
        "BUY": (
            "More bullish signals than bearish, but the setup is not overwhelmingly strong. "
            "At the current price of {close} the risk/reward is reasonable. "
            "This is a watchlist candidate or a small starter position — not a situation to go all-in."
        ),
        "HOLD": (
            "The signals are mixed right now. At {close}, the price is caught between nearby "
            "support and resistance levels. Entering in choppy conditions like this often leads "
            "to getting stopped out before the real move happens. Patience is a real edge in trading."
        ),
        "SELL": (
            "More bearish signals than bullish at {close}. "
            "The price is showing weakness and momentum is against buyers. "
            "If you don't currently hold this asset, do not enter. "
            "If you do hold it, think carefully about whether your reasons for holding still stand."
        ),
        "STRONG SELL": (
            "Multiple indicators simultaneously point bearish at {close}. "
            "RSI ({rsi}), trend direction, MACD, and Bollinger Bands all suggest significant "
            "downside risk. This is not a time to hold hoping for a recovery. "
            "Cutting losses early in a strong downtrend is almost always better than waiting."
        ),
    },
    "tr": {
        "STRONG BUY": (
            "Birden fazla gösterge aynı anda yükselen yönde hizalanıyor. "
            "{close} fiyatı aşırı satılmış koşullar gösteriyor (RSI {rsi}) ve tarihsel "
            "olarak cazip bir seviyede bulunuyor. Bu tür çoklu sinyal birleşimi nadirdir ve "
            "dikkat çekicidir. Bununla birlikte, güçlü alım sinyalleri de başarısız olabilir — "
            "kaybetmeyi göze alamayacağınız parayı riske atmayın."
        ),
        "BUY": (
            "Yükselen sinyaller düşenden fazla, ancak kurulum ezici şekilde güçlü değil. "
            "Mevcut {close} fiyatında risk/ödül oranı makul görünüyor. "
            "Bu bir izleme listesi adayı veya küçük bir başlangıç pozisyonu için uygundur — "
            "tüm sermayeyi koymak için değil."
        ),
        "HOLD": (
            "Sinyaller şu an karışık durumda. {close} fiyatında yakın destek ve "
            "direnç seviyeleri arasında sıkışmış bir piyasa görülüyor. "
            "Bu tür dalgalı koşullarda girmek çoğunlukla gerçek hareket başlamadan önce "
            "stop'a takılmakla sonuçlanır. Sabır, ticarette gerçek bir avantajdır."
        ),
        "SELL": (
            "{close} seviyesinde yükselen sinyalden çok düşen sinyal var. "
            "Fiyat zayıflık gösteriyor ve momentum alıcıların aleyhine. "
            "Bu varlığı şu an tutmuyorsanız giriş yapmayın. "
            "Tutuyorsanız, tutma nedenlerinizin hâlâ geçerli olup olmadığını dikkatle değerlendirin."
        ),
        "STRONG SELL": (
            "{close} seviyesinde birden fazla gösterge aynı anda düşen yönde. "
            "RSI ({rsi}), trend yönü, MACD ve Bollinger Bantları önemli aşağı yönlü risk "
            "işaret ediyor. Toparlanma umuduyla beklemek için uygun bir zaman değil. "
            "Güçlü bir düşüş trendinde erken zarar kesmek neredeyse her zaman beklemeyle "
            "zararı artırmaktan iyidir."
        ),
    },
}

# ── Entry plan templates ───────────────────────────────────────────────────────
# Placeholders: {close} {nearest_support} {sma_20} {nearest_resistance} {stop_loss} {low_52w}

REC_ENTRY: dict[str, dict[str, str]] = {
    "en": {
        "STRONG BUY": (
            "Rather than going all-in at once, consider splitting your entry into 3 parts:\n"
            "  Part 1 — Enter 1/3 of your intended position now at ~{close}\n"
            "  Part 2 — Add 1/3 more if price dips to the {nearest_support} support zone\n"
            "  Part 3 — Add the final 1/3 when you see a clear bounce\n"
            "           (RSI rises back above 40, or MACD crosses positive)\n"
            "This is called DCA (Dollar Cost Averaging) and it reduces risk from bad timing."
        ),
        "BUY": (
            "Consider a small starter position (25-33% of what you'd normally invest) at ~{close}.\n"
            "Wait for one more confirmation before adding more:\n"
            "  • RSI climbing back above 45\n"
            "  • Price closing above the SMA20 ({sma_20})\n"
            "  • MACD histogram turning green\n"
            "If none of those happen and price breaks below {nearest_support}, skip this trade."
        ),
        "HOLD": (
            "Do not enter yet. Instead, set price alerts:\n"
            "  Alert 1 — If price drops to {nearest_support}  (potential discount entry)\n"
            "  Alert 2 — If price breaks above {nearest_resistance} with volume  (momentum entry)\n"
            "Check back when RSI drops below 35 or the trend becomes clear."
        ),
        "SELL": (
            "Do not open a new position here.\n"
            "If you already hold this asset:\n"
            "  • Consider selling 30-50% of your position to lock in gains or reduce losses\n"
            "  • Move your stop loss up to {stop_loss} to protect what remains\n"
            "  • Reassess if price recovers above {sma_20}"
        ),
        "STRONG SELL": (
            "Do not enter under any circumstances right now.\n"
            "If you currently hold this asset:\n"
            "  • Strongly consider exiting most or all of your position\n"
            "  • At minimum, set a hard stop loss at {stop_loss}\n"
            "  • The next potential buy zone to watch is near the 52-week low ({low_52w})"
        ),
    },
    "tr": {
        "STRONG BUY": (
            "Tüm sermayenizi tek seferde koymak yerine, girişinizi 3 parçaya bölün:\n"
            "  1. Kısım — Pozisyonunuzun 1/3'ünü şimdi ~{close} seviyesinde açın\n"
            "  2. Kısım — Fiyat {nearest_support} destek bölgesine düşerse 1/3 daha ekleyin\n"
            "  3. Kısım — Net bir toparlanma gördüğünüzde son 1/3'ü ekleyin\n"
            "             (RSI 40'ın üzerine çıkınca veya MACD pozitife dönünce)\n"
            "Buna DCA (Düzenli Maliyet Ortalaması) denir ve zamanlama riskini azaltır."
        ),
        "BUY": (
            "~{close} seviyesinde küçük bir başlangıç pozisyonu düşünün (planladığınızın %25-33'ü).\n"
            "Daha fazla eklemeden önce bir doğrulama sinyali bekleyin:\n"
            "  • RSI'nin 45'in üzerine çıkması\n"
            "  • Fiyatın SMA20'nin ({sma_20}) üzerinde kapanması\n"
            "  • MACD histogramının yeşile dönmesi\n"
            "Bunlardan hiçbiri gerçekleşmezse ve fiyat {nearest_support} altına kırılırsa bu işlemi atlayın."
        ),
        "HOLD": (
            "Henüz giriş yapmayın. Bunun yerine fiyat alarmları belirleyin:\n"
            "  Alarm 1 — Fiyat {nearest_support} seviyesine düşerse  (indirimli giriş potansiyeli)\n"
            "  Alarm 2 — Fiyat {nearest_resistance} üzerinde ve hacimle kapanırsa  (momentum girişi)\n"
            "RSI 35'in altına düştüğünde veya trend netleştiğinde tekrar kontrol edin."
        ),
        "SELL": (
            "Buradan yeni pozisyon açmayın.\n"
            "Bu varlığı halihazırda tutuyorsanız:\n"
            "  • Kâr kilitlemek veya zararı azaltmak için pozisyonunuzun %30-50'sini satmayı düşünün\n"
            "  • Kalan kısım için stop loss'u {stop_loss} seviyesine çekin\n"
            "  • Fiyat {sma_20} SMA20'nin üzerine çıkarsa yeniden değerlendirin"
        ),
        "STRONG SELL": (
            "Şu koşullarda kesinlikle giriş yapmayın.\n"
            "Bu varlığı şu an tutuyorsanız:\n"
            "  • Pozisyonunuzun büyük bölümünü veya tamamını satmayı güçlü biçimde düşünün\n"
            "  • En azından {stop_loss} seviyesinde katı bir zarar kes belirleyin\n"
            "  • Bir sonraki potansiyel alım bölgesi 52 haftalık düşük civarında: {low_52w}"
        ),
    },
}

# ── Risk flag texts ────────────────────────────────────────────────────────────

RISK_TEXTS: dict[str, dict[str, str]] = {
    "en": {
        "downtrend": (
            "The overall trend is still bearish — buying into a downtrend carries higher risk. "
            "Wait for trend confirmation before going large."
        ),
        "low_volume": (
            "Volume is low — moves on low volume are less reliable and can reverse quickly."
        ),
        "falling_knife": (
            "Oversold + downtrend = 'falling knife' risk. Price can stay oversold for a long time "
            "in a real downtrend. Wait for the trend to show signs of turning."
        ),
        "near_high": (
            "Price is close to its 52-week high. Less room to run upward, "
            "and corrections from highs can be sharp."
        ),
        "low_rr": (
            "Risk/reward is {rr}:1 — below the ideal 2:1 minimum. "
            "Consider waiting for a better entry closer to support."
        ),
        "contrarian": (
            "Signal says BUY but the macro trend is DOWN. These are contrarian trades — "
            "higher reward potential but also higher failure rate. Size your position smaller."
        ),
        "always": (
            "No analysis tool is right 100% of the time. Always use a stop loss "
            "and only invest money you can afford to lose."
        ),
    },
    "tr": {
        "downtrend": (
            "Genel trend hâlâ düşen — düşüş trendine karşı alım yapmak daha yüksek risk taşır. "
            "Büyük pozisyon açmadan önce trend onayını bekleyin."
        ),
        "low_volume": (
            "Hacim düşük — düşük hacimli hareketler daha az güvenilirdir ve hızla tersine dönebilir."
        ),
        "falling_knife": (
            "Aşırı satılmış + düşüş trendi = 'düşen bıçak' riski. Fiyat gerçek bir düşüş trendinde "
            "uzun süre aşırı satılmış kalabilir. Trendin dönmeye başladığına dair işaret bekleyin."
        ),
        "near_high": (
            "Fiyat 52 haftalık yüksek seviyesine yakın. Yukarı yönlü alan daha az "
            "ve yüksek noktalardan düzeltmeler sert olabilir."
        ),
        "low_rr": (
            "Risk/ödül {rr}:1 — ideal 2:1 minimumunun altında. "
            "Desteğe daha yakın, daha iyi bir giriş için beklemeyi düşünün."
        ),
        "contrarian": (
            "Sinyal AL diyor ama makro trend DÜŞÜŞ. Bu zıt yönlü işlemlerdir — "
            "daha yüksek ödül potansiyeli ama aynı zamanda daha yüksek başarısızlık oranı. "
            "Pozisyon boyutunuzu küçük tutun."
        ),
        "always": (
            "Hiçbir analiz aracı %100 doğru değildir. Her zaman stop loss kullanın "
            "ve kaybetmeyi göze alamayacağınız parayı yatırmayın."
        ),
    },
}


# ── Lang class ─────────────────────────────────────────────────────────────────


class Lang:
    """Wraps all translation dictionaries and exposes clean helper methods."""

    def __init__(self, code: str) -> None:
        if code not in SUPPORTED_LANGS:
            raise ValueError(
                f"Unsupported language: {code}. Choose from {list(SUPPORTED_LANGS)}"
            )
        self.code = code

    # ── Static strings ─────────────────────────────────────────────────────────

    def t(self, key: str, **kwargs: object) -> str:
        """Return a translated static string, optionally formatted with kwargs."""
        text = STRINGS[self.code].get(key) or STRINGS["en"].get(key, key)
        return text.format(**kwargs) if kwargs else text

    # ── Coded values ───────────────────────────────────────────────────────────

    def signal(self, code: str) -> str:
        return SIGNAL_NAMES[self.code].get(code, code)

    def trend(self, code: str) -> str:
        return TREND_NAMES[self.code].get(code, code)

    def trend_detail(self, trend_code: str) -> str:
        return TREND_DETAILS[self.code].get(trend_code, trend_code)

    def summary(self, signal_code: str) -> str:
        return SUMMARIES[self.code].get(signal_code, "")

    def rsi_lbl(self, code: str) -> str:
        return RSI_LABELS[self.code].get(code, code)

    def bb_lbl(self, code: str) -> str:
        return BB_LABELS[self.code].get(code, code)

    def volume_lbl(self, code: str) -> str:
        return VOLUME_LABELS[self.code].get(code, code)

    def position_lbl(self, code: str) -> str:
        return POSITION_LABELS[self.code].get(code, code)

    def event(self, key: str, params: dict) -> str:
        """Format and translate a market event. params are passed to str.format()."""
        template = EVENTS[self.code].get(key) or EVENTS["en"].get(key, key)
        return template.format(**params) if params else template

    # ── Recommendation sections ────────────────────────────────────────────────

    def rec_action(self, signal: str) -> str:
        return REC_ACTIONS[self.code].get(signal, REC_ACTIONS["en"].get(signal, signal))

    def rec_reasoning(self, signal: str, close: str, rsi: str) -> str:
        template = REC_REASONING[self.code].get(signal) or REC_REASONING["en"].get(
            signal, ""
        )
        return template.format(close=close, rsi=rsi)

    def rec_entry(
        self,
        signal: str,
        close: str,
        nearest_support: str,
        sma_20: str,
        nearest_resistance: str,
        stop_loss: str,
        low_52w: str,
    ) -> str:
        template = REC_ENTRY[self.code].get(signal) or REC_ENTRY["en"].get(signal, "")
        return template.format(
            close=close,
            nearest_support=nearest_support,
            sma_20=sma_20,
            nearest_resistance=nearest_resistance,
            stop_loss=stop_loss,
            low_52w=low_52w,
        )

    def rec_key_levels(
        self,
        close: float,
        sma_20: float,
        sma_50: float,
        nearest_support: float,
        nearest_resistance: float,
        bb_lower: float,
        bb_upper: float,
        low_52w: float,
        high_52w: float,
        risk_per_unit: float,
        reward_per_unit: float,
        rr_ratio: float,
    ) -> list[str]:
        c = self.code
        if c == "tr":
            return [
                f"Güncel fiyat       : {close:,.2f}",
                f"En yakın destek    : {nearest_support:,.2f}  (fiyat tabanı — burada toparlanma bekleyin)",
                f"SMA 20             : {sma_20:,.2f}  (kısa vadeli trend çizgisi)",
                f"SMA 50             : {sma_50:,.2f}  (orta vadeli trend çizgisi)",
                f"En yakın direnç    : {nearest_resistance:,.2f}  (fiyat tavanı — burada satış baskısı beklenir)",
                f"Bollinger alt bant : {bb_lower:,.2f}  (istatistiksel olarak aşırı satılmış bölge)",
                f"Bollinger üst bant : {bb_upper:,.2f}  (istatistiksel olarak aşırı alınmış bölge)",
                f"52 haftalık düşük  : {low_52w:,.2f}",
                f"52 haftalık yüksek : {high_52w:,.2f}",
                f"Risk/Ödül          : {rr_ratio}:1  "
                f"(~{risk_per_unit:,.2f} riske karşı ~{reward_per_unit:,.2f} kazanç potansiyeli)",
            ]
        return [
            f"Current price   : {close:,.2f}",
            f"Nearest support : {nearest_support:,.2f}  (price floor — watch for a bounce here)",
            f"SMA 20          : {sma_20:,.2f}  (short-term trend line)",
            f"SMA 50          : {sma_50:,.2f}  (medium-term trend line)",
            f"Nearest resist. : {nearest_resistance:,.2f}  (price ceiling — expect selling pressure here)",
            f"Bollinger lower : {bb_lower:,.2f}  (statistically oversold zone)",
            f"Bollinger upper : {bb_upper:,.2f}  (statistically overbought zone)",
            f"52-week low     : {low_52w:,.2f}",
            f"52-week high    : {high_52w:,.2f}",
            f"Risk/reward     : {rr_ratio}:1  "
            f"(risking ~{risk_per_unit:,.2f} to potentially gain ~{reward_per_unit:,.2f})",
        ]

    def rec_watch(
        self,
        sma_20: str,
        sma_50: str,
        bb_upper: str,
        nearest_support: str,
        low_52w: str,
    ) -> list[str]:
        if self.code == "tr":
            return [
                "RSI 50'nin üzerine geçerse → yükselen momentum teyit edildi",
                "RSI 30'un altına düşerse → daha derin aşırı satılmış, daha iyi giriş fırsatı",
                "RSI 70'in üzerine geçerse → kâr almayı düşünün",
                f"Fiyat SMA20'nin ({sma_20}) üzerinde kaparsa → kısa vadeli trend pozitife dönüyor",
                f"Fiyat SMA50'nin ({sma_50}) üzerinde kaparsa → orta vadeli yükselen trend teyit edildi",
                f"Fiyat {bb_upper} üst Bollinger Bandını kırarsa → güçlü momentum ama aşırı alınmış riski",
                "MACD histogramı yeşile dönerse → taze yükselen momentum",
                "MACD histogramı kırmızıya dönerse → taze düşen momentum",
                "Fiyat hareketinde hacim artışı (2x+ ortalama) → hareketi teyit eder",
                f"Fiyat {nearest_support} seviyesinde tutunur ve toparlanırsa → destek gerçek, alıcılar burada",
                f"Fiyat {low_52w} (52 haftalık düşük) altına kırılırsa → büyük uyarı, trend çok daha kötüleşebilir",
            ]
        return [
            "RSI crosses above 50 → bullish momentum confirmed",
            "RSI crosses below 30 → deeper oversold, better entry opportunity",
            "RSI crosses above 70 → consider taking profit",
            f"Price closes above SMA20 ({sma_20}) → short-term trend turning positive",
            f"Price closes above SMA50 ({sma_50}) → medium-term trend confirmed bullish",
            f"Price breaks above {bb_upper} (Bollinger upper) → strong momentum but overbought risk",
            "MACD histogram turns green → fresh bullish momentum",
            "MACD histogram turns red → fresh bearish momentum",
            "Volume spike (2x+ average) on a price move → confirms the direction of the move",
            f"Price holds at {nearest_support} with bounce → support is real and buyers are here",
            f"Price breaks below {low_52w} (52-week low) → major warning, trend could get much worse",
        ]

    def rec_exit(
        self, stop_loss: str, take_profit_1: str, take_profit_2: str
    ) -> list[str]:
        if self.code == "tr":
            return [
                f"Zarar Kes      : {stop_loss}  — fiyat bu seviyenin altında kaparsa derhal çıkın",
                f"Kâr Al #1      : {take_profit_1}  — ilk direnç, burada %30-50 satmayı düşünün",
                f"Kâr Al #2      : {take_profit_2}  — güçlü hedef, burada daha fazlasını satmayı düşünün",
                "Genel Kural    : Kazanan bir işlemin büyük zarara dönmesine izin vermeyin — fiyat yükseldikçe stop'u yukarı çekin",
                "Genel Kural    : RSI 75+'a ulaşırsa varlık muhtemelen aşırı alınmış — biraz kâr alın",
                "Genel Kural    : Fiyat giriş noktanızdan %8-10'dan fazla düşerse tezinizi yeniden değerlendirin",
            ]
        return [
            f"Stop loss      : {stop_loss}  — exit immediately if price closes below this",
            f"Take profit #1 : {take_profit_1}  — first resistance, consider selling 30-50% here",
            f"Take profit #2 : {take_profit_2}  — stronger target, consider selling more here",
            "General rule   : Never let a winning trade turn into a big loss — trail your stop up as price rises",
            "General rule   : If RSI hits 75+, the asset is likely overbought — take some profit",
            "General rule   : If price drops more than 8-10% from your entry, reconsider your thesis",
        ]

    def rec_risks(self, risk_flags: list[str], rr_ratio: float) -> list[str]:
        result: list[str] = []
        for flag in risk_flags:
            template = RISK_TEXTS[self.code].get(flag) or RISK_TEXTS["en"].get(
                flag, flag
            )
            result.append(template.format(rr=rr_ratio))
        return result


# ── Language selection helper ──────────────────────────────────────────────────


def select_language() -> Lang:
    """Prompt the user to choose a language and return the corresponding Lang."""
    print("\n" + "=" * 44)
    print("  Choose your language / Dilinizi seçin:")
    print("=" * 44)
    for i, (code, name) in enumerate(SUPPORTED_LANGS.items(), start=1):
        print(f"  {i}. {name}")
    print("=" * 44)
    codes = list(SUPPORTED_LANGS.keys())
    while True:
        choice = input("  > ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(codes):
            return Lang(codes[int(choice) - 1])
        # Also accept typing the code directly
        if choice.lower() in codes:
            return Lang(choice.lower())
        print(f"  Please enter a number (1-{len(codes)}) / Lütfen bir numara girin.")
