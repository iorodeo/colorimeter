from __future__ import print_function
import os
import sys
import time
import platform
import matplotlib
import matplotlib.pyplot as plt 
plt.ion()
import numpy
import numpy.random
import functools
from PyQt4 import QtCore
from PyQt4 import QtGui

from basic_ui import Ui_MainWindow 
from colorimeter import Colorimeter
from colorimeter import constants
from colorimeter.main_window import MainWindowCommon

DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 

class BasicMainWindow(MainWindowCommon,Ui_MainWindow):

    def __init__(self,parent=None):
        super(BasicMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        super(BasicMainWindow,self).connectActions()
        self.plotCheckBox.stateChanged.connect(self.plotCheckBox_Callback)
        for ledNum in constants.LED_NUMBERS:
            checkBox = getattr(self,'LED{0}CheckBox'.format(ledNum))
            checkBox.stateChanged.connect(self.ledCheckBox_Callback)

    def initialize(self):
        super(BasicMainWindow,self).initialize()
        self.measValues = None
        self.aboutText = constants.BASIC_ABOUT_TEXT
        for ledNum in constants.LED_NUMBERS:
            checkBox = getattr(self,'LED{0}CheckBox'.format(ledNum))
            checkBox.setCheckState(QtCore.Qt.Checked)
        self.plotCheckBox.setCheckState(QtCore.Qt.Checked)
        self.updateWidgetEnabled()

    def setMode(self,sensorMode):
        super(BasicMainWindow,self).setMode(sensorMode)
        modeConfig = self.getModeConfig(sensorMode)
        self.LEDLabel.setVisible(modeConfig['LEDLabelVisible'])
        for ledNum in constants.LED_NUMBERS:
            checkBox = getattr(self,'LED{0}CheckBox'.format(ledNum))
            try:
                ledValues = modeConfig['LED'][ledNum]
            except KeyError:
                checkBox.setVisible(False)
                checkBox.setText('')
                continue
            checkBox.setVisible(ledValues['visible'])
            checkBox.setText(ledValues['text'])
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.measValues = None
        self.closeFigure()

    def ledCheckBox_Callback(self):
        self.updateResultsDisplay()
        if self.plotCheckBox.isChecked():
            create = True
        else:
            create = False
        self.updatePlot(create=create)

    def plotCheckBox_Callback(self,value):
        if value == QtCore.Qt.Unchecked:
            if self.fig is not None:
                self.closeFigure()
        else:
            self.updatePlot(create=True)

    def calibratePressed_Callback(self):
        super(BasicMainWindow,self).calibratePressed_Callback()
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.setWidgetEnabledOnMeasure()

    def calibrateClicked_Callback(self):
        super(BasicMainWindow,self).calibrateClicked_Callback()
        if self.isCalibrated: 
            freq = None  
            tran = 1.0, 1.0, 1.0, 1.0
            abso = 0.0, 0.0, 0.0, 0.0
            self.measValues = freq, tran, abso
        self.updateResultsDisplay()

    def measurePressed_Callback(self):
        super(BasicMainWindow,self).measurePressed_Callback()
        self.setWidgetEnabledOnMeasure()
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')

    def measureClicked_Callback(self):
        super(BasicMainWindow,self).measureClicked_Callback()
        modeConfig = self.getModeConfig()
        if len(modeConfig['LED']) > 1: 
            self.updatePlot(create=True)
        self.updateResultsDisplay()

    def getMeasurement(self):
        modeConfig = self.getModeConfig()
        if constants.DEVEL_FAKE_MEASURE:
            n = len(modeConfig['LED'])
            freqValues = tuple(numpy.random.random((n,)))
            tranValues = tuple(numpy.random.random((n,)))
            absoValues = tuple(numpy.random.random((n,)))
            self.measValues = freqValues, tranValues, absoValues
        else:
            error = False
            n = len(modeConfig['LED']) 
            freqValues = [None for i in range(n)]
            tranValues = [None for i in range(n)]
            absoValues = [None for i in range(n)]
            for i, ledNum  in enumerate(modeConfig['LED']):
                devColor = modeConfig['LED'][ledNum]['devColor']
                try:
                    freqValues[i], tranValues[i], absoValues[i] = self.dev.getMeasurement(devColor)
                except IOError, e: 
                    msgTitle = 'Measurement Error:'
                    msgText = 'unable to get {0} measurement: {0}'.format(color, str(e))
                    QtGui.QMessageBox.warning(self,msgTitle, msgText)
                    error = True
                    break
            if error:
                self.measValues = None
            else:
                self.measValues = freqValues, tranValues, absoValues

    def updatePlot(self,create=False):
        modeConfig = self.getModeConfig()
        if not create and not plt.fignum_exists(constants.PLOT_FIGURE_NUM):
            return
        if self.measValues is None:
            return
        freqValues, tranValues, absoValues = self.measValues

        if self.plotCheckBox.isChecked():
            barWidth = constants.PLOT_BAR_WIDTH 
            xLabelList, absoList = [], []
            for ledNum, ledDict in modeConfig['LED'].iteritems():
                if self.isLEDChecked(ledNum):
                    xLabelList.append(ledDict['text'])
                    absoList.append(absoValues[ledNum])
            if not absoList:
                self.closeFigure()
                return

            posList = range(1,len(absoList)+1)
            yticks = 0.5*numpy.arange(0.0,2.0*max([max(absoList),1.0]))
            xlim = (
                    posList[0]  - 0.5*constants.PLOT_BAR_WIDTH, 
                    posList[-1] + 1.5*constants.PLOT_BAR_WIDTH,
                    )
            ylim = (0,max(constants.PLOT_YLIM_ADJUST*max(absoList),1.0))
            plt.clf()
            self.fig = plt.figure(constants.PLOT_FIGURE_NUM)
            self.fig.canvas.manager.set_window_title('Colorimeter Basic: Absorbance Plot')
            ax = self.fig.add_subplot(111)

            for y in yticks[1:]:
                ax.plot(xlim,[y,y],'k:')

            digits = self.getSignificantDigits()
            for p, a, c in zip(posList, absoList, xLabelList): 
                colorSymb = constants.PLOT_COLOR_DICT[c]
                ax.bar([p],[a],width=barWidth,color=colorSymb,linewidth=2)
                textXPos = p+0.5*barWidth
                textYPos = a+0.01
                valueStr = '{value:1.{digits}f}'.format(value=a,digits=digits)
                ax.text(textXPos,textYPos,valueStr,ha ='center',va ='bottom')

            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
            ax.set_xticks([x+0.5*barWidth for x in posList])
            ax.set_xticklabels(xLabelList)
            ax.set_ylabel('Absorbance')
            ax.set_xlabel('LED')
            ax.set_yticks(yticks)
            plt.draw() 

    def updateResultsDisplay(self):
        if self.measValues is None:
            self.transmissionTextEdit.setText('')
            self.absorbanceTextEdit.setText('')
        else:
            freqValues, tranValues, absoValues = self.measValues
            digits = self.getSignificantDigits()
            modeConfig = self.getModeConfig()
            tranStrList, absoStrList = [], []
            for ledNum, ledDict in modeConfig['LED'].iteritems():
                if self.isLEDChecked(ledNum):
                    tranStr = '{color}:\t{value:1.{digits}f}'.format(
                            color=ledDict['text'], 
                            value=tranValues[ledNum],
                            digits=digits
                            )
                    tranStrList.append(tranStr)
                    absoStr = '{color}:\t{value:1.{digits}f}'.format(
                            color=ledDict['text'], 
                            value=absoValues[ledNum],
                            digits=digits
                            )
                    absoStrList.append(absoStr)
            tranStr = os.linesep.join(tranStrList)
            absoStr = os.linesep.join(absoStrList)
            self.transmissionTextEdit.setText(tranStr)
            self.absorbanceTextEdit.setText(absoStr)

    def isLEDChecked(self,ledNum):
        checkBox = getattr(self,'LED{0}CheckBox'.format(ledNum))
        return checkBox.isChecked()

    def getData(self):
        freqValues, tranValues, absoValues = self.measValues
        modeConfig = self.getModeConfig()
        maxNameLen = max([len(d['text']) for d in modeConfig['LED'].values()])
        dataList = []
        for ledNum, ledDict in modeConfig['LED'].iteritems():
            tran = tranValues[ledNum]
            abso = absoValues[ledNum]
            if self.isLEDChecked(ledNum):
                textPadded = padString(ledDict['text'],maxNameLen)
                dataList.append((textPadded,tran,abso))
        return dataList

    def haveData(self):
        if self.measValues is None:
            return False
        else:
            return True

    def getSaveFileHeader(self):
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S %Z') 
        headerList = [ 
                '# {0}'.format(timeStr),
                '# Colorimeter Data', 
                '# --------------------------------', 
                '# LED | Transmittance | Absorbance', 
                ]
        headerStr = os.linesep.join(headerList)
        return headerStr

    def setWidgetEnabledOnMeasure(self):
        self.transmissionTextEdit.setEnabled(False)
        self.absorbanceTextEdit.setEnabled(False)
        self.transmissionGroupBox.setEnabled(False)
        self.absorbanceGroupBox.setEnabled(False)
        self.samplesLineEdit.setEnabled(False)
        self.setLEDCheckBoxesEnabled(False)
        self.plotCheckBox.setEnabled(False)

    def updateWidgetEnabled(self):
        super(BasicMainWindow,self).updateWidgetEnabled()
        if self.dev is None:
            self.transmissionTextEdit.setEnabled(False)
            self.absorbanceTextEdit.setEnabled(False)
            self.calibratePushButton.setEnabled(False)
            self.measurePushButton.setEnabled(False)
            self.transmissionGroupBox.setEnabled(False)
            self.absorbanceGroupBox.setEnabled(False)
            self.setLEDCheckBoxesEnabled(False)
            self.portLineEdit.setEnabled(True)
            self.plotCheckBox.setEnabled(False)
            self.LEDLabel.setEnabled(False)
            self.statusbar.showMessage('Not Connected')
        else:
            self.transmissionTextEdit.setEnabled(True)
            self.absorbanceTextEdit.setEnabled(True)
            self.calibratePushButton.setEnabled(True)
            self.transmissionGroupBox.setEnabled(True)
            self.absorbanceGroupBox.setEnabled(True)
            self.portLineEdit.setEnabled(False)
            modeConfig = self.getModeConfig()
            if self.isCalibrated:
                self.measurePushButton.setEnabled(True)
            else:
                self.measurePushButton.setEnabled(False)
            if self.isCalibrated and (len(modeConfig['LED']) > 1): 
                self.setLEDCheckBoxesEnabled(True)
                self.plotCheckBox.setEnabled(True)
            else:
                self.setLEDCheckBoxesEnabled(False)
                self.plotCheckBox.setEnabled(False)
            self.statusbar.showMessage('Connected, Stopped')

    def setLEDCheckBoxesEnabled(self,value): 
        for ledNum in constants.LED_NUMBERS: 
            checkBox = getattr(self,'LED{0}CheckBox'.format(ledNum))
            checkBox.setEnabled(value)


def padString(x,n):
    if len(x) < n:
        d = n - len(x)
        xNew = '{0}{1}'.format(x,' '*d)
    else:
        xNew = x
    return xNew


def startBasicMainWindow(app):
    mainWindow = BasicMainWindow()
    mainWindow.main()
    app.exec_()

def startBasicApp():
    app = QtGui.QApplication(sys.argv)
    startBasicMainWindow(app)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    startBasicApp()

