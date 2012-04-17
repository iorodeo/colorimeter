from __future__ import print_function
import sys
import functools
import random
from matplotlib import pylab

from PyQt4 import QtCore
from PyQt4 import QtGui

from colorimeter_plot_gui_ui import Ui_MainWindow 
#from colorimeter import Colorimeter


class ColorimeterPlotMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self,parent=None):
        super(ColorimeterPlotMainWindow,self).__init__(parent)
        self.radioButtonColors = ('red', 'green', 'blue', 'white')
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        self.connectPushButton.pressed.connect(self.connectPushButton_Pressed)
        self.connectPushButton.clicked.connect(self.connectPushButton_Clicked)
        self.redRadioButton

        for color in self.radioButtonColors:
            button = getattr(self,'{0}RadioButton'.format(color))
            callback = functools.partial(self.colorRadioButton_Clicked, color)
            button.clicked.connect(callback)
        self.plotPushButton.clicked.connect(self.plotPushButton_Clicked)

    def initialize(self):

        pylab.ion()
        self.serialPortLineEdit.setText('/dev/ttyUSB0')
        self.redRadioButton.setChecked(True)
        self.connectPushButton.setText('Disconnect')

        # Disable widgets for start up condition
        if 0:
            for color in self.radioButtonColors:
                button = getattr(self,'{0}RadioButton'.format(color))
                button.setEnabled(False)

            self.dataTableWidget.setEnabled(False)

            self.calibratePushButton.setEnabled(False)
            self.measurePushButton.setEnabled(False)
            self.plotPushButton.setEnabled(False)

        # Write some data to the table
        if 0:
            numValues = 20
            tableValues = []
            for i in range(numValues):
                value0 = float(i+1)
                value1 = 2.0*(i+1) + random.random()
                tableValues.append((value0, value1))
        else:
            tableValues = [
            (0.00E+000,   0),
            (2.21E-006,   0.05), 
            (4.42E-006,   0.1), 
            (6.63E-006,   0.14),
            (8.84E-006,   0.19),
            (1.11E-005,   0.22),
            (1.33E-005,   0.27),
            (1.55E-005,   0.32),
            (1.77E-005,   0.37),
            (1.99E-005,   0.4 ),
            (2.21E-005,   0.45),
            ]
            tableValues = [(1.e6*x,y) for x,y in tableValues]
            numValues = len(tableValues)


        # Set up data table
        self.dataTableWidget.setRowCount(len(tableValues))
        self.dataTableWidget.setColumnCount(2)
        self.dataTableWidget.setHorizontalHeaderLabels(('Concentration (uM)','Absorbance')) 
        self.dataTableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        for i, rowValues in enumerate(tableValues):
            for j, value in enumerate(rowValues):
                tableItem = QtGui.QTableWidgetItem()
                self.dataTableWidget.setItem(i,j,tableItem)
                tableItem.setText('{0:1.3f}'.format(value))



                
    def connectPushButton_Pressed(self):
        print('connectPushButton_Pressed')

    def connectPushButton_Clicked(self):
        print('connectPushButton_Clicked')

    def colorRadioButton_Clicked(self,color):
        print(color)

    def plotPushButton_Clicked(self):
        print('plotPushButton_Clicked')
        dataList = []
        for i in range(self.dataTableWidget.rowCount()):
            tableItem = self.dataTableWidget.item(i,0)
            x = float(tableItem.text())
            tableItem = self.dataTableWidget.item(i,1)
            y = float(tableItem.text())
            dataList.append((x,y))

        xList = [x for x,y in dataList]
        yList = [y for x,y in dataList]
        if len(dataList) > 1:
            polyFit = pylab.polyfit(xList,yList,1)
            xFit = pylab.linspace(min(xList), max(xList), 500)
            yFit = pylab.polyval(polyFit, xFit)
            hFit = pylab.plot(xFit,yFit,'r')
        pylab.plot(xList,yList,'ob')
        pylab.grid('on')
        pylab.xlabel('concentration (uM)')
        pylab.ylabel('absorbance')
        slope = polyFit[0]
        pylab.figlegend((hFit,),('slope = {0:1.3f}'.format(slope),), 'upper left')
        pylab.show()
        

    def main(self):
        self.show()

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    mainWindow = ColorimeterPlotMainWindow()
    mainWindow.main()
    app.exec_()

