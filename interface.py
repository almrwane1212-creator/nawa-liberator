import streamlit as st
import hashlib

# --- 1. إعدادات المحركات والـ SEO ---
st.set_page_config(
    page_title="نوى | NAWA OS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed" # لجعلها تبدو كالموبايل عند الفتح
)

# دالة الهوية الرقمية
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# تهيئة البيانات
if 'vault' not in st.session_state:
    st.session_state.vault = {"balance": 0, "books": 0, "videos": 0, "research": 0, "exp": 0}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- 2. التصميم الجمالي (CSS) لجعلها تشبه التطبيقات ---
st.markdown("""
    <style>
    .main { background: linear-gradient(180deg, #0e1117 0%, #1a1c24 100%); }
    div[st-decorator="true"] { display: none; }
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #4CAF50;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. القائمة الجانبية (لوحة التحكم) ---
with st.sidebar:
    st.title("🛡️ بوابة نوى")
    user_secret = st.text_input("مفتاحك السري (ID):", type="password")
    if user_secret:
        did = generate_nawa_did(user_secret)
        st.success(f"الهوية نشطة")
        st.metric("رصيدك الحالي", f"{st.session_state.vault['balance']} 🪙")
    st.divider()
    st.caption("إصدار المنصة: v2.5 Stable")

# --- 4. الواجهة الرئيسية (التنقل السريع) ---
st.write("# 🛡️ مـنصة نـوى")
st.caption("نظام الاستحواذ المعرفي والبحث العميق")

tabs = st.tabs(["🔍 الرادار", "👤 هويتي", "💬 المجتمع", "🛒 المتجر"])

# --- قسم الرادار ---
with tabs[0]:
    col_input, col_type = st.columns([3, 1])
    with col_input:
        topic = st.text_input("ماذا سنستكشف اليوم؟", placeholder="اكتب موضوع البحث هنا...")
    with col_type:
        dtype = st.selectbox("النوع", ["فيديو 🎥", "كتاب PDF 📚", "بحث علمي 🔬"])

    if topic:
        queries = {
            "فيديو 🎥": f"https://www.google.com/search?q={topic}+video",
            "كتاب PDF 📚": f"https://www.google.com/search?q=filetype:pdf+{topic}",
            "بحث علمي 🔬": f"https://scholar.google.com/scholar?q={topic}"
        }
        st.link_button(f"🚀 فتح مسار {topic}", queries[dtype], use_container_width=True)
        
        if st.button("📦 توثيق الاستحواذ وحصد المكافأة"):
            st.session_state.vault['balance'] += 25
            st.session_state.vault['exp'] += 50
            st.balloons()
            st.rerun()

# --- قسم الملف الشخصي ---
with tabs[1]:
    st.subheader("📊 إحصائيات السيادة")
    c1, c2, c3 = st.columns(3)
    c1.metric("📚 كتب", st.session_state.vault['books'])
    c2.metric("🎥 فيديو", st.session_state.vault['videos'])
    c3.metric("✨ خبرة", st.session_state.vault['exp'])
    
    if user_secret:
        st.info(f"كود الهوية DID: {generate_nawa_did(user_secret)}")

# --- قسم الدردشة ---
with tabs[2]:
    st.subheader("🌐 تنسيق المجتمع")
    for msg in st.session_state.chat_history:
        st.chat_message("user").write(f"**{msg['user']}**: {msg['text']}")
    
    if prompt := st.chat_input("تحدث مع السياديين..."):
        if user_secret:
            u_name = generate_nawa_did(user_secret)[:8]
            st.session_state.chat_history.append({"user": u_name, "text": prompt})
            st.rerun()

# --- قسم المتجر ---
with tabs[3]:
    st.subheader("🛒 المتجر الرقمي")
    st.write("حول رصيدك إلى ميزات!")
    st.button("🔓 فتح أدوات البحث المتقدم (500 🪙)", disabled=True)
    
