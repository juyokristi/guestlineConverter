import streamlit as st
import pandas as pd
import pdfplumber

# Function to extract tables from PDF using pdfplumber
def extract_pdf(file):
    tables = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    
    # Convert the list of tables into a pandas DataFrame
    # Assuming the PDF has a consistent table format
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

    # Download as Excel
    excel = df.to_excel(index=False, engine='xlsxwriter')
    st.download_button("Download as Excel", excel, "data.xlsx")
