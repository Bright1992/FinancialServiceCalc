# -*- coding: utf-8 -*-
import os, sys, io, time
import pandas
import urllib
import re
import shutil
import numpy
import datetime
from numpy import *

def calculateVolume(filename, output_file):
    output_file = 'volumefile/volume_' + output_file + '.txt'
    read_file = open(filename, 'rU')
    f = open(filename)
    judgeholiday = f.readline().decode('gbk').strip()
    if judgeholiday == '<script language="javascript">':
        print ' has no tradings.'
    else:
        count = len(read_file.readlines())-1
        line = f.readline().decode('gbk')
        count_volume = []
        count_volume = [0] * 48
        for count_i in range(1, count):
            line = f.readline().decode('gbk')
            p = re.compile(r'\s*')
            value = p.split(line)
            #print value[5]
            #time.sleep(1)
            if (value[5] == u'卖出'):
                continue
            if value[0] >= '14:55:00':
                count_volume[47] += int(value[3])
                continue
            if value[0] >= '14:50:00':
                count_volume[46] += int(value[3])
                continue
            if value[0] >= '14:45:00':
                count_volume[45] += int(value[3])
                continue
            if value[0] >= '14:40:00':
                count_volume[44] += int(value[3])
                continue
            if value[0] >= '14:35:00':
                count_volume[43] += int(value[3])
                continue
            if value[0] >= '14:30:00':
                count_volume[42] += int(value[3])
                continue
            if value[0] >= '14:25:00':
                count_volume[41] += int(value[3])
                continue
            if value[0] >= '14:20:00':
                count_volume[40] += int(value[3])
                continue
            if value[0] >= '14:15:00':
                count_volume[39] += int(value[3])
                continue
            if value[0] >= '14:10:00':
                count_volume[38] += int(value[3])
                continue
            if value[0] >= '14:05:00':
                count_volume[37] += int(value[3])
                continue
            if value[0] >= '14:00:00':
                count_volume[36] += int(value[3])
                continue
            if value[0] >= '13:55:00':
                count_volume[35] += int(value[3])
                continue
            if value[0] >= '13:50:00':
                count_volume[34] += int(value[3])
                continue
            if value[0] >= '13:45:00':
                count_volume[33] += int(value[3])
                continue
            if value[0] >= '13:40:00':
                count_volume[32] += int(value[3])
                continue
            if value[0] >= '13:35:00':
                count_volume[31] += int(value[3])
                continue
            if value[0] >= '13:30:00':
                count_volume[30] += int(value[3])
                continue
            if value[0] >= '13:25:00':
                count_volume[29] += int(value[3])
                continue
            if value[0] >= '13:20:00':
                count_volume[28] += int(value[3])
                continue
            if value[0] >= '13:15:00':
                count_volume[27] += int(value[3])
                continue
            if value[0] >= '13:10:00':
                count_volume[26] += int(value[3])
                continue
            if value[0] >= '13:05:00':
                count_volume[25] += int(value[3])
                continue
            if value[0] >= '13:00:00':
                count_volume[24] += int(value[3])
                continue
            if value[0] >= '11:25:00':
                count_volume[23] += int(value[3])
                continue
            if value[0] >= '11:20:00':
                count_volume[22] += int(value[3])
                continue
            if value[0] >= '11:15:00':
                count_volume[21] += int(value[3])
                continue
            if value[0] >= '11:10:00':
                count_volume[20] += int(value[3])
                continue
            if value[0] >= '11:05:00':
                count_volume[19] += int(value[3])
                continue
            if value[0] >= '11:00:00':
                count_volume[18] += int(value[3])
                continue
            if value[0] >= '10:55:00':
                count_volume[17] += int(value[3])
                continue
            if value[0] >= '10:50:00':
                count_volume[16] += int(value[3])
                continue
            if value[0] >= '10:45:00':
                count_volume[15] += int(value[3])
                continue
            if value[0] >= '10:40:00':
                count_volume[14] += int(value[3])
                continue
            if value[0] >= '10:35:00':
                count_volume[13] += int(value[3])
                continue
            if value[0] >= '10:30:00':
                count_volume[12] += int(value[3])
                continue
            if value[0] >= '10:25:00':
                count_volume[11] += int(value[3])
                continue
            if value[0] >= '10:20:00':
                count_volume[10] += int(value[3])
                continue
            if value[0] >= '10:15:00':
                count_volume[9] += int(value[3])
                continue
            if value[0] >= '10:10:00':
                count_volume[8] += int(value[3])
                continue
            if value[0] >= '10:05:00':
                count_volume[7] += int(value[3])
                continue
            if value[0] >= '10:00:00':
                count_volume[6] += int(value[3])
                continue
            if value[0] >= '09:55:00':
                count_volume[5] += int(value[3])
                continue
            if value[0] >= '09:50:00':
                count_volume[4] += int(value[3])
                continue
            if value[0] >= '09:45:00':
                count_volume[3] += int(value[3])
                continue
            if value[0] >= '09:40:00':
                count_volume[2] += int(value[3])
                continue
            if value[0] >= '09:35:00':
                count_volume[1] += int(value[3])
                continue
            if value[0] < '09:35:00':
                count_volume[0] += int(value[3])
                continue
        #f_2 = open(output_file,'w')
        file_object = open(output_file, 'w')
        for i in range(0, 48):
            #print count_volume[i]
            file_object.write(str(count_volume[i]))
            file_object.write("\n")
        file_object.close()
    f.close()
    

