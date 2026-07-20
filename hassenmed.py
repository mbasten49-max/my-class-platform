import streamlit as st
import re

# إعدادات الصفحة والعنوان
st.set_page_config(page_title="منصة الأستاذ الحسن التعليمية", page_icon="📚", layout="centered")

# دالة ذكية لتحويل رابط قوقل درايف العادي إلى رابط مباشر يشتغل فوراً في المنصة
def make_direct_link(url):
    if "drive.google.com" in url:
        # استخراج معرف الملف الفرعي باستخدام التعبيرات النمطية
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://docs.google.com/uc?export=download&id={file_id}"
    return url

# نظام التحقق من رموز دخول الطلاب المشتركين
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 منصة الأستاذ الحسن التعليمية")
    st.write("مرحباً بك! هذه المنصة محمية ومخصصة للطلاب المشتركين فقط.")
    
    password = st.text_input("أدخل رمز الاشتراك الخاص بك المستعمل:", type="password")
    if st.button("دخول المنصة"):
        # قائمة الرموز الصالحة للطلاب (يمكنك إضافة أو تغيير الرموز هنا في أي وقت)
        allowed_passwords = ["STUDENT_AHMED_77", "1234"]
        
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
    
    # تفريغ الروابط القديمة. ضع روابط فيديوهات قوقل درايف الخاصة بك هنا بين القوسين:
    # مثال لإضافة فيديو أول:
    # st.video(make_direct_link("ضع_رابط_الفيديو_الأول_هنا"))
    # مثال لإضافة فيديو ثانٍ:
    # st.video(make_direct_link("ضع_رابط_الفيديو_الثاني_هنا"))
    
    st.info("قم بوضع روابط الفيديوهات داخل الكود ليتم عرضها تلقائياً.")

    st.markdown("---")

    # 🎵 2. قسم المقاطع الصوتية
    st.header("🎵 المقاطع الصوتية المتاحة")
    st.write("استمع إلى الشروحات الصوتية التوضيحية:")
    
    # ضع روابط الملفات الصوتية هنا بين القوسين:
    # st.audio(make_direct_link("ضع_رابط_الصوت_هنا"))
    
    st.info("قم بوضع روابط الملفات الصوتية داخل الكود ليتم عرضها تلقائياً.")

    st.markdown("---")

    # 🖼️ 3. قسم الصور والتمارين التوضيحية
    st.header("🖼️ الصور والرسوم التوضيحية المتاحة")
    st.write("شاهد نص التمارين والمسائل الفيزيائية والرياضية المرفقة:")
    
    # ضع روابط الصور هنا بين القوسين، ويمكنك كتابة عنوان تذكيري لكل صورة:
    # st.image(make_direct_link("ضع_رابط_الصورة_الأولى_هنا"), caption="تمرين الحركة المستقيمة")
    # st.image(make_direct_link("ضع_رابط_الصورة_الثانية_هنا"), caption="مسألة الدارة الكهربائية")
    
    st.info("قم بوضع روابط الصور داخل الكود ليتم عرضها تلقائياً.")
