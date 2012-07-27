# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_solution_dialog.ui'
#
# Created: Thu Jul 26 17:19:23 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_testSolutionDialog(object):
    def setupUi(self, testSolutionDialog):
        testSolutionDialog.setObjectName("testSolutionDialog")
        testSolutionDialog.resize(263, 169)
        self.verticalLayout = QtGui.QVBoxLayout(testSolutionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtGui.QListWidget(testSolutionDialog)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget = QtGui.QWidget(testSolutionDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(125, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.quitPushButton = QtGui.QPushButton(self.widget)
        self.quitPushButton.setObjectName("quitPushButton")
        self.horizontalLayout.addWidget(self.quitPushButton)
        self.modePushButton = QtGui.QPushButton(self.widget)
        self.modePushButton.setObjectName("modePushButton")
        self.horizontalLayout.addWidget(self.modePushButton)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(testSolutionDialog)
        QtCore.QMetaObject.connectSlotsByName(testSolutionDialog)

    def retranslateUi(self, testSolutionDialog):
        testSolutionDialog.setWindowTitle(QtGui.QApplication.translate("testSolutionDialog", "Test Solution Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.quitPushButton.setText(QtGui.QApplication.translate("testSolutionDialog", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.modePushButton.setText(QtGui.QApplication.translate("testSolutionDialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

