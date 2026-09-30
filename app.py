import streamlit as st

# Initialize complaints list with default examples
if "complaints" not in st.session_state:
    st.session_state.complaints = [
        {"id": 1, "text": "A large pothole has formed near the main junction on Anna Nagar 2nd Avenue.", "status": "Pending"},
        {"id": 2, "text": "An uncollected pile of garbage has been sitting for three days near Usman Road.", "status": "In Progress"}
    ]

# Sidebar View Switcher
st.sidebar.title("Portal Navigation")
portal_mode = st.sidebar.radio("Select View", ["Citizen Portal", "Government Admin Portal"])

# Citizen Portal View
if portal_mode == "Citizen Portal":
    st.header("Citizen Grievance Portal")
    
    new_complaint = st.text_input("Enter your complaint:")
    
    # File uploader for images
    uploaded_image = st.file_uploader("Upload an image of the issue (Optional)", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Issue Photo", width=300)
    
    if st.button("Submit Complaint"):
        if new_complaint:
            new_id = len(st.session_state.complaints) + 1
            st.session_state.complaints.append({
                "id": new_id, 
                "text": new_complaint, 
                "status": "Pending",
                "image": uploaded_image
            })
            st.success("Complaint submitted successfully with photo!")
            
    st.subheader("Track Complaints")
    for c in st.session_state.complaints:
        st.write(f"**ID:** {c['id']} | **Complaint:** {c['text']} | **Status:** `{c['status']}`")
        if "image" in c and c["image"] is not None:
            st.image(c["image"], width=150)

# Government Admin Portal View
elif portal_mode == "Government Admin Portal":
    st.header("Government Official Dashboard")
    st.write("Review and update citizen complaints.")

    for i, c in enumerate(st.session_state.complaints):
        st.markdown(f"---")
        st.write(f"**Complaint ID:** {c['id']}")
        st.write(f"**Description:** {c['text']}")
        if "image" in c and c["image"] is not None:
            st.image(c["image"], width=150)
        
        current_status_index = ["Pending", "In Progress", "Resolved"].index(c['status'])
        new_status = st.selectbox(
            f"Update Status for ID {c['id']}", 
            ["Pending", "In Progress", "Resolved"], 
            index=current_status_index, 
            key=f"status_{i}"
        )
        
        if st.button(f"Save Status for ID {c['id']}", key=f"btn_{i}"):
            st.session_state.complaints[i]['status'] = new_status
            st.success(f"Complaint ID {c['id']} updated to **{new_status}**!")
