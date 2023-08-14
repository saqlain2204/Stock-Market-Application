import streamlit as st
import yfinance as yf
import plotly.express as px
from PIL import Image
import streamlit_authenticator as stauth
import os
from dotenv import load_dotenv

 
#--USER AUTHENTICATION
def user_auth():
    load_dotenv('.env')
    names = os.getenv('names').split(",")
    usernames = os.getenv('usernames').split(",")
    passwords = os.getenv('passwords').split(",")

    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator=stauth.Authenticate(names, usernames, hashed_passwords, "finance_dashboard","1234a",cookie_expiry_days=0)
    name, authentication_status, username = authenticator.login('Login','sidebar')


    return authentication_status, name, authenticator



hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


### Sidebar:

def sidebar_access():
    with st.sidebar:
        image = Image.open('logo.png')
        st.image(image)

        ## User eneters the ticker Symbol
        company = st.sidebar.text_input("Enter the ticker (eg: msft for Microsoft, reliance.ns for Reliance NSE)")

        stock=yf.Ticker(company)

        ## User gets the choice of selecting the input format of data
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

        return company, start_date, end_date, interval, period, stock

## Main Screen

## Image in main Screen
### Using Columns to align image in the centre
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('logo.png')

st.markdown("<h1 style='text-align: center; color: #7fc3f7;'>Welcome to FinTrack</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'>This application is currently in its Beta version.</p>", unsafe_allow_html=True)

## Main page function
def main_page(company, start_date, end_date, interval, period, stock):

    try:
        ticker = yf.download(company, start=start_date, end=end_date,  interval=interval, period=period)  

        ## Columns:
        High_col, low_col, button_col = st.columns(3, gap="medium")

        ## A column which contains the highest price of the stock in the given period
        with High_col:
            High=ticker["High"].max()
            High_time = ticker["High"].idxmax()
            st.title(f"Highest")
            st.markdown(f"##### :green[{High}] \n :green[Time: {High_time}]")

        ## A columns which contains the lowest price of the stock in the given period
        with low_col:
            Low=ticker["Low"].min()
            Low_time = ticker["High"].idxmin()                                                       
            st.title(f"Lowest")
            st.markdown(f"##### :red[{Low}] \n :red[Time: {Low_time}]")

        ## Refresh Button
        with button_col:
            st.markdown(" \n")
            refresh=st.button("Refresh")
        if(refresh):
            ticker = yf.download(company, start=start_date, end=end_date,  interval=interval, period=period)

        ## Displaying DataFrame
        st.dataframe(ticker.iloc[::-1], use_container_width=True)

        graph, share_holders , balance_sheet, news = st.tabs(["Statistics","Share Holders", "Balance sheet","News"])

        with graph:
            ## Graphs:
            var= st.selectbox("Select the dependent variable",("Open","High","Low","Adj Close","Volume"))
            st.plotly_chart(px.line(data_frame=ticker, y=ticker[var]), use_container_width=True)

        with share_holders:
           stock.major_holders['Percentage share']=stock.major_holders[0]
           del stock.major_holders[0]
           stock.major_holders['Description']=stock.major_holders[1]
           del stock.major_holders[1]
           stock.major_holders


        with balance_sheet:
            ## Balance Sheet
            st.dataframe(stock.balance_sheet, use_container_width=True)

        with news:
            for i in range(5):
                new=stock.news[i]['title']
                link=stock.news[i]['link']
                st.write(f"{new}: \n {link}")

    except:
        ## Throws warning if any error pops up
        st.warning("Enter a valid ticker name in the sidebar to generate Data")     

def main():
    ans, name, authenticator=user_auth()

    if ans==True:
        authenticator.logout('Log Out','sidebar')
        st.sidebar.title(f"Welcome :blue[{name.upper()}]😀")
        ## Accessing all the variables in the sidebar
        company, start_date, end_date, interval, period, stock = sidebar_access() 

        ## Calling the main page function to display the dataframe and the graphs
        main_page(company, start_date, end_date, interval, period, stock)          
    elif ans==None:
        st.sidebar.warning("Enter Username/password")

    else:
        st.sidebar.error("Username/password is incorrect")

if __name__=="__main__":
    main()