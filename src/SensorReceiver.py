from PyQt4 import QtNetwork, QtCore
import time

class SensorReceiver(QtCore.QObject):
    """ Data receiver class
    
    Currently formatted for use with the "Sensor Data" iPhone/iPod app. 
    
    """
    
    dataReceived = QtCore.pyqtSignal()
    
    # @param str : error message
    # @param bool: whether or not the error is critical (show stopping)
    receiverError = QtCore.pyqtSignal(str,bool)
    
    def __init__(self, data, port, parent=None):
        QtCore.QObject.__init__(self)
        
        self.data = data
        self.port = port
        
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.listening = False
        
        self.connect(self.udpSocket, QtCore.SIGNAL("readyRead()"),
                     self.processPendingDatagrams)
    
    @QtCore.pyqtSlot()
    def closeSocket(self):
        print "closing ",self.port
        if not self.listening:
            return
        
        self.udpSocket.close()
        self.listening = False
    
    @QtCore.pyqtSlot()
    def openSocket(self):
        print "opening on ",self.port
        if self.listening:
            return

        self.udpSocket.bind(self.port)
        self.listening = True
    
    @QtCore.pyqtSlot()
    def setPortStatus(self, open):
        if open:
            self.openSocket()
        else:
            self.closeSocket()    
         
    @QtCore.pyqtSlot('int')
    def setPort(self, port):
        """ Set the listening port for this receiver
        
        This will only really take effect after the next time listening is 
        reset.
        
        """
        if (port > 1024):
            self.port = port
            print "Changing to port ",port
        
    def processPendingDatagrams(self):
        """ Processes a UDP datagram and checks for appropriate length
        """
        
        while(self.udpSocket.hasPendingDatagrams()):
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            values=datagram.split(',')
                       
            try:  
                if (len(values)<35):
                    self.handleError("Incorrect packet length, please ensure all streams are enabled in the SensorData iPod/iPhone application",False)
                    self.closeSocket()
                    return
                
                float(values[0])

                streams = self.data.getStreams()
                for i in range(len(streams)):
                    datasub = []
                    indlist = self.data.streamIndices(i)
                    for j in indlist:
                        datasub.append(float(values[j]))
                    self.data.append(i,float(values[0]),datasub)
            except ValueError:
                # Archive current data and start again 
                self.data.archiveData()
                self.data.clearData()
              
            self.dataReceived.emit()
        
    def handleError(self,errorMessage,critical=False):
        """
        signal to signify that there was a problem processing data.
        """
        print(errorMessage)
        self.receiverError.emit(errorMessage,critical)