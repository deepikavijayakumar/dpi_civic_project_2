import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Portal", ["Citizen Portal", "Government Admin Dashboard"])

# Initialize session state for storing complaints if it doesn't exist
if "complaints" not in st.session_state:
    st.session_state.complaints = []

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
            # AI Analysis Simulation (Categorization, Urgency & Summarization)
            with st.spinner("🤖 AI is analyzing your multi-modal complaint..."):
                # Basic rule-based AI simulation or hook it up to Gemini API here
                content_lower = text_complaint.lower()
                if "pothole" in content_lower or "road" in content_lower:
                    category = "Infrastructure / Roads"
                    urgency = "High"
                elif "water" in content_lower or "leak" in content_lower:
                    category = "Water Supply"
                    urgency = "Medium"
                elif "garbage" in content_lower or "waste" in content_lower:
                    category = "Sanitation"
                    urgency = "Medium"
                else:
                    category = "General Civic Issue"
                    urgency = "Low"

            # Save to session state so Admin Dashboard can see it
            new_complaint = {
                "language": selected_lang_name,
                "text": text_complaint if text_complaint else "[Voice/Image Submission]",
                "category": category,
                "urgency": urgency,
                "status": "Pending Review"
            }
            st.session_state.complaints.append(new_complaint)

            st.success(f"Complaint registered successfully in {selected_lang_name}!")
            st.info(f"🤖 **AI Analysis Result:** Categorized under **{category}** with **{urgency} Urgency**.")

# 2. GOVERNMENT ADMIN DASHBOARD
elif app_mode == "Government Admin Dashboard":
    st.title("🏛️ Government Admin Dashboard")
    st.write("Review, track, and manage incoming AI-analyzed citizen grievances.")
    
    total_count = len(st.session_state.complaints)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints", total_count)
    col2.metric("Resolved", "0")
    col3.metric("Pending Review", total_count)

    st.subheader("Live AI-Processed Complaints Feed")
    
    if total_count == 0:
        st.warning("No complaints submitted yet. Go to the Citizen Portal, submit a complaint, and see the AI analysis appear here instantly!")
    else:
        for idx, comp in enumerate(st.session_state.complaints):
            with st.expander(f"Complaint #{idx+1} - {comp['category']} ({comp['urgency']} Urgency)"):
                st.write(f"**Language:** {comp['language']}")
                st.write(f"**Description:** {comp['text']}")
                st.write(f"**AI Assigned Category:** {comp['category']}")
                st.write(f"**Urgency Level:** {comp['urgency']}")
                st.write(f"**Status:** {comp['status']}") here!")
