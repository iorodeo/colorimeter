from __future__ import print_function
import os 
import sys 
import platform
import functools
import random 
import time
import yaml
import numpy
import pkg_resources

# TEMPORARY - FOR DEVELOPMENT ##################
import random
################################################

import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt 

from PyQt4 import QtCore
from PyQt4 import QtGui

from colorimeter_measurement_ui import Ui_MainWindow 
from colorimeter_serial import Colorimeter
from colorimeter_common import file_tools

DEVEL_FAKE_MEASURE = True 

DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 
DFLT_LED_COLOR = 'red'
COLOR2LED_DICT = {'red':0,'green':1,'blue': 2,'white': 3} 

TABLE_MIN_ROW_COUNT = 1
TABLE_COL_COUNT = 2 

PLOT_FIGURE_NUM = 1
PLOT_BAR_WIDTH = 0.8
PLOT_TEXT_Y_OFFSET = 0.01
PLOT_YLIM_ADJUST = 1.15

NO_VALUE_SYMBOL = '_NV_'

class MeasurementMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self,parent=None):
        super(MeasurementMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.initialize()
        self.connectActions()

    def connectActions(self):
        """
        Connect actions for widgets in measurement GUI.
        """
        self.portLineEdit.editingFinished.connect(self.portChanged_Callback)
        self.connectPushButton.pressed.connect(self.connectPressed_Callback)
        self.connectPushButton.clicked.connect(self.connectClicked_Callback)
        self.calibratePushButton.pressed.connect(self.calibratePressed_Callback)
        self.calibratePushButton.clicked.connect(self.calibrateClicked_Callback)
        self.measurePushButton.clicked.connect(self.measureClicked_Callback)
        self.measurePushButton.pressed.connect(self.measurePressed_Callback)
        self.clearPushButton.pressed.connect(self.clearPressed_Callback)
        self.clearPushButton.clicked.connect(self.clearClicked_Callback)
        self.testSolutionComboBox.currentIndexChanged.connect(
                self.testSolutionChanged_Callback
                )

        for color in COLOR2LED_DICT:
            button = getattr(self,'{0}RadioButton'.format(color))
            callback = functools.partial(self.colorRadioButton_Clicked, color)
            button.clicked.connect(callback)
        self.plotPushButton.clicked.connect(self.plotPushButton_Clicked)

        self.actionIncludeDefaultTestSolutions.toggled.connect(
                self.populateTestSolutionComboBox
                )
        self.actionIncludeUserTestSolutions.toggled.connect(
                self.populateTestSolutionComboBox
                )

        self.actionSave.triggered.connect(self.saveFile_Callback)
        self.actionSave.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.actionLoad.triggered.connect(self.loadFile_Callback)
        self.actionLoad.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.actionEditTestSolutions.triggered.connect(self.editTestSolutions_Callback)

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

        self.tableWidget.itemChanged.connect(self.tableWidgetItemChanged_Callback)


    def initialize(self):
        """
        Initializes the measurement GUI. Sets buttons to default data, sets initial port
        based on OS, get the users home directory. etc. 
        """

        self.dev = None
        self.measIndex = 0
        self.isCalibrated = False
        self.coeff = None
        self.fig = None
        plt.ion()
        
        # Set default port based on system
        osType = platform.system()
        if osType == 'Linux': 
            self.port = DFLT_PORT_LINUX 
        else: 
            self.port = DFLT_PORT_WINDOWS 
        self.portLineEdit.setText(self.port) 

        # Get users home directory
        self.userHome = os.getenv('USERPROFILE')
        if self.userHome is None:
            self.userHome = os.getenv('HOME')
        self.lastSaveDir = self.userHome
        self.statusbar.showMessage('Not Connected')

        # Set default value for LED color
        self.setLEDColor(DFLT_LED_COLOR)

        # Set up data table
        self.cleanDataTable(setup=True)
        concentrationStr = QtCore.QString.fromUtf8("Concentration (\xc2\xb5M)")
        self.tableWidget.setHorizontalHeaderLabels(('Sample', concentrationStr)) 
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        # Set startup state for including test solution.
        self.actionIncludeDefaultTestSolutions.setChecked(True)
        self.actionIncludeUserTestSolutions.setChecked(True)

        self.user_TestSolutionDict = self.loadUserTestSolutionDict()
        self.default_TestSolutionDict = self.loadDefaultTestSolutionDict()

        self.populateTestSolutionComboBox()
        self.testSolutionComboBox.setCurrentIndex(1)

        self.updateWidgetEnabled()

    def tableWidgetItemChanged_Callback(self,item):
        print('tableWidgetItemChanged_Callback')
        if item.column() == 0:
            self.updatePlot()

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
            clipboardList.append('\r\n')
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

    def testSolutionChanged_Callback(self,index):
        print('testSolutionChanged_Callback', index)
        self.updateTestSolution(index)


    def updateTestSolution(self,index):
        if index <= 0:
            self.coeffLEDWidget.setEnabled(True)
            self.coefficientLineEdit.setText("")
            self.coeff = None
        else:
            self.coeffLEDWidget.setEnabled(False)
            itemText = str(self.testSolutionComboBox.itemText(index))
            testSolutionDict = {}
            testSolutionDict.update(self.user_TestSolutionDict)
            testSolutionDict.update(self.default_TestSolutionDict)
            pathName = testSolutionDict[itemText]
            data = file_tools.importTestSolutionData(pathName)
            self.coeff = getCoefficientFromData(data)
            self.coefficientLineEdit.setText('{0:1.1f}'.format(1.0e6*self.coeff))
            self.setLEDColor(data['led'])
        self.updateWidgetEnabled()

    def portChanged_Callback(self):
        self.port = str(self.portLineEdit.text())

    def connectPressed_Callback(self):
        if self.dev == None:
            self.connectPushButton.setText('Disconnect')
            self.connectPushButton.setFlat(True)
            self.portLineEdit.setEnabled(False)
            self.statusbar.showMessage('Connecting...')

    def connectClicked_Callback(self):
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
        self.updateWidgetEnabled()


    def cleanDataTable(self,setup=False,msg=''):
        """
        Removes any existing data from the table widget. If setup is False then
        I dialog request confirmation if presented. 
        """
        if setup:
            reply = QtGui.QMessageBox.Yes
        elif len(self.tableWidget.item(0,1).text()):
            reply = QtGui.QMessageBox.question( self, 'Message', msg, 
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        else: 
            return True

        if reply == QtGui.QMessageBox.Yes:
            if self.fig is not None:
                plt.close(self.fig)
                self.fig = None
            self.tableWidget.setRowCount(TABLE_MIN_ROW_COUNT)
            self.tableWidget.setColumnCount(TABLE_COL_COUNT)
            for row in range(TABLE_MIN_ROW_COUNT+1):
                for col in range(TABLE_COL_COUNT+1):
                    tableItem = QtGui.QTableWidgetItem()
                    tableItem.setFlags(QtCore.Qt.NoItemFlags)
                    self.tableWidget.setItem(row,col,tableItem)
            self.measIndex = 0
            return True
        else:
            return False

    def colorRadioButton_Clicked(self,color):
        if len(self.tableWidget.item(0,1).text()):
            chn_msg = "Changing channels will clear all data. Continue?"
            response = self.cleanDataTable(msg=chn_msg)
            if not response:
                color = self.currentColor
                button = getattr(self,'{0}RadioButton'.format(color))
                button.setChecked(True)
        self.currentColor = color

    def plotPushButton_Clicked(self):
        self.updatePlot(create=True)

    def calibratePressed_Callback(self):
        print('callibratePushButton_Pressed')
        self.measurePushButton.setEnabled(False)
        self.plotPushButton.setEnabled(False)
        self.clearPushButton.setEnabled(False)
        self.calibratePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Calibrating...')

    def calibrateClicked_Callback(self):
        print('calibratePushButton_Clicked')
        if not DEVEL_FAKE_MEASURE:
            self.dev.calibrate()
        self.isCalibrated = True
        self.calibratePushButton.setFlat(False)
        self.updateWidgetEnabled()

    def measurePressed_Callback(self):
        print('measPushButton_Pressed')
        self.plotPushButton.setEnabled(False)
        self.measurePushButton.setFlat(True)
        self.statusbar.showMessage('Connected, Mode: Measuring...')

    def measureClicked_Callback(self):

        rowCount = self.measIndex+1
        ledNumber = COLOR2LED_DICT[self.currentColor]

        if DEVEL_FAKE_MEASURE:  
            conc = random.random()
        else:
            freq, trans, absorb = self.dev.getMeasurement()
            conc = absorb[ledNumber]/self.coeff

        concStr = '{0:1.2f}'.format(conc)
        self.measurePushButton.setFlat(False)


        if rowCount > TABLE_MIN_ROW_COUNT:
            self.tableWidget.setRowCount(rowCount)

        # Put measurement into table
        tableItemFlags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(concStr)
        tableItem.setFlags(tableItemFlags)
        self.tableWidget.setItem(self.measIndex,1,tableItem)
        self.tableWidget.setCurrentItem(tableItem)
        tableItem.setSelected(False)

        # Select Sample table cell for data entry
        tableItemFlags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        tableItemFlags |= QtCore.Qt.ItemIsEditable
        tableItem = QtGui.QTableWidgetItem()
        tableItem.setFlags(tableItemFlags)
        tableItem.setSelected(True)
        self.tableWidget.setItem(self.measIndex,0,tableItem)
        self.tableWidget.setCurrentCell(self.measIndex,0)
        self.tableWidget.editItem(self.tableWidget.currentItem()) 

        self.measIndex+=1

        if plt.fignum_exists(PLOT_FIGURE_NUM):
            self.updatePlot()
        self.updateWidgetEnabled()

    def clearPressed_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            self.measurePushButton.setEnabled(False)
            self.plotPushButton.setEnabled(False)
        self.clearPushButton.setFlat(True)

    def clearClicked_Callback(self):
        if len(self.tableWidget.item(0,1).text()):
            erase_msg = "Clear all data?"
            self.cleanDataTable(msg=erase_msg)
        self.clearPushButton.setFlat(False) 
        self.updateWidgetEnabled()

    def saveFile_Callback(self):
        # Ensure that there is data to save.
        if self.measIndex <= 0: 
            errMsgTitle = 'Save Error'
            errMsg = 'No data to save'
            QtGui.QMessageBox.warning(self,errMsgTitle, errMsg)
            return

        # Get filename
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile) 
        fileName = dialog.getSaveFileName(
                   None,
                   'Select data file',
                   self.lastSaveDir,
                   options=QtGui.QFileDialog.DontUseNativeDialog,
                   )              
        fileName = str(fileName)
        if not fileName:
            return
        self.lastSaveDir =  os.path.split(fileName)[0]
        print(fileName)

        dataList = self.getTableData(noValueSymb=NO_VALUE_SYMBOL) 
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S %Z') 
        headerList = [ 
                '# {0}%s'.format(timeStr), 
                '# Colorimeter Data', 
                '# LED {0}'.format(self.currentColor),
                '# ----------------------------', 
                '# Label    |    Concentration ',
                ]
        headerStr = os.linesep.join(headerList)

        with open(fileName,'w') as fid:
            fid.write('{0}{1}'.format(headerStr,os.linesep))
            for x,y in dataList:
                fid.write('{0} {1}{2}'.format(x,y,os.linesep))

    def loadFile_Callback(self):
        print('loadFile_Callback')

    def editTestSolutions_Callback(self):
        print('editTestSolutions_Callback')

    def updateWidgetEnabled(self):
        """
        Updates the GUI widgets enabled properties based on the current
        state of the program.
        """
        if self.dev is None:
            self.measurePushButton.setEnabled(False)
            self.calibratePushButton.setEnabled(False)
            if self.measIndex > 0:
                self.clearPushButton.setEnabled(True)
                self.plotPushButton.setEnabled(True)
                self.tableWidget.setEnabled(True)
            else:
                self.clearPushButton.setEnabled(False)
                self.plotPushButton.setEnabled(False)
                self.tableWidget.setEnabled(False)
            self.testSolutionWidget.setEnabled(False)
            self.coeffLEDWidget.setEnabled(False)
            self.portLineEdit.setEnabled(True)
            self.statusbar.showMessage('Not Connected')
        else:
            self.testSolutionWidget.setEnabled(True)
            if self.coeff is None:
                self.calibratePushButton.setEnabled(False)
            else:
                self.calibratePushButton.setEnabled(True)
            if self.isCalibrated and self.coeff is not None:
                self.plotPushButton.setEnabled(True)
                self.clearPushButton.setEnabled(True)
                self.measurePushButton.setEnabled(True)
                self.tableWidget.setEnabled(True)
            else:
                self.plotPushButton.setEnabled(False)
                self.clearPushButton.setEnabled(False)
                self.measurePushButton.setEnabled(False)
                self.tableWidget.setEnabled(False)
            self.portLineEdit.setEnabled(False)
            self.connectPushButton.setFlat(False)
            self.statusbar.showMessage('Connected, Mode: Stopped')

    def updatePlot(self,create=False):

        if self.measIndex == 0:
            #  We don't have any measurements - close any existing plot and
            #  return
            if plt.fignum_exists(PLOT_FIGURE_NUM):
                plt.close(self.fig)
                self.fig = None
            return

        if not create and not plt.fignum_exists(PLOT_FIGURE_NUM):
            return

        dataList = self.getTableData()
        labelList, concList = zip(*dataList)

        # Create plot showing bar graph of data
        posList = range(1,len(concList)+1)
        xlim = (posList[0]-0.5*PLOT_BAR_WIDTH, posList[-1]+1.5*PLOT_BAR_WIDTH)
        ylim = (0,PLOT_YLIM_ADJUST*max(concList))

        plt.clf()
        self.fig = plt.figure(PLOT_FIGURE_NUM)
        self.fig.canvas.manager.set_window_title('Colorimeter Measurement: Concentration Plot')
        ax = self.fig.add_subplot(111)
        ax.bar(posList,concList,width=PLOT_BAR_WIDTH,color='b',linewidth=2)

        for pos, value in zip(posList, concList): 
            textXPos = pos + 0.5*PLOT_BAR_WIDTH
            textYPos = value + PLOT_TEXT_Y_OFFSET
            valueStr = '{0:1.3f}'.format(value)
            ax.text(textXPos,textYPos, valueStr, ha ='center', va ='bottom') 

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_xticks([x+0.5*PLOT_BAR_WIDTH for x in posList])
        ax.set_xticklabels(labelList)
        ax.set_ylabel('Concentration')
        ax.set_xlabel('Samples')
        plt.draw() 

    def getTableData(self,noValueSymb=None):

        concList = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i,1)
            try:
                value = float(item.text())
                concList.append(value)
            except ValueError, e:
                errMsgTitle = 'Plot Error'
                errMsg = 'Unable to convert value to float: {0}'.format(str(e))
                QtGui.QMessageBox.warning(self,errMsgTitle, errMsg)
                return

        labelList = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i,0)
            label = str(item.text())
            if not label:
                if noValueSymb is None:
                    labelList.append('{0}'.format(item.row()+1))
                else:
                    labelList.append(NO_VALUE_SYMBOL)
            else:
                labelList.append(label)

        dataList = zip(labelList, concList)
        return dataList

    def setLEDColor(self,color):
        self.currentColor = color
        button = getattr(self, '{0}RadioButton'.format(self.currentColor))
        button.setChecked(True)

    def loadDefaultTestSolutionDict(self):
        """
        Load the dictionary mapping the test solution name to the test solution
        data from the default location.
        """
        ## Works with pyinstaller
        ## ---------------------------------------------------------------
        #default_TestSolutionDir = getResourcePath('data')
        #fileList = getTestSolutionFilesFromDir(default_TestSolutionDir)
        ## ---------------------------------------------------------------
        fileList = self.getTestSolutionFilesFromResources()
        return file_tools.loadTestSolutionDict(fileList,tag='D')

    def loadUserTestSolutionDict(self):
        """
        Load the dictionary mapping test solution name to test solution data
        file from the user's directory.
        """
        userTestSolutionDir = file_tools.getUserTestSolutionDir(self.userHome)
        fileList = file_tools.getTestSolutionFilesFromDir(userTestSolutionDir)
        return file_tools.loadTestSolutionDict(fileList,tag='U')

    def getTestSolutionFilesFromResources(self): 
        """
        Get the list of test solution files form the package resources.
        """
        fileNames = pkg_resources.resource_listdir(__name__,'data')
        testFiles = []
        for name in fileNames:
            pathName = pkg_resources.resource_filename(__name__,'data/{0}'.format(name))
            testFiles.append(pathName)
        return testFiles

    def populateTestSolutionComboBox(self):
        """
        Populates the test solution combobox for the currently selected
        options (via the Options menu).
        """
        self.testSolutionComboBox.clear()
        self.testSolutionComboBox.addItem('-- (manually specify) --')
        includeDflt = self.actionIncludeDefaultTestSolutions.isChecked()
        includeUser = self.actionIncludeUserTestSolutions.isChecked()

        # Add default test solutions
        if includeDflt:
            for name in sorted(self.default_TestSolutionDict):
                self.testSolutionComboBox.addItem(name)

        if includeDflt and includeUser:
            count = self.testSolutionComboBox.count()+1
            self.testSolutionComboBox.insertSeparator(count)

        # Add user test solutions
        if includeUser:
            for name in sorted(self.user_TestSolutionDict):
                self.testSolutionComboBox.addItem(name)

        index = min([1,self.testSolutionComboBox.count()-1])
        self.testSolutionComboBox.setCurrentIndex(index)
        self.updateTestSolution(index)

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

def getCoefficientFromData(data): 
    """
    Compuetes the coefficient (slope of absorbance vs concentration)
    """
    values = data['values']
    xList, yList = zip(*values)
    xArray = numpy.array(xList)
    yArray = numpy.array(yList)
    numer = (xArray*yArray).sum()
    denom = (xArray*xArray).sum()
    slope = numer/denom
    coeff = 1.0/slope
    return coeff 

def getResourcePath(relative_path): 
    """
    Get path of resources file in both deployed and development.
    """
    base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))
    resource_path = os.path.join(base_path, relative_path)
    return resource_path

def measurementGuiMain():
    """
    Entry point for measurement gui
    """
    app = QtGui.QApplication(sys.argv)
    mainWindow = MeasurementMainWindow()
    mainWindow.main()
    app.exec_()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    measurementGuiMain()

