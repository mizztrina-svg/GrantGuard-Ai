import streamlit as st

# This sets up the look of your website
st.set_page_config(page_title="GrantGuard AI", page_icon="🛡️")

st.title("🛡️ GrantGuard AI")
st.markdown("### Your AI Partner for the $10,000 Skip Grant")
st.write("Upload your business plan below, and our AI will audit it for 'Grant-Readiness.'")

# This creates the "Upload" box on your website
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.success("Document received! We're ready to start the audit.")
    

