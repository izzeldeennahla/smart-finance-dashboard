import yfinance as yf
import pandas as pd
import pandas_ta as ta

# إعداد
ticker = 'AAPL'  # السهم اللي نستخدمه (يمكن تغييره)
period = '2y'    # المدة: سنتين من البيانات

# تحميل البيانات
df = yf.Ticker(ticker).history(period=period)
df = df.reset_index()
df.columns = ['Date','Open','High','Low','Close','Volume','Dividends','Stock Splits']

# حساب المؤشرات الفنية
df.ta.ema(length=20, append=True)
df.ta.ema(length=200, append=True)
df.ta.rsi(length=14, append=True)
df.ta.adx(length=14, append=True)

# توليد الهدف: 1 لو السهم طالع، 0 لو نازل
df['target'] = df['Close'].shift(-1) > df['Close']
df['target'] = df['target'].astype(int)

# حفظ الأعمدة النهائية فقط
final_df = df[['Date', 'Close', 'EMA_20', 'EMA_200', 'RSI_14', 'ADX_14', 'target']].dropna()

# حفظ CSV
final_df.to_csv("AAPL_training_data.csv", index=False)
print("✅ تم حفظ الملف: AAPL_training_data.csv")
