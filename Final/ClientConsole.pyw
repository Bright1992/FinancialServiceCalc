# _*_coding:utf-8_*_

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as figureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolBar
# import matplotlib.animation as animation
from matplotlib.dates import date2num, num2date
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.dates import DayLocator, MinuteLocator, SecondLocator
from matplotlib.dates import MonthLocator

import Trade as td, HistoricalData as hd
from Trade import *
from const import *

alldays = DayLocator()
months = MonthLocator()
minutes = MinuteLocator(byminute=range(0, 60, 5))
minute_formatter = DateFormatter("%H:%M")


def time2sec(time):
    ts = time.split(':')
    # print((int(ts[0])-9)*3600+(int(ts[1])-30)*60+int(ts[2]))
    return (int(ts[0]) - 9) * 3600 + (int(ts[1]) - 30) * 60 + int(ts[2])


def sec2num(year, month, day, sec):
    h = int(sec) / 3600
    m = (int(sec) - h * 3600) / 60
    s = int(sec) - h * 3600 - m * 60
    h += START_HOUR
    m += START_MIN
    h += (m / 60)
    m = m - (m / 60) * 60
    return date2num(datetime.datetime(year, month, day, h, m, s))


def del2num(second):
    h = second / 3600
    m = (second - h * 3600) / 60
    s = second - h * 3600 - m * 60
    return date2num(datetime.datetime(1, 1, 1, h, m, s)) - 1


