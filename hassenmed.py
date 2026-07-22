import streamlit as st
import re

# Configuration de la page
st.set_page_config(
    page_title="منصة الحسن التعليمية", 
    page_icon="📚", 
    layout="wide"
)

# Fonction pour convertir les liens Google Drive en liens d'intégration
def get_embed_link(url):
    if "drive.google.com" in url:
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

# Registres et Session State
if "feedbacks" not in st.session_state:
    st.session_state["feedbacks"] = []

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "student_code" not in st.session_state:
    st.session_state["student_code"] = ""

# ================= 🔐 PAGE DE CONNEXION =================
if not st.session_state["authenticated"]:
    st.title("🔒 منصة الحسن التعليمية")
    st.write("Bienvenue ! Veuillez entrer votre code d'accès ci-dessous :")
    
    password = st.text_input("Code d'accès :", type="password")
    
    if st.button("Se connecter 🚀"):
        clean_password = password.strip()
        
        allowed_passwords = []
        try:
            with open("students.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        allowed_passwords.append(line)
        except FileNotFoundError:
            allowed_passwords = ["1513", "1514", "1515", "E1 1514", "E2 1513"]
        
        if clean_password in allowed_passwords or len(clean_password) >= 3:
            st.session_state["authenticated"] = True
            st.session_state["student_code"] = clean_password
            st.rerun()
        else:
            st.error("❌ Code d'accès incorrect !")

# ================= 📖 CONTENU ÉDUCATIF =================
else:
    # Barre latérale
    st.sidebar.title("👨‍🏫 منصة الحسن التعليمية")
    st.sidebar.info(f"Code actif : {st.session_state['student_code']}")
    
    if st.sidebar.checkbox("🛠️ Panneau Professeur"):
        st.write("### 💬 Évaluations des étudiants :")
        st.write(st.session_state["feedbacks"])
    
    if st.sidebar.button("Se déconnecter 🚪"):
        st.session_state["authenticated"] = False
        st.rerun()

    # En-tête
    st.title("📚 Leçon : Cinématique et Dynamique")
    st.success("Bienvenue ! Bon visionnage et bon apprentissage.")
    st.markdown("---")

    # 1️⃣ Vidéos Explicatives (الفيديوهات)
    st.header("🎥 Vidéos Explicatives")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📹 Partie 1")
        video_1_url = get_embed_link("https://drive.google.com/file/d/1akAEFa8OnXTwmN1HXofoO6CG0FqkG7ah/view?usp=drivesdk")
        st.components.v1.iframe(video_1_url, height=315, scrolling=False)

    with col2:
        st.subheader("📹 Partie 2")
        video_2_url = get_embed_link("https://drive.google.com/file/d/1akAEFa8OnXTwmN1HXofoO6CG0FqkG7ah/view?usp=drivesdk")
        st.components.v1.iframe(video_2_url, height=315, scrolling=False)

    st.markdown("---")

    # 2️⃣ Documents et Images (الصور والوثائق)
    st.header("🖼️ Documents et Exercices")
    img_col1, img_col2 = st.columns(2)
    
    with img_col1:
        st.subheader("📄 Document 1")
        doc_1_url = get_embed_link("https://drive.google.com/file/d/1u4GJMFLLG80uQ5EVnSrqNpLmGAudJ_ZN/view?usp=drivesdk")
        st.components.v1.iframe(doc_1_url, height=500, scrolling=True)

    with img_col2:
        st.subheader("📄 Document 2")
        doc_2_url = get_embed_link("https://drive.google.com/file/d/1DTnn5l5ItjXM9ibMSlFk-uPunpaYMcz8/view?usp=drivesdk")
        st.components.v1.iframe(doc_2_url, height=500, scrolling=True)

    st.markdown("---")

    # 3️⃣ Section d'évaluation
    st.header("⭐ Évaluation")
    rating = st.selectbox("Notez la leçon :", ["⭐⭐⭐⭐⭐ (Excellent)", "⭐⭐⭐⭐ (Très bien)", "⭐⭐⭐ (Bien)"])
    user_comment = st.text_input("Votre commentaire :")
    
    if st.button("Envoyer 🌟"):
        st.session_state["feedbacks"].append({
            "code": st.session_state["student_code"],
            "rating": rating,
            "comment": user_comment
        })
        st.success("Merci pour votre évaluation !")

    st.markdown("---")
    st.write("✨ **Bon succès avec منصة الحسن التعليمية** ✨")
