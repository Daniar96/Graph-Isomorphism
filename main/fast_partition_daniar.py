import os
import sys
import time

import graph_io
from graph import *
from main.fast_coloring import Coloring_Fast


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
        graph_list = graph_io.read_graph_list(Graph, file)[0]
    return graph_list


def create_graph_coloring_list(graph_list):
    vertices = list()

    for graph in graph_list:
        vertices.extend(graph.vertices)

    #vertices.extend(graph_list[0].vertices)

    this_coloring = Coloring_Fast(vertices)
    this_coloring.assign_initial_colors()
    this_coloring.refine_colors()


def get_isomorphisms(graph_list):
    all_isomorhisms = list()
    # Convert list to a dict
    graph_dict = {i: graph_list[i] for i in range(0, len(graph_list))}
    while graph_dict:
        isomorphism_properties = [list(), bool]
        # Take a coloring and remove it so it won't be compared to itself
        index, graph = graph_dict.popitem()
        isomorphism_properties[0].append(index)
        isomorphism_properties[1] = graph.is_discrete()
        # For every graph in a list except the graph that was removed
        for coloring_index in graph_dict.keys():
            # If their neighbours are the same, then their colors could be combined
            if graph.is_isomorphism(graph_dict[coloring_index]):
                isomorphism_properties[0].append(coloring_index)
                isomorphism_properties[1] = graph_dict[coloring_index].is_discrete() and isomorphism_properties[1]
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


def handle_input(path):
    if not path.endswith("gr") and not path.endswith("grl"):
        file_to_graph = loop_in_directory(path)
    else:
        file_to_graph = {os.path.basename(path): get_graph_list(path)}

    for file in file_to_graph:
        sub_start = time.time()

        graph_list = file_to_graph[file]
        create_graph_coloring_list(graph_list)
        isomorphisms = get_isomorphisms(graph_list)
        sub_end = time.time()
        print("It took {:.5f} seconds to finish graph {}".format(sub_end - sub_start, file))
        print_isomorphisms(isomorphisms)


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    try:
        while True:
            user_input = input("Type a path to a graph file: \n")
            start = time.time()
            handle_input(user_input)
            end = time.time()
            print("It took {:.5f} seconds to finish the whole query".format(end - start))

    except KeyboardInterrupt:
        print('Interrupted')
