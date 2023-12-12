# импорт библиотек
import streamlit as st
import pandas as pd
import plotly_express as px

import streamlit as st

import pandas as pd

# Загрузка данных
D_target = pd.read_csv("./datasets/D_target.csv")
D_clients = pd.read_csv("./datasets/D_clients.csv")
D_close_loan = pd.read_csv("./datasets/D_close_loan.csv")
D_job = pd.read_csv("./datasets/D_job.csv")
D_last_credit = pd.read_csv("./datasets/D_last_credit.csv")
D_loan = pd.read_csv("./datasets/D_loan.csv")
D_pens = pd.read_csv("./datasets/D_pens.csv")
D_salary = pd.read_csv("./datasets/D_salary.csv")
D_work = pd.read_csv("./datasets/D_work.csv")


merged_data = pd.merge(D_clients, D_target, left_on="ID", right_on="ID_CLIENT", how="left")

merged_data = pd.merge(merged_data, D_salary, left_on="ID", right_on="ID_CLIENT", how="left")
merged_data = merged_data.drop_duplicates()
D_loan["ID_LOAN"] = D_loan["ID_LOAN"].astype(str)
D_close_loan["ID_LOAN"] = D_close_loan["ID_LOAN"].astype(str)
loans_data = pd.merge(D_clients, D_loan, left_on="ID", right_on="ID_CLIENT", how="left")
loans_data = pd.merge(loans_data, D_close_loan, left_on="ID_LOAN", right_on="ID_LOAN", how="left")
loans_data = loans_data.groupby(["ID"]).agg({"ID_LOAN": "count", "CLOSED_FL": "sum"}).reset_index()
loans_data = loans_data.rename(columns={"ID_LOAN": "LOAN_NUM_TOTAL", "CLOSED_FL": "LOAN_NUM_CLOSED"})
merged_data = pd.merge(merged_data, loans_data, right_on="ID", left_on="ID", how="left")
merged_data = merged_data[["AGREEMENT_RK", "TARGET", "AGE", "SOCSTATUS_WORK_FL", "SOCSTATUS_PENS_FL",
    "GENDER", "CHILD_TOTAL", "DEPENDANTS", "PERSONAL_INCOME",
    "LOAN_NUM_TOTAL", "LOAN_NUM_CLOSED"]]

st.title("Streamlit app for EDA of Bank's clients")

st.write(merged_data)