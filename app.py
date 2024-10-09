import streamlit as st
import pandas as pd
import pdfplumber
import re
from io import BytesIO

# Function to parse relevant data from raw text
def parse_raw_text(raw_text):
    all_data = []
    # Define the headers to capture all columns
    headers = ["Date", "Avail", "Total", "Indv", "Multi", "Occ%", "Ad Ch", "Accomm", "F&B", "Other", "Total Revenue"]

    # Updated regular expression to capture all columns
    # This assumes columns like date, avail, total, indv, multi, occ%, ad ch, accomm, etc.
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
    with pdfplumber.open
