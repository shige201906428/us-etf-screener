from datetime import datetime
import pandas as pd
import yfinance as yf

# 米国主要ETF 100選 ＋ 追加個別株104銘柄（合計204銘柄・重複削除済み）と業種情報
TICKERS_WITH_SECTOR = {
    # --- 元の追加個別銘柄（エネルギー・海運） ---
    "FRO": "エネルギー（石油タンカー）",
    "DHT": "エネルギー（石油タンカー）",
    "NAT": "エネルギー（石油タンカー）",
    "TRMD": "エネルギー（石油タンカー）",
    # --- マグニフィセント・セブン ＆ IT・ハイテク ---
    "AAPL": "情報技術（ハードウェア・端末）",
    "MSFT": "情報技術（ソフトウェア）",
    "GOOGL": "通信サービス（ネット・メディア）",
    "AMZN": "一般消費財（ネット小売）",
    "NVDA": "情報技術（半導体）",
    "META": "通信サービス（ネット・メディア）",
    "TSLA": "一般消費財（自動車）",
    "AVGO": "情報技術（半導体）",
    "ORCL": "情報技術（ソフトウェア）",
    "CRM": "情報技術（ソフトウェア）",
    "CSCO": "情報技術（通信機器）",
    "ACN": "情報技術（ITサービス）",
    "ADBE": "情報技術（ソフトウェア）",
    "TXN": "情報技術（半導体）",
    "QCOM": "情報技術（半導体）",
    "AMD": "情報技術（半導体）",
    "INTC": "情報技術（半導体）",
    "MU": "情報技術（半導体）",
    "AMAT": "情報技術（半導体製造装置）",
    "LRCX": "情報技術（半導体製造装置）",
    # --- ヘルスケア・製薬 ---
    "JNJ": "ヘルスケア（医薬・日用品）",
    "UNH": "ヘルスケア（医療保険・サービス）",
    "LLY": "ヘルスケア（医薬品）",
    "MRK": "ヘルスケア（医薬品）",
    "ABV": "ヘルスケア（医薬品）",
    "PFE": "ヘルスケア（医薬品）",
    "TMO": "ヘルスケア（ライフサイエンス）",
    "ABT": "ヘルスケア（医療機器・日用品）",
    "BMY": "ヘルスケア（医薬品）",
    "AMGN": "ヘルスケア（バイオ）",
    "GILD": "ヘルスケア（バイオ）",
    "ISRG": "ヘルスケア（医療機器）",
    "VRTX": "ヘルスケア（バイオ）",
    "REGN": "ヘルスケア（バイオ）",
    # --- 金融・フィンテック ---
    "JPM": "金融（総合銀行）",
    "BAC": "金融（総合銀行）",
    "WFC": "金融（総合銀行）",
    "C": "金融（総合銀行）",
    "GS": "金融（投資銀行・証券）",
    "MS": "金融（投資銀行・証券）",
    "V": "金融（決済サービス）",
    "MA": "金融（決済サービス）",
    "AXP": "金融（クレジット・決済）",
    "PYPL": "金融（デジタル決済）",
    "BLK": "金融（資産運用）",
    "SPGI": "金融（金融情報・格付け）",
    "BRK.B": "金融（複合企業・保険）",
    # --- 生活必需品・一般消費財 ---
    "PG": "生活必需品（家庭用品）",
    "KO": "生活必需品（飲料）",
    "PEP": "生活必需品（飲料・スナック）",
    "COST": "生活必需品（量販店）",
    "WMT": "生活必需品（小売・量販店）",
    "NKE": "一般消費財（アパレル）",
    "SBUX": "一般消費財（カフェ）",
    "MCD": "一般消費財（ファストフード）",
    "HD": "一般消費財（ホームセンター）",
    "LOW": "一般消費財（ホームセンター）",
    "PM": "生活必需品（タバコ）",
    "MO": "生活必需品（タバコ）",
    "CL": "生活必需品（家庭用品）",
    "EL": "生活必需品（化粧品）",
    # --- 資本財・製造・防衛 ---
    "CAT": "資本財（建設・鉱業機械）",
    "DE": "資本財（農業・建設機械）",
    "GE": "資本財（総合工業・航空）",
    "MMM": "資本財（複合企業・工業製品）",
    "HON": "資本財（複合企業・航空宇宙）",
    "LMT": "資本財（防衛・航空宇宙）",
    "RTX": "資本財（防衛・航空宇宙）",
    "BA": "資本財（航空宇宙）",
    "UNP": "資本財（鉄道輸送）",
    "UPS": "資本財（物流・運送）",
    "FDX": "資本財（物流・運送）",
    "WM": "資本財（環境・廃棄物処理）",
    # --- エネルギー・素材・公益 ---
    "XOM": "エネルギー（石油・ガス開発）",
    "CVX": "エネルギー（石油・ガス開発）",
    "COP": "エネルギー（石油・ガス開発）",
    "SLB": "エネルギー（石油サービス）",
    "EOG": "エネルギー（石油・ガス開発）",
    "LIN": "素材（産業ガス）",
    "APD": "素材（産業ガス）",
    "FCX": "素材（非鉄金属・銅）",
    "NEM": "素材（金採掘）",
    "NEE": "公益事業（再生可能エネ）",
    "DUK": "公益事業（電力）",
    "D": "公益事業（電力）",
    # --- 通信・エンターテインメント ---
    "T": "通信サービス（総合通信）",
    "VZ": "通信サービス（総合通信）",
    "DIS": "通信サービス（娯楽・エンタメ）",
    "NFLX": "通信（ストリーミング）",
    "CMCSA": "通信（メディア・ケーブル）",
    # --- 高配当・REIT・その他注目銘柄 ---
    "O": "不動産（商業施設REIT）",
    "SPG": "不動産（ショッピングモール）",
    "AMT": "不動産（通信タワーREIT）",
    "CCI": "不動産（通信タワーREIT）",
    "PLTR": "情報技術（データ分析・AI）",
    "SNOW": "情報技術（クラウド・DWH）",
    "SQ": "金融（決済・フィンテック）",
    "ABNB": "一般消費財（民泊・旅行）",
    "UBER": "一般消費財（配車・配達）",
    # ==========================================
    # --- 以下、元のETF 100選（カテゴリ別） ---
    # ==========================================
    # --- 1. 主要株価指数 ---
    "SPY": "ETF（米国大型株・S&P500）",
    "VOO": "ETF（米国大型株・S&P500）",
    "IVV": "ETF（米国大型株・S&P500）",
    "QQQ": "ETF（米国大型株・NASDAQ100）",
    "DIA": "ETF（米国大型株・NYダウ）",
    "IWM": "ETF（米国小型株・ラッセル2000）",
    "MDY": "ETF（米国中型株・S&P400）",
    "IWB": "ETF（米国大型株・ラッセル1000）",
    "VTI": "ETF（米国株総合・CRSP）",
    "ITOT": "ETF（米国株総合・S&P1500）",
    # --- 2. 高配当・増配・バリュー株 ---
    "VYM": "ETF（米国高配当株）",
    "HDV": "ETF（米国高配当・財務健全）",
    "SPYD": "ETF（米国高配当・S&P500）",
    "DVY": "ETF（米国高配当・配当重視）",
    "SDY": "ETF（米国高配当・増配）",
    "NOBL": "ETF（米国増配・S&P500配当貴族）",
    "VIG": "ETF（米国連続増配株）",
    "DGRW": "ETF（米国増配・成長重視）",
    "IVE": "ETF（米国バリュー株・S&P500）",
    "VTV": "ETF（米国バリュー株）",
    # --- 3. グロース株・モメンタム ---
    "IVW": "ETF（米国グロース株・S&P500）",
    "VUG": "ETF（米国グロース株）",
    "IWF": "ETF（米国グロース株・ラッセル）",
    "MTUM": "ETF（米国モメンタム株）",
    "ARKK": "ETF（米国イノベーション株）",
    "QQQM": "ETF（米国大型株・NASDAQ100）",
    "RPG": "ETF（米国ピュア・グロース）",
    "MGK": "ETF（米国メガキャップグロース）",
    "IWY": "ETF（米国大型・Top200）",
    "SPYG": "ETF（米国グロース株・S&P500）",
    # --- 4. セクター別（IT・ハイテク・半導体） ---
    "XLK": "ETF（米国セクター・情報技術）",
    "IYW": "ETF（米国セクター・情報技術）",
    "SMH": "ETF（米国セクター・半導体）",
    "SOXX": "ETF（米国セクター・半導体）",
    "VGT": "ETF（米国セクター・情報技術）",
    "IGV": "ETF（米国セクター・ソフトウェア）",
    "FDN": "ETF（米国セクター・ネット）",
    "XSD": "ETF（米国セクター・半導体）",
    "SKYY": "ETF（米国セクター・クラウド）",
    # --- 5. セクター別（ヘルスケア・生活必需品・通信） ---
    "XLV": "ETF（米国セクター・ヘルスケア）",
    "VHT": "ETF（米国セクター・ヘルスケア）",
    "XBI": "ETF（米国セクター・バイオ）",
    "IBB": "ETF（米国セクター・バイオ）",
    "XLP": "ETF（米国セクター・生活必需品）",
    "VDC": "ETF（米国セクター・生活必需品）",
    "XLC": "ETF（米国セクター・通信サービス）",
    "VOX": "ETF（米国セクター・通信サービス）",
    "IYZ": "ETF（米国セクター・通信サービス）",
    "XLY": "ETF（米国セクター・一般消費財）",
    # --- 6. セクター別（金融・資本財・素材・エネルギー・公益） ---
    "XLF": "ETF（米国セクター・金融）",
    "VFH": "ETF（米国セクター・金融）",
    "KRE": "ETF（米国セクター・地方銀行）",
    "XLI": "ETF（米国セクター・資本財）",
    "VIS": "ETF（米国セクター・資本財）",
    "XLB": "ETF（米国セクター・素材）",
    "VAW": "ETF（米国セクター・素材）",
    "XLE": "ETF（米国セクター・エネルギー）",
    "VDE": "ETF（米国セクター・エネルギー）",
    "XLU": "ETF（米国セクター・公益事業）",
    # --- 7. 米国以外の先進国・新興国 ---
    "VEA": "ETF（先進国株・除く米国）",
    "IEFA": "ETF（先進国株・除く米国）",
    "EFA": "ETF（先進国株・除く米国）",
    "VWO": "ETF（新興国株総合）",
    "IEMG": "ETF（新興国株総合）",
    "EEM": "ETF（新興国株総合）",
    "VT": "ETF（全世界株総合）",
    "ACWI": "ETF（全世界株・大型・中型）",
    "VXUS": "ETF（全世界株・除く米国）",
    "EWT": "ETF（特定国・台湾）",
    # --- 8. 特定国（日本・欧州・中国・インド等） ---
    "EWJ": "ETF（特定国・日本）",
    "DXJ": "ETF（特定国・日本為替ヘッジ）",
    "VGK": "ETF（特定地域・欧州）",
    "EZU": "ETF（特定地域・ユーロ圏）",
    "FXI": "ETF（特定国・中国大型株）",
    "MCHI": "ETF（特定国・中国総合）",
    "INDA": "ETF（特定国・インド）",
    "EPI": "ETF（特定国・インド収益加重）",
    "EWW": "ETF（特定国・メキシコ）",
    "EWZ": "ETF（特定国・ブラジル）",
    # --- 9. 債券・キャッシュ ---
    "BND": "ETF（米国債券総合）",
    "AGG": "ETF（米国債券総合）",
    "SHY": "ETF（米国短期国債）",
    "IEF": "ETF（米国中期国債）",
    "TLT": "ETF（米国長期国債）",
    "TIP": "ETF（米国インフレ連動債）",
    "LQD": "ETF（米国投資適格社債）",
    "HYG": "ETF（米国ハイイールド社債）",
    "BNDX": "ETF（先進国債券為替ヘッジ）",
    "VWOB": "ETF（新興国ドル建て債券）",
    # --- 10. コモディティ・不動産・その他 ---
    "GLD": "ETF（コモディティ・金）",
    "IAU": "ETF（コモディティ・金）",
    "SLV": "ETF（コモディティ・銀）",
    "USO": "ETF（コモディティ・原油）",
    "PDBC": "ETF（コモディティ総合）",
    "IYR": "ETF（米国リート総合）",
    "VNQ": "ETF（米国リート総合）",
    "XLRE": "ETF（米国セクター・不動産）",
    "VNQI": "ETF（グローバルリート）",
    "BIL": "ETF（米国超短期国債・キャッシュ）"
}

