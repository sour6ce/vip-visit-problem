# Segundo problema de DAA: Lázaro presidente del PCC
*Equipo: pss pss | Gabriel Hernández Rodríguez C411*

Dado un grafo *G=<V,E>*, una función de peso *w(e)* y una serie de consultas *Q* de la forma *<s,t>*. Determinar para cada consulta la cantidad de aristas que pertenecen a al menos un camino mínimo de *s* a *t*.

# Solución Propuesta
La solución propuesta consiste en contar el número de aristas que forman parte del camino mínimo entre dos nodos dados en un grafo no dirigido, siguiendo los siguientes pasos:
1. Calcular las distancias mínimas utilizando el algoritmo de Dijkstra o Floyd-Warshall, dependiendo de la densidad del grafo.
2. Recorrer todas las aristas del grafo y contar las que cumplen que las distancias de *s* a ella y de ella hasta *t* suman la distancia mínima de *s* a *t* por cada una de las consultas.
