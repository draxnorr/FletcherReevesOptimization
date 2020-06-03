# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import cexprtk
from PyQt5 import QtCore, QtGui, QtWidgets
import constants_file as cnst
import fletcherReevesOpt as fropt
import showoptimizationstepswindow as window2


class Ui_mainWindow(object):
    data_correctness_dict = {'fx': False, 'x0': False, 'eps_checkboxes': False}
    criteria_dict = {} # zaznaczone kryteria i wartosci
    symbol_dict = {} # nazwy zmiennych i ich wartosci

    def wyswietl_kroki(self):
        self.Dialog = QtWidgets.QDialog()
        ui = window2.Ui_Dialog ()
        ui.setupUi (self.Dialog)
        self.Dialog.exec()


    def update_criteria_dict(self):
        criteria_dict={}
        if self.checkBox_stop1.isChecked():
            self.criteria_dict["eps1"] = float(self.lineEdit_eps1.text())
        if self.checkBox_stop2.isChecked():
            self.criteria_dict["eps2"] = float(self.lineEdit_eps2.text())
        if self.checkBox_stop3.isChecked():
            self.criteria_dict["eps3"] = float(self.lineEdit_eps3.text())
        if self.checkBox_stop4.isChecked():
            self.criteria_dict["eps4"] = float(self.lineEdit_eps4.text())
        if self.checkBox_stopk1.isChecked():
            self.criteria_dict["epsk1"] = float(self.lineEdit_epsk1.text())
        if self.checkBox_stopk2.isChecked():
            self.criteria_dict["epsk2"] = float(self.lineEdit_epsk2.text())

    def startOptimization(self):
        self.update_criteria_dict()
        with open("optimization.txt","w") as file:
            file.write(self.comboBox_fx.currentText()+"\n")
            file.write(",".join(self.symbol_dict.keys())+"\n")
        with open("indirection.txt","w") as file:
            file.write (self.comboBox_fx.currentText ()+"\n")
            file.write (",".join (self.symbol_dict.keys ())+"\n")

        (fopt, xopt) = fropt.optimize_fletcher_reeves(self.comboBox_fx.currentText(), self.symbol_dict,
                                                      self.criteria_dict, float(self.lineEdit_alfa0.text()))
        self.textBrowser_f_opt.setText(str(fopt))
        self.textBrowser_x_opt.setText(", ".join([str(x) for x in xopt]))
        self.pushButton_wyswietl_kroki.setEnabled(True)

    def unlock_button_rozpocznij_opt(self):
        ans = True
        for value in self.data_correctness_dict.values():
            ans = ans and value
        self.pushButton_rozpocznij_opt.setEnabled(ans)

    def check_stop_checkboxes(self, v):
        value = self.checkBox_stop1.isChecked() or self.checkBox_stop2.isChecked () or \
            self.checkBox_stop3.isChecked () or self.checkBox_stop4.isChecked ()
        self.data_correctness_dict['eps_checkboxes'] = value
        self.unlock_button_rozpocznij_opt()

    def lock_checkBox_inne_kryteria(self, inne_kryteria_checkBox_state):
        if not self.checkBox_stopk1.isChecked() and not self.checkBox_stopk2.isChecked():
            self.checkBox_inne_kryteria.setChecked(False)
            self.checkBox_stopk1.setEnabled(False)
            self.checkBox_stopk2.setEnabled(False)

    def comboBox_fx_TextChanged(self,text):
        self.symbol_dict= {}
        exp_variables = []

        def callback(symbol):
            nonlocal exp_variables
            exp_variables.append(symbol)
            return (True, cexprtk.USRSymbolType.VARIABLE, 0.0, "")

        st = cexprtk.Symbol_Table({},cnst.m_constants, add_constants = True)

        try:
            cexprtk.Expression(text,st,callback)
            for sym in sorted (exp_variables):
                self.symbol_dict[sym] = 0.0
            self.textBrowser_x.setText('['+", ".join([*self.symbol_dict.keys()])+']')
            self.lineEdit_x0.setText(", ".join([str(x) for x in self.symbol_dict.values()]))
            self.data_correctness_dict['fx'] = True
            self.data_correctness_dict['x0'] = True
        except:
            self.comboBox_fx.removeItem(self.comboBox_fx.currentIndex())
            self.comboBox_fx.setCurrentText("Błąd odczytania funkcji. Nieznane znaki.")
            self.textBrowser_x.setText ("[]")
            self.lineEdit_x0.setText ("")
            self.data_correctness_dict['fx'] = False
            self.data_correctness_dict['x0'] = False
        self.unlock_button_rozpocznij_opt()

    def checkTextCorrectness_lineEdit_eps1(self):
        text = self.lineEdit_eps1.text()
        val_if_error = 0.001
        try:
            val = float(text)
            if val <= 0 or val > 10**200:
                val = val_if_error
            self.lineEdit_eps1.setText(str(val))
        except:
            self.lineEdit_eps1.setText (str (val_if_error))

    def checkTextCorrectness_lineEdit_eps2(self):
        text = self.lineEdit_eps2.text ()
        val_if_error = 0.001
        try:
            val = float(text)
            if val <= 0 or val > 10**200:
                val = val_if_error
            self.lineEdit_eps2.setText(str(val))
        except:
            self.lineEdit_eps2.setText(str (val_if_error))

    def checkTextCorrectness_lineEdit_eps3(self):
        text = self.lineEdit_eps3.text ()
        val_if_error = 0.001
        try:
            val = float(text)
            if val <= 0 or val > 10**200:
                val = val_if_error
            self.lineEdit_eps3.setText(str(val))
        except:
            self.lineEdit_eps3.setText (str(val_if_error))

    def checkTextCorrectness_lineEdit_eps4(self):
        text = self.lineEdit_eps4.text ()
        val_if_error = 100
        try:
            val = int(text)
            if val <= 0 or val > 10**200:
                val = val_if_error
            self.lineEdit_eps4.setText(str(val))
        except:
            self.lineEdit_eps4.setText (str(val_if_error))

    def checkTextCorrectness_lineEdit_epsk1(self):
        text = self.lineEdit_epsk1.text ()
        val_if_error = 0.001
        try:
            val = float(text)
            if val <= 0 or val > 10**200:
                val = val_if_error
            self.lineEdit_epsk1.setText(str(val))
        except:
            self.lineEdit_epsk1.setText (str(val_if_error))

    def checkTextCorrectness_lineEdit_epsk2(self):
        text = self.lineEdit_epsk2.text ()
        val_if_error = 0.001
        try:
            val = float(text)
            if val <= 0 or val > 10**200:
                val = val_if_error
            self.lineEdit_epsk2.setText(str(val))
        except:
            self.lineEdit_epsk2.setText (str(val_if_error))

    def checkTextCorrectness_lineEdit_alfa0(self):
        text = self.lineEdit_alfa0.text ()
        alfa0_MAX_VALUE = 10**200
        alfa0_MIN_VALUE = 0
        val_if_error = 1
        try:
            val = float(text)
            if val <= alfa0_MIN_VALUE or val > alfa0_MAX_VALUE:
                val = val_if_error
            self.lineEdit_alfa0.setText(str(val))
        except:
            self.lineEdit_alfa0.setText (str(val_if_error))

    def checkTextCorrectness_lineEdit_x0(self):
        # jesli blad, zapisz 0.0; odetnij, jesli podano zbyt wiele wartosci
        x0_MAX_VALUE = 10**200
        x0_MIN_VALUE = -10**200
        text = self.lineEdit_x0.text()

        values_str = text.strip().split(',')
        new_values = []
        for el in values_str:
            try:
                val = float(el)
                if val <= x0_MIN_VALUE or val > x0_MAX_VALUE:
                    val = 0.0
                new_values.append(val)
            except:
                new_values.append(0.0)

        new_elems_str = []
        for indx, key in enumerate(list(self.symbol_dict.keys())):
            if indx < len(new_values):
                self.symbol_dict[key] = new_values[indx]
            else:
                self.symbol_dict[key] = 0.0
            new_elems_str.append(str(new_values[indx]))
        self.lineEdit_x0.setText(', '.join(new_elems_str))
        self.data_correctness_dict['x0'] = True
        self.unlock_button_rozpocznij_opt()


    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setEnabled(True)
        mainWindow.resize(840, 757)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.label_funkcjacelu = QtWidgets.QLabel(self.centralwidget)
        self.label_funkcjacelu.setGeometry(QtCore.QRect(20, 0, 211, 21))
        self.label_funkcjacelu.setObjectName("label_funkcjacelu")
        self.label_metoda_opt = QtWidgets.QLabel(self.centralwidget)
        self.label_metoda_opt.setGeometry(QtCore.QRect(20, 180, 141, 41))
        self.label_metoda_opt.setObjectName("label_metoda_opt")
        self.label_fx = QtWidgets.QLabel(self.centralwidget)
        self.label_fx.setGeometry(QtCore.QRect(10, 30, 51, 41))
        self.label_fx.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_fx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_fx.setObjectName("label_fx")
        self.comboBox_metoda_opt = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_metoda_opt.setGeometry(QtCore.QRect(20, 220, 271, 41))
        self.comboBox_metoda_opt.setObjectName("comboBox_metoda_opt")
        self.comboBox_metoda_opt.addItem("")
        self.checkBox_stop2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_stop2.setGeometry(QtCore.QRect(20, 350, 31, 41))
        self.checkBox_stop2.setObjectName("checkBox_stop2")
        self.label_stop = QtWidgets.QLabel(self.centralwidget)
        self.label_stop.setGeometry(QtCore.QRect(20, 260, 111, 41))
        self.label_stop.setObjectName("label_stop")
        self.checkBox_stop1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_stop1.setGeometry(QtCore.QRect(20, 300, 31, 41))
        self.checkBox_stop1.setObjectName("checkBox_stop1")
        self.checkBox_stop3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_stop3.setGeometry(QtCore.QRect(20, 400, 31, 41))
        self.checkBox_stop3.setObjectName("checkBox_stop3")
        self.label_esp1 = QtWidgets.QLabel(self.centralwidget)
        self.label_esp1.setGeometry(QtCore.QRect(170, 300, 61, 41))
        self.label_esp1.setObjectName("label_esp1")
        self.label_eps2 = QtWidgets.QLabel(self.centralwidget)
        self.label_eps2.setGeometry(QtCore.QRect(170, 350, 61, 41))
        self.label_eps2.setObjectName("label_eps2")
        self.label_eps3 = QtWidgets.QLabel(self.centralwidget)
        self.label_eps3.setGeometry(QtCore.QRect(170, 400, 61, 41))
        self.label_eps3.setObjectName("label_eps3")
        self.lineEdit_eps1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_eps1.setEnabled(False)
        self.lineEdit_eps1.setGeometry(QtCore.QRect(220, 300, 141, 41))
        self.lineEdit_eps1.setDragEnabled(False)
        self.lineEdit_eps1.setObjectName("lineEdit_eps1")
        self.lineEdit_eps2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_eps2.setEnabled(False)
        self.lineEdit_eps2.setGeometry(QtCore.QRect(220, 350, 141, 41))
        self.lineEdit_eps2.setObjectName("lineEdit_eps2")
        self.lineEdit_eps3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_eps3.setEnabled(False)
        self.lineEdit_eps3.setGeometry(QtCore.QRect(220, 400, 141, 41))
        self.lineEdit_eps3.setObjectName("lineEdit_eps3")
        self.checkBox_stop4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_stop4.setGeometry(QtCore.QRect(20, 450, 31, 51))
        self.checkBox_stop4.setObjectName("checkBox_stop4")
        self.label_eps4 = QtWidgets.QLabel(self.centralwidget)
        self.label_eps4.setGeometry(QtCore.QRect(170, 450, 61, 41))
        self.label_eps4.setObjectName("label_eps4")
        self.lineEdit_eps4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_eps4.setEnabled(False)
        self.lineEdit_eps4.setGeometry(QtCore.QRect(220, 450, 141, 41))
        self.lineEdit_eps4.setObjectName("lineEdit_eps4")
        self.label_metoda_kierunek = QtWidgets.QLabel(self.centralwidget)
        self.label_metoda_kierunek.setGeometry(QtCore.QRect(410, 180, 361, 41))
        self.label_metoda_kierunek.setObjectName("label_metoda_kierunek")
        self.comboBox_metoda_kierunek = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_metoda_kierunek.setGeometry(QtCore.QRect(410, 220, 361, 41))
        self.comboBox_metoda_kierunek.setObjectName("comboBox_metoda_kierunek")
        self.comboBox_metoda_kierunek.addItem("")
        self.label_alfa_eq = QtWidgets.QLabel(self.centralwidget)
        self.label_alfa_eq.setGeometry(QtCore.QRect(520, 280, 31, 41))
        self.label_alfa_eq.setObjectName("label_alfa_eq")
        self.lineEdit_alfa0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_alfa0.setGeometry(QtCore.QRect(560, 280, 211, 41))
        self.lineEdit_alfa0.setObjectName("lineEdit_alfa0")
        self.checkBox_stopk2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_stopk2.setEnabled(False)
        self.checkBox_stopk2.setGeometry(QtCore.QRect(420, 430, 81, 41))
        self.checkBox_stopk2.setObjectName("checkBox_stopk2")
        self.label_eps_k2 = QtWidgets.QLabel(self.centralwidget)
        self.label_eps_k2.setGeometry(QtCore.QRect(550, 430, 51, 41))
        self.label_eps_k2.setObjectName("label_eps_k2")
        self.checkBox_stopk1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_stopk1.setEnabled(False)
        self.checkBox_stopk1.setGeometry(QtCore.QRect(420, 380, 91, 41))
        self.checkBox_stopk1.setObjectName("checkBox_stopk1")
        self.label_eps_k1 = QtWidgets.QLabel(self.centralwidget)
        self.label_eps_k1.setGeometry(QtCore.QRect(550, 380, 51, 41))
        self.label_eps_k1.setObjectName("label_eps_k1")
        self.checkBox_inne_kryteria = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_inne_kryteria.setGeometry(QtCore.QRect(400, 330, 31, 41))
        self.checkBox_inne_kryteria.setText("")
        self.checkBox_inne_kryteria.setObjectName("checkBox_inne_kryteria")
        self.lineEdit_epsk1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_epsk1.setEnabled(False)
        self.lineEdit_epsk1.setGeometry(QtCore.QRect(600, 380, 171, 41))
        self.lineEdit_epsk1.setObjectName("lineEdit_epsk1")
        self.lineEdit_epsk2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_epsk2.setEnabled(False)
        self.lineEdit_epsk2.setGeometry(QtCore.QRect(600, 430, 171, 41))
        self.lineEdit_epsk2.setObjectName("lineEdit_epsk2")
        self.pushButton_rozpocznij_opt = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_rozpocznij_opt.setGeometry(QtCore.QRect(20, 520, 341, 41))
        self.pushButton_rozpocznij_opt.setObjectName("pushButton_rozpocznij_opt")
        self.pushButton_rozpocznij_opt.setEnabled (False)
        self.label_stopk2 = QtWidgets.QLabel(self.centralwidget)
        self.label_stopk2.setGeometry(QtCore.QRect(460, 430, 91, 41))
        self.label_stopk2.setObjectName("label_stopk2")
        self.label_stopk1 = QtWidgets.QLabel(self.centralwidget)
        self.label_stopk1.setGeometry(QtCore.QRect(460, 380, 91, 41))
        self.label_stopk1.setObjectName("label_stopk1")
        self.label_alfa0 = QtWidgets.QLabel(self.centralwidget)
        self.label_alfa0.setGeometry(QtCore.QRect(460, 280, 41, 41))
        self.label_alfa0.setObjectName("label_alfa0")
        self.label_stop3 = QtWidgets.QLabel(self.centralwidget)
        self.label_stop3.setGeometry(QtCore.QRect(70, 400, 111, 41))
        self.label_stop3.setObjectName("label_stop3")
        self.label_stop2 = QtWidgets.QLabel(self.centralwidget)
        self.label_stop2.setEnabled(True)
        self.label_stop2.setGeometry(QtCore.QRect(70, 350, 121, 41))
        self.label_stop2.setObjectName("label_stop2")
        self.label_opt_w_kierunku = QtWidgets.QLabel(self.centralwidget)
        self.label_opt_w_kierunku.setGeometry(QtCore.QRect(420, 330, 391, 41))
        self.label_opt_w_kierunku.setObjectName("label_opt_w_kierunku")
        self.comboBox_fx = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_fx.setGeometry(QtCore.QRect(70, 20, 741, 61))
        self.comboBox_fx.setEditable(True)
        self.comboBox_fx.setObjectName("comboBox_fx")
        self.comboBox_fx.addItem("")
        self.comboBox_fx.addItem("")
        self.comboBox_fx.addItem("")
        self.comboBox_fx.addItem("")
        self.comboBox_fx.addItem("")
        self.comboBox_fx.addItem("")
        self.comboBox_fx.addItem ("")
        self.pushButton_wyswietl_kroki = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_wyswietl_kroki.setEnabled(False)
        self.pushButton_wyswietl_kroki.setGeometry(QtCore.QRect(410, 520, 361, 41))
        self.pushButton_wyswietl_kroki.setObjectName("pushButton_wyswietl_kroki")
        self.label_x = QtWidgets.QLabel(self.centralwidget)
        self.label_x.setGeometry(QtCore.QRect(30, 90, 31, 41))
        self.label_x.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_x.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_x.setObjectName("label_x")
        self.textBrowser_x = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_x.setEnabled(False)
        self.textBrowser_x.setGeometry(QtCore.QRect(70, 90, 741, 41))
        self.textBrowser_x.setObjectName("textBrowser_x")
        self.label_x0_startbracket = QtWidgets.QLabel(self.centralwidget)
        self.label_x0_startbracket.setGeometry(QtCore.QRect(70, 140, 41, 41))
        self.label_x0_startbracket.setObjectName("label_x0_startbracket")
        self.lineEdit_x0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_x0.setGeometry(QtCore.QRect(80, 140, 701, 41))
        self.lineEdit_x0.setObjectName("lineEdit_x0")
        self.label_x0_endbracket = QtWidgets.QLabel(self.centralwidget)
        self.label_x0_endbracket.setGeometry(QtCore.QRect(790, 140, 31, 41))
        self.label_x0_endbracket.setObjectName("label_x0_endbracket")
        self.label_f_opt = QtWidgets.QLabel(self.centralwidget)
        self.label_f_opt.setGeometry(QtCore.QRect(10, 660, 51, 41))
        self.label_f_opt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_f_opt.setObjectName("label_f_opt")
        self.textBrowser_x_opt = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_x_opt.setEnabled(False)
        self.textBrowser_x_opt.setGeometry(QtCore.QRect(70, 610, 701, 41))
        self.textBrowser_x_opt.setObjectName("textBrowser_x_opt")
        self.label_x_opt = QtWidgets.QLabel(self.centralwidget)
        self.label_x_opt.setGeometry(QtCore.QRect(20, 610, 41, 41))
        self.label_x_opt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_x_opt.setObjectName("label_x_opt")
        self.label_x0 = QtWidgets.QLabel(self.centralwidget)
        self.label_x0.setGeometry(QtCore.QRect(30, 140, 31, 41))
        self.label_x0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_x0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_x0.setObjectName("label_x0")
        self.pushButton_zamknij_aplikacje = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_zamknij_aplikacje.setGeometry(QtCore.QRect(440, 660, 331, 41))
        self.pushButton_zamknij_aplikacje.setObjectName("pushButton_zamknij_aplikacje")
        self.textBrowser_f_opt = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_f_opt.setEnabled(False)
        self.textBrowser_f_opt.setGeometry(QtCore.QRect(70, 660, 331, 41))
        self.textBrowser_f_opt.setObjectName("textBrowser_f_opt")
        self.label_stop_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_stop_2.setGeometry(QtCore.QRect(20, 570, 201, 41))
        self.label_stop_2.setObjectName("label_stop_2")
        self.label_stop4 = QtWidgets.QLabel(self.centralwidget)
        self.label_stop4.setGeometry(QtCore.QRect(70, 460, 71, 31))
        self.label_stop4.setObjectName("label_stop4")
        self.label_stop1 = QtWidgets.QLabel(self.centralwidget)
        self.label_stop1.setGeometry(QtCore.QRect(60, 300, 111, 41))
        self.label_stop1.setObjectName("label_stop1")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        self.checkBox_stop1.toggled['bool'].connect(self.lineEdit_eps1.setEnabled)
        self.checkBox_stop2.toggled['bool'].connect(self.lineEdit_eps2.setEnabled)
        self.checkBox_stop3.toggled['bool'].connect(self.lineEdit_eps3.setEnabled)
        self.checkBox_stop4.toggled['bool'].connect(self.lineEdit_eps4.setEnabled)
        self.checkBox_inne_kryteria.toggled['bool'].connect(self.checkBox_stopk1.setEnabled)
        self.checkBox_inne_kryteria.toggled['bool'].connect(self.checkBox_stopk2.setEnabled)
        self.checkBox_stopk1.toggled['bool'].connect(self.lineEdit_epsk1.setEnabled)
        self.checkBox_stopk2.toggled['bool'].connect(self.lineEdit_epsk2.setEnabled)
        self.pushButton_rozpocznij_opt.clicked['bool'].connect(self.pushButton_wyswietl_kroki.setEnabled)
        self.pushButton_zamknij_aplikacje.clicked.connect(mainWindow.close)
        self.checkBox_inne_kryteria.toggled['bool'].connect(self.checkBox_stopk1.setChecked)
        self.checkBox_inne_kryteria.toggled['bool'].connect(self.checkBox_stopk2.setChecked)
        self.checkBox_stop1.toggled['bool'].connect(self.check_stop_checkboxes)
        self.checkBox_stop2.toggled['bool'].connect(self.check_stop_checkboxes)
        self.checkBox_stop3.toggled['bool'].connect(self.check_stop_checkboxes)
        self.checkBox_stop4.toggled['bool'].connect(self.check_stop_checkboxes)
        self.checkBox_stopk1.toggled['bool'].connect(self.lock_checkBox_inne_kryteria)
        self.checkBox_stopk2.toggled['bool'].connect(self.lock_checkBox_inne_kryteria)

        self.lineEdit_eps1.editingFinished.connect(self.checkTextCorrectness_lineEdit_eps1)
        self.lineEdit_eps2.editingFinished.connect(self.checkTextCorrectness_lineEdit_eps2)
        self.lineEdit_eps3.editingFinished.connect(self.checkTextCorrectness_lineEdit_eps3)
        self.lineEdit_eps4.editingFinished.connect(self.checkTextCorrectness_lineEdit_eps4)
        self.lineEdit_epsk1.editingFinished.connect(self.checkTextCorrectness_lineEdit_epsk1)
        self.lineEdit_epsk2.editingFinished.connect(self.checkTextCorrectness_lineEdit_epsk2)
        self.lineEdit_alfa0.editingFinished.connect(self.checkTextCorrectness_lineEdit_alfa0)
        self.lineEdit_x0.editingFinished.connect(self.checkTextCorrectness_lineEdit_x0)
        self.comboBox_fx.currentIndexChanged['QString'].connect(self.comboBox_fx_TextChanged)

        self.pushButton_rozpocznij_opt.clicked.connect(self.startOptimization)
        self.pushButton_wyswietl_kroki.clicked.connect (self.wyswietl_kroki)



        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Optymalizacja metodą Fletchera-Reeves\'a"))
        self.label_funkcjacelu.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Funkcja celu</span></p></body></html>"))
        self.label_metoda_opt.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Metoda optymalizacji</span></p></body></html>"))
        self.label_fx.setText(_translate("mainWindow", "<html><head/><body><p>f(x)=</p></body></html>"))
        self.comboBox_metoda_opt.setItemText(0, _translate("mainWindow", "Metoda gradientu sprzęzonego Fletchera-Reeves\'a"))
        self.checkBox_stop2.setText(_translate("mainWindow", "2."))
        self.label_stop.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Kryteria stopu</span></p></body></html>"))
        self.checkBox_stop1.setText(_translate("mainWindow", "1."))
        self.checkBox_stop3.setText(_translate("mainWindow", "3."))
        self.label_esp1.setText(_translate("mainWindow", "<html><head/><body><p>≤ ε<span style=\" vertical-align:sub;\">1 </span>=</p></body></html>"))
        self.label_eps2.setText(_translate("mainWindow", "<html><head/><body><p>≤ ε<span style=\" vertical-align:sub;\">2 </span>=</p></body></html>"))
        self.label_eps3.setText(_translate("mainWindow", "<html><head/><body><p>≤ ε<span style=\" vertical-align:sub;\">3 </span>=</p></body></html>"))
        self.lineEdit_eps1.setText(_translate("mainWindow", "0.001"))
        self.lineEdit_eps2.setText(_translate("mainWindow", "0.001"))
        self.lineEdit_eps3.setText(_translate("mainWindow", "0.001"))
        self.checkBox_stop4.setText(_translate("mainWindow", "4. "))
        self.label_eps4.setText(_translate("mainWindow", "<html><head/><body><p>≥ L<span style=\" vertical-align:sub;\">max </span>=</p></body></html>"))
        self.lineEdit_eps4.setText(_translate("mainWindow", "100"))
        self.label_metoda_kierunek.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Metoda optymalizacji w kierunku </span></p></body></html>"))
        self.comboBox_metoda_kierunek.setItemText(0, _translate("mainWindow", "Interpolacja sześcienna"))
        self.label_alfa_eq.setText(_translate("mainWindow", "="))
        self.lineEdit_alfa0.setText(_translate("mainWindow", "1.0"))
        self.checkBox_stopk2.setText(_translate("mainWindow", "2. "))
        self.label_eps_k2.setText(_translate("mainWindow", "<html><head/><body><p>≤ ε<span style=\" vertical-align:sub;\">k2 </span>=</p></body></html>"))
        self.checkBox_stopk1.setText(_translate("mainWindow", "1. "))
        self.label_eps_k1.setText(_translate("mainWindow", "<html><head/><body><p>≤ ε<span style=\" vertical-align:sub;\">k1 </span>=</p></body></html>"))
        self.lineEdit_epsk1.setText(_translate("mainWindow", "0.001"))
        self.lineEdit_epsk2.setText(_translate("mainWindow", "0.001"))
        self.pushButton_rozpocznij_opt.setText(_translate("mainWindow", "Rozpocznij optymalizację"))
        self.label_stopk2.setText(_translate("mainWindow", "<html><head/><body><p>|f(x<span style=\" vertical-align:sub;\">n</span>)-f(x<span style=\" vertical-align:sub;\">n-1</span>)|</p></body></html>"))
        self.label_stopk1.setText(_translate("mainWindow", "||x<sub>n</sub>-x<sub>n-1</sub>||"))
        self.label_alfa0.setText(_translate("mainWindow", "<html><head/><body><p>α<span style=\" vertical-align:sub;\">0</span></p></body></html>"))
        self.label_stop3.setText(_translate("mainWindow", "<html><head/><body><p>|f(x<span style=\" vertical-align:sub;\">n</span>)-f(x<span style=\" vertical-align:sub;\">n-1</span>)|</p></body></html>"))
        self.label_stop2.setText(_translate("mainWindow", "||x<sub>n</sub>-x<sub>n-1</sub>||"))
        self.label_opt_w_kierunku.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Oddzielne kryteria stopu dla metody optymalizacji w kierunku</span></p></body></html>"))
        self.comboBox_fx.setItemText (0, _translate ("mainWindow", ""))
        self.comboBox_fx.setItemText (1, _translate ("mainWindow", "(x1-2)^2+(x2+1)^2"))
        self.comboBox_fx.setItemText(2, _translate("mainWindow", "x1^4+x2^4-0.62*x1^2-0.62*x2^2"))
        self.comboBox_fx.setItemText(3, _translate("mainWindow", "100*(x2-x1^2)^2+(1-x1)^2"))
        self.comboBox_fx.setItemText(4, _translate("mainWindow", "(x1-x2+x3)^2+(-x1+x2+x3)^2+(x1+x2-x3)^2"))
        self.comboBox_fx.setItemText(5, _translate("mainWindow", "(1+(x1+x2+1)^2*(19-14*x1+3*x1^2-14*x2+6*x1*x2 +3*x2^2))*(30+(2*x1-3*x2)^2(18-32*x1+12*x1^2+48*x2-36*x1*x2+27*x2^2))"))
        self.comboBox_fx.setItemText(6, _translate ("mainWindow", "(x1-2)^2+(x2-1)^2"))
        self.pushButton_wyswietl_kroki.setText(_translate("mainWindow", "Wyświetl kroki optymalizacji "))
        self.label_x.setText(_translate("mainWindow", "<html><head/><body><p>x = </p></body></html>"))
        self.textBrowser_x.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">[]</span></p></body></html>"))
        self.label_x0_startbracket.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">[</span></p></body></html>"))
        self.lineEdit_x0.setText(_translate("mainWindow", ""))
        self.label_x0_endbracket.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">]</span></p></body></html>"))
        self.label_f_opt.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">f(x*)=</span></p></body></html>"))
        self.textBrowser_x_opt.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">[]</span></p></body></html>"))
        self.label_x_opt.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">x* = </span></p></body></html>"))
        self.label_x0.setText(_translate("mainWindow", "<html><head/><body><p>x<span style=\" vertical-align:sub;\">0</span> = </p></body></html>"))
        self.pushButton_zamknij_aplikacje.setText(_translate("mainWindow", "Zamknij aplikację"))
        self.textBrowser_f_opt.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.label_stop_2.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Znalezione rozwiązanie optymalne</span></p></body></html>"))
        self.label_stop4.setText(_translate("mainWindow", "L"))
        self.label_stop1.setText(_translate("mainWindow", " <∇f(x),∇f(x)>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
