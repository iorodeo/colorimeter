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
        # WBD DEVEL
        self.sensorMode = 'StandardRGBLED'
        #self.sensorMode = 'CustomLEDVerB'
        #self.sensorMode = 'CustomLEDVerC'
        self.numSamples = None

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

        self.setMode(self.sensorMode)

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
        else:
            self.isCalibrated = True
        self.calibratePushButton.setFlat(False)
        self.updateWidgetEnabled()

    def measurePressed_Callback(self):
        self.calibratePushButton.setEnabled(False)
        self.measurePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Measuring...')

    def measureClicked_Callback(self):
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
            try:
                sensorMode = self.sensorMode
            except AttributeError:
                # Dummy value used when setting up widges prior to initialization
                sensorMode = 'StandardRGBLED' 
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
        return self.actionCustomLEDVerC.isChecked()

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

    def getLEDText(self,num=None):
        modeConfig = self.getModeConfig()
        if num is None:
            num = self.currentLED
        return modeConfig['LED'][num]['text']

    def getLEDSaveInfoStr(self):
        if self.isStandardRgbLEDMode():
            ledInfoStr = self.getLEDText()
        else:
            ledText = self.getLEDText()
            ledInfoStr = '{0} {1}'.format(ledText, self.sensorMode)
        return ledInfoStr


    def main(self):
        self.show()
        self.raise_()

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
        modeConfig = self.getModeConfig()

        for num in modeConfig['LED']:
            button = getattr(self,'LED{0}RadioButton'.format(num))
            callback = functools.partial(self.LEDRadioButtonClicked_Callback,num)
            button.clicked.connect(callback)
        self.plotPushButton.clicked.connect(self.plotPushButtonClicked_Callback)
        self.actionLoad.triggered.connect(self.loadFile_Callback)
        self.actionLoad.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.actionEditTestSolutions.triggered.connect(self.editTestSolutions_Callback)

    def initialize(self):
        #self.setLED(0) # default is first led 
        super(MainWindowWithTable,self).initialize()
        self.setLED(0) # default is first led 
        self.lastLoadDir = self.userHome
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
        self.setLED(0)
        super(MainWindowWithTable,self).setMode(value)
        self.tableWidget.clean(True,'')
        self.setLEDChecks()
        self.setLEDText()
        self.setLEDVisible()

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
        dataList, ledColor, sensorMode, units = self.loadDataFromFile(filename)

        if ledColor is None:
            msgTitle = 'Import Warning'
            msgText = 'Unable to determine LED from data file' 
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
        else:
            standardLEDColors = self.getAllowedLEDColors('StandardRGBLED')
            if sensorMode is None and ledColor in standardLEDColors:
                sensorMode = 'StandardRGBLED'

            modeConfig = self.getModeConfig()
            allowedSensorModes = self.getAllowedSensorModes()
            if not sensorMode in allowedSensorModes:
                msgTitle = 'Import Warning'
                msgText = 'Unknown sensor mode, {0}, in data file'.format(sensorMode)
                QtGui.QMessageBox.warning(self,msgTitle, msgText)

            allowedColors = self.getAllowedLEDColors(sensorMode)
            if ledColor in allowedColors:
                self.setMode(sensorMode)
                self.setLEDByText(ledColor)
            else:
                msgTitle = 'Import Warning'
                msgText = 'Unknown LED color for given mode, {0}, in data file'.format(ledColor)
                QtGui.QMessageBox.warning(self,msgTitle, msgText)

        self.setUnits(units);

        self.setTableData(dataList)
        self.updateWidgetEnabled()
        self.updatePlot(create=False)

    def getAllowedLEDColors(self,sensorMode): 
        modeConfig = self.getModeConfig(sensorMode)
        allowedColors = [v['text'] for k,v in modeConfig['LED'].iteritems()]
        return allowedColors

    def getAllowedSensorModes(self):
        return constants.MODE_CONFIG_DICT.keys()

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
        sensorMode = None
        units = 'uM'

        for line in fileLines:
            line = line.split()
            if not line:
                continue
            if line[0] == '#':
                if 'LED' in line:
                    colorIndex = line.index('LED')+1
                    sensorModeIndex = colorIndex+1
                    try:
                        ledColor = line[colorIndex]
                    except IndexError, e:
                        continue
                    try:
                        sensorMode = line[sensorModeIndex]
                    except IndexError, e:
                        continue
                    if ledColor == 'custom':
                        # For backwards compatibility
                        ledColor = 'D1'
                        sensorMode = 'CustomLEDVerB'
                        continue
                    continue
                if ('Label' in line) or ('Absorbance' in line):
                    if 'uM' in line:
                        units = 'uM'
                    if 'ppm' in line:
                        units = 'ppm'
                    if 'pH' in line:
                        units = 'pH'
                continue
            if len(line) >= 2: 
                x = ' '.join(line[:-1])
                y = line[-1]
            dataList.append((x,y))
        return dataList, ledColor, sensorMode, units

    def plotPushButtonClicked_Callback(self):
        self.updatePlot(create=True)

    def LEDRadioButtonClicked_Callback(self,num):
        if len(self.tableWidget.item(0,1).text()):
            chnMsg = 'Changing channels will clear all data. Continue?'
            response = self.tableWidget.clean(msg=chnMsg)
            if not response:
                self.closeFigure()
                self.setLED(self.currentLED)
        self.currentLED = num 

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

    def setLED(self,num):
        button = getattr(self,'LED{0}RadioButton'.format(num))
        button.setChecked(True)
        self.currentLED = num

    def setLEDByText(self,ledText):
        modeConfig = self.getModeConfig()
        text2Num = dict([(d['text'], n) for n, d in modeConfig['LED'].iteritems()])
        ledNum = text2Num[ledText]
        self.setLED(ledNum)

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

    def setLEDChecks(self):
        modeConfig = self.getModeConfig()
        for ledNum, ledDict in modeConfig['LED'].iteritems():
            button = getattr(self,'LED{0}RadioButton'.format(ledNum))
            button.setCheckable(True)
            if ledNum == self.currentLED:
                button.setChecked(True)
            else:
                button.setChecked(False)

    def setLEDText(self):
        modeConfig = self.getModeConfig()
        for ledNum, ledDict in modeConfig['LED'].iteritems():
            button = getattr(self,'LED{0}RadioButton'.format(ledNum))
            button.setText(ledDict['text'])

    def setLEDVisible(self):
        modeConfig = self.getModeConfig()
        for ledNum in constants.LED_NUMBERS:
            button = getattr(self,'LED{0}RadioButton'.format(ledNum))
            if ledNum in modeConfig['LED']:
                button.setVisible(True)
            else:
                button.setVisible(False)





               

                

           

