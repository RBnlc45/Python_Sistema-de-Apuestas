#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import sys
from PyQt6.QtGui import QIcon, QActionGroup, QAction
from Modelo.Partido import Partido
from Modelo.Participante import Participante
from Vista.participantespy import Ui_frmParticipantes
from Vista.resultadopy import Ui_grbResultados
from PyQt6 import uic,QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView, QMenu, QInputDialog
from Modelo.Admin import Administrador
from Modelo.Pronostico import Pronostico
admin=Administrador()
class ctrParticipantes(QMainWindow,Ui_frmParticipantes):
    def __init__(self, ventana_principal,parent=None):
        super(ctrParticipantes, self).__init__(parent)
        self.setupUi(self)
        self.venta_principal = ventana_principal
        self.inicializar_botones()
        self.inicializar_cmbs()
        self.grbDatosEditar.hide()#Oculta el panel de edición de participantes
        #Inicializar menús contextuales para las tablas
        self.jgdAgregarPronostico.customContextMenuRequested.connect(self.menuContextualAgregarPronostico)
        self.jgdEditarPronosticos.customContextMenuRequested.connect(self.menuContextualEditarPronostico)
        #Inicializar las acciones de los radio button
        self.rbtPronosticosDefinidos.clicked.connect(self.filtro_definidos)
        self.rbtPronosticosPorDefinir.clicked.connect(self.filtro_por_definirse)
    def inicializar_botones(self):#Inicializa las acciones de los pushbutton
        self.btnCrearUsuario.clicked.connect(self.ingresar_usuario)
        self.btnBuscar.clicked.connect(self.buscar_usuario)
        self.btnEditarUsuario.clicked.connect(self.editar_usuario)
        self.btnEliminar.clicked.connect(self.eliminar_usuario)
        self.btnBuscarAgregar.clicked.connect(self.agregar_pronostico)
        self.btnBuscarEditar.clicked.connect(self.editar_buscar_pronostico)
    def inicializar_cmbs(self):#Inicializa los valores en los combobox
        #Lista con los comboboxes que contienen a los participantes disponibles
        cmbs_participantes=[self.cmbParticipantesEditar,self.cmbParticipantesPronostico,self.cmbParticipantesPronostico2,self.cmbParticipantesEliminar]
        [c.clear() for c in cmbs_participantes ]#Se limpian los comboboxs
        personas=admin.obtener_lista_participantes()#Se obtienen los participantes disponibles
        personas=["{0}-{1} {2}".format(p.cedula,p.nombre,p.apellido) for p in personas]#Se crea la lista con los valores a mostrar en los comboboxes
        [c.addItems(personas) for c in cmbs_participantes]#Se agregan los elementos a los cmbs
    def verificar_telefono_cedula(self,cedula,telefono):
        if cedula.isdigit() is False or len(cedula)!=10:
            #La cédula no es válida en primera instancia
            QMessageBox.about(None,"Error en el número de cédula!","Ingrese un número de cédula válido")
            return False
        #Verificación de teléfono
        elif telefono.isdigit() is False or len(telefono)!=10:
            QMessageBox.about(None, "Error en el número de teléfono!", "Ingrese un número de teléfono válido")
            return False
        return True
    def ingresar_usuario(self):
        admin.obtener_lista_participantes()
        elementos = [self.txtDireccion, self.txtNombre, self.txtApellido, self.txtTelefono,self.txtCedula]
        cedula=self.txtCedula.text()
        nombre=self.txtNombre.text()
        apellido=self.txtApellido.text()
        telefono=self.txtTelefono.text()
        direccion=self.txtDireccion.text()
        #Verificación de datos
        if 0 in [len(p) for p in [cedula,telefono,nombre,apellido,direccion]]:#Algún campo está vacío
            QMessageBox.about(None, "Error, campos vacíos!", "Algunos campos están vacíos, asegurese de llenar todos")
            return
        elif self.verificar_telefono_cedula(cedula,telefono) is False:
            return
        self.participante = admin.obtener_participante(cedula)  # Se busca la instancia del participante
        if self.participante is not None:  # Verificación de la existencia del participante
            QMessageBox.about(None, "¡Error!", "El número de cédula que se intentó ingresar ya está registrado")
            return
        admin.obtener_premio()#Se carga la lista de premios y montos disponibles
        msg = QMessageBox.warning(self, "¡Advertencia!", "El participante está a punto de ser registrado. Se debe realizar el cobro de una cuota de $"+str(admin.premio[0])+" para ser parte del sistema.\n ¿Está de acuerdo?",
                                  QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.No:  # Se cancelo el ingreso del participante
            return
        #Se agrega el participante
        admin.agregar_participante(Participante(cedula,nombre,apellido,direccion,telefono))
        admin.premio[1]=admin.premio[1]+admin.premio[0]#Se aumenta el monto del premio con cada registro de participante
        admin.actualizar_premio()#Se guarda la lista de premios
        QMessageBox.about(None,"Ingreso Éxitoso!","El participante ha sido registrado éxitosamente")
        [e.clear() for e in elementos]#Se limpian los elementos del panel
        self.inicializar_cmbs()#Se actualizan los comboboxes de participantes
    def buscar_usuario(self):
        elementos = [self.txtDireccionEditar, self.txtNombreEditar, self.txtApellidoEditar, self.txtTelefonoEditar, self.txtCedulaEditar]
        [e.clear() for e in elementos]#Se limpian los elementos del panel de editar Participante
        self.participante=admin.obtener_participante((self.cmbParticipantesEditar.currentText())[0:10])#Se busca la instancia del participante seleccionado
        if self.participante is None:#Verificación de la no existencia del participante
            QMessageBox.about(None, "¡Error!", "El participante buscado no ha sido encontrado")
            return
        else:
            self.grbDatosEditar.show()#Se muestra el panel de edición
        #Se colocan los datos actuales del participante
        self.txtCedulaEditar.setText(self.participante.cedula)
        self.txtNombreEditar.setText(self.participante.nombre)
        self.txtApellidoEditar.setText(self.participante.apellido)
        self.txtTelefonoEditar.setText(self.participante.telefono)
        self.txtDireccionEditar.setText(self.participante.direccion)
    def editar_usuario(self):
        #Elementos del panel de edición
        elementos=[self.txtDireccionEditar,self.txtNombreEditar,self.txtApellidoEditar,self.txtTelefonoEditar,self.txtCedulaEditar]
        cedula = self.txtCedulaEditar.text()
        nombre = self.txtNombreEditar.text()
        apellido = self.txtApellidoEditar.text()
        telefono = self.txtTelefonoEditar.text()
        direccion = self.txtDireccionEditar.text()
        if 0 in [len(p) for p in [cedula,telefono,nombre,apellido,direccion]]:#Algún campo está vacío
            QMessageBox.about(None, "Error, campos vacíos!", "Algunos campos están vacíos, asegurese de llenar todos")
            return
        elif self.verificar_telefono_cedula(cedula,telefono) is False:  return
        cedula_anterior=self.participante.cedula
        self.participante.cedula=cedula
        self.participante.nombre=nombre
        self.participante.apellido=apellido
        self.participante.telefono=telefono
        self.participante.direccion=direccion
        #Se cargan los pronosticos disponibles
        admin.obtener_lista_pronosticos()
        if cedula_anterior!=cedula:#Si la cédula ha cambiado
            pronosticos=admin.obtener_pronosticos(cedula_anterior)#Se obtienen todos los pronósticos del participante
            for p in pronosticos:#Se cambia la cédula del participante en los pronósticos asociados
                p.participante=cedula
            admin.actualizar_lista_pronosticos()#Se guardan los cambios en la lista de pronósticos
        admin.actualizar_lista_participantes()#Se guardan los cambios en la lista de participantes
        self.inicializar_cmbs()#Se actualizan los valores de los cmbs
        [e.clear() for e in elementos]#Se limpian los elementos del panel de edición
        self.grbDatosEditar.hide()#Se oculta el panel de edición
    def eliminar_usuario(self):
        participante = admin.obtener_participante((self.cmbParticipantesEliminar.currentText())[0:10])  # Se busca la instancia del participante seleccionado
        if participante is None:  # Verificación de la existencia del participante
            QMessageBox.about(None, "¡Error!", "El participante ha eliminar no ha sido encontrado.")
            return
        #Se verifica si se quiere eliminar
        msg = QMessageBox.warning(self, "¡Advertencia!", "¿Está seguro en eliminar al participante {0}? ".format(self.cmbParticipantesEliminar.currentText()), QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.No:#Se canceló la eliminación
            return
        admin.obtener_lista_pronosticos()#Se recupera la lista de pronósticos disponibles
        admin.obtener_lista_partidos_disponibles()#Se recupera la lista de partidos disponibles
        pronosticos=admin.obtener_pronosticos(participante.cedula)#Se obtienen todos los pronósticos del participante
        if len(pronosticos)==0:#No tiene pronosticos
            admin.obtener_lista_participantes().remove(participante)#Se elimina el participante
            admin.actualizar_lista_participantes()#Se actualizan los cambios
            QMessageBox.about(None, "Eliminación éxitosa!", "El participante ha sido eliminado")
            self.inicializar_cmbs()
            return
        #El participante tiene pronosticos realizados
        pronosticos_ids=[p.id for p in pronosticos]#Se obtienen los ids de los pronósticos del participante
        partidos=[admin.obtener_partido_pronostico(p) for p in pronosticos_ids]#Se obtienen los partidos asociados a cada pronóstico
        [e[1].pronosticos.remove(e[0]) for e in list(zip(pronosticos_ids,partidos))]#Se eliminan los pronósticos de cada partido
        pronosticos_aux=admin.obtener_lista_pronosticos()#Se obtiene la lista de pronosticos disponibles
        pronosticos_aux=[p for p in pronosticos_aux if p.id not in pronosticos_ids]#Se eliminan los pronosticos del participante
        admin.actualizar_lista_pronosticos(pronosticos_aux)#Se actualiza la lista de pronosticos
        admin.actualizar_lista_partidos_disponibles()#Se actualiza la lista de partidos disponibles
        admin.obtener_lista_participantes().remove(participante)  # Se elimina el participante
        admin.actualizar_lista_participantes()  # Se actualiza la lista de participantes
        QMessageBox.about(None, "Eliminación éxitosa!", "El participante ha sido eliminado")
        #Se limpian los contenidos de las tablas y lbls
        self.jgdEditarPronosticos.setRowCount(0)
        self.jgdAgregarPronostico.setRowCount(0)
        self.lblColocarPuntosEB.clear()
        self.lblColocarPuntosA.clear()
        self.lblColocarParticipanteA.clear()
        self.lblColocarParticipanteEB.clear()
        self.partidos=None
        self.marcadores=None
        self.participante=None
        #Se vuelven a cargar los contenidos de los comboboxs
        self.inicializar_cmbs()

    def partidos_para_seleccionar(self,opc):
        def opc1(pronosticos,fecha=None,editar=False):
            grupos=admin.obtener_lista_grupos()
            if editar is True:#Se obtienen los grupos que tienen sus partidos con fechas definidas
                grupos = [g.codigo_grupo for g in grupos if g.fechas_definidas is True]
            else:#Se obtienen los grupos con partidos con fechas definidas y que no estén definidos
                grupos = [g.codigo_grupo for g in grupos if g.fechas_definidas is True and g.definido is False]
            partidos=list()
            [partidos.extend(p) for p in [admin.obtener_partidos_grupo(c) for c in grupos]]#Se obtiene la lista con todos lo partidos que se pueden pronosticar
            partidos = sorted(partidos, key=lambda x: x.fechaInicio)#Se ordenan los partidos por fecha
            if editar is False:#Se filtran los partidos que no deben estar disponibles para la fecha de ingreso y que no estan pronosticados
                partidos=[p for p in partidos if p not in pronosticos and p.fechaInicio > fecha]
            else:#Se filtran los partidos que están pronosticados
                partidos = [p for p in partidos if p in pronosticos]
            if len(partidos)==0 and admin.is_fase_definida(admin.obtener_lista_partidos_grupos(),True) is True and editar is False:
                #Cuando se busca pronosticar un partido de una fase y esta ya ha sido definida
                QMessageBox.about(None,"¡Aviso Importante!","La fase de grupos ha finalizado. \n No se pueden realizar más pronósticos para esta fase")
                return None
            elif len(partidos)==0 and editar is False:
                QMessageBox.about(None, "¡Aviso importante!","No existen partidos para pronosticar en la fecha de ingreso colocada.\n Puede esperar que se definan las fechas de los partidos de esta fase.")
                return None
            return partidos
        def opc2(lista,validador_fechas,pronosticos,fecha=None,editar=False):
            partidos=list(lista.values())
            if editar is True:#Filtran los partidos que están pronosticados
                partidos = [p for p in partidos if p.fechaDefinida is True and p in pronosticos]
            else:#Se filtran los partidos que no están definidos y que estan disponibles para la fecha ingresada
                partidos = [p for p in partidos if p.fechaDefinida is True and p.partidoDefinido is False and p not in pronosticos and p.fechaInicio > fecha]
            if len(partidos)==0 and admin.is_fase_definida(lista) is True and editar is False:
                QMessageBox.about(None,"Aviso Importante!","La fase actual ha finalizado. \n No se pueden realizar más pronósticos para esta fase")
                return None
            elif len(partidos)==0 and editar is False:
                QMessageBox.about(None, "Aviso importante!","No existen partidos para pronosticar en la fecha de ingreso colocada.\n Puede esperar que se definan las fechas de los partidos de esta fase.")
                return None
            return partidos
        funciones=dict(zip(["Fase de Grupos","Octavos de Final","Cuartos de Final","Semifinales","Finales"],[opc1,opc2,opc2,opc2,opc2]))
        return funciones.get(opc)
    def mostrar_tabla(self,tabla,lista,opc=True,marcador=None):
        tabla.setRowCount(0)#Se limpia la tabla
        if lista is not None:
            for i in range(0, len(lista)):#Se recorren los items de la lista
                tabla.insertRow(i)#Se coloca una fila
                elementos = lista[i].obtener_valores_mostrar()#Se obtienen los items del partido ha mostrar
                tabla.setItem(i, 0, QTableWidgetItem(elementos[0]))
                tabla.setItem(i, 1, QTableWidgetItem(QIcon(elementos[1].bandera), elementos[1].pais))#Se coloca las selección 1
                if opc is True and marcador is None:#Cuando se muestran partidos que se pueden pronosticar
                    tabla.setItem(i, 2, QTableWidgetItem(QIcon(elementos[3].bandera), elementos[3].pais)) #Se coloca la selección 2
                else:#Cuando se muestran pronósticos realizados
                    tabla.setItem(i, 2, QTableWidgetItem("{0} - {1}".format(marcador[i][0],marcador[i][1])))#Se coloca el marcador del encuentro
                    tabla.setItem(i, 3, QTableWidgetItem(QIcon(elementos[3].bandera), elementos[3].pais))#Se coloca la selección 2

    def filtro_definidos(self):#Se muestran los pronósticos de partidos definidos
        try:
            values=list(zip(self.marcadores,self.partidos))
            values=[v for v in values if v[1].partidoDefinido is True]
            partidos=[p[1] for p in values]
            marcadores=[m[0] for m in values]
            self.mostrar_tabla(self.jgdEditarPronosticos, partidos, False, marcadores)
        except:
            return
    def filtro_por_definirse(self):#Se muestran los pronósticos de partidos no definidos
        try:
            values = list(zip(self.marcadores, self.partidos))
            values = [v for v in values if v[1].partidoDefinido is False]
            partidos = [p[1] for p in values]
            marcadores = [m[0] for m in values]
            self.mostrar_tabla(self.jgdEditarPronosticos, partidos, False, marcadores)
        except:
            return

    def obtener_marcador(self,seleccion1,seleccion2):#Devuelve el marcador ingresado por el usuario
        marcador = [0, 0]  # Se inicializa el marcador a utilizar
        a = QInputDialog.getInt(self, "Marcador", "Ingrese el marcador a favor de " + seleccion1, 0, 0, 50, 1)
        if a[1] == False:  # Se canceló el ingreso
            return None
        marcador[0] = a[0]  # Se asigna el primer valor del marcador
        a = QInputDialog.getInt(self, "Marcador", "Ingrese el marcador a favor de " + seleccion2, 0, 0, 50, 1)
        if a[1] == False:  # Se canceló el ingreso
            return None
        marcador[1] = a[0]  # Se asigna el segundo valor del marcador
        # Pregunta de advertencia
        msg = QMessageBox.warning(self, "¡Advertencia!", "¿Está seguro en realizar el pronóstico?", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.No:  # Se cancelo el ingreso del marcador
            return None
        return marcador

    def agregar_pronostico(self):
        admin.obtener_lista_partidos_disponibles()#Se cargan todas las listas de partidos disponibles
        admin.obtener_lista_pronosticos()#Se cargan los pronosticos disponibles
        participante = admin.obtener_participante((self.cmbParticipantesPronostico.currentText())[0:10])  # Se busca la instancia del participante
        if participante is None: # Verificación de la existencia del participante
            QMessageBox.about(None, "Error!", "El participante no ha sido encontrado")
            return
        # Se coloca en pantalla la información del participante
        self.lblColocarParticipanteA.setText(participante.nombre + " " + participante.apellido)
        self.lblColocarPuntosA.setText(str(participante.puntos[0]))
        pronosticos=admin.obtener_pronosticos(participante.cedula)#Se obtienen todos los pronosticos que realizó el participante
        pronosticos = [admin.obtener_partido_pronostico(p.id) for p in pronosticos]#Se obtienen los partidos asociados a los pronósticos
        tipo=self.cmbTipoEncuentro.currentText()
        self.fecha_ingreso=datetime.datetime.strptime(self.dtpFechaSimulada.text(), '%d/%m/%Y %H:%M')#Se obtiene la fecha de ingreso del pronóstico
        funcion=self.partidos_para_seleccionar(tipo)#Función para buscar los partidos que se pueden pronosticar según el tipo de fase escogido
        if tipo=="Fase de Grupos":
            partidos=funcion(pronosticos,fecha=self.fecha_ingreso)
        elif tipo=="Octavos de Final":
            lista=admin.obtener_lista_partidos_octavos()
            faseDefinida=admin.is_fechas_definidas(lista)
            partidos=funcion(lista,faseDefinida,pronosticos,fecha=self.fecha_ingreso)
        elif tipo=="Cuartos de Final":
            lista = admin.obtener_lista_partidos_cuartos()
            faseDefinida = admin.is_fechas_definidas(lista)
            partidos = funcion(lista, faseDefinida,pronosticos,fecha=self.fecha_ingreso)
        elif tipo=="Semifinales":
            lista = admin.obtener_lista_partidos_semifinales()
            faseDefinida = admin.is_fechas_definidas(lista)
            partidos = funcion(lista, faseDefinida,pronosticos,fecha=self.fecha_ingreso)
        elif tipo=="Finales":
            lista = admin.obtener_lista_partidos_finales()
            faseDefinida = admin.is_fechas_definidas(lista)
            partidos = funcion(lista, faseDefinida,pronosticos,fecha=self.fecha_ingreso)
        self.mostrar_tabla(self.jgdAgregarPronostico,partidos)#Se muestran los partidos disponibles para ser pronosticados
        self.participante=participante#Se actualiza la referencia del participante buscado

    def asignar_pronostico(self,accion):#Se asigna un pronóstico
        admin.obtener_lista_partidos_disponibles()#Se cargan los partidos disponibles
        admin.obtener_lista_pronosticos()#Se cargan los pronosticos disponibles
        filaSeleccionada = [dato.text() for dato in self.jgdAgregarPronostico.selectedItems()]#Se obtiene los valores de la fila seleccionada de la tabla
        fecha=datetime.datetime.strptime(filaSeleccionada[0],'%d/%m/%Y %H:%M')#Se obtienen la fecha del partido ha pronosticar
        #Se crea un objeto referencial del partido a pronosticar
        if filaSeleccionada[2]=="PD":  partido=Partido(fecha,filaSeleccionada[1],None)
        else:  partido = Partido(fecha, filaSeleccionada[1], filaSeleccionada[2])
        partido=admin.obtener_partido(partido)#Se obtiene el partido en base a la referencia
        marcador=self.obtener_marcador(filaSeleccionada[1],filaSeleccionada[2])#Se solicita el marcador del pronóstico
        if marcador is None: return#Ingreso cancelado
        pronostico=Pronostico(self.fecha_ingreso,self.participante.cedula,marcador)#Se crea la instancia del pronóstico
        admin.agregar_pronostico(pronostico)#Se agrega el pronóstico a la lista de pronósticos
        partido.pronosticos.append(pronostico.id)#Se agrega el id del pronóstico al partido
        admin.actualizar_lista_partidos_disponibles()#Se guardan los cambios en la lista de partidos
        admin.actualizar_lista_pronosticos()#Se guardan los cambios de la lista de pronosticos
        self.agregar_pronostico()#Se actualizan las tablas de partidos disponibles para pronosticar

    def editar_buscar_pronostico(self):
        admin.obtener_lista_partidos_disponibles()#Se carga la lista de partidos disponibles
        admin.obtener_lista_pronosticos()#Se carga la lista de pronosticos disponibles
        participante = admin.obtener_participante((self.cmbParticipantesPronostico2.currentText())[0:10])  # Se busca la instancia del participante
        if participante is None:  # Verificación de la existencia del participante
            QMessageBox.about(None, "Error!", "El participante seleccionado no ha sido encontrado")
            return
        #Se coloca en pantalla la información del participante
        self.lblColocarParticipanteEB.setText(participante.nombre+" "+participante.apellido)
        self.lblColocarPuntosEB.setText(str(participante.puntos[0]))
        #Se obtienen los pronosticos asociados al participante
        pronosticos = admin.obtener_pronosticos(participante.cedula)  # Se obtienen todos los pronosticos que realizó el participante
        #Se obtienen los partidos de cada pronostico asociado
        partidos_pronosticados = [admin.obtener_partido_pronostico(p.id) for p in pronosticos]
        #Se generan los pares partido pronostico para poder posteriormente ubicarlos
        pronosticos_aux = list(zip(pronosticos,partidos_pronosticados))
        tipo = self.cmbTipoEncuentro2.currentText()#Tipo de fase seleccionada
        funcion = self.partidos_para_seleccionar(tipo)#Funcion para obtener los partidos a mostrar
        if tipo == "Fase de Grupos":
            self.partidos = funcion(partidos_pronosticados,editar=True)
        elif tipo == "Octavos de Final":
            lista=admin.obtener_lista_partidos_octavos()
            fase=admin.is_fase_definida(lista)
            self.partidos = funcion(lista, fase, partidos_pronosticados,editar=True)
        elif tipo == "Cuartos de Final":
            lista = admin.obtener_lista_partidos_cuartos()
            fase = admin.is_fase_definida(lista)
            self.partidos = funcion(lista, fase, partidos_pronosticados,editar=True)
        elif tipo == "Semifinales":
            lista = admin.obtener_lista_partidos_semifinales()
            fase = admin.is_fase_definida(lista)
            self.partidos = funcion(lista, fase, partidos_pronosticados,editar=True)
        elif tipo == "Finales":
            lista = admin.obtener_lista_partidos_finales()
            fase = admin.is_fase_definida(lista)
            self.partidos = funcion(lista, fase, partidos_pronosticados,editar=True)
        #Se ordenan los partidos obtenidos por fecha
        self.partidos=sorted(self.partidos,key=lambda x:x.fechaInicio)
        #Se obtienen los marcadores en base a los partidos obtenidos
        self.marcadores=[pr[0].marcador_pronosticado for p in self.partidos for pr in pronosticos_aux if p==pr[1]]
        #Se aplica el filtro seleccionado en el radio button
        if self.rbtPronosticosPorDefinir.isChecked() is True:
            self.filtro_por_definirse()
        else:
            self.filtro_definidos()
        #Se actualiza la referencia del participante
        self.participante = participante

    def editar_pronostico(self,accion):
        def validacion_partido_definido():#Determina los estados en los que se encuentra un partido para saber si se puede editar o no
            fecha_ingreso = datetime.datetime.strptime(self.dtpFechaSimulada2.text(), '%d/%m/%Y %H:%M')
            if partido.partidoDefinido is True:
                QMessageBox.about(None, "Error!", "El partido se ha definido, no se pueden realizar cambios")
                return False
            elif fecha_ingreso>partido.fechaInicio:
                QMessageBox.about(None, "Error!", "El partido está en juego, no se pueden realizar cambios")
                return False
            elif self.cmbTipoEncuentro2.currentText() == "Fase de Grupos":
                grupos = [chr(i) for i in range(65, 73)]
                grupo = [g for g in grupos if partido in admin.obtener_partidos_grupo(g)]
                grupo = admin.obtener_grupo_codigo(grupo[0])
                if grupo.definido is True:
                    QMessageBox.about(None, "Error!", "El partido se ha definido, no se pueden realizar cambios")
                    return False
            return True
        admin.obtener_lista_partidos_disponibles()#Se carga la lista de partidos disponibles
        admin.obtener_lista_pronosticos()#Se carga la lista de pronosticos
        filaSeleccionada = [dato.text() for dato in self.jgdEditarPronosticos.selectedItems()]#Fila de la tabla seleccioanda
        fecha = datetime.datetime.strptime(filaSeleccionada[0], '%d/%m/%Y %H:%M')#Fecha simulada de ingreso al sistema
        #Se genera una referencia parcial del partido seleccionado
        if filaSeleccionada[3] == "PD":partido = Partido(fecha, filaSeleccionada[1], None)
        else: partido = Partido(fecha, filaSeleccionada[1], filaSeleccionada[3])
        partido = admin.obtener_partido(partido)#Se obtiene el partido seleccionado
        pronostico=admin.obtener_pronosticos(self.participante.cedula)#Se obtienen los pronósticos del participante asociado
        pronostico=[p for p in pronostico if p.id in partido.pronosticos][0]#Se filtran los pronosticos para obtener el pronostico asociado al partido
        accion=accion.text()
        if accion=="Editar Pronóstico":
            if validacion_partido_definido() is False: return
            marcador_pronosticado = self.obtener_marcador(filaSeleccionada[1],filaSeleccionada[3])
            if marcador_pronosticado is None: return
            pronostico.marcador_pronosticado=marcador_pronosticado
            admin.actualizar_lista_pronosticos()
        elif accion == "Eliminar Pronóstico":
            if validacion_partido_definido() is False: return
            partido.pronosticos.remove(pronostico.id)#Se elimina la referencia del pronóstico realizado
            admin.obtener_lista_pronosticos().remove(pronostico)#Se elimina el pronóstico realizado
            admin.actualizar_lista_partidos_disponibles()#Se guardan los cambios en la lista de partidos
            admin.actualizar_lista_pronosticos()#Se guardan los cambios en la lista de pronosticos
        elif accion == "Ver Resultados":
            if partido.partidoDefinido is False:
                QMessageBox.about(None,"¡Información importante!","El partido aún no se ha definido.\n Intentelo de nuevo cuando esté disponible.")
                return
            #Ver resultado
            self.ctr=ctrResultados(partido,pronostico,self)
            self.hide()
        self.editar_buscar_pronostico()#Se actualiza la tabla de pronosticos realizados

    def menuContextualAgregarPronostico(self, posicion):#Menú para la tabla de partidos de fase de grupos
        indices = self.jgdAgregarPronostico.selectedIndexes()#Se obtiene la lista de fila seleccionada
        if indices:
            menu = QMenu()#se instancia el menú
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            menu.addAction(QAction("Colocar Pronóstico", itemsGrupo))
            itemsGrupo.triggered.connect(self.asignar_pronostico)#Se conectan las acciones del menú
            menu.exec(self.jgdAgregarPronostico.viewport().mapToGlobal(posicion))#Se inicia el menú
    def menuContextualEditarPronostico(self, posicion):#Menú para la tabla de partidos de fase de grupos
        indices = self.jgdEditarPronosticos.selectedIndexes()#Se obtiene la lista de fila seleccionada
        if indices:
            menu = QMenu()#se instancia el menú
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            menu.addAction(QAction("Editar Pronóstico", itemsGrupo))
            menu.addAction(QAction("Eliminar Pronóstico", itemsGrupo))
            menu.addAction(QAction("Ver Resultados", itemsGrupo))
            itemsGrupo.triggered.connect(self.editar_pronostico)#Se conectan las acciones del menú
            menu.exec(self.jgdEditarPronosticos.viewport().mapToGlobal(posicion))#Se inicia el menú
    def closeEvent(self, event):
        self.venta_principal.show()
        self.close()
class ctrResultados(QMainWindow,Ui_grbResultados):
    def __init__(self, partido,pronostico,ventanaAnterior,parent=None):
        super(ctrResultados, self).__init__(parent)
        self.setupUi(self)
        self.partido=partido
        self.pronostico=pronostico
        self.ventanaAnterior=ventanaAnterior
        self.actualizar_lbls()
        self.actualizar_tabla()
        self.show()
    def actualizar_lbls(self):
        self.lblPartido.setText("{0} v {1}".format(self.partido.selecciones[0],self.partido.selecciones[1]))
        self.lblMarcadorFinal2.setText("{0}-{1}".format(self.partido.marcador[0],self.partido.marcador[1]))
        self.lblMarcadorPronosticado2.setText("{0}-{1}".format(self.pronostico.marcador_pronosticado[0], self.pronostico.marcador_pronosticado[1]))
        self.lblPartidoAnulado.setVisible(self.partido.anulado)
    def actualizar_tabla(self):
        self.jtbDesgloce.setRowCount(0)
        self.jtbDesgloce.insertRow(0)
        puntos=self.pronostico.puntos
        puntos.append(sum(puntos))
        for i in range(0,len(puntos)):
            self.jtbDesgloce.setItem(0,i,QTableWidgetItem(str(puntos[i])))
    def closeEvent(self,evento):
        self.ventanaAnterior.show()
        self.close()
