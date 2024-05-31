import streamlit as st
from threshold import ter_thresholds

ter_thresholds = ter_thresholds

def calculate_ter(marriage_status, dependencies):
    if not marriage_status:
        if dependencies <= 1:
            return "A"
        elif dependencies <= 3:
            return "B"
    else:
        if dependencies == 0:
            return "A"
        elif dependencies <= 2:
            return "B"
        elif dependencies == 3:
            return "C"
    return "C"

def calculate_gross_salary(monthly_salary):
    bonus = (monthly_salary * 0.24 / 100) + (monthly_salary * 0.3 / 100)
    additional = monthly_salary * 4 / 100 if monthly_salary <= 10000000 else 480000
    return monthly_salary + bonus + additional

def find_tax_rate(gross_salary, classification):
    for range in ter_thresholds[classification]:
        if range["lower_threshold"] <= gross_salary <= range["upper_threshold"]:
            return range["tax_rate"]
    return 0

def calculate_salary_tax(gross_salary, tax_rate):
    return gross_salary * tax_rate

def calculate_nett_salary1(monthly_salary, salary_tax):
    bpjs_kes_deduction = monthly_salary * 0.01 if monthly_salary < 12000000 else 120000
    bpjs_tk_deduction = monthly_salary * 2 / 100
    conditional_deduction = monthly_salary * 1 / 100 if monthly_salary < 10042300 else 100423
    nett_salary = monthly_salary - bpjs_kes_deduction - bpjs_tk_deduction - conditional_deduction - salary_tax
    return nett_salary

def tax_calculator(monthly_salary, marriage_status, dependencies):
    ter = calculate_ter(marriage_status, dependencies)
    gross_salary = calculate_gross_salary(monthly_salary)
    tax_rate = find_tax_rate(gross_salary, ter)
    salary_tax = calculate_salary_tax(gross_salary, tax_rate)
    nett_salary = calculate_nett_salary1(monthly_salary, salary_tax)
    return {
        "TER": ter,
        "Gross Salary": f"IDR {gross_salary:,.0f}",
        "Tax Rate (%)": f"{tax_rate:.2%}",
        "Salary Tax": f"IDR {salary_tax:,.0f}",
        "Nett Salary": f"IDR {nett_salary:,.0f}"
    }

def nett_to_monthly_calculator(nett_salary, marriage_status, dependencies):
    monthly_salary = nett_salary
    while True:
        result = tax_calculator(monthly_salary, marriage_status, dependencies)
        calculated_nett_salary = float(result["Nett Salary"].replace("IDR ", "").replace(",", ""))
        if abs(calculated_nett_salary - nett_salary) < 1:
            break
        monthly_salary += 1

    return {
        "Nett Salary": f"IDR {nett_salary:,.0f}",
        "Monthly Salary": f"IDR {monthly_salary:,.0f}",
        "TER": result["TER"],
        "Gross Salary": result["Gross Salary"],
        "Tax Rate (%)": result["Tax Rate (%)"],
        "Salary Tax": result["Salary Tax"]
    }

def main():
    st.title("Salary Tax Calculator")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Calculate Monthly to Nett Salary")
        monthly_salary = st.number_input("Enter your monthly salary (IDR):", min_value=0, value=10000000)
        marriage_status = st.selectbox("Are you married?", [True, False])
        dependencies = st.number_input("Number of dependencies:", min_value=0, value=0)
        
        if st.button("Calculate Nett Salary", key="calc_nett"):
            result = tax_calculator(monthly_salary, marriage_status, dependencies)
            st.write("Results:")
            for key, value in result.items():
                st.write(f"{key}: {value}")

    with col2:
        st.header("Calculate Nett to Monthly Salary")
        nett_salary = st.number_input("Enter your nett salary (IDR):", min_value=0, value=10000000, key="nett_salary")
        marriage_status_nett = st.selectbox("Are you married?", [True, False], key="marriage_status_nett")
        dependencies_nett = st.number_input("Number of dependencies:", min_value=0, value=0, key="dependencies_nett")
        
        if st.button("Calculate Monthly Salary", key="calc_monthly"):
            result = nett_to_monthly_calculator(nett_salary, marriage_status_nett, dependencies_nett)
            st.write("Results:")
            for key, value in result.items():
                st.write(f"{key}: {value}")

if __name__ == "__main__":
    main()

