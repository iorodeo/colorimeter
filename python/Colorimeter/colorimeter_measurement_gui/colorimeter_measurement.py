from __future__ import print_function
import os 
import sys 
import random 
import time
import numpy
import pkg_resources
# TEMPORARY - FOR DEVELOPMENT ##################
import random
################################################

import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt 
plt.ion()

from PyQt4 import QtCore
from PyQt4 import QtGui

from colorimeter_measurement_ui import Ui_MainWindow 
from colorimeter_common import constants 
from colorimeter_common import import_export 
from colorimeter_common import standard_curve
from colorimeter_common.main_window import MainWindowWithTable

class MeasurementMainWindow(MainWindowWithTable, Ui_MainWindow):

    def __init__(self,parent=None):
        super(MeasurementMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.initialize()
        self.connectActions()

    def connectActions(self):
        super(MeasurementMainWindow,self).connectActions()
        self.testSolutionComboBox.currentIndexChanged.connect(
                self.testSolutionChanged_Callback
                )
        self.actionIncludeDefaultTestSolutions.toggled.connect(
                self.populateTestSolutionComboBox
                )
        self.actionIncludeUserTestSolutions.toggled.connect(
                self.populateTestSolutionComboBox
                )

    def initialize(self):
        super(MeasurementMainWindow,self).initialize()
        self.coeff = None

        # Set up data table
        self.tableWidget.clean(setup=True)
        self.tableWidget.updateFunc = self.updatePlot
        concentrationStr = QtCore.QString.fromUtf8("Concentration (\xc2\xb5M)")
        self.tableWidget.setHorizontalHeaderLabels(('Sample', concentrationStr)) 

        # Set startup state for including test solution.
        self.actionIncludeDefaultTestSolutions.setChecked(True)
        self.actionIncludeUserTestSolutions.setChecked(True)
        self.user_TestSolutionDict = self.loadUserTestSolutionDict()
        self.default_TestSolutionDict = self.loadDefaultTestSolutionDict()
        self.populateTestSolutionComboBox()
        self.testSolutionComboBox.setCurrentIndex(1)
        self.updateWidgetEnabled()

    def testSolutionChanged_Callback(self,index):
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
            data = import_export.importTestSolutionData(pathName)
            self.coeff = getCoefficientFromData(data)
            self.coefficientLineEdit.setText('{0:1.1f}'.format(1.0e6*self.coeff))
            self.setLEDColor(data['led'])
        self.updateWidgetEnabled()

    def getMeasurement(self):
        ledNumber = constants.COLOR2LED_DICT[self.currentColor]
        if constants.DEVEL_FAKE_MEASURE:  
            conc = random.random()
        else:
            freq, trans, absorb = self.dev.getMeasurement()
            conc = absorb[ledNumber]/self.coeff

        concStr = '{0:1.2f}'.format(conc)
        self.measurePushButton.setFlat(False)
        self.tableWidget.addData('',concStr,selectAndEdit=True)

    def saveFile_Callback(self):
        if self.tableWidget.measIndex <= 0: 
            errMsgTitle = 'Save Error'
            errMsg = 'No data to save'
            QtGui.QMessageBox.warning(self,errMsgTitle, errMsg)
            return

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

        dataList = self.tableWidget.getData(noValueSymb=constants.NO_VALUE_SYMBOL_LABEL) 
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
            if self.tableWidget.measIndex > 0:
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

        # Only create new figure is asked to do so
        if not create and not plt.fignum_exists(constants.PLOT_FIGURE_NUM):
            return

        # Check if there is any data to plot
        dataList = self.tableWidget.getData()
        dataList = dataListToLabelAndFloat(dataList)
        if not dataList:
            self.closeFigure()
            return 
        # Unpack data and create plot 
        labelList, concList = zip(*dataList)
        posList = range(1,len(concList)+1)
        xlim = (
                posList[0]  - 0.5*constants.PLOT_BAR_WIDTH, 
                posList[-1] + 1.5*constants.PLOT_BAR_WIDTH,
                )
        ylim = (0,constants.PLOT_YLIM_ADJUST*max(concList))
        plt.clf()
        self.fig = plt.figure(constants.PLOT_FIGURE_NUM)
        self.fig.canvas.manager.set_window_title('Colorimeter Measurement: Concentration Plot')
        ax = self.fig.add_subplot(111)
        ax.bar(posList,concList,width=constants.PLOT_BAR_WIDTH,color='b',linewidth=2)

        for pos, value in zip(posList, concList): 
            textXPos = pos + 0.5*constants.PLOT_BAR_WIDTH
            textYPos = value + constants.PLOT_TEXT_Y_OFFSET
            valueStr = '{0:1.3f}'.format(value)
            ax.text(textXPos,textYPos, valueStr, ha ='center', va ='bottom') 

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_xticks([x+0.5*constants.PLOT_BAR_WIDTH for x in posList])
        ax.set_xticklabels(labelList)
        ax.set_ylabel('Concentration')
        ax.set_xlabel('Samples')
        plt.draw() 

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
        return import_export.loadTestSolutionDict(fileList,tag='D')

    def loadUserTestSolutionDict(self):
        """
        Load the dictionary mapping test solution name to test solution data
        file from the user's directory.
        """
        userTestSolutionDir = import_export.getUserTestSolutionDir(self.userHome)
        fileList = import_export.getTestSolutionFilesFromDir(userTestSolutionDir)
        return import_export.loadTestSolutionDict(fileList,tag='U')

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

def dataListToLabelAndFloat(dataList):
    dataListNew = []
    for x,y in dataList:
        try: 
            y = float(y)
        except ValueError:
            continue
        dataListNew.append((x,y))
    return dataListNew

def getCoefficientFromData(data): 
    values = data['values']
    abso, conc = zip(*values)
    coeff = standard_curve.getCoefficient(abso,conc,fitType=constants.FIT_TYPE)
    return coeff

def getResourcePath(relative_path): 
    base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))
    resource_path = os.path.join(base_path, relative_path)
    return resource_path

def measurementGuiMain():
    app = QtGui.QApplication(sys.argv)
    mainWindow = MeasurementMainWindow()
    mainWindow.main()
    app.exec_()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    measurementGuiMain()

