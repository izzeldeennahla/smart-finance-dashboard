import streamlit as st
import pandas as pd
import requests
import pandas_ta as ta
import numpy as np
import lightgbm as lgb
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from streamlit_autorefresh import st_autorefresh
import uuid

API_KEY = "c4091513f5b543648761168b52cbada3"
BASE_URL = "https://api.twelvedata.com"

@st.cache_data(ttl=60)
def get_historical_data(symbol, interval="1h", outputsize=500):
    url = f"{BASE_URL}/time_series?symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}&format=JSON"
    res = requests.get(url)
    data = res.json()
    if "values" not in data:
        return pd.DataFrame()
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime")
    df = df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    })
    float_cols = ["Open", "High", "Low", "Close"]
    if "volume" in data["values"][0]:
        float_cols.append("Volume")
    df[float_cols] = df[float_cols].astype(float)
    return df

def detect_market(symbol):
    symbol = symbol.upper().replace("/", "")
    manual_map = {
        "BTCUSD": "BINANCE:BTCUSDT",
        "ETHUSD": "BINANCE:ETHUSDT",
        "BNBUSD": "BINANCE:BNBUSDT",
        "DOGEUSD": "BINANCE:DOGEUSDT"
    }
    if symbol in manual_map:
        return manual_map[symbol]
    if symbol.startswith("USD") or symbol.startswith("EUR") or symbol.endswith("JPY"):
        return f"FOREX:{symbol}"
    elif symbol.endswith("USDT") or "BTC" in symbol or "ETH" in symbol:
        return f"BINANCE:{symbol}"
    elif symbol.isalpha() and len(symbol) <= 5:
        return f"NASDAQ:{symbol}"
    else:
        return symbol

