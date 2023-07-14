#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 02:14:23 2023

@author: akintayosalu
"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time
key_path = "/Users/akintayosalu/Documents/algo/algobot/alphaVantageAPIKey.txt"

#Not usable -> NEED TO PAY FOR PREMIUM ACCESS TO API
#Extracting data for single ticker 
ts = TimeSeries(key=open(key_path,'r').read(), output_format='pandas')
data = ts.get_daily(symbol='MSFT', outputsize='full')[0]
data.columns = ["open","high","low","close","volume"]
#data might come in reverse order
data = data.iloc[::-1]

#Extracing stock data (historical close price) for the stocks identified
all_tickers = ["AAPL", "MSFT","CSCO","AMZN","FB"]
close_prices = pd.DataFrame()
api_call_count = 0 #for working with constraints for number of API calls
for ticker in all_tickers:
    start_time = time.time()
    ts = TimeSeries(key=open(key_path,'r').read(), output_format='pandas')
    data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')[0]
    api_call_count += 1
    data.columns = ["open","high","low","close","volume"]
    data = data.iloc[::-1]
    close_prices[ticker] = data["close"]
    if api_call_count == 5:
        api_call_count = 0
        time.sleep(60-(time.time()- start_time))