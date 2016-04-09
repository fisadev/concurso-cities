# coding: utf-8
# Este programa debe correrse con python 2
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


##############################################################
# implementacion de MST TSP hecha por Peter Norvig, sacada de:
# http://nbviewer.jupyter.org/url/norvig.com/ipython/TSP.ipynb


def altered_mst_tsp(cities):
    return alter_tour(mst_tsp(cities))


def alter_tour(tour):
    "Try to alter tour for the better by reversing segments."
    original_length = tour_length(tour)
    for (start, end) in all_segments(len(tour)):
        reverse_segment_if_better(tour, start, end)
    # If we made an improvement, then try again; else stop and return tour.
    if tour_length(tour) < original_length:
        return alter_tour(tour)
    return tour


def tour_length(tour):
    "The total of distances between each pair of consecutive cities in the tour."
    return sum(distance(tour[i], tour[i-1])
               for i in range(len(tour)))


def reverse_segment_if_better(tour, i, j):
    "If reversing tour[i:j] would make the tour shorter, then do it."
    # Given tour [...A-B...C-D...], consider reversing B...C to get [...A-C...B-D...]
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    # Are old edges (AB + CD) longer than new ones (AC + BD)? If so, reverse segment.
    if distance(A, B) + distance(C, D) > distance(A, C) + distance(B, D):
        tour[i:j] = reversed(tour[i:j])


def all_segments(N):
    "Return (start, end) pairs of indexes that form segments of tour of length N."
    return [(start, start + length)
            for length in range(N, 2-1, -1)
            for start in range(N - length + 1)]


def mst_tsp(cities):
    "Create a minimum spanning tree and walk it in pre-order, omitting duplicates."
    return preorder_traversal(tree=mst(cities), root=first(cities))


def preorder_traversal(tree, root):
    "Traverse tree in pre-order, starting at root of tree."
    result = [root]
    for child in tree.get(root, ()):
        result.extend(preorder_traversal(tree, child))
    return result


def first(collection):
    "Start iterating over collection, and return the first element."
    return next(iter(collection))


def mst(vertexes):
    """Given a set of vertexes, build a minimum spanning tree: a dict of the form {parent: [child...]},
    where parent and children are vertexes, and the root of the tree is first(vertexes)."""
    tree = {first(vertexes): []}  # the first city is the root of the tree.
    edges = shortest_edges_first(vertexes)
    while len(tree) < len(vertexes):
        (A, B) = shortest_usable_edge(edges, tree)
        tree[A].append(B)
        tree[B] = []
    return tree


def shortest_usable_edge(edges, tree):
    "Find the ehortest edge (A, B) where A is in tree and B is not."
    (A, B) = first((A, B) for (A, B) in edges if (A in tree) ^ (B in tree))  # ^ is "xor"
    return (A, B) if (A in tree) else (B, A)


def shortest_edges_first(cities):
    "Return all edges between distinct cities, sorted shortest first."
    edges = [(A, B)
             for A in cities for B in cities
             if id(A) < id(B)]
    return sorted(edges, key=lambda edge: distance(*edge))


# ########### fin implementacion de Norvig ###################


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
def distance(ciudad_a, ciudad_b):
    """
    Calculo de distancia entre ciudades, pero con cache.
    """
    if (ciudad_a, ciudad_b) in RESTRICCIONES or (ciudad_b, ciudad_a) in RESTRICCIONES:
        return 9999999999

    xa, ya = CIUDADES[ciudad_a]
    xb, yb = CIUDADES[ciudad_b]

    distancia_calculada = math.sqrt(abs(xa - xb) ** 2 + abs(ya - yb) ** 2)

    return distancia_calculada


def resolver_tsp(origen):
    """
    Utilizar la implementacion de MST TSP de Norvig para resolver el problema.
    """
    ciudades = list(CIUDADES.keys())
    # asegurar posicion de la ciudad de origen
    ciudades.remove(origen)
    ciudades.insert(0, origen)

    camino_encontrado = altered_mst_tsp(ciudades)

    return camino_encontrado, tour_length(camino_encontrado)


print "Respuesta al punto a (instantanea):"
camino_encontrado, largo = resolver_tsp('Sunchales')
print ', '.join(camino_encontrado)
print "Respuesta al punto b (instantanea):"
print largo
