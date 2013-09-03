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
        modeConfig = constants.MODE_CONFIG[sensorMode]
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
        print('Basic measure pressed')
        self.setWidgetEnabledOnMeasure()
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')

    def measureClicked_Callback(self):
        super(BasicMainWindow,self).measureClicked_Callback()
        print('Basic measure clicked')
        if self.isStandardRgbLEDMode():
            self.updatePlot(create=True)
        self.updateResultsDisplay()

    def getMeasurement(self):
        if constants.DEVEL_FAKE_MEASURE:
            if self.isStandardRgbLEDMode():
                n = constants.STD_NUMBER_OF_LEDS 
                freqValues = tuple(numpy.random.random((n,)))
                tranValues = tuple(numpy.random.random((n,)))
                absoValues = tuple(numpy.random.random((n,)))
                self.measValues = freqValues, tranValues, absoValues
            elif self.isCustomVerB_LEDMode():
                freqValues = numpy.random.random((1,))[0]
                tranValues = numpy.random.random((1,))[0]
                absoValues = numpy.random.random((1,))[0]
                self.measValues = freqValues, tranValues, absoValues
            else:
                n = constants.VERC_NUMBER_OF_LEDS
                freqValues = tuple(numpy.random.random((n,)))
                tranValues = tuple(numpy.random.random((n,)))
                absoValues = tuple(numpy.random.random((n,)))
                self.measValues = freqValues, tranValues, absoValues
        else:
            error = False
            if self.isStandardRgbLEDMode():
                n = constants.STD_NUMBER_OF_LEDS 
                freqValues = [None for i in range(n)]
                tranValues = [None for i in range(n)]
                absoValues = [None for i in range(n)]
                for i in constants.LED_NUMBERS:
                    try:
                        color = constants.STD_LED_NUM_TO_COLOR[i]
                        freqValues[i], tranValues[i], absoValues[i] = self.dev.getMeasurement(color)
                    except IOError, e:
                        msgTitle = 'Measurement Error:'
                        msgText = 'unable to get {0} measurement: {0}'.format(color, str(e))
                        QtGui.QMessageBox.warning(self,msgTitle, msgText)
                        error = True
                        break
            elif self.isCustomVerB_LEDMode():
                devColor = constants.VERB_LED_DEVICE_COLOR
                try:
                    freqValues, tranValues, absoValues = self.dev.getMeasurement(devColor)
                except IOError, e: 
                    msgTitle = 'Measurement Error:'
                    msgText = 'unable to get {0} measurement: {0}'.format(color, str(e))
                    QtGui.QMessageBox.warning(self,msgTitle, msgText)
                    error = True
            else:
                n = constants.STD_NUMBER_OF_LEDS
                freqValues = [None for i in range(n)]
                tranValues = [None for i in range(n)]
                absoValues = [None for i in range(n)]
                for i, devColor in constants.VERC_LED_NUM_TO_DEVICE_COLOR:
                    if devColor is not None:
                        pass



            if error:
                self.measValues = None
            else:
                self.measValues = freqValues, tranValues, absoValues

            ##else:
            ##    measurementFunc = self.dev.getMeasurementBlue

            #try:
            #    freqValues, tranValues, absoValues = measurementFunc()
            #    self.measValues = freqValues, tranValues, absoValues
            #except IOError, e:
            #    msgTitle = 'Measurement Error:'
            #    msgText = 'unable to get measurement: {0}'.format(str(e))
            #    QtGui.QMessageBox.warning(self,msgTitle, msgText)
            #    self.measValues = None 

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

            ##########################################################################
            # TODO
            ###########################################################################

            if self.isStandardRgbLEDMode():
                tranStrList, absoStrList = [], []
                colorNames = sorted(constants.STD_LED_COLORS)
                for color in colorNames:
                    ledNum = constants.STD_LED_COLOR_TO_NUM[color] 
                    if self.isLEDChecked(ledNum):
                        tranStr = '{color}:\t{value:1.{digits}f}'.format(
                                color=color, 
                                value=tranValues[ledNum],
                                digits=digits
                                )
                        tranStrList.append(tranStr)
                        absoStr = '{color}:\t{value:1.{digits}f}'.format(
                                color=color, 
                                value=absoValues[ledNum],
                                digits=digits
                                )
                        absoStrList.append(absoStr)
                tranStr = os.linesep.join(tranStrList)
                absoStr = os.linesep.join(absoStrList)

            elif self.isCustomVerB_LEDMode():
                tranStr = 'Led {name}: \t{value:1.{digits}f}'.format(
                        name=constants.VERB_LED_TEXT,
                        value=tranValues,
                        digits=digits
                        )
                absoStr = 'Led: {name} \t{value:1.{digits}f}'.format(
                        name = constants.VERB_LED_TEXT,
                        value=absoValues,
                        digits=digits
                        )
                
            else: # self.isCustomVerC_LEDMode
                tranStrList, absoStrList = [], []
                for ledNum, ledName in constants.VERC_LED_NUM_TO_TEXT.iteritems():
                    if not ledName:
                        continue
                    if self.isLEDChecked(ledNum):
                        transStr = 'Led {name}:\t{value:1.{digits}f}'.format(
                                name=ledName,
                                value=tranValues[ledNum],
                                digits=digits
                                ) 
                        tranStrList.append(transStr)
                        absoStr = 'Led {name}:\t{value:1.{digits}f}'.format(
                                name=ledName,
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
        colorNames = sorted(constants.COLOR2LED_DICT.keys())
        dataList = []

        if self.isStandardRgbLEDMode():
            maxNameLen = max([len(c) for c in colorNames])
            for c in colorNames:
                n = constants.COLOR2LED_DICT[c]
                tran = tranValues[n]
                abso = absoValues[n]
                if self.isColorChecked(c):
                    cPadded = padString(c,maxNameLen)
                    dataList.append((cPadded,tran,abso))
        else:
            dataList.append(['custom', tranValues, absoValues])
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
            if self.isCalibrated:
                self.measurePushButton.setEnabled(True)
            else:
                self.measurePushButton.setEnabled(False)
            if self.isCalibrated and self.isStandardRgbLEDMode(): 
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

