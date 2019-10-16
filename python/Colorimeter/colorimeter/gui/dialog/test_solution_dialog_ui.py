# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_solution_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_testSolutionDialog(object):
    def setupUi(self, testSolutionDialog):
        testSolutionDialog.setObjectName("testSolutionDialog")
        testSolutionDialog.resize(263, 169)
        self.verticalLayout = QtWidgets.QVBoxLayout(testSolutionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(testSolutionDialog)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget = QtWidgets.QWidget(testSolutionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(125, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.quitPushButton = QtWidgets.QPushButton(self.widget)
        self.quitPushButton.setObjectName("quitPushButton")
        self.horizontalLayout.addWidget(self.quitPushButton)
        self.modePushButton = QtWidgets.QPushButton(self.widget)
        self.modePushButton.setObjectName("modePushButton")
        self.horizontalLayout.addWidget(self.modePushButton)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(testSolutionDialog)
        QtCore.QMetaObject.connectSlotsByName(testSolutionDialog)

    def retranslateUi(self, testSolutionDialog):
        _translate = QtCore.QCoreApplication.translate
        testSolutionDialog.setWindowTitle(_translate("testSolutionDialog", "Test Solution Editor"))
        self.quitPushButton.setText(_translate("testSolutionDialog", "Quit"))
        self.modePushButton.setText(_translate("testSolutionDialog", "PushButton"))

