import sys

from graph import *
import graph_io
from coloring import Coloring
import os, time


def loop_in_directory(path):
    files_list = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(("grl")):
                files_list.append((file, get_graph_list(os.path.join(root, file))))
    return files_list


# Returns a list with graphs from a file
def get_graph_list(file_path):
    # Open a file to extract graphs
    with open(file_path) as file:
        # graph_list = graph_io.load_graph(file)
        graph_list = graph_io.read_graph_list(Graph, file)[0]
    return graph_list


def count_automorphism(graph, graph2):
    this_coloring = Coloring(graph.vertices + graph2.vertices)
    this_coloring.assign_initial_colors()
    this_coloring.refine_colors()
    return this_coloring.count_isomorphism([])


def get_isomorphisms(graph_list):
    all_isomorhisms = list()
    # Convert list to a dict
    graph_dict = {i: graph_list[i] for i in range(0, len(graph_list))}
    while graph_dict:
        isomorphism_properties = [list(), int]
        # Take a coloring and remove it so it won't be compared to itself
        index, graph = graph_dict.popitem()
        isomorphism_properties[0].append(index)
        isomorphism_properties[1] = 0
        # For every graph in a list except the graph that was removed
        for new_graph_index in graph_dict.keys():
            # If their neighbours are the same, then their colors could be combined
            automorphism_count = count_automorphism(graph, (graph_dict[new_graph_index]))
            if automorphism_count != 0:
                isomorphism_properties[0].append(new_graph_index)
                isomorphism_properties[1] = automorphism_count
        if len(isomorphism_properties[0]) > 1:
            all_isomorhisms.append(isomorphism_properties)
            for proved_isomorphism in isomorphism_properties[0]:
                if proved_isomorphism != index:
                    graph_dict.pop(proved_isomorphism)
    return all_isomorhisms


def print_isomorphisms(isomorphisms):
    print("Sets of possibly isomorphic graphs: ")
    for isomorphism in isomorphisms:
        print("{} {}".format(sorted(isomorphism[0]), isomorphism[1]))
    print("----------------------" + '\n')


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    try:
        while True:
            graph_path = input("Type a path to a graph file: ")
            start = time.time()

            graph = get_graph_list(graph_path)
            print("The graph was loaded")
            isomorphisms = get_isomorphisms(graph)
            print_isomorphisms(isomorphisms)
            end = time.time()
            print("It took ", end - start)





    except KeyboardInterrupt:
        print('Interrupted')