def get_etf_data():
    data_list = []
    for ticker, sector in TICKERS_WITH_SECTOR.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            if hist.empty:
                continue
            
            latest = hist.iloc[-1]
            prev = hist.iloc[-2]
            
            change = ((latest["Close"] - prev["Close"]) / prev["Close"]) * 100
            
            info = t.info
            name = info.get("shortName", ticker)
            
            div_yield = info.get("trailingAnnualDividendYield")
            if div_yield is None:
                div_yield = info.get("yield", 0)
            
            div_yield_pct = div_yield * 100 if div_yield else 0.0
            
            data_list.append({
                "Ticker": ticker,
                "Name": name,
                "Sector": sector,  # 業種情報を追加
                "Price": round(latest["Close"], 2),
                "Change": round(change, 2),
                "Volume": int(latest["Volume"]),
                "Yield": round(div_yield_pct, 2)
            })
            print(f"Fetched: {ticker} | {sector} (Yield: {div_yield_pct:.2f}%)")
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            
    return pd.DataFrame(data_list)

def generate_html(df):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    table_rows = ""
    for _, row in df.iterrows():
        # ハイライト対象：SPYD, XLF, FRO, DHT, NAT, TRMD, HDV, XLE, EPI
        if row['Ticker'] in ["SPYD", "XLF", "FRO", "DHT", "NAT", "TRMD", "HDV", "XLE", "EPI"]:
            row_style = 'style="background-color: #e8f5e9 !important; border-left: 4px solid #2e7d32;"'
        else:
            row_style = ""

        # 前日比のカラーリング
        if row['Change'] > 0:
            change_style = "color: #dc3545; font-weight: bold;"
            sign = "+"
        elif row['Change'] < 0:
            change_style = "color: #0d6efd; font-weight: bold;"
            sign = ""
        else:
            change_style = "color: #6c757d; font-weight: bold;"
            sign = ""
            
        yield_style = "color: #198754; font-weight: bold;" if row['Yield'] > 0 else "color: #6c757d;"
        yield_display = f"{row['Yield']:.2f}%" if row['Yield'] > 0 else "-"

        table_rows += f"""
                        <tr {row_style}>
                            <td class="p-2 text-center"><span class="badge bg-dark text-white p-1" style="font-size: 0.75rem; min-width: 42px;">{row['Ticker']}</span></td>
                            <td class="p-2 d-none d-md-table-cell"><span class="fw-bold text-truncate d-inline-block" style="max-width: 180px;">{row['Name']}</span></td>
                            <td class="p-2 d-none d-lg-table-cell"><span class="text-muted text-truncate d-inline-block" style="max-width: 160px; font-size: 0.75rem;">{row['Sector']}</span></td>
                            <td class="text-end p-2 fw-bold">${row['Price']:,.2f}</td>
                            <td class="text-end p-2" style="{change_style}">{sign}{row['Change']:.2f}%</td>
                            <td class="text-end p-2" style="{yield_style}">{yield_display}</td>
                            <td class="text-end p-2 text-muted d-none d-sm-table-cell">{row['Volume']:,}</td>
                        </tr>"""

    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>米国ETF・株式デイリースクリーナー</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #f4f6f9;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #333;
            padding-bottom: 20px;
        }}
        .header-section {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #fff;
            padding: 20px 0;
            margin-bottom: 15px;
            border-bottom: 4px solid #3b82f6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        .card {{
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            background-color: #ffffff;
        }}
        .table-responsive {{
            border-radius: 8px;
            overflow: hidden;
        }}
        .table {{
            margin-bottom: 0;
            vertical-align: middle;
        }}
        .table thead th {{
            background-color: #f8fafc;
            color: #475569;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.05em;
            padding: 10px 8px;
            border-bottom: 2px solid #e2e8f0;
        }}
        .table tbody td {{
            font-size: 0.8rem;
            padding: 10px 8px;
            border-bottom: 1px solid #f1f5f9;
        }}
        .table tbody tr:hover {{
            background-color: #f8fafc;
        }}
        .refresh-tag {{
            font-size: 0.75rem;
            background-color: rgba(255, 255, 255, 0.15);
            padding: 4px 8px;
            border-radius: 12px;
            display: inline-block;
            backdrop-filter: blur(4px);
        }}
        @media (max-width: 576px) {{
            .table thead th {{
                font-size: 0.65rem;
                padding: 8px 4px;
            }}
            .table tbody td {{
                font-size: 0.75rem;
                padding: 8px 4px;
            }}
            .header-section h1 {{
                font-size: 1.25rem;
            }}
        }}
    </style>
