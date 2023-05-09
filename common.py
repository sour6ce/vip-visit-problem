# Importación de módulos

import random as rand
from dataclasses import dataclass
from math import log2
from typing import Dict, List, NamedTuple, Set, Tuple

import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra, floyd_warshall

from disjoin_set import DisjoinSet

# Clase para almacenar datos de las aristas


class Edge(NamedTuple):
    origin: int
    dest: int
    weight: float

# Clase para almacenar los pares <s,t> dados


class Query(NamedTuple):
    s: int
    t: int


# Alias para definir Grafos
Graph = csr_matrix


@dataclass(init=False)
class ProblemInput():
    edge_list: List[Edge]
    queries: List[Query]

    def __init__(self, edges: List[Edge], queries: List[Query]) -> None:
        self.edge_list = edges
        self.queries = queries

        # Por cada par de nodos guarda el peso del camino entre ellos. Si no existe camino guarda 0.
        # Utiliza la implementación de matriz dispersa de scipy
        self.matrix: Graph

        # Para cada par de nodos guarda la mínima distancia entre estos
        self.dist: NDArray[np.float64]

        self.m = len(edges)  # Cantidad de aristas
        self.n = max((node for e in edges for node in [
                     e[0], e[1]]))+1  # Cantidad de nodos

        self.calculate_matrix()

    def calculate_matrix(self) -> NDArray[np.int64]:
        self.matrix = np.zeros((self.n, self.n))

        for a, b, w in self.edge_list:
            self.matrix[a, b] = w
            self.matrix[b, a] = w

        return self.matrix

    def calculate_distances(self) -> NDArray[np.int64]:
        # Criteria for algorithm to use
        cond = self.m > self.n*(self.n/log2(self.n)-1)

        if cond:
            # Algoritmo Floyd-Warshall: O(|V|^3)
            self.dist = floyd_warshall(
                self.matrix, directed=False, overwrite=False)
        else:
            # Algoritmo Dijkstra: O((|V|+|E|)|V|log|V|)
            self.dist = dijkstra(self.matrix, directed=False)

        return self.dist


# Test 1
p_in = ProblemInput([Edge(0, 1, 3), Edge(1, 2, 9), Edge(3, 1, 27)], [])
p_in.calculate_distances()
assert p_in.dist[0][1] == p_in.dist[1][0]
assert p_in.dist[0][3] == 30
assert p_in.dist[2][0] == p_in.dist[0][1] + p_in.dist[2][1]
#
