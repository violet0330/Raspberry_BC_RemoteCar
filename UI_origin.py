# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_origin.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(462, 506)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frontButton = QtWidgets.QPushButton(Form)
        self.frontButton.setObjectName("frontButton")
        self.gridLayout_2.addWidget(self.frontButton, 0, 2, 1, 1)
        self.leftButton = QtWidgets.QPushButton(Form)
        self.leftButton.setObjectName("leftButton")
        self.gridLayout_2.addWidget(self.leftButton, 1, 0, 1, 1)
        self.stopButton = QtWidgets.QPushButton(Form)
        self.stopButton.setObjectName("stopButton")
        self.gridLayout_2.addWidget(self.stopButton, 1, 2, 1, 1)
        self.rightButton = QtWidgets.QPushButton(Form)
        self.rightButton.setObjectName("rightButton")
        self.gridLayout_2.addWidget(self.rightButton, 1, 4, 1, 1)
        self.backButton = QtWidgets.QPushButton(Form)
        self.backButton.setObjectName("backButton")
        self.gridLayout_2.addWidget(self.backButton, 2, 1, 1, 1)
        self.sprayButton = QtWidgets.QPushButton(Form)
        self.sprayButton.setObjectName("sprayButton")
        self.gridLayout_2.addWidget(self.sprayButton, 2, 3, 1, 1)
        self.gridLayout_2.setColumnMinimumWidth(0, 1)
        self.gridLayout_2.setColumnMinimumWidth(1, 1)
        self.gridLayout_2.setColumnMinimumWidth(2, 1)
        self.gridLayout_2.setColumnMinimumWidth(3, 1)
        self.gridLayout_2.setColumnMinimumWidth(4, 1)
        self.gridLayout_2.setRowMinimumHeight(0, 1)
        self.gridLayout_2.setRowMinimumHeight(1, 1)
        self.gridLayout_2.setRowMinimumHeight(2, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 11)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.left = QtWidgets.QLabel(Form)
        self.left.setAlignment(QtCore.Qt.AlignCenter)
        self.left.setObjectName("left")
        self.gridLayout.addWidget(self.left, 1, 0, 1, 1)
        self.stream = QtWidgets.QLabel(Form)
        self.stream.setAlignment(QtCore.Qt.AlignCenter)
        self.stream.setObjectName("stream")
        self.gridLayout.addWidget(self.stream, 1, 1, 1, 1)
        self.front = QtWidgets.QLabel(Form)
        self.front.setAlignment(QtCore.Qt.AlignCenter)
        self.front.setObjectName("front")
        self.gridLayout.addWidget(self.front, 0, 1, 1, 1)
        self.right = QtWidgets.QLabel(Form)
        self.right.setAlignment(QtCore.Qt.AlignCenter)
        self.right.setObjectName("right")
        self.gridLayout.addWidget(self.right, 1, 2, 1, 1)
        self.back = QtWidgets.QLabel(Form)
        self.back.setAlignment(QtCore.Qt.AlignCenter)
        self.back.setObjectName("back")
        self.gridLayout.addWidget(self.back, 3, 1, 1, 1)
        self.distAvr = QtWidgets.QLabel(Form)
        self.distAvr.setAlignment(QtCore.Qt.AlignCenter)
        self.distAvr.setObjectName("distAvr")
        self.gridLayout.addWidget(self.distAvr, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 15)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 13)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.setRowStretch(0, 10)

        self.retranslateUi(Form)
        self.leftButton.clicked.connect(Form.leftButton_click) # type: ignore
        self.stopButton.clicked.connect(Form.stopButton_click) # type: ignore
        self.rightButton.clicked.connect(Form.rightButton_click) # type: ignore
        self.frontButton.clicked.connect(Form.frontButton_click) # type: ignore
        self.sprayButton.clicked.connect(Form.sprayButton_click) # type: ignore
        self.backButton.clicked.connect(Form.backButton_click) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.frontButton.setText(_translate("Form", "front"))
        self.leftButton.setText(_translate("Form", "left"))
        self.stopButton.setText(_translate("Form", "stop"))
        self.rightButton.setText(_translate("Form", "right"))
        self.backButton.setText(_translate("Form", "back"))
        self.sprayButton.setText(_translate("Form", "spray"))
        self.left.setText(_translate("Form", "×"))
        self.stream.setText(_translate("Form", "stream"))
        self.front.setText(_translate("Form", "×"))
        self.right.setText(_translate("Form", "×"))
        self.back.setText(_translate("Form", "×"))
        self.distAvr.setText(_translate("Form", "100"))
