#!/usr/bin/env python
# coding: utf-8

# https://steemit.com/python/@marketstack/how-to-download-historical-price-data-from-binance-with-python
import requests        # for making http requests to binance
import json            # for parsing what binance sends back to us
import pandas as pd    # for storing and manipulating the data we get back
import numpy as np     # numerical python, i usually need this somewhere 
                       # and so i import by habit nowadays

import matplotlib.pyplot as plt # for charts and such
    
import datetime as dt  # for dealing with times


# This function retrieves data for a single day
def get_bars(symbol, interval, start_time, end_time, limit=1000):
    url = 'https://api.binance.com/api/v1/klines'
    
    start_time = str(int(start_time.timestamp() * 1000))
    end_time = str(int(end_time.timestamp() * 1000))
    
    params = {'symbol': symbol,
             'interval': interval,
             'startTime': start_time,
             'endTime': end_time,
             'limit': str(limit)}
    
    data = json.loads(requests.get(url, params=params).text)
    df = pd.DataFrame(data)
    
    df.columns = ['open_time',
                 'open', 'high', 'low', 'close', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
    
    df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
    
    #Getting rid of last row which contains data from the following day
    df = df.iloc[:-1,:]
    
    return df


# This functions allow
def get_historical_data(symbol, interval, start_time, end_time, limit=1000):
    delta = end_time - start_time # as timedelta
    # Store results for each day here
    dataframes = []
    
    for i in range(delta.days + 1):
        start_day = start_time + dt.timedelta(days=i)
        end_day = start_day + dt.timedelta(days=1)
        
        day_bars = get_bars(symbol, interval, start_day, end_day, limit)
        
        dataframes.append(day_bars)
    # Concat all day dataframes in a single dataframe
    df = pd.concat(dataframes)
    df.iloc[:, 0:6] = df.iloc[:, 0:6].astype(np.float16)
    return df
        



if __init__ == '__main__':
    start_time = dt.datetime(2020,1,1)
    end_time = dt.datetime(2020,1,5)

    all_days = get_historical_data('ETHUSDT', '5m', start_time, end_time)

    all_days.head()