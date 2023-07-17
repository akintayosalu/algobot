#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 20:04:08 2023

@author: akintayosalu
"""

import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN","MSFT","META","GOOG"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohlcv_data = dict()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]
    
#dropping nan values
cl_price.dropna(axis=0, how="any", inplace=True)

daily_return = cl_price.pct_change() #creates dataframe with daily return for each stock
daily_return.mean(axis=1) #prints mean between all daily returns for stocks for each day
daily_return.std() #prints standard deviation of each stock 

df = daily_return.rolling(window=10).mean() #check documentation for other arguments
daily_return.rolling(window=10).std()
df = daily_return.rolling(window=10).max()
daily_return.rolling(window=10).sum()

df2 = daily_return.ewm(com=10, min_periods=10).mean() #exponential rolling average to take into account the most recent data
#need to specify min_periods for ewm as default is 0