</head>
<body>

    <div class="header-section">
        <div class="container">
            <div class="row align-items-center text-center text-md-start">
                <div class="col-12 col-md-8">
                    <h1 class="fw-bold mb-1" style="letter-spacing: -0.5px; font-size: 1.4rem;">🇺🇸 米国主要ETF・株式一覧</h1>
                    <p class="mb-2 mb-md-0 text-white-50" style="font-size: 0.75rem;">銘柄ごとのセクター情報、パフォーマンス、配当利回りを一括表示</p>
                </div>
                <div class="col-12 col-md-4 text-center text-md-end">
                    <span class="refresh-tag">
                        ⏱️ 更新: <strong>{now}</strong>
                    </span>
                </div>
            </div>
        </div>
    </div>

    <div class="container px-2 px-sm-3">
        <div class="card p-1 p-sm-2">
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th scope="col" class="text-center" style="width: 12%;">Symbol</th>
                            <th scope="col" class="d-none d-md-table-cell" style="width: 25%;">銘柄名</th>
                            <th scope="col" class="d-none d-lg-table-cell" style="width: 23%;">セクター / 種別</th>
                            <th scope="col" class="text-end" style="width: 13%;">価格</th>
                            <th scope="col" class="text-end" style="width: 12%;">前日比</th>
                            <th scope="col" class="text-end" style="width: 12%;">配当</th>
                            <th scope="col" class="text-end d-none d-sm-table-cell" style="width: 15%;">出来高</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="text-center mt-3">
            <p class="text-muted" style="font-size: 0.7rem;">
                データソース: Yahoo! Finance | 自動更新
            </p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    df_etf = get_etf_data()
    if not df_etf.empty:
        # 配当利回りの高い順にソート
        df_etf = df_etf.sort_values(by="Yield", ascending=False)
        generate_html(df_etf)
        print(f"Successfully generated index.html with {len(df_etf)} items.")
    else:
        print("No data was fetched.")
