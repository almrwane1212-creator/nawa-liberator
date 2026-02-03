import streamlit as st
import hashlib
import time
from datetime import datetime

# --- 1. محرك النواة والهوية ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# --- 2. إعدادات المنصة ---
st.set_page_config(page_title="NAWA Social", layout="wide")

# تهيئة الذاكرة (للمتابعين والدردشة)
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'users_count' not in st.session_state:
    st.session_state.users_count = 1  # أنت الأول دائمًا

# --- 3. لوحة تحكم المسؤول (Sidebar) ---
st.sidebar.title("🛡️ إدارة النواة")
if st.sidebar.checkbox("فتح لوحة المسؤول"):
    st.sidebar.subheader("📊 إحصائيات حية")
    st.sidebar.metric("المشتركون", st.session_state.users_count)
    st.sidebar.write("آخر الهويات النشطة:")
    st.sidebar.code(f"active_did: {hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}")

st.sidebar.write("---")
user_secret = st.sidebar.text_input("جملتك السرية (الهوية):", type="password")
if user_secret:
    my_did = generate_nawa_did(user_secret)
    st.sidebar.success(f"هويتك: {my_did}")

# --- 4. واجهة الدردشة والبحث ---
st.title("🛡️ مـنصة نـوى الاجتماعية")

tab1, tab2 = st.tabs(["🔍 البحث والسيادة", "💬 غرفة الدردشة العامة"])

with tab1:
    user_topic = st.text_input("ماذا ستتعلم اليوم؟")
    if user_topic:
        st.video(f"https://www.youtube.com/embed?listType=search&list={user_topic.replace(' ', '+')}")
        if st.button("احصد المكافأة"):
            st.balloons()
            st.success("تم إضافة 5 $NAWA")

with tab2:
    st.subheader("🌐 دردشة النوايا المشتركة")
    
    # عرض الرسائل
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}**: {msg['content']}")

    # إدخال رسالة جديدة
    if prompt := st.chat_input("اكتب رسالتك هنا..."):
        user_name = my_did[:10] if user_secret else "مستخدم مجهول"
        st.session_state.messages.append({"role": "user", "user": user_name, "content": prompt})
        st.rerun()

# --- 5. نظام المتابعة (تجريبي) ---
st.write("---")
col_did, col_follow = st.columns([3, 1])
with col_did:
    st.write("👤 مستخدمون قد تهمك متابعتهم (بناءً على نيتك)")
with col_follow:
    if st.button("متابعة الكل"):
        st.toast("تمت متابعة المستخدمين بنجاح!")
