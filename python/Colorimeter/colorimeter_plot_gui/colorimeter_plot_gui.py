from __future__ import print_function
import os 
import sys 
import math
import platform
import functools
import random 
import time
import numpy
import matplotlib
import yaml
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt 
plt.ion()

from PyQt4 import QtCore
from PyQt4 import QtGui

from colorimeter_plot_gui_ui import Ui_MainWindow 
from colorimeter_serial import Colorimeter
from colorimeter_common import file_tools

DEVEL_FAKE_MEASURE = True 
DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 
TABLE_MIN_ROW_COUNT = 4
TABLE_COL_COUNT = 2
FIT_TYPE = 'force_zero'
DEFAULT_LED = 'red'
COLOR2LED_DICT = {'red':0,'green':1,'blue': 2,'white': 3} 
PLOT_FIGURE_NUM = 1
NO_VALUE_SYMB = 'nan'

class ColorimeterPlotMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self,parent=None):
        super(ColorimeterPlotMainWindow,self).__init__(parent)
        self.color2LED_Dict = COLOR2LED_DICT
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
        self.clearPushButton.pressed.connect(self.clearPressed_Callback)
        self.clearPushButton.clicked.connect(self.clearClicked_Callback)

        for color in self.color2LED_Dict:
            button = getattr(self,'{0}RadioButton'.format(color))
            callback = functools.partial(self.colorRadioButtonClicked_Callback, color)
            button.clicked.connect(callback)
        self.plotPushButton.clicked.connect(self.plotPushButtonClicked_Callback)

        self.actionSave.triggered.connect(self.saveFile_Callback)
        self.actionSave.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_S)

        self.actionLoad.triggered.connect(self.loadFile_Callback)
        self.actionLoad.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)

        self.actionExport.triggered.connect(self.exportData_Callback)
        self.actionExport.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)

        self.actionImport.triggered.connect(self.importData_Callback)
        self.actionImport.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        self.actionEditTestSolutions.triggered.connect(self.editTestSolutions_Callback)

        itemDelegate = DoubleItemDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0,itemDelegate)

        self.tableWidget.contextMenuEvent = self.tableWidgetContextMenu_Callback

        self.tableWidget_CopyAction = QtGui.QAction(self.tableWidget)
        self.tableWidget_CopyAction.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_C)
        self.tableWidget_CopyAction.triggered.connect(self.copyTableWidgetData)
        self.tableWidget.addAction(self.tableWidget_CopyAction)

        self.tableWidget_DeleteAction = QtGui.QAction(self.tableWidget)
        self.tableWidget_DeleteAction.setShortcut(QtCore.Qt.Key_Delete)
        self.tableWidget_DeleteAction.triggered.connect(self.deleteTableWidgetData)
        self.tableWidget.addAction(self.tableWidget_DeleteAction)

        self.tableWidget_BackspaceAction = QtGui.QAction(self.tableWidget)
        self.tableWidget_BackspaceAction.setShortcut(QtCore.Qt.Key_Backspace)
        self.tableWidget_BackspaceAction.triggered.connect(self.deleteTableWidgetData)
        self.tableWidget.addAction(self.tableWidget_BackspaceAction)

    def editTestSolutions_Callback(self):
        print('editTestSolutions_Callback')

        
    def initialize(self):
        osType = platform.system()
        if osType == 'Linux': 
            self.port = DFLT_PORT_LINUX 
        else: 
            self.port = DFLT_PORT_WINDOWS 
        self.userHome = os.getenv('USERPROFILE')
        if self.userHome is None:
            self.userHome = os.getenv('HOME')
        self.lastLogDir = self.userHome
            
        self.portLineEdit.setText(self.port) 
        self.measIndex = 0
        self.dev = None
        self.redRadioButton.setChecked(True)
        self.currentColor = 'red'
        self.statusbar.showMessage('Not Connected')
        self.isCalibrated = False
        self.fig = None

        # Set up data table
        self.cleanDataTable(setup=True)
        self.setWidgetEnabled()
        self.cleanDataTable()
        self.isCalibrated = False

        self.tableWidget.setHorizontalHeaderLabels(('Concentration','Absorbance')) 
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self.user_TestSolutionDir = os.path.join(
                self.userHome,
                '.iorodeo_colorimeter',
                'data',
                )

    def tableWidgetContextMenu_Callback(self,event):
        """
        Callback function for the table widget context menus. Currently
        handles copy and delete actions.
        """
        menu = QtGui.QMenu(self)
        copyAction = menu.addAction("Copy")
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(self.tableWidget.mapToGlobal(event.pos()))
        if action == copyAction:
            self.copyTableWidgetData()
        if action == deleteAction:
            self.deleteTableWidgetData()

    def deleteTableWidgetData(self):
        """
        Deletes data from the table widget based on the current selection.
        """
        removeList = []
        for i in range(self.tableWidget.rowCount()):
            item0 = self.tableWidget.item(i,0)
            item1 = self.tableWidget.item(i,1)
            if self.tableWidget.isItemSelected(item0):
                if not self.tableWidget.isItemSelected(item1):
                    item0.setText("")
            if self.tableWidget.isItemSelected(item1):
                removeList.append(item1.row())

        for ind in reversed(removeList):
            if self.measIndex > 0:
                self.measIndex-=1
            self.tableWidget.removeRow(ind)

        if self.tableWidget.rowCount() < TABLE_MIN_ROW_COUNT:
            self.tableWidget.setRowCount(TABLE_MIN_ROW_COUNT)
            for row in range(self.measIndex,TABLE_MIN_ROW_COUNT): 
                for col in range(0,TABLE_COL_COUNT): 
                    tableItem = QtGui.QTableWidgetItem() 
                    tableItem.setFlags(QtCore.Qt.NoItemFlags) 
                    self.tableWidget.setItem(row,col,tableItem)

        if plt.fignum_exists(PLOT_FIGURE_NUM):
            self.updatePlot()

    def copyTableWidgetData(self): 
        """
        Copies data from the table widget to the clipboard based on the current
        selection.
        """
        selectedList = self.getTableWidgetSelectedList()

        # Create string to send to clipboard
        clipboardList = []
        for j, rowList in enumerate(selectedList):
            for i, value in enumerate(rowList):
                if not value:
                    clipboardList.append('{0}'.format(j))
                else:
                    clipboardList.append(value)
                if i < len(rowList)-1:
                    clipboardList.append(" ")
            clipboardList.append(os.linesep)
        clipboardStr = ''.join(clipboardList)
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(clipboardStr)

    def getTableWidgetSelectedList(self):
        """
        Returns list of select items in the table widget. Note, assumes that
        selection mode for the table is ContiguousSelection.
        """
        selectedList = []
        for i in range(self.tableWidget.rowCount()): 
            rowList = []
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i,j)
                if self.tableWidget.isItemSelected(item):
                    rowList.append(str(item.text()))
            selectedList.append(rowList)
        return selectedList


    def portChanged_Callback(self):
        self.port = str(self.portLineEdit.text())

    def connectPressed_Callback(self):
        if self.dev == None:
            self.connectPushButton.setText('Disconnect')
            self.connectPushButton.setFlat(True)
            self.portLineEdit.setEnabled(False)
            self.statusbar.showMessage('Connecting...')

    def connectClicked_Callback(self):
        """
        Connect/Disconnect to colorimeter device.
        """
        if self.dev == None:
            try:
                self.dev = Colorimeter(self.port)
                self.numSamples = self.dev.getNumSamples()
                connected = True
            except Exception, e:
                QtGui.QMessageBox.critical(self,'Error', str(e))
                self.connectPushButton.setText('Connect')
                self.statusbar.showMessage('Not Connected')
                self.portLineEdit.setEnabled(True)
                connected = False
        else:
            self.connectPushButton.setText('Connect')
            try:
                self.cleanUpAndCloseDevice()
            except Exception, e:
                QtGui.QMessageBox.critical(self,'Error', str(e))
            connected = False
            self.isCalibrated = False
        self.setWidgetEnabled()

    def colorRadioButtonClicked_Callback(self,color):
        """
        Callback for selecting the LED color used by the colorimeter.
        """
        if len(self.tableWidget.item(0,1).text()):
            chn_msg = "Changing channels will clear all data. Continue?"
            response = self.cleanDataTable(msg=chn_msg)
            if not response:
                color = self.currentColor
                button = getattr(self,'{0}RadioButton'.format(color))
                button.setChecked(True)
        self.currentColor = color
        print(color)

    def plotPushButtonClicked_Callback(self):
        """
        Plots the data in the table widget. 
        """
        dataList = self.getTableData()
        if not dataList:
            return
        yList = [x for x,y in dataList]
        xList = [y for x,y in dataList]

        if FIT_TYPE == 'force_zero': 
            xArray = numpy.array(xList)
            yArray = numpy.array(yList)
            numer = (xArray*yArray).sum()
            denom = (xArray*xArray).sum()
            slope = numer/denom
            xFit = numpy.linspace(min(xList), max(xList), 500)
            yFit = slope*xFit
        else:
            polyFit = numpy.polyfit(xList,yList,1)
            xFit = numpy.linspace(min(xList), max(xList), 500)
            yFit = numpy.polyval(polyFit, xFit)
            slope = polyFit[0]

        plt.clf()
        self.fig = plt.figure(PLOT_FIGURE_NUM)
        self.fig.canvas.manager.set_window_title('Colorimeter Plot')
        ax = self.fig.add_subplot(111)
        hFit = ax.plot(xFit,yFit,'r')

        ax.plot(xList,yList,'ob')
        ax.grid('on')
        ax.set_xlabel('Concentration')
        ax.set_ylabel('Absorbance ('+self.currentColor+' led)')
        self.fig.text(0.15,0.85,'slope = {0:1.3f}'.format(slope), color='r')
        plt.draw()
        
    def measurePressed_Callback(self):
        print('measPushButton_Pressed')
        self.calibratePushButton.setEnabled(False)
        self.plotPushButton.setEnabled(False)
        self.measurePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Measuring...')

    def measureClicked_Callback(self):
        """
        Takes a measurement from the colorimeter. 
        """
        if DEVEL_FAKE_MEASURE:
            abso = (random.random(),)*4
        else:
            freq, trans, abso = self.dev.getMeasurement()
        self.measurePushButton.setFlat(False)
        ledNumber = COLOR2LED_DICT[self.currentColor]
        self.addDataToTable(abso[ledNumber],'',selectEdit=True)
        self.setWidgetEnabled()

    def calibratePressed_Callback(self):
        self.measurePushButton.setEnabled(False)
        self.plotPushButton.setEnabled(False)
        self.clearPushButton.setEnabled(False)
        self.calibratePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Calibrating...')

    def calibrateClicked_Callback(self):
        if not DEVEL_FAKE_MEASURE: 
            self.dev.calibrate()
        self.isCalibrated = True
        self.calibratePushButton.setFlat(False)
        self.setWidgetEnabled()

    def clearPressed_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            self.measurePushButton.setEnabled(False)
            self.plotPushButton.setEnabled(False)
            self.calibratePushButton.setEnabled(False)
        self.clearPushButton.setFlat(True)

    def clearClicked_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            erase_msg = "Clear all data?"
            self.cleanDataTable(msg=erase_msg)
        self.clearPushButton.setFlat(False)
        self.setWidgetEnabled()

    def saveFile_Callback(self):
        """
        Save data in table to a text file.
        """
        dataList = self.getTableData(addNoValueSymb=True)
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
                   self.lastLogDir,
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        filename = str(filename)
        if not filename:
            return
        self.lastLogDir =  os.path.split(filename)[0]

        timeStr = time.strftime('%Y-%m-%d %H:%M:%S %Z') 
        header = [
                '# {0}'.format(timeStr),
                '# Colorimeter Data', 
                '# -----------------------------', 
                '# Absorbance  |  Concentration', 
                ]

        with open(filename,'w') as f:
            f.write(os.linesep.join(header))
            for x,y in dataList:
                f.write("%s%s\t\t%s"%(os.linesep,x,y))

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
                   self.lastLogDir,
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        filename = str(filename)
        if not filename:
            return 
        dataList = self.loadDataFromFile(filename)
        self.setTableData(dataList)
        if self.dev is None:
            self.setWidgetEnabled()
        else:
            self.setWidgetEnabled()

    def exportData_Callback(self):
        """
        Export data to yaml file stored in the users colorimeter data
        directory.  This data will then be available for use with the
        colorimeter measurement program.
        """
        dataList = self.getTableData()

        if not dataList:
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
        if not file_tools.isUniqueSolutionName(self.userHome,solutionName):
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
                file_tools.deleteTestSolution(self.userHome,solutionName)

        dateStr = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        file_tools.exportTestSolutionData(
                self.userHome,
                solutionName,
                dataList,
                self.currentColor,
                dateStr,
                )

    def importData_Callback(self):
        print('importData_Callback')

    def getTableData(self,addNoValueSymb=False):
        """
        Get data items from table widget - replace missing concentratino
        values with the no value symbol.
        """
        dataList = []
        for i in range(self.measIndex):
            concTableItem = self.tableWidget.item(i,0)
            absoTableItem = self.tableWidget.item(i,1)
            try:
                abso = float(absoTableItem.text())
            except ValueError, e:
                continue
            try:
                conc = float(concTableItem.text())
            except ValueError, e:
                if addNoValueSymb:
                    conc = NO_VALUE_SYMB 
                else:
                    continue
            dataList.append((abso,conc))
        return dataList

    def setTableData(self,dataList):
        """
        Set data item in the table widget from the given dataList.
        """
        self.cleanDataTable(setup=True)
        for abso, conc in dataList:
            self.addDataToTable(abso,conc)

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
        for line in fileLines:
            if not line:
                continue
            line = line.split()
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
        return dataList


    def setWidgetEnabled(self):
        """
        Kind of messay -  perhaps this could be cleaned up a bit.
        """
        if self.dev is None:

            self.calibratePushButton.setEnabled(False)
            self.measurePushButton.setEnabled(False)
            print(self.measIndex)
            if self.measIndex > 0:
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
            if self.isCalibrated:
                self.plotPushButton.setEnabled(True)
                self.clearPushButton.setEnabled(True)
                self.measurePushButton.setEnabled(True)
                self.tableWidget.setEnabled(True)
            else:
                if self.measIndex > 0:
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

    #def setWidgetEnabledOnDisconnect(self):

    #    """
    #    Enables/Disables the appropriate widgets for the when the device
    #    is disconnected from the colorimeter.
    #    """
    #    self.calibratePushButton.setEnabled(False)
    #    self.measurePushButton.setEnabled(False)
    #    self.clearPushButton.setEnabled(False)
    #    if self.measIndex > 0:
    #        self.tableWidget.setEnabled(True)
    #        self.plotPushButton.setEnabled(True)
    #    else:
    #        self.tableWidget.setEnabled(False)
    #        self.plotPushButton.setEnabled(False)
    #    self.portLineEdit.setEnabled(True)
    #    self.statusbar.showMessage('Not Connected')

    #def setWidgetEnabledOnConnect(self):
    #    """
    #    Enables/Disables the appropriate widgets for the case where the 
    #    device is connected to the colorimeter.
    #    """
    #    self.calibratePushButton.setEnabled(True)
    #    if self.isCalibrated:
    #        self.plotPushButton.setEnabled(True)
    #        self.clearPushButton.setEnabled(True)
    #        self.measurePushButton.setEnabled(True)
    #        self.tableWidget.setEnabled(True)
    #    else:
    #        if self.measIndex > 0:
    #            self.tableWidget.setEnabled(True)
    #            self.plotPushButton.setEnabled(True)
    #    self.portLineEdit.setEnabled(False)
    #    self.connectPushButton.setFlat(False)
    #    self.statusbar.showMessage('Connected, Mode: Stopped')

    def addDataToTable(self,abso,conc,selectEdit=False):
        """
        Added data to table widget. If selectEdit is set to True then the
        concetration element is selected and opened for editing by the
        user.
        """
        rowCount = self.measIndex+1
        absoStr = '{0:1.2f}'.format(abso)
        if type(conc) == float and not math.isnan(conc):
            concStr = '{0:f}'.format(conc)
        else:
            concStr = ''
        if rowCount > TABLE_MIN_ROW_COUNT:
            self.tableWidget.setRowCount(rowCount)
        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(absoStr)
        tableItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(self.measIndex,1,tableItem)
        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(concStr)
        self.tableWidget.setItem(self.measIndex,0,tableItem)
        if selectEdit:
            tableItem.setSelected(True)
            self.tableWidget.setCurrentCell(self.measIndex,0)
            self.tableWidget.editItem(self.tableWidget.currentItem()) 
        self.measIndex+=1

    def cleanDataTable(self,setup=False,msg=''):
        """
        Removes all data form the data table widget. If setup is False the user
        is prompted and asked if they really want to clear all data.
        """
        if setup:
            reply = QtGui.QMessageBox.Yes
        elif len(self.tableWidget.item(0,1).text()):
            reply = QtGui.QMessageBox.question(self,'Message', msg, 
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        else: 
            return True
        if reply == QtGui.QMessageBox.Yes:
            self.tableWidget.setRowCount(TABLE_MIN_ROW_COUNT)
            self.tableWidget.setColumnCount(TABLE_COL_COUNT)
            for row in range(0,TABLE_MIN_ROW_COUNT):
                for col in range(0,TABLE_COL_COUNT):
                    tableItem = QtGui.QTableWidgetItem()
                    tableItem.setFlags(QtCore.Qt.NoItemFlags)
                    self.tableWidget.setItem(row,col,tableItem)
            self.measIndex = 0
            return True
        else:
            return False

    def closeEvent(self,event):
        if self.dev is not None:
            self.cleanUpAndCloseDevice()
        event.accept()

    def cleanUpAndCloseDevice(self):
        self.dev.close()
        self.dev = None

    def main(self):
        self.show()

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
