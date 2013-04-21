from PyQt4 import QtCore
from PyQt4 import QtGui

from constants import TABLE_MIN_ROW_COUNT
from constants import TABLE_COL_COUNT


class ColorimeterTableWidget(QtGui.QTableWidget):

    def __init__(self,parent=None):
        super(ColorimeterTableWidget,self).__init__(parent=parent)
        self.measIndex = 0
        self.minRowCount = TABLE_MIN_ROW_COUNT
        self.contextMenuEvent = self.ContextMenu_Callback
        self.copyAction = QtGui.QAction(self)
        self.copyAction.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_C)
        self.copyAction.triggered.connect(self.copy_Callback)
        self.addAction(self.copyAction)
        self.deleteAction = QtGui.QAction(self)
        self.deleteAction.setShortcut(QtCore.Qt.Key_Delete)
        self.deleteAction.triggered.connect(self.delete_Callback)
        self.addAction(self.deleteAction)
        self.backspaceAction = QtGui.QAction(self)
        self.backspaceAction.setShortcut(QtCore.Qt.Key_Backspace)
        self.backspaceAction.triggered.connect(self.delete_Callback)
        self.addAction(self.backspaceAction)
        self.itemChanged.connect(self.itemChanged_Callback)

        self.setColumnCount(TABLE_COL_COUNT)
        self.setRowCount(self.minRowCount)
        self.updateFlag = True

    def itemChanged_Callback(self,item):
        if self.updateFlag:
            self.updateFunc()

    def ContextMenu_Callback(self,event):
        """
        Callback function for the table widget context menus. Currently
        handles copy and delete actions.
        """
        menu = QtGui.QMenu(self)
        copyAction = menu.addAction("Copy")
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copyAction:
            self.copy_Callback()
        if action == deleteAction:
            self.delete_Callback()

    def delete_Callback(self):
        """
        Deletes data from the table widget based on the current selection.
        """
        removeList = []
        for i in range(self.rowCount()):
            item0 = self.item(i,0)
            item1 = self.item(i,1)
            if self.isItemSelected(item0):
                if not self.isItemSelected(item1):
                    item0.setText("")
            if self.isItemSelected(item1):
                removeList.append(item1.row())

        for ind in reversed(removeList):
            if self.measIndex > 0:
                self.measIndex-=1
            self.removeRow(ind)

        if self.rowCount() < TABLE_MIN_ROW_COUNT:
            self.setRowCount(TABLE_MIN_ROW_COUNT)
            for row in range(self.measIndex,TABLE_MIN_ROW_COUNT): 
                for col in range(0,TABLE_COL_COUNT): 
                    tableItem = QtGui.QTableWidgetItem() 
                    tableItem.setFlags(QtCore.Qt.NoItemFlags) 
                    self.setItem(row,col,tableItem)

        self.updateFunc()

    def copy_Callback(self): 
        """
        Copies data from the table widget to the clipboard based on the current
        selection.
        """
        selectedList = self.getSelectedList()

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

    def getSelectedList(self):
        """
        Returns list of select items in the table widget. Note, assumes that
        selection mode for the table is ContiguousSelection.
        """
        selectedList = []
        for i in range(self.rowCount()): 
            rowList = []
            for j in range(self.columnCount()):
                item = self.item(i,j)
                if self.isItemSelected(item):
                    rowList.append(str(item.text()))
            selectedList.append(rowList)
        return selectedList

    def clean(self,setup=False,msg=''):
        """
        Removes any existing data from the table widget. If setup is False then
        I dialog request confirmation if presented. 
        """
        if setup:
            reply = QtGui.QMessageBox.Yes
        elif self.haveData():
            reply = QtGui.QMessageBox.question( self, 'Message', msg, 
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        else: 
            return True

        if reply == QtGui.QMessageBox.Yes:
            self.updateFlag = False
            self.setRowCount(TABLE_MIN_ROW_COUNT)
            self.setColumnCount(TABLE_COL_COUNT)
            for row in range(TABLE_MIN_ROW_COUNT+1):
                for col in range(TABLE_COL_COUNT+1):
                    tableItem = QtGui.QTableWidgetItem()
                    tableItem.setFlags(QtCore.Qt.NoItemFlags)
                    self.setItem(row,col,tableItem)
            self.measIndex = 0
            self.updateFlag = True
            return True
        else:
            return False

    def haveData(self):
        return len(self.item(0,1).text())

    def addData(self,item0,item1,selectAndEdit=False):
        """
        Added data to table widget. If selectEdit is set to True then the
        concetration element is selected and opened for editing by the
        user.
        """
        self.updateFlag = False
        rowCount = self.measIndex+1
        if rowCount > self.minRowCount:
            self.setRowCount(rowCount)
        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(item1)
        tableItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        self.setItem(self.measIndex,1,tableItem)

        tableItem = QtGui.QTableWidgetItem()
        tableItem.setText(item0)
        self.setItem(self.measIndex,0,tableItem)
        if selectAndEdit:
            tableItem.setSelected(True)
            self.setCurrentCell(self.measIndex,0)
            self.editItem(self.currentItem()) 
        self.measIndex+=1
        self.updateFlag = True

    def getData(self,noValueInclude=True,noValueSymb=None):
        """
        Get data from table widget. Data is returned as a list as rows
        from the data table.
        """
        dataList = []
        for i in range(self.measIndex):
            item0 = self.item(i,0)
            try:
                value0 = str(item0.text())
            except AttributeError:
                value0 = None
            if not value0: 
                if noValueInclude: 
                    if noValueSymb is None:
                        value0 = '{0}'.format(item0.row()+1)
                    else:
                        value0 = noValueSymb 
                else:
                    continue
            item1 = self.item(i,1)
            if item1 is None:
                continue
            try:
                value1 = str(item1.text())
            except AttributeError:
                continue
            dataList.append((value0,value1))
        return dataList

    def updateFunc(self):
        pass

