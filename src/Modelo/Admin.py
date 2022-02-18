#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
class AdministradorMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Administrador(metaclass=AdministradorMeta):
    def __init__(self):
        self.listaSelecciones=None#Lista con todas las selecciones del evento
        self.listaGrupos=None#Lista con todos lo grupos del evento
        self.listaPartidosGrupos=None#Lista con todos los grupos
        self.listaPartidosOctavos=None
        self.listaPartidosCuartos=None
        self.listaPartidosSemifinales=None
        self.listaPartidosFinales = None
        self.listaParticipantes=None
        self.listaPronosticos = None
        self.listaPartidosDisponibles=None
        self.premio = None
    #Funciones para manipular lista de Selecciones
    def obtener_lista_selecciones(self):#En caso de inicializar la clase Administrador se lee de archivos la lista de selecciones
        self.listaSelecciones = self.recuperar_estructura("../Datos/selecciones.dat")
        return self.listaSelecciones
    def actualizar_lista_selecciones(self,lista=None):
        if lista is not None:
            self.listaSelecciones=lista
        self.listaSelecciones=sorted(self.listaSelecciones, key=lambda x: x.pais)  # Se ordena por el nombre
        self.guardar_estructura("../Datos/selecciones.dat",self.listaSelecciones)
    def obtener_seleccion(self,seleccion_pais):#Se devuelve la referencia a la selección en base al pais ingresado
        try:
            if self.listaSelecciones is None: self.obtener_lista_selecciones()
            aux=list(filter(lambda x: seleccion_pais==x.pais,self.listaSelecciones))
            return aux[0]
        except:
            return None
    def obtener_selecciones(self,lista_paises):#lista_paises: lista con los nombres de los paises que se desean buscar
        try:
            self.obtener_lista_selecciones()
            aux = list(filter(lambda x: x.pais in lista_paises,self.listaSelecciones))
            return aux
        except:
            return None
    #Funciones para manipular la lista de grupos
    def obtener_lista_grupos(self):
        if self.listaGrupos is None:
            self.listaGrupos = self.recuperar_estructura("../Datos/grupos.dat")
        return self.listaGrupos
    def obtener_grupo_pais(self,pais):#Devuelve el grupo de una seleccion especifica
        try:
            if self.listaGrupos is None: self.obtener_lista_grupos()
            aux=list(filter(lambda x:pais in x.selecciones,self.listaGrupos))
            return aux[0]
        except:
            return None
    def obtener_grupo_codigo(self,codigo):#Devuelve el grupo en base al codigo (A,B...)
        try:
            if self.listaGrupos is None: self.obtener_lista_grupos()
            aux=list(filter(lambda x:codigo==x.codigo_grupo,self.listaGrupos))
            return aux[0]
        except:
            return None
    def agregar_grupo(self,grupo):
        if self.listaGrupos is None: self.obtener_lista_grupos()
        self.listaGrupos.append(grupo)
        self.guardar_estructura("../Datos/grupos.dat", self.listaGrupos)
    def actualizar_lista_grupos(self,lista=None):
        if lista is not None:
            self.listaGrupos=lista
        self.listaGrupos=sorted(self.listaGrupos,key=lambda x:x.codigo_grupo)
        self.guardar_estructura("../Datos/grupos.dat", self.listaGrupos)

    #Funciones para manipular lista de partidos fase de grupos
    def obtener_lista_partidos_grupos(self):
        if self.listaPartidosGrupos is None:
            self.listaPartidosGrupos = self.recuperar_estructura("../Datos/partidos_grupo.dat")
        return self.listaPartidosGrupos
    def obtener_partidos_grupo_pais(self,seleccion):#Devuelve la lista de partidos jugados por un pais especifico
        if self.listaPartidosGrupos is None: self.obtener_lista_partidos_grupos()
        grupo=self.obtener_grupo_pais(seleccion)
        lista_partidos=self.listaPartidosGrupos.get(grupo.codigo_grupo)
        if lista_partidos is None:
           lista_partidos=list()
        aux=list(filter(lambda x:seleccion in x.selecciones,lista_partidos))
        return aux
    def obtener_partidos_grupo(self,codigo_grupo):#Devuelve la lista de partidos jugados por un pais especifico
        grupo=self.obtener_grupo_codigo(codigo_grupo)
        if grupo is None:
            return None
        if self.listaPartidosGrupos is None: self.obtener_lista_partidos_grupos()
        lista_partidos=self.listaPartidosGrupos.get(grupo.codigo_grupo)
        return lista_partidos
    def obtener_partido_grupo(self,partido):
        try:
            self.obtener_lista_partidos_grupos()
            aux=[p for p in [g for g in self.listaPartidosGrupos.values()] if partido in p]
            aux=aux[0]
            return aux[aux.index(partido)]
        except:
            return None
    def agregar_partidos_grupos(self,partidos,grupo):#Agrega como clave el codigo de grupo y valor la lista de partidos
        if self.listaPartidosGrupos is None: self.obtener_lista_partidos_grupos()
        self.listaPartidosGrupos.update(zip([grupo],[partidos]))
        self.guardar_estructura("../Datos/partidos_grupo.dat",self.listaPartidosGrupos)
    def generar_partidos_grupos(self):
        self.obtener_lista_grupos()
        self.obtener_lista_partidos_grupos()
        grupos_listos=list(self.listaPartidosGrupos.keys())
        if len(grupos_listos)==8: raise Warning
        if len(self.listaGrupos)==0:raise UserWarning
        for g in self.listaGrupos:#Se recorren los grupos que se tienen
            if g.codigo_grupo not in grupos_listos:#Solo se emparejan los grupos que todavía no están listos
                try:
                    partidos=g.generar_partidos()
                    self.agregar_partidos_grupos(partidos,g.codigo_grupo)
                except:#Si alguno de los grupos no está completo no se emparejan sus selecciones
                    raise UserWarning()
    def actualizar_lista_partidos_grupos(self,lista=None):
        if lista is not None:
            self.listaPartidosGrupos = lista
        self.guardar_estructura("../Datos/partidos_grupo.dat", self.listaPartidosGrupos)
    #Funciones para manejar la lista de partidos de octavos
    def obtener_lista_partidos_octavos(self):
        self.listaPartidosOctavos = self.recuperar_estructura("../Datos/partidos_octavos.dat")
        return self.listaPartidosOctavos
    def obtener_partido_octavos(self,seleccion_1,seleccion_2=None):
        if seleccion_2 is None:
            try:#Busca un partido de una selección
                aux=[p for p in list(self.listaPartidosOctavos.values()) if seleccion_1 in p.selecciones]
                return aux[0]
            except:
                return None
        else:#Busca un partido entre dos selecciones
            try:
                aux=[p for p in self.listaPartidosOctavos.values() if seleccion_1 in p.selecciones and seleccion_2 in p.selecciones]
                return aux[0]
            except:
                return None
    def obtener_partido_octavos_codigo(self,codigo_partido):
        if self.listaPartidosOctavos is None: self.obtener_lista_partidos_octavos()
        try:
            partido=self.listaPartidosOctavos.get(codigo_partido)
            return partido
        except:
            return None
    def actualizar_partidos_octavos(self,lista=None):
        if lista is not None:
            self.listaPartidosOctavos=lista
        self.guardar_estructura("../Datos/partidos_octavos.dat", self.listaPartidosOctavos)
    def generar_partidos_octavos(self):
        self.obtener_lista_grupos()
        self.obtener_lista_partidos_octavos()
        #Se generan los pares de grupos para los enfrentamientos
        grupos_emparejados = list(zip([self.listaGrupos[i] for i in range(0, 8, 2)], [self.listaGrupos[i] for i in range(1, 8, 2)]))
        #Se filtran los grupos que estan definidos, y ya tienen sus encuentros formados
        grupos_emparejados_nodefinidos=list(filter(lambda x: (x[0].definido or x[1].definido) and not(x[0].definido and x[1].definido) ,grupos_emparejados))
        grupos_emparejados_definidos=list(filter(lambda x: x[0].definido and x[1].definido,grupos_emparejados))
        for p in grupos_emparejados_nodefinidos:
            codigo_grupo=p[0].codigo_grupo+p[1].codigo_grupo
            if p[0].definido:  # Primer grupo si esta definido
                g_definido=p[0]
            else:
                g_definido = p[1]
            c = g_definido.obtener_clasificados()  # Selecciones clasificadas del grupo definido
            from Modelo.PartidoEliminatorio import PartidoEliminatorio
            self.listaPartidosOctavos.update(dict(zip(["{0}1".format(codigo_grupo)], [PartidoEliminatorio(None, c[0].pais, None)])))
            self.listaPartidosOctavos.update(dict(zip(["{0}2".format(codigo_grupo)], [PartidoEliminatorio(None, c[1].pais, None)])))
        for p in grupos_emparejados_definidos:# Se actualizan los partidos con solo un equipo definido
            codigo_grupo=p[0].codigo_grupo+p[1].codigo_grupo
            #Se obtienen los clasificados de ambos grupos
            c1 = p[0].obtener_clasificados()
            c2 = p[1].obtener_clasificados()
            partido1=self.obtener_partido_octavos_codigo(codigo_grupo+"1")
            partido2 = self.obtener_partido_octavos_codigo(codigo_grupo + "2")
            if None not in partido1.selecciones and None not in partido2.selecciones:#Si el partido ya está definido
                pass
            elif partido1.selecciones[0] in p[0].selecciones:#Si el grupo previamente definido era el grupo p[0]
                partido1.selecciones[1]= c2[1].pais
                partido2.selecciones[1] = c2[0].pais
            else:
                partido1.selecciones[1] = c1[1].pais
                partido2.selecciones[1] = c1[0].pais
        self.actualizar_partidos_octavos()
    #Funciones para manejar la lista de partidos de cuartos
    def obtener_lista_partidos_cuartos(self):
        self.listaPartidosCuartos = self.recuperar_estructura("../Datos/partidos_cuartos.dat")
        return self.listaPartidosCuartos
    def obtener_partido_cuartos(self,seleccion_1,seleccion_2=None):
        if seleccion_2 is None:
            try:#Busca un partido de una selección
                aux=[p for p in list(self.listaPartidosCuartos.values()) if seleccion_1 in p.selecciones]
                return aux[0]
            except:
                return None
        else:#Busca un partido entre dos selecciones
            try:
                aux=[p for p in self.listaPartidosCuartos.values() if seleccion_1 in p.selecciones and seleccion_2 in p.selecciones]
                return aux[0]
            except:
                return None
    def actualizar_partidos_cuartos(self,lista=None):
        if lista is not None:
            self.listaPartidosCuartos=lista
        self.guardar_estructura("../Datos/partidos_cuartos.dat", self.listaPartidosCuartos)
    def generar_partidos_cuartos(self):
        self.obtener_lista_partidos_octavos()
        partidos=list()
        partidos.append(((self.listaPartidosOctavos.get("AB1")).ganador,(self.listaPartidosOctavos.get("CD1")).ganador))
        partidos.append(((self.listaPartidosOctavos.get("EF1")).ganador, (self.listaPartidosOctavos.get("GH1")).ganador))
        partidos.append(((self.listaPartidosOctavos.get("AB2")).ganador, (self.listaPartidosOctavos.get("CD2")).ganador))
        partidos.append(((self.listaPartidosOctavos.get("EF2")).ganador, (self.listaPartidosOctavos.get("GH2")).ganador))
        from Modelo.PartidoEliminatorio import PartidoEliminatorio
        partidos=[PartidoEliminatorio(None,p[0],p[1]) for p in partidos]
        self.listaPartidosCuartos=dict(zip(["A","B","C","D"],partidos))
        self.actualizar_partidos_cuartos()
    #Funciones para manejar la lista de partidos de semifinales
    def obtener_lista_partidos_semifinales(self):
        self.listaPartidosSemifinales = self.recuperar_estructura("../Datos/partidos_semifinales.dat")
        return self.listaPartidosSemifinales
    def obtener_partido_semifinales(self,seleccion_1,seleccion_2=None):
        if seleccion_2 is None:
            try:#Busca un partido de una selección
                aux=[p for p in list(self.listaPartidosSemifinales.values()) if seleccion_1 in p.selecciones]
                return aux[0]
            except:
                return None
        else:#Busca un partido entre dos selecciones
            try:
                aux=[p for p in self.listaPartidosSemifinales.values() if seleccion_1 in p.selecciones and seleccion_2 in p.selecciones]
                return aux[0]
            except:
                return None
    def actualizar_partidos_semifinales(self,lista=None):
        if lista is not None:
            self.listaPartidosSemifinales=lista
        self.guardar_estructura("../Datos/partidos_semifinales.dat", self.listaPartidosSemifinales)
    def generar_partidos_semifinales(self):
        self.obtener_lista_partidos_cuartos()
        partidos=list()
        partidos.append(((self.listaPartidosCuartos.get("A")).ganador,(self.listaPartidosCuartos.get("B")).ganador))
        partidos.append(((self.listaPartidosCuartos.get("C")).ganador, (self.listaPartidosCuartos.get("D")).ganador))
        from Modelo.PartidoEliminatorio import PartidoEliminatorio
        partidos=[PartidoEliminatorio(None,p[0],p[1]) for p in partidos]
        self.listaPartidosSemifinales=dict(zip(["A","B"],partidos))
        self.actualizar_partidos_semifinales()
    #Funciones para manejar la lista de partidos de final y tercer lugar
    def obtener_lista_partidos_finales(self):
        self.listaPartidosFinales = self.recuperar_estructura("../Datos/partidos_finales.dat")
        return self.listaPartidosFinales
    def obtener_partido_finales(self, seleccion_1, seleccion_2=None):
        if seleccion_2 is None:
            try:  # Busca un partido de una selección
                aux = [p for p in list(self.listaPartidosFinales.values()) if seleccion_1 in p.selecciones]
                return aux[0]
            except:
                return None
        else:  # Busca un partido entre dos selecciones
            try:
                aux = [p for p in self.listaPartidosFinales.values() if
                       seleccion_1 in p.selecciones and seleccion_2 in p.selecciones]
                return aux[0]
            except:
                return None
    def actualizar_partidos_finales(self, lista=None):
        if lista is not None:
            self.listaPartidosFinales = lista
        self.guardar_estructura("../Datos/partidos_finales.dat",self.listaPartidosFinales)
    def generar_partidos_finales(self):
        self.obtener_lista_partidos_semifinales()
        partidos = list()
        partido1=self.listaPartidosSemifinales.get("A")
        partido2=self.listaPartidosSemifinales.get("B")
        partidos.append((partido1.ganador, partido2.ganador))
        partidos.append((([p for p in partido1.selecciones if p!=partido1.ganador])[0],([p for p in partido2.selecciones if p!=partido2.ganador])[0]))
        from Modelo.PartidoEliminatorio import PartidoEliminatorio
        partidos = [PartidoEliminatorio(None, p[0], p[1]) for p in partidos]
        self.listaPartidosFinales = dict(zip(["A", "B"], partidos))
        self.actualizar_partidos_finales()
    #Funciones para obtener y manipular todos los partidos disponibles
    def obtener_lista_partidos_disponibles(self):#Devuelve la lista con todos los partidos que está disponibles
        self.obtener_lista_partidos_finales()
        self.obtener_lista_partidos_semifinales()
        self.obtener_lista_partidos_cuartos()
        self.obtener_lista_partidos_octavos()
        self.obtener_lista_partidos_grupos()
        self.listaPartidosDisponibles=list()
        partidos=list(self.listaPartidosGrupos.values())
        for i in range(0,len(partidos)):
            self.listaPartidosDisponibles.extend(partidos[i])
        self.listaPartidosDisponibles.extend(list(self.listaPartidosOctavos.values()))
        self.listaPartidosDisponibles.extend(list(self.listaPartidosCuartos.values()))
        self.listaPartidosDisponibles.extend(list(self.listaPartidosSemifinales.values()))
        self.listaPartidosDisponibles.extend(list(self.listaPartidosFinales.values()))
    def actualizar_lista_partidos_disponibles(self):#Devuelve la lista con todos los partidos que está disponibles
        self.actualizar_partidos_finales()
        self.actualizar_partidos_semifinales()
        self.actualizar_partidos_cuartos()
        self.actualizar_partidos_octavos()
        self.actualizar_lista_partidos_grupos()
    def obtener_partido(self,partido):
        self.obtener_lista_partidos_disponibles()
        try:
            aux=[p for p in self.listaPartidosDisponibles if p==partido]
            return aux[0]
        except:
            return None
    #Funciones para manipular lista de participantes
    def obtener_lista_participantes(self):  # En caso de inicializar la clase Administrador se lee de archivos la lista de selecciones
        if self.listaParticipantes is None:
            self.listaParticipantes = self.recuperar_estructura("../Datos/participantes.dat")
        return self.listaParticipantes
    def actualizar_lista_participantes(self, lista=None):
        if lista is not None:
            self.listaParticipantes = lista
        self.listaParticipantes = sorted(self.listaParticipantes, key=lambda x: x.nombre)  # Se ordena por el nombre
        self.guardar_estructura("../Datos/participantes.dat", self.listaParticipantes)
    def obtener_participante(self,cedula):  # lista_paises: lista con los nombres de los paises que se desean buscar
        try:
            self.obtener_lista_participantes()
            aux = list(filter(lambda x: x.cedula==cedula, self.listaParticipantes))
            return aux[0]
        except:
            return None
    def agregar_participante(self, participante):  # seleccion:nombre de
        self.listaParticipantes.append(participante)
        self.listaParticipantes = sorted(self.listaParticipantes, key=lambda x: x.nombre)  # Se ordena por el nombre
        self.guardar_estructura("../Datos/participantes.dat", self.listaParticipantes)  # Se guarda la seleccion
    #Funciones para manipular lista de pronosticos
    def obtener_lista_pronosticos(self):  # En caso de inicializar la clase Administrador se lee de archivos la lista de selecciones
        if self.listaPronosticos is None:
            self.listaPronosticos = self.recuperar_estructura("../Datos/pronosticos.dat")
        return self.listaPronosticos
    def actualizar_lista_pronosticos(self, lista=None):
        if lista is not None:
            self.listaPronosticos = lista
        self.listaPronosticos = sorted(self.listaPronosticos, key=lambda x: x.id)  # Se ordena por el nombre
        self.guardar_estructura("../Datos/pronosticos.dat", self.listaPronosticos)
    def obtener_pronostico(self,id):  # lista_paises: lista con los nombres de los paises que se desean buscar
        try:
            aux = list(filter(lambda x: x.id==id, self.listaPronosticos))
            return aux[0]
        except:
            return None
    def obtener_pronosticos(self,cedula):  # lista_paises: lista con los nombres de los paises que se desean buscar
        try:
            aux = list(filter(lambda x: x.participante==cedula, self.listaPronosticos))
            return aux
        except:
            return None
    def agregar_pronostico(self, pronostico):
        if len(self.listaPronosticos)==0:
            pronostico.id=1
        else:
            pronostico.id=self.listaPronosticos[-1].id+1#Autoincremental
        self.listaPronosticos.append(pronostico)
        self.actualizar_lista_pronosticos()
        """self.listaPronosticos = sorted(self.listaPronosticos, key=lambda x: x.id)  # Se ordena por el nombre
        self.guardar_estructura("../Datos/pronosticos.dat", self.listaPronosticos)  # Se guarda la seleccion"""
    def obtener_partido_pronostico(self,id_pronostico):
        try:
            for p in self.listaPartidosDisponibles:
                if id_pronostico in p.pronosticos:
                    return p
            return None
        except:
            return None
    #Funciones para definir las fechas de partidos y para definir los marcadores de los partidos
    def is_fechas_definidas(self,partidos,grupos=False):
        if len(partidos.items())==0:
            return False
        elif grupos is False:
            partidos = partidos.values()
        else:#Para fase de grupos, partidos debe ser la lista de listas con todos los partidos de la fase de grupos
            partidos = partidos.values()
            aux=list()
            [aux.extend(p) for p in partidos]
            partidos=aux
        partidos = [p for p in partidos if p.fechaDefinida is False]
        return len(partidos)==0#False: las fechas de los partidos no estan definidas
    def is_fase_definida(self,partidos,grupos=False):
        if len(partidos.items())==0:
            return False
        elif grupos is False:
            partidos = partidos.values()
        else:#Para fase de grupos, partidos debe ser la lista de listas con todos los partidos de la fase de grupos
            partidos = partidos.values()
            aux=list()
            [aux.extend(p) for p in partidos]
            partidos=aux
        partidos = [p for p in partidos if p.partidoDefinido is False]
        return len(partidos)==0#False: las fechas de los partidos no estan definidas
    def definir_fechas(self,partidos,grupos=False):
        if grupos is False:
            partidos = partidos.values()
        else:#Para fase de grupos, partidos debe ser la lista de listas con todos los partidos de la fase de grupos
            partidos = partidos.values()
            aux=list()
            [aux.extend(p) for p in partidos]
            partidos=aux
        for p in partidos:
            p.fechaDefinida = True
    def definir_fase(self,partidos,grupos=False):
        if grupos is False:
            partidos = partidos.values()
        else:#Para fase de grupos, partidos debe ser la lista de listas con todos los partidos de la fase de grupos
            partidos = partidos.values()
            aux=list()
            [aux.extend(p) for p in partidos]
            partidos=aux
        for p in partidos:
            p.partidoDefinido=True
    #Funciones para manipular la lista de premios
    def obtener_premio(self):
        #Premio es una lista de listas con un valor correspondiente al monto del premio en la primera posición, en la segunda un monto acumulado y en la tercera posición una lista con los ganadores asignados
        if self.premio is None:
            self.premio = self.recuperar_estructura("../Datos/premio.dat")#Lista de premios
            if len(self.premio)==0:
                self.premio=[0,0,[]]#Se inicializa la lista con los valores necesarios para la operación
        return self.premio
    def premio_agregar_monto(self, monto):
        self.premio[1]=self.premio[1]+monto#Se acumula el monto indicado
        self.actualizar_premio()
    def premio_cambiar_precio(self, precio):
        self.premio[0]=precio#Se actualiza el precio por participación de usuario
        self.actualizar_premio()
    def actualizar_premio(self):
        self.guardar_estructura("../Datos/premio.dat", self.premio)
    #Funciones para guardar y recuperar contenido de los archivos
    def recuperar_estructura(self,archivo):
        opciones=["../Datos/partidos_grupo.dat","../Datos/partidos_octavos.dat","../Datos/partidos_cuartos.dat" ,"../Datos/partidos_semifinales.dat" ,"../Datos/partidos_finales.dat"]
        try:
            with open(archivo, "rb") as file:
                if archivo in opciones:
                    return dict(pickle.load(file))
                else:
                    return list(pickle.load(file))
        except:
            if archivo in opciones:
                return dict()
            else:
                return list()
    def guardar_estructura(self,archivo, estructura):
        with open(archivo, "wb") as file:
            pickle.dump(estructura, file, pickle.HIGHEST_PROTOCOL)
