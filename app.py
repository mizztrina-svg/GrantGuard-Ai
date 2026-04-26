import streamlit as st
import PyPDF2
import google.generativeai as genai

# Setup page
st.set_page_config(page_title="GrantGuard AI", page_icon="🛡️")

st.title("🛡️ GrantGuard AI")
st.subheader("Professional Grant-Readiness Auditor")
st.write("Upload your business plan below. Our AI will audit your document for major small business grants.")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Try the most common model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Read PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        
        if st.button("Run Audit"):
            if not text.strip():
                st.error("Could not read text from this PDF. Please make sure it's not a scanned image.")
            else:
                with st.spinner("Analyzing Jacob's Party Box Rentals plan..."):
                    prompt = f"Analyze this business text for grant-readiness. Provide a score out of 100 and 3 tips for improvement. Text: {text}"
                    response = model.generate_content(prompt)
                    st.markdown("### **Audit Results**")
                    st.write(response.text)
    except Exception as e:
        st.error(f"Connection Error: {e}. Please ensure your API key is correct.")
else:
    if not api_key:
        st.info("Please enter your Gemini API Key in the sidebar to begin.")
