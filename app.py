import streamlit as st
import PyPDF2
import google.generativeai as genai

# 1. Setup the page look
st.set_page_config(page_title="GrantGuard AI", page_icon="🛡️")

st.title("🛡️ GrantGuard AI")
st.subheader("Professional Grant-Readiness Auditor")
st.write("Upload your business plan below to receive a grant-readiness score.")

# 2. Sidebar for the API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# 3. The Logic
if uploaded_file is not None and api_key:
    try:
        genai.configure(api_key=api_key)
        
        # We use 'gemini-1.5-flash' - the most reliable model right now
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        
        if st.button("Run Audit"):
            if not text.strip():
                st.error("This PDF seems empty or is a scanned image. Please use a text-based PDF.")
            else:
                with st.spinner("Analyzing Jacob's Party Box Rentals..."):
                    prompt = f"Analyze this business plan for grant-readiness. Provide a score out of 100 and 3 tips for improvement. Text: {text}"
                    response = model.generate_content(prompt)
                    st.markdown("### **Audit Results**")
                    st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please enter your API Key in the sidebar and upload your PDF to begin.")
