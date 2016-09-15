from __future__ import print_function
import os 
import sys 
import random 
import time
import numpy
import random
import matplotlib
import matplotlib.pyplot as plt 
plt.ion()

from PyQt4 import QtCore
from PyQt4 import QtGui

from measure_ui import Ui_MainWindow 
from colorimeter import constants 
from colorimeter import import_export 
from colorimeter import standard_curve
from colorimeter import nonlinear_fit
from colorimeter.main_window import MainWindowWithTable

class MeasureMainWindow(MainWindowWithTable, Ui_MainWindow):

    def __init__(self,parent=None):
        super(MeasureMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.createActionGroup()
        self.connectActions()
        self.initialize()

    def createActionGroup(self):
        self.unitsActionGroup = QtGui.QActionGroup(self)
        self.unitsActionGroup.addAction(self.actionSampleUnitsUM)
        self.unitsActionGroup.addAction(self.actionSampleUnitsPPM)
        self.unitsActionGroup.addAction(self.actionSampleUnitsPH)
        self.unitsActionGroup.setExclusive(True)

    def connectActions(self):
        super(MeasureMainWindow,self).connectActions()
        self.testSolutionComboBox.currentIndexChanged.connect(
                self.testSolutionChanged_Callback
                )
        self.actionIncludeDefaultTestSolutions.toggled.connect(
                self.populateTestSolutionComboBox
                )
        self.actionIncludeUserTestSolutions.toggled.connect(
                self.populateTestSolutionComboBox
                )
        self.coefficientLineEdit.editingFinished.connect(
                self.coeffEditingFinished_Callback
                )
        coeffValidator = QtGui.QDoubleValidator(self.coefficientLineEdit) 
        coeffValidator.setBottom(0)
        coeffValidator.fixup = self.coeffFixup
        self.coefficientLineEdit.setValidator(coeffValidator)

        self.unitsActionGroup.triggered.connect(self.unitsChanged_Callback)

    def initialize(self):
        super(MeasureMainWindow,self).initialize()
        self.coeff = None
        self.fitType = 'linear'
        self.fitParam = None
        self.fitValues = None
        self.testSolutionIndex = 1
        self.user_TestSolutionDict = {}
        self.default_TestSolutionDict = {} 
        self.noValueSymbol = constants.NO_VALUE_SYMBOL_LABEL
        self.aboutText = constants.MEASURE_ABOUT_TEXT

        # Set up data table
        self.tableWidget.clean(setup=True)
        self.tableWidget.updateFunc = self.updatePlot

        # Set startup state for including test solution.
        self.actionIncludeDefaultTestSolutions.setChecked(True)
        self.actionIncludeUserTestSolutions.setChecked(True)
        self.updateTestSolutionDicts()
        self.populateTestSolutionComboBox()
        self.testSolutionComboBox.setCurrentIndex(self.testSolutionIndex)

        self.setUnits('um')
        self.updateWidgetEnabled()

    def connectClicked_Callback(self):
        super(MeasureMainWindow,self).connectClicked_Callback()
        self.updateTestSolution(self.testSolutionIndex)

    def coeffEditingFinished_Callback(self):
        value = self.coefficientLineEdit.text()
        value = float(value)
        self.coeff = value
        self.fitType = 'linear'
        self.fitParam = None
        self.updateWidgetEnabled()

    def coeffFixup(self,value):
        value = str(value)
        if not value:
            self.coeff = None
            self.fitType = 'linear'
            self.fitParam = None
            self.updateWidgetEnabled()

    def editTestSolutions_Callback(self):
        changed = super(MeasureMainWindow,self).editTestSolutions_Callback()
        if changed:
            self.updateTestSolutionDicts()
            self.populateTestSolutionComboBox()

    def testSolutionChanged_Callback(self,index):
        try:
            testSolutionIndex = self.testSolutionIndex
        except AttributeError:
            # Dummy value used prior to initializion - when setting up widgets
            testSolutionIndex = 0

        if index != testSolutionIndex:
            erase_msg = "Change test solution and clear all data?"
            rsp = self.tableWidget.clean(msg=erase_msg)
            if rsp:
                self.isCalibrated = False
                self.updateTestSolution(index)
            else:
                self.testSolutionComboBox.setCurrentIndex(
                        self.testSolutionIndex
                        )

    def unitsChanged_Callback(self):
        if self.actionSampleUnitsUM.isChecked():
            self.setUnits('uM')
        elif self.actionSampleUnitsPPM.isChecked():
            self.setUnits('ppm')
        else:
            self.setUnits('pH')


    def updateTestSolution(self,index):
        if index <= 0:
            self.coeffLEDWidget.setEnabled(True)
            self.setLEDRadioButtonsEnabled(True)
            self.unitsActionGroup.setEnabled(True)
            self.coefficientLineEdit.setText("")
            self.coeff = None
        else:
            self.coeffLEDWidget.setEnabled(False)
            self.unitsActionGroup.setEnabled(False)
            itemText = str(self.testSolutionComboBox.itemText(index))
            testSolutionDict = {}
            testSolutionDict.update(self.user_TestSolutionDict)
            testSolutionDict.update(self.default_TestSolutionDict)
            try:
                pathName = testSolutionDict[itemText]
            except KeyError:
                return
            data = import_export.importTestSolutionData(pathName)
            if not self.checkImportData(data):
                return
            self.fitType = data['fitType']
            self.fitParams = data['fitParams']
            self.fitValues = data['values']
            self.setUnits(data['units'])
            self.coeff = getCoefficientFromData(data,self.fitType,self.fitParams)
            if self.fitType == 'linear':
                self.coefficientLineEdit.setText('{0:1.1f}'.format(1.0e6*self.coeff))
            else:
                self.coefficientLineEdit.setText(' -- nonlinear --')
            if data['led'] == 'custom':
                ledText = 'D1'
            else:
                ledText = data['led']
            self.setLEDByText(ledText)

        self.testSolutionIndex = index
        self.updateWidgetEnabled()

    def getMeasurement(self):
        if constants.DEVEL_FAKE_MEASURE:    
            absorbValue = random.random()
            #  TestFit
            #  ----------------------------------------
            #for valueIn, abso in self.fitValues:
            #    valueOut = self.absorbanceToUnit(abso)
            #    print(abso, valueIn, valueOut)
        else:
            modeConfig = self.getModeConfig()
            ledDict = modeConfig['LED'][self.currentLED]
            dummy0, dummy1, absorbValue = self.dev.getMeasurement(color=ledDict['devColor'])

        try:
            measurementValue = self.absorbanceToUnit(absorbValue)
        except ValueError, err: 
            msgTitle = 'Range Error'
            msgText = str(err)
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            return
        digits = self.getSignificantDigits()
        measurementStr = '{value:1.{digits}f}'.format(value=measurementValue,digits=digits)
        self.measurePushButton.setFlat(False)

        self.tableWidget.addData('',measurementStr,selectAndEdit=True)

    def absorbanceToUnit(self,absorb):
        if self.fitType == 'linear':
            value = absorb/self.coeff
        else:
            value = nonlinear_fit.getValueFromFit(self.coeff,absorb)
        return value


    def getSaveFileHeader(self):
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S %Z') 
        ledInfoStr = self.getLEDSaveInfoStr()
        headerList = [ 
                '# {0}'.format(timeStr), 
                '# Colorimeter Data', 
                '# LED {0}'.format(ledInfoStr),
                '# ----------------------------', 
                ]
        if self.units.lower() in ('ppm','um'):
            headerList.append('# Label    |    Concentration ')
        else:
            headerList.append('# Label    |    pH ')
        headerStr = os.linesep.join(headerList)
        return headerStr

    def updateWidgetEnabled(self):
        super(MeasureMainWindow,self).updateWidgetEnabled()
        if self.dev is None:
            self.testSolutionWidget.setEnabled(False)
            self.coeffLEDWidget.setEnabled(False)
        else:
            self.testSolutionWidget.setEnabled(True)
            if self.coeff is None:
                self.calibratePushButton.setEnabled(False)
                self.measurePushButton.setEnabled(False)
                self.plotPushButton.setEnabled(False)
            else:
                self.calibratePushButton.setEnabled(True)
        self.repaint() # (Hack) Appears to be needed so that color LED radio buttons 'checked' 
                       #  will update even when disabled

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
        labelList, sampleList = zip(*dataList)
        posList = range(1,len(sampleList)+1)
        xlim = (
                posList[0]  - 0.5*constants.PLOT_BAR_WIDTH, 
                posList[-1] + 1.5*constants.PLOT_BAR_WIDTH,
                )
        ylim = (0,constants.PLOT_YLIM_ADJUST*max(sampleList))
        plt.clf()
        self.fig = plt.figure(constants.PLOT_FIGURE_NUM)
        if self.units.lower() in ('um','ppm'):
            titleStr = 'Colorimeter Measurement: Concentration Plot'
            yLabelStr = 'Concentration ({0})'.format(self.units)
        else:
            titleStr = 'Colorimeter Measurement: PH'
            yLabelStr = '(PH)'
        self.fig.canvas.manager.set_window_title(titleStr)
        ax = self.fig.add_subplot(111)
        ax.bar(posList,sampleList,width=constants.PLOT_BAR_WIDTH,color='b',linewidth=2)

        digits = self.getSignificantDigits()
        for pos, value in zip(posList, sampleList): 
            textXPos = pos + 0.5*constants.PLOT_BAR_WIDTH
            textYPos = value + constants.PLOT_TEXT_Y_OFFSET
            valueStr = '{value:1.{digits}f}'.format(value=value,digits=digits)
            ax.text(textXPos,textYPos, valueStr, ha ='center', va ='bottom') 

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_xticks([x+0.5*constants.PLOT_BAR_WIDTH for x in posList])
        ax.set_xticklabels(labelList)
        ax.set_ylabel(yLabelStr)
        ax.set_xlabel('Samples')
        plt.draw() 

    def updateTestSolutionDicts(self):
        # User test solutions
        self.user_TestSolutionDict = self.loadUserTestSolutionDict()
        self.user_TestSolutionDict = self.filterTestSolutionDict(
                self.user_TestSolutionDict, 
                self.sensorMode
                )
        # Default test solutinos
        self.default_TestSolutionDict = self.loadDefaultTestSolutionDict()
        self.default_TestSolutionDict = self.filterTestSolutionDict(
                self.default_TestSolutionDict,
                self.sensorMode
                )

    def filterTestSolutionDict(self,testSolutionDict,mode):
        newTestSolutionDict = {}
        for testName, pathName in testSolutionDict.iteritems():
            data = import_export.importTestSolutionData(pathName)
            dataSensorMode, dummy = import_export.getModeAndLEDTextFromData(data)
            if dataSensorMode == mode:
                newTestSolutionDict[testName] = pathName
        return newTestSolutionDict

    def loadDefaultTestSolutionDict(self):
        return import_export.loadDefaultTestSolutionDict()

    def loadUserTestSolutionDict(self):
        userTestSolutionDir = import_export.getUserTestSolutionDir(self.userHome)
        fileList = import_export.getTestSolutionFilesFromDir(userTestSolutionDir)
        return import_export.loadTestSolutionDict(fileList,tag='U')

    def populateTestSolutionComboBox(self):
        self.testSolutionComboBox.clear()
        self.testSolutionComboBox.addItem('-- (manually specify) --')
        includeDflt = self.actionIncludeDefaultTestSolutions.isChecked()
        includeUser = self.actionIncludeUserTestSolutions.isChecked()

        # Add default test solutions
        if includeDflt:
            for name in sorted(self.default_TestSolutionDict):
                self.testSolutionComboBox.addItem(name)

        # Add user test solutions
        if includeUser:
            for name in sorted(self.user_TestSolutionDict):
                self.testSolutionComboBox.addItem(name)

        index = min([1,self.testSolutionComboBox.count()-1])
        self.testSolutionComboBox.setCurrentIndex(index)
        self.updateTestSolution(index)

    def setTableData(self,dataList):
        dataList = dataListToLabelAndFloat(dataList)
        self.tableWidget.clean(setup=True)
        for label, conc in dataList:
            if label == self.noValueSymbol:
                label = ''
            else:
                label = str(label)
            conc = str(conc)
            self.tableWidget.addData(label,conc)

    def checkImportData(self,data): 
        msgTitle = 'Import Error'
        if not data['fitType'] in ('linear', 'polynomial'):
            msgText = 'unknown fit type: {0}'.format(data['fitType']) 
            QtGui.QMessageBox.warning(self,msgTitle, msgText)
            return False

        if data['fitType'] == 'polynomial':
            if data['fitParams'] not in (2,3,4,5):
                msgText = 'unsuported polynomial order: {0}'.format(fitParams) 
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                return False
        return True

    def setUnits(self,units):
        if units.lower() == 'um':
            self.actionSampleUnitsUM.setChecked(True)
            self.actionSampleUnitsPPM.setChecked(False)
            self.actionSampleUnitsPH.setChecked(False)
            unitStr = QtCore.QString.fromUtf8("Concentration (\xc2\xb5M)")
        elif units.lower() == 'ppm':
            self.actionSampleUnitsUM.setChecked(False)
            self.actionSampleUnitsPPM.setChecked(True)
            self.actionSampleUnitsPH.setChecked(False)
            unitStr = QtCore.QString('Concentration (ppm)')
        else:
            self.actionSampleUnitsUM.setChecked(False)
            self.actionSampleUnitsPPM.setChecked(False)
            self.actionSampleUnitsPH.setChecked(True)
            unitStr = QtCore.QString('(pH)')
        self.units = units
        self.tableWidget.setHorizontalHeaderLabels(('Sample', unitStr)) 

    def setMode(self,value):
        super(MeasureMainWindow,self).setMode(value)
        self.updateTestSolutionDicts()
        self.populateTestSolutionComboBox()
        if self.testSolutionComboBox.count() > 1:
            index = 1
        else:
            index = 0
        self.updateTestSolution(index)

    def setLEDRadioButtonsEnabled(self,value):
        modeConfig = self.getModeConfig()
        for ledNum in modeConfig['LED']:
            button = getattr(self,'LED{0}RadioButton'.format(ledNum))
            button.setEnabled(value)

def dataListToLabelAndFloat(dataList):
    dataListNew = []
    for x,y in dataList:
        try: 
            y = float(y)
        except ValueError:
            continue
        dataListNew.append((x,y))
    return dataListNew

def getCoefficientFromData(data,fitType,fitParams): 
    values = data['values']
    abso, conc = zip(*values)
    if fitType == 'linear':
        coeff = standard_curve.getCoefficient(abso,conc,fitType=constants.LINEAR_FIT_TYPE)
    elif fitType == 'polynomial':
        order = fitParams
        coeff, dummy0, dummy1 = nonlinear_fit.getPolynomialFit(abso,conc,order=order)
    return coeff

def startMeasureMainWindow(app):
    mainWindow = MeasureMainWindow()
    mainWindow.main()
    app.exec_()

def startMeasureApp():
    app = QtGui.QApplication(sys.argv)
    startMeasureMainWindow(app)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    startMeasureApp()

