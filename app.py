import streamlit as st
import PyPDF2
import google.generativeai as genai

# Setup page
st.set_page_config(page_title="GrantGuard AI", page_icon="🛡️")

st.title("🛡️ GrantGuard AI")
st.subheader("Professional Grant-Readiness Auditor")
st.write("Upload your business plan or grant draft below. Our AI will audit your document for major small business grants, including the $10,000 Skip Grant.")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    if st.button("Run Audit"):
        with st.spinner("Analyzing for grant-readiness..."):
            prompt = f"""
            You are a Professional Grant Consultant. Analyze the following business text for 'Grant-Readiness.' 
            
            Evaluate based on:
            1. Clarity of Mission
            2. Community Impact
            3. Financial Viability
            4. Specific alignment with major grants like the $10,000 Skip Grant.
            
            Provide a 'Grant-Readiness Score' out of 100 and 3 specific tips to improve the application.
