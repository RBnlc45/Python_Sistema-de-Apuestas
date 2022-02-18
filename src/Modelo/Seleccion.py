#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Seleccion():
    def __init__(self, nombre):
        self.pais = nombre
        self.bandera = "../Icons/paises/{0}.png".format(nombre.lower().replace(" ", ""))
        self.puntos=list()#lista de puntos por partido jugados
        self.goles=0#Número de goles anotados por la selección en la
    def __eq__(self, other):#Sobrecarga de operador = para comparar selecciones
        return self.pais.lower() == other.pais.lower()
    def asignar_puntos(self,puntos,goles):
        self.puntos.append(puntos)
        self.goles=self.goles+goles
