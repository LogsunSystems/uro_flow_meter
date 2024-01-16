from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QPushButton, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QObject
from PyQt5.QtCore import *
from reportlab.lib.colors import royalblue as rb
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from cryptography.fernet import Fernet
from reportlab.lib.units import inch
from operator import itemgetter
from datetime import date
from os.path import exists
from itertools import *
import serial,serial.tools.list_ports
import paho.mqtt.client as paho
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Logo
import linecache
import os.path
import socket
import time
import json
import csv
import os

###################################### Files & Folders ######################################

PatientData_Folder = r'Patient Data/'
ConfigData_Folder = r'Config/'
ReportData_Folder = r'Report/'
iconsData_Folder = r'icons/'

logoimage_file = 'logo_img.jpeg'
Completelogoimage_file = os.path.join(iconsData_Folder, logoimage_file)

GraphImage_file = 'test.png'
CompletelGraphImage_file = os.path.join(PatientData_Folder, GraphImage_file)

temporaryData_file = 'temporary_data.txt'
CompletetemporaryData_file = os.path.join(PatientData_Folder, temporaryData_file)

temporaryDataNew_file = 'temporary_data_new.txt'
CompletetemporaryDataNew_file = os.path.join(PatientData_Folder, temporaryDataNew_file)

temporaryData_JSONfile = 'temporary_data.json'
CompletetemporaryData_JSONfile = os.path.join(PatientData_Folder, temporaryData_JSONfile)

converted_file = 'converted.csv'
Completeconverted_file = os.path.join(PatientData_Folder, converted_file)

filekey_file = 'filekey.key'
Completefilekey_file = os.path.join(ConfigData_Folder, filekey_file)

filekeybeta_file = 'filekey_beta.key'                           #Might not need Beta
Completefilekeybeta_file = os.path.join(ConfigData_Folder, filekeybeta_file)

preferences_file = 'preferences.txt'
Completepreferences_file = os.path.join(ConfigData_Folder, preferences_file)

preferencesbeta_file = 'preferences_beta.txt'                   #Might not need Beta
Completepreferencesbeta_file = os.path.join(ConfigData_Folder, preferencesbeta_file)

connect_file = 'Connect.txt'
Completeconnect_file = os.path.join(ConfigData_Folder, connect_file)

connectbeta_file = 'Connect_beta.txt'                           #Might not need Beta
Completeconnectbeta_file = os.path.join(ConfigData_Folder, connectbeta_file)

try:
    os.mkdir(PatientData_Folder)
except FileExistsError:
    print("\nPatient Data Folder Exists")

try:
    os.mkdir(ConfigData_Folder)
except FileExistsError:
    print("\nPatient Data Folder Exists")

try:
    os.mkdir(ReportData_Folder)
except FileExistsError:
    print("\nPatient Data Folder Exists")


###################################### START PAGE 1 GUI ######################################

class Ui_PageOne_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 374)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/RNDLogo/icons/Urologist1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}\n"
"QMenuBar {\n"
"    /* sets background of the menu */\n"
"    background-color: rgb(65, 65, 65);\n"
"    color:#FFF;\n"
" }\n"
"\n"
"QMenuBar::item:selected{\n"
"    background-color: rgb(85, 85, 255);\n"
" }\n"
"\n"
"QMenu::item {\n"
"     /* sets background of menu item. set this to something non-transparent             rgb(60, 148, 255);\n"
"         if you want menu color and menu item color to be different  rgb(15, 15, 15) */\n"
"    background-color: rgb(65, 65, 65);\n"
"    color:#FFF;\n"
" }\n"
"\n"
"QMenu::item:selected {\n"
"    /* when user selects item using mouse or keyboard */\n"
"    background-color: rgb(85, 85, 255);\n"
" }\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(370, 10, 41, 311))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame_DeviceStatus = QtWidgets.QFrame(self.centralwidget)
        self.frame_DeviceStatus.setGeometry(QtCore.QRect(250, 50, 91, 61))
        self.frame_DeviceStatus.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(255, 255, 255);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(255, 0, 4);\n"
"}")
        self.frame_DeviceStatus.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_DeviceStatus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_DeviceStatus.setObjectName("frame_DeviceStatus")
        self.frame_ProgramStatus = QtWidgets.QFrame(self.centralwidget)
        self.frame_ProgramStatus.setGeometry(QtCore.QRect(250, 190, 91, 61))
        self.frame_ProgramStatus.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(255, 255, 255);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(255, 0, 4);\n"
