import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(
    page_title="GLC Text To Voice", 
    page_icon="🎙️", 
    layout="wide"
)

st.title("🎬 GLC Text To Voice")
st.write("Video Editor များနှင့် လူငယ် Creator များအတွက် အဆင့်မြင့် AI Voice & Chat Assistant")
st.write("---")

# 2. Free Credit System
if 'used_credits' not in st.session_state:
    st.session_state.used_credits = 0

DAILY_LIMIT = 3000
remaining_credits = DAILY_LIMIT - st.session_state.used_credits

# 3. Sidebar Setup
st.sidebar.header("🔑 API Configurations")
api_key = st.sidebar.text_input(
    "Google AI Studio API Key", 
    type="password",
    placeholder="AI Studio Key ကို ဖြည့်ပါ"
)

st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Free Credit ယနေ့အတွက်:**")
st.sidebar.info(f"ကျန်ရှိစာလုံးရေ: {remaining_credits} / {DAILY_LIMIT}")

# 4. Multi-Language Voice Option Database
languages_db = {
    "မြန်မာ (Burmese)": {"code": "my", "voices": ["Standard Female Voice"]},
    "English (US)": {"code": "en", "voices": ["Male Accent", "Female Accent"]},
    "ไทย (Thai)": {"code": "th", "voices": ["Standard Thai"]},
    "日本語 (Japanese)": {"code": "ja", "voices": ["Tokyo Native"]}
}

# 5. Tabs Layout
tab1, tab2 = st.tabs(["🎙️ Text To Voice", "💬 GLC AI Chat Studio"])

# --- TAB 1: TEXT TO VOICE ---
with tab1:
    st.header("စာသားမှ အသံပြောင်းလဲခြင်း")
    col1, col2 = st.columns(2)
    
    with col1:
        lang_choice = st.selectbox("ဘာသာစကား ရွေးချယ်ရန်", list(languages_db.keys()))
        voice_choice = st.selectbox("အသံအမျိုးအစား", languages_db[lang_choice]["voices"])
    
    with col2:
        speed_choice = st.slider("အသံနှုန်း (Speed)", 0.5, 2.0, 1.0, 0.1)

    text_input = st.text_area("အသံပြောင်းမည့် စာသားများကို ရိုက်ထည့်ပါ", placeholder="ဒီနေရာမှာ စာသားရိုက်ပါ...")

    if st.button("Generate Audio 🚀", key="tts_btn"):
        if not text_input:
            st.error("ကျေးဇူးပြု၍ စာသားတစ်ခုခု ရိုက်ထည့်ပေးပါ။")
        elif len(text_input) > remaining_credits:
            st.error("⚠️ သင်၏ ယနေ့အတွက် Free Credit မလုံလောက်တော့ပါ။")
        else:
            with st.spinner("အသံဖိုင် ဖန်တီးနေပါသည်..."):
                try:
                    lang_code = languages_db[lang_choice]["code"]
                    tts = gTTS(text=text_input, lang=lang_code, slow=(speed_choice < 1.0))
                    
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    
                    st.audio(fp, format='audio/mp3')
                    st.success("🎉 အသံဖိုင် အောင်မြင်စွာ ထွက်ပေါ်လာပါပြီ။")
                    
                    st.session_state.used_credits += len(text_input)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TAB 2: AI CHAT STUDIO ---
with tab2:
    st.header("AI Creator Chat")
    st.write("Video Idea များ၊ Video Script များနှင့် Content Strategy မေးမြန်းနိုင်ပါသည်။")
    
    if not api_key:
        st.info("💡 AI Chat အသုံးပြုရန် Sidebar တွင် သင်၏ API Key ကို ဖြည့်သွင်းပေးပါ။")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        chat_input = st.text_input("AI အား စိတ်ကြိုက်မေးမြန်းရန် (ဥပမာ- Movie Recap Script ရေးပေးပါ)")
        
        if st.button("Ask AI ✨", key="chat_btn"):
            if chat_input:
                with st.spinner("AI စဉ်းစားနေပါသည်..."):
                    try:
                        full_prompt = f"You are GLC AI, a helpful scriptwriter and assistant for content creators. Query: {chat_input}"
                        response = model.generate_content(full_prompt)
                        st.markdown("### 🤖 AI Response:")
                        st.info(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("မေးခွန်းတစ်ခုခု ရိုက်ထည့်ပေးပါ။")
