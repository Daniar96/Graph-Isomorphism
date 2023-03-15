from graph import *
from coloring import *
from partition_refinement import *
from DDL import *


def setup():
    graph_path = 'CRefFriday2023/ColorRefFri1.grl'
    graph_list = get_graph_list(graph_path)
    combined_vertices = []
    for graph in graph_list:
        initialize(graph)
        for v in graph.vertices:
            combined_vertices.append(v)
    max_degree = len(combined_vertices)//len(graph_list)
    return combined_vertices, max_degree

def initialize(graph):
    for vertice in graph.vertices:
        vertice.set_color(0)

disjoint_graph, max_degree = setup()
saved_coloring = None
last_color = 0

#TODO: iteration over linked list
def find_Nx(Ci, i):
    Nx = doublyLinkedList()
    for vertex in list(Ci.values()):
        if len(vertex.neighbours) == i:
            if len(Nx) == 0:
                Nx.InsertToEmptyList(vertex)
            else:
                Nx.InsertToEnd(vertex)
    return Nx

def partition():
    partition = {}
    print(disjoint_graph)
    for vertex in disjoint_graph:
        if vertex.get_color() not in partition:
            partition[vertex.get_color()] = doublyLinkedList()
            partition[vertex.get_color()].InsertToEnd(vertex)
        else:
            partition[vertex.get_color()].InsertToEnd(vertex)
    return partition

def refine(C, i):
    global last_color
    Nx = find_Nx(C, i)
    queue = {0}
    L = set()
    A = {}
    for key, value in C.items():
        A[key] = 0
        for q1 in Nx:
            if q1 in C[key]:
                L.add(key)
                A[key] += 1

    for i in L: #loop though colors
        if A[i] < len(C[i]): #if there exist nodes with different configuration
            last_color = last_color+1
            cur_color = 0
            if i in queue:
                cur_color = last_color
                queue.add(last_color)
            else:
                cur_color = min(i, last_color)
                queue.add(min(i,last_color))

        for value in C[i]:
            for q1 in Nx:
                if q1 not in value.neighbours:
                    q1.set_color(cur_color)

        queue.pop(0)
        C = partition()
        print(C)
    return C

def refines(C):
    for i in range(1, max_degree):
        refine(C, i)
    return True

C = partition()
refine(C, 1)