#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 02:52:34 2023

@author: akintayosalu
"""

import requests
from bs4 import BeautifulSoup

#Normal way to grab tables from webpage
#url = "https://www.xe.com/currencycharts/"
#tables = pd.read_html(url)
#HOW TO GET STATISTICS dfrom tables on webpage
key_statistics = dict()
tickers = ["AAPL","FB","CSCO","INFY.NS","3988.HK"]

for ticker in tickers:
        
    url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker,ticker)
    headers = {"User-Agent": "Chrome/114.0.5735.198"} #work around for 404 error 
    page = requests.get(url, headers=headers) #essentially grabs webpage
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser") #parse page
    
    
    
    #tabl = soup.find_all("table",{"class":"W(100%) Bdcl(c) "}) #might have to remove space (weird quirk)
    tabl = soup.find_all("table",{"class":"W(100%) Bdcl(c)"})
    temp_stats = dict()
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            #print(row.get_text())
            temp_stats[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[-1]
            #-1 index to avoid garbage
            
    key_statistics[ticker] = temp_stats