import streamlit as st
import pandas as pd
import pdfplumber
from io import BytesIO

# Function to extract tables from the PDF and clean repeated headers
def extract_pdf(file):
    all_data = []
    headers = ["Date", "Avail", "Total", "Indv", "Multi", "Occ%", "Ad Ch", "Accomm", "F&B", 
               "Other", "ARR", "Blocks", "Rooms Sold", "Sleepers", "Inf", "APR", "Yield"]
    
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Extract table data
            tables = page.extract_tables()

            for table in tables:
                if table:  # Check if the table contains data
                    for row in table:
                        # Only append row if it's not a header
                        if row != headers and len(row) > 1:  # Ensure row contains data
                            # Adjust rows that don't have the right number of columns
                            if len(row) != len(headers):
                                row.extend([None] * (len(headers) - len(row)))
                            all_data.append(row)

    # Convert list of rows into a pandas DataFrame
    if all_data:
        df = pd.DataFrame(all_data, columns=headers)
    else:
        df = pd.DataFrame(columns=headers)  # Empty DataFrame if no data found
    
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
        writer.close()  # Replacing writer.save() with writer.close()
        output.seek(0)

        # Download as Excel
        st.download_button("Download as Excel", output, "cleaned_data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
