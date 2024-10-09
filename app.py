import streamlit as st
import pdfplumber
import re

# Streamlit interface
st.title("PDF Raw Text Debugger")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for i, page in enumerate(pdf.pages):
            st.write(f"Processing page {i + 1}")
            # Extract the raw text from each page and display it
            page_text = page.extract_text()
            st.write(f"Raw text from page {i + 1}:")
            st.text(page_text)  # Display the extracted raw text
            full_text += page_text

    # Optionally display all the text at once
    st.write("Full extracted text from the entire PDF:")
    st.text(full_text)
