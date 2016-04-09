# coding: utf-8
# Este programa debe correrse con python 2 (o con pypy si se desea una mejora
# leve de velocidad)


def recorrer_fibonacci(posicion):
    """
    Obtener los numeros de la secuencia de fibonacci hasta la posicion
    especificada.
    Hecho con enfoque iterativo y no recursivo, para poder usar un generador y
    asi no mantener listas enteras ni recalcular cosas innecesariamente.
    """
    a, b = 1, 1
    yield a
    yield b
    for _ in xrange(2, posicion):
        a, b = b, a + b
        yield b


def es_primo(numero):
    """
    Determina si un numero es o no primo. Asume que es un numero entero
    positivo.
    """
    if numero <= 3:
        return True
    elif numero % 2 == 0 or numero % 3 == 0:
        return False

    divisor = 5
    while divisor**2 <= numero:
        if numero % divisor == 0 or numero % (divisor + 2) == 0:
            return False
        divisor += 6
    return True


def resolver_punto_a():
    """
    Encontrar primos en los primeros 90 numeros de fibonacci.
    """
    return [posicion + 1
            for posicion, numero in enumerate(recorrer_fibonacci(90))
            if es_primo(numero)]


def resolver_punto_b():
    """
    Determinar la cantidad de cifras del numero 1477 de la serie de fibonacci.
    """
    return len(str(list(recorrer_fibonacci(1477))[-1]))


print "Respuesta al punto a (demora unos 2 segundos con pypy, o unos 10 segundos con python 2):"
print resolver_punto_a()
print "Respuesta al punto b (instantanea):"
print resolver_punto_b()
