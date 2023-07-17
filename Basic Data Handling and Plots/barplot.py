#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 21:28:30 2023

@author: akintayosalu
"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AMZN","MSFT","META","GOOG"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()

for ticker in stocks:
    cl_price[ticker] = yf.download(ticker, start, end)["Adj Close"]
    
#dropping nan values
cl_price.dropna(axis=0, how="any", inplace=True)

daily_return = cl_price.pct_change() #creates dataframe with daily return for each stock

fig,ax = plt.subplots() 
#plt.style.available to view plot styles
plt.style.use("ggplot")
ax.set(title="Mean Daily Return of Stocks",xlabel="Stocks",ylabel="Mean Return")
plt.bar(x=daily_return.columns, height=daily_return.mean())
plt.bar(x=daily_return.columns, height=daily_return.std(),color=["red","blue","orange","green"])