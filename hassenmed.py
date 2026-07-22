import streamlit as st
import re

# إعدادات الصفحة والعنوان
st.set_page_config(
    page_title="منصة الأستاذ الحسن التعليمية", 
    page_icon="📚", 
    layout="wide"
)

# 🎨 لمسات تصميمية وألوان مميزة للمنصة
st.markdown("""
    <style>
    /* خلفية وألوان الصفحة العامة */
    .stApp {
        background-color: #f4f7f6;
    }
    /* تصميم العناوين الرئيسية */
    h1 {
        color: #1A365D !important;
        text-align: center;
        font-weight: 700;
    }
    h2, h3 {
        color: #2B6CB0 !important;
    }
    /* تحسين شكل البطاقات والأزرار */
    .stButton>button {
        background-color: #319795;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2C7A7B;
        color: white;
    }
    /* إطار أنيق للتقييم والملاحظات */
    .rating-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        border-right: 5px solid #319795;
    }
    </style>
""", unsafe_allow_html=True)

# دالة تحويل روابط قوقل درايف إلى روابط تضمين للعرض المباشر
def get_embed_link(url):
    if "drive.google.com" in url:
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

# نظام كاشف الأجهزة لمنع مشاركة الأكواد
if "code_device_registry" not in st.session_state:
    st.session_state["code_device_registry"] = {}

# نظام حفظ التقييمات المؤقتة
if "feedbacks" not in st.session_state:
    st.session_state["feedbacks"] = []

# نظام التحقق من الدخول
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "student_code" not in st.session_state:
    st.session_state["student_code"] = ""

# ================= 🔐 شاشة تسجيل الدخول =================
if not st.session_state["authenticated"]:
    st.title("🔒 منصة الأستاذ الحسن التعليمية")
    st.subheader("أهلاً بكم في المنصة الرسمية لمتابعة الدروس والشروحات")
    st.write("هذه المنصة محمية ومخصصة للطلاب المشتركين فقط عبر رمز الدخول الخاص.")
    
    password = st.text_input("أدخل رمز الاشتراك الخاص بك:", type="password")
    
    if st.button("دخول المنصة 🚀"):
        clean_password = password.strip()
        
        allowed_passwords = []
        try:
            with open("students.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        allowed_passwords.append(line)
                        numbers_found = re.findall(r'\d+', line)
                        for num in numbers_found:
                            allowed_passwords.append(num)
                        text_only = re.sub(r'\d+', '', line).strip()
                        if text_only:
                            allowed_passwords.append(text_only)
        except FileNotFoundError:
            allowed_passwords = ["1513", "1514", "1515", "STUDENT_AHMED_77"]
        
        if clean_password in allowed_passwords:
            current_session_id = st.context.headers.get("User-Agent", "unknown_device")
            
            if clean_password in st.session_state["code_device_registry"]:
                if st.session_state["code_device_registry"][clean_password] != current_session_id:
                    st.error(f"🚨 تنبيه أمني: هذا الرمز ({clean_password}) مُستعمل حالياً على جهاز آخر! تم قفل الحساب، يرجى التواصل مع الأستاذ الحسن.")
                else:
                    st.session_state["authenticated"] = True
                    st.session_state["student_code"] = clean_password
                    st.rerun()
            else:
                st.session_state["code_device_registry"][clean_password] = current_session_id
                st.session_state["authenticated"] = True
                st.session_state["student_code"] = clean_password
                st.rerun()
        else:
            st.error("❌ رمز الاشتراك غير صحيح! يرجى التأكد من الرمز وإعادة المحاولة.")

# ================= 📖 المحتوى التعليمي للدرس =================
else:
    # الشريط الجانبي
    st.sidebar.title("👨‍🏫 منصة الأستاذ الحسن")
    st.sidebar.info(f"👤 الرمز النشط: **{st.session_state['student_code']}**")
    
    # لوحة مراقبة للأستاذ
    if st.sidebar.checkbox("🛠️ لوحة مراقبة الأستاذ"):
        st.write("### 🕵️ قائمة الأكواد والأجهزة النشطة:")
        st.json(st.session_state["code_device_registry"])
        st.write("### 💬 تقييمات وآراء الطلاب:")
        st.write(st.session_state["feedbacks"])
    
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state["authenticated"] = False
        st.rerun()

    # رأس الصفحة
    st.title("📚 الدرس الأول: الشرح والتمارين التطبيقية")
    st.success("مرحباً بك يا بطل! أتمنى لك مشاهدة ممتعة وفهماً عميقاً للدرس.")
    st.markdown("---")

    # 1️⃣ قسم الفيديوهات التعليمية
    st.header("🎥 فيديوهات الشرح والتبسيط")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📹 الجزء الأول من الشرح")
        video_1_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
        st.components.v1.iframe(video_1_url, height=315, scrolling=False)

    with col2:
        st.subheader("📹 الجزء الثاني من الشرح")
        video_2_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
        st.components.v1.iframe(video_2_url, height=315, scrolling=False)

    st.markdown("---")

    # 2️⃣ قسم التسجيل الصوتي
    st.header("🎵 المقطع الصوتي التوضيحي")
    st.caption("استمع إلى الملاحظات الصوتية الهامة الخاصة بالدرس:")
    audio_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
    st.components.v1.iframe(audio_url, height=120, scrolling=False)

    st.markdown("---")

    # 3️⃣ قسم الصور والتمارين
    st.header("🖼️ التمارين والرسوم التوضيحية")
    st.caption("صورة الدرس والتمارين المرفقة للاطلاع والمراجعة:")
    image_url = get_embed_link("https://drive.google.com/file/d/1egWOoyQlT6f8FScmdwWFCl2e80SAPYm9/view?usp=drivesdk")
    st.components.v1.iframe(image_url, height=500, scrolling=True)

    st.markdown("---")

    # 4️⃣ 🌟 قسم تقييم المنصة والدرس (إضافة جديدة)
    st.header("⭐ رأيك يهمنا: تقييم المنصة والدرس")
    st.markdown('<div class="rating-box">', unsafe_allow_html=True)
    
    rating = st.feedback("stars")
    user_comment = st.text_input("أضف ملاحظة أو كلمة للأستاذ الحسن (اختياري):")
    
    if st.button("إرسال التقييم 🌟"):
        st.session_state["feedbacks"].append({
            "code": st.session_state["student_code"],
            "stars": rating,
            "comment": user_comment
        })
        st.balloons()
        st.success("شكرًا لك على تقييمك ورأيك الرائع!")
        
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.write("✨ **مع تحيات الأستاذ الحسن - نتمنى لكم دوام التوفيق والنجاح** ✨")
