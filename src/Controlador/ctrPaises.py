#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Vista.paisespy import Ui_Form
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from Modelo.Grupo import Grupo
from Modelo.Seleccion import Seleccion
from Modelo.Admin import Administrador
admin = Administrador()
class ctrPaises(QMainWindow,Ui_Form):
    def __init__(self,venta_principal,parent=None):
        super(ctrPaises, self).__init__(parent)
        self.setupUi(self)
        self.venta_principal=venta_principal
        self.btnAgregar.clicked.connect(self.agregarSeleccion)
        self.btnCargarValores.clicked.connect(self.cargar_valores_seleccion)
        self.btnEditar.clicked.connect(self.editar_seleccion)
        self.btnEliminar.clicked.connect(self.eliminar_seleccion)
        self.cmbGrupos_2.insertItems(0, [chr(i) for i in range(65, 73)])
        self.cmbGruposEditar.insertItems(0, [chr(i) for i in range(65, 73)])
        self.cargarValoresPaises()
        self.cargarValoresGrupos()

    def agregarSeleccion(self):
        listaSelecciones=admin.obtener_lista_selecciones()
        listaGrupos=admin.obtener_lista_grupos()
        seleccion = Seleccion(self.txtNombrePais.text())
        grupo=Grupo(self.cmbGrupos_2.currentText())
        if seleccion not in listaSelecciones and len(listaSelecciones) < 32 and seleccion.pais.replace(" ","") != "":  # Si el pais no está registrado
            if admin.obtener_grupo_pais(seleccion.pais) is None:
                self.agregar_seleccion_grupo(seleccion,grupo,listaGrupos,listaSelecciones)
            else:
                QMessageBox.about(None, "Error!", "La selección ingresado ya está registrada en un grupo diferente")
        elif len(listaSelecciones) == 32:
            QMessageBox.about(None, "Error!", "Se ha completado el cupo de 32 selecciones para este evento")
        elif seleccion.pais.replace(" ", "") == "":
            QMessageBox.about(None, "Error!", "Ingrese un nombre válido")
        else:
            QMessageBox.about(None, "Error!", "La selección ingresado ya está registrada")

    def agregar_seleccion_grupo(self,seleccion,grupo,grupos,selecciones):
        if grupo not in grupos:  # si crea el grupo por primera vez
            grupo.selecciones.append(seleccion.pais)  # Se agrega el pais al grupo
            grupos.append(grupo)  # Se agrega el grupo a la lista de grupos
            selecciones.append(seleccion)  # Se agrega la nueva selección
            admin.actualizar_lista_selecciones()#Se guarda la lista de selecciones
            admin.actualizar_lista_grupos()  # se guarda la lista grupos
            QMessageBox.about(None, "¡Asignación Éxitosa!", "El país se creó y asignó correctamente al grupo seleccionado")
            self.txtNombrePais.setText("")
            self.cargarValoresGrupos()
            self.cargarValoresPaises()
        else:  # El grupo ya ha sido creado
            grupo = admin.obtener_grupo_codigo(grupo.codigo_grupo)  # se obtiene el estado actual del grupo al que se colocará el pais
            if len(grupo.selecciones) < 4:
                grupo.selecciones.append(seleccion.pais)#Se agrega la selección al grupo
                admin.actualizar_lista_grupos()#Se guarda la lista de grupos
                selecciones.append(seleccion)  # Se agrega la nueva selección
                admin.actualizar_lista_selecciones()  # Se guarda la lista de selecciones
                QMessageBox.about(None, "¡Asignación Éxitosa!", "El país se creó y asignó correctamente al grupo seleccionado")
                self.txtNombrePais.setText("")
                self.cargarValoresGrupos()
                self.cargarValoresPaises()
            else:
                QMessageBox.about(None, "¡Error!", "El grupo seleccionado contiene los 4 equipos reglamentarios")

    def cargarValoresGrupos(self):
        grupos=admin.obtener_lista_grupos()
        # Diccionario para obtener el objeto lista para cada grupo
        grupos_listas = {'A': self.lstGrupoA, 'B': self.lstGrupoB, 'C': self.lstGrupoC, 'D': self.lstGrupoD,
                         'E': self.lstGrupoE, 'F': self.lstGrupoF, 'G': self.lstGrupoG, 'H': self.lstGrupoH}
        for g in grupos:#Se muestran a las selecciones en sus grupos correspondientes
            lst = grupos_listas.get(g.codigo_grupo)
            lst.clear()
            selecciones= [p for p in g.selecciones]
            selecciones.sort()
            [lst.addItem(QListWidgetItem(QIcon(admin.obtener_seleccion(p).bandera), admin.obtener_seleccion(p).pais)) for p in selecciones]

    def cargarValoresPaises(self):  # Cargar los valores para mostrarlos en la interfaz
        selecciones = admin.obtener_lista_selecciones()
        selecciones_nombres = [p.pais for p in selecciones]#Se obtienen los nombres de las selecciones
        selecciones_nombres.sort()
        self.lstPaises.clear()
        self.cmbPaises.clear()
        self.cmbPaisesEliminar.clear()
        [self.lstPaises.addItem(QListWidgetItem(QIcon(p.bandera), p.pais)) for p in selecciones]
        self.lblCantidadPaisesValor.setText(str(len(selecciones)))
        self.cmbPaises.insertItems(0, selecciones_nombres)
        self.cmbPaisesEliminar.insertItems(0, selecciones_nombres)

    def cargar_valores_seleccion(self):
        admin.obtener_lista_selecciones()
        #Se busca la instancia de la selección solicitada
        self.seleccion = admin.obtener_seleccion(self.cmbPaises.currentText())  # Seleccion que va a ser editada
        if self.seleccion is None:
            QMessageBox.about(None,"¡Error!","El país seleccionado no se encuentra en la lista")
            return
        grupo_seleccion=admin.obtener_grupo_pais(self.seleccion.pais)#Se busca el grupo asociado al la selección
        if grupo_seleccion is None:
            self.cmbGruposEditar.setCurrentIndex(-1)
        else:
            self.cmbGruposEditar.setCurrentIndex(ord(grupo_seleccion.codigo_grupo)-65)#se coloca el cmb en la posición del grupo actual de la selección
        self.cmbGruposEditar.setEnabled(True)
        self.btnEditar.setEnabled(True)

    def editar_seleccion(self):
        def limpiar_paneles():
            self.cmbGruposEditar.setCurrentIndex(-1)
            self.cmbGruposEditar.setEnabled(False)
            self.btnEditar.setEnabled(False)
        def actualizacion_exitosa():
            QMessageBox.about(None, "Actualización éxitosa!", "Se ha cambiado el grupo de la selección escogida")
            self.cargarValoresGrupos()
            self.cargarValoresPaises()
            limpiar_paneles()
        def grupo_no_creado():
            grupo = Grupo(grupo_seleccionado)  # Se crea el nuevo grupo
            grupo.selecciones.append(nombre_ingresado)  # Se agrega la selección a la lista de selecciones del grupo
            if grupo_actual is not None:
                grupo_actual.selecciones.remove(nombre_ingresado)  # Se quita a la seleccion de su grupo anterior
            admin.agregar_grupo(grupo)  # Se agrega el grupo a la lista de grupos
        def grupo_creado():
            grupo.selecciones.append(nombre_ingresado)  # Se agrega la selección a su nuevo grupo
            if grupo_actual is not None:
                grupo_actual.selecciones.remove(nombre_ingresado)  # Se quita a la seleccion de su grupo anterior
            admin.actualizar_lista_grupos()#Se actualiza la lista
        grupo_seleccionado=self.cmbGruposEditar.currentText()
        grupo_actual=admin.obtener_grupo_pais(self.seleccion.pais)
        nombre_ingresado=self.seleccion.pais
        if grupo_seleccionado!="" and grupo_actual is not None and grupo_seleccionado!=grupo_actual.codigo_grupo:#Se trata de cambiar de grupo
            if len(admin.obtener_lista_partidos_grupos().values())!=0:#Si ya se han generado los partidos
                QMessageBox.about(None, "¡Error!","Los partidos de fase de grupos ya han sido generados, no se puede realizar un cambio de grupo")
                limpiar_paneles()
                return
            grupo=admin.obtener_grupo_codigo(grupo_seleccionado)#Se busca el grupo al que se va a cambiar la seleccion
            if grupo is not None and len(grupo.selecciones)==4:#Si el grupo esta lleno
                QMessageBox.about(None, "¡Error!","El grupo seleccionado está lleno")
                limpiar_paneles()
                return
            elif grupo is None:#Si el grupo seleccionado aun no se crea
                grupo_no_creado()
                actualizacion_exitosa()
                return
            #El grupo ya está creado
            else:
                grupo_creado()
                actualizacion_exitosa()
                return
        elif grupo_actual is None:#La selección no tiene grupo
            grupo = admin.obtener_grupo_codigo(grupo_seleccionado)  # Se busca el grupo al que se va a cambiar la seleccion
            if grupo is not None and len(grupo.selecciones) == 4:  # Si el grupo esta lleno
                QMessageBox.about(None, "Error!", "El grupo seleccionado está lleno")
                limpiar_paneles()
                return
            elif grupo is None:  # Si el grupo seleccionado aun no se crea
                grupo_no_creado()
                actualizacion_exitosa()
                return
            # El grupo ya está creado
            grupo_creado()
            actualizacion_exitosa()
            return

    def eliminar_seleccion(self):
        selecciones = admin.obtener_lista_selecciones()
        # Se busca la instancia de la selección solicitada
        seleccion=admin.obtener_seleccion(self.cmbPaisesEliminar.currentText())# Seleccion que va a ser editada
        if seleccion is None:
            QMessageBox.about(None,"¡Error!","El país seleccionado no se encuentra en la lista")
            return
        if len(admin.obtener_partidos_grupo_pais(seleccion.pais))>0:
            QMessageBox.about(None, "¡Error!", "La selección no puede ser eliminada debido a que ya tiene partidos asignados")
            return
        grupo_seleccion=admin.obtener_grupo_pais(seleccion.pais)#Se obtiene el grupo de la seleccion escogida
        grupo_seleccion.selecciones.remove(seleccion.pais)#Se elimina la selección del grupo
        selecciones.remove(seleccion)#Se elimina la seleccion de la lista de selecciones
        # Se guardan los cambios
        admin.actualizar_lista_grupos()
        admin.actualizar_lista_selecciones()
        self.cargarValoresPaises()
        self.cargarValoresGrupos()

    def closeEvent(self,event):
        self.venta_principal.show()
        self.close()