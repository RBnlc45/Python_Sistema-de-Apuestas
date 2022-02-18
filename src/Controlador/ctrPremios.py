#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Vista.premiospy import Ui_frmPremios
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView, QMenu, QInputDialog
from Modelo.Admin import Administrador
admin=Administrador()
class ctrPremios(QMainWindow,Ui_frmPremios):
    def __init__(self, ventana_principal,parent=None):
        super(ctrPremios, self).__init__(parent)
        self.setupUi(self)
        self.venta_principal = ventana_principal
        self.btnQuitarMonto.clicked.connect(self.eliminar_monto)
        self.btnRegistrar.clicked.connect(self.ingresar_monto)
        self.btnCambiarPrecio.clicked.connect(self.cambiar_precio)
        self.actualizar_contenedores()
    def actualizar_contenedores(self):
        premio = admin.obtener_premio()
        self.lblPrecioActualColocar.setText(str(premio[0]))
        self.lblMontoDisponible.setText(str(premio[1]))
    def validar_monto(self,valor):#Valida el valor ingresado
        try:
            if len(valor) == 0: raise Exception
            valor = float(valor)
            if valor <= 0: raise Exception
            return True#El valor es correcto
        except:
            QMessageBox.about(None, "¡Error en el valor ingresado!", "Debe ingresar un valor númerico mayor a 0")
            return False
    def ingresar_monto(self):
        valor = self.txtMontoAgregar.text()
        if self.validar_monto(valor) is False:
            return
        valor=float(valor)
        admin.obtener_premio()
        admin.premio_agregar_monto(valor)
        QMessageBox.about(None, "¡El monto se ha actualizado éxitosamente!", "El monto ingresado se ha registrado éxitosamente")
        self.actualizar_contenedores()
        self.txtMontoAgregar.setText("")
    def eliminar_monto(self):
        valor=self.txtMontoQuitar.text()
        if self.validar_monto(valor) is False:
            return
        valor=float(valor)
        admin.obtener_premio()
        if valor > admin.premio[1]:
            QMessageBox.about(None,"¡Error en el valor ingresado!","El valor debe ser menor o igual al monto actual.")
            return
        admin.premio_agregar_monto(-valor)
        QMessageBox.about(None,"¡El monto se ha modificado éxitosamente!","El monto disponible se ha actualizado")
        self.actualizar_contenedores()
        self.txtMontoQuitar.setText("")
    def cambiar_precio(self):
        valor=self.txtNuevoPrecio.text()
        if self.validar_monto(valor) is False:
            return
        valor=float(valor)
        admin.obtener_premio()
        admin.premio_cambiar_precio(valor)#Se cambia el precio por participación en el sistema
        QMessageBox.about(None, "¡El precio por participación se ha modificado éxitosamente!", "El precio de la participación en el torneo ha sido modificado")
        self.actualizar_contenedores()
        self.txtNuevoPrecio.setText("")

    def closeEvent(self, event):
        self.venta_principal.show()
        self.close()