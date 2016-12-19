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
#imput the global values
INTERVAL_MINUTE= Main.INTERVAL_MINUTE
INTERVAL_NUM= Main.INTERVAL_NUM
Train_day_num= Main.Train_day_num
Read_data_day_num= Main.Read_data_day_num

def factorial(num):
    if (num==0):
        return 1
    elif (num==1):
        return 1
    else:
        return num*factorial(num-1)

def trainVWAP_line_regression(stockID):
    dirlog = 'txtfile/'
    dirlog_2 = 'volumefile/'
    now = datetime.date.today()
    todayfile = os.path.exists(dirlog + stockID + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '.txt')
    count = 0
    total_volume = 0
    train_data = []
    if todayfile:
        read_historical_data = False #make program to read data begin from last 2 days
        for dayrange in range(0, Read_data_day_num):
            if count == (Train_day_num*2):
                break
            date = now - datetime.timedelta(days=dayrange)
            volume_file = dirlog_2 + 'volume_' + stockID + '_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '.txt'
            volume_file_exist_flag = os.path.exists(volume_file)
            if volume_file_exist_flag:
                if read_historical_data:
                    read_file = open(volume_file, 'rU')
                    f = open(volume_file)
                    count = count + 1
                    count_len = len(read_file.readlines())
                    if (count_len-1) != INTERVAL_NUM:
                        print 'volume data is not Impossible.'
                        time.sleep(100)
                    tmp = []
                    line = f.readline()
                    p = re.compile(r'\s*')
                    value = p.split(line)
                    total_volume += int(value[0])
                    for j in range(0, INTERVAL_NUM):
                        line = f.readline()
                        p = re.compile(r'\s*')
                        value = p.split(line)
                        #print value[0]
                        #time.sleep(1)
                        tmp.append(float(value[0]))
                    train_data.append(tmp)
                read_historical_data = True
            else:
                continue
    else:
        print 'You should input data before training.'
        return
    #print train_data
    #time.sleep(100)
    #here, we have gotten volume data
    total_volume = total_volume/20
    #print total_volume
    sum_percentage = 0
    train_file_dir = 'train_volumefile_line/' + stockID + '_10.txt'
    train_file = open(train_file_dir, 'w')
    for i in range (0, INTERVAL_NUM):
        #for every column, get every column data
        train_column = []
        for j in range (0, Train_day_num*2):
            train_column.append(train_data[Train_day_num*2-1-j][i])
        #print train_column
        #time.sleep(10)
        array_X = [[0] * Train_day_num for row in range(Train_day_num)]
        for j in range (0, Train_day_num):
            for k in range (0, Train_day_num):
                array_X[j][k] = train_column[j+k]
            #print mat_init[j]
        #print array_X
        #time.sleep(100)
        array_Y = []
        for j in range (0, Train_day_num):
            array_Y.append(train_column[Train_day_num+j])
            #print mat_Y[j]
        matrix_X = mat(array_X)
        matrix_Y = mat(array_Y).T
        matrix_X_Transpose = matrix_X.T
        matrix_tmp = (matrix_X_Transpose * matrix_X).I
        matrix_w = matrix_tmp * matrix_X_Transpose * matrix_Y
        #print matrix_w
        #print "\n"
        matrix_result = matrix_X[0] * matrix_w
        tmp = int((matrix_result[0][0]) * total_volume)
        train_file.write(str(tmp))
        train_file.write("\n")
        sum_percentage += tmp
    #print sum_percentage
    #Continue train 5 days data
    sum_percentage = 0
    train_file_dir = 'train_volumefile_line/' + stockID + '_5.txt'
    train_file = open(train_file_dir, 'w')
    for i in range (0, INTERVAL_NUM):
        #for every column, get every column data
        train_column = []
        for j in range (0, Train_day_num):
            train_column.append(train_data[Train_day_num-1-j][i])
        #print train_column
        #time.sleep(10)
        array_X = [[0] * (Train_day_num/2) for row in range(Train_day_num/2)]
        for j in range (0, (Train_day_num/2)):
            for k in range (0, (Train_day_num/2)):
                array_X[j][k] = train_column[j+k]
            #print mat_init[j]
        #print array_X
        #time.sleep(100)
        array_Y = []
        for j in range (0, (Train_day_num/2)):
            array_Y.append(train_column[(Train_day_num/2)+j])
            #print mat_Y[j]
        matrix_X = mat(array_X)
        matrix_Y = mat(array_Y).T
        matrix_X_Transpose = matrix_X.T
        matrix_tmp = (matrix_X_Transpose * matrix_X).I
        matrix_w = matrix_tmp * matrix_X_Transpose * matrix_Y
        #print matrix_w
        #print "\n"
        matrix_result = matrix_X[0] * matrix_w
        tmp = int((matrix_result[0][0]) * total_volume)
        train_file.write(str(tmp))
        train_file.write("\n")
        sum_percentage += tmp
    #print sum_percentage
    #Continue to get another way -- binary
    sum_percentage = 0
    train_file_dir = 'train_volumefile_line/' + stockID + '_binary.txt'
    train_file = open(train_file_dir, 'w')
    train_column = [0] * INTERVAL_NUM
    for i in range (0, INTERVAL_NUM):
        #for every column
        volume = 0
        for j in range (0, 6):
            if (j == 5):
                volume += train_data[j][i]/(2**5)
            else:
                volume += train_data[j][i]/((j+1)**5)
        train_column[i] = int(volume * total_volume)
    for i in range (0, INTERVAL_NUM):
        train_file.write(str(train_column[i]))
        train_file.write("\n")
    #Continue to get another way -- exp
    exp = 2.718281828459
    sum_percentage = 0
    train_file_dir = 'train_volumefile_line/' + stockID + '_e.txt'
    train_file = open(train_file_dir, 'w')
    train_column = [0] * INTERVAL_NUM
    for i in range (0, INTERVAL_NUM):
        #for every column
        volume = 0
        for j in range (0, 6):
            volume += train_data[j][i]/(factorial(j)*exp)
        train_column[i] = int(volume * total_volume)
    for i in range (0, INTERVAL_NUM):
        train_file.write(str(train_column[i]))
        train_file.write("\n")



