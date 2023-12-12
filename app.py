# импорт библиотек
import streamlit as st
import pandas as pd
import plotly_express as px

PATH = "https://www.dropbox.com/scl/fi/226nfwteim6x2x7q0c36a/football.csv?dl=1&rlkey=cd2t0odbqr8g0yxnnul51mykb"

df = st.cache_data(pd.read_csv)(PATH)

clubs = st.sidebar.multiselect('Выберите клуб', df['Club'].unique())
nationalities = st.sidebar.multiselect('Укажите национальность игроков', df['Nationality'].unique())

new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]
st.write(new_df)

# строим графики используя plotly express
fig = px.scatter(new_df, x='Overall', y='Age', color='Name')

# рисуем!
st.plotly_chart(fig)