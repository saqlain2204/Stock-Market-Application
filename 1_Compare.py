import streamlit as st
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import plotly.express as px


st.title(":blue[Enter the Ticker Symbols to compare Stocks]")

def sidebar_info():
    with st.sidebar:
        choice = st.sidebar.selectbox("Select your choice",("Enter Period","Enter Date"))

        ## If the selected format is date, then period is intitalised to None
        if choice is "Enter Date":                                              
            start_date = str(st.sidebar.date_input("Enter the Start Date"))
            end_date = str(st.sidebar.date_input("Enter the End Date"))

            ## If startdate and enddate are same it throws an error
            if start_date==end_date:
                st.sidebar.error("Start Date and End Date cannot be same. Please try again")
            period=None

        ## If selected format is not date, startdate and enddate are initialised to None
        else:
            period = st.sidebar.selectbox("Select the period format",('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'))
            start_date=None
            end_date=None

        ## Interval is selected by the user from the list of options.
        interval = st.sidebar.selectbox("Select the interval",('1m', '2m' , '5m' , '15m' , '30m' , '60m' , '90m', '1h' , '1d', '5d', '1wk', '1mo', '3mo',))
        tickers=pd.read_csv('tickers.csv')['Symbol']
        tickers = st.multiselect("Enter the stocks you would like to compare",tickers)

        parameter = st.selectbox("Enter the Parameter for cmparision",['Open','Close','Volume','Adj Close','High','Low'])

    return start_date, end_date, tuple(tickers), parameter, interval, period

def refresh(tickers, start_date, end_date, parameter, interval, period, dataframe):
    dataframe = yf.download(tickers, start_date, end_date, interval, period)[parameter]

    return dataframe


def display(start_date, end_date, tickers, parameter, interval, period):
    try:
        dataframe = yf.download(tickers, start=start_date, end=end_date, interval=interval, period=period)[parameter]
        st.dataframe(dataframe.iloc[::-1])

        st.title(f"The comparision of {parameter} is as follows")
         
        if st.button("Refresh"):
            refresh(tickers, start_date, end_date, parameter, interval, period, dataframe)
    
    
    
    except:
        st.warning("Enter valid ticker symbols to continue")

if __name__=="__main__":
     start_date, end_date, tickers, parameter, interval, period = sidebar_info()
     display(start_date, end_date, tickers, parameter, interval, period)
     