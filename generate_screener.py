import yfinance as yf
import pandas as pd
from datetime import datetime

# 米国主要ETF 100選 ＋ 追加個別銘柄（重複削除済み）
TICKERS = [
    # --- 追加された高配当個別銘柄（タンカー等） ---
    "FRO", "DHT", "NAT", "TRMD",

    # --- 1. 主要株価指数 ---
    "SPY", "VOO", "IVV", "QQQ", "DIA", "IWM", "MDY", "IWB", "VTI", "ITOT",
    # --- 2. 高配当・増配・バリュー株 ---
    "VYM", "HDV", "SPYD", "DVY", "SDY", "NOBL", "VIG", "DGRW", "IVE", "VTV",
    # --- 3. グロース株・モメンタム ---
    "IVW", "VUG", "IWF", "MTUM", "ARKK", "QQQM", "RPG", "MGK", "IWY", "SPYG",
    # --- 4. セクター別（IT・ハイテク・半導体） ---
    "XLK", "IYW", "SMH", "SOXX", "VGT", "IGV", "FDN", "XSD", "SKYY",
    # --- 5. セクター別（ヘルスケア・生活必需品・通信） ---
    "XLV", "VHT", "XBI", "IBB", "XLP", "VDC", "XLC", "VOX", "IYZ", "XLY",
    # --- 6. セクター別（金融・資本財・素材・エネルギー・公益） ---
    "XLF", "VFH", "KRE", "XLI", "VIS", "XLB", "VAW", "XLE", "VDE", "XLU",
    # --- 7. 米国以外の先進国・新興国 ---
    "VEA", "IEFA", "EFA", "VWO", "IEMG", "EEM", "VT", "ACWI", "VXUS", "EWT",
    # --- 8. 特定国（日本・欧州・中国・インド等） ---
    "EWJ", "DXJ", "VGK", "EZU", "FXI", "MCHI", "INDA", "EPI", "EWW", "EWZ",
    # --- 9. 債券・キャッシュ ---
    "BND", "AGG", "SHY", "IEF", "TLT", "TIP", "LQD", "HYG", "BNDX", "VWOB",
    # --- 10. コモディティ・不動産・その他 ---
    "GLD", "IAU", "SLV", "USO", "PDBC", "IYR", "VNQ", "XLRE", "VNQI", "BIL"
]

def get_etf_data():
    data_list = []
    for ticker in TICKERS:
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
                "Price": round(latest["Close"], 2),
                "Change": round(change, 2),
                "Volume": int(latest["Volume"]),
                "Yield": round(div_yield_pct, 2)
            })
            print(f"Fetched: {ticker} (Yield: {div_yield_pct:.2f}%)")
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            
    return pd.DataFrame(data_list)

def generate_html(df):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    table_rows = ""
    for _, row in df.iterrows():
        # ハイライト対象：SPYD, XLF, FRO, DHT, NAT, TRMD
        if row['Ticker'] in ["SPYD", "XLF", "FRO", "DHT", "NAT", "TRMD"]:
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
    <title>米国ETFデイリースクリーナー</title>
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
                    <h1 class="fw-bold mb-1" style="letter-spacing: -0.5px; font-size: 1.4rem;">🇺🇸 米国ETF・株式 デイリー</h1>
                    <p class="mb-2 mb-md-0 text-white-50" style="font-size: 0.75rem;">主要銘柄のパフォーマンスと配当率を毎日自動取得</p>
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
                            <th scope="col" class="text-center" style="width: 15%;">Symbol</th>
                            <th scope="col" class="d-none d-md-table-cell" style="width: 30%;">銘柄名</th>
                            <th scope="col" class="text-end" style="width: 25%;">価格</th>
                            <th scope="col" class="text-end" style="width: 20%;">前日比</th>
                            <th scope="col" class="text-end" style="width: 20%;">配当</th>
                            <th scope="col" class="text-end d-none d-sm-table-cell" style="width: 20%;">出来高</th>
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
        df_etf = df_etf.sort_values(by="Yield", ascending=False)
        generate_html(df_etf)
        print(f"Successfully generated index.html with {len(df_etf)} items.")
    else:
        print("No data was fetched.")
