#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 19:08:13 2023

@author: akintayosalu
"""

import datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN","MSFT","FB","GOOG"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()
ohlcv_data = dict()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]

#filling NaN values
"""
cl_price.fillna(0)
cl_price.fillna({"FB":0,"GOOG":1})
bfill drags the none NaN value in the backwards direction
cl_price.fillna(method="bfill",axis=0) #default axis is 0 (across colums)
cl_price.fillna(method="bfill",axis=1)
#inplace=False by default (original dataFrame is only changed when inplace=True)
"""
cl_price.fillna(method="bfill",axis=0, inplace=True)

#dropping NaN values 
cl_price.dropna(axis=0) #would delete row with NaN
cl_price.dropna(axis=1)#would delete column with NaN
#cl_price.dropna(axis=0, how="any", inplace=True)