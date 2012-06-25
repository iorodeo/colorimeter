from __future__ import print_function
import sys
import functools

from PyQt4 import QtCore
from PyQt4 import QtGui

from concentration_gui_ui import Ui_MainWindow 


class ConcentrationGUI_MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self,parent=None):
        super(ConcentrationGUI_MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        self.measurePushButton.clicked.connect(self.measurePushButton_Callback)
        self.testSolutionComboBox.currentIndexChanged.connect(self.selection_Callback)

    def selection_Callback(self):
        index = self.testSolutionComboBox.currentIndex()
        if index == 3:
            self.coefficientLineEdit.setText('{0:1.3}'.format(self.coefficientValue))
            self.coefficientLineEdit.setEnabled(True)

    def measurePushButton_Callback(self):
        tableItem = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(7,0,tableItem)
        tableItem.setText('{0:1.3f}'.format(0.78))
        tableItem.setBackgroundColor(QtGui.QColor().fromRgb(0,200,0,alpha=127).dark())
        tableItem = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(7,1,tableItem)
        tableItem.setText('{0:1.3f}'.format(18.3))
        tableItem.setBackgroundColor(QtGui.QColor().fromRgb(0,200,0,alpha=127).dark())
        pass

    def initialize(self):
        coefficientValue = 0.0423
        self.coefficientValue = coefficientValue


        # Example serial port
        self.portLineEdit.setText('/dev/ttyAM0')
        self.portLineEdit.setDisabled(True)
        self.connectPushButton.setText('Disconnect')

        # Example list of test solutions
        self.solution_list = ['','ammonia', 'nitrite', 'nitrate']
        self.testSolutionComboBox.insertItems(0, self.solution_list)

        # Example calibration coefficient and LED
        #coefficientValue = 0.364
        self.coefficientLineEdit.setDisabled(True)
        ledColor = 'Green'
        self.ledLabel.setText('LED Color: <font color="green"> {0} </font>'.format(ledColor))

        # Fill in example table
        absorbValues = [0.12, 0.36, 0.42, 0.29, 0.48, 0.53, 0.69]
        tableValues = [(x, x/coefficientValue) for x in absorbValues]
               
        #self.tableWidget.setRowCount(len(tableValues))
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(('Absorbance','Concentration (ppm)')) 
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        for i, rowValues in enumerate(tableValues):
            for j, value in enumerate(rowValues):
                tableItem = QtGui.QTableWidgetItem()
                self.tableWidget.setItem(i,j,tableItem)
                tableItem.setText('{0:1.3f}'.format(value))

    def main(self):
        self.show()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = ConcentrationGUI_MainWindow()
    mainWindow.main()
    app.exec_()

