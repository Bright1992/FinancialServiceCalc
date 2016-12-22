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
import Trade as td, HistoricalData as hd
from getRealtimeData import getRealtimeData,delta2num
from Trade import *
import time
from const import *

alldays = DayLocator()
months = MonthLocator()
minutes=MinuteLocator(byminute=range(0,60,5))
minute_formatter = DateFormatter("%H:%M")



def time2sec(time):
    ts=time.split(':')
    #print((int(ts[0])-9)*3600+(int(ts[1])-30)*60+int(ts[2]))
    return (int(ts[0])-9)*3600+(int(ts[1])-30)*60+int(ts[2])

def sec2num(year,month,day,sec):
    h=int(sec)/3600
    m=(int(sec)-h*3600)/60
    s=int(sec)-h*3600-m*60
    h+=START_HOUR
    m+=START_MIN
    h+=(m/60)
    m=m-(m/60)*60
    return date2num(datetime.datetime(year, month, day, h, m, s))

def del2num(second):
    h=second/3600
    m=(second-h*3600)/60
    s=second-h*3600-m*60
    return date2num(datetime.datetime(1, 1, 1, h, m, s)) - 1

class figure(QWidget):
    SCHED_PLOT = 1
    TOTAL_PLOT = 2
    CDF_PLOT = 3
    fig_num=0
    def __init__(self,parent=None,tp=1,trade_interval=60):
        super(figure,self).__init__(parent)
        self.type=tp
        figure.fig_num+=1
        self.fig_num=figure.fig_num
        self.title=''
        self.sid=''
        self.init_figure()
        self.interval=del2num(trade_interval)
        self.canvas1 = figureCanvas(self.figure1)
        self.canvas1.draw()
        self.layout=QHBoxLayout(self)
        self.layout.addWidget(self.canvas1)

    def init_figure(self):
        self.figure1=plt.figure(self.fig_num)
        self.ax1 = self.figure1.add_subplot(111)
        self.ax1.xaxis.set_major_locator(minutes)
        self.ax1.xaxis.set_major_formatter(minute_formatter)
        font = {
            'family': 'serif',
            'color': 'darked',
            'weight': 'normal',
            'size': 16,
        }
        # plt.title("Trade Volume", fontsize=20, family='TimesNewRoman')
        if self.type!=figure.CDF_PLOT:
            self.title="Trade Volume"
            plt.ylabel('Volume', fontsize=15)
            self.y1max = 10
            plt.ylim([0, self.y1max * 1.5])
        else:
            self.title="Procedure"
            plt.ylabel('Percentage',fontsize=15)
            self.y1max = 1
            plt.ylim([0,1])
        # plt.xlim([0,10000])
        plt.xlabel('Time', fontsize=15)
        if self.type!=figure.CDF_PLOT:
            self.ax2 = self.ax1.twinx()
            plt.ylabel("Price", fontsize=15)
        else:
            plt.grid()
        plt.title(self.title,fontsize=20,family="TimesNewRoman")
        # self.figure1 = plt.figure(1)

    def setSid(self,sid):
        self.sid=sid
        # print(self.title+'('+self.sid+')')
        plt.figure(self.fig_num)
        plt.title(self.title+'('+self.sid.toUpper()+')',fontsize=20)
        self.canvas1.draw()

    def setInterval(self,trade_interval):
        self.interval=del2num(trade_interval)

    def update2(self,data,xrange):
        plt.figure(self.fig_num)
        # print(data[2])
        if self.type==figure.SCHED_PLOT:
            # print(data[0])
            # print(data[2])
            self.ax1.xaxis.set_major_locator(minutes)
            self.ax1.xaxis.set_major_formatter(minute_formatter)
            if len(self.ax1.lines)>0:
                self.ax1.lines.pop(0)

            xmax=max(del2num(xrange*60)+data[0][0],data[0][-1])
            xmin=max(data[0][0],data[0][-1]-del2num(xrange*60))
            plt.xlim([xmin-self.interval*0.2,xmax+self.interval*0.2])
            plt.axes(self.ax1)

            x1=[t-self.interval*0.1 for t in data[0]]
            bar_sched = self.ax1.bar(x1, data[1], width=self.interval * 0.2, color=[1, 0.4, 0.6], label='Order Size')
            plt.ylim([0,max(data[1])*1.5])
            plt.axes(self.ax2)
            minp=min(data[2])
            maxp=max(data[2])
            dlt=float(maxp-minp)
            plt.ylim([max(0,minp-3*dlt),maxp+dlt])
            self.ax2.plot(data[0],data[2],color='blue')
            self.figure1.autofmt_xdate()
            # self.figure1.show()
            self.canvas1.draw()
        elif self.type == figure.TOTAL_PLOT:
            # print(data[0])
            # print(data[2])
            self.ax1.xaxis.set_major_locator(minutes)
            self.ax1.xaxis.set_major_formatter(minute_formatter)
            if len(self.ax1.lines) > 0:
                self.ax1.lines.pop(0)

            xmax = max(del2num(xrange * 60) + data[0][0], data[0][-1])
            xmin = max(data[0][0], data[0][-1] - del2num(xrange * 60))
            plt.xlim([xmin - self.interval * 0.2, xmax + self.interval * 0.2])
            plt.axes(self.ax1)

            x1 = [t - self.interval * 0.1 for t in data[0]]
            bar_sched = self.ax1.bar(x1, data[1], width=self.interval * 0.2, color='c', label='Order Size')
            plt.ylim([0, max(data[1]) * 1.5])
            plt.axes(self.ax2)
            minp = min(data[2])
            maxp = max(data[2])
            dlt = float(maxp - minp)
            plt.ylim([max(0, minp - 3 * dlt), maxp + dlt])
            self.ax2.plot(data[0], data[2], color='blue')
            self.figure1.autofmt_xdate()
            # self.figure1.show()
            self.canvas1.draw()

        else:
            self.ax1.xaxis.set_major_locator(minutes)
            self.ax1.xaxis.set_major_formatter(minute_formatter)
            if len(self.ax1.lines) > 0:
                self.ax1.lines.pop(0)
            xmax = max(del2num(xrange * 60) + data[0][0], data[0][-1])
            xmin = max(data[0][0], data[0][-1] - del2num(xrange * 60))
            plt.xlim([xmin - self.interval * 0.2, xmax + self.interval * 0.2])
            plt.ylim([0,1])
            self.ax1.plot(data[0],data[1],color='blue')
            self.figure1.autofmt_xdate()
            # self.figure1.show()
            self.canvas1.draw()

    def clear(self):
        plt.figure(self.fig_num)
        plt.clf()
        self.init_figure()



