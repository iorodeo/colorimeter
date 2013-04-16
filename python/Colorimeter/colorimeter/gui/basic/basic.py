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
        self.samplesLineEdit.editingFinished.connect(self.samplesChanged_Callback)
        self.plotCheckBox.stateChanged.connect(self.plotCheckBox_Callback)
        for color in constants.COLOR2LED_DICT:
            checkBox = getattr(self,'{0}CheckBox'.format(color))
            callback = functools.partial(self.colorCheckBox_Callback,color)
            checkBox.stateChanged.connect(callback)

    def initialize(self):
        super(BasicMainWindow,self).initialize()
        self.measValues = None
        self.numSamples = None
        self.aboutText = constants.BASIC_ABOUT_TEXT
        self.samplesValidator = QtGui.QIntValidator(0,2**16-1,self.samplesLineEdit)
        self.samplesLineEdit.setValidator(self.samplesValidator)
        for name in constants.COLOR2LED_DICT:
            checkBox = getattr(self,'{0}CheckBox'.format(name))
            checkBox.setCheckState(QtCore.Qt.Checked)
        self.plotCheckBox.setCheckState(QtCore.Qt.Checked)
        self.updateWidgetEnabled()

    def standardRgbLed_Callback(self): 
        changed = super(BasicMainWindow,self).standardRgbLed_Callback()
        if changed:
            self.transmissionTextEdit.setText('')
            self.absorbanceTextEdit.setText('')
            self.measValues = None
        self.updateWidgetEnabled()

    def customLed_Callback(self): 
        changed = super(BasicMainWindow,self).customLed_Callback()
        if changed:
            self.transmissionTextEdit.setText('')
            self.absorbanceTextEdit.setText('')
            self.measValues = None
            self.closeFigure()
        self.updateWidgetEnabled()

    def colorCheckBox_Callback(self,color):
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

    def connectClicked_Callback(self):
        super(BasicMainWindow,self).connectClicked_Callback()
        if self.dev is None:
            self.samplesLineEdit.setText('')
        else:
            self.samplesLineEdit.setText('{0}'.format(self.numSamples))

    def calibratePressed_Callback(self):
        super(BasicMainWindow,self).calibratePressed_Callback()
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.setWidgetEnabledOnMeasure()

    def calibrateClicked_Callback(self):
        super(BasicMainWindow,self).calibrateClicked_Callback()
        if self.isCalibrated:
            if self.isStandardRgbLedMode():
                freq = None  
                tran = 1.0, 1.0, 1.0, 1.0
                abso = 0.0, 0.0, 0.0, 0.0
            else:
                freq = None
                tran = 1.0
                abso = 0.0
            self.measValues = freq, tran, abso
        self.updateResultsDisplay()

    def measurePressed_Callback(self):
        super(BasicMainWindow,self).measurePressed_Callback()
        self.setWidgetEnabledOnMeasure()
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')

    def measureClicked_Callback(self):
        super(BasicMainWindow,self).measureClicked_Callback()
        if self.isStandardRgbLedMode():
            self.updatePlot(create=True)
        self.updateResultsDisplay()

    def getMeasurement(self):
        if constants.DEVEL_FAKE_MEASURE:
            if self.isStandardRgbLedMode():
                freqValues = tuple(numpy.random.random((4,)))
                tranValues = tuple(numpy.random.random((4,)))
                absoValues = tuple(numpy.random.random((4,)))
                self.measValues = freqValues, tranValues, absoValues
            else:
                freqValues = numpy.random.random((1,))[0]
                tranValues = numpy.random.random((1,))[0]
                absoValues = numpy.random.random((1,))[0]
                self.measValues = freqValues, tranValues, absoValues
        else:
            if self.isStandardRgbLedMode():
                measurementFunc = self.dev.getMeasurement
            else:
                measurementFunc = self.dev.getMeasurementBlue

            try:
                freqValues, tranValues, absoValues = measurementFunc()
                self.measValues = freqValues, tranValues, absoValues
            except IOError, e:
                msgTitle = 'Measurement Error:'
                msgText = 'unable to get measurement: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                self.measValues = None 

    def updatePlot(self,create=False):
        if not create and not plt.fignum_exists(constants.PLOT_FIGURE_NUM):
            return
        if self.measValues is None:
            return
        freqValues, tranValues, absoValues = self.measValues

        if self.plotCheckBox.isChecked():
            barWidth = constants.PLOT_BAR_WIDTH 
            colorNames = sorted(constants.COLOR2LED_DICT.keys())

            xLabelList = []
            absoList= []

            for c in colorNames:
                ledNumber = constants.COLOR2LED_DICT[c]
                a = absoValues[ledNumber]
                if self.isColorChecked(c):
                    xLabelList.append(c) 
                    absoList.append(a)
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

            for p, a, c in zip(posList, absoList, xLabelList): 
                colorSymb = constants.PLOT_COLOR_DICT[c]
                ax.bar([p],[a],width=barWidth,color=colorSymb,linewidth=2)
                textXPos = p+0.5*barWidth
                textYPos = a+0.01
                valueStr = '{0:1.3f}'.format(a)
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
            if self.isStandardRgbLedMode():
                tranStrList, absoStrList = [], []
                colorNames = sorted(constants.COLOR2LED_DICT)
                for c in colorNames:
                    n = constants.COLOR2LED_DICT[c] 
                    if self.isColorChecked(c):
                        tranStrList.append('{0}:\t{1:1.3f}'.format(c, tranValues[n]))
                        absoStrList.append('{0}:\t{1:1.3f}'.format(c, absoValues[n]))
                tranStr = os.linesep.join(tranStrList)
                absoStr = os.linesep.join(absoStrList)
            else:
                tranStr = 'custom led: \t{0:1.3f}'.format(tranValues)
                absoStr = 'custom led: \t{0:1.3f}'.format(absoValues)
            self.transmissionTextEdit.setText(tranStr)
            self.absorbanceTextEdit.setText(absoStr)

    def isColorChecked(self,color):
        checkBox = getattr(self,'{0}CheckBox'.format(color))
        return checkBox.isChecked()

    def samplesChanged_Callback(self):
        valueStr = str(self.samplesLineEdit.text())
        value = int(valueStr)
        if value != self.numSamples:
            self.numSamples = value
            self.dev.setNumSamples(value)

    def getData(self):
        freqValues, tranValues, absoValues = self.measValues
        colorNames = sorted(constants.COLOR2LED_DICT.keys())
        dataList = []
        maxNameLen = max([len(c) for c in colorNames])
        for c in colorNames:
            n = constants.COLOR2LED_DICT[c]
            tran = tranValues[n]
            abso = absoValues[n]
            if self.isColorChecked(c):
                cPadded = padString(c,maxNameLen)
                dataList.append((cPadded,tran,abso))
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
        self.redCheckBox.setEnabled(False)
        self.greenCheckBox.setEnabled(False)
        self.blueCheckBox.setEnabled(False)
        self.whiteCheckBox.setEnabled(False)
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
            self.samplesLineEdit.setEnabled(False)
            self.redCheckBox.setEnabled(False)
            self.greenCheckBox.setEnabled(False)
            self.blueCheckBox.setEnabled(False)
            self.whiteCheckBox.setEnabled(False)
            self.portLineEdit.setEnabled(True)
            self.plotCheckBox.setEnabled(False)
            self.ledsLabel.setEnabled(False)
            self.statusbar.showMessage('Not Connected')
        else:
            self.transmissionTextEdit.setEnabled(True)
            self.absorbanceTextEdit.setEnabled(True)
            self.calibratePushButton.setEnabled(True)
            self.transmissionGroupBox.setEnabled(True)
            self.absorbanceGroupBox.setEnabled(True)
            self.samplesLineEdit.setEnabled(True)
            self.portLineEdit.setEnabled(False)
            if self.isCalibrated:
                self.measurePushButton.setEnabled(True)
            else:
                self.measurePushButton.setEnabled(False)
            if self.isCalibrated and self.isStandardRgbLedMode(): 
                self.redCheckBox.setEnabled(True)
                self.greenCheckBox.setEnabled(True)
                self.blueCheckBox.setEnabled(True)
                self.whiteCheckBox.setEnabled(True)
                self.plotCheckBox.setEnabled(True)
            else:
                self.redCheckBox.setEnabled(False)
                self.greenCheckBox.setEnabled(False)
                self.blueCheckBox.setEnabled(False)
                self.whiteCheckBox.setEnabled(False)
                self.plotCheckBox.setEnabled(False)
            self.statusbar.showMessage('Connected, Stopped')

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

