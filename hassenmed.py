import streamlit as st
import re
import os
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة التحضير للباكالوريا", 
    page_icon="📚", 
    layout="wide"
)

# دالة لتحويل روابط Google Drive إلى روابط عرض مباشرة
def get_embed_link(url):
    if "drive.google.com" in url:
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

# إدارة حالة الجلسة والتقييمات
if "feedbacks" not in st.session_state:
    st.session_state["feedbacks"] = []

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "student_code" not in st.session_state:
    st.session_state["student_code"] = ""

# دالة لتسجيل دخول الطلاب
def log_student_login(code):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logins.txt", "a", encoding="utf-8") as file:
            file.write(f"[{now}] رمز الدخول: {code}\n")
    except Exception:
        pass

# ================= 🔐 صفحة تسجيل الدخول =================
if not st.session_state["authenticated"]:
    st.title("🔒 منصة التحضير للباكالوريا")
    st.write("أهلاً وسهلاً بكم! يرجى إدخال رمز الدخول الخاص بك للوصول إلى الدروس:")
    
    password = st.text_input("رمز الدخول (Code d'accès) :", type="password")
    
    if st.button("تسجيل الدخول 🚀"):
        clean_password = password.strip()
        
        allowed_passwords = []
        try:
            with open("students.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        allowed_passwords.append(line)
        except FileNotFoundError:
            pass

        default_passwords = [
            "1513", "1514", "1515", "1516", "1517", "1518", "1519", "1520",
            "1521", "1522", "1523", "1524", "1525", "1526", "1527", "1528", "1529", "1530",
            "E1 1514", "E2 1513", "E3 1516", "E4 1517", "E5 1518", 
            "E6 1519", "E7 1520", "E8 1521", "E9 1522", "E10 1523",
            "STUDENT2026", "BAC2026", "PHYSICS101"
        ]
        
        all_allowed = list(set(allowed_passwords + default_passwords))
        
        if clean_password in all_allowed:
            st.session_state["authenticated"] = True
            st.session_state["student_code"] = clean_password
            log_student_login(clean_password)
            st.rerun()
        else:
            st.error("❌ رمز الدخول غير صحيح! يرجى التأكد من الرمز وإعادة المحاولة.")

# ================= 📖 المحتوى التعليمي =================
else:
    # القائمة الجانبية
    st.sidebar.title("👨‍🏫 منصة التحضير للباكالوريا")
    st.sidebar.info(f"الرمز النشط حالياً: {st.session_state['student_code']}")
    
    # لوحة تحكم الأستاذ
    if st.sidebar.checkbox("🛠️ لوحة تحكم الأستاذ"):
        st.write("### 👥 سجل دخول التلاميذ:")
        
        if st.button("🗑️ مسح السجل القديم"):
            if os.path.exists("logins.txt"):
                os.remove("logins.txt")
                st.success("تم مسح السجل بنجاح!")
                st.rerun()

        try:
            with open("logins.txt", "r", encoding="utf-8") as f:
                logins_data = f.readlines()
                if logins_data:
                    for entry in reversed(logins_data):
                        st.text(entry.strip())
                else:
                    st.info("لا توجد تسجيلات دخول حالياً.")
        except FileNotFoundError:
            st.info("لا يوجد سجل دخول متوفر حتى الآن.")

        st.markdown("---")
        st.write("### 💬 تقييمات وملاحظات الطلاب:")
        st.write(st.session_state["feedbacks"])
    
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state["authenticated"] = False
        st.rerun()

    # العنوان الرئيسي
    st.title("📚 الدروس المتوفرة في المنصة")
    st.write("اختر المادة والدرس للتصفح:")

    # 📌 إنشاء تبويبات تنقل سهلة
    tab_math, tab_physics = st.tabs([
        "📐 الرياضيات: الأعداد المركبة (Nombre Complexe)", 
        "🧪 الفيزياء: السينماتيك والديناميك"
    ])

    # ================= 📐 1. تبويب الرياضيات =================
    with tab_math:
        st.header("📐 درس: الأعداد المركبة (Nombre Complexe)")
        st.success("مرحباً بكم في درس الرياضيات! نتمنى لكم تحصيلاً علمياً موفقاً.")
        st.markdown("---")

        # 🎥 فيديو شرح الرياضيات (كود التضمين الصحيح)
        st.subheader("🎥 فيديو شرح درس الأعداد المركبة")
        canva_math_video = """
        <div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%; padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0; margin: 0;"
            src="https://www.canva.com/design/DAHQq1eiNHg/vGXhkTslHgO5iI9RKli6qg/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
          </iframe>
        </div>
        """
        st.components.v1.html(canva_math_video, height=520)

        st.markdown("---")

        # 📄 أوراق ملخص الدرس (الصور الـ 6)
        st.subheader("📝 ملخص وقواعد الدرس (من دفتر الشرح)")
        st.caption("تصفح أوراق الملخص المرفقة أدناه لمراجعة كافة المفاهيم والقوانين:")

        math_images = [
            "https://drive.google.com/file/d/1E1JZjIgjbUA7FEIy4SsPhPSUbzkuYY03/view?usp=drivesdk", # الصفحة 1
            "https://drive.google.com/file/d/1ojVmPZLu8lCtfypoH33ACE2B300xMoKx/view?usp=drivesdk", # الصفحة 2
            "https://drive.google.com/file/d/1CRTsvEfMl7d8rAal6_8NOIhiLctyzX-r/view?usp=drivesdk", # الصفحة 3
            "https://drive.google.com/file/d/18ITRuvewvGp0LipcmpsqmmHOw9a3Qy_k/view?usp=drivesdk", # الصفحة 4
            "https://drive.google.com/file/d/1zKaKm2JR7WVuYqGtB6GLtrp376VtDIDu/view?usp=drivesdk", # الصفحة 5
            "https://drive.google.com/file/d/1Ag1bViXkgaS-Dgx4oJ9hR0d-8TU8j50l/view?usp=drivesdk", # الصفحة 6
        ]

        col1, col2 = st.columns(2)
        for index, img_url in enumerate(math_images):
            embed_url = get_embed_link(img_url)
            if index % 2 == 0:
                with col1:
                    st.write(f"**📄 الصفحة {index + 1}**")
                    st.components.v1.iframe(embed_url, height=500, scrolling=True)
            else:
                with col2:
                    st.write(f"**📄 الصفحة {index + 1}**")
                    st.components.v1.iframe(embed_url, height=500, scrolling=True)

    # ================= 🧪 2. تبويب الفيزياء =================
    with tab_physics:
        st.header("🧪 درس: السينماتيك والديناميك (Cinématique et Dynamique)")
        st.success("مرحباً بكم في درس الفيزياء! نتمنى لكم مشاهدة ممتعة وتحصيلاً موفقاً.")
        st.markdown("---")

        st.subheader("🎥 فيديو الشرح الرئيسي للدرس")
        canva_physics_video = """
        <div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%; overflow: hidden; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none;"
            src="https://www.canva.com/design/DAHQq1eiNHg/vGXhkTslHgO5iI9RKli6qg/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
          </iframe>
        </div>
        """
        st.components.v1.html(canva_physics_video, height=520)

        st.markdown("---")

        st.subheader("🎵 التسجيلات الصوتية")
        audio_col1, audio_col2 = st.columns(2)
        with audio_col1:
            st.write("**🎧 التسجيل الصوتي - الجزء 1**")
            audio_1_url = get_embed_link("https://drive.google.com/file/d/1m39lOssDrfcmp8k8WodTm5I9hwSR3yz_/view?usp=drivesdk")
            st.components.v1.iframe(audio_1_url, height=140, scrolling=False)
        with audio_col2:
            st.write("**🎧 التسجيل الصوتي - الجزء 2**")
            audio_2_url = get_embed_link("https://drive.google.com/file/d/1ATfgn9CAq4WvjHZniLbWfsbg8z-wprw2/view?usp=drivesdk")
            st.components.v1.iframe(audio_2_url, height=140, scrolling=False)

        st.markdown("---")

        st.subheader("🖼️ الوثائق والتمارين المرفقة")
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            st.write("**📄 وثيقة / تمرين 1**")
            doc_1_url = get_embed_link("https://drive.google.com/file/d/1u4GJMFLLG80uQ5EVnSrqNpLmGAudJ_ZN/view?usp=drivesdk")
            st.components.v1.iframe(doc_1_url, height=500, scrolling=True)
        with img_col2:
            st.write("**📄 وثيقة / تمرين 2**")
            doc_2_url = get_embed_link("https://drive.google.com/file/d/1DQRAtslUQY-T0EREb08bZhZxrcn4sGpx/view?usp=drivesdk")
            st.components.v1.iframe(doc_2_url, height=500, scrolling=True)

    # ================= ⭐ قسم التقييم والملاحظات =================
    st.markdown("---")
    st.header("⭐ تقييم الدرس")
    rating = st.selectbox("كيف تقيم فهمك لدرس اليوم؟", ["ممتاز ⭐⭐⭐⭐⭐", "جيد جداً ⭐⭐⭐⭐", "جيد ⭐⭐⭐", "يحتاج لمزيد من الشرح ⭐⭐"])
    user_comment = st.text_input("أضف تعليقك أو استفسارك حول الدرس هنا:")
    
    if st.button("إرسال التقييم 🌟"):
        st.session_state["feedbacks"].append({
            "code": st.session_state["student_code"],
            "rating": rating,
            "comment": user_comment
        })
        st.success("شكراً لك! تم استلام تقييمك بنجاح.")

    st.markdown("---")
    st.write("✨ **مع تحيات منصة التحضير للباكالوريا - نتمنى لكم التوفيق والنجاح** ✨")
