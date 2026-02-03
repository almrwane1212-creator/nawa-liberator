import streamlit as st
import hashlib
import pandas as pd
import time

# --- 1. إعدادات قاعدة البيانات (رابط ملفك) ---
# قمت بتحويل رابطك لصيغة التصدير المباشر لكي يقرأه الكود
SHEET_ID = "1WuGkpFqFqIGje2p3JHXqsyBud0semAbYgus2j52gefo"
USERS_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Users"
CHAT_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Chat"

# دالة لجلب البيانات من ملفك
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# --- 2. محرك الهوية ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# --- 3. واجهة التطبيق ---
st.set_page_config(page_title="NAWA Live DB", layout="wide")

# لوحة المسؤول
with st.sidebar:
    st.title("🛡️ مركز الإدارة")
    admin_key = st.text_input("رمز المسؤول:", type="password")
    if admin_key == "nawa2026":
        st.success("تم الاتصال بـ Google Sheets")
        # عرض البيانات الحقيقية من ملفك
        df_users = load_data(USERS_SHEET_URL)
        st.write(f"👥 عدد المشتركين في الجدول: {len(df_users)}")
        st.dataframe(df_users)

    st.write("---")
    user_secret = st.sidebar.text_input("جملتك السرية (الهوية):", type="password")

# --- 4. الأقسام (Tabs) ---
tab_search, tab_chat = st.tabs(["🔍 محرك البحث", "💬 الدردشة الحية"])

with tab_search:
    topic = st.text_input("ابحث عن المعرفة:")
    if topic:
        st.video(f"https://www.youtube.com/embed?listType=search&list={topic.replace(' ', '+')}")
        st.info(f"💡 سيتم تسجيل نشاطك تحت هويتك في ملف Google Sheets")

with tab_chat:
    st.subheader("🌐 غرفة النقاش (مربوطة بالجدول)")
    # جلب الدردشة من ملفك
    df_chat = load_data(CHAT_SHEET_URL)
    if not df_chat.empty:
        for _, row in df_chat.iterrows():
            st.chat_message("user").write(f"**{row.get('User', 'N/A')}**: {row.get('Message', '')}")
    
    if prompt := st.chat_input("اكتب رسالة..."):
        st.warning("⚠️ لإرسال البيانات فعلياً للجدول، سنحتاج لتفعيل خدمة (Google Service Account) في الخطوة القادمة.")
        st.write(f"رسالتك المسودة: {prompt}")
        
