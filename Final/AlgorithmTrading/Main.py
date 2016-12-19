# -*- coding: utf-8 -*-
import os, sys, io, time
import pandas
import urllib
import re
import shutil
import numpy
import datetime
from numpy import *

INTERVAL_MINUTE = 5 #this number should be a divisor of 60
INTERVAL_NUM = 240 / INTERVAL_MINUTE
Train_day_num = 10
Read_data_day_num = 40

import HistoricalData
import Trade
import MySQL

if __name__ == '__main__':
    #stockID = raw_input("Enter the stockID you want to buy : ")
    stockID = 'sh601988'
    buy_num = 50
    trading_style = 0 #style: 0:normal 1:aggressive 2:passive
    HistoricalData.updateStock(stockID)
    Trade.tradeStock(stockID, buy_num, trading_style)
    #trainVWAP(stockID)
