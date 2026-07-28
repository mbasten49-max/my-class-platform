import streamlit as st
import re
import os
import json
from datetime import datetime

# ---------------------------------------------------------
# 1. Configuration de la page
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحضير للباكالوريا", 
    page_icon="📚", 
    layout="wide"
)

# ---------------------------------------------------------
# 2. Fonctions utilitaires & Cache
# ---------------------------------------------------------
def get_embed_link(url: str) -> str:
    """Convertit un lien Google Drive standard en lien d'intégration (preview)."""
    if "drive.google.com" in url:
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

@st.cache_data(ttl=300)
def load_allowed_passwords() -> set:
    """Charge les mots de passe autorisés depuis un fichier texte et des valeurs par défaut."""
    passwords = {
        "1513", "1514", "1515", "1516", "1517", "1518", "1519", "1520",
        "1521", "1522", "1523", "1524", "1525", "1526", "1527", "1528", "1529", "1530",
        "E1 1514", "E2 1513", "E3 1516", "E4 1517", "E5 1518", 
        "E6 1519", "E7 1520", "E8 1521", "E9 1522", "E10 1523",
        "STUDENT2026", "BAC2026", "PHYSICS101"
    }
    if os.path.exists("students.txt"):
        try:
            with open("students.txt", "r", encoding="utf-8") as f:
                for line in f:
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith("#"):
                        passwords.add(clean_line)
        except Exception:
            pass
    return passwords

def log_student_login(code: str):
    """Enregistre l'horodatage et le code de l'élève dans un fichier de log."""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logins.txt", "a", encoding="utf-8") as file:
            file.write(f"[{now}] رمز الدخول: {code}\n")
    except Exception:
        pass

def render_drive_grid(urls: list, cols_count: int = 2, height: int = 500):
    """Affiche une grille de documents/images intégrés."""
    cols = st.columns(cols_count)
    for idx, url in enumerate(urls):
        col = cols[idx % cols_count]
        embed_url = get_embed_link(url)
        with col:
            st.markdown(f"**📄 الصفحة {idx + 1}**")
            st.components.v1.iframe(embed_url, height=height, scrolling=True)

# ---------------------------------------------------------
# 3. Initialisation des états de session (Session State)
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "student_code" not in st.session_state:
    st.session_state["student_code"] = ""

if "feedbacks" not in st.session_state:
    st.session_state["feedbacks"] = []

# ---------------------------------------------------------
# 4. Page d'authentification
# ---------------------------------------------------------
if not st.session_state["authenticated"]:
    st.title("🔒 منصة التحضير للباكالوريا")
    st.write("أهلاً وسهلاً بكم! يرجى إدخال رمز الدخول الخاص بك للوصول إلى الدروس:")
    
    with st.form("login_form"):
        password = st.text_input("رمز الدخول (Code d'accès) :", type="password")
        submit_button = st.form_submit_button("تسجيل الدخول 🚀", use_container_width=True)

        if submit_button:
            clean_password = password.strip()
            allowed = load_allowed_passwords()
            
            if clean_password in allowed:
                st.session_state["authenticated"] = True
                st.session_state["student_code"] = clean_password
                log_student_login(clean_password)
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("❌ رمز الدخول غير صحيح! يرجى التأكد من الرمز وإعادة المحاولة.")

