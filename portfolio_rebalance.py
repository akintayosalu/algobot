#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 01:20:16 2023

@author: akintayosalu
"""
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

def CAGR(data):
    #Function to calculate the Cumulative Annual Growth
    #Rate of a trading strategy
    df = data.copy()
    df["cumulative_return"] = (1 + df["monthly_return"]).cumprod()
    n = len(df)/12 #monthly annualization
    CAGR = df["cumulative_return"].tolist()[-1]**(1/n) - 1
    return CAGR

def volatility(data):
    #Function to calculate annualized volatility of trading strategy
    df = data.copy()
    vol = df["monthly_return"].std() * np.sqrt(12) #monthly annualization
    return vol

def sharpe(data, riskFreeRate):
    #Function to calculate sharpe ratio: rf is the risk free rate
    df = data.copy()
    sharpe = (CAGR(df) - 0.04)/volatility(df) #risk free rate is about 4.08%
    return sharpe

def maximum_drawdown(data):
    #Function to calculatee max drawdown
    df = data.copy()
    df["cum_return"] = (1+df["monthly_return"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    drawdown = (df["drawdown"]/df["cum_roll_max"]).max()
    return drawdown

# Download historical data (monthly) for DJI constituent stocks

tickers = ["MMM","AXP","T","BA","CAT","CSCO","KO", "XOM","GE","GS","HD",
           "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
           "UNH","VZ","V","WMT","DIS"]

ohlc_mon = {} # directory with ohlc value for each stock            
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()

# looping over tickers and creating a dataframe with close prices
for ticker in tickers:
    ohlc_mon[ticker] = yf.download(ticker,start,end,interval='1mo')
    ohlc_mon[ticker].dropna(inplace=True,how="all")
 
tickers = ohlc_mon.keys() # redefine tickers variable after removing any tickers with corrupted data

################################Backtesting####################################

# calculating monthly return for each stock and consolidating return info by stock in a separate dataframe
ohlc_dict = copy.deepcopy(ohlc_mon)
return_df = pd.DataFrame()
for ticker in tickers:
    #print("Calculating monthly return for ", ticker)
    ohlc_dict[ticker]["monthly_return"] = ohlc_dict[ticker]["Adj Close"].pct_change()
    return_df[ticker] = ohlc_dict[ticker]["monthly_return"]
return_df.dropna(inplace=True)

# function to calculate portfolio return iteratively
def pflio(data,m,x):
    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = data.copy()
    portfolio = [] #list of tickers i.e ["AMZN", "MSFT"....]
    monthly_return = [0]
    for i in range(len(df)):
        if len(portfolio) > 0:
            #iloc[i,:] translates to row i and all columns
            monthly_return.append(df[portfolio].iloc[i,:].mean())
            #monthly_return.append is just calculating the monthly average of all stocks
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            #bad stocks is grabbing the ticker names for worst stocks in a list
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        #new_picks essentially replaces bad performing stocks with good performing stocks (there can be
        #multiple of singular stock)
        #WITHOUT duplicates -> df[[t for t in tickers if t not in portfolio]]
        portfolio = portfolio + new_picks
        #print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_return), columns=["monthly_return"])
    return monthly_ret_df

#calculating overall strategy's KPIs
CAGR(pflio(return_df,6,3))
sharpe(pflio(return_df,6,3),0.025)
maximum_drawdown(pflio(return_df,6,3))
    
#calculating KPIs for Index buy and hold strategy over the same period
DJI = yf.download("^DJI",dt.date.today()-dt.timedelta(3650),dt.date.today(),interval='1mo')
DJI["monthly_return"] = DJI["Adj Close"].pct_change().fillna(0)
CAGR(DJI)
sharpe(DJI,0.025)
maximum_drawdown(DJI)

#visualization
fig, ax = plt.subplots()
plt.plot((1+pflio(return_df,6,3)).cumprod())
plt.plot((1+DJI["monthly_return"].reset_index(drop=True)).cumprod())
plt.title("Index Return vs Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return","Index Return"])    
     
        
        
        
        
        
        
        
        
        
        
        
        
        
        

