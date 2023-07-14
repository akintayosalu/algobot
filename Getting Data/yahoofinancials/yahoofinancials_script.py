#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 00:29:19 2023

@author: akintayosalu
"""
import pandas as pd
from yahoofinancials import YahooFinancials 
import datetime as dt 

all_tickers = ["AAPL", "MSFT","CSCO","AMZN","INTC"]
ticker = "MSFT"

#Extracting stock data (historical close price) for stocks identified
close_prices = pd.DataFrame()
end_date = (dt.date.today()).strftime('%Y-%m-%d') #converts daytime object to string date
beg_date = ((dt.date.today())-dt.timedelta(1825)).strftime('%Y-%m-%d')
for ticker in all_tickers:
    yahoo_financials = YahooFinancials(ticker)
    json_obj = yahoo_financials.get_historical_price_data(beg_date, end_date, "daily")
    ohlv = json_obj[ticker]['prices'] #list of dictionaries 
    temp = pd.DataFrame(ohlv)[["formatted_date","adjclose"]]
    temp.set_index("formatted_date", inplace=True) #makes the date the index of data
    temp.dropna(inplace=True) #removes nan
    close_prices[ticker] = temp["adjclose"]