import streamlit as st
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="GrantGuard AI", page_icon="🛡️")

st.title("🛡️ GrantGuard AI")
st.subheader("Professional Grant-Readiness Auditor")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and api_key:
    try:
        genai.configure(api_key=api_key)
        
        # This part automatically finds the best model available in your account
        # to prevent the 404 error once and for all.
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_to_use = models[0] if models else 'gemini-pro'
        model = genai.GenerativeModel(model_to_use)
        
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        
        if st.button("Run Audit"):
            with st.spinner(f"Using {model_to_use} to analyze Jacob's Party Box Rentals..."):
                prompt = f"Analyze this business plan for grant-readiness. Provide a score out of 100 and 3 tips for improvement. Text: {text}"
                response = model.generate_content(prompt)
                st.markdown("### **Audit Results**")
                st.write(response.text)
    except Exception as e:
        st.error(f"Almost there! Just a small tweak needed: {e}")
else:
    st.info("Paste your key on the left and upload your PDF to get started.")
        
