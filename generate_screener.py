import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# 1. 銘柄・セクター定義
TICKERS_WITH_SECTOR = {
    "FRO": "エネルギー（石油タンカー）", "DHT": "エネルギー（石油タンカー）",
    "NAT": "エネルギー（石油タンカー）", "TRMD": "エネルギー（石油タンカー）",
    "AAPL": "情報技術（ハードウェア）", "MSFT": "情報技術（ソフトウェア）",
    "GOOGL": "通信（ネットメディア）", "AMZN": "一般消費財（小売）",
    "NVDA": "情報技術（半導体）", "META": "通信（ネットメディア）",
    "TSLA": "一般消費財（自動車）", "AVGO": "情報技術（半導体）",
    "ORCL": "情報技術（ソフト）", "CRM": "情報技術（ソフト）",
    "CSCO": "情報技術（通信機器）", "ACN": "情報技術（ITサービス）",
    "ADBE": "情報技術（ソフト）", "TXN": "情報技術（半導体）",
    "QCOM": "情報技術（半導体）", "AMD": "情報技術（半導体）",
    "INTC": "情報技術（半導体）", "MU": "情報技術（半導体）",
    "AMAT": "情報技術（半導体装置）", "LRCX": "情報技術（半導体装置）",
    "JNJ": "ヘルスケア（医薬）", "UNH": "ヘルスケア（保険）",
    "LLY": "ヘルスケア（医薬）", "MRK": "ヘルスケア（医薬）",
    "ABBV": "ヘルスケア（医薬）", "PFE": "ヘルスケア（医薬）",
    "TMO": "ヘルスケア（ライフサイエンス）", "ABT": "ヘルスケア（医療機器）",
    "BMY": "ヘルスケア（医薬）", "AMGN": "ヘルスケア（バイオ）",
    "GILD": "ヘルスケア（バイオ）", "ISRG": "ヘルスケア（医療機器）",
    "VRTX": "ヘルスケア（バイオ）", "REGN": "ヘルスケア（バイオ）",
    "JPM": "金融（総合銀行）", "BAC": "金融（総合銀行）",
    "WFC": "金融（総合銀行）", "C": "金融（総合銀行）",
    "GS": "金融（投資銀行）", "MS": "金融（投資銀行）",
    "V": "金融（決済）", "MA": "金融（決済）",
    "AXP": "金融（決済）", "PYPL": "金融（決済）",
    "BLK": "金融（資産運用）", "SPGI": "金融（格付け）",
    "BRK-B": "金融（複合）", "PG": "生活必需品（家庭用品）",
    "KO": "生活必需品（飲料）", "PEP": "生活必需品（飲料）",
    "COST": "生活必需品（量販店）", "WMT": "生活必需品（小売）",
    "NKE": "一般消費財（アパレル）", "SBUX": "一般消費財（カフェ）",
    "MCD": "一般消費財（外食）", "HD": "一般消費財（ホームセンター）",
    "LOW": "一般消費財（ホームセンター）", "PM": "生活必需品（タバコ）",
    "MO": "生活必需品（タバコ）", "CL": "生活必需品（家庭用品）",
    "EL": "生活必需品（化粧品）", "CAT": "資本財（重機）",
    "DE": "資本財（重機）", "GE": "資本財（総合工業）",
    "MMM": "資本財（複合）", "HON": "資本財（複合）",
    "LMT": "資本財（防衛）", "RTX": "資本財（防衛）",
    "BA": "資本財（航空宇宙）", "UNP": "資本財（鉄道）",
    "UPS": "資本財（物流）", "FDX": "資本財（物流）",
    "WM": "資本財（廃棄物）", "XOM": "エネルギー（石油ガス）",
    "CVX": "エネルギー（石油ガス）", "COP": "エネルギー（石油ガス）",
    "SLB": "エネルギー（石油サービス）", "EOG": "エネルギー（石油ガス）",
    "LIN": "素材（産業ガス）", "APD": "素材（産業ガス）",
    "FCX": "素材（非鉄金属）", "NEM": "素材（金）",
    "NEE": "公益事業（電力）", "DUK": "公益事業（電力）",
    "D": "公益事業（電力）", "T": "通信サービス（通信）",
    "VZ": "通信サービス（通信）", "DIS": "通信サービス（娯楽）",
    "NFLX": "通信（配信）", "CMCSA": "通信（メディア）",
    "O": "不動産（商業REIT）", "SPG": "不動産（商業REIT）",
    "AMT": "不動産（通信タワー）", "CCI": "不動産（通信タワー）",
    "PLTR": "情報技術（AI）", "SNOW": "情報技術（クラウド）",
    "SQ": "金融（決済）", "ABNB": "一般消費財（旅行）",
    "UBER": "一般消費財（配達）", "SPY": "ETF（S&P500）",
    "VOO": "ETF（S&P500）", "IVV": "ETF（S&P500）",
    "QQQ": "ETF（NASDAQ100）", "DIA": "ETF（NYダウ）",
    "IWM": "ETF（小型株）", "MDY": "ETF（中型株）",
    "IWB": "ETF（大型株）", "VTI": "ETF（米国株総合）",
    "ITOT": "ETF（米国株総合）", "VYM": "ETF（高配当株）",
    "HDV": "ETF（高配当株）", "SPYD": "ETF（高配当株）",
    "DVY": "ETF（高配当株）", "SDY": "ETF（高配当増配）",
    "NOBL": "ETF（配当貴族）", "VIG": "ETF（連続増配）",
    "DGRW": "ETF（増配成長）", "IVE": "ETF（バリュー）",
    "VTV": "ETF（バリュー）", "IVW": "ETF（グロース）",
    "VUG": "ETF（グロース）", "IWF": "ETF（グロース）",
    "MTUM": "ETF（モメンタム）", "ARKK": "ETF（破壊的革新）",
    "QQQM": "ETF（NASDAQ100）", "RPG": "ETF（グロース）",
    "MGK": "ETF（メガキャップ）", "IWY": "ETF（大型株）",
    "SPYG": "ETF（グロース）", "XLK": "ETF（IT）",
    "IYW": "ETF（IT）", "SMH": "ETF（半導体）",
    "SOXX": "ETF（半導体）", "VGT": "ETF（IT）",
    "IGV": "ETF（ソフト）", "FDN": "ETF（ネット）",
    "XSD": "ETF（半導体）", "SKYY": "ETF（クラウド）",
    "XLV": "ETF（ヘルスケア）", "VHT": "ETF（ヘルスケア）",
    "XBI": "ETF（バイオ）", "IBB": "ETF（バイオ）",
    "XLP": "ETF（必需品）", "VDC": "ETF（必需品）",
    "XLC": "ETF（通信）", "VOX": "ETF（通信）",
    "IYZ": "ETF（通信）", "XLY": "ETF（消費財）",
    "XLF": "ETF（金融）", "VFH": "ETF（金融）",
    "KRE": "ETF（地銀）", "XLI": "ETF（資本財）",
    "VIS": "ETF（資本財）", "XLB": "ETF（素材）",
    "VAW": "ETF（素材）", "XLE": "ETF（エネルギー）",
    "VDE": "ETF（エネルギー）", "XLU": "ETF（公益）",
    "VEA": "ETF（先進国除く米）", "IEFA": "ETF（先進国除く米）",
    "EFA": "ETF（先進国除く米）", "VWO": "ETF（新興国株）",
    "IEMG": "ETF（新興国株）", "EEM": "ETF（新興国株）",
    "VT": "ETF（全世界株）", "ACWI": "ETF（全世界株）",
    "VXUS": "ETF（全世界除く米）", "EWT": "ETF(台湾）",
    "EWJ": "ETF（日本）", "DXJ": "ETF（日本ヘッジ）",
    "VGK": "ETF（欧州）", "EZU": "ETF（ユーロ圏）",
    "FXI": "ETF（中国大型）", "MCHI": "ETF（中国総合）",
    "INDA": "ETF（インド）", "EPI": "ETF（インド）",
    "EWW": "ETF（メキシコ）", "EWZ": "ETF（ブラジル）",
    "BND": "ETF（債券総合）", "AGG": "ETF（債券総合）",
    "SHY": "ETF（短期国債）", "IEF": "ETF（中期国債）",
    "TLT": "ETF（長期国債）", "TIP": "ETF（物価連動債）",
    "LQD": "ETF（社債）", "HYG": "ETF（ハイイールド）",
    "BNDX": "ETF（先進国債）", "VWOB": "ETF（新興国債）",
    "GLD": "ETF（金）", "IAU": "ETF（金）",
    "SLV": "ETF（銀）", "USO": "ETF（原油）",
    "PDBC": "ETF（商品総合）", "IYR": "ETF（リート）",
    "VNQ": "ETF（リート）", "XLRE": "ETF（不動産）",
    "VNQI": "ETF（海外リート）", "BIL": "ETF（キャッシュ）"
}

