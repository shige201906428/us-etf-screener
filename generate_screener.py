import yfinance as yf
import pandas as pd
from datetime import datetime

# ピックアップしたい米国ETFのティッカーシンボル
TICKERS = [
    # --- 1. 主要株価指数（コア資産） ---
    "SPY", "VOO", "IVV", "QQQ", "DIA", "IWM", "MDY", "IWB", "VTI", "ITOT",

    # --- 2. 高配当・増配・バリュー株 ---
    "VYM", "HDV", "SPYD", "DVY", "SDY", "NOBL", "VIG", "DGRW", "IVE", "VTV",

    # --- 3. グロース株・モメンタム ---
    "IVW", "VUG", "IWF", "MTUM", "ARKK", "QQQM", "RPG", "MGK", "IWY", "SPYG",

    # --- 4. セクター別（IT・ハイテク・半導体） ---
    "XLK", "IYW", "SMH", "SOXX", "VGT", "IGV", "FDN", "XSD", "SKYY", "IYW",

    # --- 5. セクター別（ヘルスケア・生活必需品・通信） ---
    "XLV", "VHT", "XBI", "IBB", "XLP", "VDC", "XLC", "VOX", "IYZ", "XLY",

    # --- 6. セクター別（金融・資本財・素材・エネルギー・公益） ---
    "XLF", "VFH", "KRE", "XLI", "VIS", "XLB", "VAW", "XLE", "VDE", "XLU",

    # --- 7. 米国以外の先進国・新興国（グローバル） ---
    "VEA", "IEFA", "EFA", "VWO", "IEMG", "EEM", "VT", "ACWI", "VXUS", "EWT",

    # --- 8. 特定国（日本・欧州・中国・インド・新興国） ---
    "EWJ", "DXJ", "VGK", "EZU", "FXI", "MCHI", "INDA", "EPI", "EWW", "EWZ",

    # --- 9. 債券・キャッシュ（短期・中期・長期・総合） ---
    "BND", "AGG", "SHY", "IEF", "TLT", "TIP", "LQD", "HYG", "BNDX", "VWOB",

    # --- 10. コモディティ・不動産（リート）・その他 ---
    "GLD", "IAU", "SLV", "USO", "PDBC", "IYR", "VNQ", "XLRE", "VNQI", "BIL"
]

def get_etf_data():
    data_list = []
    for ticker in TICKERS:
        try:
            t = yf.Ticker(ticker)
            # 最新の履歴データを取得（2日分あれば前日比が計算可能）
            hist = t.history(period="5d")
            if hist.empty:
                continue
                
            latest = hist.iloc[-1]
            prev = hist.iloc[-2]
            
            # 前日比（％）
            change = ((latest["Close"] - prev["Close"]) / prev["Close"]) * 100
            
            # 基本情報
            info = t.info
            name = info.get("shortName", ticker)
            
            data_list.append({
                "Ticker": ticker,
                "Name": name,
                "Price": round(latest["Close"], 2),
                "Change": round(change, 2),
                "Volume": int(latest["Volume"])
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            
    return pd.DataFrame(data_list)

def generate_html(df):
    # 日本時間の日時
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # テーブル行の作成
    table_rows = ""
    for _, row in df.iterrows():
        # プラス・マイナスで色分け
        color = "text-danger" if row['Change'] >= 0 else "text-primary"
        sign = "+" if row['Change'] > 0 else ""
        
        table_rows += f"""
        <tr>
            <td><strong>{row['Ticker']}</strong></td>
            <td>{row['Name']}</td>
            <td>${row['Price']:,}</td>
            <td class="{color} font-weight-bold">{sign}{row['Change']}%</td>
            <td>{row['Volume']:,}</td>
        </tr>
        """

    # HTML全体のテンプレート
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>米国ETFデイリースクリーナー</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
        <style>
            body {{ background-color: #f8f9fa; padding-top: 20px; }}
            .card {{ border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card bg-white p-4 mb-4">
                <h1 class="text-center mb-2">🇺🇸 米国ETF ピックアップツール</h1>
                <p class="text-muted text-center">最終更新日時（JST）: {now}</p>
                <div class="table-responsive">
                    <table class="table table-hover mt-3">
                        <thead class="thead-dark">
                            <tr>
                                <th>ティッカー</th>
                                <th>銘柄名</th>
                                <th>最新価格</th>
                                <th>前日比</th>
                                <th>出来高</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # index.htmlとして保存
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    df_etf = get_etf_data()
    # 変化率（前日比）の大きい順に並び替え
    df_etf = df_etf.sort_values(by="Change", ascending=False)
    generate_html(df_etf)
    print("Successfully generated index.html")
