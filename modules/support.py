import streamlit as st
from firebase_admin import firestore
from datetime import datetime


def render_support_page(user_email):
    db = firestore.client()
    st.subheader("\U0001F4E8 أرسل رسالة لفريق الدعم")

    msg = st.text_area("✉️ رسالتك")
    if st.button("\U0001F4E4 إرسال"):
        db.collection("support_messages").document(datetime.now().isoformat()).set({
            "name": user_email,
            "message": msg,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success("✅ تم إرسال الرسالة بنجاح")

    st.markdown("### \U0001F4AC ردود سابقة")
    replies = db.collection("support_messages").where("name", "==", user_email).stream()
    for r in replies:
        d = r.to_dict()
        with st.expander(f"\U0001F4E8 {d['time']}"):
            st.markdown(f"**رسالتك:** {d['message']}")
            if "reply" in d:
                st.success(f"\U0001F4AC رد: {d['reply']} (بواسطة {d.get('admin', 'الإدمن')})")
            else:
                st.info("بانتظار الرد")
