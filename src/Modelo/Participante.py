#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Participante():
    def __init__(self, cedula,nombre, apellido, direccion,telefono):
        self.cedula=cedula
        self.nombre = nombre  # Nombre del participante
        self.apellido = apellido  # Apellido del participante
        self.telefono = telefono  # Teléfono del participante
        self.direccion = direccion  # Dirección del participante
        self.puntos=[0,0,0,0,0,0,0,0,0]
        #(aciertos de 8 puntos, aciertos de 6 puntos, aciertos de 3 puntos, aciertos de 2.5 puntos, aciertos de 2 puntos, aciertos de 1 punto,bonificaciones de 0.5 puntos,numero de pronosticos)
    def __eq__(self, other):#Compara participantes por el número de cédula
        return self.cedula==other.cedula
    def agregar_puntos(self,puntos):#Acumula los puntos ganados por los pronósticos realizados
        self.puntos=[self.puntos[i]+puntos[i] for i in range(0,9)]



