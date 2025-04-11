import streamlit as st
st.set_page_config(page_title="Smart AI Forecast", layout="wide", initial_sidebar_state="expanded")

import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from firebase_config import firebase_config
import os, json
# -------------------- Firebase Auth Init --------------------
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# 🔐 Load credentials from Streamlit secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

# 💾 Firestore
db = firestore.client()


# -------------------- Load Session --------------------
session_file = "session.json"
if os.path.exists(session_file):
    with open(session_file, "r") as f:
        data = json.load(f)
        st.session_state.user = data.get("user")
        st.session_state.user_role = data.get("role")
        st.session_state.name = data.get("name")
else:
    st.session_state.user = None
    st.session_state.user_role = None
    st.session_state.name = ""

# -------------------- Login Form --------------------
def login_form():
    st.title("🔐 تسجيل الدخول")
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب"])

    with tab1:
        with st.form("login_form_inner"):
            email = st.text_input("📧 البريد الإلكتروني")
            password = st.text_input("🔑 كلمة المرور", type="password")
            submitted = st.form_submit_button("تسجيل الدخول")
            if submitted:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    role_doc = db.collection("roles").document(email).get()
                    if role_doc.exists:
                        data = role_doc.to_dict()
                        st.session_state.user = email
                        st.session_state.user_role = data.get("role", "user")
                        st.session_state.name = data.get("name", "")
                        with open(session_file, "w") as f:
                            json.dump({
                                "user": email,
                                "role": st.session_state.user_role,
                                "name": st.session_state.name
                            }, f)
                        st.success(f"مرحبًا {email}")
                        st.rerun()
                    else:
                        st.error("لا يوجد حساب مرتبط")
                except:
                    st.error("بيانات تسجيل الدخول غير صحيحة")

    with tab2:
        with st.form("signup_form"):
            new_email = st.text_input("✉️ بريد إلكتروني جديد", key="new_email")
            new_pass = st.text_input("🔐 كلمة المرور الجديدة", type="password", key="new_pass")
            new_name = st.text_input("🧑 الاسم الكامل", key="new_name")
            submitted2 = st.form_submit_button("إنشاء الحساب")
            if submitted2:
                try:
                    user = auth.create_user_with_email_and_password(new_email, new_pass)
                    db.collection("roles").document(new_email).set({
                        "name": new_name,
                        "role": "user"
                    })
                    st.success("✅ تم إنشاء الحساب بنجاح. يرجى تسجيل الدخول")
                    st.rerun()
                except:
                    st.error("حدث خطأ أثناء إنشاء الحساب")

# -------------------- Show login form if not logged in --------------------
if not st.session_state.user:
    login_form()
    st.stop()

# -------------------- Logout Button --------------------
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.user = None
    st.session_state.user_role = None
    st.session_state.name = ""
    if os.path.exists(session_file):
        os.remove(session_file)
    st.rerun()

# -------------------- Sidebar & Pages --------------------
st.sidebar.success(f"مرحبًا {st.session_state.name}")

# قائمة الصفحات حسب الدور
if st.session_state.user_role == "admin":
    options = [
        "📥 رسائل المستخدمين",
        "🧾 إدارة المستخدمين",
        "📊 التحليل الفني",
        "🗂️ سجل التوصيات",
        "💬 تواصل مع فريق الدعم",
        "📈 توقعات السوق AI",
        "🔮 توقع الأسعار المستقبلية"
    ]
else:
    options = [
        "📊 التحليل الفني",
        "🗂️ سجل التوصيات",
        "💬 تواصل مع فريق الدعم",
        "📈 توقعات السوق AI",
        "🔮 توقع الأسعار المستقبلية"
    ]

selected_page = st.sidebar.radio("📄 اختر الصفحة", options)

# -------------------- استدعاء الصفحات --------------------
from modules.trading import render_trading_page
from modules.recommendations import render_recommendations_page
from modules.support import render_support_page
from modules.admin import render_admin_messages, render_admin_users
from modules.market_forecast import render_market_forecast_page
from modules.forecast_ai import render_twelve_data_forecast

if selected_page == "📊 التحليل الفني":
    render_trading_page()
elif selected_page == "🗂️ سجل التوصيات":
    render_recommendations_page()
elif selected_page == "💬 تواصل مع فريق الدعم":
    render_support_page(st.session_state.user)
elif selected_page == "📈 توقعات السوق AI":
    render_market_forecast_page()
elif selected_page == "🔮 توقع الأسعار المستقبلية":
    render_twelve_data_forecast()
elif selected_page == "📥 رسائل المستخدمين":
    render_admin_messages()
elif selected_page == "🧾 إدارة المستخدمين":
    render_admin_users()
