from __future__ import print_function
import os 
import sys 
import platform
import functools
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
from colorimeter_serial import Colorimeter


DEVEL_FAKE_MEASURE = True 
DFLT_PORT_WINDOWS = 'com1' 
DFLT_PORT_LINUX = '/dev/ttyACM0' 
TABLE_MIN_ROW_COUNT = 4
TABLE_COL_COUNT = 2
FIT_TYPE = 'force_zero'
DEFAULT_LED = 'red'
COLOR2LED_DICT = {'red':0,'green':1,'blue': 2,'white': 3} 
PLOT_FIGURE_NUM = 1

class ColorimeterPlotMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self,parent=None):
        super(ColorimeterPlotMainWindow,self).__init__(parent)
        self.color2LED_Dict = COLOR2LED_DICT
        self.setupUi(self)
        self.connectActions()
        self.initialize()

    def connectActions(self):
        self.action_Save.triggered.connect(self.saveFile_Callback)
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
        self.setWidgetEnabledOnDisconnect()

        self.tableWidget.setHorizontalHeaderLabels(('Concentration','Absorbance')) 
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

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
            disconnect_msg = "Disconnecting will clear all data. Continue?"
            response = self.cleanDataTable(msg=disconnect_msg)
            if response == True:
                self.connectPushButton.setText('Connect')
                try:
                    self.cleanUpAndCloseDevice()
                except Exception, e:
                    QtGui.QMessageBox.critical(self,'Error', str(e))
                self.measIndex = 0
                connected = False
            if response == False:
                connected = True

        if connected:
            self.setWidgetEnabledOnConnect()
        else:
            self.setWidgetEnabledOnDisconnect()

    def closeEvent(self,event):
        if self.dev is not None:
            self.cleanUpAndCloseDevice()
        event.accept()

    def cleanUpAndCloseDevice(self):
        self.dev.close()
        self.dev = None

    def colorRadioButtonClicked_Callback(self,color):
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

        # ---------------------------------------------------------------------
        # Need to check that we have all concentration values and give 
        # reasonable message if we don't.
        # ---------------------------------------------------------------------

        print('plotPushButtonClicked_Callback',self.measIndex)
        dataList = []
        for i in range(self.measIndex):
            tableItem = self.tableWidget.item(i,1)
            x = float(tableItem.text())
            tableItem = self.tableWidget.item(i,0)
            try:
                y = float(tableItem.text())
            except ValueError, e:
                errMsgTitle = 'Plot Error'
                errMsg = 'Unable to convert concentration value to float.'
                QtGui.QMessageBox.warning(self,errMsgTitle, errMsg)
                return
            dataList.append((x,y))

        yList = [x for x,y in dataList]
        xList = [y for x,y in dataList]

        if len(dataList) > 1:
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

        rowCount = self.measIndex+1
        
        # ---------------------------------------------------------------------
        #if rowCount == 2:
        #    if not len(self.tableWidget.item(0,0).text()):
        #        errMsgTitle = 'Missing Value'
        #        errMsg = 'Concentration value not entered.'
        #        QtGui.QMessageBox.warning(self,errMsgTitle, errMsg)
        # --------------------------------------------------------------------

        if DEVEL_FAKE_MEASURE:
            absorb = (random.random(),)*4
        else:
            freq, trans, absorb = self.dev.getMeasurement()

        self.measurePushButton.setFlat(False)
        ledNumber = COLOR2LED_DICT[self.currentColor]
        absorbStr = '{0:1.2f}'.format(absorb[ledNumber])

        if rowCount > TABLE_MIN_ROW_COUNT:
            self.tableWidget.setRowCount(rowCount)

        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(absorbStr)
        tableItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(self.measIndex,1,tableItem)

        tableItem = QtGui.QTableWidgetItem()
        tableItem.setSelected(True)
        self.tableWidget.setItem(self.measIndex,0,tableItem)

        self.tableWidget.setCurrentCell(self.measIndex,0)
        self.tableWidget.editItem(self.tableWidget.currentItem()) 

        self.measIndex+=1
        self.setWidgetEnabledOnConnect()

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
        self.setWidgetEnabledOnConnect()

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
        self.setWidgetEnabledOnConnect()

    def saveFile_Callback(self):
        print('savePushButton_Clicked',self.measIndex)
        
        # ---------------------------------------------------------------------
        # Need to check that we have all concentrations values
        # --------------------------------------------------------------------- 

        if 1:#self.measIndex > 1:
            dialog = QtGui.QFileDialog()
            dialog.setFileMode(QtGui.QFileDialog.AnyFile) 
            filename = dialog.getSaveFileName(
                       None,
                       'Select log file',
                       self.lastLogDir,
                       options=QtGui.QFileDialog.DontUseNativeDialog,
                       )              
            filename = str(filename)
            self.lastLogDir =  os.path.split(filename)[0]
            dataList = []
            for i in range(self.measIndex):
                tableItem = self.tableWidget.item(i,1)
                x = float(tableItem.text())
                tableItem = self.tableWidget.item(i,0)
                y = float(tableItem.text())
                dataList.append((x,y))
            header = [
                      time.strftime('# %Y-%m-%d %H:%M:%S %Z'), \
                      '# IO Rodeo\'s Plot Slammer v0.1', \
                      '# -----------------------------', \
                      '# Absorbance  |  Concentration', \
                    ]

            with open(filename,'w') as f:
                f.write("\n".join(header))
                for x,y in dataList:
                    f.write("\n%s\t\t  %s" % (x,y))
        else:
            print('No data to save')

    def haveConcentrationData(self):
        """
        Checks to see if there is a concetration value for every absorbance 
        measurement.
        """

    def setWidgetEnabledOnDisconnect(self):
        self.calibratePushButton.setEnabled(False)
        self.measurePushButton.setEnabled(False)
        self.plotPushButton.setEnabled(False)
        self.clearPushButton.setEnabled(False)
        self.tableWidget.setEnabled(False)
        self.portLineEdit.setEnabled(True)
        self.statusbar.showMessage('Not Connected')
        self.cleanDataTable()
        self.isCalibrated = False

    def setWidgetEnabledOnConnect(self):
        self.calibratePushButton.setEnabled(True)
        if self.isCalibrated:
            self.plotPushButton.setEnabled(True)
            self.clearPushButton.setEnabled(True)
            self.measurePushButton.setEnabled(True)
            self.tableWidget.setEnabled(True)
        self.portLineEdit.setEnabled(False)
        self.connectPushButton.setFlat(False)
        self.statusbar.showMessage('Connected, Mode: Stopped')

    def cleanDataTable(self,setup=False,msg=''):
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

    def __init__(self,*args,**kwargs):
        super(DoubleItemDelegate,self).__init__(*args,**kwargs)

    def createEditor(self,parent,option,index):
        editor = super(DoubleItemDelegate,self).createEditor(parent,option,index)
        validator = DoubleValidator(editor)
        validator.setBottom(0.0)
        editor.setValidator(validator)
        return editor

class DoubleValidator(QtGui.QDoubleValidator):

    def __init__(self,*args,**kwargs):
        print('__init__')
        super(DoubleValidator,self).__init__(*args,**kwargs)

    def fixup(self,value):
        print('fixup')
        super(DoubleValidator,self).fixup(value)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    plotGuiMain()
