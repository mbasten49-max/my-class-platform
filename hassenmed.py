import streamlit as st
import base64
import os

# إعداد واجهة الصفحة
st.set_page_config(page_title="منصتي التعليمية الآمنة", page_icon="📚", layout="centered")

# جلب المسار الحقيقي للمجلد الحالي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(BASE_DIR, "students.txt")

# دالة قراءة أكواد الطلاب من الملف النصي
def load_allowed_codes():
    allowed_codes = set()
    # كود الإدارة الخاص بك (تم تعديله إلى HASSEN لتسهيل الدخول)
    allowed_codes.add("TEACHER_HASSEN") 
    
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                code = line.strip()
                if code:
                    allowed_codes.add(code)
    else:
        with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
            f.write("# اكتب أكواد الطلاب هنا، كود واحد في كل سطر:\n")
            f.write("STUDENT_AHMED_77\n")
        allowed_codes.add("STUDENT_AHMED_77")
        
    return allowed_codes

ALLOWED_CODES = load_allowed_codes()

def get_binary_file(full_path):
    with open(full_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

protect_css = """
<style>
body { -webkit-user-select: none; user-select: none; }
video::-internal-media-controls-download-button, audio::-internal-media-controls-download-button { display:none !important; }
video::-webkit-media-controls-panel, audio::-webkit-media-controls-panel { width: calc(100% + 30px) !important; }
</style>
<script>
document.addEventListener('contextmenu', event => event.preventDefault());
</script>
"""
st.markdown(protect_css, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- شاشة تسجيل الدخول بالتصحيح الجديد ---
if not st.session_state["logged_in"]:
    st.title("🔐 منصة الأستاذ الحسن التعليمية")
    st.write("مرحباً بك! هذه المنصة محمية ومخصصة للطلاب المشتركين فقط.")
    
    user_code = st.text_input("أدخل رمز الاشتراك الخاص بك المستعمل:", type="password")
    
    if st.button("دخول المنصة"):
        if user_code in ALLOWED_CODES:
            st.session_state["logged_in"] = True
            st.success("تم التحقق من الكود بنجاح! جاري تحميل الدروس...")
            st.rerun()
        else:
            st.error("❌ عذراً، هذا الكود غير صحيح أو تم إلغاء تفعيله. يرجى مراجعة الأستاذ.")

# --- الشاشة الرئيسية للدروس ---
else:
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("📂 لوحة التحكم في الدروس التعليمية")
    st.write("مرحباً بك في المنصة الآمنة لحماية المحتوى التعليمي.")
    st.divider()

    all_files = os.listdir(BASE_DIR)
    audio_extensions = ('.mp3', '.ogg', '.m4a', '.wav', '.opus')
    video_extensions = ('.mp4', '.mkv', '.mov', '.3gp')

    audio_files = [f for f in all_files if f.lower().endswith(audio_extensions)]
    video_files = [f for f in all_files if f.lower().endswith(video_extensions)]

    st.header("🎵 المقاطع الصوتية المتاحة")
    if audio_files:
        for audio in audio_files:
            st.subheader(f"📄 درس صوتي: {audio}")
            try:
                full_audio_path = os.path.join(BASE_DIR, audio)
                audio_base64 = get_binary_file(full_audio_path)
                st.markdown(f'<audio controls controlsList="nodownload" style="width: 100%;"><source src="data:audio/mp3;base64,{audio_base64}"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"حدث خطأ أثناء تشغيل الملف {audio}")
    else:
        st.info("لم يتم العثور على أي ملف صوتي في المجلد الحالي حتى الآن.")

    st.divider()

    st.header("📺 الفيديوهات المتاحة")
    if video_files:
        for video in video_files:
            st.subheader(f"🎥 شرح فيديو: {video}")
            try:
                full_video_path = os.path.join(BASE_DIR, video)
                video_base64 = get_binary_file(full_video_path)
                st.markdown(f'<video width="100%" controls controlsList="nodownload"><source src="data:video/mp4;base64,{video_base64}"></video>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"حدث خطأ أثناء تشغيل الفيديو {video}")
    else:
        st.info("لم يتم العثور على أي ملف فيديو في المجلد الحالي حتى الآن.")
