#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.Partido import Partido
from Modelo.Admin import Administrador
class Grupo():
    def __init__(self,codigo):
        self.codigo_grupo=codigo#Código asociado al grupo (letras A...H)
        self.selecciones=list()#lista de selecciones pertenecientes al grupo
        self.definido=False#Indica que para el grupo se han definido las fechas y marcadores para avanzar a la sigueinte fase
        self.fechas_definidas=False#Indica que las fechas de los enfrentamientos en este grupo estan definidas
    def __eq__(self, other):
        return self.codigo_grupo==other.codigo_grupo
    def generar_partidos(self):#Método que genera los enfrentamientos entre los equipos del grupo
        if len(self.selecciones)==4:#Solo se generán los enfrentamientos cuando el grupo esté completo
            #Lista con los pares de paises a enfrentarse, se filtran las coincidencias entre la misma selección
            ls = [(p, q) for p in self.selecciones for q in self.selecciones if p != q]
            #Se filtra la lista de enfrentamientos para contener 1 enfrentamiento entre dos selecciones
            for p in ls:
                if (p[1], p[0]) in ls:
                    ls.remove((p[1], p[0]))
            partidos_grupo=[Partido(None,p[0],p[1]) for p in ls]
            return partidos_grupo
        else:
            #raise Exception("El grupo todavía no está completo")
            raise Exception
    def obtener_clasificados(self):
        selecciones=Administrador().obtener_selecciones(self.selecciones)
        selecciones=sorted(selecciones,key=lambda x:(sum(x.puntos),x.goles),reverse=True)#ordena las selecciones por puntos y número de goles
        return selecciones[0:2]#Devuelve los dos equipos cabecera de grupo