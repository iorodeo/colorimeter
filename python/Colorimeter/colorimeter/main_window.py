from __future__ import print_function
import os
import functools
import platform
from PyQt4 import QtCore
from PyQt4 import QtGui
import matplotlib.pyplot as plt 

import constants
import import_export
from colorimeter_serial import Colorimeter
from colorimeter.gui.dialog.test_solution_dialog import TestSolutionDialog

class MainWindowCommon(QtGui.QMainWindow):

    def __init__(self,parent=None):
        super(MainWindowCommon,self).__init__(parent)

    def connectActions(self):
        self.portLineEdit.editingFinished.connect(self.portChanged_Callback)
        self.connectPushButton.pressed.connect(self.connectPressed_Callback)
        self.connectPushButton.clicked.connect(self.connectClicked_Callback)
        self.calibratePushButton.pressed.connect(self.calibratePressed_Callback)
        self.calibratePushButton.clicked.connect(self.calibrateClicked_Callback)
        self.measurePushButton.clicked.connect(self.measureClicked_Callback)
        self.measurePushButton.pressed.connect(self.measurePressed_Callback)
        self.actionSave.triggered.connect(self.saveFile_Callback)
        self.actionSave.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.actionAbout.triggered.connect(self.about_Callback)
        self.actionSave.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_A)

    def initialize(self):
        self.setAppSize()
        self.dev = None
        self.fig = None
        self.isCalibrated = False
        self.aboutCaption = 'About'
        self.aboutText = 'About Default Text'

        # Set default port based on system
        osType = platform.system()
        if osType == 'Linux': 
            self.port = constants.DFLT_PORT_LINUX 
        elif osType == 'Darwin':
            self.port = constants.DFLT_PORT_DARWIN
        else: 
            self.port = constants.DFLT_PORT_WINDOWS 
        # Get users home directory
        self.userHome = os.getenv('USERPROFILE')
        if self.userHome is None:
            self.userHome = os.getenv('HOME')
        self.lastSaveDir = self.userHome
        self.statusbar.showMessage('Not Connected')
        self.portLineEdit.setText(self.port) 
        if constants.DEVEL_FAKE_MEASURE: 
            msgTitle = 'Development'
            msgText = 'Development mode fake measure is enabled'
            QtGui.QMessageBox.warning(self,msgTitle, msgText)

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
                connected = True
            except Exception, e:
                msgTitle = 'Connection Error'
                msgText = 'unable to connect to device: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                self.connectPushButton.setText('Connect')
                self.statusbar.showMessage('Not Connected')
                connected = False
                self.dev = None
        else:
            self.connectPushButton.setText('Connect')
            try:
                self.cleanUpAndCloseDevice()
            except Exception, e:
                QtGui.QMessageBox.critical(self,'Error', str(e))
            connected = False

        if connected:
            self.numSamples = self.dev.getNumSamples()
        self.updateWidgetEnabled()
        self.connectPushButton.setFlat(False)

    def calibratePressed_Callback(self):
        self.measurePushButton.setEnabled(False)
        self.calibratePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Calibrating...')

    def calibrateClicked_Callback(self):
        if not constants.DEVEL_FAKE_MEASURE: 
            try:
                self.dev.calibrate()
                self.isCalibrated = True
            except IOError, e:
                msgTitle = 'Calibration Error:'
                msgText = 'unable to calibrate device: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                self.updateWidgetEnabled()
        else:
            self.isCalibrated = True
        self.calibratePushButton.setFlat(False)
        self.updateWidgetEnabled()

    def measurePressed_Callback(self):
        self.calibratePushButton.setEnabled(False)
        self.measurePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Measuring...')

    def measureClicked_Callback(self):
        self.getMeasurement()
        self.measurePushButton.setFlat(False)
        self.updateWidgetEnabled()

    def portChanged_Callback(self):
        self.port = str(self.portLineEdit.text())

    def setAppSize(self):
        availGeom = QtGui.QApplication.desktop().availableGeometry()
        x, y = constants.START_POS_X, constants.START_POS_Y
        width = min([0.9*(availGeom.width()-x), self.geometry().width()])
        height = min([0.9*(availGeom.height()-y), self.geometry().height()])
        self.setGeometry(x,y,width,height)

    def saveFile_Callback(self):
        if not self.haveData():
            msgTitle = 'Save Error'
            msgText = 'No data to save.'
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            return
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile) 
        if os.path.isdir(self.lastSaveDir):
            saveDir = self.lastSaveDir
        else:
            saveDir = self.userHome
        filename = dialog.getSaveFileName(
                   None,
                   'Select data file',
                   saveDir,
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        filename = str(filename)
        if not filename:
            return
        self.lastSaveDir =  os.path.split(filename)[0]
        dataList = self.getData()
        headerStr = self.getSaveFileHeader()
        with open(filename,'w') as f:
            f.write(headerStr)
            f.write(os.linesep)
            for vals in dataList: 
                for x in vals:
                    f.write('{0}  '.format(x))
                f.write(os.linesep)

    def about_Callback(self):
        aboutText = '{0} \n\n {1}'.format(
                self.aboutText,
                constants.ABOUT_TEXT_COMMON
                )
        QtGui.QMessageBox.about(self,self.aboutCaption, aboutText)

    def haveData(self):
        return False

    def getData(self):
        return []

    def closeFigure(self): 
        if self.fig is not None and plt.fignum_exists(constants.PLOT_FIGURE_NUM): 
            plt.close(self.fig)
            self.fig = None

    def closeEvent(self,event):
        if self.fig is not None:
            plt.close(self.fig)
        if self.dev is not None:
            self.cleanUpAndCloseDevice()
        event.accept()

    def cleanUpAndCloseDevice(self):
        self.dev.close()
        self.dev = None

    def main(self):
        self.show()

class MainWindowWithTable(MainWindowCommon):

    # Temporary
    # -------------------------------------------------------------------------
    def updatePlot(self):
        pass

    def editTestSolutions_Callback(self):
        userSolutionDict = import_export.loadUserTestSolutionDict(self.userHome)
        return TestSolutionDialog().edit(userSolutionDict)

    def getMeasurement(self):
        pass

    def setTableData(self):
        pass

    # -------------------------------------------------------------------------

    def __init__(self,parent=None):
        super(MainWindowWithTable,self).__init__(parent)

    def connectActions(self):
        super(MainWindowWithTable,self).connectActions()
        self.clearPushButton.pressed.connect(self.clearPressed_Callback)
        self.clearPushButton.clicked.connect(self.clearClicked_Callback)
        for color in constants.COLOR2LED_DICT:
            button = getattr(self,'{0}RadioButton'.format(color))
            callback = functools.partial(self.colorRadioButtonClicked_Callback, color)
            button.clicked.connect(callback)
        self.plotPushButton.clicked.connect(self.plotPushButtonClicked_Callback)
        self.actionLoad.triggered.connect(self.loadFile_Callback)
        self.actionLoad.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.actionEditTestSolutions.triggered.connect(self.editTestSolutions_Callback)

    def initialize(self):
        super(MainWindowWithTable,self).initialize()
        self.lastLoadDir = self.userHome
        self.setLEDColor(constants.DFLT_LED_COLOR)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.checkUserTestSolutionDir()

    def checkUserTestSolutionDir(self):
        userTestSolutionDir = import_export.getUserTestSolutionDir(self.userHome)
        if not os.path.isdir(userTestSolutionDir):
            try:
                os.makedirs(userTestSolutionDir)
            except Exception, e:
                msgTitle = 'Setup Warning'
                msgText = 'Unable to create data directory, {0}\n{1}'.format(userTestSolutionDir,str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)

    def loadFile_Callback(self):
        """
        Load data in table from a text file.
        """
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile) 
        if os.path.isdir(self.lastLoadDir):
            loadDir = self.lastLoadDir
        else:
            loadDir = self.userHome
        filename = dialog.getOpenFileName(
                   None,
                   'Select data file',
                   loadDir,
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        filename = str(filename)
        if not filename:
            return 
        self.lastLoadDir =  os.path.split(filename)[0]
        dataList, ledColor = self.loadDataFromFile(filename)
        if ledColor is None:
            msgTitle = 'Import Warning'
            msgText = 'Unable to determine LED color from data file'
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
        else:
            self.setLEDColor(ledColor)
        self.setTableData(dataList)
        self.updateWidgetEnabled()

    def loadDataFromFile(self,filename):
        """
        Load absorbance and concentration data from data file.
        """
        try:
            fileLines = []
            with open(filename,'r') as f:
                fileLines = f.readlines()
        except IOError, e:
            msgTitle = 'File Load Error'
            msgText = 'Unable to load data file: {0}'.format(str(e))
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            return 

        dataList = []
        ledColor = None
        for line in fileLines:
            line = line.split()
            if not line:
                continue
            if 'LED' in line:
                try:
                    color = line[line.index('LED')+1].lower()
                except IndexError, e:
                    continue
                if color in constants.COLOR2LED_DICT:
                    ledColor = color
                continue
            if line[0] == '#':
                continue
            if len(line) >= 2: 
                x = ' '.join(line[:-1])
                y = line[-1]
            dataList.append((x,y))
        return dataList, ledColor

    def plotPushButtonClicked_Callback(self):
        self.updatePlot(create=True)

    def colorRadioButtonClicked_Callback(self,color):
        if len(self.tableWidget.item(0,1).text()):
            chn_msg = "Changing channels will clear all data. Continue?"
            response = self.tableWidget.clean(msg=chn_msg)
            if not response:
                self.closeFigure()
                self.setLEDColor(self.currentColor)
        self.currentColor = color

    def clearPressed_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            self.measurePushButton.setEnabled(False)
            self.plotPushButton.setEnabled(False)
        self.clearPushButton.setFlat(True)

    def clearClicked_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            erase_msg = "Clear all data?"
            rsp = self.tableWidget.clean(msg=erase_msg)
            if rsp:
                self.closeFigure()
        self.clearPushButton.setFlat(False) 
        self.updateWidgetEnabled()

    def calibratePressed_Callback(self):
        super(MainWindowWithTable,self).calibratePressed_Callback()
        self.plotPushButton.setEnabled(False)
        self.clearPushButton.setEnabled(False)

    def measurePressed_Callback(self):
        super(MainWindowWithTable,self).measurePressed_Callback()
        self.plotPushButton.setEnabled(False)

    def measureClicked_Callback(self):
        super(MainWindowWithTable,self).measureClicked_Callback()
        self.updatePlot(create=False)

    def setLEDColor(self,color):
        button = getattr(self,'{0}RadioButton'.format(color))
        button.setChecked(True)
        self.currentColor = color

    def getData(self):
        return self.tableWidget.getData(noValueSymb=self.noValueSymbol)

    def haveData(self):
        return self.tableWidget.measIndex > 0

    def updateWidgetEnabled(self):
        if self.dev is None:
            self.measurePushButton.setEnabled(False)
            self.calibratePushButton.setEnabled(False)
            if self.haveData(): 
                self.clearPushButton.setEnabled(True)
                self.plotPushButton.setEnabled(True)
                self.tableWidget.setEnabled(True)
            else:
                self.clearPushButton.setEnabled(False)
                self.plotPushButton.setEnabled(False)
                self.tableWidget.setEnabled(False)
            self.portLineEdit.setEnabled(True)
            self.statusbar.showMessage('Not Connected')
        else:
            if self.isCalibrated:
                self.plotPushButton.setEnabled(True)
                self.clearPushButton.setEnabled(True)
                self.measurePushButton.setEnabled(True)
                self.tableWidget.setEnabled(True)
            else:
                if self.haveData(): 
                    self.tableWidget.setEnabled(True)
                    self.plotPushButton.setEnabled(True)
                    self.clearPushButton.setEnabled(True)
                else:
                    self.tableWidget.setEnabled(False)
                    self.plotPushButton.setEnabled(False)
                    self.clearPushButton.setEnabled(False)
                self.measurePushButton.setEnabled(False)
            self.portLineEdit.setEnabled(False)
            self.statusbar.showMessage('Connected, Mode: Stopped')


