from streamlit_gsheets import GSheetsConnection

# إنشاء اتصال بقاعدة البيانات
conn = st.connection("gsheets", type=GSheetsConnection)

def save_user_data(did, balance, exp):
    # كود لتحديث الصف الخاص بالمستخدم في Google Sheets
    df = conn.read(worksheet="Sheet1")
    # منطق التحديث (إضافة أو تعديل)
    # ... سنقوم ببرمجة التفاصيل فور تجهيزك للرابط
import streamlit as st
import hashlib
import requests
from datetime import datetime

# --- 1. إعدادات الصفحة وSEO ---
st.set_page_config(
    page_title="نوى | NAWA OS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. وظائف النظام الخلفية ---
def generate_did(secret):
    """توليد هوية رقمية مشفرة"""
    return "did:nawa:" + hashlib.sha256(secret.encode()).hexdigest()[:20]

# تهيئة بيانات الجلسة (Database البدائية)
if 'vault' not in st.session_state:
    st.session_state.vault = {"balance": 100, "exp": 0, "logs": []}
if 'chat' not in st.session_state:
    st.session_state.chat = []

# --- 3. تصميم الواجهة (CSS) لتشبه التطبيقات ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #2e7d32; color: white; border: none; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .metric-card { background: #1a1c24; padding: 15px; border-radius: 15px; border: 1px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9438/9438567.png", width=80)
    st.title("بوابة السيادة")
    user_key = st.text_input("مفتاح الدخول السري:", type="password")
    if user_key:
        my_did = generate_did(user_key)
        st.success("✅ الهوية نشطة")
        st.code(my_did, language="text")
    st.divider()
    st.info("إصدار البايثون: 3.12 | الحالة: مستقر")

# --- 5. الهيكل الرئيسي للتطبيق (Tabs) ---
tabs = st.tabs(["🔍 الرادار", "🌐 نفق العبور (VPN)", "📊 الإحصائيات", "💬 التنسيق"])

# --- TAB 1: الرادار (البحث العميق) ---
with tabs[0]:
    st.header("🔍 رادار الاستحواذ المعرفي")
    col_q, col_t = st.columns([3, 1])
    with col_q:
        query = st.text_input("ماذا تريد أن تصطاد اليوم؟", placeholder="مثال: هندسة الذكاء الاصطناعي")
    with col_t:
        category = st.selectbox("المصدر", ["كتب PDF 📚", "فيديوهات 🎥", "أبحاث 🔬"])
    
    if query:
        search_urls = {
            "كتب PDF 📚": f"https://www.google.com/search?q=filetype:pdf+{query}",
            "فيديوهات 🎥": f"https://www.youtube.com/results?search_query={query}",
            "أبحاث 🔬": f"https://scholar.google.com/scholar?q={query}"
        }
        st.link_button(f"🚀 إطلاق مسار البحث عن {query}", search_urls[category])
        
        if st.button("💰 توثيق المعرفة وحصد المكافأة"):
            st.session_state.vault['balance'] += 50
            st.session_state.vault['exp'] += 100
            st.session_state.vault['logs'].append(f"تم البحث عن {query} في {datetime.now().strftime('%H:%M')}")
            st.balloons()
            st.rerun()

# --- TAB 2: نفق العبور (المتصفح المشفر / VPN) ---
with tabs[1]:
    st.header("🛡️ نفق العبور السيادي (Proxy)")
    st.caption("تصفح المواقع من خلال سيرفرات وسيطة لحماية هويتك وتخطي الحجب.")
    
    server_list = {
        "🇩🇪 سيرفر ألمانيا": "https://api.allorigins.win/raw?url=",
        "🇺🇸 سيرفر أمريكا": "https://api.codetabs.com/v1/proxy/?quest=",
        "🌐 سيرفر عام": "https://p.ocean-proxy.com/query?url="
    }
    
    chosen_srv = st.selectbox("اختر نقطة الانطلاق:", list(server_list.keys()))
    site_url = st.text_input("أدخل رابط الموقع المستهدف:", placeholder="https://example.com")
    
    if st.button("فتح النفق الآمن ⚡"):
        if site_url:
            with st.spinner("جاري تشفير الاتصال..."):
                final_link = server_list[chosen_srv] + site_url
                st.markdown(f"""
                    <div style="border: 2px solid #2e7d32; border-radius: 15px; overflow: hidden;">
                        <iframe src="{final_link}" width="100%" height="600px" style="border:none;"></iframe>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("يرجى إدخال رابط الموقع أولاً.")

# --- TAB 3: الإحصائيات (Vault) ---
with tabs[2]:
    st.header("📊 مخزن البيانات (The Vault)")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("رصيد العملات 🪙", f"{st.session_state.vault['balance']} NAWA")
    with c2:
        st.metric("نقاط الخبرة ✨", st.session_state.vault['exp'])
    
    st.subheader("📜 سجل العمليات")
    if st.session_state.vault['logs']:
        for log in reversed(st.session_state.vault['logs']):
            st.write(f"• {log}")
    else:
        st.write("لا توجد عمليات مسجلة بعد.")

# --- TAB 4: المجتمع (Chat) ---
with tabs[3]:
    st.header("💬 غرفة تنسيق السياديين")
    if not user_key:
        st.warning("يرجى تفعيل الهوية من القائمة الجانبية للمشاركة في المحادثة.")
    else:
        # عرض الرسائل
        for m in st.session_state.chat:
            with st.chat_message("user"):
                st.write(f"**{m['sender']}**: {m['text']}")
        
        # إرسال رسالة
        if p := st.chat_input("أرسل رسالة مشفرة..."):
            st.session_state.chat.append({"sender": generate_did(user_key)[:8], "text": p})
            st.rerun()

# --- تذييل الصفحة ---
st.divider()
st.caption("نظام نـوى - مشروع سيادي مفتوح المصدر لتعزيز الاستقلال المعرفي.")
