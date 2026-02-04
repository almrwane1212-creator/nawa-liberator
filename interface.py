import streamlit as st
import hashlib
import requests
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. إعدادات الهوية والواجهة ---
st.set_page_config(page_title="نوى | NAWA OS PRO", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stButton>button { border-radius: 8px; background-color: #1b5e20; color: white; transition: 0.3s; }
    .stButton>button:hover { background-color: #2e7d32; border: 1px solid #4caf50; }
    iframe { border: 2px solid #2e7d32; border-radius: 15px; background: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام الاتصال بقاعدة البيانات (Google Sheets) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("⚠️ خطأ في الاتصال بقاعدة البيانات. تأكد من إعداد Secrets.")

def sync_data(did):
    try:
        df = conn.read(ttl=0)
        if did in df['DID'].astype(str).values:
            row = df[df['DID'] == did].iloc[0]
            return int(row['Balance']), int(row['Exp'])
        else:
            new_user = pd.DataFrame([{"DID": did, "Balance": 100, "Exp": 0}])
            updated_df = pd.concat([df, new_user], ignore_index=True)
            conn.update(data=updated_df)
            return 100, 0
    except: return 100, 0

def save_stats(did, bal, xp):
    try:
        df = conn.read(ttl=0)
        df.loc[df['DID'] == did, ['Balance', 'Exp']] = [bal, xp]
        conn.update(data=df)
    except: pass

# --- 3. محرك الرادار والذكاء الاصطناعي ---
def generate_did(key):
    return "did:nawa:" + hashlib.sha256(key.encode()).hexdigest()[:15]

def ai_summarizer(topic):
    """محاكاة للذكاء الاصطناعي لتحليل نتائج البحث"""
    return f"🔍 تحليل نوى الذكي: البحث عن '{topic}' يظهر نتائج في 3 قطاعات رئيسية. المصادر المتاحة حالياً توفر مستندات تقنية عالية الجودة. يُنصح بالتركيز على روابط الأرشيف للحصول على البيانات الأصلية."

# --- 4. الهيكل الرئيسي للتطبيق ---
with st.sidebar:
    st.title("🛡️ بوابة نوى الآمنة")
    user_key = st.text_input("المفتاح السري (Identity Key):", type="password")
    if user_key:
        my_did = generate_did(user_key)
        bal, xp = sync_data(my_did)
        st.session_state.update({"bal": bal, "xp": xp, "did": my_did})
        st.success(f"تم التحقق: {my_did[:10]}...")
    st.divider()
    st.info("نظام التخزين النشط: Google Sheets 🟢")

tabs = st.tabs(["🛰️ الرادار العميق", "🌐 نفق العبور", "📊 الخزنة"])

# --- TAB 1: الرادار العميق ---
with tabs[0]:
    st.subheader("🛰️ رادار الاستطلاع وتحليل البيانات")
    
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        topic = st.text_input("هدف البحث العميق:", placeholder="مثال: تشفير البيانات، كتب نادرة...")
    with c2:
        stype = st.selectbox("نوع الاستطلاع", ["كتب/وثائق PDF 📚", "أبحاث Scholar 🔬", "أكواد GitHub 💻", "أرشيف Archive 🏛️", "صور وبيانات 🖼️"])
    with c3:
        mode = st.radio("وضع العرض", ["داخلي 📥", "خارجي ↗️"])

    if topic:
        # هندسة روابط البحث
        queries = {
            "كتب/وثائق PDF 📚": f"https://www.google.com/search?q=filetype:pdf+{topic}",
            "أبحاث Scholar 🔬": f"https://scholar.google.com/scholar?q={topic}",
            "أكواد GitHub 💻": f"https://github.com/search?q={topic}",
            "أرشيف Archive 🏛️": f"https://archive.org/search.php?query={topic}",
            "صور وبيانات 🖼️": f"https://www.google.com/search?q={topic}&tbm=isch"
        }
        url = queries[stype]
        
        # ميزة الذكاء الاصطناعي
        with st.expander("🤖 تحليل الذكاء الاصطناعي الأولي (AI Summary)"):
            st.write(ai_summarizer(topic))
        
        if mode == "خارجي ↗️":
            st.link_button(f"🚀 انطلاق إلى {topic}", url)
        else:
            proxy = f"https://api.allorigins.win/raw?url={url}"
            st.markdown(f'<iframe src="{proxy}" width="100%" height="700px"></iframe>', unsafe_allow_html=True)
        
        if st.button("💰 توثيق الاستحواذ وحفظ البيانات (+100 عملة)"):
            if user_key:
                st.session_state.bal += 100
                st.session_state.xp += 200
                save_stats(st.session_state.did, st.session_state.bal, st.session_state.xp)
                st.balloons()
                st.success("تم الحفظ في السحابة!")
            else: st.warning("سجل دخولك أولاً")

# --- TAB 2: نفق العبور ---
with tabs[1]:
    st.subheader("🛡️ نفق العبور (Proxy)")
    site = st.text_input("أدخل رابط الموقع المستهدف:")
    if st.button("فتح النفق ⚡") and site:
        st.markdown(f'<iframe src="https://api.allorigins.win/raw?url={site}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)

# --- TAB 3: الخزنة ---
with tabs[2]:
    st.subheader("📊 خزنة البيانات الدائمة")
    if user_key:
        col_a, col_b = st.columns(2)
        col_a.metric("رصيد العملات 🪙", f"{st.session_state.bal} NAWA")
        col_b.metric("مستوى الخبرة ✨", st.session_state.xp)
        st.write(f"معرفك الرقمي الفريد: `{st.session_state.did}`")
    else:
        st.info("قم بتسجيل الدخول لمشاهدة بياناتك المخزنة في Google Sheets.")
                
