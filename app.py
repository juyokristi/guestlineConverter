import streamlit as st
import pandas as pd
import pdfplumber
from io import BytesIO

# Helper function to check if a row contains a valid date
def is_valid_date(row):
    try:
        pd.to_datetime(row[0], format="%d/%m/%Y")
        return True
    except (ValueError, IndexError):
        return False

# Function to extract relevant data from the PDF
def extract_pdf(file):
    all_data = []
    headers = ["Date", "Total", "Accomm"]

    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            st.write(f"Processing page {i + 1}")
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    # Log row for debugging
                    st.write(f"Row length: {len(row)} - Row content: {row}")

                    # Skip row if it is not valid (doesn't have at least 8 columns)
                    if len(row) < 8:
                        st.write(f"Skipping row due to insufficient columns: {row}")
                        continue
                    
                    # Skip known header row by length and content
                    if row[0].startswith("ANGELCHIPP"):
                        st.write(f"Skipping header row: {row}")
                        continue

                    # Check if the row starts with a valid date
                    if is_valid_date(row):
                        # Extract Date, Total, Accomm (adjust the indices if needed)
                        date = row[0]
                        total = row[2]
                        accomm = row[7]
                        all_data.append([date, total, accomm])

    # Convert list of rows into a pandas DataFrame
    if all_data:
        df = pd.DataFrame(all_data, columns=headers)
        return df
    else:
        return None

# Streamlit interface
st.title("PDF to CSV/Excel Converter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    df = extract_pdf(uploaded_file)
    
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
