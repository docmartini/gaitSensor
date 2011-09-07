import time
import marshal
import csv

import numpy as np

from PyQt4.QtCore import QObject
from PyQt4 import QtCore

class SensorData(QObject):
    
    SALT = 'fls4j5k2j20U*)UIOJ;j'
    
    modified = QtCore.pyqtSignal('bool')
    archiveModified = QtCore.pyqtSignal()
    
    __fname = ''
    __dirty = False
    
    __archive = {}
    
    __time = []
    
    __streamIndex = [
                     [1,2,3],
                     [4,5,6],
                     [20,21,22],
                     [23,24,25],
                     [26,27,28]
                     ]
    
    __data = [ [],[],[],[],[] ]
    
    __sensorStreams = ['Raw Accel Data','Euler Angles',
                       'Acceleration (Gravity)','User Acceleration','Rotational Rate']
    
    __sensorBreakdown= [ ['X-axis','Y-axis','Z-axis'],
                       ['Pitch','Roll','Yaw'],
                       ['X-axis','Y-axis','Z-axis'],
                       ['X-axis','Y-axis','Z-axis'],
                       ['X-axis','Y-axis','Z-axis'] ]
    __sensorLimits= [
                   [-2.2,2.2,.5],
                   [-3.25,3.25,.25],
                   [-1.2,1.2,0.2],
                   [-1.2,1.2,0.2],
                   [-1.2,1.2,0.2]
                   ]
    
    def __init__(self):
        QtCore.QObject.__init__(self)
    
    def archiveData(self):
        if len(self.__time) > 0:
            self.__archive[str(time.time())]=[self.__time,self.__data]
            self.archiveModified.emit()
    
    def getArchiveKeys(self):
        return self.__archive.keys()
    
    def getArchiveData(self,key):
        return self.__archive[str(key)]
    
    def filename(self,fname=None):
        if (fname):
            self.__fname = fname
            
        return self.__fname
    
    def deleteArchiveData(self,key):
        try:
            del(self.__archive[key])
        except KeyError:
            return False
        return True
    
    def clearData(self):
        """
        Clear the current data buffer
        """
        self.__time = []
    
        self.__data = [ [],[],[],[],[] ]
        self.__dirty = True
        self.modified.emit(self.isDirty())
    
    def isDirty(self):
        return self.__dirty
    
    def append(self,stream,time,value):
        """ Append a value to the given stream or the default stream 
        if none is given. 
        """

        if len(self.__time)==0 or time > self.__time[len(self.__time)-1]:
            self.__time.append(time)
            self.__data[stream].append(value) 
        elif time == self.__time[len(self.__time)-1]:
            self.__data[stream].append(value) 
            
        self.__dirty = True
        self.modified.emit(self.isDirty())
    
    def getTime(self,start=None,end=None):
        """ Get the timeline for this buffer
        """
        
        # sanitize the start,end values
#        if start<0:
#            start=None
#        if end<0:
#            end=None
#        if start>end:
#            tmp=start
#            start=end
#            end=tmp
            
        if(start and end):
            return self.__time[start:end]
        elif(start):
            return self.__time[start:]
        elif(end):
            return self.__time[:end]
        else:
            return self.__time
    
    def getData(self,stream,start=None,end=None):
        """ Get the current data stream or an arbitrary stream
        """
        
        # sanitize the start,end values
#        if start<0:
#            start=None
#        if end<0:
#            end=None
#        if start>end:
#            tmp=start
#            start=end
#            end=tmp
        
        if(start and end):
            return self.__data[stream][start:end]
        elif(start):
            return self.__data[stream][start:]
        elif(end):
            return self.__data[stream][:end]
        else:
            return self.__data[stream]
    
    def getLastData(self,stream):
        if (len(self.__data[stream]) > 0):
            return self.__data[stream][-1]
        else:
            return None
        
    def save(self, fname=None):
        if not fname and self.__fname == '':
            return False
        elif not fname:
            fname = self.__fname
        
        self.archiveData()
        self.clearData()
        
        self.__archive[self.SALT]=self.SALT
        
        f = open(fname,'wb')
        
        marshal.dump(self.__archive,f)
        self.filename(fname)
        self.__dirty=False
        self.modified.emit(self.isDirty())
        
    def load(self, fname):
        
        try:
            f = open(fname,'rb')
            data = marshal.load(f)
        except EOFError:
            raise IOError(0,"Incorrect file format")
        
        try:
            salt = data[self.SALT]
        except KeyError:
            raise IOError(0,"Incorrect file format")
        
        del(data[self.SALT])
        
        self.__archive = data
        self.filename(fname)
        self.__dirty=False
        self.modified.emit(self.isDirty())
        self.archiveModified.emit()
        
    def getStreams(self):
        """ Return a list of streams available for listening
        """
        return self.__sensorStreams
    
    def streamBounds(self, stream):
        """ Get an upper and lower limit on the data that will be received
        by the given stream
        """
        return self.__sensorLimits[stream]
    
    def streamIndices(self, stream):
        """ Get the indices of the stream components that are found in the 
        network packet data from the app. This is used to route values correctly
        """
        return self.__streamIndex[stream]
    
    def streamAxes(self, stream):
        """ get the axis titles that should be displayed for the given
        stream
        """
        return self.__sensorBreakdown[stream]
    
    def exportBuffer(self, filename):
        writer = csv.writer(open(filename,'wb'))
        
        headers1=['time']
        for h in self.__sensorStreams:
            headers1.append(h)
            headers1.append('')
            headers1.append('')
        
        headers2=['']
        for h in self.__sensorBreakdown:
            for h2 in h:
                headers2.append(h2)
        
        writer.writerow(headers1)
        writer.writerow(headers2)
        
        for i in range(len(self.__time)):
            output = [self.__time[i]]
            for j in range(len(self.__data)):
                for k in range(len(self.__data[j][i])):
                    output.append(self.__data[j][i][k])
            
            writer.writerow(output)
    
    def exportArchive(self, key, filename):
        writer = csv.writer(open(filename,'wb'))
        
        headers1=['time']
        for h in self.__sensorStreams:
            headers1.append(h)
            headers1.append('')
            headers1.append('')
        
        headers2=['']
        for h in self.__sensorBreakdown:
            for h2 in h:
                headers2.append(h2)
        
        writer.writerow(headers1)
        writer.writerow(headers2)
        
        time,data=self.getArchiveData(key)
        
        for i in range(len(time)):
            output = [time[i]]
            for j in range(len(data)):
                for k in range(len(data[j][i])):
                    output.append(data[j][i][k])
            
            writer.writerow(output)
    
if __name__ == '__main__':
    data = SensorData()
    data.load('test.dat')
    
    x= data.getArchiveKeys()
    
    data.exportArchive(x[0], 'x.csv')    