#_*_coding:utf-8_*_

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as figureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolBar
from matplotlib.dates import date2num,num2date
from datetime import datetime
import matplotlib.pyplot as plt
import sys

from matplotlib.dates import DateFormatter
from matplotlib.dates import DayLocator,MinuteLocator
from matplotlib.dates import MonthLocator

from getHistoricalData import getHistoricalData,getOrderSize
from getHistoricalData import delta2num

import time

alldays = DayLocator()
months = MonthLocator()
minutes=MinuteLocator(byminute=range(0,60,10))
minute_formatter = DateFormatter("%H:%M")


class graph(QWidget):
    def __init__(self,parent=None,stock='sz002024',year=0,month=0,day=0):
        super(graph,self).__init__(parent)

        interval=5
        self.data=getHistoricalData(stock,year,month,day,interval=interval)
        interval=delta2num(interval)
        figure1 = plt.figure(1) #返回当前的figure
        x = [ele[0] for ele in self.data]
        y = [ele[1] for ele in self.data]

        tm=datetime(year,month,day,11,30,0)
        ta=datetime(year,month,day,13,0,0)
        morningend=date2num(tm)
        afternoonbegin=date2num(ta)
        c=0;
        x01=[];x02=[];
        y01=[];y02=[];
        for ele in x:
            if ele<=morningend:
                x01.append(ele)
                y01.append(y[c])
            elif ele>=afternoonbegin:
                x02.append(ele)
                y02.append(y[c])
            c=c+1
        
        
        ymax=max(y);ymin=min(y)
        x1 = [ele+interval*0.1 for ele in x]
        y1 = [ele[3] for ele in self.data]
        s=sum(y1)
        y1=[ele/s*100 for ele in y1]
        y1max=max(y1)
        x2 = [ele+interval*0.5 for ele in x]
        print(len(x2))
        y2 = getOrderSize(stock)
        y2 = [ele*100 for ele in y2]
        y1max=max(y1max,max(y2))

        #ratio=0.3
        #y2 = [ele*sum(y1)*ratio for ele in y2]
        ax1=figure1.add_subplot(111)
        ax1.xaxis.set_major_locator(minutes)
        ax1.xaxis.set_major_formatter(minute_formatter)
        plt.ylabel('Volume(%)',fontsize=15)
        plt.ylim([0,y1max*1.5])
        plt.xlabel('Time',fontsize=15)
        ax2=ax1.twinx()
        bar_history=ax1.bar(x1,y1,width=interval*0.4,color='c',label='Historical Volume')
        bar_order=ax1.bar(x2,y2,width=interval*0.4,color=[1,0.4,0.6],label='Order Size')

        line_price,=ax2.plot(x01,y01,color='b',label='Price')
        ax2.plot(x02,y02,color='b')
        plt.title('%s'%stock.upper(),fontsize=20)
        plt.ylabel('Price',fontsize=15)
        plt.ylim([ymin-2*(ymax-ymin),ymax+0.25*(ymax-ymin)])
        figure1.autofmt_xdate()
        plt.grid()
        plt.legend(handles=(line_price,bar_history,bar_order),loc='upper right',ncol=3)
        #plt.legend(handles=(bar_history,),bbox_to_anchor=(0.5,-0.25),loc='lower center')
        plt.tight_layout()
        #plt.autoscale(tight=True)
        self.canvas1 = figureCanvas(figure1)
        self.canvas1.draw()
        self.toolbar1=NavigationToolBar(self.canvas1,self)

        layout = QHBoxLayout(self)
        leftLayout=QVBoxLayout(self)
        rightLayout=QVBoxLayout(self)
        layout.addLayout(leftLayout)
        #layout.addLayout(rightLayout)
        leftLayout.addWidget(self.canvas1)
        leftLayout.addWidget(self.toolbar1)
        #rightLayout.addWidget(self.canvas2)
        #rightLayout.addWidget(self.toolbar2)
        

    def __getOrderSize(self):
        y3=[ele[3]/10 for ele in self.data]
        return y3

class cdf_graph(QWidget):
    def __init__(self,parent=None,year=0,month=0,day=0,stock='0'):
        super(cdf_graph,self).__init__(parent)

        interval=5
        self.data=getHistoricalData(year=year,month=month,day=day,stock=stock,interval=interval)
        interval=delta2num(interval)
        figure2 = plt.figure(2)
        x3 = [ele[0] for ele in self.data]
        y3 = getOrderSize(stock)
        for i in range(1,len(y3)):
            y3[i]=y3[i]+y3[i-1]
        y3=[ele/y3[-1] for ele in y3]
        ax3=figure2.add_subplot(111)
        ax3.xaxis.set_major_locator(minutes)
        ax3.xaxis.set_major_formatter(minute_formatter)
        line_percent=ax3.plot(x3,y3,'-D',label='Completion Percentage')
        figure2.autofmt_xdate()
        plt.grid()
        plt.legend(loc='upper left')

        plt.title('%s'%stock.upper(),fontsize=20)
        plt.xlabel('Time',fontsize=20)
        plt.ylabel('Completion Percentage',fontsize=15)

        self.canvas2 = figureCanvas(figure2)
        self.canvas2.draw()
        self.toolbar2=NavigationToolBar(self.canvas2,self)

        layout = QHBoxLayout(self)
        rightLayout=QVBoxLayout(self)
        layout.addLayout(rightLayout)
        rightLayout.addWidget(self.canvas2)
        rightLayout.addWidget(self.toolbar2)
    
if __name__ == '__main__':
    year=2016;month=11;day=8;stock='sh600016'
    app = QApplication(sys.argv)
    ui = graph(year=year,month=month,day=day,stock=stock)
    ui2 = cdf_graph(year=year,month=month,day=day,stock=stock)
    ui.resize(1500,800)
    ui.setWindowTitle('Trade Simulation')
    ui2.setWindowTitle('Trade Simulation')
    ui.show()
    ui2.show()
    app.exec_()
