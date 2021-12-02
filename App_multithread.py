import streamlit as st
import time
from st_aggrid import AgGrid
import pandas as pd

from utils.activate_multithread import getUrls, setupThreads


st.set_page_config(page_title='Performance checker')
st.title('Stock performance checker 📈')
st.subheader('Feed me your Excel file')

uploadedFile = st.file_uploader('Choose an XLSX file', type='xlsx')
if uploadedFile:
    t1 = time.perf_counter()

    df = pd.read_excel(uploadedFile)
    urls = getUrls(df)
    price, varVal, varPerc, yearRange = setupThreads(urls)

    df["price"] = price
    df["difference1day (valuta)"] = varVal
    df["difference1day (%)"] = varPerc
    df["range (valuta; 1 year)"] = yearRange
    df.set_index("ISIN", inplace = False)

    t2 = time.perf_counter()
    print("Process time = ", t2-t1)

    AgGrid(df, height = 75, fit_columns_on_grid_load = True)