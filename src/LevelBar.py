'''
Created on 2011-09-05

@author: Ryan Brodie
'''

import sys

from PyQt4 import QtGui, QtCore

class LevelBar(QtGui.QWidget):
    '''
    classdocs
    '''
    
    value=0
    min=0
    max=0
    color=QtGui.QColor(255,255,255)


    def __init__(self):
        '''
        Constructor
        '''

        super(LevelBar, self).__init__()
        
        self.initUI()
        
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Shadow)
        
    def initUI(self):
        pass
    
    def paintEvent(self, event):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        
        self.drawEnvironment(event,qp)
        self.drawText(event,qp)
        self.drawLevel(event,qp)
        
        qp.end()
    
    def drawEnvironment(self, event, qp):
        ''' 
        Draw bounding box, median and other values
        '''
        
#        self.bgcolor = QtGui.QColor(0,0,0)
#        qp.setBrush(self.bgcolor)
#        qp.drawRect(self.rect())
    
    def drawText(self, event, qp):
        '''
        Draw text of the min/max values
        '''
        pass
    
    def drawLevel(self, event, qp):
        '''
        Draw the level bar itself
        '''
        if (self.min==self.max):
            return
        
        r=self.rect()
        fr = abs(self.max-self.value)*1.0/(self.max-self.min)
        top = (fr)*r.height()

        #print("Y: "+ str(r.y()) +", top: "+ str(top) +", r:"+str(self.rect()))
        
        r = self.rect()
        r.setY(top)
        
        qp.setBrush(self.color)
        qp.drawRect(r)
        
    
    def setColor(self, r, g, b):
        self.color = QtGui.QColor(r,g,b)
        
    def setMin(self,min):
        self.min=min
        
        if (self.min>self.value):
            self.min=self.value
            
    def setMax(self,max):
        self.max=max
        
        if (self.max<self.value):
            self.max=self.value
        
    def setValue(self, value):
        self.value = value
        
        if (self.min>self.value):
            self.min=self.value
        
        if (self.max<self.value):
            self.max=self.value
            
if __name__ == '__main__':
    # Create the GUI application
    qApp = QtGui.QApplication(sys.argv)
    # Create the Matplotlib widget
    
    lb = LevelBar()
    lb.setMin(-100)
    lb.setMax(100)
    lb.setValue(-85)
    lb.setColor(255,0,0)
    lb.show()
    
    sys.exit(qApp.exec_())