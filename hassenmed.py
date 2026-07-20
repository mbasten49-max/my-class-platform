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
        # قائمة الرموز الصالحة للطلاب
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
    st.info("سيتم عرض الفيديوهات هنا بمجرد إضافة روابطها في الكود.")

    st.markdown("---")

    # 🎵 2. قسم المقاطع الصوتية
    st.header("🎵 المقاطع الصوتية المتاحة")
    st.write("استمع إلى الشروحات الصوتية التوضيحية:")
    
    # تم وضع رابط المقطع الصوتي الخاص بك بنجاح
    st.audio(make_direct_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk"))

    st.markdown("---")

    # 🖼️ 3. قسم الصور والتمارين التوضيحية
    st.header("🖼️ الصور والرسوم التوضيحية المتاحة")
    st.write("شاهد نص التمارين والمسائل الفيزيائية والرياضية المرفقة:")
    
    # تم وضع رابط صورتك الخاصة بنجاح
    st.image(make_direct_link("https://drive.google.com/file/d/1egWOoyQlT6f8FScmdwWFCl2e80SAPYm9/view?usp=drivesdk"), caption="تمرين الدرس الحالي")
