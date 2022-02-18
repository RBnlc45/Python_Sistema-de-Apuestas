#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Pronostico():
    def __init__(self, fecha, participante, marcador):
        self.id=None
        self.fecha = fecha  # fecha en la que se realizó el pronóstico
        self.participante = participante  # Participante que realizó el pronóstico
        self.marcador_pronosticado = marcador  # Marcador que se pronosticó
        self.puntos = list()  # Lista con el desgloce de puntos obtenidos por el pronóstico (lista vacía -> partido no ha iniciado)
        self.anulado=False #Indica si el pronostico está anulado o no
        self.aciertos=list()#Lista con los valores equivalentes de numero de ciertos por numero de puntos del pronostico
    def __eq__(self, otro_pronostico):  # Sobrecarga de operador igual para comparar pronósticos
        return self.id == otro_pronostico.id
    def calcular_puntos(self,marcador_real,selecciones,ganador):
        from Modelo.Admin import Administrador
        admin = Administrador()
        self.puntos = list()  # reseteo de la lista de puntos
        marcador = list(self.marcador_pronosticado)  # lista de dos posiciones(0-goles a favor de pais1) (1-goles a favor de pais2)
        # Funciones anónimas para obtener los puntos para cada tipo de acierto
        getGanador = lambda x, y: selecciones[0] if (x > y) else selecciones[1] if y > x else None  # Devuelve el pais ganador del encuentro en base al marcadoe
        acierto_resultado = lambda x, y: 2 if (getGanador(x, y) is ganador) else 0  # otorga 2 puntos si se acertó el ganador del enfrentamiento
        acierto_marcador = lambda x, y: 1 if (x == marcador_real[0] and y == marcador_real[1]) else 0  # otorga 1 punto si se acertó el marcador del enfrentamiento
        acierto_pleno = lambda x, y: 3 if (x != 0 and y != 0) else 0  # otorga 3 puntos si los puntos de acierto de resultado y acierto de marcador son diferentes de 0
        acierto_goles = lambda x, y, z: 1 if (z != 0 and x + y > 3) else 0  # otorga 1 punto si el puntaje de acierto de marcador es diferente de 0 y las suma de goles es mayor a 3
        acierto_pleno_goles = lambda x, y: 1 if (x != 0 and y != 0) else 0  # otorga 1 punto si los puntos de acierto de goles y acierto pleno no son 0
        acierto_gol_equipo = lambda x, y, z: 0.5 if (z == 0 and (x == marcador_real[0] or y == marcador_real[1])) else 0  # otorga 0.5 puntos si el puntaje de acierto de marcador es cero y el número de goles a favor de cualquier equipo se acertaron
        pego_al_palo = lambda x, y: 0.5 if ((abs(x - marcador_real[0])==1 and abs(y - marcador_real[1])==0) or (abs(y - marcador_real[1])==1 and abs(x - marcador_real[0])==0)) else 0  # otorga 0.5 puntos si el valor absoluto de la resta del marcador pronosticado y el marcador actual es 1
        # Cálculo y asignación de los puntos
        self.puntos.append(acierto_resultado(marcador[0], marcador[1]))
        self.puntos.append(acierto_marcador(marcador[0], marcador[1]))
        self.puntos.append(acierto_pleno(self.puntos[0], self.puntos[1]))
        self.puntos.append(acierto_goles(marcador[0], marcador[1], self.puntos[1]))
        self.puntos.append(acierto_pleno_goles(self.puntos[2], self.puntos[3]))
        self.puntos.append(acierto_gol_equipo(marcador[0], marcador[1], self.puntos[1]))
        self.puntos.append(pego_al_palo(marcador[0], marcador[1]))
        participante = admin.obtener_participante(self.participante)
        self.aciertos=self.desgloce_aciertos()
        participante.agregar_puntos(self.aciertos)
        admin.actualizar_lista_participantes()
        admin.actualizar_lista_pronosticos()
    def anular_pronostico(self):
        from Modelo.Admin import Administrador
        admin=Administrador()
        admin.obtener_lista_participantes()
        admin.obtener_lista_pronosticos()
        participante=admin.obtener_participante(self.participante)
        participante.agregar_puntos(list(map(lambda x:-x,self.aciertos)))#Se restan los valores de los puntos del participante
        self.puntos=[0,0,0,0,0,0,0]#Se enceran los puntos obtenidos
        self.anulado=True
        admin.actualizar_lista_participantes()
        admin.actualizar_lista_pronosticos()
    def desgloce_aciertos(self):
        desgloce=[0,0,0,0,0,0,0,0,0]
        #Posibles puntos obtenidos en un pronóstico
        pt=[8,6,3,2.5,2,1,0.5]
        desgloce[0]=sum(self.puntos)#Puntos ha asignar
        try:
            index=pt.index(desgloce[0])
            desgloce[index + 1] = 1
        except:
            pass
        desgloce[-1]=1#Indica el aumento en el número de pronosticos
        return desgloce
