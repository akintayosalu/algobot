#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 23:21:55 2023

@author: akintayosalu
"""

import datetime as dt
import yfinance as yf 
import pandas as pd

#print(dt.datetime.today())

stocks = ["AMZN","MSFT","INTC","GOOG", "INFY.NS","3988.HK"]
start = dt.datetime.today()-dt.timedelta(360)
end = dt.date.today()
cl_price = pd.DataFrame() #empty dataframe which will be filled with closing prices
ohlcv_data = dict() #ticker -> dataframe

#Looping over tickers and create a dataframe from close prices
for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start,end)["Adj Close"]
    #Adj Close is a column
    
for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker, start,end)
    
#print(ohlcv_data["MSFT"]["Open"])