from __future__ import print_function
import os 
import sys 
import platform
import functools
import random 
import time
import matplotlib
import yaml
matplotlib.use('Qt4Agg')
from matplotlib import pylab
pylab.ion()

from PyQt4 import QtCore
from PyQt4 import QtGui

from colorimeter_measurement_ui import Ui_MainWindow 
from colorimeter_serial import Colorimeter

DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 
TABLE_MIN_ROW_COUNT = 1
TABLE_COL_COUNT = 2 
COLOR2LED_DICT = {'red':0,'green':1,'blue': 2,'white': 3} 

class MeasurementMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self,parent=None):
        super(MeasurementMainWindow,self).__init__(parent)
        self.radioButtonColors = ('red', 'green', 'blue', 'white')
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        self.portLineEdit.editingFinished.connect(self.portChanged_Callback)
        self.connectPushButton.pressed.connect(self.connectPressed_Callback)
        self.connectPushButton.clicked.connect(self.connectClicked_Callback)
        self.calibratePushButton.pressed.connect(self.calibratePressed_Callback)
        self.calibratePushButton.clicked.connect(self.calibrateClicked_Callback)
        self.measurePushButton.clicked.connect(self.measureClicked_Callback)
        self.measurePushButton.pressed.connect(self.measurePressed_Callback)
        self.clearPushButton.pressed.connect(self.clearPressed_Callback)
        self.clearPushButton.clicked.connect(self.clearClicked_Callback)

        for color in self.radioButtonColors:
            button = getattr(self,'{0}RadioButton'.format(color))
            callback = functools.partial(self.colorRadioButton_Clicked, color)
            button.clicked.connect(callback)
        self.plotPushButton.clicked.connect(self.plotPushButton_Clicked)

    def initialize(self):

        self.dev = None
        self.measIndex = 0
        self.isCalibrated = False

        self.currentColor = 'red'
        self.redRadioButton.setChecked(True)
        
        osType = platform.system()
        if osType == 'Linux': 
            self.port = DFLT_PORT_LINUX 
        else: 
            self.port = DFLT_PORT_WINDOWS 
        self.portLineEdit.setText(self.port) 

        self.userHome = os.getenv('USERPROFILE')
        if self.userHome is None:
            self.userHome = os.getenv('HOME')
        self.lastLogDir = self.userHome
        self.statusbar.showMessage('Not Connected')

        # Set up data table
        self.cleanDataTable(setup=True)
        self.setWidgetEnabledOnDisconnect()
        self.tableWidget.setHorizontalHeaderLabels(('Datetime', 'Concentration')) 
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        # Setup plot style action group 
        self.plotAxisActionGrp = QtGui.QActionGroup(self)
        self.actionPlotStyleBar.setActionGroup(self.plotAxisActionGrp)
        self.actionPlotStyleScatter.setActionGroup(self.plotAxisActionGrp)
        self.actionPlotStyleBar.setChecked(True)

        # Setup plot axis action group
        self.plotAxisActionGrp = QtGui.QActionGroup(self)
        self.actionPlotAxisTime.setActionGroup(self.plotAxisActionGrp)
        self.actionPlotAxisNumber.setActionGroup(self.plotAxisActionGrp)
        self.actionPlotAxisTime.setChecked(True)

        # Load test data
        self.default_TestDir = getResourcePath('data')
        self.default_TestFiles = os.listdir(self.default_TestDir)
        self.default_TestDict = {}
        for name in self.default_TestFiles:
            pathName = os.path.join(self.default_TestDir,name)
            try:
                with open(pathName,'r') as fid:
                    data = yaml.load(fid)
                    print(data['name'])
            except IOError, e:
                print('Unable to read data file {0}'.format(name))
                print(str(e))
                continue
            self.default_TestDict[data['name']] = pathName
            self.testSolutionComboBox.addItem(data['name'])



    def portChanged_Callback(self):
        self.port = str(self.portLineEdit.text())

    def connectPressed_Callback(self):
        if self.dev == None:
            self.connectPushButton.setText('Disconnect')
            self.connectPushButton.setFlat(True)
            self.portLineEdit.setEnabled(False)
            self.statusbar.showMessage('Connecting...')

    def connectClicked_Callback(self):
        if self.dev == None:
            try:
                self.dev = Colorimeter(self.port)
                self.numSamples = self.dev.getNumSamples()
                connected = True
            except Exception, e:
                QtGui.QMessageBox.critical(self,'Error', str(e))
                self.connectPushButton.setText('Connect')
                self.statusbar.showMessage('Not Connected')
                self.portLineEdit.setEnabled(True)
                connected = False
        else:
            disconnect_msg = "Disconnecting will clear all data. Continue?"
            response = self.cleanDataTable(msg=disconnect_msg)
            if response == True:
                self.connectPushButton.setText('Connect')
                try:
                    self.cleanUpAndCloseDevice()
                except Exception, e:
                    QtGui.QMessageBox.critical(self,'Error', str(e))
                self.measIndex = 0
                connected = False
            if response == False:
                connected = True

        if connected:
            self.setWidgetEnabledOnConnect()
        else:
            self.setWidgetEnabledOnDisconnect()

    def closeEvent(self,event):
        if self.dev is not None:
            self.cleanUpAndCloseDevice()
        event.accept()

    def cleanUpAndCloseDevice(self):
        self.dev.close()
        self.dev = None

    def cleanDataTable(self,setup=False,msg=''):
        if setup:
            reply = QtGui.QMessageBox.Yes
        elif len(self.tableWidget.item(0,1).text()):
            reply = QtGui.QMessageBox.question(self, 'Message', 
                             msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        else: 
            return True

        if reply == QtGui.QMessageBox.Yes:
            self.tableWidget.setRowCount(TABLE_MIN_ROW_COUNT)
            self.tableWidget.setColumnCount(TABLE_COL_COUNT)
            for row in range(TABLE_MIN_ROW_COUNT+1):
                for col in range(TABLE_COL_COUNT+1):
                    tableItem = QtGui.QTableWidgetItem()
                    tableItem.setFlags(QtCore.Qt.NoItemFlags)
                    self.tableWidget.setItem(row,col,tableItem)
            self.measIndex = 0
            return True
        else:
            return False

    def colorRadioButton_Clicked(self,color):
        if len(self.tableWidget.item(0,1).text()):
            chn_msg = "Changing channels will clear all data. Continue?"
            response = self.cleanDataTable(msg=chn_msg)
            if not response:
                color = self.currentColor
                button = getattr(self,'{0}RadioButton'.format(color))
                button.setChecked(True)
        self.currentColor = color

    def plotPushButton_Clicked(self):
        print('plotPushButton_Clicked',self.measIndex)
        #dataList = []
        #for i in range(self.measIndex):
        #    tableItem = self.tableWidget.item(i,1)
        #    x = float(tableItem.text())
        #    tableItem = self.tableWidget.item(i,0)
        #    y = float(tableItem.text())
        #    dataList.append((x,y))

        #yList = [x for x,y in dataList]
        #xList = [y for x,y in dataList]
        #if len(dataList) > 1:
        #    polyFit = pylab.polyfit(xList,yList,1)
        #    xFit = pylab.linspace(min(xList), max(xList), 500)
        #    yFit = pylab.polyval(polyFit, xFit)
        #    hFit = pylab.plot(xFit,yFit,'r')
        #pylab.plot(xList,yList,'ob')
        #pylab.grid('on')
        #pylab.xlabel('Concentration')
        #pylab.ylabel('Absorbance ('+self.currentColor+' led)')
        #slope = polyFit[0]
        ##pylab.figlegend((hFit,),('slope = {0:1.3f}'.format(slope),), 'upper left')
        #pylab.figtext(0.15,0.85,'slope = {0:1.3f}'.format(slope), color='r')
        #pylab.show()
        
    def setWidgetEnabledOnDisconnect(self):
        self.measurePushButton.setEnabled(False)
        self.calibratePushButton.setEnabled(False)
        self.plotPushButton.setEnabled(False)
        self.clearPushButton.setEnabled(False)
        self.tableWidget.setEnabled(False)
        self.testSolutionWidget.setEnabled(False)
        self.coeffLEDWidget.setEnabled(False)
        self.portLineEdit.setEnabled(True)
        self.statusbar.showMessage('Not Connected')
        self.cleanDataTable()
        self.isCalibrated = False

    def setWidgetEnabledOnConnect(self):
        self.calibratePushButton.setEnabled(True)
        if self.isCalibrated:
            self.plotPushButton.setEnabled(True)
            self.clearPushButton.setEnabled(True)
            self.measurePushButton.setEnabled(True)
            self.tableWidget.setEnabled(True)
            self.testSolutionWidget.setEnabled(True)
        self.portLineEdit.setEnabled(False)
        self.connectPushButton.setFlat(False)
        self.statusbar.showMessage('Connected, Mode: Stopped')

    def calibratePressed_Callback(self):
        print('callibratePushButton_Pressed')
        self.measurePushButton.setEnabled(False)
        self.plotPushButton.setEnabled(False)
        self.clearPushButton.setEnabled(False)
        self.calibratePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Calibrating...')

    def calibrateClicked_Callback(self):
        print('calibratePushButton_Clicked')
        self.dev.calibrate()
        self.isCalibrated = True
        self.calibratePushButton.setFlat(False)
        self.setWidgetEnabledOnConnect()

    def measurePressed_Callback(self):
        print('measPushButton_Pressed')
        self.plotPushButton.setEnabled(False)
        self.measurePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Measuring...')

    def measureClicked_Callback(self):
        rowCount = self.measIndex+1
        freq, trans, absorb = self.dev.getMeasurement()
        self.measurePushButton.setFlat(False)

        ledNumber = COLOR2LED_DICT[self.currentColor]
        transStr = '{0:1.2f}'.format(trans[ledNumber])
        absorbStr = '{0:1.2f}'.format(absorb[ledNumber])
        print('{0}: {1}'.format(self.currentColor, absorbStr))

        ts = time.localtime()
        timeStr = time.strftime('%m/%d/%y %H:%M:%S',ts)

        if rowCount > TABLE_MIN_ROW_COUNT:
            self.tableWidget.setRowCount(rowCount)

        # Put time string into table
        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(timeStr)
        self.tableWidget.setItem(self.measIndex,0,tableItem)

        # Put measurement into table
        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(absorbStr)
        self.tableWidget.setItem(self.measIndex,1,tableItem)
        self.tableWidget.setCurrentItem(tableItem)

        self.measIndex+=1
        self.setWidgetEnabledOnConnect()


    def clearPressed_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            self.measurePushButton.setEnabled(False)
            self.plotPushButton.setEnabled(False)
        self.clearPushButton.setFlat(True)

    def clearClicked_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            erase_msg = "Clear all data?"
            self.cleanDataTable(msg=erase_msg)
        self.clearPushButton.setFlat(False)
        self.setWidgetEnabledOnConnect()

    def main(self):
        self.show()

def measurementGuiMain():
    """
    Entry point for measurement gui
    """
    app = QtGui.QApplication(sys.argv)
    mainWindow = MeasurementMainWindow()
    mainWindow.main()
    app.exec_()

def getResourcePath(relative_path): 
    """
    Get path of resources file in both deployed and development.
    """
    base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))
    resource_path = os.path.join(base_path, relative_path)
    return resource_path

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    measurementGuiMain()

