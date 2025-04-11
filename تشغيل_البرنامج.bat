@echo off
cd /d "%~dp0"
C:\Users\C-ROAD\AppData\Local\Programs\Python\Python312\python.exe -m streamlit run smart_finance_app.py --browser.gatherUsageStats=false --server.headless=true
