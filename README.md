
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
```

### 2. 📦 Create virtual env (اختياري)

```bash
python -m venv .venv
source .venv/bin/activate  # على Linux/macOS
.venv\Scripts\activate     # على Windows
```

### 3. 🧱 Install requirements | تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### 4. 🧾 Create `.env` file | أنشئ ملف البيئة

```env
FIREBASE_API_KEY=your_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
...
```

### 5. ▶️ Run the dashboard | تشغيل التطبيق

```bash
streamlit run smart_finance_app.py
```

---

## 🌐 Deploy on Streamlit Cloud | النشر على Streamlit Cloud

1. افتح [streamlit.io/cloud](https://streamlit.io/cloud)  
2. اربط حساب GitHub واختر هذا المشروع  
3. حدّد الملف الرئيسي `smart_finance_app.py`  
4. اضغط "Deploy"

---

## 📸 Screenshots | صور من التطبيق

*(أضف صورًا من الواجهة مثل لوحة التوقع، الشارت التفاعلي، تقارير PDF)*

---

## 🔒 Security Notice | تنبيه أمني

⚠️ لا ترفع بيانات سرية (مثل مفاتيح Firebase) مباشرة داخل الكود.  
استخدم ملفات `.env` وخزّن فيها البيانات بأمان.

---

## 🙌 Author | المطوّر

تم التطوير بواسطة [@izzeldeennahla](https://github.com/izzeldeennahla) — إذا أعجبك المشروع، لا تنسَ 🌟

---

## 🪪 License | الرخصة

هذا المشروع مفتوح المصدر ومتاح بموجب رخصة MIT.
