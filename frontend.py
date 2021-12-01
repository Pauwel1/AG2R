import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import plotly.express as px

from utils.activate import iterateInvestments, singleInvestment
from utils.manipulate_df import style_df

st.set_page_config(page_title='Performance checker')
st.title('Stock performance checker 📈')
st.subheader('Feed me your Excel file')

uploaded_file = st.file_uploader('Choose an XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = iterateInvestments(uploaded_file)
    
    AgGrid(df, height = 500, fit_columns_on_grid_load = True)

upload_ISIN = st.text_input("Insert ISIN")
if upload_ISIN:
    df = singleInvestment(upload_ISIN)
    AgGrid(df, height = 75, fit_columns_on_grid_load = True)