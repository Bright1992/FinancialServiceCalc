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
    def __init__(self,parent=None,stock='0',year=0,month=0,day=0,alg='TVWAP'):
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

        if alg=='TVWAP':
            ymax=max(y);ymin=min(y)
            x1 = [ele+interval*0.1 for ele in x]
            y1 = [ele[2] for ele in self.data]
            s=sum(y1)
            y1max=max(y1)
            x2 = [ele+interval*0.5 for ele in x]
            print(len(x2))
            y2 = getOrderSize(stock)
            y2 = [ele*s/10 for ele in y2]
            y1max=max(y1max,max(y2))
        elif alg=='VWAP':
            ymax=max(y);ymin=min(y)
            x1 = [ele+interval*0.1 for ele in x]
            y1 = [ele[2] for ele in self.data]
            s=sum(y1)
            y1max=max(y1)
            x2 = [ele+interval*0.5 for ele in x]
            print(len(x2))
            y2 = self.__getOrderSize()
        elif alg=='TWAP':
            ymax=max(y);ymin=min(y)
            x1 = [ele+interval*0.1 for ele in x]
            y1 = [ele[2] for ele in self.data]
            s=sum(y1)
            y1=[ele for ele in y1]
            y1max=max(y1)
            x2 = [ele+interval*0.5 for ele in x]
            print(len(x2))
            y2 = []
            for ele in range(len(y1)):
                y2.append(s/len(y1)/5)

        #ratio=0.3
        #y2 = [ele*sum(y1)*ratio for ele in y2]
        ax1=figure1.add_subplot(111)
        # ax1.xaxis.set_major_locator(minutes)
        # ax1.xaxis.set_major_formatter(minute_formatter)
        plt.ylabel('Volume',fontsize=15)
        plt.ylim([0,y1max*1.5])
        plt.xlabel('Time',fontsize=15)
        ax2=ax1.twinx()
        # if alg=='TVWAP':
        #     bar_history=ax1.bar(x1,y1,width=interval*0.4,color='c',label='Historical Volume')
        # else:
        #     bar_history=ax1.bar(x1,y1,width=interval*0.4,color='c',label='Volume')
        # bar_order=ax1.bar(x2,y2,width=interval*0.4,color=[1,0.4,0.6],label='Order Size')

        x01=[736321.3958912037, 736321.3959606482, 736321.3959953703, 736321.3961342593, 736321.3962037037, 736321.3962731481, 736321.3964120371, 736321.3964814815, 736321.3965509259, 736321.3965856482, 736321.3966898149, 736321.3967592593, 736321.3969328704, 736321.3971759259, 736321.3973842593, 736321.3974537037, 736321.397488426, 736321.3975578704, 736321.397662037, 736321.3977314815, 736321.3977662037, 736321.3979398148, 736321.3993634259, 736321.399675926, 736321.3997106481, 736321.3998148148, 736321.3999189815, 736321.3999884259, 736321.4000578703, 736321.4000925926, 736321.4002662037, 736321.4003703704, 736321.4005439815, 736321.4006134259, 736321.400787037, 736321.4008217592, 736321.4008912037, 736321.4010300926, 736321.4011689815, 736321.4012731481, 736321.4013078704, 736321.4013773148, 736321.4014814815, 736321.4015162037, 736321.4015509259, 736321.4015856482, 736321.401863426, 736321.4019675925, 736321.4027893519, 736321.402962963, 736321.4031018518, 736321.4031712963, 736321.4032407408, 736321.4033101852, 736321.4033796296, 736321.403587963, 736321.4036226852, 736321.4036921297, 736321.4037615741, 736321.4040046296, 736321.404212963, 736321.4044212963, 736321.4044560185, 736321.4044907407, 736321.404525463, 736321.4046990741, 736321.4047337963, 736321.4065162037, 736321.406724537, 736321.4068981481, 736321.4069328704, 736321.4069675925, 736321.4070023148, 736321.4070370371, 736321.4071412038, 736321.4098148148, 736321.4099189815, 736321.4099537038, 736321.4099884259, 736321.4134953704, 736321.413599537, 736321.4136689815, 736321.4141203704, 736321.4142245371, 736321.4142939815, 736321.4143287037, 736321.4143981482, 736321.4145717593, 736321.414675926, 736321.4147453704, 736321.4150578703, 736321.4152546297, 736321.415300926, 736321.4153587963, 736321.4155671296, 736321.415636574, 736321.4157060186, 736321.4160185185, 736321.4160879629, 736321.4168171296, 736321.4168865741, 736321.417199074, 736321.4176851852, 736321.4177893519, 736321.4178587963, 736321.4182060185, 736321.4182407408, 736321.4185532407, 736321.4168171296, 736321.4168865741, 736321.417199074, 736321.4176851852, 736321.4177893519, 736321.4178587963, 736321.4182060185, 736321.4182407408, 736321.4185532407, 736321.4187268518, 736321.4187962963, 736321.4189699074, 736321.4190509259, 736321.4190856481, 736321.4191898148, 736321.4192939815, 736321.4193634259, 736321.4193981482, 736321.4194328703, 736321.419537037, 736321.4195717593, 736321.4196412037, 736321.4197106481, 736321.4198842592, 736321.4199189815]
        y01=[0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.02, 0.021, 0.0215, 0.023, 0.0245, 0.026, 0.0275, 0.029, 0.0305, 0.032, 0.0335, 0.035, 0.0365, 0.038, 0.0395, 0.041, 0.0425, 0.044, 0.0455, 0.047, 0.0485, 0.05, 0.0515, 0.053, 0.0545, 0.056, 0.0575, 0.059, 0.06, 0.0605, 0.061, 0.0615, 0.062, 0.0625, 0.063, 0.0635, 0.064, 0.0645, 0.065, 0.0655, 0.066, 0.0665, 0.067, 0.0675, 0.068, 0.0685, 0.069, 0.0695, 0.07, 0.0705, 0.071, 0.0715, 0.072, 0.0725, 0.073, 0.0735, 0.074, 0.0745, 0.075, 0.0755, 0.0775, 0.0795, 0.0815, 0.0835, 0.0855, 0.0875, 0.0895, 0.0915, 0.0935, 0.0955, 0.0975, 0.0995, 0.1015, 0.1035, 0.1055, 0.1075, 0.1095, 0.1115, 0.1135, 0.1155, 0.1175, 0.1195, 0.1215, 0.1235, 0.1255, 0.1275, 0.1295, 0.1315, 0.1325, 0.135, 0.1375, 0.14, 0.1425, 0.145, 0.1475, 0.15, 0.1525, 0.155, 0.1575, 0.16, 0.1625, 0.165, 0.1675, 0.17, 0.1725, 0.175, 0.1775, 0.18, 0.1825, 0.185, 0.1875, 0.19, 0.1925, 0.195]



        line_price,=ax2.plot(x01,y01,color='b',label='Price')
        # ax2.plot(x02,y02,color='b')
        plt.title('%s'%stock.upper(),fontsize=20)
        plt.ylabel('Price',fontsize=15)
        plt.ylim([ymin-2*(ymax-ymin),ymax+0.25*(ymax-ymin)])
        # figure1.autofmt_xdate()
        plt.grid()
        # plt.legend(handles=(line_price,bar_history,bar_order),loc='upper right',ncol=3)
        #plt.legend(handles=(bar_history,),bbox_to_anchor=(0.5,-0.25),loc='lower center')
        plt.tight_layout()
        plt.autoscale(tight=True)
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
        y3=[ele[2]/10 for ele in self.data]
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
    ui = graph(year=year,month=month,day=day,stock=stock,alg='TWAP')
    ui2 = cdf_graph(year=year,month=month,day=day,stock=stock)
    ui.resize(1500,800)
    ui.setWindowTitle('Trade Simulation')
    ui2.setWindowTitle('Trade Simulation')
    ui.show()
    ui2.show()
    app.exec_()
