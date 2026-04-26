import streamlit as st
import PyPDF2
import google.generativeai as genai

# 1. Setup the page
st.set_page_config(page_title="GrantGuard AI", page_icon="🛡️")

st.title("🛡️ GrantGuard AI")
st.subheader("Professional Grant-Readiness Auditor")
st.write("Upload your business plan below to receive a grant-readiness score.")

# 2. Sidebar for API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# 3. The Logic
if uploaded_file is not None and api_key:
    try:
        # Connect to Google
        genai.configure(api_key=api_key)
        
        # Use the most stable model name to avoid 404 errors
        model = genai.GenerativeModel('gemini-pro')
        
        # Read the PDF content
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
                    # The instructions for the AI
                    prompt = f"Analyze this business plan for grant-readiness. Provide a score out of 100 and 3 tips for improvement. Text: {text}"
                    response = model.generate_content(prompt)
                    
                    st.markdown("### **Audit Results**")
                    st.write(response.text)
                    
    except Exception as e:
        # This will catch and explain any remaining errors
        st.error(f"Setup Error: {e}")
else:
    if not api_key:
        st.info("Please enter your Gemini API Key in the sidebar and upload your PDF to begin.")
