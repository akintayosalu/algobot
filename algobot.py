#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 19:59:17 2023

@author: akintayosalu
"""

import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import pandas as pd
import time
import numpy as np
import statsmodels.api as sm

#initiating API connection and defining trade parameters
client = oandapyV20.API(access_token="05d7e64454a7504094fe680925845c5d-c78545469a1b3dcfd2e9cf332951c5f9",environment="practice")
account_id = "101-001-26553977-001"

#defining strategy parameters
pairs = ['EUR_USD','GBP_USD','USD_CHF','AUD_USD','USD_CAD','EUR_JPY','USD_JPY','AUD_JPY','AUD_USD','AUD_NZD','NZD_USD'] #currency pairs to be included in the strategy
pos_size = 2000 #max capital allocated/position size for any currency pair

#This helper function grabs the financial data (open, close, high, low, volume)
def candles(instrument):
    params = {"count": 800,"granularity": "M1"} #granularity can be in seconds S5 - S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
    candles = instruments.InstrumentsCandles(instrument=instrument,params=params)
    client.request(candles)
    ohlc_dict = candles.response["candles"]
    ohlc = pd.DataFrame(ohlc_dict)
    ohlc_df = ohlc.mid.dropna().apply(pd.Series)
    ohlc_df["volume"] = ohlc["volume"]
    ohlc_df.index = ohlc["time"]
    ohlc_df = ohlc_df.apply(pd.to_numeric)
    return ohlc_df

#This function calculates the slope of the MACD & Signal lines
def slope(ser,n):
    #calculate the slope of n consecutive points on a plot
    slopes = [i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y = ser[i-n:i]
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled,x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)

#This function creates the "short" or "long" position
def market_order(instrument,units,sl): #Json format oanda api
    #units can be positive or negative, stop loss (in pips) added/subtracted to price
    account_id = "101-001-26553977-001"
    data = {
            "order": {
            "price": "",
            "timeInForce": "FOK",
            "instrument": str(instrument),
            "units": str(units),
            "type": "MARKET",
            "positionFill": "DEFAULT"
                    }
            }
    r = orders.OrderCreate(accountID=account_id, data=data)
    client.request(r)

#Helper function to calculate True Range and Average True Range
def ATR(DF,n):
    df = DF.copy()
    df['H-L']=abs(df['h']-df['l'])
    df['H-PC']=abs(df['h']-df['c'].shift(1))
    df['L-PC']=abs(df['l']-df['c'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return round(df2["ATR"][-1],4) # round to 4 decimal places since GBPUSD, EURUSD 1pip is 0.0001

#Function to calculate MACD
#typical values a = 12; b = 26, c = 9
def MACD(DF,a,b,c):
    df = DF.copy()
    df["MA_Fast"]=df["c"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["c"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    df.dropna(inplace=True)
    return (df["MACD"],df["Signal"])

#This function identifies trade signal from MACD technical indicator 
def trade_signal(df,curr):
    signal = ""
    if df["macd"][-1] > df["signal"][-1] and df["macd_slope"][-1] > df["signal_slope"][-1]:
        signal = "Buy"
    elif df["macd"][-1] < df["signal"][-1] and df["macd_slope"][-1] < df["signal_slope"][-1]:
        signal = "Sell"
    return signal

def main():
    global pairs
    try:
        r = trades.OpenTrades(accountID=account_id) #checks curr with open trades
        open_trades = client.request(r)['trades']
        curr_ls = []
        for i in range(len(open_trades)):
            curr_ls.append(open_trades[i]['instrument'])
        pairs = [i for i in pairs if i not in curr_ls]
        for currency in pairs:
            print("analyzing ",currency)
            ohlc = candles(currency)
            ohlc["macd"] = MACD(ohlc,12,26,9)[0]
            ohlc["signal"] = MACD(ohlc,12,26,9)[1]
            ohlc["macd_slope"] = slope(ohlc["macd"],5)
            ohlc["signal_slope"] = slope(ohlc["signal"],5)
            signal = trade_signal(ohlc,currency)
            if signal == "Buy":
                market_order(currency,pos_size,3*ATR(ohlc,120)) # sl is 3 x ATR
                print("New long position initiated for ", currency)
            elif signal == "Sell":
                market_order(currency,-1*pos_size,3*ATR(ohlc,120))
                print("New short position initiated for ", currency)
    except Exception as error:
        print("error encountered....skipping this iteration")
        print("Error: ", error)
        
# Continuous execution        
starttime=time.time()
timeout = time.time() + 60*60*1  # 60 seconds times 60 meaning the script will run for 1 hr
while time.time() <= timeout:
    try:
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
        time.sleep(60 - ((time.time() - starttime) % 60.0)) # 1 minute interval between each new execution
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()