STAR_TICKERS = ["CVX", "KO", "JNJ", "PG", "SPY", "VOO", "VTI", "QQQ", "VYM", "SPYD", "HDV", "DIA", "SMH", "SOXX", "TLT", "VT"]
HIGHLIGHT_TICKERS = ["SPYD", "XLF", "FRO", "DHT", "NAT", "TRMD", "HDV", "XLE", "EPI"]

def get_etf_data():
    data_list = []
    print(f"データ取得中... ({len(TICKERS_WITH_SECTOR)}銘柄)")
    for ticker, sector in TICKERS_WITH_SECTOR.items():
        try:
            t = yf.Ticker(ticker)
            # 5日分の履歴を取得して前日比を計算
            hist = t.history(period="5d")
            if hist.empty: continue
            
            latest = hist.iloc[-1]
            prev = hist.iloc[-2]
            change = ((latest["Close"] - prev["Close"]) / prev["Close"]) * 100
            
            info = t.info
            name = info.get("shortName", ticker)
            
            # 利回り
            div_yield = info.get("trailingAnnualDividendYield")
            if div_yield is None: div_yield = info.get("yield", 0)
            div_yield_pct = div_yield * 100 if div_yield else 0.0
            
            # --- 経費率取得の強化 (ここが重要) ---
            exp_ratio = None
            if "ETF" in sector:
                # Yahoo Finance APIの複数の場所から取得を試みる
                search_keys = ["expenseRatio", "annualReportExpenseRatio", "feesExpensesTotalExpenses"]
                for key in search_keys:
                    val = info.get(key)
                    if val is not None:
                        exp_ratio = val
                        break
            
            exp_ratio_pct = round(exp_ratio * 100, 2) if exp_ratio is not None else None

            data_list.append({
                "Ticker": ticker, "Name": name, "Sector": sector,
                "Price": round(latest["Close"], 2), "Change": round(change, 2),
                "Yield": round(div_yield_pct, 2),
                "Expense": exp_ratio_pct
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue
    return pd.DataFrame(data_list)

def generate_html(df):
    now = datetime.now().strftime("%y-%m-%d %H:%M")
    # 利回りの高い順にソート
    df = df.sort_values(by="Yield", ascending=False)
    
    table_rows = ""
    for _, row in df.iterrows():
        is_star = row['Ticker'] in STAR_TICKERS
        row_class = "highlight-row" if row['Ticker'] in HIGHLIGHT_TICKERS else ""
        star_icon = "★" if is_star else ""
        
        # 色付けのロジック
        change_style = "color:#dc3545;" if row['Change'] > 0 else ("color:#0d6efd;" if row['Change'] < 0 else "")
        yield_style = "color:#198754; font-weight:bold;" if row['Yield'] > 0 else ""
        
        # 経費率の表示形式
        exp_display = f"{row['Expense']}%" if row['Expense'] is not None else "-"
        tv_url = f"https://jp.tradingview.com/symbols/{row['Ticker']}/"

        table_rows += f"""
            <tr class="{row_class}">
                <td class="star-col">{star_icon}</td>
                <td class="ticker-col"><a href="{tv_url}" target="_blank" class="ticker-link"><span class="ticker-badge">{row['Ticker']}</span></a></td>
                <td class="name-col"><div class="name-text">{row['Name']}</div><div class="sector-text">{row['Sector']}</div></td>
                <td class="price-col fw-bold">${row['Price']:,.1f}</td>
                <td class="change-col fw-bold" style="{change_style}">{row['Change']:+.1f}%</td>
                <td class="yield-col" style="{yield_style}">{row['Yield']:.1f}%</td>
                <td class="exp-col">{exp_display}</td>
            </tr>"""

    # HTMLテンプレート (CSS含む)
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>米国株/ETFスクリーナー</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background:#f1f5f9; font-size: 12px; color: #333; margin: 0; display: flex; justify-content: center; font-family: -apple-system, sans-serif; }}
        .main-container {{ width: 100%; max-width: 480px; background: white; min-height: 100vh; }}
        .header {{ background:#1e293b; color:white; padding: 10px 12px; border-bottom:2px solid #3b82f6; position: sticky; top: 0; z-index: 1000; }}
        .header h1 {{ font-size: 14px; margin:0; font-weight:700; }}
        .table {{ margin:0; table-layout: fixed; width: 100%; border-collapse: collapse; }}
        .table thead th {{ 
            background:#f8fafc; font-size: 9px; padding: 6px 1px; color:#64748b; 
            position: sticky; top: 39px; z-index: 900; border-bottom: 1px solid #e2e8f0; text-align: center;
        }}
        .table td {{ padding: 6px 1px; vertical-align: middle; border-bottom: 1px solid #f1f5f9; }}
        .star-col {{ width: 5%; text-align: center; color:#f59e0b; font-size:9px; }}
        .ticker-col {{ width: 14%; text-align: center; }}
        .name-col {{ width: 33%; text-align: left; padding-left: 4px !important; }}
        .price-col {{ width: 13%; text-align: right; }}
        .change-col {{ width: 11%; text-align: right; }}
        .yield-col {{ width: 11%; text-align: right; }}
        .exp-col {{ width: 13%; text-align: right; padding-right: 6px !important; color: #64748b; font-size: 9px; }}
        .highlight-row td {{ background-color: #f0fdf4 !important; }}
        .ticker-badge {{ background:#334155; color:white; padding:1px 3px; border-radius:3px; font-size:9px; font-weight:bold; min-width: 36px; display: inline-block; text-align: center; }}
        .ticker-link {{ text-decoration: none !important; }}
        .name-text {{ font-weight:700; line-height:1.1; font-size:10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .sector-text {{ font-size:8px; color:#94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .fw-bold {{ font-weight: 700; }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header d-flex justify-content-between align-items-center">
            <h1>🇺🇸 米国株/ETF</h1>
            <div style="font-size: 10px; opacity: 0.8;">⏱ {now}</div>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th class="star-col"></th><th class="ticker-col">TKR</th>
                    <th class="name-col">銘柄/セクター</th><th class="price-col">価格</th>
                    <th class="change-col">比</th><th class="yield-col">利回</th><th class="exp-col">経費</th>
                </tr>
            </thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>
</body>
</html>"""
    with open("index.html", "w", encoding="utf-8") as f: f.write(html_content)

if __name__ == "__main__":
    df = get_etf_data()
    if not df.empty: generate_html(df)
