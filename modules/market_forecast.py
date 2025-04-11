import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import mean_squared_error

def render_market_forecast_page():
    st.title("🤖 صفحة توقعات السوق بالذكاء الاصطناعي")

    # إدخال المستخدم
    symbols = st.text_input("🔍 أدخل رموز الأسهم مفصولة بفاصلة (مثال: AAPL,MSFT,GOOGL)", "AAPL,MSFT,GOOGL")
    period = st.selectbox("⏳ الفترة الزمنية", ["6mo", "1y", "2y", "5y"])

    # معالجة البيانات
    @st.cache_data
    def get_features(symbol, period):
        df = yf.Ticker(symbol).history(period=period).reset_index()
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=200, append=True)
        df.ta.rsi(length=14, append=True)
        df.ta.adx(length=14, append=True)
        df.dropna(inplace=True)
        df['target_cls'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        df['target_reg'] = df['Close'].shift(-1)
        df['symbol'] = symbol
        return df[['Date', 'symbol', 'EMA_20', 'EMA_200', 'RSI_14', 'ADX_14', 'Close', 'target_cls', 'target_reg']]

    all_data = []
    for sym in [s.strip() for s in symbols.split(",")]:
        try:
            all_data.append(get_features(sym, period))
        except:
            st.warning(f"⚠️ تعذر تحميل البيانات لـ {sym}")

    if not all_data:
        st.stop()

    df = pd.concat(all_data)

    # ---------------------- تدريب النموذج ----------------------
    st.info("📊 تدريب النماذج... الرجاء الانتظار")
    features = ['EMA_20', 'EMA_200', 'RSI_14', 'ADX_14']
    df.dropna(inplace=True)

    # التصنيف (شراء/بيع)
    X_cls = df[features]
    y_cls = df['target_cls']
    X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(X_cls, y_cls, test_size=0.3, random_state=42)
    model_cls = xgb.XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss')
    model_cls.fit(X_train_cls, y_train_cls)

    # التنبؤ بالقيمة المستقبلية (السعر)
    X_reg = df[features]
    y_reg = df['target_reg']
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.3, random_state=42)
    model_reg = xgb.XGBRegressor(n_estimators=100)
    model_reg.fit(X_train_reg, y_train_reg)

    # ---------------------- عرض النتائج ----------------------
    report = classification_report(y_test_cls, model_cls.predict(X_test_cls), output_dict=True)
    st.success("✅ تم تدريب النماذج بنجاح")
    st.write("**📈 دقة نموذج التوصية:**", round(report['accuracy'] * 100, 2), "%")
    mse = mean_squared_error(y_test_reg, model_reg.predict(X_test_reg))
    rmse = np.sqrt(mse)
    st.write("📉 متوسط خطأ التوقع السعري (RMSE):", round(rmse, 2))

    # ---------------------- توقعات ----------------------
    st.subheader("📋 توقعات وتحليل الأسهم")
    latest = df.groupby("symbol").tail(1).copy()
    latest['prediction_cls'] = model_cls.predict(latest[features])
    latest['confidence'] = model_cls.predict_proba(latest[features])[:, 1]
    latest['predicted_price'] = model_reg.predict(latest[features])
    latest['المخاطرة'] = latest.apply(
        lambda row: "🔵 منخفض" if row['ADX_14'] > 25 and 40 < row['RSI_14'] < 60
        else ("🟡 متوسط" if row['ADX_14'] > 20 else "🔴 مرتفع"), axis=1
    )

    def get_advice(row):
        change = (row['predicted_price'] - row['Close']) / row['Close']
        if change > 0.05:
            return "📈 يتوقع ارتفاع كبير - فرصة شراء"
        elif change < -0.05:
            return "📉 يتوقع انخفاض - يوصى بالبيع"
        else:
            return "⏳ تغير طفيف - يفضل المراقبة"

    latest['التوصية'] = latest['prediction_cls'].apply(lambda x: "✅ شراء" if x == 1 else "❌ بيع")
    latest['الثقة'] = (latest['confidence'] * 100).round(2).astype(str) + "%"
    latest['المتوقع'] = latest['predicted_price'].round(2)
    latest['التوصية النصية'] = latest.apply(get_advice, axis=1)

    st.dataframe(latest[['symbol', 'Close', 'المتوقع', 'الثقة', 'التوصية', 'المخاطرة', 'التوصية النصية']].set_index('symbol'))

    # ---------------------- رسم بياني ----------------------
    st.subheader("📉 الرسم البياني للسعر")
    selected = st.selectbox("اختر سهمًا لعرضه", latest['symbol'].unique())
    df_chart = yf.Ticker(selected).history(period=period).reset_index()
    fig = go.Figure(data=[go.Candlestick(x=df_chart['Date'],
                                         open=df_chart['Open'], high=df_chart['High'],
                                         low=df_chart['Low'], close=df_chart['Close'])])
    fig.update_layout(title=f"📊 الشارت الفني - {selected}",
                      xaxis_title="التاريخ", yaxis_title="السعر")
    st.plotly_chart(fig, use_container_width=True)
