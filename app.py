import streamlit as st
import pandas as pd
import pdfplumber

# Function to extract tables from the PDF and clean repeated headers
def extract_pdf(file):
    all_data = []
    headers = ["Date", "Total", "Accomm"]  # Only interested in these columns
    
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            st.write(f"Processing page {i + 1}")
            tables = page.extract_tables()

            if not tables:
                st.write(f"No tables found on page {i + 1}")
                continue

            for table in tables:
                st.write(f"Table from page {i + 1}:", table)  # Debugging info
                
                for row in table:
                    # Print each row to help identify issues
                    st.write(f"Row: {row}")

                    # Extract specific columns (Date, Total, Accomm) only if the row has the required length
                    if len(row) >= 9:  # Assuming column positions for Total and Accomm
                        date = row[0]  # Date is in the first column
                        total = row[2]  # Total is in the third column
                        accomm = row[7]  # Accomm is in the eighth column
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
