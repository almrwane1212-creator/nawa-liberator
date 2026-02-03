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

# --- 2. إعدادات الواجهة الاحترافية ---
st.set_page_config(page_title="NAWA Deep Search", layout="wide")
st.title("🛡️ مـحرك نـوى للبحث العـميق (Knowledge OS)")

with st.sidebar:
    st.header("⚙️ لوحة الإدارة")
    admin_pass = st.text_input("رمز المدير:", type="password")
    if admin_pass == "nawa2026":
        st.success("صلاحيات المؤسس نشطة")
        st.metric("المستخدمون النشطون", len(st.session_state.registered_users))
    
    st.write("---")
    user_secret = st.text_input("فعل هويتك السيادية:", type="password")
    if user_secret:
        my_did = generate_nawa_did(user_secret)
        st.session_state.registered_users.add(my_did)
        st.info("الهوية نشطة ✅")

# --- 3. محرك البحث العميق متعدد الأبعاد ---
tab_deep, tab_social = st.tabs(["🚀 رادار المعرفة العميق", "💬 غرفة الدردشة"])

with tab_deep:
    col_input, col_type = st.columns([2, 1])
    
    with col_input:
        topic = st.text_input("عن ماذا تريد أن تتعمق اليوم؟", placeholder="مثلاً: ميكانيكا الكم، أمن المعلومات...")
    
    with col_type:
        content_type = st.selectbox("نوع المحتوى المطلوب:", [
            "🎥 فيديوهات تعليمية (YouTube/Vimeo)", 
            "📚 كتب ومراجع (PDF)", 
            "🔬 أبحاث وأوراق علمية (Scholar)", 
            "💻 أكواد ومشاريع (GitHub)",
            "📊 عرض تقديمي (PowerPoint)"
        ])

    if topic:
        # بناء روابط البحث العميق (Google Dorking)
        query = topic.replace(" ", "+")
        
        if "🎥" in content_type:
            search_url = f"https://www.google.com/search?q={query}+tutorial+video"
        elif "📚" in content_type:
            search_url = f"https://www.google.com/search?q=filetype:pdf+{query}"
        elif "🔬" in content_type:
            search_url = f"https://scholar.google.com/scholar?q={query}"
        elif "💻" in content_type:
            search_url = f"https://github.com/search?q={query}"
        else:
            search_url = f"https://www.google.com/search?q=filetype:ppt+{query}"

        st.success(f"🔍 تم توجيه الرادار نحو {content_type}")
        
        # تصميم بطاقة النتيجة
        with st.container(border=True):
            st.write(f"### 🎯 الهدف: {topic}")
            st.write(f"المصدر المقترح: {content_type}")
            st.link_button(f"🔗 فتح مصادر {topic} الآن", search_url)
            
            st.write("---")
            st.info("بعد حصولك على المعرفة، اضغط أدناه لتوثيق الجلسة.")
            if st.button("✅ تمت المهمة بنجاح (+15 $NAWA)"):
                st.balloons()
                st.success("تم تسجيل القيمة المعرفية في محفظتك!")

with tab_social:
    st.subheader("🌐 حائط النقاش الحر")
    chat_container = st.container(height=300)
    for msg in st.session_state.chat_history:
        chat_container.chat_message("user").write(f"**{msg['user']}**: {msg['text']}")

    if prompt := st.chat_input("شارك ما تعلمته مع المجتمع..."):
        if not user_secret:
            st.error("فعل هويتك أولاً!")
        else:
            display_name = generate_nawa_did(user_secret)[:10]
            st.session_state.chat_history.append({"user": display_name, "text": prompt})
            st.rerun()
            
