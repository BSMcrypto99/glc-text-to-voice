import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# Page Configuration
st.set_page_config(page_title="GLC Text To Voice", page_icon="🎙️", layout="wide")

st.title("🎬 GLC Text To Voice")
st.write("Video Editor များနှင့် လူငယ် Creator များအတွက် အဆင့်မြင့် AI Voice & Chat Assistant")
st.write("---")

# Free Credit System Initialization
if 'used_credits' not in st.session_state:
    st.session_state.used_credits = 0

DAILY_LIMIT = 3000
remaining_credits = DAILY_LIMIT - st.session_state.used_credits

# --- SIDEBAR SETUP ---
st.sidebar.header("🔑 API Configurations")

# API Key ကို Session State ထဲတွင် အသေသေချာချာ သိမ်းဆည်းရန် ပြင်ဆင်ခြင်း
if 'api_key_input' not in st.session_state:
    st.session_state.api_key_input = ""

api_key = st.sidebar.text_input(
    "Google AI Studio API Key", 
    type="password", 
    value=st.session_state.api_key_input,
    placeholder="AI Studio Key ကို ဖြည့်ပါ"
)

# User ရိုက်ထည့်လိုက်သော Key ကို အတည်ပြုသိမ်းဆည်းခြင်း
if api_key:
    st.session_state.api_key_input = api_key

st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Free Credit ယနေ့အတွက်:**")
st.sidebar.info(f"ကျန်ရှိစာလုံးရေ: {remaining_credits} / {DAILY_LIMIT}")

# Multi-Language Voice Option Database
languages_db = {
    "မြန်မာ (Burmese)": {"code": "my", "voices": ["Standard Female"]},
    "English (US)": {"code": "en", "voices": ["Male Accent", "Female Accent"]},
    "ไทย (Thai)": {"code": "th", "voices": ["Standard Thai"]},
    "日本語 (Japanese)": {"code": "ja", "voices": ["Tokyo Native"]}
}

# Tabs Layout
tab1, tab2 = st.tabs(["🎙️ Text To Voice", "💬 AI Chat Studio"])

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

# --- TAB 2: AI CHAT STUDIO (ပြင်ဆင်ပြီး) ---
with tab2:
    st.header("AI Creator Chat")
    st.write("Video Idea များ၊ Video Script များနှင့် Content Strategy မေးမြန်းနိုင်ပါသည်။")
    
    # ရိုက်ထည့်ထားသော API Key ရှိမရှိကို သေချာစွာ စစ်ဆေးခြင်း
    if not st.session_state.api_key_input:
        st.info("💡 AI Chat အသုံးပြုရန် Sidebar တွင် သင်၏ API Key ကို ဖြည့်သွင်းပေးပါ။")
    else:
        try:
            genai.configure(api_key=st.session_state.api_key_input)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            chat_input = st.text_input("AI အား စိတ်ကြိုက်မေးမြန်းရန် (ဥပမာ- Movie Recap Script ရေးပေးပါ)")
            
            if st.button("Ask AI ✨", key="chat_btn"):
                if chat_input:
                    with st.spinner("AI စဉ်းစားနေပါသည်..."):
                        full_prompt = f"You are GLC AI, a helpful scriptwriter and assistant for content creators. Query: {chat_input}"
                        response = model.generate_content(full_prompt)
                        st.markdown("### 🤖 AI Response:")
                        st.info(response.text)
                else:
                    st.error("မေးခွန်းတစ်ခုခု ရိုက်ထည့်ပေးပါ။")
        except Exception as e:
            st.error(f"API Key သို့မဟုတ် စနစ်ချိတ်ဆက်မှု လွဲမှားနေပါသည်- {e}")
