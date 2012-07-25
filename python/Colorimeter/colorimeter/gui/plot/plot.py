import os 
import sys 
import math
import random 
import time
import numpy
import matplotlib
if matplotlib.get_backend() != 'Qt4Agg':
    matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt 
plt.ion()

from PyQt4 import QtCore
from PyQt4 import QtGui

from plot_ui import Ui_MainWindow 
from colorimeter import constants
from colorimeter import import_export 
from colorimeter import standard_curve
from colorimeter.main_window import MainWindowWithTable
from colorimeter.gui.dialog import TestSolutionDialog

class PlotMainWindow(MainWindowWithTable, Ui_MainWindow):

    def __init__(self,parent=None):
        super(PlotMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        super(PlotMainWindow,self).connectActions()
        self.actionExport.triggered.connect(self.exportData_Callback)
        self.actionExport.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.actionImport.triggered.connect(self.importData_Callback)
        self.actionImport.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        itemDelegate = DoubleItemDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0,itemDelegate)

    def importData_Callback(self):
        userSolutionDict = import_export.loadUserTestSolutionDict(self.userHome)
        dataList = TestSolutionDialog().importData(userSolutionDict)
        print(dataList)
        
    def initialize(self):
        super(PlotMainWindow,self).initialize()
        self.noValueSymbol = constants.NO_VALUE_SYMBOL_NUMBER
        self.tableWidget.clean(setup=True)
        self.tableWidget.updateFunc = self.updatePlot
        concentrationStr = QtCore.QString.fromUtf8("Concentration (\xc2\xb5M)")
        self.tableWidget.setHorizontalHeaderLabels((concentrationStr,'Absorbance')) 
        self.updateWidgetEnabled()

    def exportData_Callback(self):
        dataList = self.tableWidget.getData()
        if len(dataList) < 2:
            msgTitle = 'Export Error'
            msgText = 'insufficient data for export'
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            return

        solutionName, flag = QtGui.QInputDialog.getText(
                self,
                'Export: Test Solultion Data',
                'Enter name for test solution:',
                )
        if not flag:
            return

        solutionName = str(solutionName)
        if not import_export.isUniqueSolutionName(self.userHome,solutionName):
            msg = 'User Test solution, {0}, already exists - overwrite?'.format(solutionName)
            reply = QtGui.QMessageBox.question(
                    self,
                    'Export Warning', 
                    msg,
                    QtGui.QMessageBox.Yes, 
                    QtGui.QMessageBox.No
                    )
            if reply == QtGui.QMessageBox.No:
                return
            else:
                import_export.deleteTestSolution(self.userHome,solutionName)

        dateStr = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        import_export.exportTestSolutionData(
                self.userHome,
                solutionName,
                dataList,
                self.currentColor,
                dateStr,
                )

    def updatePlot(self,create=False):
        if not create and not plt.fignum_exists(constants.PLOT_FIGURE_NUM):
            return
        dataList = self.tableWidget.getData(noValueInclude=False)
        dataList = dataListToFloat(dataList)
        if not dataList:
            self.closeFigure()
            return
        xList,yList = zip(*dataList)

        if len(dataList) > 1:
            slope, xFit, yFit = standard_curve.getLinearFit(
                    xList,
                    yList,
                    fitType=constants.FIT_TYPE,
                    numPts=constants.PLOT_FIT_NUM_PTS,
                    )
            haveSlope = True
        else:
            haveSlope = False

        plt.clf()
        self.fig = plt.figure(constants.PLOT_FIGURE_NUM)
        self.fig.canvas.manager.set_window_title('Colorimeter Plot')
        ax = self.fig.add_subplot(111)

        if haveSlope:
            hFit = ax.plot(xFit,yFit,'r')
        ax.plot(xList,yList,'ob')
        ax.grid('on')
        ax.set_xlabel('Concentration')
        ax.set_ylabel('Absorbance ('+self.currentColor+' led)')
        if haveSlope:
            self.fig.text(
                    constants.PLOT_SLOPE_TEXT_POS[0],
                    constants.PLOT_SLOPE_TEXT_POS[1],
                    'slope = {0:1.3f}'.format(slope), 
                    color='r'
                    )
        plt.draw()

    def getMeasurement(self):
        ledNumber = constants.COLOR2LED_DICT[self.currentColor]
        if constants.DEVEL_FAKE_MEASURE:
            abso = (random.random(),)*4
        else:
            freq, trans, abso = self.dev.getMeasurement()
        self.measurePushButton.setFlat(False)
        absoStr = '{0:1.2f}'.format(abso[ledNumber])
        self.tableWidget.addData('',absoStr,selectAndEdit=True)

    def getSaveFileHeader(self):
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S %Z') 
        headerList = [ 
                '# {0}'.format(timeStr),
                '# Colorimeter Data', 
                '# LED {0}'.format(self.currentColor),
                '# -----------------------------', 
                '# Concentration | Absorbance', 
                ]
        headerStr = os.linesep.join(headerList)
        return headerStr

    def setTableData(self,dataList):
        dataList = dataListToFloat(dataList)
        self.tableWidget.clean(setup=True)
        for conc, abso in dataList:
            concStr = str(conc)
            absoStr = '{0:1.2f}'.format(abso)
            self.tableWidget.addData(concStr,absoStr)

    def updateWidgetEnabled(self):
        super(PlotMainWindow,self).updateWidgetEnabled()
        if self.dev is None:
            self.ledColorWidget.setEnabled(False)
        else:
            self.ledColorWidget.setEnabled(True)
            self.calibratePushButton.setEnabled(True)

def dataListToFloat(dataList):
    dataListFloat = []
    for x,y in dataList:
        try:
            x, y = float(x), float(y)
        except ValueError:
            continue
        dataListFloat.append((x,y))
    return dataListFloat

def startPlotGUI():
    app = QtGui.QApplication(sys.argv)
    mainWindow = PlotMainWindow()
    mainWindow.main()
    app.exec_()

class DoubleItemDelegate(QtGui.QStyledItemDelegate):

    def __init__(self,*args,**kwargs):
        super(DoubleItemDelegate,self).__init__(*args,**kwargs)

    def createEditor(self,parent,option,index):
        editor = super(DoubleItemDelegate,self).createEditor(parent,option,index)
        validator = QtGui.QDoubleValidator(editor)
        validator.setBottom(0.0)
        editor.setValidator(validator)
        return editor

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    startPlotGUI()
