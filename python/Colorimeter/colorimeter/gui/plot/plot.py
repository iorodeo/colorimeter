import os 
import sys 
import math
import random 
import time
import numpy
import matplotlib
import matplotlib.pyplot as plt 
plt.ion()

from PyQt4 import QtCore
from PyQt4 import QtGui

from plot_ui import Ui_MainWindow 
from colorimeter import constants
from colorimeter import import_export 
from colorimeter import standard_curve
from colorimeter import nonlinear_fit
from colorimeter.main_window import MainWindowWithTable
from colorimeter.gui.dialog.test_solution_dialog import TestSolutionDialog

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

        self.fitTypeActionGroup = QtGui.QActionGroup(self)
        self.fitTypeActionGroup.addAction(self.actionFitTypeLinear)
        self.fitTypeActionGroup.addAction(self.actionFitTypePolynomial2)
        self.fitTypeActionGroup.addAction(self.actionFitTypePolynomial3)
        self.fitTypeActionGroup.addAction(self.actionFitTypePolynomial4)
        self.fitTypeActionGroup.addAction(self.actionFitTypePolynomial5)
        self.fitTypeActionGroup.setExclusive(True)
        self.fitTypeActionGroup.triggered.connect(self.fitTypeChanged_Callback)

        self.unitsActionGroup = QtGui.QActionGroup(self)
        self.unitsActionGroup.addAction(self.actionUnitsUM)
        self.unitsActionGroup.addAction(self.actionUnitsPPM)
        self.unitsActionGroup.addAction(self.actionUnitsPH)
        self.unitsActionGroup.setExclusive(True)
        self.unitsActionGroup.triggered.connect(self.unitsChanged_Callback)

        itemDelegate = DoubleItemDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0,itemDelegate)

    def initialize(self):
        super(PlotMainWindow,self).initialize()
        self.aboutText = constants.PLOT_ABOUT_TEXT
        self.noValueSymbol = constants.NO_VALUE_SYMBOL_NUMBER
        self.tableWidget.clean(setup=True)
        self.tableWidget.updateFunc = self.updatePlot
        self.updateWidgetEnabled()
        self.setFitType('linear',None)
        self.setUnits('uM')

    def importData_Callback(self):
        userSolutionDict = import_export.loadUserTestSolutionDict(self.userHome,tag='U')
        dfltSolutionDict = import_export.loadDefaultTestSolutionDict(tag='D')
        solutionDict = dict(userSolutionDict.items() + dfltSolutionDict.items())
        data = TestSolutionDialog().importData(solutionDict)
        if data is not None:
            sensorMode, ledText  = import_export.getModeAndLEDTextFromData(data)
            self.setMode(sensorMode)
            self.setLEDByText(ledText)
            self.setTableData(data['values'])
            self.setFitType(data['fitType'],data['fitParams'])
            self.setUnits(data['units'])
        self.updateWidgetEnabled()
        self.updatePlot(create=False)
        
    def exportData_Callback(self):
        dataList = self.tableWidget.getData()
        fitType, fitParams = self.getFitTypeAndParams()

        if fitType == 'linear':
            if len(dataList) < 2:
                msgTitle = 'Export Error'
                msgText = 'insufficient data for export w/ linear fit' 
                msgText += ' - must have at least 2 points'
                QtGui.QMessageBox.warning(self,msgTitle, msgText)
                return

        elif fitType == 'polynomial':
            order = fitParams
            if len(dataList) <= order:
                msgTitle = 'Export Error'
                msgText = 'insufficient data for export w/ order={0} polynomial'.format(order)
                msgText += ', must have at least {0} points'.format(order+1)
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
        modeConfig = self.getModeConfig()
        ledText = modeConfig['LED'][self.currentLED]['text']
        dataDict = { 
                'name': solutionName,
                'date': dateStr,
                'led':  ledText,
                'mode': self.sensorMode, 
                'values': [map(float,x) for x in dataList],
                'fitType': fitType,
                'units': self.getUnits(),
                }
        if fitParams is not None:
            try:
                dataDict['fitParams'] = list(fitParams),
            except TypeError:
                dataDict['fitParams'] = fitParams
        else:
            dataDict['fitParams'] = 'None'

        import_export.exportTestSolutionData(self.userHome,dataDict)

    def fitTypeChanged_Callback(self):
        self.updatePlot()

    def unitsChanged_Callback(self):
        self.setUnitStr()
        self.updatePlot()

    def updatePlot(self,create=False):

        if not create and not plt.fignum_exists(constants.PLOT_FIGURE_NUM):
            return
        dataList = self.tableWidget.getData(noValueInclude=False)
        dataList = dataListToFloat(dataList)
        if not dataList:
            self.closeFigure()
            return
        xList,yList = zip(*dataList)

        fitType, fitParams = self.getFitTypeAndParams()

        haveFit = False
        haveSlope = False
        if fitType == 'linear':
            if len(dataList) > 1:
                slope, xFit, yFit = standard_curve.getLinearFit(
                        xList,
                        yList,
                        fitType=constants.LINEAR_FIT_TYPE,
                        numPts=constants.PLOT_FIT_NUM_PTS,
                        )
                haveFit = True
                haveSlope = True
        elif fitType == 'polynomial':
            order = fitParams
            if len(dataList) > order:
                coeff, xFit, yFit = nonlinear_fit.getPolynomialFit(
                        xList,
                        yList,
                        order=order,
                        numPts=constants.PLOT_FIT_NUM_PTS,
                        )
                haveFit = True
        else:
            print("unsupported fitType - we shouldn't be here")

        plt.clf()
        self.fig = plt.figure(constants.PLOT_FIGURE_NUM)
        self.fig.canvas.manager.set_window_title('Colorimeter Plot')
        ax = self.fig.add_subplot(111)

        if haveFit:
            hFit = ax.plot(xFit,yFit,'r')

        ax.plot(xList,yList,'ob')
        ax.grid('on')
        units = self.getUnits()
        if units in ('um', 'ppm'):
            ax.set_xlabel('Concentration ({0})'.format(units))
        else:
            ax.set_xlabel('({0})'.format(units))
        currentLEDText = self.getLEDText()
        ax.set_ylabel('Absorbance ('+currentLEDText+' led)')
        if haveSlope:
            self.fig.text(
                    constants.PLOT_SLOPE_TEXT_POS[0],
                    constants.PLOT_SLOPE_TEXT_POS[1],
                    'slope = {0:1.3f}'.format(slope), 
                    color='r'
                    )
        plt.draw()

    def getMeasurement(self):
        if constants.DEVEL_FAKE_MEASURE:
            absorbance = random.random()
        else:
            modeConfig = self.getModeConfig()
            ledDict = modeConfig['LED'][self.currentLED] 
            dummy0, dummy1, absorbance = self.dev.getMeasurement(ledDict['devColor'])
        digits = self.getSignificantDigits()
        absorbanceStr = '{value:1.{digits}f}'.format(value=absorbance,digits=digits)
        self.measurePushButton.setFlat(False)
        self.tableWidget.addData('',absorbanceStr,selectAndEdit=True)

    def getSaveFileHeader(self):
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S %Z') 
        ledInfoStr = self.getLEDSaveInfoStr()
        headerList = [ 
                '# {0}'.format(timeStr),
                '# Colorimeter Data', 
                '# LED {0}'.format(ledInfoStr),
                '# -----------------------------', 
                ]
        units = self.getUnits()
        if units in ('um','ppm'):
            headerList.append('# Concentration | Absorbance')
        else:
            headerList.append('# PH | Absorbance')

        headerStr = os.linesep.join(headerList)
        return headerStr

    def setTableData(self,dataList):
        dataList = dataListToFloat(dataList)
        self.tableWidget.clean(setup=True)
        digits = self.getSignificantDigits()
        for conc, abso in dataList:
            concStr = str(conc)
            absoStr = '{value:1.{digits}f}'.format(value=abso,digits=digits)
            self.tableWidget.addData(concStr,absoStr)

    def updateWidgetEnabled(self):
        super(PlotMainWindow,self).updateWidgetEnabled()
        if self.dev is None:
            self.ledColorWidget.setEnabled(False)
        else:
            self.calibratePushButton.setEnabled(True)
            self.ledColorWidget.setEnabled(True)

    def getFitTypeAndParams(self):
        if self.actionFitTypeLinear.isChecked():
            fitType = 'linear'
            params = None
        elif self.actionFitTypePolynomial2.isChecked():
            fitType = 'polynomial' 
            params = 2
        elif self.actionFitTypePolynomial3.isChecked():
            fitType = 'polynomial'
            params = 3
        elif self.actionFitTypePolynomial4.isChecked():
            fitType = 'polynomial'
            params = 4
        else:
            fitType = 'polynomial'
            params = 5
        return fitType, params

    def setFitType(self,fitType,fitParams):
        error = False
        self.actionFitTypeLinear.setChecked(False)
        self.actionFitTypePolynomial2.setChecked(False)
        self.actionFitTypePolynomial3.setChecked(False)
        self.actionFitTypePolynomial4.setChecked(False)
        self.actionFitTypePolynomial5.setChecked(False)
        if fitType.lower() == 'linear':
            self.actionFitTypeLinear.setChecked(True)
        elif fitType.lower() == 'polynomial':
            order = fitParams
            order2actionDict = {
                    2: self.actionFitTypePolynomial2,
                    3: self.actionFitTypePolynomial3,
                    4: self.actionFitTypePolynomial4,
                    5: self.actionFitTypePolynomial5,
                    }
            try:
                action = order2actionDict[order]
                action.setChecked(True)
            except KeyError:
                error = True
                errorMsg = 'unsupported polynomial order'
        else:
            error = True
            errorMsg = 'uknown fit type {0}'.format(fitType)

        if error: 
            msgTitle = 'Export Error'
            msgText = 'insufficient data for export w/ linear fit' 
            msgText += ' - must have at least 2 points'
            QtGui.QMessageBox.warning(self,msgTitle, msgText)

    def getUnits(self):
        if self.actionUnitsUM.isChecked():
            return 'uM'
        elif self.actionUnitsPPM.isChecked():
            return 'ppm'
        else:
            return 'pH'

    def setUnits(self,units):
        if  units.lower() == 'um':
            self.actionUnitsUM.setChecked(True)
            self.actionUnitsPPM.setChecked(False)
            self.actionUnitsPH.setChecked(False)
        elif units.lower() == 'ppm':
            self.actionUnitsUM.setChecked(False)
            self.actionUnitsPPM.setChecked(True)
            self.actionUnitsPH.setChecked(False)
        else:
            self.actionUnitsUM.setChecked(False)
            self.actionUnitsPPM.setChecked(False)
            self.actionUnitsPH.setChecked(True)
        self.setUnitStr()

    def setUnitStr(self):
        units = self.getUnits().lower()
        if units == 'um':
            unitStr = QtCore.QString.fromUtf8("Concentration (\xc2\xb5M)")
        elif units == 'ppm':
            unitStr = QtCore.QString('Concentration (ppm)')
        else:
            unitStr = QtCore.QString('(pH)')
        self.tableWidget.setHorizontalHeaderLabels((unitStr,'Absorbance')) 

def dataListToFloat(dataList):
    dataListFloat = []
    for x,y in dataList:
        try:
            x, y = float(x), float(y)
        except ValueError:
            continue
        dataListFloat.append((x,y))
    return dataListFloat

def startPlotMainWindow(app):
    mainWindow = PlotMainWindow()
    mainWindow.main()
    app.exec_()

def startPlotApp():
    app = QtGui.QApplication(sys.argv)
    startPlotMainWindow(app)


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
    startPlotApp()
