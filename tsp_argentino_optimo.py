# coding: utf-8
import math
from repoze.lru import lru_cache


CIUDADES = {
    'Sunchales': (+0.0, +0.0),
    'Buenos Aires': (+355.8, -405.9),
    'Catamarca': (-467.0, +274.3),
    'Corrientes': (+305.8, +383.6),
    'Cordoba': (-291.0, -53.7),
    'Formosa': (+378.1, +528.2),
    'Jujuy': (-415.1, +750.6),
    'La Plata': (+402.2, -444.8),
    'La Rioja': (-587.5, +170.5),
    'Mendoza': (-808.0, -216.8),
    'Neuquen': (-719.1, -891.4),
    'Parana': (+116.8, -89.0),
    'Posadas': (+632.0, +396.6),
    'Resistencia': (+287.3, +387.3),
    'Rio gallegos': (-852.5, -2301.7),
    'Salta': (-426.2, +683.8),
    'San Juan': (-774.7, -66.7),
    'San Luis': (-531.9, -259.5),
    'Santa Fe': (+96.4,  -77.8),
    'Santa Rosa': (-302.1, -632.0),
    'Santiago del Estero': (-300.2, +350.3),
    'Trelew': (-415.1, -1369.6),
    'Tucuman': (-405.9, +457.8),
    'Ushuaia': (-748.7, -2653.9),
    'Viedma': (-159.4, -1097.1),
}


RESTRICCIONES = set((
    ('Jujuy', 'Salta'),
    ('Resistencia', 'Corrientes'),
    ('Parana', 'Santa Fe'),
    ('Buenos Aires', 'La Plata'),
    ('Mendoza', 'San Juan'),
))


ORIGEN = 'Sunchales'


def cacheada(f):
    """
    Agregar cache a una funcion.
    """
    cache = {}

    def new_f(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    # mantener doc y nombre de la funcion original
    new_f.__doc__ = f.__doc__
    new_f.__name__ = f.__name__

    return new_f


@cacheada
def distancia(ciudad_a, ciudad_b):
    """
    Calculo de distancia entre ciudades, pero con cache.
    """
    if (ciudad_a, ciudad_b) in RESTRICCIONES or (ciudad_b, ciudad_a) in RESTRICCIONES:
        return 9999999999

    xa, ya = CIUDADES[ciudad_a]
    xb, yb = CIUDADES[ciudad_b]

    distancia_calculada = math.sqrt(abs(xa - xb) ** 2 + abs(ya - yb) ** 2)

    return distancia_calculada


def hk():
    """
    Implementacion de algoritmo de Held-Karp para TSP. Encuentra soluciones
    optimas en tiempos bastante razonables para 25 ciudades.
    Fuente para entender el tema:
    http://nbviewer.jupyter.org/url/norvig.com/ipython/TSP.ipynb
    """
    ciudades = set(CIUDADES.keys())

    mejor_camino = None
    largo_mejor_camino = 99999999999

    total = len(ciudades) - 1
    for i, otra_ciudad in enumerate(ciudades):
        if otra_ciudad is not ORIGEN:
            print i + 1, 'de', total
            camino = mejor_segmento(ORIGEN,
                                    tuple(sorted(ciudades - {ORIGEN, otra_ciudad})),
                                    otra_ciudad)
            largo = largo_camino(camino)
            print 'largo encontrado en esta rama:', largo

            if largo < largo_mejor_camino:
                print 'Y es el mejor hasta ahora!'
                mejor_camino = camino
                largo_mejor_camino = largo

    return mejor_camino


@lru_cache(maxsize=2**23)
def mejor_segmento(origen, intermedias, final):
    """
    Encontrar el segmento mas corto que vaya de origen a final, pasando por
    las ciudades intermedias especificadas.
    """
    intermedias = set(intermedias)
    if not intermedias:
        return [origen, final]
    else:
        return min((mejor_segmento(origen,
                                   tuple(sorted(intermedias - {intermedia})),
                                   intermedia) + [final]
                    for intermedia in intermedias),
                   key=largo_segmento)


def largo_segmento(segmento):
    """
    Calcula el largo de un segmento de un camino (solo la distancia entre las
    ciudades que aparecen en el segmento).
    """
    return sum(distancia(segmento[i], segmento[i-1])
               for i in range(1, len(segmento)))


def largo_camino(camino):
    """
    Calcula el largo total de un camino, incluyendo la vuelta a la ciudad de
    origen.
    """
    # lindo truco que se le ocurrio a norvig, lo que sucede aca con el -1
    # (calcula la distancia del retorno)
    return sum(distancia(camino[i], camino[i - 1])
               for i in range(len(camino)))


print "Respuesta al punto a (demora unas cuantas horas):"
print "NOTA: es el camino OPTIMO. En serio. Es el algoritmo Held-Karp, el mejor para encontrar optimos en TSP."
camino_encontrado = hk()
print camino_encontrado
print "Respuesta al punto b (instantanea):"
print largo_camino(camino_encontrado)