class figure(QWidget):
    SCHED_PLOT = 1
    TOTAL_PLOT = 2
    CDF_PLOT = 3
    fig_num = 0

    def __init__(self, parent=None, tp=1, trade_interval=60):
        super(figure, self).__init__(parent)
        self.type = tp
        figure.fig_num += 1
        self.fig_num = figure.fig_num
        self.title = ''
        self.sid = ''
        self.init_figure()
        self.interval = del2num(trade_interval)
        self.canvas1 = figureCanvas(self.figure1)
        self.canvas1.draw()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.canvas1)
        if self.type != figure.CDF_PLOT:
            if trade_interval < 60:
                self.xlocater = SecondLocator(bysecond=range(0, 60, trade_interval))
                self.xformatter = DateFormatter("%H:%M:%S")
            else:
                self.xlocater = MinuteLocator(byminute=range(0, 60, trade_interval / 60))
                self.xformatter = DateFormatter("%H:%M")
        else:
            if trade_interval < 5:
                self.xlocater = SecondLocator(bysecond=range(0, 60, 12 * trade_interval))
                self.xformatter = DateFormatter("%H:%M:%S")
            else:
                self.xlocater = MinuteLocator(byminute=range(0, 60, trade_interval / 5))
                self.xformatter = DateFormatter("%H:%M")

    def init_figure(self):
        self.figure1 = plt.figure(self.fig_num)
        self.ax1 = self.figure1.add_subplot(111)
        self.ax1.xaxis.set_major_locator(minutes)
        self.ax1.xaxis.set_major_formatter(minute_formatter)

        if self.type != figure.CDF_PLOT:
            if self.type == figure.SCHED_PLOT:
                self.title = "Order Volume"
            else:
                self.title = "Total Order Volume"
            plt.ylabel('Volume', fontsize=15)
            self.y1max = 10
            plt.ylim([0, self.y1max * 1.5])
        else:
            self.title = "Completion Percentage"
            plt.ylabel('Percentage', fontsize=15)
            self.y1max = 1
            plt.ylim([0, 1])
        # plt.xlim([0,10000])
        plt.xlabel('Time', fontsize=15)
        if self.type != figure.CDF_PLOT:
            self.ax2 = self.ax1.twinx()
            plt.ylabel("Price", fontsize=15)
        else:
            plt.grid()
        plt.title(self.title, fontsize=20)
        # self.figure1 = plt.figure(1)

    def setSid(self, sid):
        self.sid = sid
        # print(self.title+'('+self.sid+')')
        plt.figure(self.fig_num)
        plt.title(self.title + '(' + self.sid.toUpper() + ')', fontsize=20)
        self.canvas1.draw()

    def setInterval(self, trade_interval):
        self.interval = del2num(trade_interval)

    def update2(self, data, xrange):
        plt.figure(self.fig_num)
        self.ax1.clear()
        self.xlocater=MinuteLocator(byminute=range(0,60,int(ceil(float(xrange)/20))))
        self.xformatter=DateFormatter("%H:%M")
        if self.type != figure.CDF_PLOT:
            self.ax2.clear()
        if self.type == figure.SCHED_PLOT:
            plt.title(self.title + '(' + self.sid.toUpper() + ')', fontsize=20)
            xmax = max(del2num(xrange * 60) + data[0][0], data[0][-1])
            xmin = max(data[0][0], data[0][-1] - del2num(xrange * 60))
            plt.xlim([xmin - self.interval * 0.2, xmax + self.interval * 0.2])
            self.ax1.xaxis.set_major_locator(self.xlocater)
            self.ax1.xaxis.set_major_formatter(self.xformatter)

            plt.axes(self.ax1)
            x1 = data[0]
            plt.xlabel('Time', fontsize=15)
            bar_order = self.ax1.bar(x1, data[1], width=self.interval * 0.5, color=[1, 0.4, 0.6], label='Order Size',
                                     align='center')
            plt.ylabel('Volume', fontsize=15)
            plt.ylim([0, max(data[1]) * 1.5])
            plt.axes(self.ax2)
            plt.ylabel('Price', fontsize=15)
            minp = min(data[2])
            maxp = max(data[2])
            dlt = float(maxp - minp)
            plt.ylim([max(0, minp - 3 * dlt - 0.1), maxp + dlt + 0.1])
            line_price, = self.ax2.plot(data[0], data[2], color='blue', label='Price')
            self.figure1.autofmt_xdate()
            plt.legend(handles=(line_price, bar_order), loc='upper right', ncol=3)
            self.canvas1.draw()
        elif self.type == figure.TOTAL_PLOT:
            plt.title(self.title + '(' + self.sid.toUpper() + ')', fontsize=20)
            xmax = max(del2num(xrange * 60) + data[0][0], data[0][-1])
            xmin = max(data[0][0], data[0][-1] - del2num(xrange * 60))
            plt.xlim([xmin - self.interval * 0.2, xmax + self.interval * 0.2])
            plt.axes(self.ax1)
            plt.ylabel('Volume', fontsize=15)

            self.ax1.xaxis.set_major_locator(self.xlocater)
            self.ax1.xaxis.set_major_formatter(self.xformatter)
            plt.xlabel('Time', fontsize=15)

            x1 = data[0]
            bar_total = self.ax1.bar(x1, data[1], width=self.interval * 0.5, color='c', label='Order Size',
                                     align='center')
            plt.ylim([0, max(data[1]) * 1.5])
            plt.axes(self.ax2)
            plt.ylabel('Price', fontsize=15)
            minp = min(data[2])
            maxp = max(data[2])
            dlt = float(maxp - minp)
            plt.ylim([max(0, minp - 3 * dlt - 0.1), maxp + dlt + 0.1])
            line_price, = self.ax2.plot(data[0], data[2], color='blue', label='Price')
            self.figure1.autofmt_xdate()
            plt.legend(handles=(line_price, bar_total), loc='upper right', ncol=3)
            # self.figure1.show()
            self.canvas1.draw()
        else:
            plt.title(self.title + '(' + self.sid.toUpper() + ')', fontsize=20)
            plt.ylabel('Percentage', fontsize=15)
            plt.xlabel('Time', fontsize=15)
            plt.grid()
            self.ax1.xaxis.set_major_locator(self.xlocater)
            self.ax1.xaxis.set_major_formatter(self.xformatter)
            xmax = max(del2num(xrange * 60) + data[0][0],data[0][-1])
            xmin = data[0][0]
            plt.xlim([xmin - self.interval * 0.2, xmax + self.interval * 0.2])
            plt.ylim([0, 1])
            self.ax1.plot(data[0], data[1], color='blue')
            self.figure1.autofmt_xdate()
            self.canvas1.draw()

    def clear(self):
        plt.figure(self.fig_num)
        plt.clf()
        self.init_figure()


