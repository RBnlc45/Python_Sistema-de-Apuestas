#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from Vista.principalpy import Ui_MainWindow

class ctrPrincipal(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(ctrPrincipal, self).__init__(parent)
        self.setupUi(self)
        self.jtbPartidos.triggered.connect(self.partidos)
        self.jtbPaises.triggered.connect(self.paises)
        self.jtbParticipantes.triggered.connect(self.participantes)
        self.jtbGanadores.triggered.connect(self.ganadores)
        self.jtbSalir.triggered.connect(self.closeEvent)
        self.jtbPremios.triggered.connect(self.premios)
    def partidos(self):
        from Controlador.ctrPartidos import ctrPartidos
        self.ventana = ctrPartidos(self)
        self.ventana.show()
        self.hide()
    def paises(self):
        from Controlador.ctrPaises import ctrPaises
        self.ventana = ctrPaises(self)
        self.ventana.show()
        self.hide()
    def participantes(self):
        from Controlador.ctrParticipantes import ctrParticipantes
        self.ventana = ctrParticipantes(self)
        self.ventana.show()
        self.hide()
    def ganadores(self):
        from Controlador.ctrGanadores import ctrGanadores
        self.ventana = ctrGanadores(self)
        self.ventana.show()
        self.hide()
    def premios(self):
        from Controlador.ctrPremios import ctrPremios
        self.ventana = ctrPremios(self)
        self.ventana.show()
        self.hide()
    def closeEvent(self, event=None):
        self.close()



