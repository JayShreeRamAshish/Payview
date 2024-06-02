import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
#import xlsxwriter
import altair as alt
from db_setup import*

st.set_page_config(
    page_title="Payroll Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="auto"
)

# Add company logo to the sidebar
logo_url = "https://c.saavncdn.com/753/Jay-Shree-Ram-Hindi-2022-20220621115533-500x500.jpg"  # Replace with your logo URL or local file path
st.sidebar.image(logo_url, use_column_width=True)
st.sidebar.title("Happy HR India Limited")

# Initialize the database
init_db()

# Streamlit Application
st.title("Data Analysis Application")

# Navigation
menu = ["PayView","Import Data","Download Payroll Data","Download Attendance Data","Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

# Bar Chart for Male and Female wise Gross Salary

if choice == "PayView":
    month = st.text_input("Enter Month (e.g., 202305 for May 2023)")
    if month:
        conn = sqlite3.connect('data_analysis.db')
        payroll_data = pd.read_sql(f"SELECT * FROM payroll WHERE Month_Val = '{month}'", conn)
        attendance_data = pd.read_sql(f"SELECT * FROM attendance WHERE Month_Val = '{month}'", conn)
        conn.close()
        # Create columns for charts
        col1, col2 = st.columns(2)
         
        with col1:
        # New chart: Department-wise Gross_Salary, Total_Deductions, Net_Pay
            st.subheader("Department-wise Gross Salary, Total Deductions, and Net Pay")
            payroll_data ['Net_Pay'] = payroll_data ['Gross_Salary'] - payroll_data ['Total_Deductions']
            chart_data = pd.melt(payroll_data , id_vars=['Department_Name'], value_vars=['Gross_Salary', 'Total_Deductions', 'Net_Pay'], var_name='Metric', value_name='Value')
            chart = alt.Chart(chart_data).mark_bar().encode(
            x='Department_Name:N',
            y='Value:Q',
            color='Metric:N',
            tooltip=['Department_Name', 'Metric', 'Value']
            ).properties(
            width=600,  # Adjusted width
            height=400  # Adjusted height
            ).configure_axis(
            labelFontSize=12,
            titleFontSize=12
            ).configure_legend(
            titleFontSize=12,
            labelFontSize=12
            )
            st.altair_chart(chart, use_container_width=False)
        
        with col2:
            st.subheader("Male and Female wise Gross Salary")
            chart = alt.Chart(payroll_data).mark_bar().encode(
            x='Gender:N',
            y='Gross_Salary:Q',
            color='Gender:N',
            column='Department_Name:N'
            ).properties(
            width=200,
            height=300
            ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
            ).configure_legend(
            titleFontSize=14,
            labelFontSize=12
            )
            st.altair_chart(chart, use_container_width=False)
        
# Import Data
elif choice == "Import Data":
    st.subheader("Import Data from Excel Sheet, Allow Files - Only xlsx")

    # Upload Payroll Data
    st.subheader("Upload Payroll Data")
    payroll_file = st.file_uploader("Upload Payroll Excel File", type=["xlsx"])

    if payroll_file:
        df = pd.read_excel(payroll_file)
        st.dataframe(df)

        if st.button("Upload Payroll Data"):
            conn = sqlite3.connect('data_analysis.db')
            df.to_sql('payroll', conn, if_exists='append', index=False)
            conn.close()
            st.success("Payroll data uploaded successfully!")

    # Upload Attendance Data
    st.subheader("Upload Attendance Data")
    attendance_file = st.file_uploader("Upload Attendance Excel File", type=["xlsx"])

    if attendance_file:
        df = pd.read_excel(attendance_file)
        st.dataframe(df)

        if st.button("Upload Attendance Data"):
            conn = sqlite3.connect('data_analysis.db')
            df.to_sql('attendance', conn, if_exists='append', index=False)
            conn.close()
            st.success("Attendance data uploaded successfully!")



# Download Payroll Data
elif choice == "Download Payroll Data":
    st.subheader("Download Payroll Data")

    # Select Month
    month = st.text_input("Enter Month (e.g., 202305 for May 2023)")

    if st.button("Load Data"):
        conn = sqlite3.connect('data_analysis.db')
        
        # Fetch Payroll Data
        payroll_query = f"SELECT * FROM payroll WHERE Month_Val = '{month}'"
        payroll_data = pd.read_sql(payroll_query, conn)
        st.subheader("Payroll Data")
        st.dataframe(payroll_data)
        conn.close()

    # Download Data
    if st.button("Download Data as Excel"):
        conn = sqlite3.connect('data_analysis.db')
        payroll_data = pd.read_sql(f"SELECT * FROM payroll WHERE Month_Val = '{month}'", conn)
        conn.close()

        with BytesIO() as b:
            with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
                payroll_data.to_excel(writer, sheet_name='Payroll', index=False)
            b.seek(0)
            st.download_button("Download Excel file", data=b, file_name=f'{month}_data.xlsx')
    # Data Analysis
    if month:
        conn = sqlite3.connect('data_analysis.db')
        payroll_data = pd.read_sql(f"SELECT * FROM payroll WHERE Month_Val = '{month}'", conn)
        conn.close()
        
# Download Attendance Data
elif choice == "Download Attendance Data":
    st.subheader("Download Attendance Data")

    # Select Month
    month = st.text_input("Enter Month (e.g., 202305 for May 2023)")

    if st.button("Load Data"):
        conn = sqlite3.connect('data_analysis.db')

        # Fetch Attendance Data
        attendance_query = f"SELECT * FROM attendance WHERE Month_Val = '{month}'"
        attendance_data = pd.read_sql(attendance_query, conn)
        st.subheader("Attendance Data")
        st.dataframe(attendance_data)
        conn.close()

    # Download Data
    if st.button("Download Data as Excel"):
        conn = sqlite3.connect('data_analysis.db')
        attendance_data = pd.read_sql(f"SELECT * FROM attendance WHERE Month_Val = '{month}'", conn)
        conn.close()

        with BytesIO() as b:
            with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
                attendance_data.to_excel(writer, sheet_name='Attendance', index=False)
            b.seek(0)
            st.download_button("Download Excel file", data=b, file_name=f'{month}_data.xlsx')

    # Data Analysis
    if month:
        conn = sqlite3.connect('data_analysis.db')
        payroll_data = pd.read_sql(f"SELECT * FROM payroll WHERE Month_Val = '{month}'", conn)
        conn.close()       
        
elif choice=="Dashboard":
    # Data Analysis
    month = st.text_input("Enter Month (e.g., 202305 for May 2023)")
    if month:
        conn = sqlite3.connect('data_analysis.db')
        payroll_data = pd.read_sql(f"SELECT * FROM payroll WHERE Month_Val = '{month}'", conn)
        attendance_data = pd.read_sql(f"SELECT * FROM attendance WHERE Month_Val = '{month}'", conn)
        conn.close()

        st.subheader("Data Analysis")

        # Department-wise Male and Female Count
        st.subheader("Department-wise Male and Female Count")
        gender_count = payroll_data.groupby(['Department_Name', 'Gender']).size().unstack(fill_value=0)
        st.table(gender_count)
        
        # Male-Female wise Salary Summary
        st.subheader("Male-Female wise Salary Summary")
        #gender_Salary_Summary = payroll_data.groupby('Gender')(['Gender','Gross_Salary']).sum()
        gender_Salary_Summary=payroll_data.groupby(['Gender','Department_Name'])['Gross_Salary'].sum().reset_index()
        st.table(gender_Salary_Summary)

        # Department-wise Gross and Deduction
        st.subheader("Department-wise Gross and Deduction")
        gross_deduction = payroll_data.groupby('Department_Name')[['Gross_Salary', 'Total_Deductions']].sum()
        st.table(gross_deduction)

        # Monthly Attendance
        st.subheader("Monthly Attendance")
        monthly_attendance = attendance_data['Status'].value_counts()
        st.table(monthly_attendance)

        # Comparison between two months (For demonstration, we'll use hardcoded months)
        st.subheader("Comparison between Two Months")
        month1 = ""
        month2 = ""

        conn = sqlite3.connect('data_analysis.db')
        month1_data = pd.read_sql(f"SELECT * FROM payroll WHERE Month_Val = '{month1}'", conn)
        month2_data = pd.read_sql(f"SELECT * FROM payroll WHERE Month_Val = '{month2}'", conn)
        conn.close()

        comparison = month1_data[['EmpID', 'Gross_Salary']].merge(month2_data[['EmpID', 'Gross_Salary']], on='EmpID', suffixes=('_May', '_Jun'))
        st.table(comparison)

