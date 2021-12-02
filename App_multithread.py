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

    priceNow = []
    inValuta = []
    inPercent = []
    afterYear = []

    df = pd.read_excel(uploadedFile)
    urls = getUrls(df)
    price, varVal, varPerc, yearRange = setupThreads(urls)
    
    priceNow.append(price)
    inValuta.append(varVal)
    inPercent.append(varPerc)
    afterYear.append(yearRange)

    df["price"] = priceNow
    df["difference1day (valuta)"] = inValuta
    df["difference1day (%)"] = inPercent
    df["range (valuta; 1 year)"] = afterYear
    df.set_index("ISIN", inplace = False)

    t2 = time.perf_counter()
    print("Process time = ", t2-t1)

    AgGrid(df, height = 75, fit_columns_on_grid_load = True)