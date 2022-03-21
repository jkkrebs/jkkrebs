# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 15:46:26 2021

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
from PyQt5 import QtCore, QtWidgets #, QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self). __init__(fig)
        fig.tight_layout()
        
class LIVE_PLOT_APP(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('emisGUI.ui',self)
        self.resize(888, 600)
        
        self.threadpool = QtCore.QThreadPool()
        
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.addWidget(self.canvas, (40,280))
        self.reference_plot = None
        self.q = queue.Queue(maxsize=20)
        
        #initialize instrumentation here
        wavlen=[610, 611, 612, 613, 614]
        
        length = int((self.lineEdit_endwav - self.lineEdit_startwav)/self.lineEdit_scanstep)
        self.plotdata = np.zeros((length, len(wavlen))) #wavlen is list of all taken
        
        self.update_plot()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval) #msec
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
        self.lineEdit_startwav.textChanged['QString'].connect(self.update_window_length)
    
        self.lineEdit_endwav.textChanged['QSring'].connect(self.update_sample_rate)
    
        self.lineEdit_scanstep.textChanged['QString'].connect(self.update_down_sample)
    
        self.lineEdit_phase.textChanged['QString'].connect(self.update_interval)
        
        self.pushButton_startscan.clicked.connect(self.start_worker)
        
    def getData(self):
        pass
    
    def start_worker(self):
        worker = Worker(self.start_stream, )
        self.threadpool.start(worker)
        
    def start_stream(self):
        self.lineEdit_startwav.setEnabled(False)
        self.lineEdit_endwav.setEnabled(False)
        self.lineEdit_scanstep.setEnabled(False)
        self.pushButton_startscan.setEnabled(False)
        self.getData()
        
    def update_window_length(self,value):
        self.window_length = int(value)
        length = int(self.window_length*self.lineEdit_scanstep) #need to fix this
        self.plotdata = np.zeros((length, len(value)))
        self.update_plot()
        
    def update_interval(self,value):
        self.interval = int(value)
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
    def update_plot(self):
        try:
            data=[0]
            
            while True:
                try:
                    data= self.q.get_nowait()
                except queue.Empty:
                    break
                shift = len(data)
                self.plotdata = np.roll(self.plotdata, -shift, axis = 0)
                self.plotdata[-shift:,:] = data
                self.ydata = self.plotdata[:]
                self.canvas.axes.set_facecolor((0,0,0))
                
                if self.reference_plot is None:
                    plot_refs = self.canvas.axes.plot(self.ydata, color=(0,1,0.29))
                    self.reference_plot = plot_refs[0]
                else:
                    self.reference_plot.set_ydata(self.ydata)
                    
            self.canvas.axes.yaxis.grid(True,linestyle='--')
            start, end = self.canvas.axes.get_ylim()
            self.canvas.axes.yaxis.set_ticks(np.arange(start,end,0.1))
            self.canvas.axes.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            self.canvas.axes.set_ylim(ymin=-0.5, ymax=0.5)
            self.canvas.draw()
            
        except:
            pass
        
class Worker(QtCore.QRunnable):
    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function()
        self.args = args
        self.kwargs = kwargs
        
    @pyqtSlot()
    def run(self):
        self.function(*self.args, **self.kwargs)
        
app = QtWidgets.QApplication(sys.argv)
mainWindow = LIVE_PLOT_APP()
mainWindow.show()
sys.exit(app.exec_())

        
    
        
        