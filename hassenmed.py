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

# دالة لتحويل روابط Google Drive إلى روابط تشغيل مباشر أو معاينة
def get_embed_link(url, mode="embed"):
    if "drive.google.com" in url:
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            if mode == "stream":
                # رابط التحديث المباشر لمشغل الفيديو
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            else:
                # رابط التضمين المباشر للمستندات والملفات
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
        
        # الفيديوهات الأساسية
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("📹 مقدمة - الجزء الأول")
            video_1_url = get_embed_link("https://drive.google.com/file/d/1akAEFa8OnXTwmN1HXofoO6CG0FqkG7ah/view?usp=drivesdk", mode="stream")
            st.video(video_1_url)

        with col_b:
            st.subheader("📹 مقدمة - الجزء الثاني")
            video_2_url = get_embed_link("https://drive.google.com/file/d/1P_p56TkizadnefcG_XUk8kenJwnDedSD/view?usp=drivesdk", mode="stream")
            st.video(video_2_url)

        st.markdown("##### 🎬 سلسلة الفيديوهات التفصيلية (V1 - V8)")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.subheader("📹 الفيديو الأول (V1)")
            v1_url = get_embed_link("https://drive.google.com/file/d/1_eTKz82AyRHBvO_KJx9t73IMmq1xgwws/view?usp=drivesdk", mode="stream")
            st.video(v1_url)

        with v_col2:
            st.subheader("📹 الفيديو الثاني (V2)")
            v2_url = get_embed_link("https://drive.google.com/file/d/1MHeoWceHGZUtJvRj5gjcZogYoy_WhOT3/view?usp=drivesdk", mode="stream")
            st.video(v2_url)

        v_col3, v_col4 = st.columns(2)
        with v_col3:
            st.subheader("📹 الفيديو الثالث (V3)")
            v3_url = get_embed_link("https://drive.google.com/file/d/1N6XoTAZh5JChA8nIyf_uBYNLHuuPvl-N/view?usp=drivesdk", mode="stream")
            st.video(v3_url)

        with v_col4:
            st.subheader("📹 الفيديو الرابع (V4)")
            v4_url = get_embed_link("https://drive.google.com/file/d/1SCvZzBvC6Eu4haTxpm9PWIvM_W0fju-Y/view?usp=drivesdk", mode="stream")
            st.video(v4_url)

        v_col5, v_col6 = st.columns(2)
        with v_col5:
            st.subheader("📹 الفيديو الخامس (V5)")
            v5_url = get_embed_link("https://drive.google.com/file/d/1BWghiTBgdyRIcEEuWUjM2gpddnDl8-Xi/view?usp=drivesdk", mode="stream")
            st.video(v5_url)

        with v_col6:
            st.subheader("📹 الفيديو السادس (V6)")
            v6_url = get_embed_link("https://drive.google.com/file/d/1i6Jf1udgXvtEnJoSgR6IflM9YNlCBe8k/view?usp=drivesdk", mode="stream")
            st.video(v6_url)

        v_col7, v_col8 = st.columns(2)
        with v_col7:
            st.subheader("📹 الفيديو السابع (V7)")
            v7_url = get_embed_link("https://drive.google.com/file/d/1RbqsJ14J1GLUK4M2wDi-iwp5HH1CZ7vA/view?usp=drivesdk", mode="stream")
            st.video(v7_url)

        with v_col8:
            st.subheader("📹 الفيديو الثامن (V8)")
            v8_url = get_embed_link("https://drive.google.com/file/d/1vcO8hml4ov_0kL4wqaPM195tTS811p6m/view?usp=drivesdk", mode="stream")
            st.video(v8_url)

        st.markdown("---")

        # 2️⃣ التسجيلات الصوتية
        st.header("🎵 التسجيلات الصوتية")
        st.caption("استمع إلى الملاحظات والتوضيحات الصوتية الهامة الخاصة بالدرس:")
        
        audio_col1, audio_col2 = st.columns(2)
        
        with audio_col1:
            st.subheader("🎧 التسجيل الصوتي - الجزء 1")
            audio_1_url = get_embed_link("https://drive.google.com/file/d/1m39lOssDrfcmp8k8WodTm5I9hwSR3yz_/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(audio_1_url, height=130, scrolling=False)

        with audio_col2:
            st.subheader("🎧 التسجيل الصوتي - الجزء 2")
            audio_2_url = get_embed_link("https://drive.google.com/file/d/1ATfgn9CAq4WvjHZniLbWfsbg8z-wprw2/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(audio_2_url, height=130, scrolling=False)

        st.markdown("---")

        # 3️⃣ الوثائق والتمارين (D1 - D4)
        st.header("📄 الوثائق والتمارين (D1 - D4)")
        
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.subheader("📑 وثيقة / تمرين D1")
            d1_url = get_embed_link("https://drive.google.com/file/d/106P96_1pS1-VLQOb5JNg8pOnb29E-ki1/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(d1_url, height=500, scrolling=True)

        with d_col2:
            st.subheader("📑 وثيقة / تمرين D2")
            d2_url = get_embed_link("https://drive.google.com/file/d/1DCDYjGUTQrikjn6W7c8g5srvDMkj43HP/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(d2_url, height=500, scrolling=True)

        d_col3, d_col4 = st.columns(2)
        with d_col3:
            st.subheader("📑 وثيقة / تمرين D3")
            d3_url = get_embed_link("https://drive.google.com/file/d/1af4IDZ3dqBKfuYbfSGh7Nejsfme7WdH3/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(d3_url, height=500, scrolling=True)

        with d_col4:
            st.subheader("📑 وثيقة / تمرين D4")
            d4_url = get_embed_link("https://drive.google.com/file/d/1HDPfVTYz8fOdDUuouuugNQAhnndV8h4C/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(d4_url, height=500, scrolling=True)

        st.markdown("---")

        # 4️⃣ الصور الشارحة والمخططات (Ph1 - Ph3)
        st.header("🖼️ الصور والمخططات الشارحة (Ph1 - Ph3)")
        
        ph_col1, ph_col2 = st.columns(2)
        with ph_col1:
            st.subheader("🖼️ صورة شارحة Ph1")
            ph1_url = get_embed_link("https://drive.google.com/file/d/1-vykH4ezLRgTceOU96ppOZ6Cw-cNF7AC/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(ph1_url, height=500, scrolling=True)

        with ph_col2:
            st.subheader("🖼️ صورة شارحة Ph2")
            ph2_url = get_embed_link("https://drive.google.com/file/d/1pKfJqaepm4UIaJQcke-hK7MHSE-8IkvJ/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(ph2_url, height=500, scrolling=True)

        ph_col3, _ = st.columns(2)
        with ph_col3:
            st.subheader("🖼️ صورة شارحة Ph3")
            ph3_url = get_embed_link("https://drive.google.com/file/d/11dEgCU5BXApsgAAEVZYxfCnaNr1-47Mh/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(ph3_url, height=500, scrolling=True)

        st.markdown("---")

        # 5️⃣ قسم التمارين والحلول النموذجية
        st.header("📝 التمارين وحلولها النموذجية")
        
        # ملف التمرين الرئيسي
        st.subheader("📌 ملف التمرين الرئيسي")
        ex_url = get_embed_link("https://drive.google.com/file/d/1LktDDD5Q1064JH0j8CDIeiMgwg4vvbpS/view?usp=drivesdk", mode="embed")
        st.components.v1.iframe(ex_url, height=500, scrolling=True)

        st.markdown("##### 💡 الحلول والمتابعة")
        sol_col1, sol_col2 = st.columns(2)
        
        with sol_col1:
            st.subheader("✅ الحل الأول (Solution 1)")
            sol1_url = get_embed_link("https://drive.google.com/file/d/19nHHWNj0uSAaq5q4Z2VAkxgXFdwJvRlj/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(sol1_url, height=500, scrolling=True)

        with sol_col2:
            st.subheader("✅ تتمة الحل 1 (Suit solution 1)")
            suit1_url = get_embed_link("https://drive.google.com/file/d/1O9WrQjFYCC4aMPpGtyEkidP9wRjTZxTJ/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(suit1_url, height=500, scrolling=True)

        sol_col3, _ = st.columns(2)
        with sol_col3:
            st.subheader("✅ تتمة الحل 2 (Suit solution 2)")
            suit2_url = get_embed_link("https://drive.google.com/file/d/14bUCDKua8nsENbpG-X0U6a6_mqRrrjNN/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(suit2_url, height=500, scrolling=True)

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
            sv_1 = get_embed_link("https://drive.google.com/file/d/13i0KO4fahDLxAPeU0UvE_mtLVVP_kHrj/view?usp=drivesdk", mode="stream")
            st.video(sv_1)

        with v_col2:
            st.subheader("📹 الفيديو الثاني")
            sv_2 = get_embed_link("https://drive.google.com/file/d/1WrQNZVDGfm_WX61L7p6Z3dKuHOafmY0d/view?usp=drivesdk", mode="stream")
            st.video(sv_2)

        st.markdown("---")

        v_col3, v_col4 = st.columns(2)
        with v_col3:
            st.subheader("📹 الفيديو الثالث")
            sv_3 = get_embed_link("https://drive.google.com/file/d/18zd5weNJiuhiHTO4LIAv_-SiNko_8o_0/view?usp=drivesdk", mode="stream")
            st.video(sv_3)

        with v_col4:
            st.subheader("📹 الفيديو الرابع")
            sv_4 = get_embed_link("https://drive.google.com/file/d/1qYR2uGxwbJAJ-B90C9U3yiDdE2I9prxY/view?usp=drivesdk", mode="stream")
            st.video(sv_4)

        st.markdown("---")

        # 2️⃣ صور ووثائق العلوم
        st.header("🖼️ الصور والوثائق الشارحة")
        s_img1, s_img2 = st.columns(2)

        with s_img1:
            st.subheader("📄 الوثيقة / الصورة 1")
            img_url_1 = get_embed_link("https://drive.google.com/file/d/1GhsHcaQOvjDLrQOkXWEPsWLiKFPV8FO5/view?usp=drivesdk", mode="embed")
            st.components.v1.iframe(img_url_1, height=500, scrolling=True)

        with s_img2:
            st.subheader("📄 الوثيقة / الصورة 2")
            img_url_2 = get_embed_link("https://drive.google.com/file/d/17zW26q2O1Fiqjs4MPtzSIfGrSLNXXI7h/view?usp=drivesdk", mode="embed")
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
