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
new_colr = 0

def partition():
    partition = {}
    for vertex in disjoint_graph:
        if vertex.get_color() not in partition:
            partition[vertex.get_color()] = [vertex]
        else:
            partition[vertex.get_color()].append(vertex)
    return partition

# def refines(C):
#     for i in range(1, max_degree):
#         refine(C, i)
#     return True
#

def new_color():
    return new_colr+1
def find_Nx(Ci, i):
    Nx = []
    for vertex in list(Ci.values()):
        for v in vertex:
            if len(v.neighbours) == i:
                Nx.append(v)
    return Nx


def refine(C, x): # x - degree, aka delta function; C - partition by colors
    global new_colr
    L = set()  # store unique colors
    A = {}  # states with color i in Ci
    Nx = find_Nx(C, x)
    Queue = [0]

    # Compute L and A
    # Works correctly!
    for key, value in C.items():
        A[key] = 0
        for q1 in Nx:
            if q1 in C[key]:
                L.add(key)
                A[key] += 1

    # Split color classes
    #ToDo: find logic behind Queue updates
    while len(Queue) != 0: #i think it should be deleted
        curr_color = Queue[0]
        print(L)
        for i in L:
            print(i)
            if A[i] < len(C[i]):
                new_colr = new_color()
                print('new', new_colr)
                for q in C[i]:
                    if i in Queue:
                        curr_color = new_colr
                    else:
                        t = min(i, new_colr)
                        curr_color = t
                    Queue.append(curr_color)
                    if curr_color not in C.keys():
                        C[curr_color] = [q]
                    else:
                        C[curr_color].append(q)
            #The number of tabs might be wrong
            Queue = list(set(Queue))
            print(Queue[0])
            Queue.pop(0)
            print("queue",Queue)

    # Update colors of states
    for key, value in C.items():
        for v in value:
            for q1 in Nx:
                if q1 not in v.neighbours:
                    q1.set_color(curr_color)
    C = partition()
    print(C)










C = partition()
refine(C, 2)