def calculateVolume(filename, output_file):
    #volume result is zheng xu de 
    output_file = 'volumefile/volume_' + output_file + '.txt'
    read_file = open(filename, 'rU')
    f = open(filename)
    judgeholiday = f.readline().decode('gbk').strip()
    actual_total_volume = 0
    if judgeholiday == '<script language="javascript">':
        print 'Has no tradings.'
    else:
        count = len(read_file.readlines())-1
        count_volume = []
        count_volume = [0] * INTERVAL_NUM
        #print count_volume
        for count_i in range(0, count):
            line = f.readline().decode('gbk')
            p = re.compile(r'\s*')
            value = p.split(line)
            if (value[5] == u'卖盘'):
                continue
            if (value[5] == u'中性盘'):
                continue
            actual_total_volume += int(value[3])
            time_now = value[0]
            seconds_dec = INTERVAL_MINUTE * 60
            time_end = datetime.datetime.strptime("2010-01-03 15:00:00", "%Y-%m-%d %H:%M:%S")
            for index in range(1, INTERVAL_NUM+1):
                delta = datetime.timedelta(seconds=seconds_dec)
                time_end = time_end - delta
                time_string = time_end.strftime("%H:%M:%S")
                if (str(time_end) == "2010-01-03 13:00:00"):
                    time_end = datetime.datetime.strptime("2010-01-03 11:30:00", "%Y-%m-%d %H:%M:%S")
                if (str(time_end) == "2010-01-03 09:30:00"):
                    #print "ok"
                    time_end = time_end - delta
                    time_string = time_end.strftime("%H:%M:%S")
                #print time_string
                if (time_now >= time_string):
                    count_volume[INTERVAL_NUM - index] += int(value[3])
                    break
            #print count_volume
            #time.sleep(3)
        #print count_volume
        #time.sleep(10)
        count_volume_percentage = [] * INTERVAL_NUM
        count_volume_total = 0
        for i in range(0, INTERVAL_NUM):
            count_volume_total = count_volume_total + count_volume[i]
        if (count_volume_total != actual_total_volume):
            print "volume calculation error"
            time.sleep(300)
        file_object = open(output_file, 'w')
        file_object.write(str(count_volume_total))
        file_object.write("\n")
        for i in range(0, INTERVAL_NUM):
            percentage = (float)(count_volume[i]) / (float)(count_volume_total)
            file_object.write(str(percentage))
            file_object.write("\n")
        file_object.close()
    f.close()
                
                

def spiderData(excelUrl, localDir):
    spiderurl = excelUrl
    spiderdir = localDir
    urllib.urlretrieve(spiderurl, spiderdir)

def updateStock(stockID):
    str1 = 'http://market.finance.sina.com.cn/downxls.php?date='
    str2 = "&symbol="
    shareid = stockID
    dirlog = 'txtfile/'
    now = datetime.date.today()
    #print now
    todayfile = os.path.exists(dirlog + shareid + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '.txt')
    if todayfile:
        print 'No need to update MySQL.'
        trainVWAP_line_regression(stockID)
    else:
        print 'Updating MySQL'
        for dayrange in range(0, Read_data_day_num):
            date = now - datetime.timedelta(days=dayrange)
            print date
            url2 = str1 + str(date) + str2 + shareid
            print url2
            insertfilename2 = shareid + '_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day)
            localDirinsert2 = dirlog+insertfilename2+'.txt'
            spiderData(url2, localDirinsert2)
            calculateVolume(localDirinsert2, insertfilename2)
            #if the day before current day has data, then break
            date = now - datetime.timedelta(days=(dayrange+1))
            hisfile = os.path.exists(dirlog + shareid + '_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '.txt')
            if hisfile:
                break
        trainVWAP_line_regression(stockID)
