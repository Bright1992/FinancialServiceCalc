# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import time
import datetime
import urllib2


def currentdata( stockname):
    try:
        #s = urllib2.urlopen("http://hq.sinajs.cn/list=sh600030").read()
        s = urllib2.urlopen("http://hq.sinajs.cn/list=" + stockname).read()
        #s = s.decode('gbk')
        #if s != s1:
        #print(s)
        s = s.split(',', 31)
        #print(s)
        #print(len(s))
        return s
    except  urllib2.HTTPError  as e:
        print (e.code)

if __name__=="__main__":
    stockname = "sh600030"
    curtime = datetime.datetime.now()
    destime = curtime.replace(hour=16, minute=0, second=0, microsecond=0)
    while(curtime < destime):
        data = currentdata(stockname)
        curtime = datetime.datetime.now()
        time.sleep(5)
        print(data[31])





