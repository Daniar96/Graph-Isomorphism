from graph import *
from coloring import *
from graph_io import *


def count_twins(graph):
    vertices = graph.vertices
    twins_multiplier = 0
    counter = 0
    fact = 1
    known_twins = []
    for vertex1 in vertices:
        if vertex1 in known_twins:
            continue
        for vertex2 in vertices:
            if vertex1 == vertex2:
                continue
            neighbours1 = vertex1.neighbours
            neighbours2 = vertex2.neighbours
            if vertex1 in neighbours2 and vertex2 in neighbours1:
                neighbours2.remove(vertex1)
                neighbours1.remove(vertex2)
            if neighbours1 == neighbours2:
                print(vertex1, " twins: ",vertex2)
                counter += 1
                known_twins.append(vertex2)
        if counter > 0:
            for i in range(1, counter + 2):
                fact = fact * i
            twins_multiplier = twins_multiplier + fact
            fact = 1
        counter = 0
    return twins_multiplier


g = Graph(False, 6)
g.add_edge(Edge(g.vertices[0], g.vertices[1]))
g.add_edge(Edge(g.vertices[0], g.vertices[2]))
g.add_edge(Edge(g.vertices[0], g.vertices[3]))
g.add_edge(Edge(g.vertices[0], g.vertices[4]))
g.add_edge(Edge(g.vertices[5], g.vertices[1]))
g.add_edge(Edge(g.vertices[5], g.vertices[2]))
g.add_edge(Edge(g.vertices[5], g.vertices[3]))
g.add_edge(Edge(g.vertices[5], g.vertices[4]))
# g.add_edge(Edge(g.vertices[1], g.vertices[2]))
# g.add_edge(Edge(g.vertices[2], g.vertices[3]))
# g.add_edge(Edge(g.vertices[3], g.vertices[4]))
g.add_edge(Edge(g.vertices[0], g.vertices[5]))
print(count_twins(g))


