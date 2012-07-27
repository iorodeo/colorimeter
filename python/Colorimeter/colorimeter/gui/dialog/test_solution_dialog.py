from __future__ import print_function
import os
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from test_solution_dialog_ui import Ui_testSolutionDialog

from colorimeter import import_export

class TestSolutionDialog(QtGui.QDialog,Ui_testSolutionDialog):

    def __init__(self, mode='edit', parent=None):
        super(TestSolutionDialog,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.initialize(mode)

    def connectActions(self):
        self.quitPushButton.clicked.connect(
                self.quitPushButtonClicked_Callback
                )
        self.modePushButton.clicked.connect(
                self.modePushButtonClicked_Callback
                )

    def initialize(self,mode):
        self.mode = mode
        self.changed = False
        self.selectedItem = None
        self.setModal(True)
        self.listWidget.setAlternatingRowColors(True)
        self.testSolutionDict = {} 

    def quitPushButtonClicked_Callback(self):
        self.selectedItem = None
        self.testSolutionDict = None
        self.close()

    def modePushButtonClicked_Callback(self):
        if self.listWidget.count() <= 0:
            return;
        listItem = self.listWidget.currentItem()
        if not self.listWidget.isItemSelected(listItem):
            return
        itemName = str(listItem.text())
        self.selectedItem = listItem
        if self.mode == 'edit':
            msg = 'Delete {0}?'.format(itemName)
            reply = QtGui.QMessageBox.question( self, 'Delete', msg, 
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                testSolutionDict = self.testSolutionDict
                fileName = testSolutionDict.pop(itemName)
                os.remove(fileName)
                self.testSolutionDict = testSolutionDict
                self.changed = True
        else:
            self.close()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self,value):
        value = value.lower()
        if value == 'edit':
            buttonText = 'Delete'
            windowTitle = 'Test Solution Editor'
        elif value == 'import':
            buttonText = 'Import'
            windowTitle = 'Test Solution Importer'
        else:
            raise ValueError, 'unknown mode {0}'.format(value)
        self.modePushButton.setText(buttonText)
        self.setWindowTitle(windowTitle)
        self._mode = value

    @property
    def testSolutionDict(self):
        return self._testSolutionDict

    @testSolutionDict.setter
    def testSolutionDict(self,newDict):
        self.listWidget.clear()
        if newDict:
            nameList = sorted(newDict.keys())
            for name in nameList:
                listItem = QtGui.QListWidgetItem()
                listItem.setText(name)
                self.listWidget.addItem(listItem)
            self._testSolutionDict = newDict

    def edit(self,testSolutionDict):
        self.mode = 'edit'
        self.testSolutionDict = testSolutionDict
        self.run()
        return self.changed

    def importData(self,testSolutionDict):
        self.mode = 'import'
        self.testSolutionDict = testSolutionDict
        self.run()
        if self.selectedItem is not None:
            itemName = str(self.selectedItem.text())
            fileName = self.testSolutionDict[itemName] 
            itemData = import_export.importTestSolutionData(fileName) 
            return itemData
        else:
            return None

    def run(self):
        self.show()
        self.exec_()

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    mode = 'edit'
    app = QtGui.QApplication(sys.argv)
    dlg = TestSolutionDialog(mode)

    userHome = os.getenv('USERPROFILE')
    if userHome is None:
        userHome = os.getenv('HOME')
    userSolutionDict = import_export.loadUserTestSolutionDict(userHome)


    if 1:
        value = dlg.edit(userSolutionDict)
    if 0:
        dataList = dlg.importData(userSolutionDict)


    
