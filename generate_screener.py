import yfinance as yf
import pandas as pd
from datetime import datetime

# ピックアップしたい米国ETFのティッカーシンボル
TICKERS = [
    "SPY", "QQQ", "DIA", "IWM", "VTI", 
    "VOO", "VEU", "VWO", "IYW", "XLK", 
    "XLF", "XLV", "XLE", "GLD", "TLT"
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
