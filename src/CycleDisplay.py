'''
Created on 2011-08-05

@author: Ryan Brodie
'''

import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyQt4 import QtCore, QtGui

class CycleDisplay(FigureCanvas):
    '''
    classdocs
    '''


    def __init__(self, dataBuffer, size=1):
        '''
        Constructor
        '''
        
        self.dataBuffer=dataBuffer
        
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        
        self.axes = self.fig.add_subplot(1,size,1)
        
        self.tstart = time.time()
        self.timerEvent(None)
        
        self.draw()
        
    def addSubplot(self):
        pass
        
    def timerEvent(self, evt):
        """
        Timer event method - serves as the primary redraw, 
        """
        
        if not self.isVisible():
            return