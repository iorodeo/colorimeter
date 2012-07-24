from __future__ import print_function
import os
import sys
import platform
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt 
import numpy
import numpy.random
import functools
from PyQt4 import QtCore
from PyQt4 import QtGui

from colorimeter_basic_gui_ui import Ui_MainWindow 
from colorimeter_serial import Colorimeter
from colorimeter_common import constants

DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 

class BasicMainWindow(QtGui.QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(BasicMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        self.connectPushButton.pressed.connect(self.connectPressed_Callback)
        self.connectPushButton.clicked.connect(self.connectClicked_Callback)
        self.calibratePushButton.pressed.connect(self.calibratePressed_Callback)
        self.calibratePushButton.clicked.connect(self.calibrateClicked_Callback)
        self.measurePushButton.clicked.connect(self.measureClicked_Callback)
        self.measurePushButton.pressed.connect(self.measurePressed_Callback)
        self.samplesLineEdit.editingFinished.connect(self.samplesChanged_Callback)
        self.plotCheckBox.stateChanged.connect(self.plotCheckBox_Callback)
        for color in constants.COLOR2LED_DICT:
            checkBox = getattr(self,'{0}CheckBox'.format(color))
            callback = functools.partial(self.colorCheckBox_Callback,color)
            checkBox.stateChanged.connect(callback)
        self.actionSave.triggered.connect(self.saveFile_Callback)
        self.actionSave.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_S)

    def saveFile_Callback(self):
        print('saveFile_Callback')

    def colorCheckBox_Callback(self,color):
        self.updateResultsDisplay()
        self.updatePlot()

    def plotCheckBox_Callback(self,value):
        if value == QtCore.Qt.Unchecked:
            if self.fig is not None:
                plt.close(self.fig)
                self.fig = None
        else:
            if self.fig is None:
                self.updatePlot(create=True)

    def initialize(self):
        self.dev = None
        self.fig = None
        self.measValues = None
        self.numSamples = None
        self.isCalibrated = False
        osType = platform.system()
        if osType == 'Linux': 
            self.port = DFLT_PORT_LINUX 
        else: 
            self.port = DFLT_PORT_WINDOWS 
        self.portLineEdit.setText(self.port) 
        self.samplesValidator = QtGui.QIntValidator(0,2**16-1,self.samplesLineEdit)
        self.samplesLineEdit.setValidator(self.samplesValidator)
        for name in constants.COLOR2LED_DICT:
            checkBox = getattr(self,'{0}CheckBox'.format(name))
            checkBox.setCheckState(QtCore.Qt.Checked)
            
        self.plotCheckBox.setCheckState(QtCore.Qt.Checked)
        plt.ion()

        self.updateWidgetEnabled()

    def connectPressed_Callback(self):
        if self.dev == None:
            self.connectPushButton.setText('Disconnect')
            self.portLineEdit.setEnabled(False)

    def connectClicked_Callback(self):
        connected = False
        if self.dev == None:
            try:
                self.dev = Colorimeter(self.port)
                connected = True
            except Exception, e:
                msgTitle = 'Connection Error'
                msgText = 'unable to connect to device: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                self.dev = None
        else:
            self.dev.close()
            self.dev = None
        if connected:
            self.numSamples = self.dev.getNumSamples()
            self.samplesLineEdit.setText('{0}'.format(self.numSamples))
        else:
            self.connectPushButton.setText('Connect')
            self.samplesLineEdit.setText('')
        self.updateWidgetEnabled()

    def calibratePressed_Callback(self):
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.measurePushButton.setEnabled(False)
        self.setWidgetEnabledOnMeasure()

    def calibrateClicked_Callback(self):
        if not constants.DEVEL_FAKE_MEASURE: 
            try:
                self.dev.calibrate()
            except IOError, e:
                msgTitle = 'Calibration Error:'
                msgText = 'unable to calibrate device: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                self.updateWidgetEnabled()
                return 

        freq = None  
        tran = 1.0, 1.0, 1.0, 1.0
        abso = 0.0, 0.0, 0.0, 0.0
        self.measValues = freq, tran, abso
        self.isCalibrated = True
        self.updateResultsDisplay()
        self.updateWidgetEnabled()

    def measurePressed_Callback(self):
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.calibratePushButton.setEnabled(False)
        self.setWidgetEnabledOnMeasure()

    def measureClicked_Callback(self):
        if constants.DEVEL_FAKE_MEASURE:
            freqValues = tuple(numpy.random.random((4,)))
            tranValues = tuple(numpy.random.random((4,)))
            absoValues = tuple(numpy.random.random((4,)))
        else:
            try:
                freqValues, tranValues, absoValues = self.dev.getMeasurement()
            except IOError, e:
                msgTitle = 'Measurement Error:'
                msgText = 'unable to get measurement: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                self.updateWidgetEnabled()
                return 

        self.measValues = freqValues, tranValues, absoValues
        self.updateResultsDisplay()
        self.updatePlot(create=True)
        self.updateWidgetEnabled()

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
            return 
        freqValues, tranValues, absoValues = self.measValues
        tranStrList, absoStrList = [], []
        colorNames = sorted(constants.COLOR2LED_DICT)
        for c in colorNames:
            n = constants.COLOR2LED_DICT[c] 
            if self.isColorChecked(c):
                tranStrList.append('{0}:\t{1:1.3f}'.format(c, tranValues[n]))
                absoStrList.append('{0}:\t{1:1.3f}'.format(c, absoValues[n]))
        tranStr = os.linesep.join(tranStrList)
        absoStr = os.linesep.join(absoStrList)
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
                self.redCheckBox.setEnabled(True)
                self.greenCheckBox.setEnabled(True)
                self.blueCheckBox.setEnabled(True)
                self.whiteCheckBox.setEnabled(True)
                self.plotCheckBox.setEnabled(True)

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

def basicGuiMain():
    app = QtGui.QApplication(sys.argv)
    mainWindow = BasicMainWindow()
    mainWindow.main()
    app.exec_()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    basicGuiMain()

