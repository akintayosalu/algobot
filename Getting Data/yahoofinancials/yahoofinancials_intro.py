#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 00:29:19 2023

@author: akintayosalu
"""
#alternative to yfinance
from yahoofinancials import YahooFinancials 

ticker = 'MSFT'
yahoo_financials = YahooFinancials(ticker)
data = yahoo_financials.get_historical_price_data("2018-04-24","2020-04-24","daily")
#Information is in the form of a JSON object