from common import *


class RandomProblemInput(ProblemInput):
    def __init__(self, n: int, m: int, q: int, min_w: float = 1.0,
                 max_w: float = None, seed: int = None):
        self.queries: List[Query] = []

        self.__edges = []

        self.m = m
        self.n = n

        self.__r = rand.Random(seed)

        # Usa un peso máximo útil por defecto
        max_w = 2.0*m if max_w is None else max_w

        self.edge_list: List[Edge] = []

        # Grafo negativo. Por cada nodo guarda los que no están conectados con él.
        # Útil para construir el grafo
        self.ngraph = [set((k for k in range(n) if k != i)) for i in range(n)]
        # Nodos que permiten más aristas conectadas a ellos
        self.not_full = set(range(n))

        # Acota la cantidad de aristas entre la mínima y máxima cantidad de aristas.
        m = max(
            min((n*(n-1))//2,  # Cantidad de aristas de un grafo completo
                m  # Cantidad de aristas dada
                ),
            n-1  # Cantidad de aristas de un árbol
        )

        # Se utiliza conjuntos disjuntos para construir un grafo conexo asegurando
        # unir nodos de forma que enlaces dos componentes conexas distintas
        dj = DisjoinSet(self.n)

        def add_edge(a: int, b: int):
            # Genera un peso aleatorio
            w = self.__r.randint(min_w, max_w)

            # Añade la arista a la lista de aristas con las que se define el grafo
            self.edge_list.append(Edge(a, b, w))

            # Actualiza el grafo negativo
            self.ngraph[a].remove(b)
            if len(self.ngraph[a]) == 0:
                self.not_full.remove(a)
            self.ngraph[b].remove(a)
            if len(self.ngraph[b]) == 0:
                self.not_full.remove(b)

            # Actualiza los conjuntos disjuntos
            r = dj.merge(edge[0], edge[1])

        # Utiliza las primeras n-1 aristas para construir un árbol
        for _ in range(n-1):
            # Escoge 2 nodos que pertenezcan a dos componentes conexas distintas cualesquiera
            edge = self.__r.sample(dj.get_all_parents(), 2)

            # Define una arista entre ellos
            add_edge(edge[0], edge[1])

        assert dj.get_setsize(0) == n

        for _ in range(n-1, m):
            # Escoge un nodo aleatorio entre aquellos cuyo grado actual es menor que n-1
            a = self.__r.choice(sorted(self.not_full))

            # Escoge un nodo aleatorio entre los que no están conectados a él
            b = self.__r.choice(sorted(self.ngraph[a]))

            # Define una arista entre ellos
            add_edge(a, b)

        # Genera consultas aleatorias
        nd = self.__r.choices(list(range(self.n)), k=q*2)
        self.queries = [Query(s, t) for s, t in zip(nd[:q], nd[q:])]
        self.calculate_matrix()
