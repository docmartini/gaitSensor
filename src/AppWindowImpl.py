'''
Created on 2011-08-05

@author: Ryan Brodie
'''

import time, random

from PyQt4 import QtGui, QtCore

from numpy import linspace

from AppWindow import Ui_MainWindow
from LevelBar import LevelBar

FPS = 72

class AppWindowImpl(QtGui.QMainWindow, Ui_MainWindow):
    '''
    classdocs
    '''


    def __init__(self, dataBuffer, parent=None):
        '''
        Constructor
        '''
        
        super(AppWindowImpl, self).__init__(parent)
        self.setupUi(self)

        self.data=dataBuffer

        self.bars = [LevelBar(),LevelBar(),LevelBar()]
        for i in range(3):
            self.bars[i].setMin(-3.25)
            self.bars[i].setMax(3.25)
            self.bars[i].setValue(0)
            self.horizontalLayout.addWidget(self.bars[i])

        self.bars[0].setColor(255,0,0)
        self.bars[1].setColor(0,255,0)
        self.bars[2].setColor(0,0,255)
        
        self.tstart = time.time()
        self.timerEvent(None)
        self.startTimer(1000.0/FPS)
        
    def timerEvent(self, evt):
        """
        Timer event method - serves as the primary redraw, 
        """
        
        val = self.data.getLastData(1)
        
        if not val:
            val = [0,0,0]
        
        for i in range(3):
            self.bars[i].setValue(val[i])
            self.bars[i].repaint()