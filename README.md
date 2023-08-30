# algobot
Algorithmic Trading Bot (Work in Progress)
# Description 
Algobot is an algorithmic trading bot that automates the process of buying and selling foreign exchange trades. Specifically, Algobot translates financial data (open, close, high, & low prices and trade volume) into technical indicators that produce "buy" and "sell" signals, which then lead to Algobot making API calls that create real short and long trades on the Oanda online forex broker.
# Deployment
- For deployment, the user needs to create a demo/paid account on Oanda (refer to miscellaneous/oanda_resources.txt) and generate API access code
- Need to download pandas, numpy, time libraries, Statsmodels API and OANDA Python wrapper (refer to miscellaneous/oanda_resources.txt)
- Run algobot.py to make use of the bot
# Getting Data
Scripts in this folder describe how to obtain price data from resources such as YahooFinancials, yfinance and Alpha Vantage APIs
# Web Scraping
These scripts provide an alternative way of extracting financial data by utilizing the web scraping library of Beautiful Soup
# Basic Data Handling and Plots
This file's programs demonstrate how to handle NaN values in retrieved data as well as visaulization of informaiton into line plots
# Technical Indicators 
Scripts in this file describe how to code financial technical indicators such as MACD, ATR, Bollinger Bands, RSI, ADX and Renko using the Pandas library
# Performance Measurement - KPIs
Scripts that detail how to calculate performance indicators such as CAGR, Volatility, Sharpe & Sortino ratios, Maximum Drawdown and Calmar Ratio for trading strategies 
# Backtesting Strategies
Code for testing trading strategies on historical data and calculating the returns and performance measurements 

