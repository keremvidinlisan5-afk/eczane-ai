import streamlit as st
import google.generativeai as genai

# --- GÜVENLİ AYAR ---
# API Key'i kodun içine yazmıyoruz, Streamlit'in 'Secrets' kısmından alacağız.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Anahtarı bulunamadı veya geçersiz. Lütfen Streamlit Secrets ayarını kontrol edin.")

# Sayfa Yapılandırması
st.set_page_config(page_title="Karşıyaka Eczanesi AI", layout="wide", page_icon="💊")

# Ana Başlık
st.title("🔬 Karşıyaka'nın En İyi Eczanesi | AI Asistanı")
st.markdown("---")

with st.sidebar:
    st.header("📋 Hasta Analizi")
    hikaye = st.text_area("Şikayeti Yazın:", placeholder="Örn: 22 yaş, rozalı cilt...", height=250)
    analiz_et = st.button("Analiz Et ✨")

if analiz_et and hikaye:
    prompt = f"Sen Karşıyaka Eczanesi'nin uzmanısın. Müşteri şikayeti: {hikaye}. Uygun bir rutin öner."
    with st.spinner("İnceleniyor..."):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Hata: {e}")