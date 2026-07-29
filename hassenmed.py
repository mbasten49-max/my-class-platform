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
    except Exception as e:
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

        # الأكواد المعتمدة في النظام
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
    
    # اختيار المادة
    subject = st.sidebar.radio("اختر المادة التعليمية:", ["الفيزياء والكيمياء ⚛️", "علوم الطبيعة والحياة 🧪"])
    
    st.sidebar.markdown("---")

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

    # ================= ⚛️ مادة الفيزياء والكيمياء =================
    if subject == "الفيزياء والكيمياء ⚛️":
        st.title("📚 درس: السينماتيك والديناميك (Cinématique et Dynamique)")
        st.success("مرحباً بكم! نتمنى لكم مشاهدة ممتعة وتحصيلاً علمياً موفقاً.")
        st.markdown("---")

        # 1️⃣ الفيديوهات الشارحة
        st.header("🎥 الفيديوهات الشارحة للدرس")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📹 الجزء الأول")
            video_1_url = get_embed_link("https://drive.google.com/file/d/1akAEFa8OnXTwmN1HXofoO6CG0FqkG7ah/view?usp=drivesdk")
            st.components.v1.iframe(video_1_url, height=315, scrolling=False)

        with col2:
            st.subheader("📹 الجزء الثاني")
            video_2_url = get_embed_link("https://drive.google.com/file/d/1P_p56TkizadnefcG_XUk8kenJwnDedSD/view?usp=drivesdk")
            st.components.v1.iframe(video_2_url, height=315, scrolling=False)

        st.markdown("---")

        # 2️⃣ التسجيلات الصوتية
        st.header("🎵 التسجيلات الصوتية")
        st.caption("استمع إلى الملاحظات والتوضيحات الصوتية الهامة الخاصة بالدرس:")
        
        audio_col1, audio_col2 = st.columns(2)
        
        with audio_col1:
            st.subheader("🎧 التسجيل الصوتي - الجزء 1")
            audio_1_url = get_embed_link("https://drive.google.com/file/d/1m39lOssDrfcmp8k8WodTm5I9hwSR3yz_/view?usp=drivesdk")
            st.components.v1.iframe(audio_1_url, height=130, scrolling=False)

        with audio_col2:
            st.subheader("🎧 التسجيل الصوتي - الجزء 2")
            audio_2_url = get_embed_link("https://drive.google.com/file/d/1ATfgn9CAq4WvjHZniLbWfsbg8z-wprw2/view?usp=drivesdk")
            st.components.v1.iframe(audio_2_url, height=130, scrolling=False)

        st.markdown("---")

        # 3️⃣ الوثائق والتمارين
        st.header("🖼️ الوثائق والتمارين المرفقة")
        img_col1, img_col2 = st.columns(2)
        
        with img_col1:
            st.subheader("📄 وثيقة / تمرين 1")
            doc_1_url = get_embed_link("https://drive.google.com/file/d/1u4GJMFLLG80uQ5EVnSrqNpLmGAudJ_ZN/view?usp=drivesdk")
            st.components.v1.iframe(doc_1_url, height=500, scrolling=True)

        with img_col2:
            st.subheader("📄 وثيقة / تمرين 2")
            doc_2_url = get_embed_link("https://drive.google.com/file/d/1DQRAtslUQY-T0EREb08bZhZxrcn4sGpx/view?usp=drivesdk")
            st.components.v1.iframe(doc_2_url, height=500, scrolling=True)

    # ================= 🧪 مادة علوم الطبيعة والحياة =================
    elif subject == "علوم الطبيعة والحياة 🧪":
        st.title("🧪 دروس علوم الطبيعة والحياة")
        st.success("مرحباً بكم في قسم العلوم الطبيعية! تابعوا الفيديوهات والصور الشارحة للدرس أدناه.")
        st.markdown("---")

        # 1️⃣ فيديوهات العلوم
        st.header("🎥 الفيديوهات الشارحة")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.subheader("📹 الفيديو الأول")
            sv_1 = get_embed_link("https://drive.google.com/file/d/13i0KO4fahDLxAPeU0UvE_mtLVVP_kHrj/view?usp=drivesdk")
            st.components.v1.iframe(sv_1, height=315, scrolling=False)

        with v_col2:
            st.subheader("📹 الفيديو الثاني")
            sv_2 = get_embed_link("https://drive.google.com/file/d/1WrQNZVDGfm_WX61L7p6Z3dKuHOafmY0d/view?usp=drivesdk")
            st.components.v1.iframe(sv_2, height=315, scrolling=False)

        st.markdown("---")

        v_col3, v_col4 = st.columns(2)
        with v_col3:
            st.subheader("📹 الفيديو الثالث")
            sv_3 = get_embed_link("https://drive.google.com/file/d/18zd5weNJiuhiHTO4LIAv_-SiNko_8o_0/view?usp=drivesdk")
            st.components.v1.iframe(sv_3, height=315, scrolling=False)

        with v_col4:
            st.subheader("📹 الفيديو الرابع")
            sv_4 = get_embed_link("https://drive.google.com/file/d/1qYR2uGxwbJAJ-B90C9U3yiDdE2I9prxY/view?usp=drivesdk")
            st.components.v1.iframe(sv_4, height=315, scrolling=False)

        st.markdown("---")

        # 2️⃣ صور ووثائق العلوم
        st.header("🖼️ الصور والوثائق الشارحة")
        s_img1, s_img2 = st.columns(2)

        with s_img1:
            st.subheader("📄 الوثيقة / الصورة 1")
            img_url_1 = get_embed_link("https://drive.google.com/file/d/1GhsHcaQOvjDLrQOkXWEPsWLiKFPV8FO5/view?usp=drivesdk")
            st.components.v1.iframe(img_url_1, height=500, scrolling=True)

        with s_img2:
            st.subheader("📄 الوثيقة / الصورة 2")
            img_url_2 = get_embed_link("https://drive.google.com/file/d/17zW26q2O1Fiqjs4MPtzSIfGrSLNXXI7h/view?usp=drivesdk")
            st.components.v1.iframe(img_url_2, height=500, scrolling=True)

    # ================= 4️⃣ قسم التقييم والملاحظات =================
    st.markdown("---")
    st.header("⭐ تقييم الدرس")
    rating = st.selectbox("كيف تقيم فهمك لدرس اليوم؟", ["ممتاز ⭐⭐⭐⭐⭐", "جيد جداً ⭐⭐⭐⭐", "جيد ⭐⭐⭐", "يحتاج لمزيد من الشرح ⭐⭐"])
    user_comment = st.text_input("أضف تعليقك أو استفسارك حول الدرس هنا:")
    
    if st.button("إرسال التقييم 🌟"):
        st.session_state["feedbacks"].append({
            "code": st.session_state["student_code"],
            "subject": subject,
            "rating": rating,
            "comment": user_comment
        })
        st.success("شكراً لك! تم استلام تقييمك بنجاح.")

    st.markdown("---")
    st.write("✨ **مع تحيات منصة التحضير للباكالوريا - نتمنى لكم التوفيق والنجاح** ✨")
