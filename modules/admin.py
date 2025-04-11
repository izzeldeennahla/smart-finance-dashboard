import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# تحقق من تهيئة Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("stock-ai-dashboard-firebase-adminsdk-fbsvc-8be709e0ac.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def render_admin_messages():
    st.title("📥 رسائل المستخدمين")
    msgs = db.collection("support_messages").order_by("time", direction=firestore.Query.DESCENDING).stream()
    for msg in msgs:
        data = msg.to_dict()
        with st.expander(f"📨 {data['name']} - {data['time']}"):
            st.write(data['message'])
            reply = st.text_area("✍️ الرد", key=msg.id)
            if st.button("📤 إرسال الرد", key=f"send_{msg.id}"):
                db.collection("support_messages").document(msg.id).update({"reply": reply, "admin": st.session_state.user})
                st.success("تم الرد بنجاح")

def render_admin_users():
    st.title("🧾 إدارة المستخدمين")
    users = db.collection("roles").stream()
    for u in users:
        data = u.to_dict()
        email = u.id
        name = data.get("name", "")
        role = data.get("role", "user")
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.markdown(f"**{email}** | الاسم: {name} | الصلاحية: {role}")
        if role != "admin":
            if col2.button("🛡️ ترقية لإدمن", key=email+"_admin"):
                db.collection("roles").document(email).update({"role": "admin"})
                st.success(f"تمت ترقية {email}")
                st.rerun()
        else:
            if col3.button("⬇️ تحويل لمستخدم", key=email+"_user"):
                db.collection("roles").document(email).update({"role": "user"})
                st.warning(f"تمت إزالة صلاحيات الإدمن من {email}")
                st.rerun()

def render_admin_panel():
    st.sidebar.title("📊 لوحة تحكم الإدمن")
    option = st.sidebar.radio("اختر القسم:", ["📥 رسائل المستخدمين", "🧾 إدارة المستخدمين"])
    
    if option == "📥 رسائل المستخدمين":
        render_admin_messages()
    elif option == "🧾 إدارة المستخدمين":
        render_admin_users()