class backend_caller(QObject):
    def __init__(self, parent=None):
        super(backend_caller, self).__init__(parent)

    @pyqtSlot(figure, list, int)
    def plotFunc(self, fig, data, xrange):
        print(xrange)
        fig.update2(data, xrange)
        if len(data)==4:
            self.orderFinished.emit()

    @pyqtSlot(figure)
    def clearFig(self, fig):
        fig.clear()

    @pyqtSlot(str, int, int)
    def getSchedule(self, sid, ordersize, alg):
        if hd.updateStock(str(sid)) != 0:
            self.sidNotExsist.emit()
            return

        trade_style = 0  # not implemented yet
        self.schedPrepared.emit(td.tradeStock(sid, int(ordersize), trade_style, alg))

    schedPrepared = pyqtSignal(tuple)
    sidNotExsist = pyqtSignal()
    orderFinished = pyqtSignal()


class backend_thread(QThread):
    def __init__(self, parent=None):
        super(backend_thread, self).__init__(parent)

    def __del__(self):
        pass


class console(QMainWindow):
    STOPPED=1
    FINISHED=2
    server = backend_caller()
    def __init__(self, parent=None):
        super(console, self).__init__(parent)
        self.interval = 50
        self.trade_interval = 60
        self.set_speed_ratio(60)
        self.draw_layout()
        self.algs = ['TWAP', 'VWAP(10 day)', 'VWAP(5 day)', 'VWAP(binary)', 'VWAP(exp)']
        self.set_alg(self.algs)
        self.init_param()
        self.init_timer(self.interval)

        self.readyFlag = False
        self.runningFlag = False
        self.check_state()

        self.year = 1
        self.month = 1
        self.day = 1

        self.btn_start.clicked.connect(self.onButtonStartClicked)
        self.btn_stop.clicked.connect(self.onButtonStopClicked)
        self.text_sid.textEdited.connect(self.checkReady)
        self.text_ordersize.textEdited.connect(self.checkReady)
        self.text_alg.currentIndexChanged.connect(self.checkReady)
        self.server_thread = backend_thread()
        console.server.moveToThread(self.server_thread)
        self.plotReq.connect(console.server.plotFunc)
        self.getSchedReq.connect(console.server.getSchedule)
        console.server.schedPrepared.connect(self.onSchedPrepared)
        console.server.sidNotExsist.connect(self.onSidNotExsist)
        console.server.orderFinished.connect(self.showFinMessage)

        # debug
        self.text_sid.setText("sh601988")
        self.text_ordersize.setText("2000")
        self.text_alg.setCurrentIndex(2)
        self.readyFlag = True

    def init_tbview(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderItem(0, QStandardItem("Time"))
        self.model.setHorizontalHeaderItem(1, QStandardItem("Volume"))
        self.model.setHorizontalHeaderItem(2, QStandardItem("Share"))
        self.model.setHorizontalHeaderItem(3, QStandardItem("Price"))
        self.model.setHorizontalHeaderItem(4, QStandardItem("Total Value"))
        self.model.setHorizontalHeaderItem(5, QStandardItem("Finished"))
        self.tbView_rtinfo = QTableView()
        self.tbView_rtinfo.setFixedHeight(400)
        self.tbView_rtinfo.setFixedWidth(550)
        self.tbView_rtinfo.setShowGrid(True)
        self.tbView_rtinfo.setModel(self.model)
        self.tbView_rtinfo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbView_rtinfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.model.resizeColumnsToContents()
        self.tbView_rtinfo.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

    def draw_layout(self):
        self.label_sid = QLabel("Stock ID:")
        self.label_volume = QLabel("Volume:")
        self.label_alg = QLabel("Algorithm:")
        self.text_sid = QLineEdit()
        self.text_ordersize = QLineEdit()
        self.text_ordersize.setValidator(QIntValidator(0, 1000000))
        self.text_alg = QComboBox()
        self.label_sid.setMinimumWidth(100)
        self.label_volume.setMinimumWidth(100)
        self.label_alg.setMinimumWidth(100)
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.optionLayout = QGridLayout()

        self.hLayout1 = QHBoxLayout()
        self.hLayout1.addWidget(self.label_sid)
        self.hLayout1.addWidget(self.text_sid)
        self.hLayout2 = QHBoxLayout()
        self.hLayout2.addWidget(self.label_volume)
        self.hLayout2.addWidget(self.text_ordersize)
        self.hLayout3 = QHBoxLayout()
        self.hLayout3.addWidget(self.label_alg)
        self.hLayout3.addWidget(self.text_alg)
        self.hLayout4 = QHBoxLayout()
        self.hLayout4.addWidget(self.btn_start)
        self.hLayout4.addWidget(self.btn_stop)

        self.hLayout1.addStretch()
        self.hLayout2.addStretch()
        self.hLayout3.addStretch()
        self.hLayout4.addStretch()

        self.optionLayout.addLayout(self.hLayout1, 1, 0)
        self.optionLayout.addLayout(self.hLayout2, 2, 0)
        self.optionLayout.addLayout(self.hLayout3, 3, 0)
        self.optionLayout.addLayout(self.hLayout4, 4, 0)

        hline1 = QSplitter()
        hline1.setFixedHeight(50)
        self.optionLayout.addWidget(hline1, 0, 0)
        self.optionLayout.addWidget(hline1, 5, 0, 6, 0)

        self.vLayout_summary = QVBoxLayout()

        font = QFont()
        font.setPixelSize(25)
        font.setFamily("TimesNewRoman")
        font.setBold(True)

        self.label_summary = QLabel("Trade Summary")
        self.label_summary.setFont(font)

        self.label_summary.setAlignment(Qt.AlignCenter)
        self.vLayout_summary.addWidget(self.label_summary)

        self.textBsr_summary = QTextBrowser()
        self.vLayout_summary.addWidget(self.textBsr_summary)
        self.textBsr_summary.setFixedHeight(600)
        self.vLayout_summary.addStretch()

        # self.figure1=plt.figure(1)
        # self.canvas_sched = figureCanvas(self.figure1)
        self.canvas_sched = figure(tp=figure.SCHED_PLOT, trade_interval=self.trade_interval)
        self.canvas_sched.setMaximumHeight(475)
        self.canvas_sched.setFixedWidth(800)

        # self.figure2=plt.figure(2)
        # self.canvas_rt = figureCanvas(self.figure2)
        self.canvas_rt = figure(tp=figure.TOTAL_PLOT, trade_interval=self.trade_interval)
        self.canvas_rt.setMaximumHeight(475)
        self.canvas_rt.setFixedWidth(800)

        # self.figure3=plt.figure(3)
        # self.canvas_cdf=figureCanvas(self.figure3)
        self.canvas_cdf = figure(tp=figure.CDF_PLOT, trade_interval=self.trade_interval)
        self.canvas_cdf.setMaximumHeight(475)
        self.canvas_cdf.setFixedWidth(700)

        self.init_tbview()

        self.hLayout5 = QHBoxLayout()
        self.hLayout5.addStretch()
        self.hLayout5.addWidget(self.tbView_rtinfo)
        self.hLayout5.addStretch()

        self.vLayout_rtinfo = QVBoxLayout()
        self.vLayout_rtinfo.setAlignment(Qt.AlignCenter)
        self.vLayout_rtinfo.addStretch()
        self.label_rtinfo = QLabel("Order Information")
        self.label_rtinfo.setAlignment(Qt.AlignCenter)
        self.label_rtinfo.setFont(font)
        self.vLayout_rtinfo.addWidget(self.label_rtinfo)
        self.vLayout_rtinfo.addLayout(self.hLayout5)
        self.vLayout_rtinfo.addStretch()

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.optionLayout, 0, 0)
        self.mainLayout.addLayout(self.vLayout_summary, 1, 0, 4, 1)
        self.mainLayout.addWidget(self.canvas_sched, 0, 1, 2, 2)
        self.mainLayout.addWidget(self.canvas_cdf, 0, 3, 2, 4)
        self.mainLayout.addWidget(self.canvas_rt, 2, 1, 3, 2)
        self.mainLayout.addLayout(self.vLayout_rtinfo, 2, 3, 3, 4)

        self.vline1 = QSplitter()
        self.vline1.setFixedWidth(50)
        self.mhLayout = QHBoxLayout()

        cWidget = QWidget()
        cWidget.setLayout(self.mhLayout)
        # self.setLayout(self.mhLayout)
        self.setCentralWidget(cWidget)
        self.mhLayout.addWidget(self.vline1)
        self.mhLayout.addLayout(self.mainLayout)

        # self.mainLayout.setMargin(30)
        color = QColor(190, 190, 190)
        palette = QPalette()
        palette.setColor(QPalette.Window, color)
        # palette.setColor(QPalette.Text,color)
        self.setPalette(palette)

    def set_alg(self, algs):
        self.text_alg.addItem("Please Select Algorithm")
        for alg in algs:
            self.text_alg.addItem(alg)

    def init_param(self):
        # self.connect(self,SIGNAL("plotReq()"),self.server_thread,SLOT("plotFunc()"))
        self.cur_sched_vol = 0
        self.sched_vol = []
        self.sched_time = []
        self.sched_price = []
        self.total_vol = []
        self.total_price = []
        self.idx = [0, 0, 0, 0, 0, 0, 0]
        self.cur_sched_vol = 0
        self.cur_sched_price = 0
        self.cur_sched_N = 0
        self.cur_total_vol = 0
        self.cur_total_price = 0
        self.cur_total_N = 0
        self.xrange = self.trade_interval * 20 / 60
        self.total_time = 0
        self.finished = 0
        self.cdf_array = []
        self.cdf_time = []
        self.total_value = 0
        self.issue_num = 0
        self.model.removeRows(0, self.model.rowCount())

    def init_canvas(self):
        self.canvas_sched.clear()
        self.canvas_rt.clear()
        self.canvas_cdf.clear()

    def check_state(self):
        if self.readyFlag == True and self.runningFlag == False:
            self.btn_start.setEnabled(True)
        else:
            self.btn_start.setEnabled(False)
        if (self.runningFlag == True):
            self.btn_stop.setEnabled(True)
            self.text_alg.setEnabled(False)
            self.text_sid.setEnabled(False)
            self.text_ordersize.setEnabled(False)
        else:
            self.btn_stop.setEnabled(False)
            self.text_alg.setEnabled(True)
            self.text_sid.setEnabled(True)
            self.text_ordersize.setEnabled(True)

    def set_speed_ratio(self, ratio):
        self.sec_per_interval = ratio * self.interval / 1000.0

    def init_timer(self, interval):
        # interval=50
        self.timer = QTimer()
        self.timer.setInterval(interval)
        self.total_time = 0
        # self.timer.start(interval)
        self.timer.timeout.connect(self.updateCanvas)

    @pyqtSlot()
    def onButtonStartClicked(self):
        if not os.path.exists("txtfile"):
            os.mkdir("txtfile")
        if not os.path.exists("volumefile"):
            os.mkdir("volumefile")
        if not os.path.exists("train_volumefile_line"):
            os.mkdir("train_volumefile_line")
        self.textBsr_summary.setText("")
        self.sched_data = None
        self.init_param()
        self.server_thread.start()
        self.init_canvas()
        self.getSchedReq.emit(str(self.sid), int(self.ordersize), self.alg)
        self.total_data = None
        self.runningFlag = True
        self.check_state()
        self.btn_stop.setEnabled(False)
        self.statusBar().showMessage("The Schedule is Being Preparing...")

    @pyqtSlot()
    def onButtonStopClicked(self):
        self.timer.stop()
        xrange2 = self.sched_time[-1] - self.sched_time[0] + self.trade_interval / 3600.0 / 24
        xrange2 = xrange2 * 24 * 60
        sched_data = [self.sched_time, self.sched_vol, self.sched_price]
        total_data = [self.sched_time, self.total_vol, self.sched_price]
        cdf_data = [self.sched_time, self.cdf_array, 0, 0]
        self.plotReq.emit(self.canvas_sched, sched_data, xrange2)
        self.plotReq.emit(self.canvas_rt, total_data, xrange2)
        self.plotReq.emit(self.canvas_cdf, cdf_data, xrange2)
        self.runningFlag = False
        self.check_state()
        self.state = console.STOPPED

    @pyqtSlot()
    def checkReady(self):
        self.sid = self.text_sid.text()
        self.ordersize = self.text_ordersize.text()
        self.alg = self.text_alg.currentIndex()
        if len(self.sid) > 0 and len(self.ordersize) > 0 and self.alg > 0:
            self.readyFlag = True
        else:
            self.readyFlag = False
        self.check_state()

    def updateCanvas(self):
        if self.idx[0] >= len(self.sched_data):
            print("No Schedule Issued")
            return
        if self.idx[1] >= len(self.total_data):
            print("No Trading Data")
            return
        self.total_time += self.sec_per_interval  # sec_per_interval must be less than trade_interval!!
        if floor(self.total_time / self.trade_interval) > floor(
                        (self.total_time - self.sec_per_interval) / self.trade_interval):
            if self.cur_total_N == 0:
                if len(self.total_vol) > 0:
                    self.cur_total_price = self.total_price[-1]
            else:
                self.cur_total_price /= float(self.cur_total_N)

            if self.cur_sched_N == 0:
                if len(self.total_vol) > 0:
                    self.cur_sched_price = self.total_price[-1]
                elif len(self.sched_vol) > 0:
                    self.cur_sched_price = self.cur_price[-1]
            else:
                self.cur_sched_price /= float(self.cur_sched_N)

            if self.cur_total_price > 10:
                pass

            self.sched_vol.append(self.cur_sched_vol)
            self.sched_time.append(sec2num(self.year,
                                           self.month,
                                           self.day,
                                           floor(float(self.total_time) / self.trade_interval) * self.trade_interval))
            self.sched_price.append(self.cur_sched_price)
            self.total_vol.append(self.cur_total_vol)
            self.total_price.append(self.cur_total_price)
            self.cdf_array.append(self.finished / float(self.ordersize))

            sched_data = [self.sched_time, self.sched_vol, self.sched_price]
            sched_data_s = [d[max(0, len(d) - self.xrange * 60 / self.canvas_sched.interval):] for d in sched_data]
            total_data = [self.sched_time, self.total_vol, self.sched_price]
            total_data_s = [d[max(0, len(d) - self.xrange * 60 / self.canvas_rt.interval):] for d in total_data]
            cdf_data = [self.sched_time, self.cdf_array]
            cdf_data_s = [d[max(0, len(d) - self.xrange * 10 * 60 / self.canvas_cdf.interval):] for d in cdf_data]

            # emit signals
            self.plotReq.emit(self.canvas_sched, sched_data_s, self.xrange)
            self.plotReq.emit(self.canvas_rt, total_data_s, self.xrange)
            self.plotReq.emit(self.canvas_cdf, cdf_data_s, self.xrange * 10)

            self.cur_sched_vol = 0
            self.cur_sched_price = 0
            self.cur_sched_N = 0
            self.cur_total_N = 0
            self.cur_total_vol = 0
            self.cur_total_price = 0

        # if
        while self.idx[0] < len(self.sched_data) and time2sec(self.sched_data[self.idx[0]][0]) <= self.total_time:
            self.cur_sched_vol += float(self.sched_data[self.idx[0]][2])
            self.cur_sched_N += float(self.sched_data[self.idx[0]][2])
            self.cur_sched_price += float(self.sched_data[self.idx[0]][1]) * float(self.sched_data[self.idx[0]][2])
            # self.cdf_time.append(sec2num(self.year,
            #                              self.month,
            #                              self.day,
            #                              time2sec(self.sched_data[self.idx[0]][0])))
            # print([str(num2date(x)) for x in self.cdf_time],len(self.cdf_time),'N')
            self.finished += float(self.sched_data[self.idx[0]][2])
            # self.cdf_array.append(self.finished / int(self.ordersize))
            # t1=time.time()

            # #emit signal
            # self.plotReq.emit(self.canvas_cdf,[self.cdf_time,self.cdf_array],self.xrange*10)

            if self.finished >= float(self.ordersize):
                self.onOrderFinished()
            self.total_value += SHARE_PER_VOLUME * float(self.sched_data[self.idx[0]][1]) * float(
                self.sched_data[self.idx[0]][2])
            self.update_tbview()
            self.idx[0] += 1

        while self.idx[1] < len(self.total_data) and time2sec(self.total_data[self.idx[1]][0]) <= self.total_time:
            self.cur_total_vol += float(self.total_data[self.idx[1]][2])
            self.cur_total_N += float(self.total_data[self.idx[1]][2])
            self.cur_total_price += float(self.total_data[self.idx[1]][1]) * float(self.total_data[self.idx[1]][2])
            self.idx[1] += 1

    # define signals
    # @pyqtSignal(figure,list,int)
    plotReq = pyqtSignal(figure, list, int)
    getSchedReq = pyqtSignal(str, int, int)

    @pyqtSlot(list)
    def onSchedPrepared(self, sched_data):
        (self.sched_data, self.total_data, self.trade_date,self.WAP) = sched_data
        i = 0
        for x in self.total_data:
            if x[0] < "09:30:00":
                i += 1
            else:
                break
        self.total_data = self.total_data[i:]
        # print(self.sched_data,self.trade_date)
        self.year = int(self.trade_date.year)
        self.month = int(self.trade_date.month)
        self.day = int(self.trade_date.day)
        self.canvas_sched.setSid(self.sid)
        self.canvas_rt.setSid(self.sid)
        self.canvas_cdf.setSid(self.sid)
        self.timer.start()
        self.btn_stop.setEnabled(True)
        self.statusBar().showMessage("Trade Is Being Performed")

    @pyqtSlot()
    def onSidNotExsist(self):
        QMessageBox.warning(self, "Warning", "Stock ID Not Exsist!")
        self.runningFlag = False
        self.check_state()

    @pyqtSlot()
    def onOrderFinished(self):
        self.timer.stop()
        xrange2 = self.sched_time[-1] - self.sched_time[0] + self.trade_interval / 3600.0 / 24
        xrange2 = xrange2 * 24 * 60
        sched_data = [self.sched_time, self.sched_vol, self.sched_price]
        total_data = [self.sched_time, self.total_vol, self.sched_price]
        cdf_data = [self.sched_time, self.cdf_array, 0, 0]
        self.plotReq.emit(self.canvas_sched, sched_data, xrange2)
        self.plotReq.emit(self.canvas_rt, total_data, xrange2)
        self.plotReq.emit(self.canvas_cdf, cdf_data, xrange2)
        self.runningFlag = False
        self.check_state()
        self.state = console.FINISHED

    @pyqtSlot()
    def showFinMessage(self):
        if self.state==console.STOPPED:
            QMessageBox.information(self, "Stopped", "Trade Stopped!")
            self.statusBar().showMessage("Trade Has Been Stopped")
            self.server_thread.quit()
            self.server_thread.wait()
            self.update_summary()
        else:
            QMessageBox.information(self, "Finish", "Trade Finished!", "OK")
            self.statusBar().showMessage("Trade Has Been Finished")
            self.server_thread.quit()
            self.server_thread.wait()
            self.update_summary()

    def closeEvent(self, *args, **kwargs):
        self.timer.stop()
        self.server_thread.exit()
        self.server_thread.wait()

    def update_summary(self):
        summary = ""
        summary += "Stock ID: %s\n" % self.sid.toUpper()
        summary += "Trade Algorithm: %s\n" % self.algs[self.alg - 1]
        summary += "Planned Volume: %s\n" % self.ordersize
        summary += "Performed Volume: %.0f\n" % self.finished
        if self.finished > 0:
            summary += "Average Price: %.2f\n" % (self.total_value / self.finished)
        else:
            summary += "Average Price: 0.00\n"
        summary += "Total Value: %.2f\n" % self.total_value
        summary += "Actual VWAP/TWAP: %.2f\n"%self.WAP
        self.textBsr_summary.setText(summary)

    def update_tbview(self):
        self.model.setItem(self.issue_num, 0, QStandardItem("%s" % self.sched_data[self.idx[0]][0]))
        self.model.setItem(self.issue_num, 1, QStandardItem("%d" % int(self.sched_data[self.idx[0]][2])))
        self.model.setItem(self.issue_num, 2,
                           QStandardItem("%d" % (int(self.sched_data[self.idx[0]][2]) * SHARE_PER_VOLUME)))
        self.model.setItem(self.issue_num, 3, QStandardItem("%.2f" % float(self.sched_data[self.idx[0]][1])))
        self.model.setItem(self.issue_num, 4, QStandardItem("%.2f" % (
            float(self.sched_data[self.idx[0]][1]) * int(self.sched_data[self.idx[0]][2]) * SHARE_PER_VOLUME)))
        self.model.setItem(self.issue_num, 5, QStandardItem("%d/%d" % (int(self.finished), int(self.ordersize))))
        self.model.item(self.issue_num, 0).setTextAlignment(Qt.AlignCenter)
        self.model.item(self.issue_num, 1).setTextAlignment(Qt.AlignCenter)
        self.model.item(self.issue_num, 2).setTextAlignment(Qt.AlignCenter)
        self.model.item(self.issue_num, 3).setTextAlignment(Qt.AlignCenter)
        self.model.item(self.issue_num, 4).setTextAlignment(Qt.AlignCenter)
        self.model.item(self.issue_num, 5).setTextAlignment(Qt.AlignCenter)
        self.tbView_rtinfo.verticalScrollBar().setSliderPosition(self.tbView_rtinfo.verticalScrollBar().maximum())
        self.issue_num += 1


if __name__ == '__main__':
    # print(del2num(1))
    if not os.path.exists("txtfile"):
        os.mkdir("txtfile")
    if not os.path.exists("volumefile"):
        os.mkdir("volumefile")
    if not os.path.exists("train_volumefile_line"):
        os.mkdir("train_volumefile_line")
    app = QApplication(sys.argv)
    ui = console()
    # ui2 = cdf_graph(year=year,month=month,day=day,stock=stock)
    ui.setFixedSize(1920, 990)
    ui.move(0, 0)
    ui.setWindowTitle('Trade Simulation')
    # ui2.setWindowTitle('Trade Simulation')
    ui.show()
    # ui2.show()
    app.exec_()
