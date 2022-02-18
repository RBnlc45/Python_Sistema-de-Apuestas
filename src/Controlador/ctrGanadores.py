#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Vista.ganadorespy import Ui_frmGanadores
from PyQt6 import uic,QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from Modelo.Admin import Administrador
admin=Administrador()
class ctrGanadores(QMainWindow,Ui_frmGanadores):
    def __init__(self, ventana_principal,parent=None):
        super(ctrGanadores, self).__init__(parent)
        self.setupUi(self)
        self.venta_principal = ventana_principal
        self.ganadoresDefinidos = False
        self.clasificar_participantes()
        self.btnDefinirGanador.clicked.connect(self.definir_ganador)
        self.rdbDesgloce.clicked.connect(self.clasificar_participantes)
    def clasificar_participantes(self):
        participantes=admin.obtener_lista_participantes()
        if len(participantes)==0: return
        participantes=sorted(participantes,key=lambda x:x.puntos,reverse=True)
        self.mostrar_tabla(participantes,self.ganadoresDefinidos)

    def mostrar_tabla(self,lista,ganadores=False):
        self.jgdParticipantes.setRowCount(0)
        if self.rdbDesgloce.isChecked() is True:
            [self.jgdParticipantes.showColumn(i) for i in range(5,14)]
        else:
            [self.jgdParticipantes.hideColumn(i) for i in range(5, 14)]
        if ganadores is True:#Si se definieron ganadores se coloca una nueva columna con el premio asignado a los ganadors
            if self.jgdParticipantes.isColumnHidden(4) is True:
                self.jgdParticipantes.showColumn(4)
        else:
            self.jgdParticipantes.hideColumn(4)
        for i in range(0,len(lista)):
            self.jgdParticipantes.insertRow(i)
            self.jgdParticipantes.setItem(i, 0, QTableWidgetItem(str(lista[i].cedula)))
            self.jgdParticipantes.setItem(i, 1, QTableWidgetItem(str(lista[i].nombre)))
            self.jgdParticipantes.setItem(i, 2, QTableWidgetItem(str(lista[i].apellido)))
            self.jgdParticipantes.setItem(i, 3, QTableWidgetItem(str(lista[i].puntos[0])))
            if ganadores==True:
                if lista[i].cedula in admin.premio[2]:
                    self.jgdParticipantes.setItem(i, 4, QTableWidgetItem("$ "+str(admin.premio[1]/len(admin.premio[2]))))
            if self.rdbDesgloce.isChecked() is True:
                [self.jgdParticipantes.setItem(i, 4+j, QTableWidgetItem(str(lista[i].puntos[j]))) for j in range(1,9) ]
    def definir_ganador(self):
        admin.obtener_premio()#Se obtiene el premio disponible
        participantes = admin.obtener_lista_participantes()
        if len(participantes) == 0:
            QMessageBox.about(None,"¡Aviso Importante!","Todavía no se han ingresado participantes")
            return
        participantes = sorted(participantes, key=lambda x: x.puntos, reverse=True)#Se ordenan los participantes por sus puntos
        primer_ganador=participantes[0]#Se obtiene el participante que está primero
        ganadores=list(filter(lambda x:x.puntos==primer_ganador.puntos,participantes))#Si filtran los ganadores
        admin.premio[2]=[g.cedula for g in ganadores]
        admin.actualizar_premio()
        self.ganadoresDefinidos=True
        self.mostrar_tabla(participantes,True)
        QMessageBox.about(None,"Ganadores asignados con éxito!","Se han asignado los premios a los respectivos ganadores.")
    def closeEvent(self, event):
        self.venta_principal.show()
        self.close()