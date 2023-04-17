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
    graph_path = 'test/FastPartitionGraphs/threepaths160.gr'
    graph_list = convert_to_dllist(get_graph_list(graph_path))
    graph = graph_list.get(0)
    # initialize(graph)
    combined_vertices = convert_to_dllist(graph.vertices)
    max_degree = combined_vertices.size()//graph_list.size()
    # print(combined_vertices)
    return combined_vertices, max_degree

# def initialize(graph):
#     for vertice in graph.vertices:
#         vertice.set_color(0)

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

def find_Nx(partition, i):
    Nx = DoublyLinkedList()
    vertices = [v for vertex in partition.values() for v in vertex if len(v.neighbours) == i]
    for vertex in vertices:
        Nx.append(vertex)
    return Nx
def refine(C, x):
    global leftover
    global queue

    L = set()  # store unique colors
    A = {}  # states with color i in Ci

    # Split color classes
    Nx = find_Nx(C, x)

    if Nx.size() == 0:
        return C

    # Compute L and A
    for vertex in Nx:
        color = vertex.get_color()
        if color not in L:
            L.add(color)
        A[color] = A.get(color, 0) + 1
    L -= set(leftover)

    # Split color class into 2 new classes
    for i in L:
        if A[i] < C[i].size():
            new_colr = len(C)
            C[new_colr] = DoublyLinkedList()
            for q in set(C[i]) & set(Nx):
                C[i].delete_value(q)
                q.set_color(new_colr)
                C[new_colr].append(q)
            if C[new_colr].size() == 0:
                del C[new_colr]
                continue

            if i in queue:
                queue.append(new_colr)
            else:
                queue.append(min(i, new_colr))

    return C


def refines(C):
    global leftover
    while True:
        for i in range(1, max_degree+1):
            new_partition = refine(C, i)
            C = new_partition
        t = queue.delete_start()
        if t is None:
            break
        leftover.append(t)
    return C


def split():
    copy_dict = {}
    for graph in graph_list:
        partitions = partition_graph(graph)
        copy_dict.update({key: len(list(value)) for key, value in partitions.items()})
        print(copy_dict)
    copy_dict.clear()

start = time()
C = partition()
refines(C)
split()
end = time()
print('It took: ', end-start)