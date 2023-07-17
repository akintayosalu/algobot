#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 19:49:38 2023

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
    
cl_price.dropna(axis=0, how="any", inplace=True)


cl_price.mean()
cl_price.std() #standaard deviation
cl_price.median()
cl_price.describe()

cl_price.head(8)#see first 8 rows
cl_price.tail()#find bottom rows

daily_return = cl_price.pct_change()
# cl_price.pct_change() == cl_price/cl_price.shift(1) - 1 #shift moves data down by n rows, negative number moves rows up
daily_return.mean()
daily_return.std()

