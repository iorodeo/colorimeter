from __future__ import print_function
import sys
import platform
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt 
import numpy
from PyQt4 import QtCore
from PyQt4 import QtGui
from colorimeter_basic_gui_ui import Ui_MainWindow 
from colorimeter_serial import Colorimeter

DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 

class BasicMainWindow(QtGui.QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(BasicMainWindow,self).__init__(parent)
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
        self.samplesLineEdit.editingFinished.connect(self.samplesChanged_Callback)
        self.plotCheckBox.stateChanged.connect(self.plotCheckBox_Callback)

    def plotCheckBox_Callback(self,value):
        if value == QtCore.Qt.Unchecked:
            if self.fig is not None:
                plt.close(self.fig)
                self.fig = None

    def initialize(self):
        self.ledColors = 'red', 'green', 'blue', 'white'
        osType = platform.system()
        if osType == 'Linux': 
            self.port = DFLT_PORT_LINUX 
        else: 
            self.port = DFLT_PORT_WINDOWS 
        self.portLineEdit.setText(self.port) 
        self.setWidgetEnableOnDisconnect()
        self.dev = None
        self.numSamples = None
        self.samplesValidator = QtGui.QIntValidator(0,2**16-1,self.samplesLineEdit)
        self.samplesLineEdit.setValidator(self.samplesValidator)
        for name in self.ledColors:
            checkBox = getattr(self,'{0}CheckBox'.format(name))
            checkBox.setCheckState(QtCore.Qt.Checked)
            
        self.plotCheckBox.setCheckState(QtCore.Qt.Checked)
        plt.ion()
        self.fig = None
        

    def portChanged_Callback(self):
        self.port = str(self.portLineEdit.text())

    def connectPressed_Callback(self):
        if self.dev == None:
            self.connectPushButton.setText('Disconnect')
            self.portLineEdit.setEnabled(False)

    def connectClicked_Callback(self):
        if self.dev == None:
            self.dev = Colorimeter(self.port)
            self.setWidgetEnableOnConnect()
            self.numSamples = self.dev.getNumSamples()
            self.samplesLineEdit.setText('{0}'.format(self.numSamples))
        else:
            self.connectPushButton.setText('Connect')
            self.dev.close()
            self.dev = None
            self.setWidgetEnableOnDisconnect()
            self.samplesLineEdit.setText('')

    def calibratePressed_Callback(self):
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.measurePushButton.setEnabled(False)
        self.setWidgetEnableOnMeasure()

    def calibrateClicked_Callback(self):
        self.dev.calibrate()
        trans  = 1.0, 1.0, 1.0, 1.0
        absorb = 0.0, 0.0, 0.0, 0.0
        self.updateResultsDisplay(trans,absorb)
        self.setWidgetEnableOnConnect()

    def measurePressed_Callback(self):
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.calibratePushButton.setEnabled(False)
        self.setWidgetEnableOnMeasure()

    def measureClicked_Callback(self):
        freq, trans, absorb = self.dev.getMeasurement()
        self.updateResultsDisplay(trans,absorb)
        self.setWidgetEnableOnConnect()

        if self.plotCheckBox.isChecked():
            barWidth = 0.8
            yticks = 0.5*numpy.arange(0.0,2.0*max([max(absorb),1.0]))
            colorList = ('r','g','b','w')
            xLabelList = ('red', 'green', 'blue', 'white') 
            posList = range(1,len(absorb)+1)
            xlim = (posList[0],posList[-1]+barWidth)
            ylim = (0,max(1.2*max(absorb),1.0))

            plt.clf()
            self.fig = plt.figure(1)
            self.fig.canvas.manager.set_window_title('Colorimeter Basic: Absorbance Plot')
            ax = self.fig.add_subplot(111)
            for y in yticks[1:]:
                ax.plot(xlim,[y,y],'k:')
            for pos, value, color in zip(posList, absorb,colorList): 
                ax.bar([pos],[value],width=barWidth,color=color,linewidth=2)
                textXPos = pos+0.5*barWidth
                textYPos = value+0.01
                valueStr = '{0:1.3f}'.format(value)
                ax.text(textXPos,textYPos,valueStr,ha ='center',va ='bottom')

            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)

            ax.set_xticks([x+0.5*barWidth for x in posList])
            ax.set_xticklabels(xLabelList)
            ax.set_ylabel('Absorbance')
            ax.set_xlabel('LED')
            ax.set_yticks(yticks)
            plt.draw() 


    def updateResultsDisplay(self,trans,absorb):
        transStrList = []
        absorbStrList = []
        if self.redCheckBox.isChecked():
            transStrList.append('red:    {0:1.3f}'.format(trans[0]))
            absorbStrList.append('red:    {0:1.3f}'.format(absorb[0]))
        if self.greenCheckBox.isChecked():
            transStrList.append('green:  {0:1.3f}'.format(trans[1]))
            absorbStrList.append('green:  {0:1.3f}'.format(absorb[1]))
        if self.blueCheckBox.isChecked():
            transStrList.append('blue:   {0:1.3f}'.format(trans[2]))
            absorbStrList.append('blue:   {0:1.3f}'.format(absorb[2]))
        if self.whiteCheckBox.isChecked():
            transStrList.append('white:  {0:1.3f}'.format(trans[3]))
            absorbStrList.append('white:  {0:1.3f}'.format(absorb[3]))
        transStr = '\n'.join(transStrList)
        absorbStr = '\n'.join(absorbStrList)
        self.transmissionTextEdit.setText(transStr)
        self.absorbanceTextEdit.setText(absorbStr)

    def samplesChanged_Callback(self):
        valueStr = str(self.samplesLineEdit.text())
        value = int(valueStr)
        if value != self.numSamples:
            self.numSamples = value
            self.dev.setNumSamples(value)

    def setWidgetEnableOnMeasure(self):
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


    def setWidgetEnableOnConnect(self):
        self.transmissionTextEdit.setEnabled(True)
        self.absorbanceTextEdit.setEnabled(True)
        self.calibratePushButton.setEnabled(True)
        self.measurePushButton.setEnabled(True)
        self.transmissionGroupBox.setEnabled(True)
        self.absorbanceGroupBox.setEnabled(True)
        self.samplesLineEdit.setEnabled(True)
        self.redCheckBox.setEnabled(True)
        self.greenCheckBox.setEnabled(True)
        self.blueCheckBox.setEnabled(True)
        self.whiteCheckBox.setEnabled(True)
        self.portLineEdit.setEnabled(False)
        self.plotCheckBox.setEnabled(True)

    def setWidgetEnableOnDisconnect(self):
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

