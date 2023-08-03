#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 01:16:06 2023

@author: akintayosalu
"""
import yfinance as yf
import numpy as np
import pandas as pd

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

def CAGR(data):
    df = data.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cumulative_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252 #252 is number of trading days in a year (removing weekends and holidays)
    CAGR = df["cumulative_return"][-1]**(1/n) - 1
    return CAGR

def sharpe(data, riskFreeRate):
    df = data.copy()
    sharpe = (CAGR(df) - 0.04)/volatility(df) #risk free rate is about 4.08%
    return sharpe

def sortino(data,riskFreeRate):
    df = data.copy()
    df["return"] = df["Adj Close"].pct_change()
    negative_return = np.where(df["return"]>0,0,df["return"])
    #use pandas series so nan values are ignored in calculation
    #filter out zero values
    #sqrt(252) for daily annualization
    negative_volatility = pd.Series(negative_return[negative_return!=0]).std() * np.sqrt(252)
    return (CAGR(df) - riskFreeRate)/negative_volatility

for ticker in ohlcv_data:
    print("Sharpe for {} = {}".format(ticker, sharpe(ohlcv_data[ticker], 0.04)))
    print("Sortino for {} = {}".format(ticker, sortino(ohlcv_data[ticker], 0.04)))
    
    
    
    