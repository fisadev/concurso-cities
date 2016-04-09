# coding: utf-8
# Este programa debe correrse con python 2
from crypt import crypt
from itertools import product


def generar_palabras():
    """
    Generar 'palabras' de hasta 6 caracteres de largo, en minusculas.
    """
    letras = 'abcdefghijklmnopqrstuvwxyz'

    for largo in range(3, 7):
        conjuntos = [letras, ] * largo
        for letras_elegidas in product(*conjuntos):
            palabra = ''.join(letras_elegidas)
            yield palabra


def leer_palabras(path_archivo):
    """
    De un copy-paste de paginas de wikipedia, etc.
    """
    with open(path_archivo) as archivo_palabras:
        return [palabra.strip().lower()[:6]
                for palabra in archivo_palabras.read().split()]


def encontrar_passwords():
    """
    Probar todas las combinaciones de 6 letras, hasheando cada una para ver si
    coinciden con los hashes guardados en los /etc/shadow
    Para el tema de equipos, basicamente fui probando con copiar y pegar
    contenido en texto de distintas paginas de wikipedia en el archivo
    equipos.txt, hasta que con la NBA funciono.
    """
    hashes = [
        ('ox', 'ox45K6RsEUfmQ', generar_palabras()),  # fido
        ('$1$42dJ1xYh', '$1$42dJ1xYh$MfrRke8/Ej3h5.vMtNEhC.', leer_palabras('./colores.txt')),  # white
        ('$6$SZGpKoPi', '$6$SZGpKoPi$GGGqHYKy6PO/H5nvV0AmaGB/5krnxVuz2k2uX81O.CF5nYctE5RlR/rzJQCL3ZsF8yratCRbSR2ZuwKzvve.D0', leer_palabras('./equipos.txt')),  # knicks
    ]

    encontradas = []

    for algo_y_salt, hash_resultado, origen_passwords in hashes:
        for password in origen_passwords:
            if crypt(password, algo_y_salt) == hash_resultado:
                encontradas.append(password)
                break

    return encontradas


print "Respuesta a los puntos a, b, c (instantanea):"
print ', '.join(encontrar_passwords())
