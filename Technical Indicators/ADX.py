#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 00:54:30 2023

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

def ADX(data, n=20):
    df = data.copy()
    df["ATR"] = ATR(df,n)
    df["UpMove"] = df["High"] - df["High"].shift(1)
    df["DownMove"] = df["Low"].shift(1) -  df["Low"]
    df["+DM"] = np.where((df["UpMove"] > df["DownMove"]) & (df["UpMove"]>0),df["UpMove"],0)
    df["-DM"] = np.where((df["DownMove"] > df["UpMove"]) & (df["DownMove"]>0),df["DownMove"],0)
    #use span because multiplier for EMA is same as span
    df["+DI"] = 100 * (df["+DM"]/df["ATR"]).ewm(span=n, min_periods=n).mean()
    df["-DI"] = 100 * (df["-DM"]/df["ATR"]).ewm(span=n, min_periods=n).mean()
    #change from span->com
    df["ADX"] = 100*abs((df["+DI"]-df["-DI"])/(df["+DI"]+df["-DI"])).ewm(com=n, min_periods=n).mean()
    return df["ADX"]

for ticker in ohlcv_data:
    ohlcv_data[ticker]["ADX"] = ADX(ohlcv_data[ticker],20)