# coding: utf-8
# Este programa debe correrse con python 2
import math


def leer_coordenadas():
    """
    Leer las coordenadas de los puntos desde el archivo cilindro.asc.
    """
    with open('./cilindro.asc') as archivo_coordenadas:
        return [tuple(float(n) for n in linea.split())
                for linea in archivo_coordenadas.readlines()]


def distancia(punto_a, punto_b, solo_xy=False):
    """
    Calculo de distancia entre puntos.
    """
    xa, ya, za = punto_a
    xb, yb, zb = punto_b

    suma = abs(xa - xb) ** 2 + abs(ya - yb) ** 2
    if not solo_xy:
        suma += abs(za - zb) ** 2

    distancia_calculada = math.sqrt(suma)

    return distancia_calculada


def encontrar_mejor_punto(coordenadas, es_mejor, filtro=None):
    """
    Encontrar el punto que mejor cumpla una determinada condicion, expresada
    como comparacion con otros puntos.
    Opcionalmente se puede especificar un filtro para los puntos.
    """
    mejor_punto = coordenadas[0]
    for punto in coordenadas:
        if es_mejor(punto, mejor_punto) and (filtro is None or filtro(punto)):
            mejor_punto = punto

    return mejor_punto


def obtener_xy_centro(top_tapa_superior, bottom_tapa_inferior):
    """
    Determinar el centro del cilindro en el plano xy, en base a los dos
    extremos verticales encontrados.
    """
    desde_x, hasta_x = sorted((top_tapa_superior[0], bottom_tapa_inferior[0]))
    desde_y, hasta_y = sorted((top_tapa_superior[1], bottom_tapa_inferior[1]))

    x = desde_x + (hasta_x - desde_x) / 2
    y = desde_y + (hasta_y - desde_y) / 2

    return x, y


def deducir_informacion_cilindro():
    """
    Deducir la informacion pedida del cilindro: altura, radio e inclinacion.
    """
    coordenadas = leer_coordenadas()
    top_tapa_superior = encontrar_mejor_punto(coordenadas,
                                              lambda a, b: a[2] > b[2])
    bottom_tapa_inferior = encontrar_mejor_punto(coordenadas,
                                                 lambda a, b: a[2] < b[2])

    z_centro = bottom_tapa_inferior[2] + (top_tapa_superior[2] - bottom_tapa_inferior[2]) / 2
    x_centro, y_centro = obtener_xy_centro(top_tapa_superior,
                                           bottom_tapa_inferior)

    centro = x_centro, y_centro, z_centro

    def mas_descentrado_xy(punto, otro_punto):
        dist_punto = distancia(centro, punto, solo_xy=True)
        dist_otro_punto = distancia(centro, otro_punto, solo_xy=True)
        return dist_punto > dist_otro_punto

    # de la mitad superior, encontrar el punto mas descentrado en el plano xy
    bottom_tapa_superior = encontrar_mejor_punto(coordenadas,
                                                 mas_descentrado_xy,
                                                 lambda a: a[2] >= z_centro)

    altura_cilindro = distancia(bottom_tapa_superior, bottom_tapa_inferior)

    diametro_cilindro = distancia(top_tapa_superior, bottom_tapa_superior)
    radio_cilindro = diametro_cilindro / 2

    # usando pitagoras podemos sacar el angulo de inclinacion, tomando el lado
    # como hipotenusa (inclinada), y la diferencia en el plano xy como cateto
    # opuesto (recto plano)
    diferencia_xy = distancia(bottom_tapa_superior, bottom_tapa_inferior,
                              solo_xy=True)
    inclinacion_cilindro = math.asin(diferencia_xy / altura_cilindro)
    inclinacion_cilindro = math.degrees(inclinacion_cilindro)

    return altura_cilindro, radio_cilindro, inclinacion_cilindro


altura, radio, inclinacion = deducir_informacion_cilindro()
print "Respuesta al punto a (instantaneo):"
print altura
print "Respuesta al punto b (instantaneo):"
print radio
print "Respuesta al punto c (instantaneo):"
print inclinacion

# altura del cilindro
# radio del cilindro
# inclinación del eje del cilindro en radianes con respecto al eje z
