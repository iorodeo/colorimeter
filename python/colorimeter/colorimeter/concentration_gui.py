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
        pass

    def initialize(self):

        # Example serial port
        self.portLineEdit.setText('/dev/ttyUSB0')

        # Example list of test solutions
        self.solution_list = ['ammonia', 'nitrite', 'nitrate']
        self.testSolutionComboBox.insertItems(0, self.solution_list)

        # Example calibration coefficient and LED
        coefficientValue = 0.364
        self.coefficientLineEdit.setText('{0:1.3}'.format(coefficientValue))
        ledColor = 'Red'
        self.ledLabel.setText('LED Color: <font color="red"> {0} </font>'.format(ledColor))

        # Fill in example table
        absorbValues = [0.42, 0.29, 0.48, 0.53, 0.69]
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