"}")
        self.frame_ProgramStatus.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ProgramStatus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ProgramStatus.setObjectName("frame_ProgramStatus")
        self.connect_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.connect_pushButton.setGeometry(QtCore.QRect(530, 30, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.connect_pushButton.setFont(font)
        self.connect_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.connect_pushButton.setObjectName("connect_pushButton")
        self.calibrate_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.calibrate_pushButton.setGeometry(QtCore.QRect(530, 100, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.calibrate_pushButton.setFont(font)
        self.calibrate_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.calibrate_pushButton.setObjectName("calibrate_pushButton")
        self.start_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.start_pushButton.setGeometry(QtCore.QRect(530, 170, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.start_pushButton.setFont(font)
        self.start_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.start_pushButton.setObjectName("start_pushButton")
        self.quit_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.quit_pushButton.setGeometry(QtCore.QRect(530, 240, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.quit_pushButton.setFont(font)
        self.quit_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.quit_pushButton.setObjectName("quit_pushButton")
        self.label_DeviceStatus = QtWidgets.QLabel(self.centralwidget)
        self.label_DeviceStatus.setGeometry(QtCore.QRect(50, 40, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_DeviceStatus.setFont(font)
        self.label_DeviceStatus.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_DeviceStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DeviceStatus.setObjectName("label_DeviceStatus")
        self.label_ProgramStatus = QtWidgets.QLabel(self.centralwidget)
        self.label_ProgramStatus.setGeometry(QtCore.QRect(50, 180, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_ProgramStatus.setFont(font)
        self.label_ProgramStatus.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_ProgramStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ProgramStatus.setObjectName("label_ProgramStatus")
        self.label_DeviceStatus_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_DeviceStatus_2.setGeometry(QtCore.QRect(50, 70, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_DeviceStatus_2.setFont(font)
        self.label_DeviceStatus_2.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_DeviceStatus_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DeviceStatus_2.setObjectName("label_DeviceStatus_2")
        self.label_ProgramStatus_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_ProgramStatus_2.setGeometry(QtCore.QRect(50, 210, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_ProgramStatus_2.setFont(font)
        self.label_ProgramStatus_2.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_ProgramStatus_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ProgramStatus_2.setObjectName("label_ProgramStatus_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuGeneral = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.menuGeneral.setFont(font)
        self.menuGeneral.setObjectName("menuGeneral")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.menuTools.setFont(font)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionGenerate_Report = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionGenerate_Report.setFont(font)
        self.actionGenerate_Report.setObjectName("actionGenerate_Report")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionPreferences.setFont(font)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionSetup = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionSetup.setFont(font)
        self.actionSetup.setObjectName("actionSetup")
        self.actionServer_Credentials = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionServer_Credentials.setFont(font)
        self.actionServer_Credentials.setObjectName("actionServer_Credentials")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionQuit.setFont(font)
        self.actionQuit.setObjectName("actionQuit")
        self.menuGeneral.addAction(self.actionGenerate_Report)
        self.menuGeneral.addAction(self.actionPreferences)
        self.menuGeneral.addAction(self.actionQuit)
        self.menuTools.addAction(self.actionSetup)
        self.menuTools.addAction(self.actionServer_Credentials)
        self.menubar.addAction(self.menuGeneral.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UroflowMeter"))
        self.connect_pushButton.setText(_translate("MainWindow", "Connect"))
        self.calibrate_pushButton.setText(_translate("MainWindow", "Calibrate"))
        self.start_pushButton.setText(_translate("MainWindow", "Start"))
        self.quit_pushButton.setText(_translate("MainWindow", "Exit"))
        self.label_DeviceStatus.setText(_translate("MainWindow", "Device"))
        self.label_ProgramStatus.setText(_translate("MainWindow", "Software"))
        self.label_DeviceStatus_2.setText(_translate("MainWindow", "Status"))
        self.label_ProgramStatus_2.setText(_translate("MainWindow", "Status"))
        self.menuGeneral.setTitle(_translate("MainWindow", "General"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionGenerate_Report.setText(_translate("MainWindow", "Generate Report"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionSetup.setText(_translate("MainWindow", "Setup"))
        self.actionServer_Credentials.setText(_translate("MainWindow", "Server Credentials"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

###################################### END PAGE 1 GUI ######################################

###################################### START PAGE 1 ######################################

        self.start_pushButton.clicked.connect(self.start_click)
        self.actionQuit.triggered.connect(QApplication.instance().quit)
        self.quit_pushButton.clicked.connect(QApplication.instance().quit)
        self.actionServer_Credentials.triggered.connect(self.connect)
        self.actionSetup.triggered.connect(self.setup)
        self.connect_pushButton.clicked.connect(ui4.connect_mqtt)
        self.calibrate_pushButton.clicked.connect(self.calibration)
        self.actionPreferences.triggered.connect(self.preferences)
        self.actionGenerate_Report.triggered.connect(self.report)

    def start_click(self):
        #Start the Device
        msg1 = str('{"Command":"On"}')
        ui4.client.publish("/Device/Command",msg1)
        
        if os.path.exists(CompletetemporaryData_file):
            os.remove(CompletetemporaryData_file)
        else:
            print("\nThe file does not exist")
        
        #MainWindow10.show()
        MainWindow10.hide()
        MainWindow16.show()


    #Preferences Window
    def preferences(checked):
        if MainWindow14.isVisible():
            MainWindow14.close()
        else:
            MainWindow14.show()

    #Server Calibration Window
    def connect(checked):
        if MainWindow5.isVisible():
            MainWindow5.close()
        else:
            MainWindow5.show()

    #Calibration Popup
    def calibration(checked):
        msg1 = str('{"Calibration":"On"}')
        ui4.client.publish("/Device/Command",msg1)

    #Generate report Popup
    def report(checked):
        if MainWindow10.isVisible():
            MainWindow10.hide()
        else:
            MainWindow10.show()
    
    #Login for Setup
    def setup(checked):
        if MainWindow15.isVisible():
            MainWindow15.hide()
        else:
            MainWindow15.show()


###################################### END PAGE 1 ######################################


###################################### START PREFERENCES PAGE GUI ######################################

class Ui_preferences_MainWindow(object):
    def setupUi3(self, prefrences_MainWindow):
        prefrences_MainWindow.setObjectName("prefrences_MainWindow")
        prefrences_MainWindow.resize(777, 496)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        prefrences_MainWindow.setFont(font)
        prefrences_MainWindow.setStyleSheet("QMainWindow{\n"
"    \n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(prefrences_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.save_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.save_pushButton.setGeometry(QtCore.QRect(310, 409, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.save_pushButton.setFont(font)
        self.save_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.save_pushButton.setObjectName("save_pushButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 40, 641, 331))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.clinic_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.clinic_label.setFont(font)
        self.clinic_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.clinic_label.setObjectName("clinic_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.clinic_label)
        self.clinic_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.clinic_lineEdit.setFont(font)
        self.clinic_lineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.clinic_lineEdit.setObjectName("clinic_lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.clinic_lineEdit)
        self.doc_name_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.doc_name_label.setFont(font)
        self.doc_name_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.doc_name_label.setObjectName("doc_name_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.doc_name_label)
        self.doc_name_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.doc_name_lineEdit.setFont(font)
        self.doc_name_lineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.doc_name_lineEdit.setObjectName("doc_name_lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doc_name_lineEdit)
        self.specilist_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.specilist_label.setFont(font)
        self.specilist_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.specilist_label.setObjectName("specilist_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.specilist_label)
        self.specilist_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.specilist_lineEdit.setFont(font)
        self.specilist_lineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.specilist_lineEdit.setObjectName("specilist_lineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.specilist_lineEdit)
        self.clinic_address_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.clinic_address_label.setFont(font)
        self.clinic_address_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.clinic_address_label.setObjectName("clinic_address_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.clinic_address_label)
        self.clinic_address_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.clinic_address_lineEdit.setFont(font)
        self.clinic_address_lineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.clinic_address_lineEdit.setObjectName("clinic_address_lineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.clinic_address_lineEdit)
        self.mobile_no_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.mobile_no_label.setFont(font)
        self.mobile_no_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.mobile_no_label.setObjectName("mobile_no_label")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.mobile_no_label)
        self.mobile_no_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.mobile_no_lineEdit.setFont(font)
        self.mobile_no_lineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.mobile_no_lineEdit.setObjectName("mobile_no_lineEdit")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.mobile_no_lineEdit)
        self.doc_email_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.doc_email_label.setFont(font)
        self.doc_email_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.doc_email_label.setObjectName("doc_email_label")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.doc_email_label)
        self.doc_email_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.doc_email_lineEdit.setFont(font)
        self.doc_email_lineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.doc_email_lineEdit.setObjectName("doc_email_lineEdit")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.doc_email_lineEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(7, QtWidgets.QFormLayout.LabelRole, spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(9, QtWidgets.QFormLayout.LabelRole, spacerItem4)
        prefrences_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(prefrences_MainWindow)
        self.statusbar.setObjectName("statusbar")
        prefrences_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(prefrences_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(prefrences_MainWindow)

    def retranslateUi(self, prefrences_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        prefrences_MainWindow.setWindowTitle(_translate("prefrences_MainWindow", "Preferences"))
        appIcon = QIcon("icons/preference.png")
        prefrences_MainWindow.setWindowIcon(appIcon)
        self.save_pushButton.setText(_translate("prefrences_MainWindow", "SAVE"))
        self.clinic_label.setText(_translate("prefrences_MainWindow", "Clinic"))
        self.doc_name_label.setText(_translate("prefrences_MainWindow", "Doctor Name"))
        self.specilist_label.setText(_translate("prefrences_MainWindow", "Specilist"))
        self.clinic_address_label.setText(_translate("prefrences_MainWindow", "Address"))
        self.mobile_no_label.setText(_translate("prefrences_MainWindow", "Mobile No."))
        self.doc_email_label.setText(_translate("prefrences_MainWindow", "Email"))

###################################### END PREFERENCES PAGE GUI ######################################

###################################### START PREFERENCES PAGE ######################################

        self.save_pushButton.clicked.connect(self.save)

        PrefBetaExists = os.path.exists(Completepreferencesbeta_file)
        if(PrefBetaExists):
            with open(Completefilekeybeta_file,'r') as filekey:
                key = filekey.readline()

            fernet = Fernet(key)
            with open (Completepreferencesbeta_file, 'rb') as file:
                # Read Encrypted data
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            # write original file
            with open (Completepreferencesbeta_file, 'wb') as file:
                file.write(decrypted_data)
        

            with open(Completepreferencesbeta_file,'r') as f, open (Completepreferences_file, 'w') as outfile:
                for i in f.readlines():
                    if not i.strip():
                        continue
                    if i:
                        outfile.write(i)

            self.line1 = linecache.getline(r"Config/preferences.txt", 1)
            self.line2 = linecache.getline(r"Config/preferences.txt", 2)
            self.line3 = linecache.getline(r"Config/preferences.txt", 3)
            self.line4 = linecache.getline(r"Config/preferences.txt", 4)
            self.line5 = linecache.getline(r"Config/preferences.txt", 5)
            self.line6 = linecache.getline(r"Config/preferences.txt", 6)
            self.clinic_lineEdit.setText(self.line1)
            self.doc_name_lineEdit.setText(self.line2)
            self.specilist_lineEdit.setText(self.line3)
            self.clinic_address_lineEdit.setText(self.line4)
            self.mobile_no_lineEdit.setText(self.line5)
            self.doc_email_lineEdit.setText(self.line6)

            key = Fernet.generate_key()

            # string the key in a file
            with open(Completefilekey_file, 'wb') as filekey:
                filekey.write(key)

            fernet = Fernet(key)
  
            # opening the original file to encrypt
            with open(Completepreferences_file, 'rb') as file:
                original = file.read()
      
            # encrypting the file
            encrypted = fernet.encrypt(original)
  
            # opening the file in write mode and 
            # writing the encrypted data
            with open(Completepreferences_file, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)


            # string the key in a file
            with open(Completefilekeybeta_file, 'wb') as filekey:
                filekey.write(key)

            fernet = Fernet(key)
  
            # opening the original file to encrypt
            with open(Completepreferencesbeta_file, 'rb') as file:
                original = file.read()
      
            # encrypting the file
            encrypted = fernet.encrypt(original)
  
            # opening the file in write mode and 
            # writing the encrypted data
            with open(Completepreferencesbeta_file, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

        else:
            print("\nNeed to create preferences")                         #Delete this please


    def save(self):
        stringData1 = self.clinic_lineEdit.text()
        stringData2 = self.doc_name_lineEdit.text()
        stringData3 = self.specilist_lineEdit.text()
        stringData4 = self.clinic_address_lineEdit.text()
        intData1 = self.mobile_no_lineEdit.text()
        stringData5 = self.doc_email_lineEdit.text()


        f = open(Completepreferencesbeta_file, "w")
        #f= open('preferences_beta.txt','w+')     #Giving '+' helps, or else no file extension
        f.write(stringData1)
        f.write('\n')
        f.write(stringData2)
        f.write('\n')
        f.write(stringData3)
        f.write('\n')
        f.write(stringData4)
        f.write('\n')
        f.write(intData1)
        f.write('\n')
        f.write(stringData5)
        f.write('\n')
        f.close()

        key = Fernet.generate_key()

                # save the key in a file
        with open (Completefilekeybeta_file, 'wb') as filekey:
            filekey.write(key)
        
        fernet = Fernet(key)

            # opening the original file to encrypt
        with open(Completepreferencesbeta_file, 'rb') as file:
            original = file.read()
      
            # encrypting the file
        encrypted = fernet.encrypt(original)
  
            # opening the file in write mode and 
            # writing the encrypted data
        with open(Completepreferencesbeta_file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)


        if MainWindow7.isVisible():
            MainWindow7.close()
        else:
            MainWindow7.show()


###################################### END PAGE PREFERENCES ######################################

###################################### START PAGE PREFERENCE POPUP GUI ######################################

class Ui_prefrences_popup_MainWindow(object):
    def setupUi6(self, prefrences_popup_MainWindow):
        prefrences_popup_MainWindow.setObjectName("prefrences_popup_MainWindow")
        prefrences_popup_MainWindow.resize(477, 202)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        prefrences_popup_MainWindow.setFont(font)
        prefrences_popup_MainWindow.setAcceptDrops(False)
        prefrences_popup_MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(prefrences_popup_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 30, 351, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.ok_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.ok_pushButton.setGeometry(QtCore.QRect(180, 120, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.ok_pushButton.setFont(font)
        self.ok_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.ok_pushButton.setObjectName("ok_pushButton")
        prefrences_popup_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(prefrences_popup_MainWindow)
        self.statusbar.setObjectName("statusbar")
        prefrences_popup_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(prefrences_popup_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(prefrences_popup_MainWindow)

    def retranslateUi(self, prefrences_popup_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        prefrences_popup_MainWindow.setWindowTitle(_translate("prefrences_popup_MainWindow", "Notification"))
        appIcon = QIcon("icons/check.png")
        prefrences_popup_MainWindow.setWindowIcon(appIcon)
        self.label.setText(_translate("prefrences_popup_MainWindow", "Data Saved Successfully"))
        self.ok_pushButton.setText(_translate("prefrences_popup_MainWindow", "OK"))

###################################### STOP PAGE PREFERENCE POPUP GUI ######################################

###################################### START PAGE PREFERENCE POPUP ######################################

        self.ok_pushButton.clicked.connect(self.ok)
    
    #Prefrences Saved
    def ok(checked):
        if MainWindow7.isVisible():
            MainWindow7.close()
            MainWindow4.close()
        else:
            MainWindow7.show()

###################################### STOP PAGE PREFERENCE POPUP ######################################

###################################### START PAGE DUMMY PREFERENCES GUI ######################################

class Ui_dummy_prefrences_MainWindow(object):
    def setupUi14(self, dummy_prefrences_MainWindow):
        dummy_prefrences_MainWindow.setObjectName("dummy_prefrences_MainWindow")
        dummy_prefrences_MainWindow.resize(788, 668)
        dummy_prefrences_MainWindow.setStyleSheet("QMainWindow{\n"
"    \n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(dummy_prefrences_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ok_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.ok_pushButton.setGeometry(QtCore.QRect(320, 530, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ok_pushButton.setFont(font)
        self.ok_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.doc_name_label = QtWidgets.QLabel(self.centralwidget)
        self.doc_name_label.setGeometry(QtCore.QRect(150, 130, 149, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.doc_name_label.setFont(font)
        self.doc_name_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.doc_name_label.setObjectName("doc_name_label")
        self.clinic_label = QtWidgets.QLabel(self.centralwidget)
        self.clinic_label.setGeometry(QtCore.QRect(150, 46, 63, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.clinic_label.setFont(font)
        self.clinic_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.clinic_label.setObjectName("clinic_label")
        self.clinic_address_label = QtWidgets.QLabel(self.centralwidget)
        self.clinic_address_label.setGeometry(QtCore.QRect(150, 299, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.clinic_address_label.setFont(font)
        self.clinic_address_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.clinic_address_label.setObjectName("clinic_address_label")
        self.specilist_label = QtWidgets.QLabel(self.centralwidget)
        self.specilist_label.setGeometry(QtCore.QRect(150, 214, 96, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.specilist_label.setFont(font)
        self.specilist_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.specilist_label.setObjectName("specilist_label")
        self.doc_email_label = QtWidgets.QLabel(self.centralwidget)
        self.doc_email_label.setGeometry(QtCore.QRect(150, 467, 65, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.doc_email_label.setFont(font)
        self.doc_email_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.doc_email_label.setObjectName("doc_email_label")
        self.mobile_no_label = QtWidgets.QLabel(self.centralwidget)
        self.mobile_no_label.setGeometry(QtCore.QRect(150, 383, 121, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.mobile_no_label.setFont(font)
        self.mobile_no_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.mobile_no_label.setObjectName("mobile_no_label")
        self.specilist_print_label = QtWidgets.QLabel(self.centralwidget)
        self.specilist_print_label.setGeometry(QtCore.QRect(300, 200, 391, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.specilist_print_label.setFont(font)
        self.specilist_print_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.specilist_print_label.setAlignment(QtCore.Qt.AlignCenter)
        self.specilist_print_label.setObjectName("specilist_print_label")
        self.doc_name_print_label = QtWidgets.QLabel(self.centralwidget)
        self.doc_name_print_label.setGeometry(QtCore.QRect(300, 120, 401, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.doc_name_print_label.setFont(font)
        self.doc_name_print_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.doc_name_print_label.setAlignment(QtCore.Qt.AlignCenter)
        self.doc_name_print_label.setObjectName("doc_name_print_label")
        self.mobile_no_print_label = QtWidgets.QLabel(self.centralwidget)
        self.mobile_no_print_label.setGeometry(QtCore.QRect(305, 360, 401, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.mobile_no_print_label.setFont(font)
        self.mobile_no_print_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.mobile_no_print_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mobile_no_print_label.setObjectName("mobile_no_print_label")
        self.clinic_address_print_label = QtWidgets.QLabel(self.centralwidget)
        self.clinic_address_print_label.setGeometry(QtCore.QRect(305, 276, 401, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.clinic_address_print_label.setFont(font)
        self.clinic_address_print_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.clinic_address_print_label.setAlignment(QtCore.Qt.AlignCenter)
        self.clinic_address_print_label.setObjectName("clinic_address_print_label")
        self.clinic_print_label = QtWidgets.QLabel(self.centralwidget)
        self.clinic_print_label.setGeometry(QtCore.QRect(300, 40, 401, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.clinic_print_label.setFont(font)
        self.clinic_print_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.clinic_print_label.setAlignment(QtCore.Qt.AlignCenter)
        self.clinic_print_label.setObjectName("clinic_print_label")
        self.doc_email_print_label = QtWidgets.QLabel(self.centralwidget)
        self.doc_email_print_label.setGeometry(QtCore.QRect(290, 460, 421, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.doc_email_print_label.setFont(font)
        self.doc_email_print_label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.doc_email_print_label.setAlignment(QtCore.Qt.AlignCenter)
        self.doc_email_print_label.setObjectName("doc_email_print_label")
        dummy_prefrences_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(dummy_prefrences_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 788, 26))
        self.menubar.setObjectName("menubar")
        dummy_prefrences_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(dummy_prefrences_MainWindow)
        self.statusbar.setObjectName("statusbar")
        dummy_prefrences_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(dummy_prefrences_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(dummy_prefrences_MainWindow)

    def retranslateUi(self, dummy_prefrences_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        dummy_prefrences_MainWindow.setWindowTitle(_translate("dummy_prefrences_MainWindow", "MainWindow"))
        appIcon = QIcon("icons/preference.png")
        dummy_prefrences_MainWindow.setWindowIcon(appIcon)
        self.ok_pushButton.setText(_translate("dummy_prefrences_MainWindow", "OK"))
        self.doc_name_label.setText(_translate("dummy_prefrences_MainWindow", "Doctor Name"))
        self.clinic_label.setText(_translate("dummy_prefrences_MainWindow", "Clinic"))
        self.clinic_address_label.setText(_translate("dummy_prefrences_MainWindow", "Address"))
        self.specilist_label.setText(_translate("dummy_prefrences_MainWindow", "Specilist"))
        self.doc_email_label.setText(_translate("dummy_prefrences_MainWindow", "Email"))
        self.mobile_no_label.setText(_translate("dummy_prefrences_MainWindow", "Mobile No."))
        self.specilist_print_label.setText(_translate("dummy_prefrences_MainWindow", "Specilist Type"))
        self.doc_name_print_label.setText(_translate("dummy_prefrences_MainWindow", "Doctor Name"))
        self.mobile_no_print_label.setText(_translate("dummy_prefrences_MainWindow", "Number"))
        self.clinic_address_print_label.setText(_translate("dummy_prefrences_MainWindow", "Address Fill"))
        self.clinic_print_label.setText(_translate("dummy_prefrences_MainWindow", "Clinic Name"))
        self.doc_email_print_label.setText(_translate("dummy_prefrences_MainWindow", "name@example.com"))

###################################### END PAGE DUMMY PREFERENCES GUI ######################################


###################################### START PAGE DUMMY PREFERENCES ######################################

        self.ok_pushButton.clicked.connect(self.ok)

        prefExist = os.path.exists(Completepreferences_file)
        prefBetaExist = os.path.exists(Completepreferencesbeta_file)

        if (prefExist):
            with open(Completefilekey_file, 'r') as filekey:
                key = filekey.readline()
            
            fernet = Fernet(key)


            with open(Completepreferences_file,'rb') as file:
                encrypted_data = file.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)

            with open(Completepreferences_file, "wb") as file:
                file.write(decrypted_data)

            with open(Completepreferences_file,"r") as file:
                self.line1 = linecache.getline(r"Config/preferences.txt", 1)
                self.line2 = linecache.getline(r"Config/preferences.txt", 2)
                self.line3 = linecache.getline(r"Config/preferences.txt", 3)
                self.line4 = linecache.getline(r"Config/preferences.txt", 4)
                self.line5 = linecache.getline(r"Config/preferences.txt", 5)
                self.line6 = linecache.getline(r"Config/preferences.txt", 6)

                self.clinic_print_label.setText(_translate("dummy_prefrences_MainWindow", str(self.line1)))
                self.doc_name_print_label.setText(_translate("dummy_prefrences_MainWindow", str(self.line2)))
                self.specilist_print_label.setText(_translate("dummy_prefrences_MainWindow", str(self.line3)))
                self.clinic_address_print_label.setText(_translate("dummy_prefrences_MainWindow", str(self.line4)))
                self.mobile_no_print_label.setText(_translate("dummy_prefrences_MainWindow", str(self.line5)))
                self.doc_email_print_label.setText(_translate("dummy_prefrences_MainWindow", str(self.line6)))

            key = Fernet.generate_key()

            # string the key in a file
            with open(Completefilekey_file, 'wb') as filekey:
                filekey.write(key)

            fernet = Fernet(key)
  
            # opening the original file to encrypt
            with open(Completepreferences_file, 'rb') as file:
                original = file.read()
      
            # encrypting the file
            encrypted = fernet.encrypt(original)
  
            # opening the file in write mode and 
            # writing the encrypted data
            with open(Completepreferences_file, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

        elif(prefExist):
            if(prefBetaExist):
                print("\nBoth exist")
            else:
                print("\nto be encrypted")
        else:
            if MainWindow15.isVisible():
                MainWindow15.close()
            else:
                MainWindow15.show()

    def ok(checked):
        if MainWindow14.isVisible():
            MainWindow14.close()
        else:
            MainWindow14.show()


###################################### END PAGE DUMMY PREFERENCES ######################################


###################################### START PAGE SETUP GUI ######################################

class Ui_setup_MainWindow(object):
    def setupUi15(self, setup_MainWindow):
        setup_MainWindow.setObjectName("setup_MainWindow")
        setup_MainWindow.resize(653, 409)
        font = QtGui.QFont()
        font.setPointSize(15)
        setup_MainWindow.setFont(font)
        setup_MainWindow.setStyleSheet("QMainWindow{    \n"
"    background-color: rgb(35, 35, 35);\n"
"}\n"
"\n"
"QMenuBar {\n"
"    /* sets background of the menu */\n"
"    background-color: rgb(65, 65, 65);\n"
"    color:#FFF;\n"
" }\n"
"\n"
"QMenuBar::item:selected{\n"
"    background-color: rgb(85, 85, 255);\n"
" }\n"
"\n"
"QMenu::item {\n"
"     /* sets background of menu item. set this to something non-transparent             rgb(60, 148, 255);\n"
"         if you want menu color and menu item color to be different  rgb(15, 15, 15) */\n"
"    background-color: rgb(65, 65, 65);\n"
"    color:#FFF;\n"
" }\n"
"\n"
"QMenu::item:selected {\n"
"    /* when user selects item using mouse or keyboard */\n"
"    background-color: rgb(85, 85, 255);\n"
" }")
        self.centralwidget = QtWidgets.QWidget(setup_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 40, 501, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(120, 130, 421, 111))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.login_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.login_pushButton.setGeometry(QtCore.QRect(110, 270, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_pushButton.setFont(font)
        self.login_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.login_pushButton.setObjectName("login_pushButton")
        self.leave_pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.leave_pushButton_2.setGeometry(QtCore.QRect(380, 270, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.leave_pushButton_2.setFont(font)
        self.leave_pushButton_2.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.leave_pushButton_2.setObjectName("leave_pushButton_2")
        setup_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(setup_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 653, 26))
        self.menubar.setObjectName("menubar")
        setup_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(setup_MainWindow)
        self.statusbar.setObjectName("statusbar")
        setup_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(setup_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(setup_MainWindow)

    def retranslateUi(self, setup_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        setup_MainWindow.setWindowTitle(_translate("setup_MainWindow", "Setup Login"))
        appIcon = QIcon("icons/login.png")
        setup_MainWindow.setWindowIcon(appIcon)
        self.label_3.setText(_translate("setup_MainWindow", "Please login first to change Prefrences"))
        self.label.setText(_translate("setup_MainWindow", "Username"))
        self.lineEdit.setPlaceholderText(_translate("setup_MainWindow", "Username"))
        self.label_2.setText(_translate("setup_MainWindow", "Password"))
        self.lineEdit_2.setPlaceholderText(_translate("setup_MainWindow", "Password"))
        self.login_pushButton.setText(_translate("setup_MainWindow", "LogIn"))
        self.leave_pushButton_2.setText(_translate("setup_MainWindow", "Leave"))

###################################### END PAGE SETUP GUI ######################################

###################################### START PAGE SETUP ######################################

        self.login_pushButton.clicked.connect(self.login)
        self.leave_pushButton_2.clicked.connect(self.leave)

        self.confirm = "RNDTECH"
        self.passconfirm = "hcetdnr"
    
    #Check  password
    def login(self):
        self.stringData1 = self.lineEdit.text()                 #Username
        self.stringData2 = self.lineEdit_2.text()               #Password
        self.stringData1.strip()
        self.stringData2.strip()

        if (self.confirm == self.stringData1):
            if (self.passconfirm == self.stringData2):
                
                #Open Prefrences (Edit)
                if MainWindow4.isVisible():
                    MainWindow4.close()
                else:
                    MainWindow4.show()
            else:
                print("\nWrong password")
        else:
            print("\nWrong Username")
    
    #Close Login page
    def leave(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit.setPlaceholderText('Username')
        self.lineEdit_2.setPlaceholderText('Password')
        if MainWindow15.isVisible():
            MainWindow15.close()
        else:
            MainWindow15.show()


###################################### END PAGE SETUP ######################################


###################################### START CALIBRATE POPUP PAGE ######################################

class Ui_Calibrate_popup_MainWindow(object):
    def setupUi5(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(437, 202)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Calibration/icons/calibrate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 30, 291, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButtonOK = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonOK.setGeometry(QtCore.QRect(160, 110, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.pushButtonOK.setFont(font)
        self.pushButtonOK.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.pushButtonOK.setObjectName("pushButtonOK")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 437, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Calibration Successful!!"))
        self.pushButtonOK.setText(_translate("MainWindow", "OK"))

###################################### END CALIBRATE POPUP PAGE ######################################

###################################### START CALIBRATE POPUP PAGE MAIN ######################################


        self.pushButtonOK.clicked.connect(self.OK)

    def OK (self):
        if MainWindow6.isVisible():
            MainWindow6.hide()
        else:
            MainWindow6.show()


###################################### END CALIBRATE POPUP PAGE MAIN ######################################


###################################### START PAGE CON_DISSCON GUI ######################################

class Ui_server_credentials_MainWindow(object):
    def setupUi4(self, server_credentials_MainWindow):
        server_credentials_MainWindow.setObjectName("server_credentials_MainWindow")
        server_credentials_MainWindow.resize(816, 755)
        font = QtGui.QFont()
        font.setFamily("Arial")
        server_credentials_MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ServerCredentials/icons/connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        server_credentials_MainWindow.setWindowIcon(icon)
        server_credentials_MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(server_credentials_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Device_setup_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Device_setup_pushButton.setGeometry(QtCore.QRect(310, 650, 181, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Device_setup_pushButton.sizePolicy().hasHeightForWidth())
        self.Device_setup_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Device_setup_pushButton.setFont(font)
        self.Device_setup_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.Device_setup_pushButton.setObjectName("Device_setup_pushButton")
        self.PasswordWiFilabel = QtWidgets.QLabel(self.centralwidget)
        self.PasswordWiFilabel.setGeometry(QtCore.QRect(390, 270, 121, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PasswordWiFilabel.sizePolicy().hasHeightForWidth())
        self.PasswordWiFilabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.PasswordWiFilabel.setFont(font)
        self.PasswordWiFilabel.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.PasswordWiFilabel.setObjectName("PasswordWiFilabel")
        self.WiFi_setup_label = QtWidgets.QLabel(self.centralwidget)
        self.WiFi_setup_label.setGeometry(QtCore.QRect(330, 200, 161, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WiFi_setup_label.sizePolicy().hasHeightForWidth())
        self.WiFi_setup_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.WiFi_setup_label.setFont(font)
        self.WiFi_setup_label.setStyleSheet("background-color: none;\n"
"color: rgb(6, 103, 229);")
        self.WiFi_setup_label.setAlignment(QtCore.Qt.AlignCenter)
        self.WiFi_setup_label.setObjectName("WiFi_setup_label")
        self.MQTTusernamelabel = QtWidgets.QLabel(self.centralwidget)
        self.MQTTusernamelabel.setGeometry(QtCore.QRect(490, 480, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MQTTusernamelabel.sizePolicy().hasHeightForWidth())
        self.MQTTusernamelabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.MQTTusernamelabel.setFont(font)
        self.MQTTusernamelabel.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.MQTTusernamelabel.setObjectName("MQTTusernamelabel")
        self.UpdatepushButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdatepushButton.setGeometry(QtCore.QRect(460, 90, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UpdatepushButton.sizePolicy().hasHeightForWidth())
        self.UpdatepushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.UpdatepushButton.setFont(font)
        self.UpdatepushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.UpdatepushButton.setObjectName("UpdatepushButton")
        self.MQTTusernamelabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.MQTTusernamelabel_2.setGeometry(QtCore.QRect(610, 480, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MQTTusernamelabel_2.sizePolicy().hasHeightForWidth())
        self.MQTTusernamelabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.MQTTusernamelabel_2.setFont(font)
        self.MQTTusernamelabel_2.setStyleSheet("background-color: rgb(45, 45, 45);\n"
"color: #FFF;")
        self.MQTTusernamelabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.MQTTusernamelabel_2.setObjectName("MQTTusernamelabel_2")
        self.USBPortlabel = QtWidgets.QLabel(self.centralwidget)
        self.USBPortlabel.setGeometry(QtCore.QRect(30, 90, 121, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.USBPortlabel.sizePolicy().hasHeightForWidth())
        self.USBPortlabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.USBPortlabel.setFont(font)
        self.USBPortlabel.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.USBPortlabel.setObjectName("USBPortlabel")
        self.MQTTPortlabel = QtWidgets.QLabel(self.centralwidget)
        self.MQTTPortlabel.setGeometry(QtCore.QRect(310, 560, 81, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MQTTPortlabel.sizePolicy().hasHeightForWidth())
        self.MQTTPortlabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.MQTTPortlabel.setFont(font)
        self.MQTTPortlabel.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.MQTTPortlabel.setObjectName("MQTTPortlabel")
        self.USB_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.USB_comboBox.setGeometry(QtCore.QRect(140, 90, 241, 38))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.USB_comboBox.setFont(font)
        self.USB_comboBox.setStyleSheet("QComboBox{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 1px;\n"
"     border-left-color: rgb(54, 54, 54);\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 2px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 2px;\n"
" }\n"
"\n"
"QComboBox:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 2px solid rgb(74, 74, 74);\n"
"    selection-background-color: rgb(6, 103, 229);\n"
"    background-color: rgb(54, 54, 54);\n"
"    color:#FFF\n"
" }\n"
"\n"
"QComboBox:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.USB_comboBox.setObjectName("USB_comboBox")
        self.USB_comboBox.addItem("")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(40, 170, 741, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.line.setFont(font)
        self.line.setStyleSheet("Line{\n"
"    background-color: rgb(35, 35, 35);\n"
"    color:rgb(255, 255, 255)\n"
"}")
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.Serial_setup_label = QtWidgets.QLabel(self.centralwidget)
        self.Serial_setup_label.setGeometry(QtCore.QRect(330, 30, 161, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Serial_setup_label.sizePolicy().hasHeightForWidth())
        self.Serial_setup_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.Serial_setup_label.setFont(font)
        self.Serial_setup_label.setStyleSheet("background-color: none;\n"
"color: rgb(6, 103, 229);")
        self.Serial_setup_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Serial_setup_label.setObjectName("Serial_setup_label")
        self.CancelpushButton = QtWidgets.QPushButton(self.centralwidget)
        self.CancelpushButton.setGeometry(QtCore.QRect(550, 650, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CancelpushButton.sizePolicy().hasHeightForWidth())
        self.CancelpushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.CancelpushButton.setFont(font)
        self.CancelpushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.CancelpushButton.setObjectName("CancelpushButton")
        self.waringlabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.waringlabel_2.setGeometry(QtCore.QRect(470, 310, 241, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waringlabel_2.sizePolicy().hasHeightForWidth())
        self.waringlabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setItalic(True)
        self.waringlabel_2.setFont(font)
        self.waringlabel_2.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.waringlabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.waringlabel_2.setObjectName("waringlabel_2")
        self.PasswordWiFilineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordWiFilineEdit.setGeometry(QtCore.QRect(500, 270, 181, 38))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PasswordWiFilineEdit.sizePolicy().hasHeightForWidth())
        self.PasswordWiFilineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.PasswordWiFilineEdit.setFont(font)
        self.PasswordWiFilineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.PasswordWiFilineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordWiFilineEdit.setObjectName("PasswordWiFilineEdit")
        self.SavepushButton = QtWidgets.QPushButton(self.centralwidget)
        self.SavepushButton.setGeometry(QtCore.QRect(140, 650, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SavepushButton.sizePolicy().hasHeightForWidth())
        self.SavepushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.SavepushButton.setFont(font)
        self.SavepushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.SavepushButton.setObjectName("SavepushButton")
        self.waringlabel = QtWidgets.QLabel(self.centralwidget)
        self.waringlabel.setGeometry(QtCore.QRect(70, 310, 241, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waringlabel.sizePolicy().hasHeightForWidth())
        self.waringlabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setItalic(True)
        self.waringlabel.setFont(font)
        self.waringlabel.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.waringlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.waringlabel.setObjectName("waringlabel")
        self.MQTT_setup_label = QtWidgets.QLabel(self.centralwidget)
        self.MQTT_setup_label.setGeometry(QtCore.QRect(340, 420, 161, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MQTT_setup_label.sizePolicy().hasHeightForWidth())
        self.MQTT_setup_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.MQTT_setup_label.setFont(font)
        self.MQTT_setup_label.setStyleSheet("background-color: none;\n"
"color: rgb(6, 103, 229);")
        self.MQTT_setup_label.setAlignment(QtCore.Qt.AlignCenter)
        self.MQTT_setup_label.setObjectName("MQTT_setup_label")
        self.SSIDWiFilabel = QtWidgets.QLabel(self.centralwidget)
        self.SSIDWiFilabel.setGeometry(QtCore.QRect(40, 270, 91, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SSIDWiFilabel.sizePolicy().hasHeightForWidth())
        self.SSIDWiFilabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.SSIDWiFilabel.setFont(font)
        self.SSIDWiFilabel.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.SSIDWiFilabel.setObjectName("SSIDWiFilabel")
        self.ConnectpushButton = QtWidgets.QPushButton(self.centralwidget)
        self.ConnectpushButton.setGeometry(QtCore.QRect(640, 90, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConnectpushButton.sizePolicy().hasHeightForWidth())
        self.ConnectpushButton.setSizePolicy(sizePolicy)
        self.ConnectpushButton.setCheckable(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.ConnectpushButton.setFont(font)
        self.ConnectpushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.ConnectpushButton.setObjectName("ConnectpushButton")
        self.MQTTIPlabel = QtWidgets.QLabel(self.centralwidget)
        self.MQTTIPlabel.setGeometry(QtCore.QRect(60, 480, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MQTTIPlabel.sizePolicy().hasHeightForWidth())
        self.MQTTIPlabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.MQTTIPlabel.setFont(font)
        self.MQTTIPlabel.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.MQTTIPlabel.setObjectName("MQTTIPlabel")
        self.MQTTPortlabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.MQTTPortlabel_2.setGeometry(QtCore.QRect(380, 560, 111, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MQTTPortlabel_2.sizePolicy().hasHeightForWidth())
        self.MQTTPortlabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.MQTTPortlabel_2.setFont(font)
        self.MQTTPortlabel_2.setStyleSheet("background-color: rgb(45, 45, 45);\n"
"color: #FFF;")
        self.MQTTPortlabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.MQTTPortlabel_2.setObjectName("MQTTPortlabel_2")
        self.SSIDWiFilineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.SSIDWiFilineEdit.setGeometry(QtCore.QRect(110, 270, 181, 38))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SSIDWiFilineEdit.sizePolicy().hasHeightForWidth())
        self.SSIDWiFilineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.SSIDWiFilineEdit.setFont(font)
        self.SSIDWiFilineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.SSIDWiFilineEdit.setObjectName("SSIDWiFilineEdit")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(40, 390, 741, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.line_2.setFont(font)
        self.line_2.setStyleSheet("Line{\n"
"    background-color: rgb(35, 35, 35);\n"
"    color:rgb(255, 255, 255)\n"
"}")
        self.line_2.setMidLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.MQTTIPlineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.MQTTIPlineEdit.setGeometry(QtCore.QRect(180, 480, 181, 38))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MQTTIPlineEdit.sizePolicy().hasHeightForWidth())
        self.MQTTIPlineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.MQTTIPlineEdit.setFont(font)
        self.MQTTIPlineEdit.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.MQTTIPlineEdit.setObjectName("MQTTIPlineEdit")
        server_credentials_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(server_credentials_MainWindow)
        self.statusbar.setObjectName("statusbar")
        server_credentials_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(server_credentials_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(server_credentials_MainWindow)

    def retranslateUi(self, server_credentials_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        appIcon = QIcon("icons/connect.png")
        server_credentials_MainWindow.setWindowIcon(appIcon)
        server_credentials_MainWindow.setWindowTitle(_translate("server_credentials_MainWindow", "MainWindow"))
        self.Device_setup_pushButton.setText(_translate("server_credentials_MainWindow", "Device Setup"))
        self.PasswordWiFilabel.setText(_translate("server_credentials_MainWindow", "Password *"))
        self.WiFi_setup_label.setText(_translate("server_credentials_MainWindow", "WiFi Setup"))
        self.MQTTusernamelabel.setText(_translate("server_credentials_MainWindow", "Username:"))
        self.UpdatepushButton.setText(_translate("server_credentials_MainWindow", "Update"))
        self.MQTTusernamelabel_2.setText(_translate("server_credentials_MainWindow", "RNDTECH"))
        self.USBPortlabel.setText(_translate("server_credentials_MainWindow", "USB Port:"))
        self.MQTTPortlabel.setText(_translate("server_credentials_MainWindow", "Port:"))
        self.USB_comboBox.setItemText(0, _translate("server_credentials_MainWindow", "SERIAL"))
        self.Serial_setup_label.setText(_translate("server_credentials_MainWindow", "Serial Setup"))
        self.CancelpushButton.setText(_translate("server_credentials_MainWindow", "Cancel"))
        self.waringlabel_2.setText(_translate("server_credentials_MainWindow", "*Max 14 Characters"))
        self.SavepushButton.setText(_translate("server_credentials_MainWindow", "Save"))
        self.waringlabel.setText(_translate("server_credentials_MainWindow", "*Max 14 Characters"))
        self.MQTT_setup_label.setText(_translate("server_credentials_MainWindow", "MQTT Setup"))
        self.SSIDWiFilabel.setText(_translate("server_credentials_MainWindow", "SSID *"))
        self.ConnectpushButton.setText(_translate("server_credentials_MainWindow", "Connect"))
        self.MQTTIPlabel.setText(_translate("server_credentials_MainWindow", "Broker IP:"))
        self.MQTTPortlabel_2.setText(_translate("server_credentials_MainWindow", "1883"))


###################################### END PAGE CON_DISSCON GUI ######################################

###################################### START PAGE CON_DISSCON ######################################

        self.client = paho.Client()
        self.client.on_connect = self.on_connect_mqtt
        self.client.on_message = self.on_message_mqtt
        self.SavepushButton.clicked.connect(self.connect_mqtt)
        self.CancelpushButton.clicked.connect(self.cancel)
        self.Device_setup_pushButton.clicked.connect(self.setup)
        self.UpdatepushButton.clicked.connect(self.update)
        self.ConnectpushButton.clicked.connect(self.connect_serial)
        #self.pushButton_2.clicked.connect(self.disconnect_mqtt)


        connBetaExist = os.path.exists(Completeconnectbeta_file)
        if (connBetaExist):
            with open(Completeconnectbeta_file,"r") as f, open(Completeconnect_file,"w") as outfile:
                for i in f.readlines():
                    if not i.strip():
                        continue
                    if i:
                       outfile.write (i)

            self.line1 = linecache.getline(r"Config/Connect.txt", 1)
            self.line2 = linecache.getline(r"Config/Connect.txt", 2)
            self.line3 = linecache.getline(r"Config/Connect.txt", 3)

            self.a = self.line1.translate({ord('\n'):None})
            self.b = self.line2.translate({ord('\n'):None})
            self.c = self.line3.translate({ord('\n'):None})
            #self.d = self.line4.translate({ord('\n'):None})
            self.SSIDWiFilineEdit.setText(self.a)
            self.PasswordWiFilineEdit.setText(self.b)
            self.MQTTIPlineEdit.setText(self.c)

    def No_IP(self):
        self.msgBox = QMessageBox()
        self.msgBox.setText("Please Enter IP address")
        self.msgBox.setWindowTitle("Error")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.exec()

    def No_SSID(self):
        self.msgBox = QMessageBox()
        self.msgBox.setText("Please Enter SSID address")
        self.msgBox.setWindowTitle("Error")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.exec()

    def No_Password(self):
        self.msgBox = QMessageBox()
        self.msgBox.setText("Please Enter Password")
        self.msgBox.setWindowTitle("Error")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.exec()


    def connect_mqtt(self):

        newString1 = self.MQTTIPlineEdit.text()
        newString2 = self.SSIDWiFilineEdit.text()
        newString3 = self.PasswordWiFilineEdit.text()

        IpAddr = newString1.strip()
        ssidMqtt = newString2.strip()
        passwordMqtt = newString3.strip()

        if(not (ssidMqtt and ssidMqtt.strip())):
            self.No_SSID()
            return
        elif(not (passwordMqtt and passwordMqtt.strip())):
            self.No_Password()
            return
        elif(not (IpAddr and IpAddr.strip())):
            self.No_IP()
            return


        f = open (Completeconnectbeta_file, 'w')
        #f= open('preferences_beta.txt','w+')     #Giving '+' helps, or else no file extension
        f.write(self.SSIDWiFilineEdit.text())
        f.write('\n')
        f.write(self.PasswordWiFilineEdit.text())
        f.write('\n')
        f.write(self.MQTTIPlineEdit.text())
        f.write('\n')
        f.close()

        #Auto check IP address
        #IpAddr = self.MQTTIPlineEdit.text()
        #hostname=socket.gethostname()
        #IpAddr = socket.gethostbyname(hostname)


        #MQTT details
        self.MQTT_SERVER = IpAddr
        self.MQTT_PATH = "#"
        self.username = self.MQTTusernamelabel_2.text()
        self.password = "rndtech"
        self.topic = self.MQTTPortlabel_2.text()
        self.port=1883
        self.mqtt_server_connected=0
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.MQTT_SERVER, self.port, 60)
        self.client.loop_start()
        #if MainWindow5.isVisible():
        #    MainWindow5.hide()
    
    def Generate_report_popup(self):
        if MainWindow10.isVisible():
            MainWindow10.hide()
        else:
            MainWindow10.show()

    def on_message_mqtt(self,client, userdata, msg):
        confirm = str(msg.payload.decode())
        
        #Commands To Check received Messages
        if(str(msg.topic)=="/Device/Command"):
            if confirm == '{"Calibration":"On"}':
                #Calibraion Popup
                if MainWindow6.isVisible():
                    MainWindow6.hide()
                else:
                    MainWindow6.show()

        if(str(msg.topic)=="/PC/Command"):
            #Alert Popup
            if confirm == '{"Command":"Alert"}':
                if MainWindow3.isVisible():
                    MainWindow16.hide()
                    MainWindow3.hide()
                else:
                    MainWindow16.hide()
                    MainWindow3.show()

            #Download Data Popup
            if confirm == '{"Command":"Download?"}':
                if MainWindow2.isVisible():
                    MainWindow16.hide()
                    MainWindow2.hide()
                else:
                    MainWindow16.hide()
                    MainWindow2.show()
        
        #Make sure device is connected to MQTT broker
            if confirm == '{"Status":"True"}':
                ui.frame_DeviceStatus.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(255, 255, 255);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(85, 255, 0);\n"
"}")
        
#        #Device Start Popup
#        if(str(msg.topic)=="/Device/Command"):
#            if confirm == '{"Command":"On"}':
#                if MainWindow16.isVisible():
#
#                else:
#                    MainWindow16.show()
        
        if(str(msg.topic) == "/PC/Data"):
            # Show popup when data starts downloading
            if confirm == '{"Status":"Start"}':
                MainWindow12.show()

            f = open (CompletetemporaryData_file,'a+')
            f.write(msg.payload.decode())
            print(msg.payload.decode())
            f.write('\n')
            f.close()

            #Confirm End bit
            if confirm == '{"Status":"Finish"}':
            #if confirm == 'Finish':
                #Data saved Popup
                if MainWindow12.isVisible():
                    MainWindow12.hide()
                    time.sleep(0.3)
                   #MainWindow7.show()
                    self.Generate_report_popup()
                    #if MainWindow10.isVisible():
                    #    MainWindow10.hide()
                    #else:
                    #    MainWindow10.show()

    #Close Server Credentials Window
    def cancel(checked):
        if MainWindow5.isVisible():
            MainWindow5.hide()
        else:
            MainWindow5.show()


    def on_connect_mqtt(self,client, userdata, flags, rc):
        print("\nConnected with result code "+str(rc))
        self.client.subscribe(self.MQTT_PATH)
        self.mqtt_server_connected=1
        if(rc==0):
            print("\nConnection successful")

            msg1 = str('{"Command":"Constat"}')
            self.client.publish("/Device/Command", msg1)

            ui.frame_ProgramStatus.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(255, 255, 255);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(85, 255, 0);\n"
"}")
        else:
            ui.frame_ProgramStatus.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(255, 255, 255);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(255, 0, 4);\n"
"}")
            print("\nSomething went wrong,\nplease check Server credentials.\nAlso make sure computer and server are in the same network.")
    
    def done(self,val):
        if(self.mqtt_server_connected==0):
            print("\nConnect to MQTT Server")
        else:
            print(str(val))

    def update(self):
        self.serialPort = serial.Serial()
        self.serialPort.timeout = 0.5
        self.serialPort.baudrate = 115200
        self.portList = [port.device for port in serial.tools.list_ports.comports()]
        #serial.update_ports() # call to the update ports function in Custom Serial File
        self.USB_comboBox.clear()#Clear the Previous Port List if any
        self.USB_comboBox.addItems(self.portList)# update New Port List
    
    def serialerror(self):
        self.msgBox = QMessageBox()
        self.msgBox.setText("Please check your USB cable connection and update again!")
        self.msgBox.setWindowTitle("Error")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.exec()
    

    def connect_serial(self):
        if(self.ConnectpushButton.isChecked()):
            print("Button press")
            time.sleep(0.5)
            port = self.USB_comboBox.currentText()
            if (not (port and port.strip())):
                self.serialerror()
                return

            self.serialPort.port = port
            try:
                self.serialPort.open()
            except:
                self.show_popup()
        
            if(self.serialPort.is_open):
                self.ConnectpushButton.setText('Disconnect')
                time.sleep(1)
            else:
                self.ConnectpushButton.setChecked(False)
        else:
            self.disconnect_serial()
            self.ConnectpushButton.setText('Connect')
    
    def disconnect_serial(self):
        self.serialPort.close()
    
    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Popup")
        msg.setText("Reconnect USB and Update the list again!")
        msg.setStandardButtons(QMessageBox.ok)
        x = msg.exec_()

    def setup(self):
        #Auto Check IP address
        #hostname=socket.gethostname()
        #IpAddr = socket.gethostbyname(hostname)
        usb_port = self.USB_comboBox.currentText()
        newString = self.MQTTIPlineEdit.text()
        IpAddr = newString.strip()

        var = '"'
        realIp = var+IpAddr+var
        string1 = self.SSIDWiFilineEdit.text()
        string2 = self.PasswordWiFilineEdit.text()
        WiFiSSID_temp = string1.strip()
        WiFiPassword_temp = string2.strip()
        WiFiSSID = var+WiFiSSID_temp+var
        WiFiPassword = var+WiFiPassword_temp+var

        data = ""
        #arduino = serial.Serial(port=usb_port, baudrate=115200, timeout=.5)

        time.sleep(1)

        ssid_temp = '{"SSID":'+WiFiSSID+',"PASSWORD":'+WiFiPassword+',"BRO_IP":'+realIp+',"BRO_UNAME":"RNDTECH","BRO_PASSWD":"rndtech","BRO_PORT":"1883"}'
        #ssid = bytes(str(ssid_temp), 'utf-8')
        #print(ssid.decode('utf-8'))

        #Enter Setup Mode
        self.serialPort.write(b'S')
        index = -1
        while (index == -1):
            #Confirm if device in setup mode
            data = self.serialPort.readline().decode('utf-8').strip()
            index = data.find("MQTT")
            print("\nThis is:- " ,index)

        #Enter Write mode
        self.serialPort.write(b'W')
        #Wait for initialization
        time.sleep(1)
        self.serialPort.write(ssid_temp.encode('utf-8'))
        print(ssid_temp)
        print(ssid_temp.encode())

        #Confirm if Write is finished
        while (data != 'A'):
            data = self.serialPort.readline().decode('utf-8').strip()
            #value = data.decode('utf-8')

        #Quit Setup Mode
        #Setup Complete popup
        self.serialPort.write(b'Q')
        if MainWindow17.isVisible():
            MainWindow17.hide()
        else:
            MainWindow17.show()

###################################### END PAGE CON_DISSCON ######################################

###################################### START PAGE CONFIG GUI ######################################

class Ui_MainWindow(object):
    def setupUi17(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(446, 204)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 421, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.ok_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.ok_pushButton.setGeometry(QtCore.QRect(180, 110, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.ok_pushButton.setFont(font)
        self.ok_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.ok_pushButton.setObjectName("ok_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Device is Configured"))
        self.ok_pushButton.setText(_translate("MainWindow", "OK"))

###################################### STOP PAGE CONFIG popup GUI ######################################

###################################### START PAGE CONFIG MAIN ######################################

        self.ok_pushButton.clicked.connect(self.ok)

    def ok(checked):
        if MainWindow17.isVisible():
            MainWindow17.close()
        else:
            MainWindow17.show()
    
###################################### STOP PAGE CONFIG MAIN ######################################

###################################### START PAGE SAVING DATA GUI ######################################
class Ui_DataSaving_popup_MainWindow(object):
    def setupUi12(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 180)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Popups/icons/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 50, 361, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Saving Data"))
        self.label.setText(_translate("MainWindow", "Please wait until data is saved!"))

###################################### END PAGE SAVING DATA GUI ######################################


###################################### START PAGE RECORDING DATA GUI ######################################
class Ui_Device_Start(object):
    def setupUi16(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 195)
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Popups/icons/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 40, 271, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Please Wait !"))
        self.label.setText(_translate("MainWindow", "Device is recording"))

###################################### START PAGE RECORDING DATA GUI ######################################


###################################### START PAGE ALERT POPUP GUI ######################################

class Ui_Alert_MainWindow(object):
    def setupUi2(self, Alert_MainWindow):
        Alert_MainWindow.setObjectName("Alert_MainWindow")
        Alert_MainWindow.resize(600, 289)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        Alert_MainWindow.setFont(font)
        Alert_MainWindow.setStyleSheet("QMainWindow{\n"
"    \n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(Alert_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.save_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.save_pushButton.setGeometry(QtCore.QRect(160, 170, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.save_pushButton.setFont(font)
        self.save_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.save_pushButton.setObjectName("save_pushButton")
        self.discard_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.discard_pushButton.setGeometry(QtCore.QRect(310, 170, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.discard_pushButton.setFont(font)
        self.discard_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.discard_pushButton.setObjectName("discard_pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 50, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 100, 451, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        Alert_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Alert_MainWindow)
        self.statusbar.setObjectName("statusbar")
        Alert_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(Alert_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Alert_MainWindow)

    def retranslateUi(self, Alert_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Alert_MainWindow.setWindowTitle(_translate("Alert_MainWindow", "Alert"))
        appIcon = QIcon("icons/alert.png")
        Alert_MainWindow.setWindowIcon(appIcon)
        self.save_pushButton.setText(_translate("Alert_MainWindow", "Save"))
        self.discard_pushButton.setText(_translate("Alert_MainWindow", "Discard"))
        self.label.setText(_translate("Alert_MainWindow", "You have some unsaved data."))
        self.label_2.setText(_translate("Alert_MainWindow", "Would you like to save it?"))

###################################### START PAGE ALERT POPUP GUI ######################################

###################################### START PAGE ALERT POPUP GUI ######################################

        self.save_pushButton.clicked.connect(self.save)
        self.discard_pushButton.clicked.connect(self.discard)
    
    #To save data
    def save(checked):
        msg = str('{"Response":"Yes"}')
        ui4.client.publish("/Device/Command",msg)
        # Alert Popup
        if MainWindow3.isVisible():
            MainWindow3.hide()
        else:
            MainWindow3.show()
    
    #To delete the unwanted data
    def discard(checked):
        msg = str('{"Response":"No"}')
        ui4.client.publish("/Device/Command",msg)
        #Alert Popup
        if MainWindow3.isVisible():
            MainWindow3.hide()
        else:
            MainWindow16.hide()
            MainWindow3.show()

###################################### START PAGE ALERT POPUP GUI ######################################

###################################### START PAGE DOWNLOAD POPUP GUI ######################################
class Ui_download_MainWindow(object):
    def setupUi9(self, download_MainWindow):
        download_MainWindow.setObjectName("download_MainWindow")
        download_MainWindow.resize(662, 304)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        download_MainWindow.setFont(font)
        download_MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(download_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 90, 441, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 30, 501, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.yes_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.yes_pushButton.setGeometry(QtCore.QRect(150, 180, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.yes_pushButton.setFont(font)
        self.yes_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.yes_pushButton.setObjectName("yes_pushButton")
        self.no_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.no_pushButton.setGeometry(QtCore.QRect(380, 180, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.no_pushButton.setFont(font)
        self.no_pushButton.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.no_pushButton.setObjectName("no_pushButton")
        download_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(download_MainWindow)
        self.statusbar.setObjectName("statusbar")
        download_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(download_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(download_MainWindow)

    def retranslateUi(self, download_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        download_MainWindow.setWindowTitle(_translate("download_MainWindow", "Download"))
        appIcon = QIcon("icons/save_blue.png")
        download_MainWindow.setWindowIcon(appIcon)
        self.label.setText(_translate("download_MainWindow", "Do you want to save the data now?"))
        self.label_2.setText(_translate("download_MainWindow", "Reading is complete. Ready to send data."))
        self.yes_pushButton.setText(_translate("download_MainWindow", "Yes"))
        self.no_pushButton.setText(_translate("download_MainWindow", "No"))

###################################### END PAGE DONWLOAD POPUP GUI ######################################

###################################### START PAGE DONWLOAD POPUP ######################################

        self.yes_pushButton.clicked.connect(self.yes)
        self.no_pushButton.clicked.connect(self.no)

        
    
    #Save the Data
    def yes(checked):
        msg = str('{"Download":"Yes"}')
        ui4.client.publish("/Device/Command",msg)
        
        if MainWindow2.isVisible():
            MainWindow2.hide()
        else:
            MainWindow2.show()
    
    #Don't save the Data
    def no(checked):
        msg = str('{"Download":"No"}')
        ui4.client.publish("/Device/Command",msg)


        if os.path.exists(CompletetemporaryData_file):
            os.remove(CompletetemporaryData_file)
        else:
            print("\nThe file does not exist")

        if MainWindow2.isVisible():
            MainWindow2.hide()
        else:
            MainWindow16.hide()
            MainWindow3.show()
        

###################################### END PAGE DONWLOAD POPUP ######################################


###################################### START PAGE PATIENT DETAILS GUI ######################################

class Ui_PatientDetails_Report_MainWindow(object):
    def setupUi10(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1071, 589)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Preferences/icons/preference.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(35, 35, 35);\n"
"}\n"
"QMenuBar {\n"
"    /* sets background of the menu */\n"
"    background-color: rgb(65, 65, 65);\n"
"    color:#FFF;\n"
" }\n"
"\n"
"QMenuBar::item:selected{\n"
"    background-color: rgb(85, 85, 255);\n"
" }\n"
"\n"
"QMenu::item {\n"
"     /* sets background of menu item. set this to something non-transparent             rgb(60, 148, 255);\n"
"         if you want menu color and menu item color to be different  rgb(15, 15, 15) */\n"
"    background-color: rgb(65, 65, 65);\n"
"    color:#FFF;\n"
" }\n"
"\n"
"QMenu::item:selected {\n"
"    /* when user selects item using mouse or keyboard */\n"
"    background-color: rgb(85, 85, 255);\n"
" }\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_Logo = QtWidgets.QLabel(self.centralwidget)
        self.label_Logo.setGeometry(QtCore.QRect(950, 510, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_Logo.setFont(font)
        self.label_Logo.setText("")
        self.label_Logo.setPixmap(QtGui.QPixmap(":/RNDLogo/icons/logo_img.jpeg"))
        self.label_Logo.setScaledContents(True)
        self.label_Logo.setObjectName("label_Logo")
        self.label_PatientName = QtWidgets.QLabel(self.centralwidget)
        self.label_PatientName.setGeometry(QtCore.QRect(20, 30, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_PatientName.setFont(font)
        self.label_PatientName.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_PatientName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_PatientName.setObjectName("label_PatientName")
        self.lineEdit_PatientName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_PatientName.setGeometry(QtCore.QRect(210, 40, 821, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_PatientName.setFont(font)
        self.lineEdit_PatientName.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_PatientName.setObjectName("lineEdit_PatientName")
        self.label_PatientID = QtWidgets.QLabel(self.centralwidget)
        self.label_PatientID.setGeometry(QtCore.QRect(20, 110, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_PatientID.setFont(font)
        self.label_PatientID.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_PatientID.setAlignment(QtCore.Qt.AlignCenter)
        self.label_PatientID.setObjectName("label_PatientID")
        self.lineEdit_PatientID = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_PatientID.setGeometry(QtCore.QRect(210, 120, 301, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_PatientID.setFont(font)
        self.lineEdit_PatientID.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_PatientID.setObjectName("lineEdit_PatientID")
        self.label_RefDocName = QtWidgets.QLabel(self.centralwidget)
        self.label_RefDocName.setGeometry(QtCore.QRect(490, 110, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_RefDocName.setFont(font)
        self.label_RefDocName.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_RefDocName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_RefDocName.setObjectName("label_RefDocName")
        self.lineEdit_RefDocName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_RefDocName.setGeometry(QtCore.QRect(730, 120, 301, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_RefDocName.setFont(font)
        self.lineEdit_RefDocName.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_RefDocName.setObjectName("lineEdit_RefDocName")
        self.label_Address = QtWidgets.QLabel(self.centralwidget)
        self.label_Address.setGeometry(QtCore.QRect(20, 190, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_Address.setFont(font)
        self.label_Address.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_Address.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Address.setObjectName("label_Address")
        self.lineEdit_Address = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Address.setGeometry(QtCore.QRect(210, 200, 821, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_Address.setFont(font)
        self.lineEdit_Address.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_Address.setObjectName("lineEdit_Address")
        self.lineEdit_MobileNo = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_MobileNo.setGeometry(QtCore.QRect(210, 280, 301, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_MobileNo.setFont(font)
        self.lineEdit_MobileNo.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_MobileNo.setObjectName("lineEdit_MobileNo")
        self.label_MobileNo = QtWidgets.QLabel(self.centralwidget)
        self.label_MobileNo.setGeometry(QtCore.QRect(20, 270, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_MobileNo.setFont(font)
        self.label_MobileNo.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_MobileNo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_MobileNo.setObjectName("label_MobileNo")
        self.comboBoxGender = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxGender.setGeometry(QtCore.QRect(830, 280, 201, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBoxGender.setFont(font)
        self.comboBoxGender.setStyleSheet("QComboBox{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: right;\n"
"     width: 13px;\n"
" }\n"
"\n"
"QComboBox:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 2px solid rgb(74, 74, 74);\n"
"    selection-background-color: rgb(6, 103, 229);\n"
"    \n"
"    background-color: rgb(54, 54, 54);\n"
"    color:#FFF\n"
" }\n"
"\n"
"QComboBox:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.comboBoxGender.setObjectName("comboBoxGender")
        self.comboBoxGender.addItem("")
        self.comboBoxGender.addItem("")
        self.label_Gender = QtWidgets.QLabel(self.centralwidget)
        self.label_Gender.setGeometry(QtCore.QRect(660, 270, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_Gender.setFont(font)
        self.label_Gender.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_Gender.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Gender.setObjectName("label_Gender")
        self.label_DOB = QtWidgets.QLabel(self.centralwidget)
        self.label_DOB.setGeometry(QtCore.QRect(40, 350, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_DOB.setFont(font)
        self.label_DOB.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_DOB.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DOB.setObjectName("label_DOB")
        self.lineEdit_DOBDD = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_DOBDD.setGeometry(QtCore.QRect(210, 360, 111, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_DOBDD.setFont(font)
        self.lineEdit_DOBDD.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_DOBDD.setObjectName("lineEdit_DOBDD")
        self.lineEdit_DOBMM = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_DOBMM.setGeometry(QtCore.QRect(330, 360, 111, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_DOBMM.setFont(font)
        self.lineEdit_DOBMM.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_DOBMM.setObjectName("lineEdit_DOBMM")
        self.lineEdit_DOBYY = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_DOBYY.setGeometry(QtCore.QRect(450, 360, 111, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_DOBYY.setFont(font)
        self.lineEdit_DOBYY.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_DOBYY.setObjectName("lineEdit_DOBYY")
        self.label_Age = QtWidgets.QLabel(self.centralwidget)
        self.label_Age.setGeometry(QtCore.QRect(760, 350, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_Age.setFont(font)
        self.label_Age.setStyleSheet("background-color: none;\n"
"color: #FFF;")
        self.label_Age.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Age.setObjectName("label_Age")
        self.lineEdit_Age = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Age.setGeometry(QtCore.QRect(890, 360, 141, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_Age.setFont(font)
        self.lineEdit_Age.setStyleSheet("QLineEdit{\n"
"    border: 5px solid rgb(50, 50, 50);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(54, 54, 54);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    border:2px solid rgb(74, 74, 74);\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"    border:2px solid rgb(85, 85, 255);\n"
"    background-color: rgb(63, 63, 63);\n"
"}")
        self.lineEdit_Age.setObjectName("lineEdit_Age")
        self.pushButton_GenerateReport = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_GenerateReport.setGeometry(QtCore.QRect(250, 450, 211, 34))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.pushButton_GenerateReport.setFont(font)
        self.pushButton_GenerateReport.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.pushButton_GenerateReport.setObjectName("pushButton_GenerateReport")
        self.pushButton_Cancel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(680, 450, 211, 34))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.pushButton_Cancel.setFont(font)
        self.pushButton_Cancel.setStyleSheet("QPushButton{\n"
"    background-color: ;\n"
"    background-color: rgb(6, 103, 229);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"    color:#FFF;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(5, 117, 252);\n"
"}\n"
"QPushButton:pressed{\n"
"    border:2px solid rgb(5, 116, 250);\n"
"    background-color: rgb(73, 161, 255);\n"
"}")
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_PatientName.setText(_translate("MainWindow", "Patient Name *"))
        self.lineEdit_PatientName.setPlaceholderText(_translate("MainWindow", "Full Name"))
        self.label_PatientID.setText(_translate("MainWindow", "Patient ID"))
        self.label_RefDocName.setText(_translate("MainWindow", "Ref. Doctor Name"))
        self.label_Address.setText(_translate("MainWindow", "Address"))
        self.label_MobileNo.setText(_translate("MainWindow", "Mobile No."))
        self.comboBoxGender.setItemText(0, _translate("MainWindow", "Male"))
        self.comboBoxGender.setItemText(1, _translate("MainWindow", "Female"))
        self.label_Gender.setText(_translate("MainWindow", "Gender"))
        self.label_DOB.setText(_translate("MainWindow", "Date of Birth"))
        self.lineEdit_DOBDD.setPlaceholderText(_translate("MainWindow", "DD"))
        self.lineEdit_DOBMM.setPlaceholderText(_translate("MainWindow", "MM"))
        self.lineEdit_DOBYY.setPlaceholderText(_translate("MainWindow", "YYYY"))
        self.label_Age.setText(_translate("MainWindow", "Age"))
        self.pushButton_GenerateReport.setText(_translate("MainWindow", "Generate Report"))
        self.pushButton_Cancel.setText(_translate("MainWindow", "Cancel"))

###################################### END PAGE PATIENT DETAILS GUI ######################################

###################################### START PAGE PATIENT DETAILS MAIN ######################################

        self.pushButton_GenerateReport.clicked.connect(self.Generate)
        self.pushButton_Cancel.clicked.connect(self.no)


    #Close popup
    def no(checked):
        
        # Clear all the filled spaces
        ui10.lineEdit_Address.clear()
        ui10.lineEdit_Age.clear()
        ui10.lineEdit_MobileNo.clear()
        ui10.lineEdit_PatientID.clear()
        ui10.lineEdit_PatientName.clear()
        ui10.lineEdit_RefDocName.clear()
        ui10.lineEdit_DOBDD.clear()
        ui10.lineEdit_DOBMM.clear()
        ui10.lineEdit_DOBYY.clear()
        ui10.lineEdit_DOBDD.setPlaceholderText(("DD"))
        ui10.lineEdit_DOBMM.setPlaceholderText(("MM"))
        ui10.lineEdit_DOBYY.setPlaceholderText(("YYYY"))


        ui.frame_DeviceStatus.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(255, 255, 255);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(255, 0, 4);\n"
"}")
        if MainWindow10.isVisible():
            MainWindow10.hide()
        else:
            MainWindow10.show()

    def Incomplete_form(self):
        self.msgBox = QMessageBox()
        self.msgBox.setText("Inclompete Form!.\nPlease enter Patient Name")
        self.msgBox.setWindowTitle("Error")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.exec()

    def Absent_Data(self):
        self.msgBox = QMessageBox()
        self.msgBox.setText("There is no data!")
        self.msgBox.setWindowTitle("Error")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.exec()

    def Zero_Data(self):
        self.msgBox = QMessageBox()
        self.msgBox.setText("Report cannot be generated since data is Null!")
        self.msgBox.setWindowTitle("Error")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.exec()

    #Generate Report
    def Generate(checked):
        PatientName = ui10.lineEdit_PatientName.text()
        if(not (PatientName and PatientName.strip())):
            ui10.Incomplete_form()
            return
        
        file_exist1 = exists(CompletetemporaryData_JSONfile)
        file_exist2= exists(Completeconverted_file)
        file_exist5 = exists(CompletetemporaryDataNew_file)
        file_exist8 = exists(CompletetemporaryData_file)

        if (file_exist1 == True):
            os.remove(CompletetemporaryData_JSONfile)
        if (file_exist2 == True):
            os.remove(Completeconverted_file)
        if (file_exist5 == True):
            os.remove(CompletetemporaryDataNew_file)
        if (file_exist8 == False):
            ui10.Absent_Data()
            return

        with open(CompletetemporaryData_file, "r") as f:
            lines = f.readlines()
        with open(CompletetemporaryData_file, "w") as f:
            for line in lines:
                #Remove Following line before going to CSV
                if line.strip("\n") != '{"Status":"Start"}':
                    f.write(line)

        with open(CompletetemporaryData_file, "r") as f:
            lines = f.readlines()
        with open(CompletetemporaryData_file, "w") as f:
            for line in lines:
                
                #Remove Following line before going to CSV
                if line.strip("\n") != '{"Status":"Finish"}':
                    f.write(line)

        with open(CompletetemporaryData_file) as f:
            lines = f.readlines()

        count = 0
        for line in lines:
            count += 1
            #print(f'line {count}: {line}')
            
            #Remove Brackets before going to CSV
            new = line.strip('\n')
            new1 = new.strip('{')
            new2 = new1.strip('}')
            print(new2)

            f = open(CompletetemporaryDataNew_file,'a')
            f.write(new2)
            f.write('\n')
            #f.write(confirm)
            f.close()
        
        #Convert to json
        with open(CompletetemporaryDataNew_file) as logfile:
            log_list = []
            for line in logfile:
                pipe_split = [ele.strip() for ele in line.split(",")]
                line_dict = dict()
                for ele in pipe_split:
                    key,val = ele.split(":")
                    line_dict[key] = val
                log_list.append(line_dict)

        
        #Save in Json file
        with open(CompletetemporaryData_JSONfile,'w') as f:
            json.dump(log_list,f,indent=2)
        
        
        #Convert to CSV
        pdObj = pd.read_json(r'Patient Data/temporary_data.json', orient=None)
        pdObj.to_csv(Completeconverted_file, index=False)
    
        s = []
        x = []
        y = []
        z = []

        with open(Completeconverted_file,'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            next(lines)
            for row in lines:
                s.append(int(row[2]))                           #Row 3 is Time
                z.append(int(row[1]))                           #Row 2 is Volume
                #x = np.divide(s, 1000)

            for i in range(0, len(z)):
                if z[i] < 0:
                    z[i] = 0
        #print("\nThis is time: " ,s)
        #print("\nThis is Volume: " ,z)

        a = np.nonzero(z)
        araa = np.array(a)
        #print("\nThe hell: ", type(araa))
        print (len(araa))
        print (araa)

        if araa.any()== False:
            ui10.Zero_Data()
            return
        non_zero = a[0][0]
        #print(non_zero)

        if non_zero!=0:
            b = non_zero
            print("\nhow many non zeros",  b)
            del z[:b]
            del s[-b:]
            print("\nVolume length", len(z))                               #Volume
            print("\nTime length", len(s))                               #Time
            #full_length_x = len(x)
            #before_pop = full_length_x-1
            #s.pop(before_pop)
            #s.insert(0,0)
            x = np.divide(s, 1000)
            print("\ntime after divide", x)
            y = z
            print("\nThis is Volume: " ,y)
            #y = z[b:-c]

        
        i = 0
        y2 = []
        y2+= [0]
        for i in range(0, len(y)-1):
            y2+= [y[i+1]-y[i]]
        
        for i in range(0, len(y2)):
            if y2[i] < 0:
                y2[i] = 0

        print("\nFlow Rate is", y2)
        print("\nLength of Flow Rate:- ", len(y2))

        c = 90  
        avg1 = [y2]
        print("This is AVG1" ,avg1)
        del avg1[-c:]                                                #change to 90
        print(c)
        avg = y2[:-c]
        print(len(y2))

        print("This is avg1\n")
        print("\nLength ", len(avg1))
        print(avg1)
        #output = [idx for idx, value in enumerate(avg)  if value <= 2]
        #g = ''.join(str(output).split(','))

        print("\nI am delete" ,avg)
        print("\nLength ", len(avg))

        diff_var = y2
        print("\nI am diff_var", diff_var)

        chopped_array = np.array(diff_var)
        print("\nChopped array" ,chopped_array)
        
        get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
        e = get_indexes(0,chopped_array)
        #for ele in sorted(e, reverse = True):
        chopped_array1 = np.delete(chopped_array, e)
        print("\nChopped 0 array", chopped_array1)

        compounded_avg_temp = np.average(chopped_array1)
        compounded_avg = round(compounded_avg_temp, 2)
        maxcomputedflow_temp = np.amax(chopped_array1)
        print(maxcomputedflow_temp)
        maxcomputedflow_temp1 = np.setdiff1d(chopped_array1, maxcomputedflow_temp)
        print("\nType of array is:- " ,type(chopped_array))
        chopped_array.tolist()
        print("\nType of array is:- " ,type(chopped_array))
        print (maxcomputedflow_temp1)
        maxcomputedflow = np.amax(maxcomputedflow_temp1)

        

        average_temp = np.average(avg)
        average_oneSec = average_temp*2                             # Per one Sec
        average = round(average_oneSec, 2)
        maxFlowrate= np.amax(chopped_array1)
        indicetomax= np.where(avg == np.amax(avg))

        timetomax_temp = x[indicetomax]
        timetomax = np.amin(timetomax_temp)


        maxVolume= y[len(y) - 1]
        voidtime = x[:-c]
        totalTime_temp = voidtime[len(voidtime) - 1]
        totalTime = round(totalTime_temp, 2)
        delay_time = x[b-1]

        chopped_array = np.array(avg)

        #print("Chopped array again", chopped_array)
        #print("New any",chopped_array.all())

        if chopped_array.all():
            ui10.Zero_Data()
            return

        chopped_time = np.array(x)

        get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
        #d1 = get_indexes(-2, chopped_array)
        d2 = get_indexes(-1, chopped_array)
        d3 = get_indexes(0, chopped_array)
        d4 = get_indexes(1, chopped_array)
        #d5 = get_indexes(2, chopped_array)

        unwanted_values = d2+d3+d4
        unwanted_values.sort()
        print("\nIndexes of Unwanted values:- ", unwanted_values)


        indexes_for_time1 = []
        for k, g in groupby(enumerate(unwanted_values), lambda x: x[0]-x[1]):
            indexes_for_time1.append(list(map(itemgetter(1), g)))
        
        length_of_indexes = len(indexes_for_time1)
        print(indexes_for_time1)
        print(chopped_array)
        print(unwanted_values)
        print(chopped_time)
        for i in range(0, length_of_indexes):
            print("\nSub arrays are:- " ,indexes_for_time1[i])

        max1 = []
        min1 = []
        for i in range (0, length_of_indexes):
            max1+=[np.amax(indexes_for_time1[i])]
            min1+=[np.amin(indexes_for_time1[i])]
        
        length_of_max = len(max1)
        length_of_min = len(min1)

        chopped_time1 = chopped_time[:-c]


        max_and_min = []
        for i in range (0, length_of_max):
            max2 = max1[i]
            min2 = min1[i]
            max_and_min += [chopped_time1[max2]-chopped_time1[min2]]
            print(max_and_min,"=", chopped_time1[max2], "-",chopped_time1[min2])

        interval_time1 = 0
        for ele in range(0, len(max_and_min)):
            interval_time1 = interval_time1 + max_and_min[ele]
        
        interval_time = round(interval_time1, 2)
        flowTime = totalTime-interval_time
        

        #length_together = len(max_and_min)
        #before_temp = []
        #before_temp1 = []
        #for i in range (0, length_together):
        #    before_temp = max_and_min[i]
        #    before_temp1 += [chopped_time[before_temp]]
        
        #length_before_temp = len(before_temp1)
        #temp_time = []

        #for i in range (0, length_before_temp-1):
        #    temp_time += [before_temp1[i+1]- before_temp1[i]]
        
        #del temp_time[1::2]
        #interval_time1 = 0
        #for ele in range(0, len(temp_time)):
        #    interval_time1 = interval_time1 + temp_time[ele]
        
        #interval_time = round(interval_time1,2)



        fig,ax = plt.subplots()

        ax.set_xticks(np.arange(0,200,10))
        ax.set_yticks(np.arange(0,60,5))
        ax.set_xlim(0,180)
        ax.set_ylim(0,50)
        ax.plot(x, y2, color="blue", label = "Uroflow Graph")
        fig.set_size_inches(13, 5)
        # set x-axis label
        ax.set_xlabel("Time",color="green",fontsize=14)
        # set y-axis label
        ax.set_ylabel("Flowrate",color="blue",fontsize=12)
        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        ax2.set_yticks(np.arange(0,1800,100))
        ax2.set_ylim(0,1000)
        # make a plot with different y-axis using second axis object
        ax2.plot(x, y,color="red", linestyle= "solid")
        ax2.set_ylabel("Volume (ml)",color="red",fontsize=12)
        #ax.grid()
        ax.grid(axis = 'x')
        ax2.grid()                                      #DONT USE GRID(YES WE HAVE TO)
        #plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
        plt.savefig(CompletelGraphImage_file, bbox_inches='tight')
        #plt.show()
        #plt.close()
        np.diff

        newpath = 'Report'
        try:
            os.mkdir(newpath)
            print (newpath)
        except FileExistsError:
            print("\nit is there")                                # Delete this please
        save_path3 = r'Report/'
        
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
    
    
        #file_name3 = ui.patient_lineEdit.text()+ " " + str(d1) +" Report.pdf"
        file_name3 = ui10.lineEdit_PatientName.text()+ " " + str(today) +" Report.pdf"
        CompleteReport_File = os.path.join(save_path3, file_name3)


        canvas = Canvas(CompleteReport_File, pagesize=A4)

        stringData1 = ui3.clinic_lineEdit.text()
        stringData2 = ui3.doc_name_lineEdit.text()
        stringData3 = ui3.specilist_lineEdit.text()
        stringData4 = ui3.clinic_address_lineEdit.text()
        stringData5 = ui3.mobile_no_lineEdit.text()
        stringData6 = ui3.doc_email_lineEdit.text()


        # Clinic Name
        canvas.setFont("Helvetica-Bold", 15)
        canvas.drawCentredString(300, 800, text= stringData1.strip())

        # Doctor Name
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 10.65 * inch, "Doctor Name: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.47 * inch, 10.65 * inch, stringData2.strip())

        # Specilist
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5 * inch, 10.65 * inch, "Specilist: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.65 * inch, 10.65 * inch, stringData3.strip())

        # Mobile No.
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 10.35 * inch, "Mobile No. : ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.31 * inch, 10.35 * inch, stringData5.strip())

        # Address
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 10.5 * inch, "Address: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.16 * inch, 10.5 * inch, stringData4.strip())

        # Email
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5 * inch, 10.35 * inch, "Email: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.45 * inch, 10.35 * inch, stringData6.strip())

        # Border
        canvas.drawString(0.3 * inch, 10.15 * inch, "--------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        # Patient Details
        canvas.setFont("Helvetica-Bold", 15)
        canvas.drawString(3.1 * inch, 9.9 * inch, "Patient Details")

        # Patient Name
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 9.7 * inch, "Patient Name: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.5 * inch, 9.7 * inch, ui10.lineEdit_PatientName.text())

        # Reference Doctor Name
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5.0 * inch, 9.55 * inch, "Ref. Doctor Name: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(6.25 * inch, 9.55 * inch, ui10.lineEdit_RefDocName.text())

        # Patient ID
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5 * inch, 9.7 * inch, "Patient ID : ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.85 * inch, 9.7 * inch, ui10.lineEdit_MobileNo.text())

        # Date of Birth
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 9.55 * inch, "Date of Birth: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.42 * inch, 9.55 * inch, ui10.lineEdit_DOBDD.text()+"/" + ui10.lineEdit_DOBMM.text()+"/"+ui10.lineEdit_DOBYY.text())

        # Gender
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5 * inch, 9.4 * inch, "Gender: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.6 * inch, 9.4 * inch, ui10.comboBoxGender.currentText())

        # Mobile No. Patient
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 9.25 * inch, "Mobile No. : ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.31 * inch, 9.25 * inch, ui10.lineEdit_MobileNo.text())

        # Age
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5* inch, 9.25 * inch, "Age : ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.4 * inch, 9.25 * inch, ui10.lineEdit_Age.text()+" Yrs")

        # Address
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 9.4 * inch, "Address: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.16 * inch, 9.4 * inch, ui10.lineEdit_Address.text())

        # Border
        canvas.drawString(0.3 * inch, 9.0 * inch, "--------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        # Main Graph
        canvas.drawImage(image=CompletelGraphImage_file, x=35,y=290,height= 4* inch, width= 7.5 * inch)
        
        # Max. Graph
        #canvas.drawImage(image=CompletelGraphImage_file, x=50,y=235,height= 2* inch, width= 3 * inch)
        
        # Average Graph
        #canvas.drawImage(image=CompletelGraphImage_file, x=320,y=235,height= 2* inch, width= 3 * inch)

        #Logo
        canvas.drawImage(image=Completelogoimage_file, x=15,y=15,height= 0.5* inch, width= 0.7 * inch)

        canvas.setFont("Helvetica-Bold",8)
        canvas.drawString(5.2 * inch, 0.3 * inch, "R & D Tech. "+", Yogesh Shindikar "+", +91 98817 35805")

        # Characteristics
        canvas.setFont("Helvetica-Bold", 15)
        canvas.drawString(0.5 * inch, 3.0 * inch, "Characteristics: ")

        # Voided Volume
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 2.7 * inch, "Voided Volume: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.6 * inch, 2.7 * inch, str(maxVolume)+" ml")

        # Voided Time
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5.0 * inch, 2.7 * inch, "Voided Time: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.93 * inch, 2.7 * inch, str(totalTime)+" Sec")

        # Max. Flow rate
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 2.55 * inch, "Max. Flow Rate: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.58 * inch, 2.55 * inch, str(maxFlowrate)+" ml/sec")

        # Flow Time
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5.0 * inch, 2.55 * inch, "Flow Time: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.8 * inch, 2.55 * inch, str(flowTime)+" Sec")

        # Computed Max Flow
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 2.4 * inch, "Computed Max. Flow : ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(2.05 * inch, 2.4 * inch, str(maxcomputedflow)+" ml/sec")

        # Time to Max.
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5.0 * inch, 2.4 * inch, "Time to Max. : ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(6.0 * inch, 2.4 * inch, str(timetomax)+" Sec")

        # Average Flow rate
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 2.25 * inch, "Average Flow Rate: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(1.85 * inch, 2.25 * inch, str(float(average)) +" ml/sec")

        # Delay Time
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5 * inch, 2.25 * inch, "Delay time: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(5.8 * inch, 2.25 * inch, str(delay_time) +" Sec")

        # Computed Average Flow
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 2.1 * inch, "Computed Average Flow: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(2.25 * inch, 2.1 * inch, str(compounded_avg) +" ml/sec")

        # Interval Time
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(5.0 * inch, 2.1 * inch, "Interval Time: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(6.0 * inch, 2.1 * inch, str(interval_time) +" sec")

        # Post Voided Residual
        canvas.setFont("Helvetica-Bold",10)
        canvas.drawString(0.5 * inch, 1.95 * inch, "Post Voided Residual (PVR): ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(2.45 * inch, 1.95 * inch, "___________")



        # Comments
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(0.5 * inch, 1.5 * inch, "Comments: ")
        canvas.setFont("Times-Roman",10)
        canvas.drawString(0.3 * inch, 1.2 * inch, "____________________________________________________________________________________________________________")
        canvas.drawString(0.3 * inch, 0.9 * inch, "____________________________________________________________________________________________________________")


        # Save the PDF file
        canvas.save()

        # Delete all the files.
        if os.path.exists(CompletetemporaryData_file):
            os.remove(CompletetemporaryData_file)
        else:
            print("\nThe file does not exist")

        if os.path.exists(CompletetemporaryData_JSONfile):
            os.remove(CompletetemporaryData_JSONfile)
        else:
            print("\nThe file does not exist")

        if os.path.exists(Completeconverted_file):
            os.remove(Completeconverted_file)
        else:
            print("\nThe file does not exist")

        if os.path.exists(CompletetemporaryDataNew_file):
            os.remove(CompletetemporaryDataNew_file)
        else:
            print("\nThe file does not exist")
        

        # Clear all the filled spaces
        ui10.lineEdit_Address.clear()
        ui10.lineEdit_Age.clear()
        ui10.lineEdit_MobileNo.clear()
        ui10.lineEdit_PatientID.clear()
        ui10.lineEdit_PatientName.clear()
        ui10.lineEdit_RefDocName.clear()
        ui10.lineEdit_DOBDD.clear()
        ui10.lineEdit_DOBMM.clear()
        ui10.lineEdit_DOBYY.clear()
        ui10.lineEdit_DOBDD.setPlaceholderText(("DD"))
        ui10.lineEdit_DOBMM.setPlaceholderText(("MM"))
        ui10.lineEdit_DOBYY.setPlaceholderText(("YYYY"))


        ui.frame_DeviceStatus.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(255, 255, 255);\n"
"    border-radius:15px;\n"
"    color:#FFF;\n"
"    padding-left:20px;\n"
"    padding-right:20px;\n"
"    background-color: rgb(255, 0, 4);\n"
"}")
        
        if MainWindow10.isVisible():
            MainWindow10.hide()
        else:
            MainWindow10.show()
        

###################################### END PAGE PATIENT DETAILS MAIN ######################################

###################################### END ALL ######################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow1 = QtWidgets.QMainWindow()                               # First Window with start
    MainWindow2 = QtWidgets.QMainWindow()
    MainWindow3 = QtWidgets.QMainWindow()
    MainWindow4 = QtWidgets.QMainWindow()                               # Preferences Window
    MainWindow5 = QtWidgets.QMainWindow()                               # Server Credentials
    MainWindow6 = QtWidgets.QMainWindow()                              # Calibrate popup
    MainWindow7 = QtWidgets.QMainWindow()                               # Preferences popup Window
    MainWindow10 = QtWidgets.QMainWindow()                              # Report old Window number replace with Patient Details window
    MainWindow12 = QtWidgets.QMainWindow()
    MainWindow14 = QtWidgets.QMainWindow()                              # Preferences DUMMY Window
    MainWindow15 = QtWidgets.QMainWindow()                              # Login for setup
    MainWindow16 = QtWidgets.QMainWindow()                             # Device Started popup (OLD:- Patient details saved)
    MainWindow17 = QtWidgets.QMainWindow()                              # USB device Configured popup


    ui10 = Ui_PatientDetails_Report_MainWindow()
    ui10.setupUi10(MainWindow10)
    MainWindow10.show()
    MainWindow10.hide()
    
    ui4 = Ui_server_credentials_MainWindow()
    ui4.setupUi4(MainWindow5)

    ui = Ui_PageOne_MainWindow()
    ui.setupUi(MainWindow1)
    MainWindow1.show()

    ui12 = Ui_DataSaving_popup_MainWindow()
    ui12.setupUi12(MainWindow12)
    MainWindow12.show()
    MainWindow12.hide()
    
    ui5 = Ui_Calibrate_popup_MainWindow()
    ui5.setupUi5(MainWindow6)
    MainWindow6.show()
    MainWindow6.hide()

    ui16 = Ui_Device_Start()
    ui16.setupUi16(MainWindow16)
    MainWindow16.show()
    MainWindow16.hide()

    ui17 = Ui_MainWindow()
    ui17.setupUi17(MainWindow17)
    MainWindow17.show()
    MainWindow17.hide()

    ui15 = Ui_setup_MainWindow()
    ui15.setupUi15(MainWindow15)

    ui14 = Ui_dummy_prefrences_MainWindow()
    ui14.setupUi14(MainWindow14)

    ui9 = Ui_download_MainWindow()
    ui9.setupUi9(MainWindow2)
    MainWindow2.show()
    MainWindow2.hide()

    ui2 = Ui_Alert_MainWindow()
    ui2.setupUi2(MainWindow3)
    MainWindow3.show()
    MainWindow3.hide()

    ui3 = Ui_preferences_MainWindow()
    ui3.setupUi3(MainWindow4)
    ui6 = Ui_prefrences_popup_MainWindow()
    ui6.setupUi6(MainWindow7)

    sys.exit(app.exec_())