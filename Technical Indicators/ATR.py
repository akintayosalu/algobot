#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 02:24:16 2023

@author: akintayosalu
"""

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = dict()

for ticker in tickers:
    temp = yf.download(ticker,period="1mo", interval="5m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    
def ATR(data, n=14):
    df = data.copy()
    df["High-Low"] = df["High"] - df["Low"]
    #shift(1) means that calculation is for previous close 
    df["High-Previous Close"] = df["High"] - df["Adj Close"].shift(1)
    df["Low-Previous Close"] = df["Low"] - df["Adj Close"].shift(1)
    #axis=1 ensures max is across rows instead of columns
    #skipna=False means presence of nan means the max cannott be found
    df["True Range"] = df[["High-Low","High-Previous Close","Low-Previous Close"]].max(axis=1,skipna=False)
    #might use com instead of span
    df["ATR"] = df["True Range"].ewm(span=n, min_periods=n).mean()
    return df["ATR"]

for ticker in ohlcv_data:
    ohlcv_data[ticker]["ATR"] = ATR(ohlcv_data[ticker])