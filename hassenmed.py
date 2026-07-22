import streamlit as st
import re

# Configuration de la page
st.set_page_config(
    page_title="Plateforme Éducative Prof. El Hassan", 
    page_icon="📚", 
    layout="wide"
)

# 🎨 Style CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f6;
    }
    h1 {
        color: #1A365D !important;
        text-align: center;
        font-weight: 700;
    }
    h2, h3 {
        color: #2B6CB0 !important;
    }
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
    .rating-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #319795;
    }
    </style>
""", unsafe_allow_html=True)

# Fonction pour convertir les liens Google Drive
def get_embed_link(url):
    if "drive.google.com" in url:
        match = re.search(r'/d/([^/]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"
    return url

# Registres
if "code_device_registry" not in st.session_state:
    st.session_state["code_device_registry"] = {}

if "feedbacks" not in st.session_state:
    st.session_state["feedbacks"] = []

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "student_code" not in st.session_state:
    st.session_state["student_code"] = ""

# ================= 🔐 PAGE DE CONNEXION =================
if not st.session_state["authenticated"]:
    st.title("🔒 Plateforme Éducative Prof. El Hassan")
    st.subheader("Bienvenue sur la plateforme officielle de cours")
    st.write("Accès sécurisé réservé uniquement aux étudiants inscrits.")
    
    password = st.text_input("Entrez votre code d'accès :", type="password")
    
    if st.button("Se connecter 🚀"):
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
            st.session_state["authenticated"] = True
            st.session_state["student_code"] = clean_password
            st.rerun()
        else:
            st.error("❌ Code d'accès incorrect ! Veuillez vérifier et réessayer.")

# ================= 📖 CONTENU ÉDUCATIF =================
else:
    # Barre latérale
    st.sidebar.title("👨‍🏫 Prof. El Hassan")
    st.sidebar.info(f"👤 Code actif : **{st.session_state['student_code']}**")
    
    # Panneau professeur
    if st.sidebar.checkbox("🛠️ Panneau Professeur"):
        st.write("### 💬 Évaluations des étudiants :")
        st.write(st.session_state["feedbacks"])
    
    if st.sidebar.button("Se déconnecter 🚪"):
        st.session_state["authenticated"] = False
        st.rerun()

    # En-tête
    st.title("📚 Leçon 1 : Explications et Exercices")
    st.success("Bienvenue ! Bon visionnage et bon apprentissage.")
    st.markdown("---")

    # 1️⃣ Vidéos
    st.header("🎥 Vidéos Explicatives")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📹 Partie 1")
        video_1_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
        st.components.v1.iframe(video_1_url, height=315, scrolling=False)

    with col2:
        st.subheader("📹 Partie 2")
        video_2_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
        st.components.v1.iframe(video_2_url, height=315, scrolling=False)

    st.markdown("---")

    # 2️⃣ Audio
    st.header("🎵 Enregistrement Audio")
    st.caption("Écoutez les remarques importantes du cours :")
    audio_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
    st.components.v1.iframe(audio_url, height=120, scrolling=False)

    st.markdown("---")

    # 3️⃣ Documents / Images
    st.header("🖼️ Exercices et Illustrations")
    st.caption("Consultez les exercices ci-dessous :")
    image_url = get_embed_link("https://drive.google.com/file/d/1egWOoyQlT6f8FScmdwWFCl2e80SAPYm9/view?usp=drivesdk")
    st.components.v1.iframe(image_url, height=500, scrolling=True)

    st.markdown("---")

    # 4️⃣ Section d'évaluation (Version Compatible)
    st.header("⭐ Évaluez la leçon")
    st.markdown('<div class="rating-box">', unsafe_allow_html=True)
    
    rating = st.selectbox("Notez la leçon :", ["⭐⭐⭐⭐⭐ (Excellent)", "⭐⭐⭐⭐ (Très bien)", "⭐⭐⭐ (Bien)", "⭐⭐ (Passable)", "⭐ (À améliorer)"])
    user_comment = st.text_input("Laissez un commentaire au Prof. El Hassan (Optionnel) :")
    
    if st.button("Envoyer l'avis 🌟"):
        st.session_state["feedbacks"].append({
            "code": st.session_state["student_code"],
            "rating": rating,
            "comment": user_comment
        })
        st.success("Merci beaucoup pour votre évaluation !")
        
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #319795;'>✨ Bon succès avec le Professeur El Hassan ✨</h4>", unsafe_allow_html=True)
