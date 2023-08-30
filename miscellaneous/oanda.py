#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:31:12 2023

@author: akintayosalu
"""

import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import pandas as pd

client = oandapyV20.API(access_token="05d7e64454a7504094fe680925845c5d-c78545469a1b3dcfd2e9cf332951c5f9",environment="practice")

#get historical data (candles)
params = {"count": 150,"granularity": "M5"} #granularity can be in seconds S5 - S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
candles = instruments.InstrumentsCandles(instrument="USD_JPY",params=params)
client.request(candles)
#print(candles.response)
ohlc_dict = candles.response["candles"] #grabs response field of candles
ohlc = pd.DataFrame(ohlc_dict) #turns json -> dataframe
ohlc_df = ohlc.mid.dropna().apply(pd.Series) #grabs the mid column of ohlc
#and turns the keys "o","h","l","c" into columns
ohlc_df["volume"] = ohlc["volume"]
ohlc_df.index = ohlc["time"]
ohlc_df = ohlc_df.apply(pd.to_numeric)

#streaming data (getting live price info)
params = {"instruments": "USD_JPY"}
account_id = "101-001-26553977-001" #can grab info 
r = pricing.PricingInfo(accountID=account_id, params=params)
i=0
""""""
while i <=20:
    rv = client.request(r)
    print("Time=",rv["time"])
    print("bid=",rv["prices"][0]["closeoutBid"])
    print("ask=",rv["prices"][0]["closeoutAsk"])
    print("*******************")
    i+=1

    
#trading account details
r = accounts.AccountDetails(accountID=account_id)
client.request(r)
print(r.response)

#trading account summary
r = accounts.AccountSummary(accountID=account_id)
client.request(r)
print(r.response)

#orders
data = {
        "order": {
        "price": "1.15",
        "stopLossOnFill": {
        "timeInForce": "GTC",
        "price": "1.2"
                          },
        "timeInForce": "FOK",
        "instrument": "USD_JPY",
        "units": "100",
        "type": "MARKET",
        "positionFill": "DEFAULT"
                }
        }
            
r = orders.OrderCreate(accountID=account_id, data=data)
client.request(r)

#slightly more sophisticated way of placing an order
def ATR(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['h']-df['l'])
    df['H-PC']=abs(df['h']-df['c'].shift(1))
    df['L-PC']=abs(df['l']-df['c'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return round(df2["ATR"][-1],2)

def market_order(instrument,units,sl):
    """units can be positive or negative, stop loss (in pips) added/subtracted to price """
    params = {"instruments": instrument}
    account_id = "101-001-26553977-001"
    r = pricing.PricingInfo(accountID=account_id, params=params)
    rv = client.request(r)
    if units > 0:
        price = float(rv["prices"][0]["closeoutAsk"])
        st_ls = price - sl
    else:
        price = float(rv["prices"][0]["closeoutBid"])
        st_ls = price + sl
    
    data = {
            "order": {
            "price": "",
            "stopLossOnFill": {
            "timeInForce": "GTC",
            "price": str(st_ls)
                              },
            "timeInForce": "FOK",
            "instrument": str(instrument),
            "units": str(units),
            "type": "MARKET",
            "positionFill": "DEFAULT"
                    }
            }
    return data


#check trades
v = trades.OpenTrades(accountID=account_id)
client.request(v)

#close trade
r = orders.OrderCreate(accountID=account_id, data=market_order("USD_JPY",-100,3*ATR(ohlc_df,120)))
client.request(r)


#check trades
r = trades.OpenTrades(accountID=account_id)
client.request(r)
#client.request(r)['trades'][0]['currentUnits']