import streamlit as st
import hashlib
import requests
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. إعدادات الصفحة وجماليات الواجهة ---
st.set_page_config(
    page_title="نوى | NAWA OS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تصميم CSS لتحويل الواجهة إلى نمط "تطبيق موبايل"
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #2e7d32; color: white; height: 50px; font-weight: bold; }
    .metric-card { background: #1a1c24; padding: 20px; border-radius: 15px; border: 1px solid #2e7d32; text-align: center; }
    div[data-testid="stMetricValue"] { color: #4CAF50; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. وظائف الربط مع قاعدة البيانات (Google Sheets) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def sync_user_data(did):
    """جلب بيانات المستخدم أو إنشاء سجل جديد في جوجل شيت"""
    try:
        df = conn.read(ttl=0) # قراءة البيانات الحالية (بدون تخزين مؤقت)
        if did in df['DID'].astype(str).values:
            user_row = df[df['DID'] == did].iloc[0]
            return int(user_row['Balance']), int(user_row['Exp'])
        else:
            # إضافة مستخدم جديد بـ 100 عملة ترحيبية
            new_user = pd.DataFrame([{"DID": did, "Balance": 100, "Exp": 0}])
            updated_df = pd.concat([df, new_user], ignore_index=True)
            conn.update(data=updated_df)
            return 100, 0
    except Exception as e:
        # في حال فشل الربط، استخدام قيم افتراضية مؤقتة
        return 100, 0

def update_user_stats(did, new_balance, new_exp):
    """تحديث النقاط في جدول جوجل"""
    try:
        df = conn.read(ttl=0)
        df.loc[df['DID'] == did, ['Balance', 'Exp']] = [new_balance, new_exp]
        conn.update(data=df)
    except:
        pass

# --- 3. المنطق الخلفي للهوية ---
def generate_did(secret):
    return "did:nawa:" + hashlib.sha256(secret.encode()).hexdigest()[:20]

# تهيئة الجلسة
if 'vault' not in st.session_state:
    st.session_state.vault = {"balance": 0, "exp": 0, "logs": []}

# --- 4. القائمة الجانبية (بوابة الدخول) ---
with st.sidebar:
    st.title("🛡️ بوابة نوى")
    user_key = st.text_input("أدخل مفتاحك السري:", type="password")
    if user_key:
        my_did = generate_did(user_key)
        # مزامنة البيانات مع جوجل شيت فور الدخول
        bal, xp = sync_user_data(my_did)
        st.session_state.vault['balance'] = bal
        st.session_state.vault['exp'] = xp
        st.success(f"مرحباً، {my_did[:10]}...")
    st.divider()
    st.caption("نظام التخزين: Google Sheets ✅")

# --- 5. الواجهة الرئيسية (التنقل بين الأقسام) ---
tabs = st.tabs(["🔍 الرادار", "🌐 النفق (VPN)", "📊 الخزنة", "💬 التنسيق"])

# --- قسم الرادار ---
with tabs[0]:
    st.subheader("🔍 رادار البحث عن المعرفة")
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("موضوع البحث:", placeholder="مثال: الأمن السيبراني")
    with col2:
        cat = st.selectbox("النوع", ["كتب PDF 📚", "فيديو 🎥", "أبحاث 🔬"])

    if topic:
        links = {
            "كتب PDF 📚": f"https://www.google.com/search?q=filetype:pdf+{topic}",
            "فيديو 🎥": f"https://www.youtube.com/results?search_query={topic}",
            "أبحاث 🔬": f"https://scholar.google.com/scholar?q={topic}"
        }
        st.link_button(f"🚀 انطلاق إلى {topic}", links[cat])
        
        if st.button("💰 توثيق الاستحواذ (+50 عملة)"):
            if user_key:
                st.session_state.vault['balance'] += 50
                st.session_state.vault['exp'] += 100
                update_user_stats(generate_did(user_key), st.session_state.vault['balance'], st.session_state.vault['exp'])
                st.balloons()
                st.rerun()
            else:
                st.error("يرجى إدخال مفتاحك السري أولاً لحفظ النقاط!")

# --- قسم النفق (VPN المصغر) ---
with tabs[1]:
    st.subheader("🛡️ نفق العبور المشفر (Proxy)")
    proxy_server = "https://api.allorigins.win/raw?url="
    target = st.text_input("أدخل رابط الموقع المحجوب:", placeholder="https://example.com")
    
    if st.button("فتح النفق الآمن ⚡"):
        if target:
            st.markdown(f'<iframe src="{proxy_server + target}" width="100%" height="600px" style="border:2px solid #2e7d32; border-radius:15px;"></iframe>', unsafe_allow_html=True)

# --- قسم الخزنة (الإحصائيات الدائمة) ---
with tabs[2]:
    st.subheader("📊 إحصائياتك في قاعدة البيانات")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("رصيدك الحالي 🪙", f"{st.session_state.vault['balance']} NAWA")
    with c2:
        st.metric("مستوى الخبرة ✨", st.session_state.vault['exp'])
    st.info("ملاحظة: يتم حفظ بياناتك تلقائياً في Google Sheets عند كل عملية.")

# --- قسم التنسيق (الدردشة) ---
with tabs[3]:
    st.subheader("💬 غرفة التنسيق")
    if user_key:
        if "messages" not in st.session_state: st.session_state.messages = []
        for m in st.session_state.messages:
            with st.chat_message("user"): st.write(f"**{m['user']}**: {m['text']}")
        
        if p := st.chat_input("اكتب رسالة..."):
            st.session_state.messages.append({"user": generate_did(user_key)[:8], "text": p})
            st.rerun()
    else:
        st.warning("يجب تسجيل الدخول للمشاركة.")

st.divider()
st.caption("NAWA OS v3.0 | Powered by Streamlit & Google Sheets")
