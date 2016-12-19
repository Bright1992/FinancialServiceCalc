# -*- coding: utf-8 -*-
import os, sys, io, time
import pandas
import MySQLdb
import urllib
import re
import shutil
import numpy
import datetime
from numpy import *

def insertMysql(username, password, filename, localdir):
    conn = MySQLdb.Connect(host='localhost', user=username, passwd=password, db='Financial', charset='utf8', use_unicode= True)
    #conn.set_character_set('utf-8')
    cursor = conn.cursor()
    txtfile = localdir
    read_file = open(txtfile, 'rU')
    f = open(txtfile)
    judgeholiday = f.readline().decode('gbk').strip()
    if judgeholiday == '<script language="javascript">':
        print filename + 'has no tradings!'
    else:
        create_str = 'create table if not exists ' + filename + """(tradetime varchar(20),
        tradeprice varchar(20), pricechange varchar(20), turnover varchar(20), tradevolume varchar(20))"""
        cursor.execute(create_str)
        query = 'insert into ' + filename +' values(%s, %s, %s, %s, %s)'
        count = len(read_file.readlines())-1
        print count
        line = f.readline().decode('gbk')
        for count_i in range(1, count):
            line = f.readline().decode('gbk')
            p = re.compile(r'\s*')
            value = p.split(line)
            tradetime = value[0]
            #print tradetime
            tradeprice = value[1]
            pricechange = value[2]
            turnover = value[3]
            tradevolume = value[4]
            values = (tradetime, tradeprice, pricechange, turnover, tradevolume)
            cursor.execute(query, values)
    cursor.close()
    conn.commit()
    conn.close()

def deleteMysql(username, password, filename, localdir):
    conn = MySQLdb.Connect(host='localhost', user=username, passwd=password, db='Financial', charset='utf8',
                           use_unicode=True)
    cursor = conn.cursor()
    #cursor.execute('use Financial')
    deletetxt = localdir
    if os.path.exists(deletetxt):
        os.remove(deletetxt)
    cursor.execute("""drop table if exists """ + filename)
    cursor.close()
    conn.commit()
    conn.close()

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
            #if the day before current day has data, then break
            date = now - datetime.timedelta(days=(dayrange+1))
            hisfile = os.path.exists(dirlog + shareid + '_' + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '.txt')
            if hisfile:
                break
            insertMysql(username, password, insertfilename2, localDirinsert2)
