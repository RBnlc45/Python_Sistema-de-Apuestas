#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from PyQt6.QtGui import QIcon, QActionGroup, QAction
from Modelo import PartidoEliminatorio
from Modelo.Partido import Partido
from Vista.partidospy import Ui_frmPartidos
from Vista.actualizacionFechapy import Ui_frmActualizarFecha
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem,QMenu, QInputDialog
from Modelo.Admin import Administrador

admin=Administrador()
class ctrPartidos(QMainWindow,Ui_frmPartidos):
    def __init__(self, ventana_principal,parent=None):
        super(ctrPartidos, self).__init__(parent)
        self.venta_principal=ventana_principal
        self.setupUi(self)
        #Inicilización de componentes
        self.inicializar_botones()
        self.acciones_botones()
        self.asignacion_menus_contextuales()
        self.cmbGrupos.insertItems(0, [chr(i) for i in range(65, 73)])
        self.cmbGruposTablaPosiciones.insertItems(0, [chr(i) for i in range(65, 73)])
        #Mostrar partidos de octavos
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosOctavos,list((admin.obtener_lista_partidos_octavos()).values()))
        #Mostrar partidos de cuartos
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosCuartos,list((admin.obtener_lista_partidos_cuartos()).values()))
        #Mostrar partidos de semifinales
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosSemifinales,list((admin.obtener_lista_partidos_semifinales()).values()))
        #Mostrar partidos de finales
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosFinales,list((admin.obtener_lista_partidos_finales()).values()))

    def acciones_botones(self):
        self.btnAsignar.clicked.connect(self.generar_partidos_grupos)
        self.btnActualizar.clicked.connect(self.actualizar_calendario_grupos)
        self.btnMostrar.clicked.connect(self.tabla_posiciones)
        self.btnDefinirMarcadores.clicked.connect(self.definir_marcadores)
        self.btnDefinirFechas.clicked.connect(self.definir_fechas_partidos_grupo)
        self.btnDefinirFechasOctavos.clicked.connect(self.definir_fechas_octavos)
        self.btnDefinirFaseOctavos.clicked.connect(self.definir_marcadores_octavos)
        self.btnDefinirFechasCuartos.clicked.connect(self.definir_fechas_cuartos)
        self.btnDefinirFaseCuartos.clicked.connect(self.definir_marcadores_cuartos)
        self.btnDefinirFechasSemifinales.clicked.connect(self.definir_fechas_semifinales)
        self.btnDefinirFaseSemifinales.clicked.connect(self.definir_marcadores_semifinales)
        self.btnDefinirFechasFinales.clicked.connect(self.definir_fechas_finales)
        self.btnDefinirFaseFinales.clicked.connect(self.definir_marcadores_finales)
    def inicializar_botones(self):
        self.btnDefinirFechas.setEnabled(False)
        self.btnDefinirMarcadores.setEnabled(False)
        if admin.is_fase_definida(admin.obtener_lista_partidos_grupos(),True) is True:
            self.btnDefinirFechasOctavos.setEnabled(not admin.is_fechas_definidas(admin.obtener_lista_partidos_octavos()))
            self.btnDefinirFaseOctavos.setEnabled(not admin.is_fase_definida(admin.obtener_lista_partidos_octavos()))
        if admin.is_fase_definida(admin.obtener_lista_partidos_octavos()) is True:
            self.btnDefinirFechasCuartos.setEnabled(not admin.is_fechas_definidas(admin.obtener_lista_partidos_cuartos()))
            self.btnDefinirFaseCuartos.setEnabled(not admin.is_fase_definida(admin.obtener_lista_partidos_cuartos()))
        if admin.is_fase_definida(admin.obtener_lista_partidos_cuartos()) is True:
            self.btnDefinirFechasSemifinales.setEnabled(not admin.is_fechas_definidas(admin.obtener_lista_partidos_semifinales()))
            self.btnDefinirFaseSemifinales.setEnabled(not admin.is_fase_definida(admin.obtener_lista_partidos_semifinales()))
        if admin.is_fase_definida(admin.obtener_lista_partidos_semifinales()) is True:
            self.btnDefinirFechasFinales.setEnabled(not admin.is_fechas_definidas(admin.obtener_lista_partidos_finales()))
            self.btnDefinirFaseFinales.setEnabled(not admin.is_fase_definida(admin.obtener_lista_partidos_finales()))
    def asignacion_menus_contextuales(self):
        self.jgdTablaPartidosCuartos.customContextMenuRequested.connect(self.menuContextualCuartos)
        self.jgdTablaPartidosOctavos.customContextMenuRequested.connect(self.menuContextualOctavos)
        self.jgdTablaPartidosSemifinales.customContextMenuRequested.connect(self.menuContextualSemifinales)
        self.jgdTablaPartidosFinales.customContextMenuRequested.connect(self.menuContextualFinales)
    def get_marcador_penales(self,seleccion1,seleccion2):#Devuelve una lista con los marcadores ingresados de un partido de fase Eliminatoria
        marcador = [0, 0]
        marcador_penales = None
        a = QInputDialog.getInt(self, "Marcador tiempo reglamentario","Ingrese el marcador final a favor de " + seleccion1, 0, 0, 50, 1)
        if a[1] == False:  # Se canceló el ingreso
            return None
        marcador[0] = a[0]#Se asigna el número de goles de la selección 1
        a = QInputDialog.getInt(self, "Marcador tiempo reglamentario","Ingrese el marcador final a favor de " + seleccion2, 0, 0, 50, 1)
        if a[1] == False:  # Se canceló el ingreso
            return None
        marcador[1] = a[0]#Se asigna el número de goles de la selección 2
        if marcador[0] == marcador[1]:  # Si hay empate en tiempo reglamentario
            marcador_penales = [0, 0]#Se inicializa la lista con los marcadores en penales
            a = QInputDialog.getInt(self, "Marcador penales", "Ingrese el marcador en penales a favor de " + seleccion1, 0, 0, 50, 1)
            if a[1] == False:  # Se canceló el ingreso
                return None
            marcador_penales[0] = a[0]#Se asigna el número de goles de la selección 1
            a = QInputDialog.getInt(self, "Marcador penales", "Ingrese el marcador en penales a favor de " + seleccion2, 0, 0, 50, 1)
            if a[1] == False:  # Se canceló el ingreso
                return None
            marcador_penales[1] = a[0]#Se asigna el número de goles de la selección 2
            if marcador_penales[0] == marcador_penales[1]:
                QMessageBox.about(None, "Error!", "No puede haber empate en la definición de penales")
                return None
        #Advertencia para determinar si se quiere ingresar el marcador
        msg = QMessageBox.warning(self, "Advertencia", "¿Está seguro en cambiar el marcador? \n ",QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.No:
            return None
        return [marcador,marcador_penales]#Se devuelven los marcadores
    def generar_partidos_grupos(self):
        try:
            admin.generar_partidos_grupos()
            QMessageBox.about(None, "Partidos Generados!", "Los partidos de la fase de grupos se han generado con éxito.")
        except UserWarning:
            QMessageBox.about(None, "Error!", "Para generar automáticamente los partidos, todos los grupos deben tener sus 4 selecciones respectivas")
        except Warning:
            QMessageBox.about(None, "Información!","Ya se han generado los partidos de la fase de grupos.")
    def actualizar_calendario_grupos(self):
        #Se recupera la lista de partidos del grupo escogido
        lista_partidos=admin.obtener_partidos_grupo(self.cmbGrupos.currentText())
        #Se limpia la tabla
        self.jgdTablaPartidosGrupos.clearContents()
        if lista_partidos is not None:#Si existen partidos definidos para ese grupo
            grupo=admin.obtener_grupo_codigo(self.cmbGrupos.currentText())#Se obtiene la instancia del grupo
            self.btnDefinirMarcadores.setEnabled(not(grupo.definido))#Se deshabilita el botón si el grupo está definido
            self.btnDefinirFechas.setEnabled(not(grupo.fechas_definidas))#Se deshabilita el botón si las fechas está definidas
            self.jgdTablaPartidosGrupos.customContextMenuRequested.connect(self.menuContextualGrupos)#Se coloca el menú que se mostrará al hacer clik derecho en la tabla
            lista_partidos_aux=[p for p in lista_partidos if p.fechaInicio is not None] #se filtran los partidos con fecha definida
            lista_partidos_aux=sorted(lista_partidos_aux,key=lambda x:x.fechaInicio)#se ordenan los partidos por fecha
            lista_partidos_aux.extend([p for p in lista_partidos if p.fechaInicio is None])#se colocan los partidos sin fecha definida
            self.mostrar_en_tabla_partidos(self.jgdTablaPartidosGrupos, lista_partidos_aux)#Se manda a mostrar en tabla

    def actualizar_datos_fases(self,tabla,obtener_partido,obtener_lista_partidos,actualizar_partidos,accion):
        def actualizar_fecha():
            seleccion1 = admin.obtener_seleccion(filaSeleccionada[1])
            partido=obtener_partido(seleccion1.pais)
            if partido is None:
                return
            self.ctrlActualizarFecha=ctrActualizacionFecha(partido,self,actualizar_partidos,tabla,obtener_lista_partidos)
        def actualizar_marcador():
            #Se obtiene la referencia al partido específico
            partido=obtener_partido(filaSeleccionada[1],filaSeleccionada[3])
            #Se solicita el marcador
            marcadores=self.get_marcador_penales(filaSeleccionada[1],filaSeleccionada[3])
            if marcadores is None:
                 return
            marcador=marcadores[0]
            marcador_penales=marcadores[1]
            #Se actualiza el marcador del partido
            partido.actualizar_marcador(marcador,marcador_penales)
            #Se actualiza la lista de partidos
            actualizar_partidos()
            #Se actualiza la tabla
            self.mostrar_en_tabla_partidos(tabla,list(partidos.values()))
        def anular_partido():
            seleccion1 = admin.obtener_seleccion(filaSeleccionada[1])
            partido = obtener_partido(seleccion1.pais)
            if partido is None:
                return
            if partido.anulado is True:
                QMessageBox.about(None,"¡Aviso Importante!","El partido ya ha sido anulado")
                return
            partido.anular_partido()#Se manda a anular el partido
            actualizar_partidos()#Se guardan los cambios
            QMessageBox.about(None, "¡Partido anulado éxitosamente!", "El partido ha sido anulado")
        admin.obtener_lista_partidos_disponibles()
        filaSeleccionada = [dato.text() for dato in tabla.selectedItems()]
        partidos=obtener_lista_partidos()
        definicionFase = admin.is_fase_definida(partidos)
        definicionFechas = admin.is_fechas_definidas(partidos)
        if definicionFase is True and accion.text() != "Anular Partido":  # Los octavos de final están definidos
            QMessageBox.about(None, "Fase Definida",  "La fase actual está definida no se puede realizar cambios")
        elif definicionFechas is False and accion.text() == "Actualizar Fecha":
            actualizar_fecha()
        elif definicionFechas is True and accion.text() == "Actualizar Marcador":
            actualizar_marcador()
        elif definicionFechas is False and accion.text() == "Actualizar Marcador":
            QMessageBox.about(None, "Error!", "Las fechas de todos los enfrentamientos de la fase deben estar definidas para poder actualizar los marcadores")
        elif accion.text() == "Anular Partido":
            anular_partido()
    def actualizar_datos_grupos(self,accion):
        filaSeleccionada = [dato.text() for dato in self.jgdTablaPartidosGrupos.selectedItems()]
        def actualizar_fecha():
            #Se obtiene la fecha de la fila seleccionada
            fecha=filaSeleccionada[0]
            #Se obtienen las instancias de selecciones de la fila seleccionada
            seleccion1 = admin.obtener_seleccion(filaSeleccionada[1])
            seleccion2 = admin.obtener_seleccion(filaSeleccionada[3])
            if fecha=="PD":#Si la fecha no está definida
                fecha=None
            else:#Si la fecha se ha definido
                fecha=datetime.datetime.strptime(fecha,'%d/%m/%Y %H:%M')#se obtiene el datetime de la fecha
            partido=Partido(fecha,seleccion1.pais,seleccion2.pais)#se crea una instancia referencial del Partido
            partido=admin.obtener_partido_grupo(partido)#Se busca el partido en la lista de partidos de fase de grupos
            if partido is None:#Si no se encontró el partido
                return
            #Si se encontró el partido
            self.ctrlActualizarFecha=ctrActualizacionFecha(partido,self,admin.actualizar_lista_partidos_grupos)#Se instancia al controlador de la ventana para el ingreso de la fecha
        def actualizar_marcador():
            admin.obtener_lista_partidos_disponibles()
            fecha = filaSeleccionada[0]
            # Se obtienen las instancias de selecciones de la fila seleccionada
            seleccion1 = admin.obtener_seleccion(filaSeleccionada[1])
            seleccion2 = admin.obtener_seleccion(filaSeleccionada[3])
            fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y %H:%M')#Se obtiene la fecha de la fila seleccionada
            partido = Partido(fecha, seleccion1.pais, seleccion2.pais)#Se crea una instancia referencial del partido
            partido = admin.obtener_partido_grupo(partido)# Se busca la instancia del partido
            marcador=[0,0]#Se inicializa el marcador a utilizar
            a=QInputDialog.getInt(self,"Marcador","Ingrese el marcador a favor de "+seleccion1.pais,0,0,50,1)
            if a[1]==False:#Se canceló el ingreso
                return
            marcador[0]=a[0]#Se asigna el primer valor del marcador
            a = QInputDialog.getInt(self, "Marcador", "Ingrese el marcador a favor de " + seleccion2.pais, 0, 0, 50, 1)
            if a[1]==False:#Se canceló el ingreso
                return
            marcador[1] = a[0]#Se asigna el segundo valor del marcador
            #Pregunta de advertencia
            msg = QMessageBox.warning(self, "Advertencia", "¿Está seguro en cambiar el marcador? \n ", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            if msg == QMessageBox.StandardButton.No:#Se cancelo el ingreso del marcador
                return
            #Se actualiza el marcador del partido
            partido.actualizar_marcador(marcador)
            #Se actualiza la lista de partidos
            admin.actualizar_lista_partidos_grupos()
            self.btnActualizar.click()
        def anular_partido():
            # Se obtiene la fecha de la fila seleccionada
            fecha = filaSeleccionada[0]
            seleccion1 = admin.obtener_seleccion(filaSeleccionada[1])
            seleccion2 = admin.obtener_seleccion(filaSeleccionada[3])
            if fecha == "PD":  # Si la fecha no está definida
                fecha = None
            else:  # Si la fecha se ha definido
                fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y %H:%M')  # se obtiene el datetime de la fecha
            partido = Partido(fecha, seleccion1.pais, seleccion2.pais)  # se crea una instancia referencial del Partido
            partido = admin.obtener_partido_grupo(
                partido)  # Se busca el partido en la lista de partidos de fase de grupos
            if partido is None:  # Si no se encontró el partido
                return
            if partido.anulado is True:
                QMessageBox.about(None,"¡Aviso Importante!","El partido ya ha sido anulado")
                return
            partido.anular_partido()#Se manda a anular el partido
            # Se actualiza la lista de partidos
            admin.actualizar_lista_partidos_grupos()
            QMessageBox.about(None, "¡Partido anulado éxitosamente!", "El partido ha sido anulado")
        definicionFase=admin.is_fase_definida(admin.obtener_lista_partidos_grupos(),True)#Se
        grupo = admin.obtener_grupo_codigo(self.cmbGrupos.currentText())#Se obtiene le grupo seleccionado
        if definicionFase is True and accion.text() != "Anular Partido":
            QMessageBox.about(None, "Fase de Grupos Definida","La fase de grupos está definida no se puede realizar cambios")
        elif grupo.fechas_definidas is False and accion.text()=="Actualizar Fecha":
            actualizar_fecha()
        elif grupo.fechas_definidas is True and grupo.definido is False and accion.text()=="Actualizar Marcador":
            actualizar_marcador()
        elif grupo.fechas_definidas is True and accion.text()=="Actualizar Fecha":
            QMessageBox.about(None,"Fechas definidas","Las fechas para este grupo están definidas, no se pueden hacer cambios")
        elif grupo.definido is True and accion.text() == "Actualizar Marcador":
            QMessageBox.about(None, "Marcadores Definidos","Los marcadores de los partidos de este grupo se han definido, no se puede realizar cambios")
        elif grupo.fechas_definidas is False and grupo.definido is False and accion.text()=="Actualizar Marcador":
            QMessageBox.about(None, "Error!","Las fechas deben estar definidas para poder actualizar los marcadores")
        elif accion.text() == "Anular Partido":
            anular_partido()
    def actualizar_datos_octavos(self,accion):
        tabla=self.jgdTablaPartidosOctavos
        obtener_partido=admin.obtener_partido_octavos
        obtener_lista_partidos=admin.obtener_lista_partidos_octavos
        actualizar_partidos=admin.actualizar_partidos_octavos
        self.actualizar_datos_fases(tabla,obtener_partido,obtener_lista_partidos,actualizar_partidos,accion)
    def actualizar_datos_cuartos(self,accion):
        tabla = self.jgdTablaPartidosCuartos
        obtener_partido = admin.obtener_partido_cuartos
        obtener_lista_partidos = admin.obtener_lista_partidos_cuartos
        actualizar_partidos = admin.actualizar_partidos_cuartos
        self.actualizar_datos_fases(tabla, obtener_partido, obtener_lista_partidos, actualizar_partidos, accion)
    def actualizar_datos_semifinales(self,accion):
        tabla = self.jgdTablaPartidosSemifinales
        obtener_partido = admin.obtener_partido_semifinales
        obtener_lista_partidos = admin.obtener_lista_partidos_semifinales
        actualizar_partidos = admin.actualizar_partidos_semifinales
        self.actualizar_datos_fases(tabla, obtener_partido, obtener_lista_partidos, actualizar_partidos, accion)
    def actualizar_datos_finales(self,accion):
        tabla = self.jgdTablaPartidosFinales
        obtener_partido = admin.obtener_partido_finales
        obtener_lista_partidos = admin.obtener_lista_partidos_finales
        actualizar_partidos = admin.actualizar_partidos_finales
        self.actualizar_datos_fases(tabla, obtener_partido, obtener_lista_partidos, actualizar_partidos, accion)
    def definir_fechas_partidos_grupo(self):
        partidos_grupo=admin.obtener_partidos_grupo(self.cmbGrupos.currentText())
        aux=list(filter(lambda x:x.fechaInicio is None,partidos_grupo))
        if len(aux)>0:
            QMessageBox.about(None,"Error!","Todas las fechas de los partidos deben estar definidas para continuar")
        else:
            msg = QMessageBox.warning(self, "Advertencia","¿Está seguro en definir las fechas de los enfrentamientos de este grupo? \n Una vez definidos no se pueden realizar cambios",
                                      QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            if msg == QMessageBox.StandardButton.No:
                return
            grupo=admin.obtener_grupo_codigo(self.cmbGrupos.currentText())
            grupo.fechas_definidas=True
            admin.actualizar_lista_grupos()
            QMessageBox.about(None, "Definición éxitosa", "Las fechas de los enfrentamientos del grupo se han definido")
            self.btnActualizar.click()
    def definir_fechas_fases(self,tabla,limite,lista_partidos,actualizar_partidos,btnFechas):
        partidos = lista_partidos()#lista con los partidos de la fase necesaria
        aux = list(filter(lambda x: x.fechaInicio is None, partidos.values()))#partidos con fechas no definidas
        if len(partidos.values()) < limite:#Dependiendo de la fase, todos los partidos deben ser generados
            QMessageBox.about(None, "Error!", "Todos los encuentros deben estar definidos para continuar")
        elif len(aux) > 0:#No deben existir partidos sin una fecha colocada
            QMessageBox.about(None, "Error!", "Todas las fechas de los partidos deben estar definidas para continuar")
        else:
            msg = QMessageBox.warning(self, "Advertencia", "¿Está seguro en definir las fechas de los enfrentamientos? \n Una vez definidos no se pueden realizar cambios",
                                      QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            if msg == QMessageBox.StandardButton.No:
                return
            admin.definir_fechas(partidos)#Se definen las fechas de todos los enfrentamientos
            actualizar_partidos()
            QMessageBox.about(None, "Definición éxitosa", "Las fechas de los enfrentamientos se han definido")
            self.mostrar_en_tabla_partidos(tabla,list(partidos.values()))
            btnFechas.setEnabled(False)
    def definir_fechas_octavos(self):
        self.definir_fechas_fases(self.jgdTablaPartidosOctavos,8,admin.obtener_lista_partidos_octavos,admin.actualizar_partidos_octavos,self.btnDefinirFechasOctavos)
    def definir_fechas_cuartos(self):
        self.definir_fechas_fases(self.jgdTablaPartidosCuartos, 4, admin.obtener_lista_partidos_cuartos, admin.actualizar_partidos_cuartos, self.btnDefinirFechasCuartos)
    def definir_fechas_semifinales(self):
        self.definir_fechas_fases(self.jgdTablaPartidosSemifinales, 2, admin.obtener_lista_partidos_semifinales, admin.actualizar_partidos_semifinales, self.btnDefinirFechasSemifinales)
    def definir_fechas_finales(self):
        self.definir_fechas_fases(self.jgdTablaPartidosFinales, 2, admin.obtener_lista_partidos_finales, admin.actualizar_partidos_finales, self.btnDefinirFechasFinales)
    def definir_marcadores(self):
        admin.obtener_lista_partidos_disponibles()
        admin.obtener_lista_pronosticos()
        partidos_grupo = admin.obtener_partidos_grupo(self.cmbGrupos.currentText())
        aux = list(filter(lambda x: None in x.marcador, partidos_grupo))
        if len(aux) > 0:
            QMessageBox.about(None, "Error!", "Todos los marcadores deben estar definidos para continuar")
            return
        msg = QMessageBox.warning(self, "Advertencia", "¿Está seguro en definir los marcadores? \n Una vez definidos no se pueden realizar cambios y en caso de existir errores los pronósticos asociados deberán ser anulados sin posibilidad de corrección",
                                  QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.No:  return
        for p in partidos_grupo:  p.partidoDefinido=True
        admin.actualizar_lista_partidos_grupos()
        grupo = admin.obtener_grupo_codigo(self.cmbGrupos.currentText())
        grupo.definido = True
        admin.actualizar_lista_grupos()
        [p.calcular_pronosticos() for p in partidos_grupo]#Se actualizan los pronosticos de los encuentros
        admin.generar_partidos_octavos()
        QMessageBox.about(None, "Definición éxitosa", "Los marcadores de los enfrentamientos del grupo se han definido")
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosOctavos,list((admin.obtener_lista_partidos_octavos()).values()))
        self.btnActualizar.click()
        self.inicializar_botones()
    def definir_marcadores_fases(self,lista_partidos,actualizar_partidos,generar_partidos,btnFase,final=False):
        admin.obtener_lista_partidos_disponibles()
        admin.obtener_lista_pronosticos()
        partidos = lista_partidos()
        aux = list(filter(lambda x: None in x.marcador, partidos.values()))
        if len(aux) > 0:
            QMessageBox.about(None, "Error!", "Todos los marcadores deben estar definidos para continuar")
            return
        msg = QMessageBox.warning(self, "Advertencia","¿Está seguro en definir los marcadores? \n Una vez definidos no se pueden realizar cambios y en caso de existir errores los pronósticos asociados deberán ser anulados sin posibilidad de corrección",
                                  QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.No:
            return
        admin.definir_fase(partidos)#Se definen todos los partidos de la fase
        [p.calcular_pronosticos() for p in partidos.values()]  # Se actualizan los pronosticos de los partidos asociados
        actualizar_partidos()
        if final is False: generar_partidos()
        btnFase.setEnabled(False)
        QMessageBox.about(None, "Definición éxitosa", "Los marcadores de los enfrentamientos se han definido")
        self.inicializar_botones()
    def definir_marcadores_octavos(self):
        self.definir_marcadores_fases(admin.obtener_lista_partidos_octavos,admin.actualizar_partidos_octavos,admin.generar_partidos_cuartos,self.btnDefinirFaseOctavos)
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosCuartos,list((admin.obtener_lista_partidos_cuartos()).values()))
    def definir_marcadores_cuartos(self):
        self.definir_marcadores_fases(admin.obtener_lista_partidos_cuartos, admin.actualizar_partidos_cuartos,  admin.generar_partidos_semifinales, self.btnDefinirFaseCuartos)
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosSemifinales, list((admin.obtener_lista_partidos_semifinales()).values()))
    def definir_marcadores_semifinales(self):
        self.definir_marcadores_fases(admin.obtener_lista_partidos_semifinales, admin.actualizar_partidos_semifinales,admin.generar_partidos_finales, self.btnDefinirFaseSemifinales)
        self.mostrar_en_tabla_partidos(self.jgdTablaPartidosFinales, list((admin.obtener_lista_partidos_finales()).values()))
    def definir_marcadores_finales(self):
        self.definir_marcadores_fases(admin.obtener_lista_partidos_finales, admin.actualizar_partidos_finales, None, self.btnDefinirFaseFinales,True)
    #Manejo de tablas
    def tabla_posiciones(self):
        grupo=admin.obtener_grupo_codigo(self.cmbGruposTablaPosiciones.currentText())
        if grupo is None:#Si no se encuentra el grupo
            return
        grupo_selecciones=admin.obtener_selecciones(grupo.selecciones)
        grupo_selecciones=sorted(grupo_selecciones,key=lambda x:(sum(x.puntos),x.goles) if None not in x.puntos else x.goles,reverse=True)
        self.mostrar_en_tabla_posiciones(self.jgdPosiciones,grupo_selecciones)
    def mostrar_en_tabla_partidos(self,tabla,lista):
        tabla.setRowCount(0)
        if lista is not None:
            for i in range(0,len(lista)):
                tabla.insertRow(i)
                elementos=lista[i].obtener_valores_mostrar()
                tabla.setItem(i,0,QTableWidgetItem(elementos[0]))
                tabla.setItem(i, 1, QTableWidgetItem(QIcon(elementos[1].bandera),elementos[1].pais))
                tabla.setItem(i, 2, QTableWidgetItem(elementos[2]))
                tabla.setItem(i, 3, QTableWidgetItem(QIcon(elementos[3].bandera),elementos[3].pais))
                if isinstance(lista[i],PartidoEliminatorio.PartidoEliminatorio):
                    tabla.setItem(i, 4, QTableWidgetItem(elementos[4]))
    def mostrar_en_tabla_posiciones(self,tabla,lista):
        tabla.clearContents()
        if lista is not None:
            for i in range(0,len(lista)):
                tabla.setItem(i, 0, QTableWidgetItem(QIcon(lista[i].bandera),lista[i].pais))
                tabla.setItem(i, 1, QTableWidgetItem(str(sum(list(filter(lambda x:x is not None,lista[i].puntos))))))
                tabla.setItem(i, 2, QTableWidgetItem(str(lista[i].goles)))



    #Menús Contextuales
    def menuContextualGrupos(self, posicion):#Menú para la tabla de partidos de fase de grupos
        indices = self.jgdTablaPartidosGrupos.selectedIndexes()#Se obtiene la lista de fila seleccionada
        if indices:
            menu = QMenu()#se instancia el menú
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            if admin.obtener_grupo_codigo(self.cmbGrupos.currentText()).definido is not True:#Si el grupo no está definido
                menu.addAction(QAction("Actualizar Fecha", itemsGrupo))
                menu.addAction(QAction("Actualizar Marcador", itemsGrupo))
            else:#Si el grupo está definido
                menu.addAction(QAction("Anular Partido", itemsGrupo))
            itemsGrupo.triggered.connect(self.actualizar_datos_grupos)#Se conectan las acciones del menú
            menu.exec(self.jgdTablaPartidosGrupos.viewport().mapToGlobal(posicion))#Se inicia el menú
    def menuContextualOctavos(self, posicion):#Menú para la tabla de octavos
        indices = self.jgdTablaPartidosOctavos.selectedIndexes()
        if indices:
            menu = QMenu()
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)

            if admin.is_fase_definida(admin.obtener_lista_partidos_octavos()) is not True:#Si la segunda fase no esta definida
                menu.addAction(QAction("Actualizar Fecha", itemsGrupo))
                menu.addAction(QAction("Actualizar Marcador", itemsGrupo))
            else:#Si la segunda fase está definida
                menu.addAction(QAction("Anular Partido", itemsGrupo))
            itemsGrupo.triggered.connect(self.actualizar_datos_octavos)
            menu.exec(self.jgdTablaPartidosOctavos.viewport().mapToGlobal(posicion))
    def menuContextualCuartos(self, posicion):#Menú para la tabla de octavos
        indices = self.jgdTablaPartidosCuartos.selectedIndexes()
        if indices:
            menu = QMenu()
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            if admin.is_fase_definida(admin.obtener_lista_partidos_cuartos()) is not True:#Si la segunda fase no esta definida
                menu.addAction(QAction("Actualizar Fecha", itemsGrupo))
                menu.addAction(QAction("Actualizar Marcador", itemsGrupo))
            else:#Si la segunda fase está definida
                menu.addAction(QAction("Anular Partido", itemsGrupo))
            itemsGrupo.triggered.connect(self.actualizar_datos_cuartos)
            menu.exec(self.jgdTablaPartidosCuartos.viewport().mapToGlobal(posicion))
    def menuContextualSemifinales(self, posicion):#Menú para la tabla de octavos
        indices = self.jgdTablaPartidosSemifinales.selectedIndexes()
        if indices:
            menu = QMenu()
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            if admin.is_fase_definida(admin.obtener_lista_partidos_semifinales()) is not True:#Si la segunda fase no esta definida
                menu.addAction(QAction("Actualizar Fecha", itemsGrupo))
                menu.addAction(QAction("Actualizar Marcador", itemsGrupo))
            else:#Si la segunda fase está definida
                menu.addAction(QAction("Anular Partido", itemsGrupo))
            itemsGrupo.triggered.connect(self.actualizar_datos_semifinales)
            menu.exec(self.jgdTablaPartidosSemifinales.viewport().mapToGlobal(posicion))
    def menuContextualFinales(self, posicion):#Menú para la tabla de octavos
        indices = self.jgdTablaPartidosFinales.selectedIndexes()
        if indices:
            menu = QMenu()
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            if admin.is_fase_definida(admin.obtener_lista_partidos_finales()) is not True:#Si la segunda fase no esta definida
                menu.addAction(QAction("Actualizar Fecha", itemsGrupo))
                menu.addAction(QAction("Actualizar Marcador", itemsGrupo))
            else:#Si la segunda fase está definida
                menu.addAction(QAction("Anular Partido", itemsGrupo))
            itemsGrupo.triggered.connect(self.actualizar_datos_finales)
            menu.exec(self.jgdTablaPartidosFinales.viewport().mapToGlobal(posicion))
    def closeEvent(self,event):
        self.venta_principal.show()
        self.close()

class ctrActualizacionFecha(QMainWindow,Ui_frmActualizarFecha):
    def __init__(self, partido,ventanaAnterior,actualizar_partidos,tabla=None,obtener_partidos=None,parent=None):
        super(ctrActualizacionFecha, self).__init__(parent)
        self.setupUi(self)
        self.partido=partido
        self.ventanaAnterior=ventanaAnterior
        self.actualizar_partidos=actualizar_partidos
        self.tabla=tabla
        self.obtener_partidos=obtener_partidos
        self.brnConfirmar.clicked.connect(self.actualizar)
        self.show()
    def actualizar(self):
        a=QMessageBox.warning(self,"Advertencia","Está seguro en cambiar la fecha?",QMessageBox.StandardButton.Yes,QMessageBox.StandardButton.No)
        if a==QMessageBox.StandardButton.No:
            return
        fecha=str(self.dtpFecha.selectedDate().toPyDate())
        hora=str(self.dtpHora.text())
        fecha_nueva=datetime.datetime.strptime("{0} {1}".format(fecha,hora),'%Y-%m-%d %H:%M')
        self.partido.fechaInicio=fecha_nueva
        self.actualizar_partidos()
        if not isinstance(self.partido, PartidoEliminatorio.PartidoEliminatorio):
            self.ventanaAnterior.btnActualizar.click()
        else:
            self.ventanaAnterior.mostrar_en_tabla_partidos(self.tabla,list((self.obtener_partidos()).values()))
        self.close()
