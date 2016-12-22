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

from HistoricalData import updateStock
import Trade as td
from getRealtimeData import getRealtimeData,delta2num
from Trade import *
import time

alldays = DayLocator()
months = MonthLocator()
minutes=MinuteLocator(byminute=range(0,60,10))
minute_formatter = DateFormatter("%H:%M")


class console(QWidget):
    def __init__(self,parent=None,stock='0',year=0,month=0,day=0,alg='TVWAP'):
        super(console,self).__init__(parent)
        self.draw_layout()
        algs=['TWAP','VWAP(10 day)','VWAP(5 day)','VWAP(binary)','VWAP(exp)']
        self.set_alg(algs)

    def draw_layout(self):
        self.label_sid=QLabel("Stock ID:")
        self.label_volume=QLabel("Volume:")
        self.label_alg=QLabel("Algorithm:")
        self.text_sid=QLineEdit()
        self.text_volume=QLineEdit()
        self.text_alg=QComboBox()
        self.label_sid.setMinimumWidth(100)
        self.label_volume.setMinimumWidth(100)
        self.label_alg.setMinimumWidth(100)
        self.btn_start=QPushButton("Start")
        self.btn_stop=QPushButton("Stop")
        self.mainLayout=QGridLayout(self)
        self.optionLayout=QGridLayout()

        self.hLayout1=QHBoxLayout()
        self.hLayout1.addWidget(self.label_sid)
        self.hLayout1.addWidget(self.text_sid)
        self.hLayout2=QHBoxLayout()
        self.hLayout2.addWidget(self.label_volume)
        self.hLayout2.addWidget(self.text_volume)
        self.hLayout3=QHBoxLayout()
        self.hLayout3.addWidget(self.label_alg)
        self.hLayout3.addWidget(self.text_alg)
        self.hLayout4=QHBoxLayout()
        self.hLayout4.addWidget(self.btn_start)
        self.hLayout4.addWidget(self.btn_stop)

        self.hLayout1.addStretch()
        self.hLayout2.addStretch()
        self.hLayout3.addStretch()
        self.hLayout4.addStretch()

        self.optionLayout.addLayout(self.hLayout1,1,0)
        self.optionLayout.addLayout(self.hLayout2,2,0)
        self.optionLayout.addLayout(self.hLayout3,3,0)
        self.optionLayout.addLayout(self.hLayout4,4,0)

        hline1=QSplitter()
        hline1.setFixedHeight(10)
        self.optionLayout.addWidget(hline1,0,0)
        self.optionLayout.addWidget(hline1,5,0,6,0)
        self.vline1=QSplitter()

        self.vLayout_summary=QVBoxLayout()

        self.label_summary=QLabel("Trade Summary")
        font=QFont()
        font.setPixelSize(30)
        self.label_summary.setFont(font)

        self.label_summary.setAlignment(Qt.AlignCenter)
        self.vLayout_summary.addWidget(self.label_summary)

        self.textBsr_summary=QTextBrowser()
        self.vLayout_summary.addWidget(self.textBsr_summary)

        self.figure1=plt.figure(1)
        self.canvas_sched = figureCanvas(self.figure1)
        self.canvas_sched.setMaximumHeight(500)
        self.canvas_sched.setFixedWidth(800)

        self.figure2=plt.figure(2)
        self.canvas_rt = figureCanvas(self.figure2)
        self.canvas_rt.setMaximumHeight(500)
        self.canvas_rt.setFixedWidth(800)

        self.figure3=plt.figure(3)
        self.canvas_cdf=figureCanvas(self.figure3)
        self.canvas_cdf.setMaximumHeight(500)
        self.canvas_cdf.setFixedWidth(800)

        self.textBsr_rtinfo = QTextBrowser()
        self.textBsr_rtinfo.setMaximumWidth(500)
        self.textBsr_rtinfo.setFixedWidth(800)

        self.vLayout_rtinfo=QVBoxLayout()
        self.label_rtinfo=QLabel("Instant Information")
        self.label_rtinfo.setAlignment(Qt.AlignCenter)
        self.label_rtinfo.setFont(font)
        self.vLayout_rtinfo.addWidget(self.label_rtinfo)
        self.vLayout_rtinfo.addWidget(self.textBsr_rtinfo)

        self.mainLayout.addLayout(self.optionLayout,0,0)
        self.mainLayout.addLayout(self.vLayout_summary,1,0,4,1)
        self.mainLayout.addWidget(self.canvas_sched,0,1,2,2)
        self.mainLayout.addWidget(self.canvas_rt,0,3,2,4)
        self.mainLayout.addWidget(self.canvas_cdf,2,1,3,2)
        self.mainLayout.addLayout(self.vLayout_rtinfo,2,3,3,4)

    def set_alg(self,algs):
        for alg in algs:
            self.text_alg.addItem(alg)

    def misc(self,stock='0',year=0,month=0,day=0,alg='TVWAP'):
        interval = 5
        self.data = getRealtimeData(stock, year, month, day, interval=interval)
        interval = delta2num(interval)
        figure1 = plt.figure(1)  # 返回当前的figure
        x = [ele[0] for ele in self.data]
        y = [ele[1] for ele in self.data]

        tm = datetime.datetime(year, month, day, 11, 30, 0)
        ta = datetime.datetime(year, month, day, 13, 0, 0)
        morningend = date2num(tm)
        afternoonbegin = date2num(ta)
        c = 0
        x01 = []
        x02 = []
        y01 = []
        y02 = []
        for ele in x:
            if ele <= morningend:
                x01.append(ele)
                y01.append(y[c])
            elif ele >= afternoonbegin:
                x02.append(ele)
                y02.append(y[c])
            c = c + 1

        if alg == 'TVWAP':
            ymax = max(y);
            ymin = min(y)
            x1 = [ele + interval * 0.1 for ele in x]
            y1 = [ele[2] for ele in self.data]
            s = sum(y1)
            y1max = max(y1)
            x2 = [ele + interval * 0.5 for ele in x]
            print(len(x2))
            # y2 = getOrderSize(stock)
            y2 = [ele * s / 10 for ele in y2]
            y1max = max(y1max, max(y2))
        elif alg == 'VWAP':
            ymax = max(y);
            ymin = min(y)
            x1 = [ele + interval * 0.1 for ele in x]
            y1 = [ele[2] for ele in self.data]
            s = sum(y1)
            y1max = max(y1)
            x2 = [ele + interval * 0.5 for ele in x]
            print(len(x2))
            y2 = self.__getOrderSize()
        elif alg == 'TWAP':
            ymax = max(y);
            ymin = min(y)
            x1 = [ele + interval * 0.1 for ele in x]
            y1 = [ele[2] for ele in self.data]
            s = sum(y1)
            y1 = [ele for ele in y1]
            y1max = max(y1)
            x2 = [ele + interval * 0.5 for ele in x]
            print(len(x2))
            y2 = []
            for ele in range(len(y1)):
                y2.append(s / len(y1) / 5)

        # ratio=0.3
        # y2 = [ele*sum(y1)*ratio for ele in y2]
        ax1 = figure1.add_subplot(111)
        ax1.xaxis.set_major_locator(minutes)
        ax1.xaxis.set_major_formatter(minute_formatter)
        plt.ylabel('Volume', fontsize=15)
        plt.ylim([0, y1max * 1.5])
        plt.xlabel('Time', fontsize=15)
        ax2 = ax1.twinx()
        if alg == 'TVWAP':
            bar_history = ax1.bar(x1, y1, width=interval * 0.4, color='c', label='Historical Volume')
        else:
            bar_history = ax1.bar(x1, y1, width=interval * 0.4, color='c', label='Volume')
        bar_order = ax1.bar(x2, y2, width=interval * 0.4, color=[1, 0.4, 0.6], label='Order Size')

        line_price, = ax2.plot(x01, y01, color='b', label='Price')
        ax2.plot(x02, y02, color='b')
        plt.title('%s' % stock.upper(), fontsize=20)
        plt.ylabel('Price', fontsize=15)
        plt.ylim([ymin - 2 * (ymax - ymin), ymax + 0.25 * (ymax - ymin)])
        figure1.autofmt_xdate()
        plt.grid()
        plt.legend(handles=(line_price, bar_history, bar_order), loc='upper right', ncol=3)
        # plt.legend(handles=(bar_history,),bbox_to_anchor=(0.5,-0.25),loc='lower center')
        plt.tight_layout()
        # plt.autoscale(tight=True)
        self.canvas1 = figureCanvas(figure1)
        self.canvas1.draw()
        self.toolbar1 = NavigationToolBar(self.canvas1, self)

        layout = QHBoxLayout(self)
        leftLayout = QVBoxLayout(self)
        rightLayout = QVBoxLayout(self)
        layout.addLayout(leftLayout)
        # layout.addLayout(rightLayout)
        leftLayout.addWidget(self.canvas1)
        leftLayout.addWidget(self.toolbar1)
        # rightLayout.addWidget(self.canvas2)
        # rightLayout.addWidget(self.toolbar2)

    def getSechedule(self,stock_id,alg):
        if(alg=='TWAP'):
            pass
        elif(alg=='VWAP_10_day_train'):
            pass
        elif(alg=='VWAP_5_day_train'):
            pass
        elif(alg=='VWAP_binary'):
            pass
        elif(alg=='VWAP_exp'):
            pass

class cdf_graph(QWidget):
    def __init__(self,parent=None,year=0,month=0,day=0,stock='0'):
        super(cdf_graph,self).__init__(parent)

        interval=5
        self.data=getRealtimeData(year=year,month=month,day=day,stock=stock,interval=interval)
        interval=delta2num(interval)
        figure2 = plt.figure(2)
        x3 = [ele[0] for ele in self.data]
        #y3 = getOrderSize(stock)
        y3=x3
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
    year=2016;month=11;day=11;stock='sh601988'
    app = QApplication(sys.argv)
    ui = console(year=year,month=month,day=day,stock=stock,alg='TWAP')
    #ui2 = cdf_graph(year=year,month=month,day=day,stock=stock)
    ui.setFixedSize(1920,1000)
    ui.move(0,0)
    ui.setWindowTitle('Trade Simulation')
    #ui2.setWindowTitle('Trade Simulation')
    ui.show()
    #ui2.show()
    app.exec_()
