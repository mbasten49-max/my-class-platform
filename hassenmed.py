import streamlit as st
import re

# إعدادات الصفحة والعنوان
st.set_page_config(page_title="منصة الأستاذ الحسن التعليمية", page_icon="📚", layout="centered")

# دالة ذكية لتحويل روابط قوقل درايف إلى روابط تضمين متوافقة مع التحديثات الأمنية
def get_embed_link(url):
    if "drive.google.com" in url:
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

# نظام التحقق من رموز دخول الطلاب المشتركين
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 منصة الأستاذ الحسن التعليمية")
    st.write("مرحباً بك! هذه المنصة محمية ومخصصة للطلاب المشتركين فقط.")
    
    password = st.text_input("أدخل رمز الاشتراك الخاص بك المستعمل:", type="password")
    if st.button("دخول المنصة"):
        
        # 🔑 قراءة الأكواد تلقائياً من ملف المفكرة الخاص بك students.txt
        allowed_passwords = []
        try:
            with open("students.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    # تخطي السطور الفارغة أو التعليقات التي تبدأ بـ #
                    if line and not line.startswith("#"):
                        allowed_passwords.append(line)
        except FileNotFoundError:
            # أكواد احتياطية في حال لم يجد النظام الملف مؤقتاً
            allowed_passwords = ["1514", "1513", "STUDENT_AHMED_77"]
        
        if password in allowed_passwords:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("رمز الاشتراك غير صحيح! يرجى التحقق من الأستاذ الحسن.")
else:
    # واجهة لوحة التحكم الداخلية للأستاذ والطلاب
    st.title("📂 لوحة التحكم في الدروس التعليمية")
    st.write("مرحباً بك في المنصة الآمنة لحماية المحتوى التعليمي.")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("---")
    
    # 🎥 1. قسم الفيديوهات التعليمية
    st.header("🎥 الفيديوهات المتاحة")
    st.write("بإمكانك مشاهدة المحتوى المرئي للدروس هنا:")
    st.info("سيتم عرض الفيديوهات هنا بمجرد إضافة روابطها في الكود.")

    st.markdown("---")

    # 🎵 2. قسم المقاطع الصوتية
    st.header("🎵 المقاطع الصوتية المتاحة")
    st.write("استمع إلى الشروحات الصوتية التوضيحية:")
    
    audio_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
    st.components.v1.iframe(audio_url, height=150, scrolling=False)

    st.markdown("---")

    # 🖼️ 3. قسم الصور والتمارين التوضيحية
    st.header("🖼️ الصور والرسوم التوضيحية المتاحة")
    st.write("شاهد نص التمارين والمسائل الفيزيائية والرياضية المرفقة:")
    
    image_url = get_embed_link("https://drive.google.com/file/d/1egWOoyQlT6f8FScmdwWFCl2e80SAPYm9/view?usp=drivesdk")
    st.components.v1.iframe(image_url, height=450, scrolling=True)
