# 📊 Smart Finance Dashboard | لوحة التوقع المالي الذكية

An AI-powered forecasting dashboard for stock market and crypto analysis using deep learning and technical indicators — built with Python, Streamlit, and Firebase.  
لوحة ذكية تعتمد على الذكاء الاصطناعي لتوقع أسعار الأسهم والعملات الرقمية باستخدام التعلم العميق والمؤشرات الفنية — مبنية بلغة بايثون وStreamlit وFirebase.

---

## 🚀 Features | المميزات

- ⏱️ Real-time price forecasting (LSTM-based)  
  توقع الأسعار اللحظي باستخدام شبكات LSTM

- 📉 Technical indicators: EMA, RSI, MACD, ADX, Bollinger Bands  
  مؤشرات فنية متنوعة مثل المتوسطات، ومؤشر القوة النسبية

- 📊 Buy/Sell recommendation via CatBoost classifier  
  توصية شراء أو بيع باستخدام مصنّف ذكي

- 🔄 Price volatility & return distributions  
  تحليل التذبذب وعوائد الأسعار

- 🧾 One-click export to PDF  
  تصدير التقرير بنقرة واحدة إلى ملف PDF

- ☁️ Firebase integration  
  تكامل مع Firebase لتخزين الجلسات أو إدارة المستخدمين

---

## 🧰 Tech Stack | الأدوات المستخدمة

- **Frontend (الواجهة)**: [Streamlit](https://streamlit.io/)
- **Backend (الخوارزميات)**: Python, LSTM (TensorFlow/Keras), LightGBM, CatBoost
- **Data Sources (مصادر البيانات)**: [TwelveData](https://twelvedata.com), Alpha Vantage, Yahoo Finance
- **Storage (التخزين)**: Firebase, Local Pickle/JSON models

---

## 🧪 How to Run Locally | تشغيل المشروع محليًا

### 1. 📥 Clone the repo | انسخ المشروع

```bash
git clone https://github.com/izzeldeennahla/smart-finance-dashboard.git
cd smart-finance-dashboard
