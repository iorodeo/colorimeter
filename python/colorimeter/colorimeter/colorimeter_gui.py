import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from colorimeter_gui_ui import Ui_MainWindow 
from colorimeter import Colorimeter

DFLT_PORT = '/dev/ttyACM0'

class ColorimeterMainWindow(QtGui.QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(ColorimeterMainWindow,self).__init__(parent)
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

    def initialize(self):
        self.port = DFLT_PORT
        self.portLineEdit.setText(self.port) 
        self.setWidgetEnableOnDisconnect()
        self.dev = None
        self.numSamples = None
        self.samplesValidator = QtGui.QIntValidator(0,2**16-1,self.samplesLineEdit)
        self.samplesLineEdit.setValidator(self.samplesValidator)

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
        self.transmissionTextEdit.setEnabled(False)
        self.absorbanceTextEdit.setEnabled(False)
        self.transmissionGroupBox.setEnabled(False)
        self.absorbanceGroupBox.setEnabled(False)
        self.measurePushButton.setEnabled(False)
        self.samplesLineEdit.setEnabled(False)
        self.redCheckBox.setEnabled(False)
        self.greenCheckBox.setEnabled(False)
        self.blueCheckBox.setEnabled(False)
        self.whiteCheckBox.setEnabled(False)

    def calibrateClicked_Callback(self):
        self.dev.calibrate()
        self.setWidgetEnableOnConnect()

    def measurePressed_Callback(self):
        self.transmissionTextEdit.setText('')
        self.absorbanceTextEdit.setText('')
        self.transmissionTextEdit.setEnabled(False)
        self.absorbanceTextEdit.setEnabled(False)
        self.transmissionGroupBox.setEnabled(False)
        self.absorbanceGroupBox.setEnabled(False)
        self.calibratePushButton.setEnabled(False)
        self.samplesLineEdit.setEnabled(False)
        self.redCheckBox.setEnabled(False)
        self.greenCheckBox.setEnabled(False)
        self.blueCheckBox.setEnabled(False)
        self.whiteCheckBox.setEnabled(False)

    def measureClicked_Callback(self):
        freq, trans, absorb = self.dev.getMeasurement()
        transStrList = []
        absorbStrList = []
        if self.redCheckBox.isChecked():
            transStrList.append('red:    {0:1.2f}'.format(trans[0]))
            absorbStrList.append('red:    {0:1.2f}'.format(absorb[0]))
        if self.greenCheckBox.isChecked():
            transStrList.append('green:  {0:1.2f}'.format(trans[1]))
            absorbStrList.append('green:  {0:1.2f}'.format(absorb[1]))
        if self.blueCheckBox.isChecked():
            transStrList.append('blue:   {0:1.2f}'.format(trans[2]))
            absorbStrList.append('blue:   {0:1.2f}'.format(absorb[2]))
        if self.whiteCheckBox.isChecked():
            transStrList.append('white:  {0:1.2f}'.format(trans[3]))
            absorbStrList.append('white:  {0:1.2f}'.format(absorb[3]))
        transStr = '\n'.join(transStrList)
        absorbStr = '\n'.join(absorbStrList)
        self.transmissionTextEdit.setText(transStr)
        self.absorbanceTextEdit.setText(absorbStr)
        self.setWidgetEnableOnConnect()

    def samplesChanged_Callback(self):
        valueStr = str(self.samplesLineEdit.text())
        value = int(valueStr)
        if value != self.numSamples:
            self.numSamples = value
            self.dev.setNumSamples(value)

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

    def main(self):
        self.show()


def colorimeterMain():
    app = QtGui.QApplication(sys.argv)
    mainWindow = ColorimeterMainWindow()
    mainWindow.main()
    app.exec_()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    colorimeterMain()

