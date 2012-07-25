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
        self.pushButton.pressed.connect(self.pushButtonPressed_Callback)
        self.pushButton.clicked.connect(self.pushButtonClicked_Callback)

    def initialize(self,mode):
        self.changed = False
        self.setModal(True)

    def pushButtonPressed_Callback(self):
        print('pushButtonPressed_Callback')

    def pushButtonClicked_Callback(self):
        print('pushButtonClicked_Callback')
        if self.mode == 'edit':
            pass
        else:
            pass

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
        self.pushButton.setText(buttonText)
        self.setWindowTitle(windowTitle)
        self._mode = value

    def edit(self):
        self.mode = 'edit'
        self.run()
        return self.changed

    def importDataList(self):
        self.mode = 'import'
        self.run()
        return []

    def run(self):
        self.show()
        self.exec_()




# -----------------------------------------------------------------------------
if __name__ == '__main__':

    mode = 'edit'
    app = QtGui.QApplication(sys.argv)
    dlg = TestSolutionDialog(mode)
    if 1:
        value = dlg.edit()
    if 0:
        dataList = dlg.importDataList()


    
