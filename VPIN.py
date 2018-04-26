import pybitflyer
import json
import time
import requests
import pandas as pd
import datetime
from statistics import mean, median,variance,stdev
from scipy.stats import norm
from datetime import datetime

public_api = pybitflyer.API()

def get_now_data():
    while True:
        try:
            executions = public_api.executions(product_code = "FX_BTC_JPY")
            if executions != []:
                break
        except requests.exceptions.ConnectionError:
            print("connection error")
            time.sleep(1)
        except UnboundLocalError:
            print("unboundlocal error")
            time.sleep(1)
        except json.decoder.JSONDecodeError:
            print("jsondecode error")
            time.sleep(1)
    return executions

def small_difference_data(n):
    past_number = get_now_data()[0]['id']
    time.sleep(n)
    now_data = get_now_data()
    now_number = now_data[0]['id']
    difference_list = [x for x in now_data if past_number <= x['id'] <= now_number]
    return difference_list

def get_time_var_data(n, unit):
    difference_list = small_difference_data(n)
    if difference_list == []:
        return (0,0)
    else:
        return difference_list[-1]['price'], sum([x['size'] for x in difference_list]) / unit 

def get_bucket_data(n, unit, volumebucket):
    price = []
    volume = []
    while sum(volume) < volumebucket:
        p,v = get_time_var_data(n, unit)
        price.append(p)
        volume.append(v)
    return price, volume

def invalance_calc(price, volume, volumebucket):
    sd = stdev(price) if len(price) != 1 else 0
    invalance = 0
    for i in range(len(price)-1):
        vb = volume[i+1] * norm.cdf((price[i+1] - price[i])/ sd) if sd != 0 else volume[i+1] / 2
        vs = volume[i+1] - vb
        invalance += abs(vb-vs)
        i += 1
    return invalance

def delappend(listdata, add_item):
    del listdata[0]
    listdata.append(add_item)
    return listdata

def summary(listdata, volumebucket):
    return sum(listdata)/(len(listdata) * volumebucket) 

def VPIN(n, m, unit, volumebucket):
    print('time bar =', n)
    print('volume bucket =', volumebucket)
    print('vpin unit =', m)
    listdata = [0 for x in range(m)]
    while True:
        price,volume = get_bucket_data(n, unit, volumebucket)
        invalance = invalance_calc(price, volume, volumebucket)
        listdata = delappend(listdata, invalance)
        vpin = summary(listdata, volumebucket)
        print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 'VPIN =', vpin)
        while True:
            try:
                ticker_data = public_api.ticker(product_code = "FX_BTC_JPY")
                midprice = int((ticker_data['best_bid'] + ticker_data['best_ask']) / 2)
                if midprice != []:
                    break
            except requests.exceptions.ConnectionError:
                print("connection error")
                time.sleep(1)
            except UnboundLocalError:
                print("unboundlocal error")
                time.sleep(1)
            except json.decoder.JSONDecodeError:
                print("jsondecode error")
                time.sleep(1)
        with open('Historical_VPIN.csv', 'a') as f:
                        f.write('{},{}\n'.format(vpin,midprice))

VPIN(1,2,0.1,150)
