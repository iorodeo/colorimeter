import os 
import sys 
import math
import random 
import time
import numpy
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt 
plt.ion()

from PyQt4 import QtCore
from PyQt4 import QtGui

from colorimeter_plot_gui_ui import Ui_MainWindow 
from colorimeter_common import constants
from colorimeter_common import import_export 
from colorimeter_common import standard_curve
from colorimeter_common.main_window import MainWindowWithTable

class ColorimeterPlotMainWindow(MainWindowWithTable, Ui_MainWindow):

    def __init__(self,parent=None):
        super(ColorimeterPlotMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        super(ColorimeterPlotMainWindow,self).connectActions()
        self.actionExport.triggered.connect(self.exportData_Callback)
        self.actionExport.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.actionImport.triggered.connect(self.importData_Callback)
        self.actionImport.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        itemDelegate = DoubleItemDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0,itemDelegate)

    def editTestSolutions_Callback(self):
        print('editTestSolutions_Callback')

    def importData_Callback(self):
        print('importData_Callback')
        
    def initialize(self):
        super(ColorimeterPlotMainWindow,self).initialize()
        self.tableWidget.clean(setup=True)
        self.tableWidget.updateFunc = self.updatePlot
        self.tableWidget.setHorizontalHeaderLabels(('Concentration','Absorbance')) 
        self.updateWidgetEnabled()

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

    def saveFile_Callback(self):
        dataList = self.tableWidget.getData(noValueSymb=True)
        if not dataList:
            msgTitle = 'Save Error'
            msgText = 'No data to save.'
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            return
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile) 
        filename = dialog.getSaveFileName(
                   None,
                   'Select data file',
                   self.lastSaveDir,
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        filename = str(filename)
        if not filename:
            return
        self.lastSaveDir =  os.path.split(filename)[0]

        timeStr = time.strftime('%Y-%m-%d %H:%M:%S %Z') 
        header = [
                '# {0}'.format(timeStr),
                '# Colorimeter Data', 
                '# LED {0}'.format(self.currentColor),
                '# -----------------------------', 
                '# Absorbance  |  Concentration', 
                ]

        with open(filename,'w') as f:
            f.write(os.linesep.join(header))
            f.write(os.linesep)
            for x,y in dataList:
                f.write('{0}  {1}{2}'.format(y,x,os.linesep))
            f.write('{0}'.format(os.linesep))

    def loadFile_Callback(self):
        """
        Load data in table from a text file.
        """
        print('loadFile_Callback')
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile) 
        filename = dialog.getOpenFileName(
                   None,
                   'Select data file',
                   self.lastSaveDir,
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        filename = str(filename)
        if not filename:
            return 
        dataList, ledColor = self.loadDataFromFile(filename)
        if ledColor is None:
            msgTitle = 'Import Warning'
            msgText = 'Unable to determine LED color from data file'
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
        else:
            self.setLEDColor(ledColor)
        self.setTableData(dataList)
        self.updateWidgetEnabled()

    def exportData_Callback(self):
        """
        Export data to yaml file stored in the users colorimeter data
        directory.  This data will then be available for use with the
        colorimeter measurement program.
        """
        dataList = self.getTableData()

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

    def setTableData(self,dataList):
        """
        Set data item in the table widget from the given dataList.
        """
        self.tableWidget.clean(setup=True)
        for abso, conc in dataList:
            concStr = str(conc)
            absoStr = '{0:1.2f}'.format(abso)
            self.tableWidget.addData(concStr,absoStr)

    def loadDataFromFile(self,filename):
        """
        Load absorbance and concentration data from data file.
        """
        try:
            fileLines = []
            with open(filename,'r') as f:
                fileLines = f.readlines()
        except IOError, e:
            msgTitle = 'File Load Error'
            msgText = 'Unable to load data file: {0}'.format(str(e))
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            return 

        dataList = []
        ledColor = None

        for line in fileLines:
            line = line.split()
            if not line:
                continue
            if 'LED' in line:
                try:
                    color = line[line.index('LED')+1].lower()
                except IndexError, e:
                    continue
                if color in constants.COLOR2LED_DICT:
                    ledColor = color
                continue
            if line[0] == '#':
                continue
            try:
                abso = float(line[0])
            except ValueError, e:
                continue
            try:
                conc = float(line[1])
            except ValueError:
                conc = ''
            dataList.append((abso,conc))

        return dataList, ledColor


    def updateWidgetEnabled(self):
        """
        Kind of messay -  perhaps this could be cleaned up a bit.
        """
        if self.dev is None:
            self.calibratePushButton.setEnabled(False)
            self.measurePushButton.setEnabled(False)
            self.ledColorWidget.setEnabled(False)
            if self.tableWidget.measIndex > 0:
                self.tableWidget.setEnabled(True)
                self.plotPushButton.setEnabled(True)
                self.clearPushButton.setEnabled(True)
            else:
                self.tableWidget.setEnabled(False)
                self.plotPushButton.setEnabled(False)
                self.clearPushButton.setEnabled(False)
            self.portLineEdit.setEnabled(True)
            self.statusbar.showMessage('Not Connected')
        else:
            self.calibratePushButton.setEnabled(True)
            self.ledColorWidget.setEnabled(True)
            if self.isCalibrated:
                self.plotPushButton.setEnabled(True)
                self.clearPushButton.setEnabled(True)
                self.measurePushButton.setEnabled(True)
                self.tableWidget.setEnabled(True)
            else:
                if self.tableWidget.measIndex > 0:
                    self.tableWidget.setEnabled(True)
                    self.plotPushButton.setEnabled(True)
                    self.clearPushButton.setEnabled(True)
                else:
                    self.tableWidget.setEnabled(False)
                    self.plotPushButton.setEnabled(False)
                    self.clearPushButton.setEnabled(False)
            self.portLineEdit.setEnabled(False)
            self.connectPushButton.setFlat(False)
            self.statusbar.showMessage('Connected, Mode: Stopped')


def dataListToFloat(dataList):
    dataListFloat = []
    for x,y in dataList:
        try:
            x, y = float(x), float(y)
        except ValueError:
            continue
        dataListFloat.append((x,y))
    return dataListFloat

def plotGuiMain():
    """
    Entry point for plotting gui
    """
    app = QtGui.QApplication(sys.argv)
    mainWindow = ColorimeterPlotMainWindow()
    mainWindow.main()
    app.exec_()

class DoubleItemDelegate(QtGui.QStyledItemDelegate):
    """
    Item delegate for double items - assigns a validator to the editor to
    check/limit inputs.
    """

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
    plotGuiMain()
