#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 20:38:26 2023

@author: akintayosalu
"""

import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN","MSFT","META","GOOG"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]
    
#dropping nan values
cl_price.dropna(axis=0, how="any", inplace=True)

daily_return = cl_price.pct_change() #creates dataframe with daily return for each stock

cl_price.plot(subplots=True, title="Stock Price Evolution", grid=True) #layour argument does not seem to work 
#subplots creates different plots for each column
daily_return.plot(subplots=True, title="Stock Price Evolution", grid=True)
(1+daily_return).cumprod().plot() #cumulative product