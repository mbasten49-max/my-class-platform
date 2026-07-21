import streamlit as st
import re

# إعدادات الصفحة والعنوان
st.set_page_config(page_title="منصة الأستاذ الحسن التعليمية", page_icon="📚", layout="centered")

# دالة تحويل روابط قوقل درايف إلى روابط تضمين
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

# نظام التحقق من الدخول
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "student_code" not in st.session_state:
    st.session_state["student_code"] = ""

if not st.session_state["authenticated"]:
    st.title("🔒 منصة الأستاذ الحسن التعليمية")
    st.write("مرحباً بك! هذه المنصة محمية ومخصصة للطلاب المشتركين فقط.")
    
    # 📌 السطر المصلح هنا: نص واحد فقط داخل الدالة
    password = st.text_input("أدخل رمز الاشتراك الخاص بك المستعمل:", type="password")
    
    if st.button("دخول المنصة"):
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
            # قائمة احتياطية في حال عدم وجود ملف المفكرة
            allowed_passwords = ["E1 1514", "E2 1513", "E3 1515", "E4 1516", "E5 1517", "E5 1518", "1514", "1513", "1515"]
        
        if clean_password in allowed_passwords:
            # نظام بصمة الجهاز لمنع التكرار
            current_session_id = st.context.headers.get("User-Agent", "unknown_device")
            
            if clean_password in st.session_state["code_device_registry"]:
                if st.session_state["code_device_registry"][clean_password] != current_session_id:
                    st.error(f"🚨 تنبيه أمني: هذا الكود ({clean_password}) تم تشغيله على جهاز آخر! تم قفل الحساب مؤقتاً، يرجى مراجعة الأستاذ الحسن.")
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
            st.error("رمز الاشتراك غير صحيح! يرجى التحقق من الأستاذ الحسن.")
else:
    # واجهة لوحة التحكم الداخلية للأستاذ والطلاب
    st.title("📂 لوحة التحكم في الدروس التعليمية")
    st.sidebar.write(f"👤 الكود النشط حالياً: {st.session_state['student_code']}")
    
    # لوحة مراقبة للأستاذ
    if st.sidebar.checkbox("🛠️ لوحة مراقبة الأستاذ"):
        st.write("### 🕵️ الأكواد النشطة حالياً في النظام:")
        st.json(st.session_state["code_device_registry"])
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.markdown("---")
    
    # 🎥 قسم الفيديوهات التعليمية
    st.header("🎥 الفيديوهات المتاحة")
    st.info("سيتم عرض الفيديوهات هنا بمجرد إضافة روابطها في الكود.")

    st.markdown("---")

    # 🎵 قسم المقاطع الصوتية
    st.header("🎵 المقاطع الصوتية المتاحة")
    audio_url = get_embed_link("https://drive.google.com/file/d/1Z_s7pVsJbr3gNQ-oCSJjtIuzB-pU4HhV/view?usp=drivesdk")
    st.components.v1.iframe(audio_url, height=150, scrolling=False)

    st.markdown("---")

    # 🖼️ قسم الصور والتمارين التوضيحية
    st.header("🖼️ الصور والرسوم التوضيحية المتاحة")
    image_url = get_embed_link("https://drive.google.com/file/d/1egWOoyQlT6f8FScmdwWFCl2e80SAPYm9/view?usp=drivesdk")
    st.components.v1.iframe(image_url, height=450, scrolling=True)
