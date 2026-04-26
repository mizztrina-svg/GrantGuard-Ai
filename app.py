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
            prompt = f"Analyze this business text for grant-readiness. Provide a score out of 100 and 3 tips for improvement. Text: {text}"
            response = model.generate_content(prompt)
            st.markdown("### **Audit Results**")
            st.write(response.text)
else:
    if not api_key:
        st.info("Please enter your Gemini API Key in the sidebar to begin.")
