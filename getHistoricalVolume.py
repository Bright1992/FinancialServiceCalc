import re
import os

from matplotlib.dates import date2num,num2date
import datetime

from math import ceil,floor

def getHistoricalData(year,month,day,opentime='09:25',morningclose='11:30',afternoonopen='13:00',closetime='15:00'):
    filename="sh601988_%04d_%d_%d.txt"%(year,month,day)
    f=open(filename,'rU')

    s=re.compile(r'\s*')
    c=0
    pool=[]

    for line in f.readlines():
        if c==0:
            c=1
            continue
        value=s.split(line)
        if value[5]=='¬Ú≈Ã':
            pool.append(value[:-2])
            hms=pool[-1][0].split(':')
            t=datetime.datetime(year,month,day,int(hms[0]),int(hms[1]),int(hms[2]))
            pool[-1][0]=date2num(t)
            if pool[-1][2]=='--':
                pool[-1][2]='0'
    pool=sorted(pool,key=lambda x:x[0])

    def hms2num(hms):
        lhms=hms.split(':')
        h=int(lhms[0])
        if len(lhms)<=1:
            m=0
        else:
            m=int(lhms[1])
        if len(lhms)<=2:
            s=0
        else:
            s=int(lhms[2])
        return date2num(datetime.datetime(year,month,day,h,m,s))

    #starttime=hms2num('10:00')
    opentime=hms2num(opentime)
    morningclose=hms2num(morningclose)
    afternoonopen=hms2num(afternoonopen)
    closetime=hms2num(closetime)
    interval=delta2num(5)

    if opentime>pool[0][0]:
        raise ValueError("found transactions before opentime")

    pool2=[];c=1
    accPrice=0;accTurnover=0;accVolume=0
    lastTime=opentime
    lastPrice=float(pool[0][1])
    lastChange=0
    lastTurnover=0
    lastVolume=0
    for record in pool:
        tradetime=record[0]
        tradeprice = float(record[1])
        pricechange = float(record[2])
        turnover = float(record[3])
        tradevolume = float(record[4])

        n0=(lastTime-opentime)/interval
        n1=(tradetime-opentime)/interval
        if n1>=c:
            n01=n0
            while n1>=c:
                accTurnover=accTurnover+lastTurnover*(c-n01)/(n1-n0)
                accVolume=accVolume+lastVolume*(c-n01)/(n1-n0)
                if accTurnover==0:
                    accPrice=lastPrice
                else:
                    accPrice=accVolume/accTurnover/100
                vtrade=[opentime+(c-1)*interval,accPrice,accTurnover,accVolume]
                pool2.append(vtrade)
                accPrice=0;accTurnover=0;accVolume=0
                n01=c
                c=c+1
        else:
            m=max([n0,c-1])
            #print(n0,n1)
            if n1!=n0:
                accTurnover=accTurnover+lastTurnover*(n1-m)/(n1-n0)
                accVolume=accVolume+lastVolume*(n1-m)/(n1-n0)
            else:
                accTurnover=accTurnover+lastTurnover
                accVolume=accVolume+lastVolume
        n0=n1
        lastTime=tradetime
        lastPrice=tradeprice
        lastChange=pricechange
        lastTurnover=turnover
        lastVolume=tradevolume

    while c<=(closetime-opentime)/interval:
        vtrade=[opentime+(c-1)*interval,(float)(pool[-1][1]),0,0]
        pool2.append(vtrade)
        c=c+1

    pool3=[]
    for ele in pool2:
        if ele[0]<morningclose or ele[0]>=afternoonopen:
            pool3.append(ele)
    return pool3


def delta2num(minute):
    return date2num(datetime.datetime(1,1,1,0,minute,0))-1



if __name__=='__main__':
    day=11
    month=5
    year=2016
    data=getHistoricalData(year,month,day)
