import streamlit as st
import requests

st.title("📄 Plagiarism Checker")

st.markdown("Upload original and submitted text files to check for plagiarism.")

original_file = st.file_uploader("Upload Original File", type=["txt"])
submission_file = st.file_uploader("Upload Submission File", type=["txt"])

if st.button("Check Plagiarism") and original_file and submission_file:
    with st.spinner("Checking..."):
        files = {
            "original": original_file,
            "submission": submission_file
        }
        try:
            response = requests.post("http://localhost:5000/check", files=files)
            if response.status_code == 200:
                data = response.json()
                st.metric("Similarity Score", f"{data['similarity_score'] * 100:.2f}%")
                st.metric("Plagiarism Probability", f"{data['probability'] * 100:.2f}%")
                st.success("Plagiarism Detected" if data["plagiarized"] else "No Plagiarism Detected")

                st.markdown("### 🔍 Highlighted Matches in Original")
                st.markdown(data["highlighted_original"], unsafe_allow_html=True)

                st.markdown("### 🔍 Highlighted Matches in Submission")
                st.markdown(data["highlighted_submission"], unsafe_allow_html=True)
            else:
                st.error("Error from Flask API")
        except Exception as e:
            st.error(f"Connection failed: {e}")
