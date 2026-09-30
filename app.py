import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.title("Citizen Grievance Portal")

# 1. Expanded Language Selector (Including Indian Languages)
languages = {
    "English": "en",
    "Tamil (தமிழ்)": "ta",
    "Hindi (हिंदी)": "hi",
    "Telugu (తెలుగు)": "te",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Malayalam (മലയാളം)": "ml",
    "Marathi (मराठी)": "mr",
    "Bengali (বাংলা)": "bn",
    "Portuguese (Brasil)": "pt",
    "Russian (Россия)": "ru",
    "Chinese (中国)": "zh"
}

selected_lang_name = st.selectbox("Select Language / மொழியைத் தேர்ந்தெடுக்கவும் / भाषा चुनें", list(languages.keys()))
lang_code = languages[selected_lang_name]

# 2. Text Input
text_complaint = st.text_area(f"Enter your complaint ({selected_lang_name}):")

# 3. Voice Input
st.write(f"🎤 Record voice note ({selected_lang_name}):")
audio_data = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key=f'voice_{lang_code}')

if audio_data:
    st.audio(audio_data['bytes'])
    st.success("Voice note captured successfully!")

# 4. Image Upload
image_file = st.file_uploader("Upload an image of the issue (Optional)", type=["jpg", "png", "jpeg"])

# 5. Submit Action
if st.button("Submit Complaint"):
    if not text_complaint and not audio_data and not image_file:
        st.warning("Please provide a complaint via text, voice, or image.")
    else:
        st.success(f"Complaint registered successfully in {selected_lang_name}!")
