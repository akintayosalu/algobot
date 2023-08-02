#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 01:37:57 2023

@author: akintayosalu
"""
import yfinance as yf
import numpy as np
from stocktrends import Renko

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = dict()
hour_data = dict()
renko_data = dict()

for ticker in tickers:
    temp = yf.download(ticker,period="1mo", interval="5m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    
    temp = yf.download(ticker,period="1y", interval="1h")
    temp.dropna(how="any", inplace=True)
    hour_data[ticker] = temp
    
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

def renko_df(data, hourly_data):
    df = data.copy()
    df.drop("Close",axis=1, inplace=True) #axis=1 to delete column
    df.reset_index(inplace=True) #turns index into regular column
    df.columns = ["date","open","high","low","close","volume"]
    df2 = Renko(df)
    df2.brick_size = round(ATR(hourly_data, 120).iloc[-1],0) * 3 #gives last number in series
    renko_df = df2.get_ohlc_data()
    return renko_df
    
for ticker in ohlcv_data:
    renko_data[ticker] = renko_df(ohlcv_data[ticker],hour_data[ticker])
    
    