def render_twelve_data_forecast():
    # استخدام مفتاح UUID لضمان التفرد وعدم التكرار
    count = st_autorefresh(interval=60000, key=str(uuid.uuid4()))

    if count > 0:
        st.toast("📡 تم تحديث البيانات تلقائيًا!", icon="🔄")

    # باقي الكود كما هو بدون تغيير...
    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Settings")
    symbol = st.sidebar.text_input("Enter Symbol (e.g., AAPL, BTC/USD)", value="AAPL")
    interval = st.sidebar.selectbox("Interval", ["1min", "5min", "15min", "1h", "1day"], index=3)
    forecast_days = st.sidebar.selectbox("Forecast Steps Ahead", [1, 3, 5, 7, 14,30], index=2)

    st.title("📊 AI-Powered Forecast Dashboard")
    tabs = st.tabs(["📈 Forecast", "📊 Chart", "📋 Data", "📤 Export"])

    df = get_historical_data(symbol, interval=interval)
    if df.empty or len(df) < 100:
        st.error("Not enough data or invalid symbol.")
        return

    df.ta.ema(length=20, append=True)
    df.ta.ema(length=200, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.adx(length=14, append=True)
    df.ta.macd(append=True)
    df.ta.bbands(append=True)
    df.dropna(inplace=True)

    df['Target_Price'] = df['Close'].shift(-forecast_days)
    df['Target_Class'] = (df['Target_Price'] > df['Close']).astype(int)
    df.dropna(inplace=True)

    features = ["EMA_20", "EMA_200", "RSI_14", "ADX_14", "MACD_12_26_9", "BBL_5_2.0", "BBU_5_2.0"]
    X = df[features]
    y_cls = df['Target_Class']

    model_cls = CatBoostClassifier(iterations=300, learning_rate=0.05, depth=6, verbose=0, random_seed=42)
    model_cls.fit(X, y_cls)

    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df[features])
    sequence_length = 10
    X_seq, y_seq = [], []
    for i in range(len(scaled_features) - sequence_length - forecast_days):
        X_seq.append(scaled_features[i:i+sequence_length])
        y_seq.append(scaled_features[i+sequence_length + forecast_days - 1][features.index("EMA_20")])

    X_seq, y_seq = np.array(X_seq), np.array(y_seq)
    X_train_seq, X_test_seq, y_train_seq, y_test_seq = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

    model_lstm = Sequential()
    model_lstm.add(LSTM(64, return_sequences=False, input_shape=(X_seq.shape[1], X_seq.shape[2])))
    model_lstm.add(Dropout(0.2))
    model_lstm.add(Dense(1))
    model_lstm.compile(optimizer='adam', loss='mse')
    model_lstm.fit(X_train_seq, y_train_seq, epochs=20, batch_size=16, verbose=0)

    last_sequence = scaled_features[-sequence_length:]
    last_sequence = np.expand_dims(last_sequence, axis=0)
    forecast_scaled = model_lstm.predict(last_sequence)[0][0]
    forecast_price = scaler.inverse_transform(
        [[0]*features.index("EMA_20") + [forecast_scaled] + [0]*(len(features) - features.index("EMA_20") -1)]
    )[0][features.index("EMA_20")]

    y_pred = model_lstm.predict(X_test_seq)
    rmse = np.sqrt(mean_squared_error(y_test_seq, y_pred))
    mae = mean_absolute_error(y_test_seq, y_pred)

    current_price = df['Close'].iloc[-1]
    diff = forecast_price - current_price
    movement_pred = model_cls.predict(df[features].iloc[-1:].values)[0]
    advice = "Buy" if movement_pred == 1 else "Sell"

    std_dev = df['Close'].std()
    returns = df['Close'].pct_change().dropna()
    fig_std, ax = plt.subplots(figsize=(5, 3))
    ax.hist(returns, bins=30, density=True, alpha=0.6, color='steelblue')
    mean, std = returns.mean(), returns.std()
    x = np.linspace(returns.min(), returns.max(), 100)
    pdf_line = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean)/std)**2)
    ax.plot(x, pdf_line, color='darkblue', linewidth=2)
    ax.set_title('Returns Distribution')
    os.makedirs("temp", exist_ok=True)
    std_chart_path = "temp/std_dist.png"
    plt.tight_layout()
    plt.savefig(std_chart_path, dpi=300)
    plt.close()

    with tabs[0]:
        st.header("📈 Forecast Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${round(current_price, 2)}")
        delta_color = "normal"
        col2.metric(f"Forecast ({forecast_days} steps)", f"${round(forecast_price, 2)}", delta=round(diff, 2), delta_color=delta_color)
        col3.metric("Trend", "Up" if movement_pred else "Down")
        st.markdown(f"""
        ### Recommendation
        - **{advice}**
        ### Accuracy
        - RMSE(Root Mean Squared Error): `{rmse:.4f}`
        - MAE(mean absolute error): `{mae:.4f}`
        ### Volatility
        - Std Dev (Close): `{std_dev:.4f}`
        """)
        st.image(std_chart_path, width=480)

    with tabs[1]:
        st.header("📊 Interactive Chart")
        symbol_exchange = detect_market(symbol)
        widget_code = f'''
        <div class="tradingview-widget-container" style="width: 100%; height: 800px;">
          <div id="tradingview_chart"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js">
          {{
            "width": "100%",
            "height": "800",
            "symbol": "{symbol_exchange}",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "details": true,
            "calendar": true,
            "support_host": "https://www.tradingview.com"
          }}
          </script>
        </div>
        '''
        st.components.v1.html(widget_code, height=820)

    # تبويب 📋 Data
    with tabs[2]:
        st.header("📋 Raw Data Table")
        st.dataframe(df.tail(30).round(2))

    # دالة حفظ الجدول كصورة
    def save_table_image(df, filename="table.png"):
        fig, ax = plt.subplots(figsize=(10, min(1 + 0.4 * len(df), 12)))
        ax.axis('off')
        table = ax.table(cellText=df.round(2).values, colLabels=df.columns, loc='center', cellLoc='center')
        table.scale(1.2, 1.2)
        plt.tight_layout()
        os.makedirs("temp", exist_ok=True)
        filepath = os.path.join("temp", filename)
        plt.savefig(filepath, dpi=300)
        plt.close()
        return filepath

    # دالة توليد تقرير PDF
    def generate_pdf(symbol, current, forecast, diff, rmse, mae, movement, advice, chart_path, table_path, compare_path, std_chart_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Forecast Report - {symbol}", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Current Price: ${round(current, 2)}", ln=True)
        pdf.cell(200, 10, txt=f"Forecasted Price: ${round(forecast, 2)}", ln=True)
        pdf.cell(200, 10, txt=f"Difference: {round(diff, 2)}", ln=True)
        pdf.cell(200, 10, txt=f"RMSE: {round(rmse, 2)}", ln=True)
        pdf.cell(200, 10, txt=f"MAE: {round(mae, 2)}", ln=True)
        pdf.cell(200, 10, txt=f"Predicted Movement: {'Up' if movement else 'Down'}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Recommendation: {advice}")
        if chart_path and os.path.exists(chart_path):
            pdf.image(chart_path, x=10, w=190)
        if table_path and os.path.exists(table_path):
            pdf.add_page()
            pdf.cell(200, 10, txt="Raw Data", ln=True)
            pdf.image(table_path, x=10, w=190)
        if compare_path and os.path.exists(compare_path):
            pdf.add_page()
            pdf.cell(200, 10, txt="Prediction vs Reality", ln=True)
            pdf.image(compare_path, x=10, w=190)
        if std_chart_path and os.path.exists(std_chart_path):
            pdf.add_page()
            pdf.cell(200, 10, txt="Standard Deviation Chart", ln=True)
            pdf.image(std_chart_path, x=10, w=190)
        filename = f"report_{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf.output(filename)
        for f in [chart_path, table_path, compare_path, std_chart_path]:
            if os.path.exists(f): os.remove(f)
        return filename

    # تبويب 📤 Export
    with tabs[3]:
        st.header("📤 Export Report")
        compare_df = pd.DataFrame({
            "Actual Price": scaler.inverse_transform(
                np.pad(y_test_seq.reshape(-1, 1), ((0, 0), (features.index("EMA_20"), len(features) - features.index("EMA_20") - 1)), 'constant'))[:, features.index("EMA_20")],
            "Predicted Price": scaler.inverse_transform(
                np.pad(y_pred.reshape(-1, 1), ((0, 0), (features.index("EMA_20"), len(features) - features.index("EMA_20") - 1)), 'constant'))[:, features.index("EMA_20")]
        })
        compare_df["Difference"] = compare_df["Predicted Price"] - compare_df["Actual Price"]
        fig = go.Figure(data=[go.Candlestick(
            x=df['datetime'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick'
        )])
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['EMA_20'], name='EMA 20'))
        fig.add_trace(go.Scatter(x=df['datetime'], y=df['EMA_200'], name='EMA 200'))
        fig.update_layout(title='Price Chart', xaxis_title='Date', yaxis_title='Price')
        fig.write_image("chart_temp.png")

        table_path = save_table_image(df[['datetime', 'Open', 'High', 'Low', 'Close'] + features].tail(30))
        compare_path = save_table_image(compare_df.tail(15), filename="compare_temp.png")
        filename = generate_pdf(symbol, current_price, forecast_price, diff, rmse, mae, movement_pred, advice,
                                "chart_temp.png", table_path, compare_path, std_chart_path)
        with open(filename, "rb") as f:
            st.download_button("Download PDF Report", f, file_name=filename)
        os.remove(filename)

render_twelve_data_forecast()
