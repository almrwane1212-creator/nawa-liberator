import streamlit as st
import hashlib
import time

# --- 1. محرك الهوية والبيانات ---
def generate_nawa_did(user_seed):
    return "did:nawa:" + hashlib.sha256(user_seed.encode()).hexdigest()[:24]

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'registered_users' not in st.session_state:
    st.session_state.registered_users = set()

# --- 2. إعدادات الواجهة الشاملة ---
st.set_page_config(page_title="NAWA Global", layout="wide")
st.title("🛡️ مـحرك نـوى العالمي (Universal Search)")

with st.sidebar:
    st.header("⚙️ لوحة الإدارة")
    admin_pass = st.text_input("رمز المدير:", type="password")
    if admin_pass == "nawa2026":
        st.success("صلاحيات المؤسس نشطة")
        st.metric("المستخدمون النشطون", len(st.session_state.registered_users))
    
    st.write("---")
    user_secret = st.text_input("فعل هويتك للبحث والدردشة:", type="password")
    if user_secret:
        my_did = generate_nawa_did(user_secret)
        st.session_state.registered_users.add(my_did)
        st.info("هويتك السيادية نشطة ✅")

# --- 3. محرك البحث المتعدد المصادر ---
tab_search, tab_social = st.tabs(["🌐 رادار الإنترنت", "💬 غرفة الدردشة"])

with tab_search:
    st.subheader("ابحث عن فيديوهات أو دورات في أي موقع")
    col_input, col_source = st.columns([3, 1])
    
    with col_input:
        topic = st.text_input("ما هو موضوعك اليوم؟", placeholder="مثلاً: تعلم التجارة الإلكترونية، شرح الفيزياء...")
    
    with col_source:
        source = st.selectbox("المصدر:", ["كل المواقع (جوجل فيديو)", "يوتيوب", "فيميو (Vimeo)", "ديلي موشن"])

    if topic:
        # بناء روابط البحث بناءً على المصدر المختار
        if source == "كل المواقع (جوجل فيديو)":
            search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}&tbm=vid"
        elif source == "يوتيوب":
            search_url = f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}"
        elif source == "فيميو (Vimeo)":
            search_url = f"https://vimeo.com/search?q={topic.replace(' ', '+')}"
        else:
            search_url = f"https://www.dailymotion.com/search/{topic.replace(' ', '+')}"

        st.info(f"🔍 جاري البحث عن '{topic}' في {source}...")
        
        # عرض بطاقة توجيه ذكية
        st.success("✅ تم العثور على مصادر تعليمية!")
        st.write("بسبب قيود الحماية في بعض المواقع، نوصي بفتح البحث في نافذة مستقلة لضمان أفضل جودة:")
        
        st.link_button(f"🚀 فتح نتائج {source} الآن", search_url)
        
        st.write("---")
        if st.button("✅ سجلت دخولي وشاهدت (احصد 10 $NAWA)"):
            st.balloons()
            st.success("تم تسجيل نشاطك التعليمي بنجاح!")

with tab_social:
    st.subheader("🌐 حائط النقاش الحر")
    chat_container = st.container(height=300)
    for msg in st.session_state.chat_history:
        chat_container.chat_message("user").write(f"**{msg['user']}**: {msg['text']}")

    if prompt := st.chat_input("تفاعل مع المجتمع..."):
        if not user_secret:
            st.error("أدخل جملتك السرية في القائمة الجانبية أولاً!")
        else:
            display_name = generate_nawa_did(user_secret)[:10]
            st.session_state.chat_history.append({"user": display_name, "text": prompt})
            st.rerun()
            
