from graph import *
from coloring import *
from partition_refinement import *
from DDL import *
from time import *

graph_list = DoublyLinkedList()
queue = DoublyLinkedList()
leftover = DoublyLinkedList()

def setup():
    global graph_list
    graph_path = 'FastPartitionGraphs/threepaths160.gr'
    graph_list = convert_to_dllist(get_graph_list(graph_path))
    graph = graph_list.get(0)
    initialize(graph)
    combined_vertices = convert_to_dllist(graph.vertices)
    max_degree = combined_vertices.size()//graph_list.size()
    # print(combined_vertices)
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
            partition[vertex.get_color()] = convert_to_dllist([vertex])
        else:
            partition[vertex.get_color()].append(vertex)
    return partition

def partition_graph(graph):
    partition = {}
    for vertex in graph:
        if vertex.get_color() not in partition:
            partition[vertex.get_color()] = convert_to_dllist([vertex])
        else:
            partition[vertex.get_color()].append(vertex)
    return partition

def new_color():
    return new_colr+1
def find_Nx(Ci, i):
    Nx = DoublyLinkedList()
    for vertex in list(Ci.values()):
        for v in vertex:
            if len(v.neighbours) == i:
                Nx.append(v)
    return Nx


def refine(C, x): # x - degree, aka delta function; C - partition by colors
    global new_colr
    global leftover

    L = DoublyLinkedList()  # store unique colors
    A = {}  # states with color i in Ci
    global queue

    # Split color classes
    Nx = find_Nx(C, x)

    if Nx.size() == 0:
        # new_colr=new_color()
        return C

    # print('NX', Nx)
    # print('queue', queue)
    # print('degree: ', x)

    # Compute L and A
    for key, value in C.items():
        A[key] = 0
        for q1 in Nx:
            if q1 in C[key]:
                if key not in L:
                    L.append(key)
                A[key] += 1
    # print('left', leftover)
    L = convert_to_dllist(filter(lambda k: k not in leftover, L))


    # print('l',L)
    # print('A', A)
    # print('C', C)
    # split color class into 2 new classes
    for i in L: # i dont need L
        # print('len:', len(C[i]))
        # print('color', i)
        if A[i] < C[i].size():
            new_colr = new_color()
            C[new_colr] = DoublyLinkedList()
            # print('new', new_colr)
            for q in Nx:
                for key, value in list(C.items()):
                    if q in list(value):
                        C[key].delete_value(q)
                C[new_colr].append(q)
            # for key, value in list(C.items()):
            #     for q in value:
            #         if (q in Nx): # create new color class with vertices from Nx!
            #             C[new_colr].append(q)
            #             C[key].remove(q)
            # print(C[i].size(), C[new_colr].size())
            if C[new_colr].size() == 0:
                del C[new_colr]
                continue

            if i in queue:
                queue.append(new_colr)
            else:
                queue.append(min(i, new_colr))

        # Update colors of states
        for key, value in C.items():
            for v in value:
                v.set_color(key)
    C = partition()
    # print(C)
    # print('queueuu', queue)

    return C

def refines(C):
    global leftover
    t = 0
    #TODO: add loop over queue until its empty
    while t != None:
        for i in range(1, max_degree+1):
            new_partition = refine(C, i)
            C = new_partition
        t = queue.delete_start()
        leftover.append(t)
    #     print('leftover', leftover)
    #     print('pop', queue)
    #
    # print(C)
    return C


def split():
    copy_dict={}
    for i in range(graph_list.size()):
        # print(partition_graph(graph_list[i]))
        dict_p = partition_graph(graph_list.get(i))
        for key, value in list(dict_p.items()):
            copy_dict[key] = len(list(value))
        print(copy_dict)
        copy_dict.clear()

start = time()
C = partition()
refines(C)
split()
end = time()
print('It took: ', end-start)