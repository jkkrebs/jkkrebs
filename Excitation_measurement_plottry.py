# -*- coding: utf-8 -*-
"""
Created on Thu May 20 09:51:55 2021

@author: kkrebs
"""

import sys
import numpy as np
from PyQt5 import QtCore #, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import pyvisa
import time
import matplotlib.pyplot as plt
#import pandas as pd
import matplotlib.figure as Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

rm = pyvisa.ResourceManager()
rm.list_resources()
Lockin = rm.open_resource('GPIB0::6::INSTR')
Lockin.read_termination="\n"
Cornerstone = rm.open_resource('GPIB0::4::INSTR')
Cornerstone.read_termination="\r\n"
McPherson = rm.open_resource('ASRL1::INSTR', baud_rate=19200)
McPherson.write_termination="\r"
McPherson.read_termination="\r"

class MplCanvas(FigureCanvas):
    def __init__(self, parent= None, width = 5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes=fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()

class Emission_GUI(QMainWindow):
    def __init__(self):
        super(Emission_GUI,self).__init__()
        loadUi('EmisGUI.ui',self) 
        self.setWindowTitle('Excitation Measurement GUI')    
        
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.widget_futureplot.addWidget(self.canvas, 2,1,1,1)
        self.reference_plot = None
        
        self.plotdata = np.zeros()
        self.update_plot()
        self.timer=QtCore.QTimer()
        self.timer.setInterval(1000) #msec
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
        self.lineEdit_phase.setText(phase)
        self.lineEdit_freq.setText(freq)
        self.lineEdit_time_const.setText(str(tau))
 
        self.pushButton_startscan.clicked.connect(self.excitation_scan)
        self.pushButton_alignbtn.clicked.connect(self.alignment)
        self.pushButton_initialize.clicked.connect(self.initialize)
        
#    def update_plot(self):
        # try:
        #     data=[0]
            
        #     while True:
        #         try:
        #             data=self.xchan
#                except Empty:
#                   break
#               shift = len(data)
        #         self.plotdata = np.roll(self.plotdata, -shift,axis = 0)
        #         self.plotdata[-shift:,:]=data
        #         self.ydata = self.plotdata[:]
        #         self.canvas.axes.set_facecolor((0,0,0))
                
        #         if self.reference_plot is None:
        #             plot_refs = self.canvas.axes.pot(self.ydata, color=(0,1,0.29))
        #             self.reference_plot = plot_refs[0]
        #         else:
        #             self.reference_plot.set_ydata(self.ydata)
            
        #     self.canvas.axes.yaxis.grid(True, linestyle='--')
        #     start, end = self.canvas.axes.get_ylim()
        #     self.canvas.axes.yaxis.set_ticks(np.arange(start, end, 0.1))
        #     self.canvas.axes.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        #     self.canvas.axes.set_ylim(ymin=0.0, ymax = 0.1)
        #     self.canvas.draw()
        # except:
        #     pass

           
    
    def closeEvent(self,events): #when the GUI is closed the instruments close
        McPherson.close()
        Cornerstone.close()
        Lockin.close()
        print('GUI and resources closed')
    
    def initialize(self):
        initial_wavelen = self.lineEdit_detectionwavalign.text()
        initial_code=str(float(initial_wavelen) * 18)
        McPherson.write('H' + initial_code) # initializes McPherson at initial_wavelen nm
        cornerstone_wav = Cornerstone.query('WAVE?')
        time.sleep(2)
        position = McPherson.query_ascii_values('Q', separator = ':', converter='x')#query location and status
        self.lineEdit_wavelength.setText(str(position[1]/18))
        self.lineEdit_excitationwavalign.setText(cornerstone_wav)
        

    def alignment(self):
        Corn_wav_desire = self.lineEdit_excitationwavalign.text()
        McPh_wav_desire = str(float(self.lineEdit_McPherson_wavlen.text())*18)        
        Cornerstone.write('GOWAVE ' + Corn_wav_desire)
        McPherson.write('M' + McPh_wav_desire)
        time.sleep(1)
        Cornerstone_wav = Cornerstone.query('WAVE?')
        position = McPherson.query_ascii_values('Q', separator = ':', converter='x')#query location and status
        while position[0] == 52: #52 means McPherson is still Moving
            time.sleep(0.25)
            position = McPherson.query_ascii_values('Q', separator = ':', converter='x')
        self.lineEdit_wavelength.setText(str(position[1]/18))
        self.lineEdit_excitationwavalign.setText(Cornerstone_wav)
        
        
    def excitation_scan(self):
        phase=Lockin.query('PHAS?')
        freq=Lockin.query('freq?')
        time_const_code=Lockin.query('OFLT?')
        # key-value pairs for tau conversion from tau_code
        time_const = {"0":0.00001,"1":.000030,"2":0.0001,"3":0.0003,"4":0.001,"5":0.003,"6":0.010,"7":0.030,"8":0.100,"9":0.300,"10":1,"11":3}
        tau = time_const[time_const_code] # converted through dictionary to value in seconds
        
        # self.lineEdit_phase.setText(phase)
        # self.lineEdit_freq.setText(freq)
        # self.lineEdit_time_const.setText(str(tau))
        
        self.start_lambda = float(self.lineEdit_startwav.text())
        self.end_lambda = float(self.lineEdit_endwav.text())
        self.step_size = float(self.lineEdit_scanstep.text())
        
        l = self.start_lambda
        data =[]
        
        while l < self.end_lambda + self.step_size:
            Corn_wav_desire = l
            Cornerstone.write('GOWAVE ' + Corn_wav_desire)
            time.sleep(0.5)
            
            Cornerstone_wav = Cornerstone.query('WAVE?')
            
            time.sleep(5*tau)
            
            xchan=Lockin.query('OUTP?1')
            ychan=Lockin.query('OUTP?2')
            
            self.lineEdit_wavelength.setText(str(Cornerstone_wav))
            self.lineEdit_xch.setText(xchan)
            self.lineEdit_ych.setText(ychan)
 
            data.append(np.array([float(Cornerstone_wav),float(xchan),float(ychan)]))
            # update plot
            
            l += self.step_size

        #write data out to file
        data = np.asarray(data) #list of 1_D arrays becomes 2_D array
        np.savetxt(r"C:\Users\kkrebs\Desktop\data\exampleFile.txt", data)
       
        
app= QApplication(sys.argv)
widget=Emission_GUI()
widget.show()

sys.exit(app.exec_())


