import streamlit as st
import pandas as pd
import pdfplumber
from io import BytesIO

# Function to extract tables from the PDF and clean repeated headers
def extract_pdf(file):
    all_data = []
    headers = ["Date", "Total", "Accomm"]  # Only interested in these columns
    
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Extract table data
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Extract specific columns (Date, Total, Accomm) only if the row has the required length
                    if len(row) >= 9:  # Assuming column positions for Total and Accomm
                        date = row[0]  # Date is in the first column
                        total = row[2]  # Total is in the third column
                        accomm = row[7]  # Accomm is in the eighth column
                        all_data.append([date, total, accomm])

    # Convert list of rows into a pandas DataFrame
    df = pd.DataFrame(all_data, columns=headers)
    
    return df

# Streamlit interface
st.title("PDF to CSV/Excel Converter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    df = extract_pdf(uploaded_file)
    
    if df.empty:
        st.error("No data extracted from the PDF. Please check the file format.")
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
