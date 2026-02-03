import streamlit as st
import hashlib
import time

# --- محرك النواة ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# محاكاة لجلب محتوى حقيقي (بناءً على النية)
def get_nawa_content(intent):
    content_map = {
        "تعلم مهارة": "https://www.youtube.com/embed/dQw4w9WgXcQ", # مثال لرابط تعليمي
        "استكشاف إبداعي": "https://www.youtube.com/embed/3JZ_D3ELwOQ",
        "ترفيه واعٍ": "https://www.youtube.com/embed/2Vv-BfVoq4g"
    }
    return content_map.get(intent, "https://www.youtube.com/embed/dQw4w9WgXcQ")

# --- الواجهة ---
st.set_page_config(page_title="NAWA | النواة", layout="wide")
st.title("🛡️ مـنصة نـوى (NAWA)")

# لوحة التحكم الجانبية
st.sidebar.header("👤 محفظة الهوية")
user_secret = st.sidebar.text_input("الجملة السرية:", type="password")
if user_secret:
    st.sidebar.info(f"DID: {generate_nawa_did(user_secret)}")
    st.sidebar.metric(label="رصيد $NAWA", value="150.50", delta="+10.25")

# منطقة العمل الرئيسية
st.header("تحديد المسار")
col1, col2 = st.columns([1, 2])

with col1:
    intent = st.selectbox("ما هي نيتك الآن؟", ["تعلم مهارة", "استكشاف إبداعي", "ترفيه واعٍ"])
    duration = st.number_input("المدة (بالدقائق):", min_value=1, value=10)
    start_btn = st.button("🚀 ابدأ جلسة السيادة")

with col2:
    if start_btn:
        st.success(f"جاري البحث عن محتوى يخدم نية ({intent})...")
        video_url = get_nawa_content(intent)
        
        # عرض الفيديو داخل المنصة (بدون تشتيت)
        st.video(video_url)
        
        # عداد الوقت الحقيقي
        st.write("---")
        st.warning(f"⚠️ وضع التركيز نشط. لا تغادر الصفحة لتربح المكافأة.")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.1) # محاكاة للوقت (للتجربة السريعة)
            progress_bar.progress(i + 1)
        
        st.balloons()
        st.success("🎉 أحسنت! التزمت بنيتك. تم إضافة 5 $NAWA لمحفظتك.")
                # --- نظام دعم المبدعين الجديد ---
        st.write("---")
        st.subheader("🙌 هل أعجبك المحتوى؟")
        tip_amount = st.slider("اختر مبلغا لدعم المبدع من أرباحك:", 0.1, 5.0, 0.5)
        
        if st.button("إرسال دعم $NAWA للمبدع"):
            # محاكاة لعملية التحويل عبر البلوكشين
            with st.spinner('جاري تنفيذ التحويل اللامركزي...'):
                time.sleep(1.5)
                st.success(f"تم إرسال {tip_amount} $NAWA مباشرة لمحفظة المبدع. شكراً لتقديرك!")
                
        