class console(QWidget):
    def __init__(self,parent=None,stock='0',year=0,month=0,day=0,alg='TVWAP'):
        super(console,self).__init__(parent)
        self.draw_layout()
        algs=['TWAP','VWAP(10 day)','VWAP(5 day)','VWAP(binary)','VWAP(exp)']
        self.set_alg(algs)
        self.interval=50
        self.trade_interval=30
        self.init_canvas()
        self.set_speed_ratio(60)
        self.init_timer(self.interval)

        self.readyFlag=False
        self.runningFlag=False
        self.check_state()

        self.year=1
        self.month=1
        self.day=1

        self.btn_start.clicked.connect(self.onButtonStartClicked)
        self.btn_stop.clicked.connect(self.onButtonStopClicked)
        self.text_sid.textEdited.connect(self.checkReady)
        self.text_ordersize.textEdited.connect(self.checkReady)
        self.text_alg.currentIndexChanged.connect(self.checkReady)

        #debug
        self.text_sid.setText("sh601988")
        self.text_ordersize.setText("2000")
        self.text_alg.setCurrentIndex(2)
        self.readyFlag=True

    def draw_layout(self):
        self.label_sid=QLabel("Stock ID:")
        self.label_volume=QLabel("Volume:")
        self.label_alg=QLabel("Algorithm:")
        self.text_sid=QLineEdit()
        self.text_ordersize=QLineEdit()
        self.text_ordersize.setValidator(QIntValidator(0,1000000))
        self.text_alg=QComboBox()
        self.label_sid.setMinimumWidth(100)
        self.label_volume.setMinimumWidth(100)
        self.label_alg.setMinimumWidth(100)
        self.btn_start=QPushButton("Start")
        self.btn_stop=QPushButton("Stop")
        self.optionLayout=QGridLayout()

        self.hLayout1=QHBoxLayout()
        self.hLayout1.addWidget(self.label_sid)
        self.hLayout1.addWidget(self.text_sid)
        self.hLayout2=QHBoxLayout()
        self.hLayout2.addWidget(self.label_volume)
        self.hLayout2.addWidget(self.text_ordersize)
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
        hline1.setFixedHeight(50)
        self.optionLayout.addWidget(hline1,0,0)
        self.optionLayout.addWidget(hline1,5,0,6,0)

        self.vLayout_summary=QVBoxLayout()

        font=QFont()
        font.setPixelSize(25)
        font.setFamily("TimesNewRoman")
        font.setBold(True)

        self.label_summary=QLabel("Trade Summary")
        self.label_summary.setFont(font)

        self.label_summary.setAlignment(Qt.AlignCenter)
        self.vLayout_summary.addWidget(self.label_summary)

        self.textBsr_summary=QTextBrowser()
        self.vLayout_summary.addWidget(self.textBsr_summary)
        self.textBsr_summary.setFixedHeight(600)
        self.vLayout_summary.addStretch()

        # self.figure1=plt.figure(1)
        # self.canvas_sched = figureCanvas(self.figure1)
        self.canvas_sched=figure(tp=figure.SCHED_PLOT)
        self.canvas_sched.setMaximumHeight(475)
        self.canvas_sched.setFixedWidth(800)

        # self.figure2=plt.figure(2)
        # self.canvas_rt = figureCanvas(self.figure2)
        self.canvas_rt=figure(tp=figure.TOTAL_PLOT)
        self.canvas_rt.setMaximumHeight(475)
        self.canvas_rt.setFixedWidth(800)

        # self.figure3=plt.figure(3)
        # self.canvas_cdf=figureCanvas(self.figure3)
        self.canvas_cdf=figure(tp=figure.CDF_PLOT)
        self.canvas_cdf.setMaximumHeight(475)
        self.canvas_cdf.setFixedWidth(700)

        self.textBsr_rtinfo = QTextBrowser()
        self.textBsr_rtinfo.setFixedHeight(400)
        self.textBsr_rtinfo.setFixedWidth(500)

        self.hLayout5=QHBoxLayout()
        self.hLayout5.addStretch()
        self.hLayout5.addWidget(self.textBsr_rtinfo)
        self.hLayout5.addStretch()

        self.vLayout_rtinfo=QVBoxLayout()
        self.vLayout_rtinfo.setAlignment(Qt.AlignCenter)
        self.vLayout_rtinfo.addStretch()
        self.label_rtinfo=QLabel("Instant Information")
        self.label_rtinfo.setAlignment(Qt.AlignCenter)
        self.label_rtinfo.setFont(font)
        self.vLayout_rtinfo.addWidget(self.label_rtinfo)
        self.vLayout_rtinfo.addLayout(self.hLayout5)
        self.vLayout_rtinfo.addStretch()

        self.mainLayout=QGridLayout()
        self.mainLayout.addLayout(self.optionLayout,0,0)
        self.mainLayout.addLayout(self.vLayout_summary,1,0,4,1)
        self.mainLayout.addWidget(self.canvas_sched,0,1,2,2)
        self.mainLayout.addWidget(self.canvas_cdf,0,3,2,4)
        self.mainLayout.addWidget(self.canvas_rt,2,1,3,2)
        self.mainLayout.addLayout(self.vLayout_rtinfo,2,3,3,4)

        self.vline1=QSplitter()
        self.vline1.setFixedWidth(50)
        self.mhLayout=QHBoxLayout(self)
        self.mhLayout.addWidget(self.vline1)
        self.mhLayout.addLayout(self.mainLayout)

        # self.mainLayout.setMargin(30)
        color=QColor(190,190,190)
        palette = QPalette()
        palette.setColor(QPalette.Window,color)
        self.setPalette(palette)

    def set_alg(self,algs):
        self.text_alg.addItem("Please Select Algorithm")
        for alg in algs:
            self.text_alg.addItem(alg)

    def init_canvas(self):
        self.cur_sched_vol=0
        self.sched_vol=[]
        self.sched_time=[]
        self.sched_price=[]
        self.total_vol=[]
        self.total_price=[]
        self.idx=[0,0,0,0,0,0,0]
        self.cur_sched_vol = 0
        self.cur_sched_price = 0
        self.cur_sched_N = 0
        self.cur_total_vol = 0
        self.cur_total_price = 0
        self.cur_total_N = 0
        self.xrange=self.trade_interval*20/60
        self.total_time = 0
        self.finished = 0
        self.cdf_array=[]

    def check_state(self):
        if self.readyFlag==True and self.runningFlag==False:
            self.btn_start.setEnabled(True)
        else:
            self.btn_start.setEnabled(False)
        if(self.runningFlag==True):
            self.btn_stop.setEnabled(True)
        else:
            self.btn_stop.setEnabled(False)

    def set_speed_ratio(self,ratio):
        self.sec_per_interval=ratio*self.interval/1000.0

    def init_timer(self,interval):
        # interval=50
        self.timer=QTimer()
        self.timer.setInterval(interval)
        self.total_time=0
        # self.timer.start(interval)
        self.timer.timeout.connect(self.updateCanvas)

    @pyqtSlot()
    def onButtonStartClicked(self):
        self.sched_data=None
        self.init_canvas()
        try:
            (self.sched_data,self.total_data,self.trade_date)=self.getSechedule()
        except e:
            print(e)
        i=0
        for x in self.total_data:
            if x[0]<"09:30:00":
                i+=1
            else:
                break
        self.total_data=self.total_data[i:]
        # print(self.sched_data,self.trade_date)
        self.year=int(self.trade_date.year)
        self.month=int(self.trade_date.month)
        self.day=int(self.trade_date.day)
        self.canvas_sched.clear()
        # self.canvas_rt.clear()
        # self.canvas_cdf.clear()
        self.timer.start()
        self.runningFlag=True
        self.check_state()
        self.canvas_sched.setSid(self.sid)
        self.canvas_rt.setSid(self.sid)
        self.canvas_cdf.setSid(self.sid)

    @pyqtSlot()
    def onButtonStopClicked(self):
        # QMessageBox.information(self,"stop",'ok')
        self.timer.stop()
        self.runningFlag=False
        self.check_state()

    @pyqtSlot()
    def checkReady(self):
        self.sid=self.text_sid.text()
        self.ordersize=self.text_ordersize.text()
        self.alg=self.text_alg.currentIndex()
        if len(self.sid)>0 and len(self.ordersize)>0 and self.alg>0:
            self.readyFlag=True
        else:
            self.readyFlag=False
        self.check_state()

    def updateCanvas(self):
        self.total_time+=self.sec_per_interval  #sec_per_interval must be less than trade_interval!!
        if floor(self.total_time/self.trade_interval)>floor((self.total_time-self.sec_per_interval)/self.trade_interval):
            if self.cur_total_N==0:
                if len(self.total_vol)>0:
                    self.cur_total_price=self.total_price[-1]
            else:
                self.cur_total_price/=float(self.cur_total_N)

            if self.cur_sched_N==0:
                if len(self.total_vol)>0:
                    self.cur_sched_price=self.total_price[-1]
                elif len(self.sched_vol)>0:
                    self.cur_sched_price = self.cur_price[-1]
            else:
                self.cur_sched_price/=float(self.cur_sched_N)

            if self.cur_total_price>10:
                pass

            self.sched_vol.append(self.cur_sched_vol)
            self.sched_time.append(sec2num(self.year,
                                           self.month,
                                           self.day,
                                           floor(float(self.total_time)/self.trade_interval)*self.trade_interval))
            self.sched_price.append(self.cur_sched_price)
            self.total_vol.append(self.cur_total_vol)
            self.total_price.append(self.cur_total_price)
            self.finished += self.sched_vol[-1]
            self.cdf_array.append(self.finished/int(self.ordersize))

            self.canvas_sched.update2([self.sched_time,self.sched_vol,self.sched_price],self.xrange)
            self.canvas_rt.update2([self.sched_time,self.total_vol,self.sched_price],self.xrange)
            self.canvas_cdf.update2([self.sched_time,self.cdf_array],self.xrange*10)
            
            self.cur_sched_vol=0
            self.cur_sched_price=0
            self.cur_sched_N=0
            self.cur_total_N=0
            self.cur_total_vol=0
            self.cur_total_price=0


        while self.idx[0]<len(self.sched_data) and time2sec(self.sched_data[self.idx[0]][0])<=self.total_time:
            self.cur_sched_vol+=float(self.sched_data[self.idx[0]][2])
            self.idx[0]+=1
            self.cur_sched_N+=float(self.sched_data[self.idx[0]][2])
            self.cur_sched_price+=float(self.sched_data[self.idx[0]][1])*float(self.sched_data[self.idx[0]][2])

        while self.idx[1] < len(self.total_data) and time2sec(self.total_data[self.idx[1]][0]) <= self.total_time:
            self.cur_total_vol+=float(self.total_data[self.idx[1]][2])
            self.idx[1]+=1
            self.cur_total_N+=float(self.total_data[self.idx[1]][2])
            self.cur_total_price+=float(self.total_data[self.idx[1]][1])*float(self.total_data[self.idx[1]][2])

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
            #print(len(x2))
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
            #print(len(x2))
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
            #print(len(x2))
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

    def getSechedule(self):
        self.trade_data=hd.updateStock(self.sid)
        self.trade_style=0  #not implemented yet
        return td.tradeStock(self.sid,int(self.ordersize),self.trade_style,self.alg)

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
    # print(del2num(1))
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
