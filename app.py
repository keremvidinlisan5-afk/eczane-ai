import streamlit as st
import google.generativeai as genai

# --- AYARLAR ---
API_KEY = "AIzaSyCdwedOJ5bfp-wwZXkv0s1mK5OesGHcFao"

# Sayfa Yapılandırması
st.set_page_config(page_title="Karşıyaka'nın EN İYİ Eczanesi", layout="wide", page_icon="💊")

# 1. Gemini'yi Dinamik Olarak Başlatma
def initialize_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # Bilgisayarının erişebildiği tüm modelleri listele
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not models:
            st.error("API Anahtarın hiçbir modele erişemiyor. Lütfen Google AI Studio'dan yeni bir anahtar al.")
            return None
        
        # En iyi modelleri sırayla dene
        target_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        selected_model = None
        
        for target in target_models:
            if target in models:
                selected_model = target
                break
        
        if not selected_model:
            selected_model = models[0] # Hiçbiri yoksa listedeki ilkini al
            
        return genai.GenerativeModel(selected_model)
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

model = initialize_model(API_KEY)

# --- ARAYÜZ ---
st.title("🔬 Aybüke Eczanesi Uzman AI Asistanı")
st.markdown("---")

with st.sidebar:
    st.header("📋 Hasta Analizi")
    hikaye = st.text_area("Şikayeti Detaylı Yazın:", 
                          placeholder="Örn: 25 yaş, akne lekesi, fast food beslenme...",
                          height=250)
    analiz_et = st.button("Analiz Et ve Rutin Oluştur ✨")

if analiz_et:
    if model is None:
        st.error("Model başlatılamadı. Lütfen API anahtarını kontrol et.")
    elif not hikaye:
        st.warning("Lütfen şikayet metni girin.")
    else:
        prompt = f"""
        Sen dermo-kozmetik uzmanı bir eczacısın. Aybüke'nin Dijital Asistanısın.
        Müşteri Hikayesi: {hikaye}
        
        Lütfen stoktaki markalardan (Bioderma, LRP, Caudalie, SVR, Cosmed, CeraVe, Solante) 
        hastaya uygun 3 ayrı bütçeli (Ekonomik, Orta, Premium) rutin oluştur.
        Nedenlerini bilimsel ama sıcak bir dille açıkla.
        """
        
        with st.spinner("AI Eczacı envanteri inceliyor..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"İşlem sırasında bir hata oluştu: {e}")
else:
    st.info("Aybüke abla, hastanın bilgilerini sol tarafa yazarak başlayabilirsin.")
