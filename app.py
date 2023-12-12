import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image


D_target = pd.read_csv("./datasets/D_target.csv")
D_clients = pd.read_csv("./datasets/D_clients.csv")
D_close_loan = pd.read_csv("./datasets/D_close_loan.csv")
D_job = pd.read_csv("./datasets/D_job.csv")
D_last_credit = pd.read_csv("./datasets/D_last_credit.csv")
D_loan = pd.read_csv("./datasets/D_loan.csv")
D_pens = pd.read_csv("./datasets/D_pens.csv")
D_salary = pd.read_csv("./datasets/D_salary.csv")
D_work = pd.read_csv("./datasets/D_work.csv")

age_target = Image.open("./datasets/age_target.png")
corr = Image.open("./datasets/corr.png")
gender_age = Image.open("./datasets/gender_age.png")
pairplot = Image.open("./datasets/pairplot.png")
pens_target = Image.open("./datasets/pens_target.png")
personal_income = Image.open("./datasets/personal_income.png")


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
perc_95 = np.nanpercentile(merged_data["PERSONAL_INCOME"], 95)
merged_data["PERSONAL_INCOME"] = np.where(merged_data["PERSONAL_INCOME"] > perc_95, np.NaN,merged_data["PERSONAL_INCOME"])
merged_data["GENDER"].replace(0, "Female", inplace=True)
merged_data["GENDER"].replace(1, "Male", inplace=True)
merged_data["SOCSTATUS_PENS_FL"].replace(0, "not_pens", inplace=True)
merged_data["SOCSTATUS_PENS_FL"].replace(1, "pens", inplace=True)
merged_data["SOCSTATUS_WORK_FL"].replace(0, "not_work", inplace=True)
merged_data["SOCSTATUS_WORK_FL"].replace(1, "work", inplace=True)
df_num = merged_data[["AGE","CHILD_TOTAL", "DEPENDANTS", "PERSONAL_INCOME", "LOAN_NUM_TOTAL", "LOAN_NUM_CLOSED"]]
stat = df_num.describe()

st.title("Streamlit app for EDA of Bank's clients")
st.divider()

st.write('**Распределение по полу и возрасту**')
st.image(gender_age)
st.divider()

st.write('**Распределение дохода**')
st.image(personal_income)
st.divider()

st.write('**Матрица корреляций**')
st.image(corr)
st.divider()

st.write('**Распределение признаков между собой**')
st.image(pairplot)
st.divider()

st.write('**Распределение возраста к таргету**')
st.image(age_target)
st.divider()

st.write('**Распределение флага пенсионера к таргету**')
st.image(gender_age)
st.divider()

st.write('**Таблица с данными**')
st.write(merged_data)