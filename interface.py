import streamlit as st
import hashlib
import time

# --- محرك الهوية (مدمج هنا لحل مشكلة الاستيراد) ---
def generate_nawa_did(user_seed):
    timestamp = str(time.time())
    raw_id = user_seed + timestamp
    return "did:nawa:" + hashlib.sha256(raw_id.encode()).hexdigest()[:24]

# --- إعدادات الواجهة ---
st.set_page_config(page_title="NAWA | النواة", page_icon="🛡️", layout="centered")

st.title("🛡️ مـنصة نـوى (NAWA)")
st.subheader("استعد سيادتك الرقمية الآن")

# القسم الأول: الهوية
st.sidebar.header("بوابة الهوية")
user_secret = st.sidebar.text_input("أدخل جملتك السرية لتوليد الـ DID:", type="password")

if user_secret:
    did = generate_nawa_did(user_secret)
    st.sidebar.success(f"معرفك اللامركزي نشط:\n{did}")

# القسم الثاني: واجهة النية
st.write("---")
st.header("ماذا تريد أن تنجز الآن؟")
col1, col2 = st.columns(2)

with col1:
    intent = st.selectbox("اختر نيتك:", ["تعلم مهارة", "استكشاف إبداعي", "ترفيه واعٍ", "تواصل هادف"])

with col2:
    duration = st.slider("كم دقيقة تخصص لهذه النية؟", 5, 120, 20)

if st.button("تفعيل وكيل نوى الذكي"):
    st.balloons()
    st.info(f"🚀 تم عزل المشتتات. وكيلك الذكي يحلل الويب لخدمة نيتك في ({intent}).")
    
    with st.spinner('جاري الاتصال بالشبكة اللامركزية...'):
        time.sleep(2)
        st.write("### 💎 نتائج منقية لك:")
        st.checkbox("محتوى مقترح 1: مقدمة في الويب 3")
        st.checkbox("محتوى مقترح 2: كيف تسيطر على وقتك")
        
