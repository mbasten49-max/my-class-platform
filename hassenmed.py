import streamlit as st

# إعدادات الصفحة والعنوان
st.set_page_config(page_title="منصة الأستاذ الحسن التعليمية", page_icon="📚", layout="centered")

# التحقق من تسجيل الدخول لحماية المحتوى
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# واجهة تسجيل الدخول للطلاب
if not st.session_state["authenticated"]:
    st.title("🔒 منصة الأستاذ الحسن التعليمية")
    st.write("مرحباً بك! هذه المنصة محمية ومخصصة للطلاب المشتركين فقط.")
    
    password = st.text_input("أدخل رمز الاشتراك الخاص بك المستعمل:", type="password")
    if st.button("دخول المنصة"):
        if password == "1234": # يمكنك تغيير الرمز الماستر من هنا
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("رمز الاشتراك غير صحيح!")
else:
    # واجهة لوحة التحكم الداخلية
    st.title("📂 لوحة التحكم في الدروس التعليمية")
    st.write("مرحباً بك في المنصة الآمنة لحماية المحتوى التعليمي.")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("---")
    
    # 🎥 قسم الفيديوهات التعليمية
    st.header("🎥 الفيديوهات المتاحة")
    # 📝 لإضافة فيديو جديد: امسح الرابط التجريبي بالأسفل وضع رابط فيديو قوقل درايف بعد تحويله لروابط مباشرة
    st.video("https://www.w3schools.com/html/mov_bbb.mp4") 

    st.markdown("---")

    # 🎵 قسم المقاطع الصوتية
    st.header("🎵 المقاطع الصوتية المتاحة")
    # 📝 لإضافة مقطع صوتي: ضع رابط الصوت هنا
    st.audio("https://www.w3schools.com/html/horse.mp3")

    st.markdown("---")

    # 🖼️ قسم الصور والتمارين التوضيحية
    st.header("🖼️ الصور والرسوم التوضيحية المتاحة")
    # 📝 لإضافة صورة تمرين: ضع رابط الصورة هنا
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", caption="تمرين اليوم")
