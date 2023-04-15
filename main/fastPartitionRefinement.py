from graph import *
from coloring import *
from partition_refinement import *
from DDL import *
from time import *

graph_list = []
queue = [0]
leftover = []

def setup():
    global graph_list
    graph_path = 'FastPartitionGraphs/threepaths5.gr'
    graph_list = get_graph_list(graph_path)
    combined_vertices = []
    for graph in graph_list:
        initialize(graph)
        for v in graph.vertices:
            combined_vertices.append(v)
    max_degree = len(combined_vertices)//len(graph_list)
    print(combined_vertices)
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

def partition_graph(graph):
    partition = {}
    for vertex in graph:
        if vertex.get_color() not in partition:
            partition[vertex.get_color()] = [vertex]
        else:
            partition[vertex.get_color()].append(vertex)
    return partition

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
    global leftover

    L = set()  # store unique colors
    A = {}  # states with color i in Ci
    global queue

    # Split color classes
    Nx = find_Nx(C, x)

    if len(Nx) == 0:
        # new_colr=new_color()
        return C, False

    print('NX', Nx)
    print('queue', queue)
    print('degree: ', x)

    # Compute L and A
    # Works correctly!
    for key, value in C.items():
        A[key] = 0
        for q1 in Nx:
            if q1 in C[key]:
                L.add(key)
                A[key] += 1
    print('left', leftover)
    L = list(filter(lambda k: k not in leftover, L))


    print('l',L)
    print('A', A)
    print('C', C)
    # split color class into 2 new classes
    for i in L: # i dont need L
        print('len:', len(C[i]))
        print('color', i)
        if A[i] < len(C[i]):
            new_colr = new_color()
            C[new_colr] = []
            print('new', new_colr)
            for q in Nx:
                for key, value in list(C.items()):
                    if q in list(value):
                        C[key].remove(q)
                C[new_colr].append(q)
            # for key, value in list(C.items()):
            #     for q in value:
            #         if (q in Nx): # create new color class with vertices from Nx!
            #             C[new_colr].append(q)
            #             C[key].remove(q)
            print(len(C[i]), len(C[new_colr]))
            if len(C[new_colr]) == 0:
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
    print(C)
    print('queueuu', queue)

    return C, True

def refines(C):
    global leftover
    #TODO: add loop over queue until its empty
    while queue:
        for i in range(1, max_degree+1):
            new_partition, check = refine(C, i)
            #TODO: check whether partition terminates correctly
           # check whether the partition is stable such that degree existed in Nx
           #  if C == new_partition and check == True:
           #      print(C)
           #      return C
           #  else:
            C = new_partition
        t = queue.pop(0)
        leftover.append(t)
        print('leftover', leftover)
        print('pop', queue)

    print(C)
    return C

# def split():
#     for i in range(len(graph_list)):
#         print(f'[{i}', end='')
#         for j in range(i + 1, len(graph_list)):
#             if partition_graph(graph_list[i]) == partition_graph(graph_list[j]):
#                 print(j, end=' ')
#         print(']')

def split():
    copy_dict={}
    print('split')
    for i in range(len(graph_list)):
        # print(partition_graph(graph_list[i]))
        dict_p = partition_graph(graph_list[i])
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