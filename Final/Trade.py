# -*- coding: utf-8 -*-
import os, sys, io, time
import pandas
import urllib
import re
import shutil
import numpy
import datetime
from numpy import *

import Main

# imput the global values
INTERVAL_MINUTE = Main.INTERVAL_MINUTE
INTERVAL_NUM = Main.INTERVAL_NUM
Train_day_num = Main.Train_day_num
Read_data_day_num = Main.Read_data_day_num

TWAP_collect_trading_data_nums = 50


def trading_VWAP(trading_schedule, trading_data, trading_count, stockID, buy_num, trading_style):
    # trading_schedule
    txt_file = open(trading_schedule, 'rU')
    f = open(trading_schedule)
    count = len(txt_file.readlines())
    volume_data = [0] * count
    total_volume = 0
    for i in range(0, count):
        line = f.readline().decode('gbk')
        p = re.compile(r'\s*')
        value = p.split(line)
        volume_data[i] = (int)(value[0])
        total_volume += (int)(value[0])
    # print volume_data
    trading_schedule_data = [0] * count
    trading_schedule_data_total = 0
    for i in range(0, count):
        trading_schedule_data[i] = (int)((float)(volume_data[i]) / total_volume * buy_num)
        trading_schedule_data_total += trading_schedule_data[i]
    trading_schedule_data[0] = trading_schedule_data[0] + buy_num - trading_schedule_data_total
    # print trading_schedule_data
    time_start = datetime.datetime.strptime("2010-01-03 09:30:00", "%Y-%m-%d %H:%M:%S")
    seconds_inc = INTERVAL_MINUTE * 60
    # time_string = time_start.strftime("%H:%M:%S")
    time_schedule = []
    for i in range(0, count):
        time_string = time_start.strftime("%H:%M:%S")
        time_schedule.append(time_string)
        delta = datetime.timedelta(seconds=seconds_inc)
        time_start = time_start + delta
        if (str(time_start) == "2010-01-03 11:30:00"):
            time_start = datetime.datetime.strptime("2010-01-03 13:00:00", "%Y-%m-%d %H:%M:%S")
            # print time_string
            # print time_schedule[i]
    buy_record = []
    total_buy = 0
    total_cost = 0
    buy_remainder_total = buy_num
    for i in range(0, count):
        trading_volume_interval = trading_schedule_data[i]
        if (trading_volume_interval == 0):
            continue
        trading_volume_per_5s = (int)((float)(trading_volume_interval) / 6 / INTERVAL_MINUTE)
        trading_volume_per_5s += 1
        buy_remainder = trading_volume_interval
        for j in range(0, trading_count):
            if (trading_data[j][0] >= time_schedule[i]):
                # print trading_data[j][0]
                for k in range(0, (6 * INTERVAL_MINUTE)):
                    cost = trading_volume_per_5s * (int)((float)(trading_data[j + k][1]) * 100)
                    total_cost += cost
                    buy_record_item = [trading_data[j + k][0], trading_data[j + k][1], trading_volume_per_5s, cost,
                                       buy_remainder_total]
                    print buy_record_item
                    buy_record.append(buy_record_item)
                    total_buy += trading_volume_per_5s
                    buy_remainder_total = buy_remainder_total - trading_volume_per_5s
                    if (trading_volume_per_5s == buy_remainder):
                        break
                    buy_remainder = buy_remainder - trading_volume_per_5s
                    if (buy_remainder < trading_volume_per_5s):
                        trading_volume_per_5s = buy_remainder
                break
    print total_buy
    return


def trading_TWAP(trading_data, trading_nums, stockID, buy_num, trading_style):
    # trading_volume_per_interval = (buy_num - buy_num%INTERVAL_NUM) / INTERVAL_NUM
    # print trading_volume_per_interval
    volume_count = 0
    for i in range(1, TWAP_collect_trading_data_nums):
        volume_count += int(trading_data[i][2])
    volume_average = volume_count / TWAP_collect_trading_data_nums
    # print volume_average
    percentage = 3
    trading_volume_per_5s = 0
    for percentage in range(0, 100):
        trading_volume_per_5s = (int)(volume_average * percentage / 100)
        trading_amount = trading_volume_per_5s * (trading_nums - TWAP_collect_trading_data_nums - 180)
        if (trading_amount > buy_num):
            trading_volume_per_5s += 1
            break
    # print final_percentage
    # print trading_volume_per_5s
    # time.sleep(10)
    total_cost = 0
    buy_record = []
    buy_remainder = buy_num
    for i in range(TWAP_collect_trading_data_nums, trading_nums):
        cost = trading_volume_per_5s * (int)((float)(trading_data[i][1]) * 100)
        total_cost += cost
        buy_record_item = [trading_data[i][0], trading_data[i][1], trading_volume_per_5s, cost, buy_remainder]
        print buy_record_item
        buy_record.append(buy_record_item)
        if (trading_volume_per_5s == buy_remainder):
            break
        buy_remainder = buy_remainder - trading_volume_per_5s
        if (buy_remainder < trading_volume_per_5s):
            trading_volume_per_5s = buy_remainder
    # calculate acutal TWAP
    total_price = 0
    for i in range(0, trading_nums):
        total_price += (float)(trading_data[i][1])
    acutal_TWAP = total_price / trading_nums
    # print total_cost
    print "Our TWAP is: " + (str)((float)(total_cost) / buy_num / 100)
    print "Acutal TWAP is " + (str)(acutal_TWAP)
    return


