#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 00:40:10 2023

@author: akintayosalu
"""

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = dict()

for ticker in tickers:
    temp = yf.download(ticker, period="7mo", interval="1d")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
   
def CAGR(data):
    df = data.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cumulative_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252 #252 is number of trading days in a year (removing weekends and holidays)
    CAGR = df["cumulative_return"][-1]**(1/n) - 1
    return CAGR

for ticker in ohlcv_data:
    print("CAGR for {} = {}".format(ticker, CAGR(ohlcv_data[ticker])))