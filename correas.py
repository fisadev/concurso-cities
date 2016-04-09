# coding: utf-8
# Este programa debe correrse con python 2
import math


def superposicion_circulos(radio, distancia):
    """
    Calcula el area definida por la superposicion de dos circulos.
    Fuente para entender la logica del calculo:
    http://mathworld.wolfram.com/Circle-CircleIntersection.html
    """
    primer_termino = 2.0 * (radio ** 2.0) * math.acos(distancia / (2.0 * radio))
    segundo_termino = (distancia / 2.0) * math.sqrt(4.0 * (radio ** 2.0) - (distancia ** 2.0))

    area = primer_termino - segundo_termino

    return area


def superposicion_esferas(radio, distancia):
    """
    Calcula el area definida por la superposicion de dos esferas.
    Fuente para entender la logica del calculo:
    http://mathworld.wolfram.com/Sphere-SphereIntersection.html
    """
    area = (1.0 / 12.0) * math.pi * (4.0 * radio + distancia) * ((2.0 * radio - distancia) ** 2.0)

    return area


print "Respuesta al punto a (instantanea):"
print superposicion_circulos(radio=1, distancia=1)
print "Respuesta al punto b (instantanea):"
print superposicion_esferas(radio=1, distancia=1)
