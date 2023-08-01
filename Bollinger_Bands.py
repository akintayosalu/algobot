#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 02:57:33 2023

@author: akintayosalu
"""

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = dict()

for ticker in tickers:
    temp = yf.download(ticker,period="1mo", interval="5m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    
def bollinger_bands(data, n=14):
    df = data.copy()
    df["Middle Band"] = df["Adj Close"].rolling(n).mean()
    df["Upper Band"] = df["Middle Band"] + 2*df["Adj Close"].rolling(n).std(ddof=0)
    df["Lower Band"] = df["Middle Band"] - 2*df["Adj Close"].rolling(n).std(ddof=0)
    df["Band Width"] = df["Upper Band"] - df["Lower Band"]
    return df[["Middle Band","Upper Band", "Lower Band", "Band Width"]]

for ticker in ohlcv_data:
    ohlcv_data[ticker][["MB","UB", "LB", "Width"]] = bollinger_bands(ohlcv_data[ticker], 20)