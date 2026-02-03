import streamlit as st
import hashlib
import time

# --- 1. محرك الهوية ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# --- 2. إدارة البيانات (بدون تعقيدات خارجية) ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # تخزين الرسائل
if 'registered_users' not in st.session_state:
    st.session_state.registered_users = set()  # تخزين المشتركين

# --- 3. تصميم الواجهة ---
st.set_page_config(page_title="NAWA Network", layout="wide")
st.title("🛡️ شبكة نـوى (NAWA)")

# لوحة المسؤول الجانبية
with st.sidebar:
    st.header("⚙️ لوحة الإدارة")
    admin_pass = st.text_input("رمز المدير:", type="password")
    if admin_pass == "nawa2026":
        st.success("تم تفعيل صلاحيات المؤسس")
        st.metric("عدد المستخدمين النشطين", len(st.session_state.registered_users))
        st.write("قائمة الهويات:")
        for user in st.session_state.registered_users:
            st.code(user)
    
    st.write("---")
    user_secret = st.text_input("جملتك السرية للهوية:", type="password")
    if user_secret:
        my_did = generate_nawa_did(user_secret)
        st.session_state.registered_users.add(my_did)
        st.info(f"هويتك نشطة:\n{my_did[:15]}...")

# --- 4. الأقسام الاجتماعية ---
tab_search, tab_social = st.tabs(["🔍 محرك السيادة", "💬 غرفة الدردشة"])

with tab_search:
    topic = st.text_input("ماذا تريد أن تتعلم؟")
    if topic:
        st.video(f"https://www.youtube.com/embed?listType=search&list={topic.replace(' ', '+')}")
        if st.button("تأكيد المهمة وحصد 5 $NAWA"):
            st.balloons()
            st.toast("تمت إضافة المكافأة لمحفظتك!")

with tab_social:
    st.subheader("🌐 حائط النقاش الحر")
    
    # عرض الدردشة
    chat_container = st.container(height=300)
    for msg in st.session_state.chat_history:
        chat_container.chat_message("user").write(f"**{msg['user']}**: {msg['text']}")

    # إرسال رسالة
    if prompt := st.chat_input("اكتب رسالتك للمجتمع..."):
        if not user_secret:
            st.error("يجب تفعيل هويتك من القائمة الجانبية أولاً!")
        else:
            display_name = generate_nawa_did(user_secret)[:10]
            st.session_state.chat_history.append({"user": display_name, "text": prompt})
            st.rerun() # تحديث الصفحة لرؤية الرسالة فوراً
