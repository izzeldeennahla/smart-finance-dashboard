
# 📊 Smart Finance Dashboard

An AI-powered forecasting dashboard for stock market and crypto analysis using deep learning and technical indicators — built with Python, Streamlit, and Firebase.

---

## 🚀 Features

- ⏱️ Real-time price forecasting using deep learning (LSTM)
- 📉 Technical indicators: EMA, RSI, MACD, ADX, Bollinger Bands
- 📊 Buy/Sell recommendations using CatBoost classifier
- 🔄 Volatility analysis & return distribution histograms
- 🧾 Export full forecast reports in PDF format
- ☁️ Firebase integration for session logging or data storage

> ⚠️ This dashboard includes **multiple AI-based forecasting modules**, each with **its own model, source code logic, and data source**.
> Forecast results and recommendations vary across modules depending on the strategy, AI model, and market data source.

---

## 🧰 Tech Stack

- **Frontend**: Streamlit
- **AI Models**: LSTM (TensorFlow/Keras), LightGBM, CatBoost
- **Data APIs**: TwelveData, Alpha Vantage, Yahoo Finance
- **Storage**: Firebase, Pickle, JSON

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/izzeldeennahla/smart-finance-dashboard.git
cd smart-finance-dashboard
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Add a `.env` file:
```env
FIREBASE_API_KEY=your_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
...
```

### Then run the app:
```bash
streamlit run smart_finance_app.py
```

---

## 🌐 Deploy on Streamlit Cloud

1. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
2. Connect your GitHub and select the repo
3. Set `smart_finance_app.py` as the main file
4. Click **Deploy**

---

## 📸 Application Screenshots

### 🧭 Sidebar Menu
![Sidebar Menu](assets/screenshots/sidebar_dashboard_menu.png)

### 🔍 Stock Symbol & Filters
![Symbol Filters](assets/screenshots/sidebar_symbol_and_filters.png)

### 📊 Technical Analysis View + TradingView Chart
![Technical Analysis](assets/screenshots/technical_analysis_dashboard.png)

### 📋 Recommendations Log
![Recommendations](assets/screenshots/recommendations_log.png)

### 📬 Contact Support Page
![Support Contact](assets/screenshots/support_contact_page.png)

### 🤖 AI Market Forecast Page
![AI Forecast](assets/screenshots/ai_market_forecast_page.png)

### 📈 Forecast Summary View
![Forecast Summary](assets/screenshots/forecast_summary_page.png)

### 💹 Interactive Chart
![Interactive Chart](assets/screenshots/interactive_chart.png)

### 🧮 Raw Data Table
![Raw Data](assets/screenshots/raw_data_table.png)

### 📨 Export PDF Section
![Export PDF](assets/screenshots/export_pdf_section.png)

### 📄 Forecast PDF Report Sample
![PDF Report](assets/screenshots/forecast_pdf_report.png)

### 📊 Prediction vs Reality + Standard Deviation
![prediction_vs_reality_and_std_chart.pdf.png)


---

## 🔐 Security Notice

Please do not upload your real Firebase keys or API credentials publicly. Use `.env` files to store secrets safely.

---

## 🙌 Author

Developed by [@izzeldeennahla](https://github.com/izzeldeennahla) — feel free to contribute or star ⭐ this project.

---

## 🪪 License

Open-source under the MIT License.
