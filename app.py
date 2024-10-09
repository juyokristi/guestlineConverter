import streamlit as st
import pandas as pd
import pdfplumber
from io import BytesIO

# Function to extract tables from PDF using pdfplumber
def extract_pdf(file):
    tables = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    
    # Convert the list of tables into a pandas DataFrame
    df_list = [pd.DataFrame(table) for table in tables if len(table) > 0]
    df = pd.concat(df_list, ignore_index=True)
    return df

# Streamlit interface
st.title("PDF to CSV/Excel Converter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    df = extract_pdf(uploaded_file)

    # Displaying the DataFrame in Streamlit
    st.dataframe(df)

    # Download as CSV
    csv = df.to_csv(index=False)
    st.download_button("Download as CSV", csv, "data.csv", "text/csv")

    # Create Excel file in memory using BytesIO
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()

    # Download as Excel
    st.download_button("Download as Excel", output.getvalue(), "data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
