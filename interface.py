import streamlit as st
import hashlib
import time

# --- 1. محرك النواة والهوية ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# --- 2. إعدادات الواجهة ---
st.set_page_config(page_title="NAWA | النواة", layout="wide")
st.title("🛡️ مـنصة نـوى (NAWA)")

# لوحة التحكم الجانبية
st.sidebar.header("👤 محفظة الهوية")
user_secret = st.sidebar.text_input("الجملة السرية:", type="password")
if user_secret:
    st.sidebar.info(f"DID: {generate_nawa_did(user_secret)}")
    st.sidebar.metric(label="رصيد $NAWA", value="155.50", delta="+5.00")

# --- 3. منطقة البحث والسيادة ---
st.header("تحديد المسار والبحث الذكي")
user_topic = st.text_input("عن ماذا تريد أن تتعلم اليوم؟", placeholder="اكتب موضوعك هنا...")

if user_topic:
    search_query = user_topic.replace(" ", "+")
    # رابط البحث المباشر
    video_url = f"https://www.youtube.com/results?search_query={search_query}"
    embed_url = f"https://www.youtube.com/embed?listType=search&list={search_query}"

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write(f"### 🎯 نيتك: {user_topic}")
        st.info("إذا لم يظهر الفيديو بجانبك، استخدم الزر بالأسفل للفتح المباشر.")
        # زر الفتح الخارجي المضمون 100%
        st.link_button("🔗 فتح قائمة الفيديوهات في نافذة جديدة", video_url)
        
        if st.button("✅ ابدأ الجلسة واحصد المكافأة"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)
            st.balloons()
            st.success("تمت إضافة 5 $NAWA لرصيدك!")

    with col2:
        # محاولة العرض داخل التطبيق
        st.components.v1.iframe(embed_url, height=450, scrolling=True)

# --- 4. نظام دعم المبدعين ---
st.write("---")
st.subheader("🙌 هل أعجبك المحتوى؟")
tip = st.slider("دعم المبدع من أرباحك:", 0.1, 5.0, 0.5)
if st.button("إرسال دعم $NAWA"):
    st.success(f"تم إرسال {tip} $NAWA بنجاح!")
# --- 5. لوحة تحكم المسؤول (تجريبية) ---
st.sidebar.write("---")
if st.sidebar.checkbox("عرض إحصائيات المنصة (للمسؤول فقط)"):
    st.sidebar.subheader("📊 نشاط النواة")
    # هنا سنربط مستقبلاً بقاعدة البيانات الحقيقية
    st.sidebar.write("عدد المشتركين الجدد: 12")
    st.sidebar.write("آخر الهويات المسجلة:")
    st.sidebar.code("did:nawa:a1b2... (متصل الآن)")
    
