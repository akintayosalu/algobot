#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 01:06:44 2023

@author: akintayosalu
"""
import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = dict()

for ticker in tickers:
    temp = yf.download(ticker, period="7mo", interval="1d")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    
def volatility(data):
    df = data.copy()
    df["return"] = df["Adj Close"].pct_change()
    vol = df["return"].std() * np.sqrt(252) #daily annualization
    return vol

for ticker in ohlcv_data:
    print("Volatility of {} = {}".format(ticker, volatility(ohlcv_data[ticker])))