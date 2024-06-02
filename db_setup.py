import sqlite3

def init_db():
    conn = sqlite3.connect('data_analysis.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS payroll (
        Month_Val TEXT,
        EmpID TEXT,
        Name TEXT,
        Total_Days INTEGER,
        Present_Days INTEGER,
        Basic_Salary REAL,
        HRA REAL,
        Conveyance_Allowance REAL,
        Medical_Reimbursement REAL,
        Special_Allowance REAL,
        LTA REAL,
        Petrol_Allowance REAL,
        Driver_Allowance REAL,
        Super_Annuation REAL,
        Sodexo_Meal_Voucher REAL,
        Telephone_Allowance REAL,
        Business_Attire_Allowance REAL,
        Bonus REAL,
        Relocation_Bonus REAL,
        Gratuity REAL,
        Sodexo_Gift_Voucher REAL,
        Gross_Salary REAL,
        Mobile_Phone_Deduction REAL,
        TDS REAL,
        Profession_Tax REAL,
        Provident_Fund REAL,
        Total_Deductions REAL,
        Net_Pay REAL,
        Gender TEXT,
        Branch_Name TEXT,
        Department_Name TEXT
    )
    ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        Month_Val TEXT,
        EmpID TEXT,
        Date TEXT,
        Status TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

init_db()
