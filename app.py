import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from pandas_datareader import data as pdr
from datetime import date
import plotly.express as px


### Sidebar:
with st.sidebar:
    def sidebar_access():
        ## User eneters the ticker Symbol
        company = st.sidebar.text_input("Enter the ticker (eg: msft for Microsoft, reliance.ns for Reliance NSE)")

        stock=yf.Ticker(company)

        ## User gets the choice of selecting the input format of data
        choice = st.sidebar.selectbox("Select your choice",("Enter Period","Enter Date"))

        if choice is "Enter Date":                                              ## If the selected format is date, then period is intitalised to None
            start_date = str(st.sidebar.date_input("Enter the Start Date"))
            end_date = str(st.sidebar.date_input("Enter the End Date"))

            ## If startdate and enddate are same it throws an error
            if start_date==end_date:
                st.sidebar.error("Start Date and End Date cannot be same. Please try again")
            period=None

        else:                                                                   ## If selected format is not date, startdate and enddate are initialised to None
            period = st.sidebar.selectbox("Select the period format",('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'))
            start_date=None
            end_date=None

        ## Interval is selected by the user from the list of options.
        interval = st.sidebar.selectbox("Select the interval",('1m', '2m' , '5m' , '15m' , '30m' , '60m' , '90m', '1h' , '1d', '5d', '1wk', '1mo', '3mo',))

        return company, start_date, end_date, interval, period, stock
## Main Screen
st.markdown("# Welcome to our financial DashBoard.\n ###### This application is currently in its Beta version/testing period.")

## Main page function
def main_page(company, start_date, end_date, interval, period, stock):
    try:
        ticker = yf.download(company, start=start_date, end=end_date,  interval=interval, period=period)  

        ## Columns:
        High_col, low_col = st.columns(2, gap="medium")

        with High_col:                                                      ## A column which contains the highest price of the stock in the given period
            st.title(f"Highest")
            High=ticker["High"].max()
            st.markdown(f"##### {High}")

        with low_col:                                                       ## A columns which contains the lowest price of the stock in the given period
            st.title(f"Lowest")
            Low=ticker["Low"].min()
            st.markdown(f"##### {Low}")

        ## Displaying DataFrame
        st.dataframe(ticker, use_container_width=True)

        graph, balance_sheet = st.tabs(["Statistics", "Balance sheet"])

        with graph:
            ## Graphs:
            var= st.selectbox("Select the dependent variable",("Open","High","Low","Adj Close","Volume"))
            st.plotly_chart(px.line(data_frame=ticker, y=ticker[var]), use_container_width=True)

        with balance_sheet:
            ## Balance Sheet
            st.dataframe(stock.balance_sheet, use_container_width=True)
 
    except:
        st.warning("Enter a valid ticker name in the sidebar to generate Data")     ## Throws warning if any error pops up

def main():

    company, start_date, end_date, interval, period, stock = sidebar_access()  ## Accessing all the variables in the sidebar
    main_page(company, start_date, end_date, interval, period, stock)          ## Calling the main page function to display the dataframe and the graphs
    ## Objects:
    
    

if __name__=="__main__":
    main()