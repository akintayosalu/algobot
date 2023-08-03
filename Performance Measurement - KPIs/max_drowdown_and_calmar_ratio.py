#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 01:51:00 2023

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
    
def maximum_drawdown(data):
    df = data.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["cum_return"] = (1+df["return"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    drawdown = (df["drawdown"]/df["cum_roll_max"]).max()
    return drawdown

def calmar(data):
    return CAGR(data)/maximum_drawdown(data)

for ticker in ohlcv_data:
    print("Maximum drawdown of {} = {}".format(ticker, maximum_drawdown(ohlcv_data[ticker])))
    print("Calamar ratio of {} = {}".format(ticker, calmar(ohlcv_data[ticker])))