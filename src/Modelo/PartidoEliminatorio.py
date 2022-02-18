#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.Partido import Partido
from Modelo.Seleccion import Seleccion


class PartidoEliminatorio(Partido):
    def __init__(self,fechaInicio,seleccion_1, seleccion_2):
        super(PartidoEliminatorio, self).__init__(fechaInicio,seleccion_1, seleccion_2)
        self.marcador_penales=[None,None]#Marcador en caso de tener empate al final de los 120 minutos reglamentarios

    def actualizar_marcador(self, marcador,marcador_penales=None):
        getGanador = lambda x, y: self.selecciones[0] if x > y else self.selecciones[1] if y > x else None
        if marcador[0]==marcador[1] and marcador_penales is not None:#Empate es el resultado en el tiempo reglamentario
            # Actualiza el ganador del enfrentamiento
            self.ganador = getGanador(marcador_penales[0], marcador_penales[1])
            self.marcador=marcador
            self.marcador_penales=marcador_penales
        else:#No hubo penales
            self.ganador = getGanador(marcador[0], marcador[1])
            self.marcador=marcador
            self.marcador_penales=list()

    def calcular_pronosticos(self):
        from Modelo.Admin import Administrador
        admin = Administrador()
        admin.obtener_lista_pronosticos()
        # Actualización de puntajes de los pronósticos asociados
        pronosticos = [admin.obtener_pronostico(p) for p in self.pronosticos]
        if None not in self.marcador_penales:#Si no hubo penales
            ganador=self.ganador
        else:#Si hubo penales el ganador es el del tiempo reglamentario
            ganador=None
        for p in pronosticos:  # Se recorre la lista de pronosticos
            p.calcular_puntos(self.marcador, self.selecciones, ganador)  # se calculan los puntos obtenidos
        admin.actualizar_lista_pronosticos()

    def obtener_valores_mostrar(self):
        from Modelo.Admin import Administrador
        admin=Administrador()
        seleccion_1 = admin.obtener_seleccion(self.selecciones[0])
        seleccion_2 = admin.obtener_seleccion(self.selecciones[1])
        if None in self.marcador and None in self.marcador_penales:  # todavia no inicia el partido
            marcador = "PD"
            marcador_penales="PD"
        else:
            marcador = "{0}-{1}".format(self.marcador[0], self.marcador[1])
            if len(self.marcador_penales)==0:#No hubo penales
                marcador_penales="NA"
            else:
                marcador_penales = "{0}-{1}".format(self.marcador_penales[0], self.marcador_penales[1])
        if self.fechaInicio is None:
            fecha = "PD"
        else:
            fecha = self.fechaInicio.strftime('%d/%m/%Y %H:%M')
        if seleccion_2 is None:
            seleccion_2 = Seleccion("PD")
        return [fecha, seleccion_1, marcador, seleccion_2,marcador_penales]