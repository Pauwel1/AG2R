import streamlit as st
from st_aggrid import AgGrid

from utils.activate_single_input import iterateInvestments, singleInvestment


st.set_page_config(page_title='Performance checker')
st.title('Stock performance checker 📈')
st.subheader('Feed me your Excel file')

uploaded_file = st.file_uploader('Choose an XLSX file', type='xlsx')
if uploaded_file:
    df = iterateInvestments(uploaded_file)
    AgGrid(df, height = 500, fit_columns_on_grid_load = True)

upload_ISIN = st.text_input("Insert ISIN")
if upload_ISIN:
    df = singleInvestment(upload_ISIN)
    AgGrid(df, height = 75, fit_columns_on_grid_load = True)