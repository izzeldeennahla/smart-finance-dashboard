import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objs as go
from helpers.ai_utils import ai_analysis
from tradingview_ta import TA_Handler, Interval, Exchange

def get_tradingview_signal(symbol):
    try:
        handler = TA_Handler(
            symbol=symbol.upper(),
            screener="america",  # يمكن تغييره إلى "crypto" أو "forex"
            exchange="NASDAQ",   # حسب السوق (مثلاً BINANCE للعملات الرقمية)
            interval=Interval.INTERVAL_1_DAY
        )
        analysis = handler.get_analysis()
        return analysis.summary['RECOMMENDATION']
    except Exception as e:
        return f"❌ خطأ في جلب التوصية: {e}"

def render_trading_page():
    stock = st.sidebar.text_input("رمز السهم أو الأصل المالي", "AAPL")
    period = st.sidebar.selectbox("الفترة الزمنية", ('1mo','3mo','6mo','1y','2y','5y','10y'))
    show_data = st.sidebar.checkbox("📋 عرض البيانات")
    show_chart = st.sidebar.checkbox("📉 عرض الرسم البياني")
    show_tradingview = st.sidebar.checkbox("📈 TradingView")

    df = yf.Ticker(stock).history(period=period).reset_index()
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=200, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.adx(length=14, append=True)
    df = df.dropna()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['time'] = df['Date'].dt.strftime('%Y-%m-%d')

    # تحليل الذكاء الاصطناعي
    proba, risk, reco = ai_analysis(df)

    # توصية TradingView
    tv_signal = get_tradingview_signal(stock)

    st.subheader("📊 النتائج الفنية")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🤖 توصية AI")
        st.write(f"**التوصية:** {reco}")
        st.write(f"**الثقة:** {round(proba * 100, 2)}%")
        st.write(f"**المخاطرة:** {risk}")

    with col2:
        st.markdown("### 📈 توصية TradingView")
        st.write(f"**الحالة العامة:** `{tv_signal}`")

    with st.expander("📘 شرح معنى التوصيات"):
        st.markdown("""
        - ✅ شراء: المؤشرات والنموذج يتوقعان ارتفاعًا.
        - ❌ بيع: المؤشرات تشير إلى انخفاض.
        - ⏳ راقب: لا يوجد اتجاه واضح.
        - STRONG_BUY / STRONG_SELL: من TradingView = توصية قوية.
        """)

    if show_chart:
        fig = go.Figure(data=[go.Candlestick(
            x=df['time'], open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='Candlestick')])
        fig.add_trace(go.Scatter(x=df['time'], y=df['EMA_20'], name='EMA20'))
        fig.add_trace(go.Scatter(x=df['time'], y=df['EMA_200'], name='EMA200'))
        fig.update_layout(
            title="📉 الشارت الفني",
            xaxis_title="التاريخ",
            yaxis_title="السعر",
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)

    if show_data:
        st.dataframe(df.tail(20))

    if show_tradingview:
        st.subheader("📈 الرسم التفاعلي من TradingView")
        st.markdown(
            f"""
            <iframe src="https://www.tradingview.com/widgetembed/?symbol=NASDAQ%3A{stock.upper()}&interval=D&theme=light&style=1&timezone=Etc%2FUTC&locale=ar&hide_side_toolbar=true&hide_top_toolbar=true" width="100%" height="500" frameborder="0"></iframe>
            """,
            unsafe_allow_html=True
        )
