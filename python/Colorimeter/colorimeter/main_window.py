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
        self.samplesLineEdit.editingFinished.connect(self.samplesChanged_Callback)
        self.samplesValidator = QtGui.QIntValidator(0,2**16-1,self.samplesLineEdit)
        self.samplesLineEdit.setValidator(self.samplesValidator)
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

        self.modeActionGroup = QtGui.QActionGroup(self)
        self.modeActionGroup.addAction(self.actionStandardRGBLED)
        self.modeActionGroup.addAction(self.actionCustomLEDVerB)
        self.modeActionGroup.addAction(self.actionCustomLEDVerC)
        self.modeActionGroup.setExclusive(True)
        self.actionStandardRGBLED.setChecked(True)

        standardRgbLED_Callback = functools.partial(self.sensorMode_Callback,'StandardRGBLED')
        self.actionStandardRGBLED.triggered.connect(standardRgbLED_Callback)
        customVerB_Callback = functools.partial(self.sensorMode_Callback,'CustomLEDVerB')
        self.actionCustomLEDVerB.triggered.connect(customVerB_Callback)
        customVerC_Callback = functools.partial(self.sensorMode_Callback,'CustomLEDVerC')
        self.actionCustomLEDVerC.triggered.connect(customVerC_Callback)

        self.significantDigitActionGroup = QtGui.QActionGroup(self)
        self.significantDigitActionGroup.setExclusive(True)
        self.significantDigitAction2Value = {}
        
        for i in constants.SIGNIFICANT_DIGITS_LIST:
            actionName = 'actionSignificantDigits{0}'.format(i)
            action = QtGui.QAction(self.menuSignificantDigits)
            action.setCheckable(True)
            action.setText('{0}'.format(i))
            self.menuSignificantDigits.addAction(action)
            self.significantDigitActionGroup.addAction(action)
            if i == constants.DEFAULT_SIGNIFICANT_DIGIT_INDEX:
                action.setChecked(True)
            self.significantDigitAction2Value[action] = i

    def initialize(self):
        self.setAppSize()
        self.dev = None
        self.fig = None
        self.isCalibrated = False
        self.aboutCaption = 'About'
        self.aboutText = 'About Default Text'
        self.sensorMode = 'StandardRGBLED'
        self.numSamples = None
        self.setMode(self.sensorMode)

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
        if self.dev is None:
            self.connectPushButton.setText('Disconnect')
            self.connectPushButton.setFlat(True)
            self.portLineEdit.setEnabled(False)
            self.statusbar.showMessage('Connecting...')

    def connectClicked_Callback(self):
        if self.dev is None:
            self.connectDevice()
        else:
            self.disconnectDevice()
        self.updateWidgetEnabled()
        self.connectPushButton.setFlat(False)

    def connectDevice(self):
        if constants.DEVEL_FAKE_MEASURE:
            self.dev = 'dummy' 
        else:
            try:
                self.dev = Colorimeter(self.port)
                self.numSamples = self.dev.getNumSamples()
            except Exception, e:
                msgTitle = 'Connection Error'
                msgText = 'unable to connect to device: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                self.connectPushButton.setText('Connect')
                self.statusbar.showMessage('Not Connected')
                self.dev = None
            if self.dev is not None:
                modeConfig = self.getModeConfig()
                self.setDeviceColorMode(modeConfig['colorMode'])
                self.samplesLineEdit.setText('{0}'.format(self.numSamples))

    def disconnectDevice(self):
        if constants.DEVEL_FAKE_MEASURE:
            self.dev = None
        else:
            self.connectPushButton.setText('Connect')
            try:
                self.cleanUpAndCloseDevice()
            except Exception, e:
                QtGui.QMessageBox.critical(self,'Error', str(e))
        self.samplesLineEdit.setText('')

    def samplesChanged_Callback(self):
        valueStr = str(self.samplesLineEdit.text())
        value = int(valueStr)
        if value != self.numSamples:
            self.numSamples = value
            if self.dev is not None:
                self.dev.setNumSamples(value)

    def calibratePressed_Callback(self):
        self.measurePushButton.setEnabled(False)
        self.calibratePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Calibrating...')

    def calibrateClicked_Callback(self):
        if not constants.DEVEL_FAKE_MEASURE: 
            modeConfig = self.getModeConfig()
            error = False
            for ledNum, ledValues in modeConfig['LED'].iteritems():
                try:
                    self.dev.calibrate(ledValues['devColor'])
                except IOError, e:
                    msgTitle = 'Calibration Error:'
                    msgText = 'unable to calibrate device: {0}'.format(str(e))
                    QtGui.QMessageBox.warning(self,msgTitle, msgText)
                    error = True
            if error:
                self.isCalibrated = False
            else:
                self.isCalibrated = True

            #try:
            #    if self.isStandardRgbLEDMode():
            #        self.dev.calibrate()
            #    elif self.isCustomVerB_LEDMode():
            #        self.dev.calibrate(constants.VERB_LED_DEVICE_COLOR)
            #    else: 
            #        for ledNum in constants.LED_NUMBERS:
            #            devColor = constants.VERC_LED_NUM_TO_DEVICE_COLOR[ledNum]
            #            if devColor is not None:
            #                self.dev.calibrate(devColor)
            #    self.isCalibrated = True
            #except IOError, e:
            #    msgTitle = 'Calibration Error:'
            #    msgText = 'unable to calibrate device: {0}'.format(str(e))
            #    QtGui.QMessageBox.warning(self,msgTitle, msgText)
            #    self.updateWidgetEnabled()
        else:
            self.isCalibrated = True
        self.calibratePushButton.setFlat(False)
        self.updateWidgetEnabled()

    def measurePressed_Callback(self):
        print('measure pressed')
        self.calibratePushButton.setEnabled(False)
        self.measurePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Measuring...')

    def measureClicked_Callback(self):
        print('measure clicked')
        self.getMeasurement()
        self.measurePushButton.setFlat(False)
        self.updateWidgetEnabled()



    def getMeasurement():
        pass

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

    def sensorMode_Callback(self,newSensorMode):
        if (self.dev is not None) and (newSensorMode != self.sensorMode): 
            if self.haveData():
                reply = QtGui.QMessageBox.question(
                        self, 
                        'Message', 
                        'Changing sensor mode will clear all data. Continue?', 
                        QtGui.QMessageBox.Yes, 
                        QtGui.QMessageBox.No
                        )
            else:
                reply = QtGui.QMessageBox.Yes

            if reply == QtGui.QMessageBox.Yes:
                self.setMode(newSensorMode)
            else:
                self.sensorModeSetChecked(self.sensorMode)


    def sensorModeSetChecked(self,sensorMode):
        modeAction = getattr(self, 'action{0}'.format(sensorMode))
        modeAction.setChecked(True)


    def setMode(self,sensorMode):
        self.sensorModeSetChecked(sensorMode)
        modeConfig = self.getModeConfig(sensorMode)
        if (self.dev is not None) and (not constants.DEVEL_FAKE_MEASURE):
            self.setDeviceColorMode(modeConfig['colorMode'])
        self.isCalibrated = False
        self.sensorMode = sensorMode 
        self.updateWidgetEnabled()

    def getModeConfig(self,sensorMode=None):
        if sensorMode == None:
            sensorMode = self.sensorMode
        return constants.MODE_CONFIG_DICT[sensorMode]

    def setDeviceColorMode(self,colorMode): 
        try:
            if colorMode == 'specific':
                self.dev.setSensorModeColorSpecific()
            else:
                self.dev.setSensorModeColorIndependent()
        except Exception, e:
            msgTitle = 'Set LED Mode Error'
            msgText = 'error setting device LED mode: {0}'.format(str(e))
            QtGui.QMessageBox.warning(self,msgTitle, msgText)

    def isStandardRgbLEDMode(self):
        return self.actionStandardRGBLED.isChecked()

    def isCustomVerB_LEDMode(self):
        return self.actionCustomLEDVerB.isChecked()

    def isCustomVerC_LEDMode(self):
        return self.actionCustomLEDVerB.isChecked()

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
        if not constants.DEVEL_FAKE_MEASURE:    
            self.dev.close()
        self.dev = None

    def updateWidgetEnabled(self):
        if self.dev is None:
            self.actionStandardRGBLED.setEnabled(False)
            self.actionCustomLEDVerB.setEnabled(False)
            self.actionCustomLEDVerC.setEnabled(False)
            self.samplesLineEdit.setEnabled(False)
        else:
            self.actionStandardRGBLED.setEnabled(True)
            self.actionCustomLEDVerB.setEnabled(True)
            self.actionCustomLEDVerC.setEnabled(True)
            self.samplesLineEdit.setEnabled(True)

    def getSignificantDigits(self):
        for action, value in self.significantDigitAction2Value.iteritems():
            if action.isChecked():
                return value

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
        self.setLEDColor(constants.STD_DFLT_LED_COLOR)
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

    def setMode(self,value):
        super(MainWindowWithTable,self).setMode(value)
        if value == 'StandardRGBLED':
            self.tableWidget.clean(True,'')
            self.setColorLEDChecks()
        elif value == 'custom':
            self.tableWidget.clean(True,'')
            self.clearColorLEDChecks()
        else:
            raise ValueError, 'unkown LED mode {0}'.format(value)

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
            if ledColor in constants.COLOR2LED_DICT:
                self.setMode('StandardRGBLED')
                self.setLEDColor(ledColor)
            elif ledColor == 'custom':
                self.setMode('custom')
            else:
                msgTitle = 'Import Warning'
                msgText = 'Unknown LED color, {0}, in data file'.format(ledColor)
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
        self.setTableData(dataList)
        self.updateWidgetEnabled()
        self.updatePlot(create=False)

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
                if color in constants.COLOR2LED_DICT or color=='custom':
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
        super(MainWindowWithTable,self).updateWidgetEnabled()
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
            self.statusbar.showMessage('Connected, Stopped')

    def clearColorLEDChecks(self):
        for color in constants.COLOR2LED_DICT:
            button = getattr(self,'{0}RadioButton'.format(color))
            button.setChecked(False)
            button.setCheckable(False)

    def setColorLEDChecks(self):
        for color in constants.COLOR2LED_DICT:
            button = getattr(self,'{0}RadioButton'.format(color))
            button.setCheckable(True)
            if color == self.currentColor:
                button.setChecked(True)
            else:
                button.setChecked(False)

           

