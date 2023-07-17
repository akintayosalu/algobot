# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests 
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AAPL","FB","CSCO","INFY.NS","3988.HK"]

income_statement_dict = dict()
balance_sheet_dict = dict()
cashflow_st_dict = dict()

for ticker in tickers:
    #scraping income statement 
    url = "https://finance.yahoo.com/quote/{}/financials?p={}".format(ticker,ticker)
    income_statement = dict()
    table_title = dict()
    headers = {"User-Agent": "Chrome/114.0.5735.198"} #work around for 404 error 
    page = requests.get(url, headers=headers) #essentially grabs webpage
    
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser") #parse page
    #find content in div
    tabl = soup.find_all("div",{"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    

    for t in tabl:
        heading = t.find_all("div",{"class":"D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
            
        rows = t.find_all("div",{"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            #stores the first year info
            income_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
            #print(row.get_text(separator="|")) #grabs the text 
    temp = pd.DataFrame(income_statement).T #transpose to get correct formatting
    temp.columns = table_title["Breakdown"] #set correct headings for data 
    income_statement_dict[ticker] = temp
    
    #scraping balance sheet statement 
    url = "https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(ticker,ticker)
    balance_sheet = dict()
    table_title = dict()
    headers = {"User-Agent": "Chrome/114.0.5735.198"} #work around for 404 error 
    page = requests.get(url, headers=headers) #essentially grabs webpage
    
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser") #parse page
    #find content in div
    tabl = soup.find_all("div",{"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    

    for t in tabl:
        heading = t.find_all("div",{"class":"D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
            
        rows = t.find_all("div",{"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            #stores the first year info
            balance_sheet[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
            #print(row.get_text(separator="|")) #grabs the text 
    temp = pd.DataFrame(balance_sheet).T #transpose to get correct formatting
    temp.columns = table_title["Breakdown"] #set correct headings for data 
    balance_sheet_dict[ticker] = temp
    
    #scraping cashflow statement 
    url = "https://finance.yahoo.com/quote/{}/cash-flow?p={}".format(ticker,ticker)
    cashflow_st = dict()
    table_title = dict()
    headers = {"User-Agent": "Chrome/114.0.5735.198"} #work around for 404 error 
    page = requests.get(url, headers=headers) #essentially grabs webpage
    
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser") #parse page
    #find content in div
    tabl = soup.find_all("div",{"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    

    for t in tabl:
        heading = t.find_all("div",{"class":"D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
            
        rows = t.find_all("div",{"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            #stores the first year info
            cashflow_st[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
            #print(row.get_text(separator="|")) #grabs the text 
    temp = pd.DataFrame(cashflow_st).T #transpose to get correct formatting
    temp.columns = table_title["Breakdown"] #set correct headings for data 
    cashflow_st_dict[ticker] = temp
   
#changes data from string -> int
for ticker in tickers:
    for col in income_statement_dict[ticker].columns:
        income_statement_dict[ticker][col] = income_statement_dict[ticker][col].str.replace(',|-','')
        income_statement_dict[ticker][col] = pd.to_numeric(income_statement_dict[ticker][col], errors="coerce")
        
for ticker in tickers:
    for col in balance_sheet_dict[ticker].columns:
        balance_sheet_dict[ticker][col] = balance_sheet_dict[ticker][col].str.replace(',|-','')
        balance_sheet_dict[ticker][col] = pd.to_numeric(balance_sheet_dict[ticker][col], errors="coerce")
        
for ticker in tickers:
    for col in cashflow_st_dict[ticker].columns:
        cashflow_st_dict[ticker][col] = cashflow_st_dict[ticker][col].str.replace(',|-','')
        cashflow_st_dict[ticker][col] = pd.to_numeric(cashflow_st_dict[ticker][col], errors="coerce")
    
    