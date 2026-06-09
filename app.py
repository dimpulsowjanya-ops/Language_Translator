import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO

# Page configuration
st.set_page_config(page_title="Global Text & Voice Translator", page_icon="🔊", layout="centered")

# Supported languages list mapping names to simple codes and speech accents
LANGUAGES = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Mandarin Chinese": "zh-CN",
    "Arabic": "ar",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Russian": "ru",
    "Bengali": "bn",
    "Telugu": "te"
}

st.title("🌐 Text & Speech AI Translator")
st.write("Type your text, translate instantly, and play back the audio pronunciation.")

st.divider()

# Create two columns for clean side-by-side control layout
col1, col2 = st.columns(2)

with col1:
    st.write("### 📥 Source Settings")
    source_options = ["Auto-Detect"] + list(LANGUAGES.keys())
    source_lang_name = st.selectbox("Text is written in:", source_options)
    source_code = "auto" if source_lang_name == "Auto-Detect" else LANGUAGES[source_lang_name]

with col2:
    st.write("### 📤 Target Settings")
    target_lang_name = st.selectbox("Translate into:", list(LANGUAGES.keys()))
    target_code = LANGUAGES[target_lang_name]

st.write("") 

# Main Text Input Area
st.write("### ✍️ Enter Text")
input_text = st.text_area(
    "Type or paste your text here:", 
    height=130, 
    placeholder="Type something here to translate..."
)

translate_button = st.button("🔄 Translate & Generate Audio", use_container_width=True)

st.divider()

# Processing the text translation and speech generation
if translate_button:
    if input_text.strip():
        try:
            # 1. Machine Translation Layer
            with st.spinner("Translating text..."):
                translated_text = GoogleTranslator(source=source_code, target=target_code).translate(input_text)
            
            # Display text result block
            st.write(f"### ✨ Result ({target_lang_name}):")
            st.success(translated_text)
            st.code(translated_text, language="text")
            
            # 2. Text-to-Speech Audio Layer
            with st.spinner("Generating audio pronunciation..."):
                # Run speech generator engine
                tts = gTTS(text=translated_text, lang=target_code, slow=False)
                
                # Convert the audio into an in-memory byte buffer to avoid Windows disk storage errors
                audio_buffer = BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
            
            # Display native Streamlit audio player block
            st.write("### 🔊 Listen:")
            st.audio(audio_buffer, format="audio/mp3")
            
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
    else:
        st.warning("Please input text inside the box before running.")
