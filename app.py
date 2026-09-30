import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Portal", ["Citizen Portal", "Government Admin Dashboard"])

# 1. CITIZEN PORTAL
if app_mode == "Citizen Portal":
    st.title("Citizen Grievance Portal")

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

    text_complaint = st.text_area(f"Enter your complaint ({selected_lang_name}):")

    st.write(f"🎤 Record voice note ({selected_lang_name}):")
    audio_data = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key=f'voice_{lang_code}')

    if audio_data:
        st.audio(audio_data['bytes'])
        st.success("Voice note captured successfully!")

    image_file = st.file_uploader("Upload an image of the issue (Optional)", type=["jpg", "png", "jpeg"])

    if st.button("Submit Complaint"):
        if not text_complaint and not audio_data and not image_file:
            st.warning("Please provide a complaint via text, voice, or image.")
        else:
            st.success(f"Complaint registered successfully in {selected_lang_name}!")

# 2. GOVERNMENT ADMIN DASHBOARD
elif app_mode == "Government Admin Dashboard":
    st.title("🏛️ Government Admin Dashboard")
    st.write("Review, track, and manage incoming citizen grievances here.")
    
    # Placeholder metrics / table for admin view
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints", "124", "+12 today")
    col2.metric("Resolved", "98", "79%")
    col3.metric("Pending Review", "26", "Action Required")

    st.subheader("Recent Submitted Complaints")
    st.info("No active complaints in the session storage yet. Submit one from the Citizen Portal to see it appear here!")