# ---------------------------------------------------------
# 5. Interface Principale & Contenu
# ---------------------------------------------------------
else:
    # Sidebar - Panneau latéral
    st.sidebar.title("👨‍🏫 منصة التحضير للباكالوريا")
    st.sidebar.info(f"الرمز النشط حالياً: `{st.session_state['student_code']}`")
    
    # Espace Enseignant
    if st.sidebar.checkbox("🛠️ لوحة تحكم الأستاذ"):
        st.subheader("👥 سجل دخول التلاميذ")
        
        if st.button("🗑️ مسح السجل القديم"):
            if os.path.exists("logins.txt"):
                os.remove("logins.txt")
                st.success("تم مسح السجل بنجاح!")
                st.rerun()

        if os.path.exists("logins.txt"):
            with open("logins.txt", "r", encoding="utf-8") as f:
                logins_data = f.readlines()
                if logins_data:
                    st.text_area("البيانات الحالية:", value="".join(reversed(logins_data)), height=200)
                else:
                    st.info("لا توجد تسجيلات دخول حالياً.")
        else:
            st.info("لا يوجد سجل دخول متوفر حتى الآن.")

        st.markdown("---")
        st.subheader("💬 تقييمات وملاحظات الطلاب")
        if st.session_state["feedbacks"]:
            st.json(st.session_state["feedbacks"])
        else:
            st.info("لا توجد تقييمات جديدة.")

    if st.sidebar.button("تسجيل الخروج 🚪", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    # Contenu Principal
    st.title("📚 الدروس المتوفرة في المنصة")
    st.write("اختر المادة والدرس للتصفح:")

    tab_math, tab_physics = st.tabs([
        "📐 الرياضيات: الأعداد المركبة (Nombre Complexe)", 
        "🧪 الفيزياء: السينماتيك والديناميك"
    ])

    # --- Onglet 1: Mathématiques ---
    with tab_math:
        st.header("📐 درس: الأعداد المركبة (Nombre Complexe)")
        st.success("مرحباً بكم في درس الرياضيات! نتمنى لكم تحصيلاً علمياً موفقاً.")
        st.markdown("---")

        st.subheader("🎥 فيديو شرح درس الأعداد المركبة")
        canva_math_video = """
        <div style="position: relative; width: 100%; height: 0; padding-top: 56.25%; overflow: hidden; border-radius: 8px;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none;"
            src="https://www.canva.com/design/DAHQq1eiNHg/vGXhkTslHgO5iI9RKli6qg/view?embed" allowfullscreen allow="fullscreen">
          </iframe>
        </div>
        """
        st.components.v1.html(canva_math_video, height=520)

        st.markdown("---")
        st.subheader("📝 ملخص وقواعد الدرس (من دفتر الشرح)")
        st.caption("تصفح أوراق الملخص المرفقة أدناه لمراجع كافة المفاهيم والقوانين:")

        math_images = [
            "https://drive.google.com/file/d/1E1JZjIgjbUA7FEIy4SsPhPSUbzkuYY03/view?usp=drivesdk",
            "https://drive.google.com/file/d/1ojVmPZLu8lCtfypoH33ACE2B300xMoKx/view?usp=drivesdk",
            "https://drive.google.com/file/d/1CRTsvEfMl7d8rAal6_8NOIhiLctyzX-r/view?usp=drivesdk",
            "https://drive.google.com/file/d/18ITRuvewvGp0LipcmpsqmmHOw9a3Qy_k/view?usp=drivesdk",
            "https://drive.google.com/file/d/1zKaKm2JR7WVuYqGtB6GLtrp376VtDIDu/view?usp=drivesdk",
            "https://drive.google.com/file/d/1Ag1bViXkgaS-Dgx4oJ9hR0d-8TU8j50l/view?usp=drivesdk",
        ]
        render_drive_grid(math_images, cols_count=2, height=500)

    # --- Onglet 2: Physique ---
    with tab_physics:
        st.header("🧪 درس: السينماتيك والديناميك (Cinématique et Dynamique)")
        st.success("مرحباً بكم في درس الفيزياء! نتمنى لكم مشاهدة ممتعة وتحصيلاً موفقاً.")
        st.markdown("---")

        st.subheader("🎥 فيديو الشرح الرئيسي للدرس")
        canva_physics_video = """
        <div style="position: relative; width: 100%; height: 0; padding-top: 56.25%; overflow: hidden; border-radius: 12px;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none;"
            src="https://www.canva.com/design/DAHQq1eiNHg/vGXhkTslHgO5iI9RKli6qg/view?embed" allowfullscreen allow="fullscreen">
          </iframe>
        </div>
        """
        st.components.v1.html(canva_physics_video, height=520)

        st.markdown("---")
        st.subheader("🎵 التسجيلات الصوتية")
        audio_col1, audio_col2 = st.columns(2)
        with audio_col1:
            st.write("**🎧 التسجيل الصوتي - الجزء 1**")
            st.components.v1.iframe(get_embed_link("https://drive.google.com/file/d/1m39lOssDrfcmp8k8WodTm5I9hwSR3yz_/view?usp=drivesdk"), height=140, scrolling=False)
        with audio_col2:
            st.write("**🎧 التسجيل الصوتي - الجزء 2**")
            st.components.v1.iframe(get_embed_link("https://drive.google.com/file/d/1ATfgn9CAq4WvjHZniLbWfsbg8z-wprw2/view?usp=drivesdk"), height=140, scrolling=False)

        st.markdown("---")
        st.subheader("🖼️ الوثائق والتمارين المرفقة")
        physics_docs = [
            "https://drive.google.com/file/d/1u4GJMFLLG80uQ5EVnSrqNpLmGAudJ_ZN/view?usp=drivesdk",
            "https://drive.google.com/file/d/1DQRAtslUQY-T0EREb08bZhZxrcn4sGpx/view?usp=drivesdk",
        ]
        render_drive_grid(physics_docs, cols_count=2, height=500)

    # --- Section Évaluation & Retours ---
    st.markdown("---")
    st.header("⭐ تقييم الدرس")
    
    with st.form("feedback_form"):
        rating = st.selectbox("كيف تقيم فهمك لدرس اليوم؟", ["ممتاز ⭐⭐⭐⭐⭐", "جيد جداً ⭐⭐⭐⭐", "جيد ⭐⭐⭐", "يحتاج لمزيد من الشرح ⭐⭐"])
        user_comment = st.text_input("أضف تعليقك أو استفسارك حول الدرس هنا:")
        submit_feedback = st.form_submit_button("إرسال التقييم 🌟")

        if submit_feedback:
            st.session_state["feedbacks"].append({
                "code": st.session_state["student_code"],
                "rating": rating,
                "comment": user_comment,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("شكراً لك! تم استلام تقييمك بنجاح.")

    st.markdown("---")
    st.write("✨ **مع تحيات منصة التحضير للباكالوريا - نتمنى لكم التوفيق والنجاح** ✨")
