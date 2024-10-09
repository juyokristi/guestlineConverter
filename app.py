import streamlit as st
import pandas as pd
import pdfplumber
import re
from io import BytesIO

# Function to parse relevant data from raw text (this time capturing all columns)
def parse_raw_text(raw_text):
    all_data = []
    # Assuming the columns are Date, Avail, Total, Indv, Multi, Occ%, Ad Ch, Accomm, F&B, Other, etc.
    headers = ["Date", "Avail", "Total", "Indv", "Multi", "Occ%", "Ad Ch", "Accomm", "F&B", "Other", "Total Revenue"]

    # Updated regular expression to capture all columns (adjust as needed based on actual text structure)
    # This regex assumes a structure where columns appear in order on each line
    pattern = re.compile(
        r"(\d{2}/\d{2}/\d{4})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})"
    )

    # Search for matching rows
    matches = pattern.findall(raw_text)

    for match in matches:
        all_data.append(list(match))

    # Convert list of rows into a pandas DataFrame
    if all_data:
        df = pd.DataFrame(all_data, columns=headers)
        return df
    else:
        return None

# Streamlit interface
st.title("PDF to CSV/Excel Converter - Extract All Columns")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for i, page in enumerate(pdf.pages):
            st.write(f"Processing page {i + 1}")
            full_text += page.extract_text()

    # Parse the raw text for all columns
    df = parse_raw_text(full_text)
    
    if df is None or df.empty:
        st.error("No data extracted from the PDF. Please check the file format or columns.")
    else:
        # Display the DataFrame in Streamlit
        st.dataframe(df)

        # Download as CSV
        csv = df.to_csv(index=False)
        st.download_button("Download as CSV", csv, "cleaned_data.csv", "text/csv")

        # Create Excel file in memory
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.close()
        output.seek(0)

        # Download as Excel
        st.download_button("Download as Excel", output, "cleaned_data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
