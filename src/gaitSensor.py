'''
Created on 2011-08-05

@author: Ryan Brodie
'''

import sys
import warnings

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject

from AppWindowImpl import AppWindowImpl
from SensorData import SensorData
from SensorReceiver import SensorReceiver

DEFAULT_PORT = 10552

class Controller(QObject):
    
    dataBuffer=None
    sensorReceiver=None
    window=None
    
    def __init__(self):
        QObject.__init__(self)
        
        self.dataBuffer = SensorData()
        self.sensorReceiver = SensorReceiver(self.dataBuffer, DEFAULT_PORT)
        self.window = AppWindowImpl(self.dataBuffer)
        
        self.eventSetup()
        
        self.window.show()
    
    def eventSetup(self):
        # Open a listener
        self.connect(self.window.actionListen, 
                     QtCore.SIGNAL('triggered(bool)'),
                     self.listen)
        
        # Secondary packet/signal processing
        self.connect(self.sensorReceiver,
                     QtCore.SIGNAL('dataReceived()'),
                     self.received)
    
    @QtCore.pyqtSlot()
    def received(self):
        pass
    
    @QtCore.pyqtSlot('bool')  
    def listen(self, isActive):
        if (isActive):
            self.sensorReceiver.openSocket()
        else:
            self.sensorReceiver.closeSocket()

if __name__ == '__main__':
    warnings.simplefilter('ignore')
    app = QtGui.QApplication(sys.argv)
    
    controller = Controller()
    
    sys.exit(app.exec_())