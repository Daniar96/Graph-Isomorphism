from collections import Counter

from main.DDL_short import DoublyLinkedList_Short


class Coloring_Fast(object):

    def __repr__(self):
        """
        A programmer-friendly representation of the coloring.
        """
        coloring_string = "Coloring:\n"
        for color in self.color_to_vertex.keys():
            coloring_string += 'Color = {}, #Vertices = {} \n'.format(color, len(self.color_to_vertex[color]))
        return coloring_string

    def __init__(self, vertices):
        self.vertices = vertices
        # Create a new dictionary to hold vertices mapped to colours(#neigbours)
        self.color_to_vertex = dict()
        self.ref_queue = DoublyLinkedList_Short()
        self.iter = 0

    def __len__(self):
        count = 0
        for sublist in self.color_to_vertex.values():
            count += len(sublist)
        return count

    def is_discrete(self):
        for color in self.color_to_vertex.keys():
            if len(self.color_to_vertex[color]) != 1:
                return False
        return True

    def assign_initial_colors(self):
        # For every vertex in the graph
        for vertex in self.vertices:
            # Get number of neighbours(color)
            neighbours_num = len(vertex.neighbours)
            # Set number of neighbours as a color for a vertex
            vertex.set_color(neighbours_num)
            # If there is no color in the dictionary yet
            if neighbours_num not in self.color_to_vertex.keys():
                # Add a list with a vertex
                self.color_to_vertex[neighbours_num] = [DoublyLinkedList_Short(), True]
                self.ref_queue.append(vertex.color)
            # If there is already this color in the dictionary
            # Add a vertex to list of vertices
            self.color_to_vertex[neighbours_num][0].append(vertex)
            vertex.change_partition(self.color_to_vertex[neighbours_num][0])
        return

    def refine_colors(self):
        while self.ref_queue.head is not None:
            color = self.ref_queue.get_and_remove(0)
            self.iter += 1

            self.color_to_vertex[color][1] = False
            neighbours = set(
                [neighbour for vertex in self.color_to_vertex[color][0] for neighbour in vertex.neighbours])

            # A list L of all colors i such that Ci contains vertices that have neighbours in C(color) mapped to
            # The number A[i] of such states in Ci
            color_counts = {vertex.color: sum(1 for other_vertex in neighbours if other_vertex.color == vertex.color)
                            for vertex in neighbours}
            if len(color_counts.keys()) < 2:
                continue

            to_recolor = self.split_colors(color_counts, color)
            self.execute_color_changes(to_recolor)
        print("Done")
        return

    def split_colors(self, L, main_c):
        to_recolor = {}
        # For each i ∈ L:
        for color in L.keys():
            Ci = self.color_to_vertex[color][0]
            # Decide whether Ci should split up(whether A[i] < | Ci |)
            if not L[color] < Ci.size():
                continue
            # If so, choose a new color l, and update Queue by adding i or l.
            leftover = DoublyLinkedList_Short()
            color_classes = 2
            split_classes = {}
            neighbours_in_C_num = int()
            for vertex in Ci:
                neighbours_in_C_num = [neighbour.color for neighbour in vertex.neighbours].count(main_c)
                if neighbours_in_C_num not in split_classes.keys():
                    if color_classes == 0:
                        leftover.append(vertex)
                    color_classes -= 1
                    split_classes[neighbours_in_C_num] = DoublyLinkedList_Short()
                    split_classes[neighbours_in_C_num].append(vertex)
                else:
                    split_classes[neighbours_in_C_num].append(vertex)
            split_classes[neighbours_in_C_num].merge(leftover)
            if len(split_classes.values()) == 2:
                to_recolor[color] = tuple(split_classes.values())

        return to_recolor

    def execute_color_changes(self, to_recolor):
        for color_i in to_recolor.keys():
            put_both_in_q = self.color_to_vertex[color_i][1]
            partition = sorted(to_recolor[color_i], key=lambda x: x.size())
            i_list, l_list = partition[0], partition[1]
            color_l = self.get_new_color()
            self.ref_queue.append(color_l)
            if put_both_in_q:
                self.ref_queue.append(color_i)
            self.change_color(color_i, i_list, put_both_in_q)
            self.change_color(color_l, l_list, True)

    def change_color(self, new_color, vertex_list, in_queue):
        new_partition = DoublyLinkedList_Short()
        self.color_to_vertex[new_color] = [new_partition, in_queue]
        for vertex in vertex_list:
            vertex.partition.delete_value(vertex)
            vertex.partition = new_partition
            vertex.set_color(new_color)
            new_partition.append(vertex)

    def get_new_color(self):

        new_color = len(self.color_to_vertex.keys())
        while new_color in self.color_to_vertex.keys():
            new_color += 1

        return new_color

    def get_color_class(self):
        for color in self.color_to_vertex.keys():
            if len(self.color_to_vertex[color]) >= 4:
                return color
        return -1

    def check_bijection_or_unbalanced(self):
        """
        Checks if the coloring is unbalanced or defines a bijection
        :return: 0 if unbalanced, 1 if bijection, -1 if neither
        """
        is_bijection = True

        for color_class_vertices in self.color_to_vertex.values():
            if len(color_class_vertices) % 2 == 1:
                return 0
            if len(color_class_vertices) != 2:
                is_bijection = False
            elif color_class_vertices[0].graph == color_class_vertices[1].graph:
                is_bijection = False
        return 1 if is_bijection else -1

    def reset_colors_with_dict(self):
        for color in self.color_to_vertex.keys():
            for vertex in self.color_to_vertex[color]:
                vertex.set_color(color)

    def count_isomorphism(self, previous_x_y):
        check = self.check_bijection_or_unbalanced()
        if check != -1:
            return check
        color_class = self.get_color_class()
        if color_class == -1:
            return 0
        x = self.color_to_vertex[color_class][0]
        y = [vertex for vertex in self.color_to_vertex[color_class][1:] if vertex.graph != x.graph]
        num = 0
        for y_vertex in y:
            this_x_y = previous_x_y + [(x, y_vertex)]
            new_coloring = Coloring_Fast(self.vertices)
            new_coloring.assign_initial_colors()

            for x_y in this_x_y:
                x_y_colored_vertices = new_coloring.color_to_vertex.pop(x_y[0].color)
                new_coloring.color_to_vertex[x_y[0].color] = [vertex for vertex in x_y_colored_vertices if
                                                              vertex not in x_y]
                new_coloring.assign_new_color(list(x_y))
                new_coloring.execute_color_changes()
            new_coloring.refine_colors()
            num += new_coloring.count_isomorphism(this_x_y)
            self.reset_colors_with_dict()
        return num

    def find_isomorphism(self, previous_x_y):
        check = self.check_bijection_or_unbalanced()
        if check == 1:
            gr = self.vertices[0].graph
            gr_list = list()
            gr_list2 = list()
            for color_list in self.color_to_vertex.values():
                for vertex in color_list:
                    if vertex.graph == gr:
                        gr_list.append(vertex)
                    else:
                        gr_list2.append(vertex)
            gr_list = sorted(gr_list, key=lambda vertex: vertex.label)
            gr_list2 = sorted(gr_list2, key=lambda vertex: vertex.label)
            print(gr_list)
            print(gr_list2)
            return True
        elif check == 0:
            return False
        color_class = self.get_color_class()
        if color_class == -1:
            return False
        x = self.color_to_vertex[color_class][0]
        y = [vertex for vertex in self.color_to_vertex[color_class][1:] if vertex.graph != x.graph]

        for y_vertex in y:
            this_x_y = previous_x_y + [(x, y_vertex)]
            new_coloring = Coloring_Fast(self.vertices)
            new_coloring.assign_initial_colors()

            for x_y in this_x_y:
                x_y_colored_vertices = new_coloring.color_to_vertex.pop(x_y[0].color)
                new_coloring.color_to_vertex[x_y[0].color] = [vertex for vertex in x_y_colored_vertices if
                                                              vertex not in x_y]
                new_coloring.assign_new_color(list(x_y))
                new_coloring.execute_color_changes()
            new_coloring.refine_colors()
            if 1 == new_coloring.find_isomorphism(this_x_y):
                return True
            self.reset_colors_with_dict()
        return False