def tradeStock(stockID, buy_num, trading_style):
    train_file_dir_1 = 'train_volumefile_line/' + stockID + '_10.txt'
    train_file_dir_2 = 'train_volumefile_line/' + stockID + '_5.txt'
    train_file_dir_3 = 'train_volumefile_line/' + stockID + '_binary.txt'
    train_file_dir_4 = 'train_volumefile_line/' + stockID + '_e.txt'
    dirlog = 'txtfile/'
    dirlog_2 = 'volumefile/'
    now = datetime.date.today()
    for dayrange in range(0, Read_data_day_num):
        abspath=sys.path[0]+'\\AlgorithmTrading'
        date = now - datetime.timedelta(days=dayrange)
        volume_file_exist_flag = False
        volume_file = dirlog_2 + 'volume_' + stockID + '_' + str(date.year) + '_' + str(date.month) + '_' + str(
            date.day) + '.txt'
        volume_file_exist_flag = os.path.exists(volume_file)
        if volume_file_exist_flag:
            txt_file_name = stockID + '_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day)
            txt_file_dir = dirlog + txt_file_name + '.txt'
            break
    if (os.path.exists(txt_file_dir) == False):
        print txt_file_dir
        print 'This sentence should not be printed. Check your code.'
        return
    txt_file = open(txt_file_dir, 'rU')
    f = open(txt_file_dir)
    count = len(txt_file.readlines()) - 1
    # print count
    judgeholiday = f.readline().decode('gbk').strip()
    # print judgeholiday
    if judgeholiday == '<script language="javascript">':
        print 'This sentence should not be printed. Check your code.'
        return
    trading_data = []
    total_volume = 0
    total_money = 0
    trading_count = 0
    for i in range(0, count):
        line = f.readline().decode('gbk')
        p = re.compile(r'\s*')
        value = p.split(line)
        # print value
        if (value[5] == u'卖盘'):
            continue
        if (value[5] == u'中性盘'):
            continue
        total_volume += int(value[3])
        total_money += int(value[4])
        trading_item = [value[0], value[1], value[3]]
        # print trading_item
        trading_data.append(trading_item)
        trading_count += 1
        # trading_data[count-1-i] = trading_item
        # time.sleep(1)
    swap_begin = 0
    swap_end = trading_count - 1
    for n in range(0, trading_count):
        temp = trading_data[swap_begin]
        trading_data[swap_begin] = trading_data[swap_end]
        trading_data[swap_end] = temp
        swap_begin += 1
        swap_end -= 1
        if ((swap_begin == swap_end) or (((swap_begin + 1) == swap_end))):
            break
            # for n in range (0, trading_count):
            # here, I suppose to delete the fisrt item in 09:25:00
            # print trading_data[n]
            # time.sleep(1)
    VWAP = total_money / total_volume
    print "after 5 seconds, we will start TWAP"
    time.sleep(3)
    trading_TWAP(trading_data, trading_count, stockID, buy_num, trading_style)
    print "after 5 seconds, we will start VWAP_10_day_train"
    time.sleep(3)
    trading_VWAP(train_file_dir_1, trading_data, trading_count, stockID, buy_num, trading_style)
    print "after 5 seconds, we will start VWAP_5_day_train"
    time.sleep(3)
    trading_VWAP(train_file_dir_2, trading_data, trading_count, stockID, buy_num, trading_style)
    print "after 5 seconds, we will start VWAP_binary"
    time.sleep(3)
    trading_VWAP(train_file_dir_3, trading_data, trading_count, stockID, buy_num, trading_style)
    print "after 5 seconds, we will start VWAP_exp"
    time.sleep(3)
    trading_VWAP(train_file_dir_4, trading_data, trading_count, stockID, buy_num, trading_style)
    return
