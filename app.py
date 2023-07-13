import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from pandas_datareader import data as pdr
from datetime import date
import plotly.express as px


st.markdown("# Welcome to our financial DashBoard.\n ###### This application is currently in its Beta version/testing period.")

with st.sidebar:
    company = st.sidebar.text_input("Enter the ticker (eg: msft for Microsoft, reliance.ns for Reliance NSE)")

    choice = st.sidebar.selectbox("Select your choice",("Enter Period","Enter Date"))

    if choice is "Enter Date":
        start_date = str(st.sidebar.date_input("Enter the Start Date"))
        end_date = str(st.sidebar.date_input("Enter the End Date"))
        if start_date==end_date:
            st.error("Start Date and End Date cannot be same. Please try again")
        period=None

    else:
        period = st.sidebar.selectbox("Select the period format",('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'))
        start_date=None
        end_date=None

    interval = st.sidebar.selectbox("Select the interval",('1m', '2m' , '5m' , '15m' , '30m' , '60m' , '90m', '1h' , '1d', '5d', '1wk', '1mo', '3mo',))

try:
    ticker = yf.download(company, start=start_date, end=end_date,  interval=interval, period=period)
    
    High_col, low_col = st.columns(2, gap="medium")

    with High_col:
        st.title(f"Highest in Period: {period}")
        High=ticker["High"].max()
        st.markdown(f"##### {High}")

    with low_col:
        st.title(f"lowest in Period: {period}")
        Low=ticker["Low"].min()
        st.markdown(f"##### {Low}")



    st.dataframe(ticker, use_container_width=True)

    var= st.selectbox("Select the dependent variable",("Open","High","Low","Adj Close","Volume"))
    st.plotly_chart(px.line(data_frame=ticker, y=ticker[var]), use_container_width=True)

except:
    st.warning("Enter a valid ticker name")


