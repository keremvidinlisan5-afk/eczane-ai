import streamlit as st
import google.generativeai as genai

# --- GÜVENLİ BAĞLANTI ---
# API Key'i kodun içine yazma, Streamlit Secrets'tan alacağız
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("API Anahtarı bulunamadı! Streamlit Secrets ayarını yapmalısın.")

    # Mevcut modelleri tara ve çalışan ilkini seç
    model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_list else model_list[0]
    model = genai.GenerativeModel(target)
except Exception as e:
    st.error(f"Sistem başlatılamadı: {e}")

# --- ARAYÜZ ---
st.set_page_config(page_title="Karşıyaka Eczanesi AI", layout="wide")
st.title("🔬 Karşıyaka'nın En İyi Eczanesi | AI Asistanı")

hikaye = st.text_area("Hasta Şikayeti:", placeholder="Şikayeti buraya yazın...", height=200)

if st.button("Analiz Et ✨"):
    if hikaye:
        with st.spinner("AI Eczacı inceliyor..."):
            try:
                response = model.generate_content(f"Sen bir eczacısın. Şikayet: {hikaye}. 3 rutin öner.")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
