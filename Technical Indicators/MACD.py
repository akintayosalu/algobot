#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 02:23:19 2023

@author: akintayosalu
"""

import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = dict()

for ticker in tickers:
    temp = yf.download(ticker,period="1mo", interval="15m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[ticker] = temp
    


    
    
#default values
def MACD(data, fast=12,slow=26,signal=9):
    df = data.copy()
    df["macd_fast"] = data["Adj Close"].ewm(span=fast, min_periods=fast).mean()
    df["macd_slow"] = data["Adj Close"].ewm(span=slow, min_periods=slow).mean()
    df["macd"] = df["macd_fast"] - df["macd_slow"]
    df["signal"] = df["macd"].ewm(span=signal, min_periods=signal).mean()
    return df.loc[:,["macd", "signal"]]  #returns columns with macd and signal info

for ticker in ohlcv_data:
    ohlcv_data[ticker][["MACD","SIGNAL"]] = MACD(ohlcv_data[ticker])