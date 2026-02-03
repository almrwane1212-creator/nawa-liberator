import streamlit as st
import hashlib
import time

# --- محرك النواة ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

# محاكاة لجلب محتوى حقيقي (بناءً على النية)
        
# --- 1. محرك البحث الذكي الجديد ---
def get_dynamic_content(topic):
    # تحويل نص البحث إلى رابط يوتيوب مدمج وآمن
    search_query = topic.replace(" ", "+")
    return f"https://www.youtube.com/embed?listType=search&list={search_query}"

# --- 2. منطقة العمل الرئيسية المحدثة ---
st.header("تحديد المسار والبحث الذكي")
col1, col2 = st.columns([1, 2])

with col1:
    # خانة بحث حرة بدلاً من الاختيارات الثابتة
    user_topic = st.text_input("عن ماذا تريد أن تتعلم اليوم؟", placeholder="مثلاً: بايثون، الذكاء الاصطناعي...")
    duration = st.number_input("المدة (بالدقائق):", min_value=1, value=10)
    start_btn = st.button("🚀 تفعيل محرك البحث السيادي")

with col2:
    if start_btn and user_topic:
        st.success(f"جاري تنقية النتائج لـ: {user_topic}")
        embed_url = get_dynamic_content(user_topic)
        
        # عرض نتائج البحث مباشرة داخل تطبيقك
        st.components.v1.iframe(embed_url, height=450, scrolling=True)
        
        # نظام المكافآت وعداد الوقت
        st.write("---")
        progress_bar = st.progress(0)
        st.warning("⚠️ وضع التركيز نشط: المكافأة مرتبطة بإنهاء الوقت.")
        for i in range(100):
            time.sleep(0.1) # محاكاة للوقت (يمكنك زيادته لاحقاً)
            progress_bar.progress(i + 1)
        
        st.balloons()
        st.success(f"تمت المهمة! أضفنا 5 $NAWA لرصيدك لبحثك عن {user_topic}")

# --- 3. نظام دعم المبدعين ---
st.write("---")
st.subheader("🙌 هل أعجبك المحتوى؟")
tip_amount = st.slider("اختر مبلغا لدعم المبدع من أرباحك:", 0.1, 5.0, 0.5)
if st.button("إرسال دعم $NAWA للمبدع"):
    st.success(f"تم إرسال {tip_amount} $NAWA مباشرة. شكراً لتقديرك!")
