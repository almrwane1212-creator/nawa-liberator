import streamlit as st
import hashlib
import time

# --- 1. إعدادات الصفحة والـ SEO (يجب أن يكون أول أمر في الكود) ---
st.set_page_config(
    page_title="نوى | منصة السيادة المعرفية والبحث العميق",
    page_icon="🛡️",
    layout="wide",
    menu_items={
        'Get Help': 'https://nawa-liberator.streamlit.app',
        'About': "# نوى هي منصة للبحث العميق وتحصيل المعرفة والسيادة الرقمية وتوليد الهوية المشفرة"
    }
)

# --- 2. محرك القواعد والبيانات ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# تهيئة الذاكرة الشاملة (Session State)
if 'vault' not in st.session_state:
    st.session_state.vault = {"balance": 0, "books": 0, "videos": 0, "research": 0, "exp": 0}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# دالة لتحديد المستوى بناءً على الخبرة (EXP)
def get_rank(exp):
    if exp < 100: return "🌱 مستكشف ناشئ"
    if exp < 500: return "🛡️ محارب معرفة"
    if exp < 1500: return "📜 حكيم النواة"
    return "♾️ سيادي مطلق"

# --- 3. الواجهة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("بوابة السيادة")
    user_secret = st.text_input("مفتاح الهوية (جملة السر):", type="password")
    
    if user_secret:
        did = generate_nawa_did(user_secret)
        rank = get_rank(st.session_state.vault['exp'])
        st.success(f"الرتبة: {rank}")
        st.metric("رصيد $NAWA", f"{st.session_state.vault['balance']} 🪙")
        st.progress(min((st.session_state.vault['exp'] % 500) / 500, 1.0), text="التقدم للمستوى القادم")
    else:
        st.info("أدخل مفتاحك لبدء الاستحواذ المعرفي")

# --- 4. أقسام المنصة الرئيسية ---
tab_radar, tab_profile, tab_market, tab_social = st.tabs([
    "📡 رادار البحث العميق", "📊 ملف السيادة", "🛒 المتجر الرقمي", "💬 غرفة التنسيق"
])

# القسم 1: الرادار (البحث والتحصيل)
with tab_radar:
    st.subheader("محرك البحث السيادي")
    c1, c2 = st.columns([3, 1])
    with c1:
        topic = st.text_input("أدخل هدف الاستخراج (الموضوع):", placeholder="عن ماذا تبحث؟")
    with c2:
        dtype = st.selectbox("نوع الهدف:", ["فيديو 🎥", "كتاب PDF 📚", "بحث علمي 🔬"])

    if topic:
        queries = {
            "فيديو 🎥": f"https://www.google.com/search?q={topic}+video",
            "كتاب PDF 📚": f"https://www.google.com/search?q=filetype:pdf+{topic}",
            "بحث علمي 🔬": f"https://scholar.google.com/scholar?q={topic}"
        }
        st.link_button(f"🚀 اختراق المسار وجلب {topic}", queries[dtype])
        
        st.write("---")
        if st.button("✅ توثيق الاستحواذ (+50 EXP | +25 $NAWA)"):
            st.session_state.vault['balance'] += 25
            st.session_state.vault['exp'] += 50
            type_key = 'videos' if 'فيديو' in dtype else ('books' if 'كتاب' in dtype else 'research')
            st.session_state.vault[type_key] += 1
            st.balloons()
            st.rerun()

# القسم 2: الملف الشخصي (Profile)
with tab_profile:
    st.header(f"📊 سجل السيادة | {get_rank(st.session_state.vault['exp'])}")
    col1, col2, col3 = st.columns(3)
    col1.metric("📚 كتب مستخرجة", st.session_state.vault['books'])
    col2.metric("🎥 فيديوهات محصورة", st.session_state.vault['videos'])
    col3.metric("🔬 أبحاث موثقة", st.session_state.vault['research'])
    
    st.write("---")
    st.subheader("🛡️ الهوية الرقمية المشفرة (DID)")
    if user_secret:
        st.code(generate_nawa_did(user_secret))
        st.caption("هذا الكود هو بصمتك الفريدة في نظام نوى.")
    else:
        st.warning("أدخل الجملة السرية في القائمة الجانبية لتوليد هويتك.")

# القسم 3: المتجر (Marketplace)
with tab_market:
    st.header("🛒 تبادل القيمة")
    st.write(f"رصيدك الحالي: **{st.session_state.vault['balance']} $NAWA**")
    shop_col1, shop_col2 = st.columns(2)
    with shop_col1:
        st.info("🔓 فتح دورة مشفرة (500 $NAWA)")
        st.button("شراء الآن", key="buy1", disabled=st.session_state.vault['balance'] < 500)
    with shop_col2:
        st.warning("🔑 مفتاح المكتبة العميقة (1000 $NAWA)")
        st.button("ترقية الحساب", key="buy2", disabled=st.session_state.vault['balance'] < 1000)

# القسم 4: الدردشة (Social)
with tab_social:
    st.subheader("🌐 غرفة تنسيق المجتمع")
    chat_container = st.container(height=350)
    with chat_container:
        for msg in st.session_state.chat_history:
            st.chat_message("user").write(f"**{msg['user']}**: {msg['text']}")
    
    if prompt := st.chat_input("أرسل تحديثاً للمجتمع..."):
        if user_secret:
            u_name = generate_nawa_did(user_secret)[:8]
            st.session_state.chat_history.append({"user": u_name, "text": prompt})
            st.rerun()
        else:
            st.error("يجب تفعيل الهوية أولاً لتتمكن من الدردشة.")
        
