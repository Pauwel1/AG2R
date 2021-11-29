import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import plotly.express as px

from utils.activate import iterateInvestments, singleInvestment
from utils.manipulate_df import style_df

st.set_page_config(page_title='Performance checker')
st.title('Stock performance checker 📈')
st.subheader('Feed me with your Excel file')

uploaded_file = st.file_uploader('Choose an XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = iterateInvestments(uploaded_file)

    # df = df.style.applymap(style_df, props='color:red;')
    
    AgGrid(df, height=500, fit_columns_on_grid_load=True)


    # groupby_column = st.selectbox(
    #     'What would you like to analyse?',
    #     ('price', 'difference1day (valuta)', 'difference1day (%)', 'range (1 year)'),
    # )

    # # -- GROUP DATAFRAME
    # output_columns = ['ISIN', 'Dénomination', "price", 'difference1day (valuta)', 'difference1day (%)', 'range (1 year)']
    # df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    # # -- PLOT DATAFRAME
    # fig = px.bar(
    #     df_grouped,
    #     x=groupby_column,
    #     y='ISIN',
    #     color='Dénomination',
    #     color_continuous_scale=['red', 'yellow', 'green'],
    #     template='plotly_white',
    #     title=f'<b>Sales & Profit by {groupby_column}</b>'
    # )
    # st.plotly_chart(fig)


upload_ISIN = st.text_input("Insert ISIN number")
if upload_ISIN:
    df = singleInvestment(upload_ISIN)
    st.dataframe(df)