import streamlit as st
import google.generativeai as genai

# --- GÜVENLİ BAĞLANTI ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets ayarını kontrol edin.")

    # Modelleri tara ve en uygununu seç (404 hatasını önlemek için)
    model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_list else model_list[0]
    model = genai.GenerativeModel(target)
except Exception as e:
    st.error(f"Sistem başlatılamadı: {e}")

# --- ENVANTER BİLGİSİ (Zekaya öğretilecek liste) ---
# Buraya senin listedeki kritik markaları ve ürün gruplarını ekledim
envanter_ozet = """
Eczane Stoklarımızda Bulunan Markalar:
- BIODERMA: Sebium (Yağlı), Sensibio (Hassas), Atoderm (Kuru), Pigmentbio (Leke).
- LA ROCHE-POSAY: Effaclar, Anthelios, Lipikar, Cicaplast, Mela B3, Toleriane.
- CAUDALIE: Vinoperfect (Leke), Resveratrol (Yaşlanma Karşıtı), Vinopure, Vinohydra.
- SVR: Sebiaclear, Ampoule A/B/C, Topialyse, Cicavit.
- COSMED: Alight, Sun Essential, Skinologist, Atopia.
- CERAVE: Tüm temizleyiciler ve nemlendiriciler, Blemish Control.
- SOLANTE: Pigmenta, Acnes, Tele-Rubor, Pregna, İrritica.
- EMBRYOLISSE: Lait-Creme Concentre.
"""

# --- ARAYÜZ ---
st.set_page_config(page_title="Karşıyaka Eczanesi AI", layout="wide", page_icon="💊")
st.title("🔬 Karşıyaka'nın En İyi Eczanesi | AI Asistanı")
st.markdown("---")

with st.sidebar:
    st.header("📋 Hasta Analizi")
    hikaye = st.text_area("Şikayeti ve Detayları Yazın:", 
                          placeholder="Örn: 25 yaş, rozalı cilt, akneye meyilli...", 
                          height=300)
    analiz_et = st.button("Analiz Et ve Rutin Oluştur ✨")

if analiz_et:
    if not hikaye:
        st.warning("Lütfen önce bir şikayet metni girin.")
    else:
        # Yapay zekaya giden profesyonel komut
        prompt = f"""
        Sen Karşıyaka Eczanesi'nin dermo-kozmetik uzmanısın.
        
        Müşteri Hikayesi: {hikaye}
        
        Eczanemizdeki Güncel Stoklar:
        {envanter_ozet}
        
        Lütfen bu hastaya:
        1. Şikayetini biyolojik açıdan analiz et (yaş ve beslenme detaylarına değin).
        2. SADECE yukarıdaki stoklarda bulunan ürünleri kullanarak 3 AYRI RUTİN (Ekonomik, Orta, Premium) oluştur.
        3. Her rutin; Temizleyici, Serum ve Güneş Kremi içermeli.
        4. Aybüke abla samimiyetiyle ürünlerin neden seçildiğini açıkla.
        """
        
        with st.spinner("AI Eczacı envanteri ve şikayeti inceliyor..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
else:
    st.info("Aybüke abla, hastanın bilgilerini sol tarafa yazarak başlayabilirsin.")
