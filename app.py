import streamlit as st
import pdfplumber
import re
import pandas as pd
from io import BytesIO

# Helper function to capture all data rows without a strict column pattern
def parse_raw_text(raw_text):
    all_data = []

    # Display the raw text for reference
    st.write("Extracted raw text:")
    st.text(raw_text)

    # Basic regex to capture data rows with dates and numeric values
    pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+([\d\s]+)")

    # Search for matching rows
    matches = pattern.findall(raw_text)
    
    # For debugging, show what matches were found
    st.write("Matches found:", matches)
    
    for match in matches:
        row = match[0] + " " + match[1]  # combine the date and the rest of the row's data
        all_data.append(row.split())  # split the row into individual columns

    return all_data

# Streamlit interface
st.title("PDF Data Extractor (Raw Text Mode)")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for i, page in enumerate(pdf.pages):
            st.write(f"Processing page {i + 1}")
            full_text += page.extract_text()

    # Parse the raw text to extract all data rows
    all_data = parse_raw_text(full_text)
    
    if not all_data:
        st.error("No data extracted from the PDF. Please check the file format or columns.")
    else:
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        st.dataframe(df)

        # Download as CSV
        csv = df.to_csv(index=False)
        st.download_button("Download as CSV", csv, "extracted_data.csv", "text/csv")

        # Create Excel file in memory
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.close()
        output.seek(0)

        # Download as Excel
        st.download_button("Download as Excel", output, "extracted_data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
