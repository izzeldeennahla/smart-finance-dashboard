import streamlit as st
import pandas as pd
from firebase_admin import firestore

db = firestore.client()

def render_recommendations_page():
    st.subheader("📁 سجل التوصيات")
    stock_filter = st.text_input("🔎 ابحث برمز السهم")

    docs = db.collection("stock_analysis").order_by("time", direction=firestore.Query.DESCENDING).stream()
    records = [doc.to_dict() for doc in docs if stock_filter.lower() in doc.to_dict().get('stock', '').lower()]

    if records:
        st.dataframe(pd.DataFrame(records))
    else:
        st.info("📭 لا توجد توصيات متاحة حالياً.")
