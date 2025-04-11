import xgboost as xgb
import yfinance as yf
import joblib
import os
import pandas as pd

def ai_analysis(df):
    required_columns = ['EMA_20', 'EMA_200', 'RSI_14', 'ADX_14']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return 0, "❌ غير معروف", f"⚠️ الأعمدة الناقصة: {', '.join(missing)}"

    model_path = "xgb_ai_model.json"

    # تدريب النموذج إذا لم يكن موجود
    if not os.path.exists(model_path):
        df_train = yf.Ticker("AAPL").history(period="5y").reset_index()
        try:
            import pandas_ta as ta
        except ImportError:
            return 0, "❌ خطأ", "⚠️ مكتبة pandas_ta غير مثبتة"

        df_train.ta.ema(length=20, append=True)
        df_train.ta.ema(length=200, append=True)
        df_train.ta.rsi(length=14, append=True)
        df_train.ta.adx(length=14, append=True)
        df_train['target'] = (df_train['Close'].shift(-1) > df_train['Close']).astype(int)
        df_train.dropna(inplace=True)

        X = df_train[required_columns]
        y = df_train['target']

        model = xgb.XGBClassifier(n_estimators=250, max_depth=5, learning_rate=0.05, random_state=42)
        model.fit(X, y)
        model.save_model(model_path)

    # تحليل السهم
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    latest_data = df[required_columns].iloc[-1].values.reshape(1, -1)
    prediction = model.predict(latest_data)[0]
    prediction_proba = model.predict_proba(latest_data)[0][1]

    rsi = df['RSI_14'].iloc[-1]
    adx = df['ADX_14'].iloc[-1]

    if adx > 25 and 40 < rsi < 60:
        risk = "🔵 منخفض"
    elif adx > 20:
        risk = "🟡 متوسط"
    else:
        risk = "🔴 مرتفع"

    recommendation = "⏳ راقب"
    if prediction == 1 and prediction_proba > 0.6:
        recommendation = "✅ شراء"
    elif prediction == 0 and prediction_proba > 0.6:
        recommendation = "❌ بيع"

    return round(prediction_proba * 100, 2), risk, recommendation
