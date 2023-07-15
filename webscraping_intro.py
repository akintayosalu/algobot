# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests 
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/quote/AAPL/financials?p=AAPL"
headers = {"User-Agent": "Chrome/114.0.5735.198"} #work around for 404 error 
page = requests.get(url, headers=headers) #essentially grabs webpage

page_content = page.content
soup = BeautifulSoup(page_content, "html.parser") #parse page
#find content in div
tabl = soup.find_all("div",{"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})

income_statement = dict()

for t in tabl:
    rows = t.find_all("div",{"class":"D(tbr) fi-row Bgc($hoverBgColor):h"})
    for row in rows:
        #stores the first year info
        income_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1]
        print(row.get_text(separator="|")) #grabs the text 
