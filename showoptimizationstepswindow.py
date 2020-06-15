# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showoptimizationstepswindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import math
import numpy as np
import matplotlib
import constants_file
import cexprtk

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)




class Ui_Dialog(object):
    def uzupelnij_listWidget_optymalizacja_kierunek(self):
        pass
    #todo

    def uzupelnij_listWidget_optymalizacja(self):
        with open("optimization.txt") as file:
            for line in file:
                self.listWidget_optymalizacja.addItem(line)

    def uzupelnij_comboBoxes(self):
        with open("optimization.txt") as file:
            file.readline()
            line2 = file.readline().strip()
        for elem in line2.split(","):
            self.comboBox_zmienna1.addItem (elem)
            self.comboBox_zmienna2.addItem (elem)

    def sprawdz_lineEdit_os_pion(self):
        default_dolna = -1.0
        default_gorna = 1.0
        text_dolna = self.lineEdit_gdolna_pion.text()
        text_gorna = self.lineEdit_ggorna_pion.text()
        try:
            num_dolna = float(text_dolna)
            num_gorna = float(text_gorna)

            if math.isnan(num_dolna) or math.isinf(num_dolna) \
                    or math.isnan(num_gorna) or math.isinf(num_gorna):
                num_dolna = default_dolna
                num_gorna = default_gorna

            if num_dolna > num_gorna:
                num_dolna = num_gorna-10**(-8)

            self.lineEdit_gdolna_pion.setText(str(num_dolna))
            self.lineEdit_ggorna_pion.setText(str(num_gorna))
        except:
            self.lineEdit_gdolna_pion.setText(str(default_dolna))
            self.lineEdit_ggorna_pion.setText(str(default_gorna))

    def sprawdz_lineEdit_os_poziom(self):
        default_dolna = -1.0
        default_gorna = 1.0
        text_dolna = self.lineEdit_gdolna_poziom.text ()
        text_gorna = self.lineEdit_ggorna_poziom.text ()
        try:
            num_dolna = float (text_dolna)
            num_gorna = float (text_gorna)

            if math.isnan (num_dolna) or math.isinf (num_dolna) \
                    or math.isnan (num_gorna) or math.isinf (num_gorna):
                num_dolna = default_dolna
                num_gorna = default_gorna

            if num_dolna > num_gorna:
                num_dolna = num_gorna - 10 ** (-8)

            self.lineEdit_gdolna_poziom.setText (str (num_dolna))
            self.lineEdit_ggorna_poziom.setText (str (num_gorna))
        except:
            self.lineEdit_gdolna_poziom.setText (str (default_dolna))
            self.lineEdit_ggorna_poziom.setText (str (default_gorna))

    def sprawdz_lineEdit_rozdzielczosc_siatki(self):
        default_val = 100
        try:
            val = int(self.lineEdit_rozdzielczosc_siatki.text())
            if val<0 or 10000 < val:
                val = default_val
            self.lineEdit_rozdzielczosc_siatki.setText (str(val))
        except:
            self.lineEdit_rozdzielczosc_siatki.setText (str(default_val))

    def rysujSiatke(self):
        poziom_dolna = float(self.lineEdit_gdolna_poziom.text())
        poziom_gorna =float(self.lineEdit_ggorna_poziom.text())
        pion_dolna = float(self.lineEdit_gdolna_pion.text())
        pion_gorna = float(self.lineEdit_ggorna_pion.text())
        l_probek = int(self.lineEdit_rozdzielczosc_siatki.text())

        X=np.linspace(poziom_dolna,poziom_gorna,l_probek)
        Y=np.linspace(pion_dolna,pion_gorna,l_probek)

        expr_text = self.listWidget_optymalizacja.item(0).text()
        symbols_text = self.listWidget_optymalizacja.item(1).text().strip()
        dict = {}

        for i, elem in enumerate(symbols_text.split (","),0):
            dict[elem] = 0.0
            if len(self.listWidget_optymalizacja.selectedItems())!=0:
                selected_row = self.listWidget_optymalizacja.row(self.listWidget_optymalizacja.selectedItems()[0])
                if selected_row>1 and selected_row < self.listWidget_optymalizacja.count()-1:
                    text = self.listWidget_optymalizacja.selectedItems()[0].text()
                    values = text.split(',')[1].split('[')[1].split (']')[0].split()
                    try:
                        dict[elem] = float(values[i])
                    except:
                        print("Error: rysujSiatke; Błąd przypisania wartości pozostałych zmiennych przy generowaniu przekroju")
            else:
                text = self.listWidget_optymalizacja.item( self.listWidget_optymalizacja.count()-2).text ()
                values = text.split (',')[1].split ('[')[1].split (']')[0].split ()
                try:
                    dict[elem] = float (values[i])
                except:
                    print (
                        "Error: rysujSiatke; Błąd przypisania wartości pozostałych zmiennych przy generowaniu przekroju")

        st = cexprtk.Symbol_Table(dict,constants_file.m_constants,add_constants=True)
        expr = cexprtk.Expression(expr_text,st)

        text_pozostale_zmienne = ""
        for key, value in dict.items():
            if key != self.comboBox_zmienna1.currentText() and key != self.comboBox_zmienna2.currentText():
                text_pozostale_zmienne = text_pozostale_zmienne+key+"="+str(value)+", "
        self.lineEdit_pozostale_zmienne.setText(text_pozostale_zmienne)

        if self.comboBox_zmienna1.currentText() == self.comboBox_zmienna2.currentText(): #wykres 1d
            c=np.zeros((l_probek,))
            for i in range (0, len (X)):
                st.variables[self.comboBox_zmienna1.currentText ()] = X[i]
                c[i]=expr()
            self.sc.axes.cla ()
            self.sc.axes.plot(X, c)
            self.sc.axes.set_xlabel(self.comboBox_zmienna1.currentText())
            self.sc.axes.set_ylabel("f(x)")
        else: #wykres 2d
            c=np.zeros((l_probek,l_probek))
            for i in range (0, l_probek):
                for j in range (0, l_probek):
                    st.variables[self.comboBox_zmienna1.currentText()]=X[i]
                    st.variables[self.comboBox_zmienna2.currentText()]=Y[j]
                    c[j,i]=expr()
            self.sc.axes.cla()
            self.sc.axes.contourf(X,Y,c)
            self.rysujWszystkieKroki(dict)
            self.sc.axes.set_xlim(poziom_dolna,poziom_gorna)
            self.sc.axes.set_ylim(pion_dolna,pion_gorna)
            self.sc.axes.set_xlabel (self.comboBox_zmienna1.currentText ())
            self.sc.axes.set_ylabel (self.comboBox_zmienna2.currentText())
        self.sc.draw ()

    def rysujWszystkieKroki(self,dict):
        p_x=0.0
        p_y=0.0
        text = self.listWidget_optymalizacja.item(2).text ().split (',')[1]
        values = text.split ('[')[1].split (']')[0].split ()
        p_x_pre = float (values[list(dict.keys()).index (self.comboBox_zmienna1.currentText())])
        p_y_pre = float (values[list(dict.keys()).index (self.comboBox_zmienna2.currentText())])
        self.sc.axes.scatter (p_x_pre, p_y_pre, marker='o', c='m', s=20)
        for i in range (3,self.listWidget_optymalizacja.count()-1):
            text = self.listWidget_optymalizacja.item(i).text().split(',')[1]
            values = text.split('[')[1].split(']')[0].split()
            p_x = float(values[list(dict.keys()).index(self.comboBox_zmienna1.currentText())])
            p_y = float(values[list(dict.keys()).index(self.comboBox_zmienna2.currentText())])
            self.sc.axes.scatter(p_x,p_y,marker='o',c='k',s=15)
            self.sc.axes.plot(np.array([p_x,p_x_pre]),np.array([p_y,p_y_pre]),c='0.75',ms=15)
            p_x_pre, p_y_pre = (p_x,p_y)
        self.sc.axes.scatter (p_x, p_y, marker='o', c='r', s=20)


    def setupUi(self, Dialog):
        Dialog.setObjectName ("Dialog")
        Dialog.resize(1310, 615)
        self.lineEdit_ggorna_pion = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_ggorna_pion.setGeometry (QtCore.QRect(1150, 230, 91, 20))
        self.lineEdit_ggorna_pion.setObjectName ("lineEdit_ggorna_pion")
        self.label_zmienne = QtWidgets.QLabel (Dialog)
        self.label_zmienne.setGeometry (QtCore.QRect(980, 140, 100, 16))
        self.label_zmienne.setObjectName ("label_zmienne")
        self.label_granica_gorna = QtWidgets.QLabel (Dialog)
        self.label_granica_gorna.setGeometry (QtCore.QRect(1150, 140, 100, 16))
        self.label_granica_gorna.setObjectName ("label_granica_gorna")
        self.pushButton_wyswietl_siatke = QtWidgets.QPushButton (Dialog)
        self.pushButton_wyswietl_siatke.setGeometry (QtCore.QRect(980, 280, 311, 51))
        self.pushButton_wyswietl_siatke.setObjectName ("pushButton_wyswietl_siatke")
        self.label_os_pionowa = QtWidgets.QLabel (Dialog)
        self.label_os_pionowa.setGeometry (QtCore.QRect(980, 190, 61, 16))
        self.label_os_pionowa.setObjectName ("label_os_pionowa")
        self.comboBox_zmienna2 = QtWidgets.QComboBox (Dialog)
        self.comboBox_zmienna2.setGeometry (QtCore.QRect(980, 230, 51, 21))
        self.comboBox_zmienna2.setObjectName ("comboBox_zmienna2")
        self.lineEdit_ggorna_poziom = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_ggorna_poziom.setGeometry (QtCore.QRect(1150, 160, 91, 20))
        self.lineEdit_ggorna_poziom.setObjectName ("lineEdit_ggorna_poziom")
        self.lineEdit_gdolna_pion = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_gdolna_pion.setGeometry (QtCore.QRect(1050, 230, 91, 20))
        self.lineEdit_gdolna_pion.setObjectName ("lineEdit_gdolna_pion")
        self.label_os_pozioma = QtWidgets.QLabel (Dialog)
        self.label_os_pozioma.setGeometry (QtCore.QRect(980, 120, 61, 16))
        self.label_os_pozioma.setObjectName ("label_os_pozioma")
        self.lineEdit_gdolna_poziom = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_gdolna_poziom.setGeometry (QtCore.QRect(1050, 160, 91, 20))
        self.lineEdit_gdolna_poziom.setObjectName ("lineEdit_gdolna_poziom")
        self.widget_siatka = QtWidgets.QWidget (Dialog)
        self.widget_siatka.setGeometry (QtCore.QRect(550, 35, 436, 321))
        self.widget_siatka.setObjectName ("widget_siatka")
        self.comboBox_zmienna1 = QtWidgets.QComboBox (Dialog)
        self.comboBox_zmienna1.setGeometry (QtCore.QRect(980, 160, 51, 21))
        self.comboBox_zmienna1.setObjectName ("comboBox_zmienna1")
        self.label_granice_dolna = QtWidgets.QLabel (Dialog)
        self.label_granice_dolna.setGeometry (QtCore.QRect(1050, 140, 100, 16))
        self.label_granice_dolna.setObjectName ("label_granice_dolna")
        self.pushButton_wroc = QtWidgets.QPushButton (Dialog)
        self.pushButton_wroc.setGeometry (QtCore.QRect(980, 550, 311, 51))
        self.pushButton_wroc.setObjectName ("pushButton_wroc")
        self.label_kroki_opt = QtWidgets.QLabel (Dialog)
        self.label_kroki_opt.setGeometry (QtCore.QRect(20, 20, 191, 16))
        self.label_kroki_opt.setObjectName ("label_kroki_opt")
        self.label_przekroj = QtWidgets.QLabel (Dialog)
        self.label_przekroj.setGeometry (QtCore.QRect(640, 20, 201, 16))
        self.label_przekroj.setObjectName ("label_przekroj")
        self.label_rozdzielczosc_siatki = QtWidgets.QLabel (Dialog)
        self.label_rozdzielczosc_siatki.setGeometry (QtCore.QRect(980, 91, 331, 16))
        self.label_rozdzielczosc_siatki.setObjectName ("label_rozdzielczosc_siatki")
        self.lineEdit_rozdzielczosc_siatki = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_rozdzielczosc_siatki.setGeometry (QtCore.QRect(1210, 90, 81, 21))
        self.lineEdit_rozdzielczosc_siatki.setObjectName ("lineEdit_rozdzielczosc_siatki")
        self.label_kroki_kierunek = QtWidgets.QLabel (Dialog)
        self.label_kroki_kierunek.setGeometry (QtCore.QRect(20, 340, 191, 16))
        self.label_kroki_kierunek.setObjectName ("label_kroki_kierunek")
        self.listWidget_optymalizacja = QtWidgets.QListWidget (Dialog)
        self.listWidget_optymalizacja.setGeometry (QtCore.QRect(20, 40, 521, 291))
        self.listWidget_optymalizacja.setObjectName ("listWidget_optymalizacja")
        self.listWidget_optymalizacja_kierunek = QtWidgets.QListWidget (Dialog)
        self.listWidget_optymalizacja_kierunek.setEnabled (False)
        self.listWidget_optymalizacja_kierunek.setGeometry (QtCore.QRect (20, 370, 521, 231))
        self.listWidget_optymalizacja_kierunek.setObjectName ("listWidget_optymalizacja_kierunek")

        self.lineEdit_pozostale_zmienne = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_pozostale_zmienne.setGeometry (QtCore.QRect(980, 60, 311, 21))
        self.lineEdit_pozostale_zmienne.setObjectName ("lineEdit_wartosci_zmiennych")
        self.lineEdit_pozostale_zmienne.setEnabled(False)
        self.label_pozostale_zmienne = QtWidgets.QLabel (Dialog)
        self.label_pozostale_zmienne.setGeometry (QtCore.QRect (980, 40, 331, 16))
        self.label_pozostale_zmienne.setObjectName ("label_pozostale_zmienne")

        self.widget_siatka_2 = QtWidgets.QWidget(Dialog)
        self.widget_siatka_2.setGeometry(QtCore.QRect(550, 360, 436, 256))
        self.widget_siatka_2.setObjectName("widget_siatka_2")

        self.pushButton_wyswietl_siatke_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_wyswietl_siatke_2.setGeometry(QtCore.QRect(980, 490, 311, 51))
        self.pushButton_wyswietl_siatke_2.setObjectName("pushButton_wyswietl_siatke_2")

        self.lineEdit_a_0 = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_a_0.setEnabled (False)
        self.lineEdit_a_0.setGeometry (QtCore.QRect (980, 390, 301, 20))
        self.lineEdit_a_0.setObjectName ("lineEdit_a_0")
        self.label_a = QtWidgets.QLabel (Dialog)
        self.label_a.setGeometry (QtCore.QRect (980, 360, 161, 31))
        self.label_a.setObjectName ("label_a")
        self.label_przekroj_2 = QtWidgets.QLabel (Dialog)
        self.label_przekroj_2.setGeometry (QtCore.QRect (640, 350, 201, 16))
        self.label_przekroj_2.setObjectName ("label_przekroj_2")
        self.lineEdit_a_a0 = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_a_a0.setEnabled (False)
        self.lineEdit_a_a0.setGeometry (QtCore.QRect (980, 420, 301, 20))
        self.lineEdit_a_a0.setObjectName ("lineEdit_a_a0")
        self.lineEdit_a_aopt = QtWidgets.QLineEdit (Dialog)
        self.lineEdit_a_aopt.setEnabled (False)
        self.lineEdit_a_aopt.setGeometry (QtCore.QRect (980, 450, 301, 20))
        self.lineEdit_a_aopt.setObjectName ("lineEdit_a_aopt")

        self.pushButton_wyswietl_siatke.clicked.connect(self.rysujSiatke)

        self.lineEdit_gdolna_pion.editingFinished.connect(self.sprawdz_lineEdit_os_pion)
        self.lineEdit_ggorna_pion.editingFinished.connect(self.sprawdz_lineEdit_os_pion)
        self.lineEdit_gdolna_poziom.editingFinished.connect (self.sprawdz_lineEdit_os_poziom)
        self.lineEdit_ggorna_poziom.editingFinished.connect (self.sprawdz_lineEdit_os_poziom)

        self.lineEdit_rozdzielczosc_siatki.editingFinished.connect(self.sprawdz_lineEdit_rozdzielczosc_siatki)


        self.uzupelnij_listWidget_optymalizacja()
        self.uzupelnij_listWidget_optymalizacja_kierunek()
        self.uzupelnij_comboBoxes()

        self.sc = MplCanvas(self, width=10, height=10, dpi=70)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.sc)
        self.widget_siatka.setLayout (self.layout)

        self.sc2 = MplCanvas (self, width=3, height=3, dpi=80)

        self.layout2 = QtWidgets.QVBoxLayout ()
        self.layout2.addWidget (self.sc2)
        self.widget_siatka_2.setLayout (self.layout2)

        self.retranslateUi(Dialog)
        self.pushButton_wroc.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.label_zmienne.setText(_translate("Dialog", "Zmienne"))
        self.label_granica_gorna.setText(_translate("Dialog", "Granica górna"))
        self.pushButton_wyswietl_siatke.setText(_translate("Dialog", "Wyświetl siatkę"))
        self.label_os_pionowa.setText(_translate("Dialog", "Oś pionowa"))
        self.lineEdit_ggorna_poziom.setText(_translate("Dialog", "1.0"))
        self.lineEdit_gdolna_poziom.setText(_translate("Dialog", "-1.0"))
        self.lineEdit_ggorna_pion.setText (_translate ("Dialog", "1.0"))
        self.lineEdit_gdolna_pion.setText(_translate("Dialog", "-1.0"))
        self.label_os_pozioma.setText(_translate("Dialog", "Oś pozioma"))
        self.label_granice_dolna.setText(_translate("Dialog", "Granica dolna"))
        self.pushButton_wroc.setText(_translate("Dialog", "Wróć do okna głównego"))
        self.label_kroki_opt.setText(_translate("Dialog", "Kroki optymalizacji"))
        self.label_przekroj.setText(_translate("Dialog", "Przekrój przestrzeni rozwiązań"))
        self.label_rozdzielczosc_siatki.setText(_translate("Dialog", "Liczba próbek siatki na przedziale"))
        self.lineEdit_rozdzielczosc_siatki.setText(_translate("Dialog", "100"))
        self.label_kroki_kierunek.setText(_translate("Dialog", "Kroki metody optymalizacji w kierunku"))
        self.lineEdit_pozostale_zmienne.setText(_translate("Dialog", "Wartości pozostałych zmiennych"))
        self.label_pozostale_zmienne.setText (_translate ("Dialog", "Przekrój dla zmiennych"))
        self.pushButton_wyswietl_siatke_2.setText (_translate ("Dialog", "Wyświetl przekrój w kierunku"))
        self.lineEdit_a_0.setText (_translate ("Dialog", ""))
        self.label_a.setText (_translate ("Dialog", "Minimalizacja f(x<sub>k</sub>+av<sub>k</sub>)=f(a)"))
        self.label_przekroj_2.setText (_translate ("Dialog", "Przekrój przestrzeni w kierunku"))
        self.lineEdit_a_a0.setText (_translate ("Dialog", ""))
        self.lineEdit_a_aopt.setText (_translate ("Dialog", ""))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