def spiderData(excelUrl, localDir):
    spiderurl = excelUrl
    spiderdir = localDir
    urllib.urlretrieve(spiderurl, spiderdir)


def updateMySQL():
    username = 'root'
    password = 'as123456'
    str1 = 'http://market.finance.sina.com.cn/downxls.php?date='
    str2 = "&symbol="
    shareid = 'sh601988'
    dirlog = 'txtfile/'
    now = datetime.date.today()
    print now
    todayfile = os.path.exists(dirlog + shareid + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '.txt')
    #hisday = now - datetime.timedelta(days=180)
    #hisfile = os.path.exists(dirlog + shareid + '_' + str(hisday.year) + '_' + str(hisday.month) + '_' + str(hisday.day) + '.txt')
    if todayfile:
        print 'no need to update.'
    else:
        print 'updating'
        for dayrange in range(0, 30):
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
            #insertMysql(username, password, insertfilename2, localDirinsert2)


def trainVWAP(stockID):
    dirlog = 'txtfile/'
    dirlog_2 = 'volumefile/'
    now = datetime.date.today()
    todayfile = os.path.exists(dirlog + stockID + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '.txt')
    count = 0
    train_data = []
    if todayfile:
        #input 20 day data
        for dayrange in range(0, 40):
            date = now - datetime.timedelta(days=dayrange)
            volume_file = dirlog_2 + 'volume_' + stockID + '_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '.txt'
            volume_file_exist_flag = os.path.exists(volume_file)
            if volume_file_exist_flag:
                #print 'haha'
                read_file = open(volume_file, 'rU')
                f = open(volume_file)
                count = count + 1
                #input data
                count = len(read_file.readlines())
                if count != 48:
                    print 'volume data is not 48. Impossible.'
                    time.sleep(100)
                tmp = []
                for j in range(0, count):
                    line = f.readline()
                    p = re.compile(r'\s*')
                    value = p.split(line)
                    #print value[0]
                    #time.sleep(1)
                    tmp.append(int(value[0]))
                train_data.append(tmp)
            else:
                continue
            if count == 20:
                break
    else:
        print 'You should input data before training.'
    #print train_data
    #here, we have gotten 20 days volume data
    for i in range (0, 48):
        #for every column, get every column data
        train_column = []
        for j in range (0, 20):
            train_column.append(train_data[j][i])
        print train_column
        mat_init = mat(zeros((10,10)))
        for j in range (0, 10):
            count_tmp = j
            for k in range (0, 10):
                mat[j][k] = train_column[k + count_tmp]
        print mat_init
            



def TWAP(stockID, orderSize):
    dirlog = 'txtfile/'
    now = datetime.date.today()
    filename = dirlog_ + 'volume_' + stockID + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '.txt'
    for i in range (0, 7):
        date = now - datetime.timedelta(days=dayrange)
        filename = dirlog_ + 'volume_' + stockID + '_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '.txt'
        file_exist_flag = os.path.exists(filename)
        if file_exist_flag:
            break
        else:
            continue
    f = open(filename)
    

	
if __name__ == '__main__':
    #stockID = raw_input("Enter the stockID you want to buy : ")
    stockID = 'sh601988'
    updateMySQL()
    trainVWAP(stockID)