import streamlit as st
import pandas as pd
import tabula

# Function to extract tables from PDF
def extract_pdf(file):
    tables = tabula.read_pdf(file, pages='all', multiple_tables=True)
    df = pd.concat(tables, ignore_index=True)
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
