# Form implementation generated from reading ui file 'resultado.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_grbResultados(object):
    def setupUi(self, grbResultados):
        grbResultados.setObjectName("grbResultados")
        grbResultados.resize(839, 506)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(grbResultados.sizePolicy().hasHeightForWidth())
        grbResultados.setSizePolicy(sizePolicy)
        grbResultados.setMaximumSize(QtCore.QSize(839, 506))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icons/Iconos/puntaje.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        grbResultados.setWindowIcon(icon)
        self.jtbDesgloce = QtWidgets.QTableWidget(grbResultados)
        self.jtbDesgloce.setGeometry(QtCore.QRect(20, 180, 811, 101))
        self.jtbDesgloce.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.jtbDesgloce.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.jtbDesgloce.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.jtbDesgloce.setObjectName("jtbDesgloce")
        self.jtbDesgloce.setColumnCount(8)
        self.jtbDesgloce.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.jtbDesgloce.setHorizontalHeaderItem(7, item)
        self.lblReglas = QtWidgets.QLabel(grbResultados)
        self.lblReglas.setGeometry(QtCore.QRect(210, 290, 431, 171))
        self.lblReglas.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lblReglas.setObjectName("lblReglas")
        self.layoutWidget = QtWidgets.QWidget(grbResultados)
        self.layoutWidget.setGeometry(QtCore.QRect(290, 10, 251, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.lytEnfrentamiento = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.lytEnfrentamiento.setContentsMargins(0, 0, 0, 0)
        self.lytEnfrentamiento.setObjectName("lytEnfrentamiento")
        self.lblEnfrentamiento = QtWidgets.QLabel(self.layoutWidget)
        self.lblEnfrentamiento.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblEnfrentamiento.setObjectName("lblEnfrentamiento")
        self.lytEnfrentamiento.addWidget(self.lblEnfrentamiento)
        self.lblPartido = QtWidgets.QLabel(self.layoutWidget)
        self.lblPartido.setText("")
        self.lblPartido.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblPartido.setObjectName("lblPartido")
        self.lytEnfrentamiento.addWidget(self.lblPartido)
        self.layoutWidget1 = QtWidgets.QWidget(grbResultados)
        self.layoutWidget1.setGeometry(QtCore.QRect(280, 100, 271, 41))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.lytMarcador = QtWidgets.QFormLayout(self.layoutWidget1)
        self.lytMarcador.setContentsMargins(0, 0, 0, 0)
        self.lytMarcador.setObjectName("lytMarcador")
        self.lblMarcadorFinal = QtWidgets.QLabel(self.layoutWidget1)
        self.lblMarcadorFinal.setObjectName("lblMarcadorFinal")
        self.lytMarcador.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblMarcadorFinal)
        self.lblMarcadorFinal2 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblMarcadorFinal2.setText("")
        self.lblMarcadorFinal2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblMarcadorFinal2.setObjectName("lblMarcadorFinal2")
        self.lytMarcador.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lblMarcadorFinal2)
        self.lblMarcadorPronosticado = QtWidgets.QLabel(self.layoutWidget1)
        self.lblMarcadorPronosticado.setObjectName("lblMarcadorPronosticado")
        self.lytMarcador.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblMarcadorPronosticado)
        self.lblMarcadorPronosticado2 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblMarcadorPronosticado2.setText("")
        self.lblMarcadorPronosticado2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblMarcadorPronosticado2.setObjectName("lblMarcadorPronosticado2")
        self.lytMarcador.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lblMarcadorPronosticado2)
        self.lblPartidoAnulado = QtWidgets.QLabel(grbResultados)
        self.lblPartidoAnulado.setEnabled(True)
        self.lblPartidoAnulado.setGeometry(QtCore.QRect(30, 150, 191, 21))
        self.lblPartidoAnulado.setObjectName("lblPartidoAnulado")

        self.retranslateUi(grbResultados)
        QtCore.QMetaObject.connectSlotsByName(grbResultados)

    def retranslateUi(self, grbResultados):
        _translate = QtCore.QCoreApplication.translate
        grbResultados.setWindowTitle(_translate("grbResultados", "Desglose de Resultados"))
        item = self.jtbDesgloce.horizontalHeaderItem(0)
        item.setText(_translate("grbResultados", "Acierto Resultado"))
        item = self.jtbDesgloce.horizontalHeaderItem(1)
        item.setText(_translate("grbResultados", "Acierto Marcador"))
        item = self.jtbDesgloce.horizontalHeaderItem(2)
        item.setText(_translate("grbResultados", "Acierto Pleno"))
        item = self.jtbDesgloce.horizontalHeaderItem(3)
        item.setText(_translate("grbResultados", "Marcador y Goles"))
        item = self.jtbDesgloce.horizontalHeaderItem(4)
        item.setText(_translate("grbResultados", "Acierto Pleno y Goles"))
        item = self.jtbDesgloce.horizontalHeaderItem(5)
        item.setText(_translate("grbResultados", "Acierto Goles Dos Equipos"))
        item = self.jtbDesgloce.horizontalHeaderItem(6)
        item.setText(_translate("grbResultados", "Pegó en el palo"))
        item = self.jtbDesgloce.horizontalHeaderItem(7)
        item.setText(_translate("grbResultados", "Total"))
        self.lblReglas.setText(_translate("grbResultados", "* Acierto de resultado: 2 puntos\n"
"* Acierto de marcador: 1 puntos*\n"
"\n"
"Bonificaciones:\n"
"* Acierto de marcador y resultado (acierto pleno): Bono de 3 puntos*.\n"
"* Acierto de marcador, con suma de goles mayor a 3: Bono de 1 punto.\n"
"* Acierto de marcador y resultado, con suma de goles mayor a 3: 1 punto.\n"
"* Acierto de los goles de uno de los dos equipos: 0.5 puntos.\n"
"* Bono \"pegó en el palo\": Si le faltó o sobró un gol para el acierto pleno: 0.5 puntos."))
        self.lblEnfrentamiento.setText(_translate("grbResultados", "Enfrentamiento"))
        self.lblMarcadorFinal.setText(_translate("grbResultados", "Marcador Final:"))
        self.lblMarcadorPronosticado.setText(_translate("grbResultados", "Marcador Pronosticado:"))
        self.lblPartidoAnulado.setText(_translate("grbResultados", "El partido asociado ha sido anulado!"))