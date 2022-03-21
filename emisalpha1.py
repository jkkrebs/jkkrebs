# -*- coding: utf-8 -*-
"""
Created on Tue May 18 10:17:31 2021

@author: kkrebs
"""
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import queue
import numpy as np

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class MplCanvas(FigureCanvas):
    def __init__(self,parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()
        
        
class PyShine_LIVE_PLOT_APP(QtWidgets.QMainWindow):
    def __int__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('pythonemissionalpha.ui',self)
        self.resize(888,600)
        icon = QtGui.Qicon()
        icon.addPizmap(QtGui.QPixmap("PyShine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        self.canvas=MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.gridLayout_4.addWidget(self.canvas,2,1,1,1)
        self.reference_plot = None
        
        #parameters are initialized here
        self.device = 0
        self.window_length = 1000
        #etc
        
        #device_info = sd.query_devices(self.device, 'input')
        #self.samplerate=device_info['default_samplerate']
        length = int(self.window_length*self.samplerate/(1000*self.dawnsample))
        #sd.default.samplerate=self.samplerate
        
        self.plotdata=np.zeros((length,len(self.channels)))
        
        self.update_plot()
        self.timer=QtCore.QTimer()
        self.timer.setInterval(self.interval) #msec
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        #self.lineEdit_2.textChanged['QString'].connect(self.update_interval)
        #self.pushButton.clicked.connect(self.start_worker)
        
    #def getData(self):
        #yeah, still need to write this one
        
    def start_worker(self):
        worker=Worker(self.start_stream, )
        self.threadpool.start(worker)
        
    def start_stream(self):
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        # disable all inputs that shouldn't be changed during scan
        self.getData()
        
    def update_now(self,value):
        self.device=self.devices_list.index(value)
        print('Device:', self.devices_list.index(value))
        
    def update_window_length(self, value):
        self.window_length=int(value)
        length=int(self.window_length*self.samplerate/(1000*self.downsample))
        self.plotdata=np.zeros((length,len(self.channels)))
        self.update_plot()
        
    def update_sample_rate(self, value):
        self.samplerate=int(value)
        sd.default.samplerate=self.sampleratelength=int(self.window_length*self.samplerate/(1000*self.downsample))
        self.plotdata=np.zeros((length,len(self.channels)))
        self.update_plot()
        
    def update_down_sample(self, value):
        self.downsample=int(value)
        length = int(self.window_length*self.samplerate/(1000*self.downsample))
        self.plotdata=np.zeros((length,len(self.channels)))
        self.update_plot()
        
    def update_interval(self,value):
        self.interval=int(value)
        self.timer.setInterval(self.interval) #msec
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
    def update_plot(self):
        try:
            data=[0]
            
            while True:
                try:
                    data=self.q.get_nowait()
                except queue.Empty:
                    break
                shift = len(data)
                self.plotdata= np.roll(self.plotdata, -shift,axis=0)
                self.plotdata[-shift:,:]=data
                self.ydata=self.plotdata[:]
                self.canvas.axes.set_facecolor((0,0,0))
                
                
                if self.reference_plot is None:
                    plot_refs=self.canvas.axes.plot(self.ydata,color=(0,1,0.29))
                    self.reference_plot=plot_refs[0]
                else:
                    self.reference_plot.set_ydata(self.ydata)
                    
                    
            self.canvas.axes.yaxis.grid(True,linestyle='--')
            start, end=self.canvas.axes.get_ylim()
            self.canvas.axes.yaxis.set_ticks(np.arange(start,end,0.1))
            self.canvas.axes.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            self.canvas.axes.set_ylim(ymin=-0.5, ymax=0.5)
            self.canvas.draw()
        except:
            pass
        
#www.pyshine.com
class Worker(QtCore.QRunnable):
    
    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        
    @pyqtSlot()
    def run(self):
        
        self.function(*self.args, **self.kwargs)
        
        
        
app = QtWidgets.QApplication(sys.argv)
pythonemissionalpha = PyShine_LIVE_PLOT_APP()
pythonemissionalpha.show()
sys.exit(app.exec_())

        
            
        
        
        
        
        
        
        
        