#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.Admin import Administrador
from Modelo.Seleccion import Seleccion

admin=Administrador()
class Partido():
    def __init__(self, fechaInicio,seleccion_1, seleccion_2):
        self.fechaInicio = fechaInicio # fecha y hora en la que se juega el partido
        self.selecciones=[seleccion_1,seleccion_2]
        self.marcador =[None,None]# marcador del partido, clave: pais, valor: número de goles anotados
        self.pronosticos = list()  # Lista con todos los pronosticos asociados a ese partido
        self.ganador = None  # Se inicializa al ganador el cual por defecto es None (empate)
        self.fechaDefinida=False #Indica si el partido tiene definida su fecha
        self.partidoDefinido=False#Indica si el partido tiene definido el marcador
        self.anulado=False#Indica si el partido fue anulado
    def __eq__(self, other):
        return (self.selecciones[0] in other.selecciones and self.selecciones[1] in other.selecciones and self.fechaInicio == other.fechaInicio)
    def actualizar_marcador(self, marcador):
        def cambio_marcador():
            if self.ganador is None:  # Empate en resultado anterior
                seleccion_1.puntos.remove(1)
                seleccion_2.puntos.remove(1)
            else:  # Se asignan 3 puntos al ganador
                if self.ganador == seleccion_1.pais:#ganador anterior es seleccion 1
                    seleccion_1.puntos.remove(3)
                    seleccion_2.puntos.remove(0)
                else:
                    seleccion_2.puntos.remove(3)
                    seleccion_1.puntos.remove(0)
            seleccion_1.goles = seleccion_1.goles - self.marcador[0]
            seleccion_2.goles = seleccion_2.goles - self.marcador[1]
        selecciones=self.selecciones
        # Función anónima para obtener el ganador del enfrentamiento
        getGanador = lambda x, y: selecciones[0] if x > y else selecciones[1] if y > x else None
        # Actualiza el ganador del enfrentamiento
        ganador = getGanador(marcador[0], marcador[1])
        #Actualización de los puntajes de las selecciones asociadas
        seleccion_1 = admin.obtener_seleccion(selecciones[0])
        seleccion_2 = admin.obtener_seleccion(selecciones[1])
        if None not in self.marcador:#Si el marcador ya se ha actualizado antes
            cambio_marcador()
        if ganador is None:#Empate
            seleccion_1.asignar_puntos(1,marcador[0])
            seleccion_2.asignar_puntos(1,marcador[1])
        else:#Se asignan 3 puntos al ganador
            if ganador == seleccion_1.pais:
                seleccion_1.asignar_puntos(3,marcador[0])
                seleccion_2.asignar_puntos(0,marcador[1])
            else:
                seleccion_2.asignar_puntos(3,marcador[1])
                seleccion_1.asignar_puntos(0,marcador[0])
        admin.actualizar_lista_selecciones()
        self.marcador = marcador
        self.ganador=ganador
    def calcular_pronosticos(self):
        # Actualización de puntajes de los pronósticos asociados
        admin.obtener_lista_pronosticos()
        pronosticos = [admin.obtener_pronostico(p) for p in self.pronosticos]
        for p in pronosticos:  # Se recorre la lista de pronosticos
            p.calcular_puntos(self.marcador, self.selecciones, self.ganador)  # se calculan los puntos obtenidos
        admin.actualizar_lista_pronosticos()
    def obtener_valores_mostrar(self):
        seleccion_1 = admin.obtener_seleccion(self.selecciones[0])
        seleccion_2 = admin.obtener_seleccion(self.selecciones[1])
        if None in self.marcador:#todavia no inicia el partido
            marcador="PD"
        else:
            marcador="{0}-{1}".format(self.marcador[0],self.marcador[1])
        if self.fechaInicio is None:
            fecha="PD"
        else:
            fecha=self.fechaInicio.strftime('%d/%m/%Y %H:%M')
        if seleccion_2 is None:
            seleccion_2=Seleccion("PD")
        return [fecha,seleccion_1,marcador,seleccion_2]
    def anular_partido(self):#Método para anular el partido y todos sus pronósticos asociados
        admin.obtener_lista_pronosticos()
        pronosticos = [admin.obtener_pronostico(p) for p in self.pronosticos]
        for p in pronosticos:  # Se recorre la lista de pronosticos
            p.anular_pronostico()  # se anulan los puntos obtenidos
        self.anulado=True#Se anula el partido
        admin.actualizar_lista_pronosticos()