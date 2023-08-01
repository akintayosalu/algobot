#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 03:43:44 2023

@author: akintayosalu
"""

import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = dict()

for ticker in tickers:
    temp = yf.download(ticker,period="1mo", interval="5m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    
def RSI(data, n=14):
    df = data.copy()
    df["change"] = df["Adj Close"] -  df["Adj Close"].shift(1)
    #np.where is similar to if function in excel
    df["gain"] = np.where(df["change"] >= 0, df["change"],0)
    df["loss"] = np.where(df["change"] < 0, -1*df["change"],0)
    df["avgGain"] = df["gain"].ewm(alpha=1/n, min_periods=n).mean() #should be similar to RMAA
    df["avgLoss"] = df["loss"].ewm(alpha=1/n, min_periods=n).mean()
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["RSI"] = 100 - (100/(1+df["rs"]))
    return df["RSI"]

for ticker in ohlcv_data:
    ohlcv_data[ticker]["RSI"] = RSI(ohlcv_data[ticker])