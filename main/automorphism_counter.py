import os
import sys
import time

import graph_io
from graph import *
from main.coloring import Coloring


def loop_in_directory(dir_path):
    file_to_graph = dict()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith("grl") or file.endswith("gr"):
                file_to_graph[file] = get_graph_list(os.path.join(root, file))
    return file_to_graph


# Returns a list with graphs from a file
def get_graph_list(file_path):
    # Open a file to extract graphs
    with open(file_path) as file:
        if file_path.endswith("gr"):
            auto_graph = graph_io.read_graph(Graph, file)[0]
            file.seek(0)
            return [auto_graph, graph_io.read_graph(Graph, file)[0]]
        graph_list = graph_io.read_graph_list(Graph, file)[0]
    return graph_list


def count_automorphism(graph, graph2):
    this_coloring = Coloring(graph.vertices + graph2.vertices)
    this_coloring.assign_initial_colors()
    this_coloring.refine_colors()
    return this_coloring.count_isomorphism([])


def get_isomorphisms(graph_list):
    all_isomorphisms = list()
    # Convert list to a dict
    graph_dict = {i: graph_list[i] for i in range(0, len(graph_list))}
    while graph_dict:
        isomorphism_properties = [list(), int]
        # Take a coloring and remove it, so it won't be compared to itself
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
            all_isomorphisms.append(isomorphism_properties)
            for proved_isomorphism in isomorphism_properties[0]:
                if proved_isomorphism != index:
                    graph_dict.pop(proved_isomorphism)
    return all_isomorphisms


def print_isomorphisms(isomorphisms):
    print("Sets of possibly isomorphic graphs: ")
    for isomorphism in isomorphisms:
        print("{} {}".format(sorted(isomorphism[0]), isomorphism[1]))
    print("----------------------" + '\n')


def handle_input(path):
    if not path.endswith("gr") and not path.endswith("grl"):
        file_to_graph = loop_in_directory(path)
    else:
        file_to_graph = {os.path.basename(path): get_graph_list(path)}

    for file in file_to_graph:
        sub_start = time.time()

        graph_list = file_to_graph[file]
        isomorphisms = get_isomorphisms(graph_list)
        sub_end = time.time()
        print("It took {:.2f} seconds to finish graph {}".format(sub_end - sub_start, file))
        print_isomorphisms(isomorphisms)


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    try:
        while True:
            user_input = input("Type a path to a graph file: \n")
            start = time.time()
            handle_input(user_input)
            end = time.time()
            print("It took {:.2f} seconds to finish the whole query".format(end - start))

    except KeyboardInterrupt:
        print('Interrupted')
