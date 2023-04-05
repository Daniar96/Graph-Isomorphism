from collections import Counter


class Coloring(object):

    def __repr__(self):
        """
        A programmer-friendly representation of the coloring.
        """
        coloring_string = "Coloring:\n"
        for color in self.color_to_vertex.keys():
            coloring_string += 'Color = {}, #Vertices = {} \n'.format(color, len(self.color_to_vertex[color]))
        return coloring_string

    def __init__(self, vertices):
        self.this_iteration_color_change = list()
        self.vertices = vertices
        # Create a new dictionary to hold vertices mapped to colours(#neigbours)
        self.color_to_vertex = dict()
        self.taken_colors = set()
        self.test = [1, 1]

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
            if neighbours_num not in self.taken_colors:
                # Add a list with a vertex
                self.color_to_vertex[neighbours_num] = [vertex]
                self.taken_colors.add(neighbours_num)
            # If there is already this color in the dictionary
            else:
                # Add a vertex to list of vertices
                self.color_to_vertex[neighbours_num].append(vertex)

    def refine_colors(self):
        while not self.is_refined():

            for color in list(self.color_to_vertex.keys()):
                if 1 == len(self.color_to_vertex[color]):
                    continue
                self.taken_colors.remove(color)
                self.recolor_by_neighbours(self.color_to_vertex.pop(color))
                self.execute_color_changes()

    def refine_colors_test(self, test):
        self.test = test
        self.refine_colors()

    def is_refined(self):
        for color in self.color_to_vertex.keys():
            vertices = self.color_to_vertex[color]
            if len(vertices) == 1:
                continue
            first_vertex = vertices[0]
            neighbour_colors = [neighbour.get_color() for neighbour in first_vertex.neighbours]
            for vertex in vertices:
                vertex_colors = [neighbour.get_color() for neighbour in vertex.neighbours]
                if Counter(vertex_colors) != Counter(neighbour_colors):
                    return False
        return True

    def recolor_by_neighbours(self, vertices_list):
        while vertices_list:
            # Take a vertex from a list
            vertex = vertices_list.pop(0)
            # Create a list of vertices with same neighbours and add this vertex
            same_neighbours_list = [vertex]
            # Get neighbours of this vertex
            neighbour_colors = [vertex.color for vertex in vertex.neighbours]
            # For every vertex in a list except the vertex that was removed
            for vertex_to_compare in vertices_list:
                colors_to_compare = [vertex_to_compare.color for vertex_to_compare in
                                     vertex_to_compare.neighbours]
                # If their neighbours are the same, then their colors could be combined
                if Counter(neighbour_colors) == Counter(colors_to_compare):
                    same_neighbours_list.append(vertex_to_compare)

            # Assign new color to all the vertices with a same color
            if len(same_neighbours_list) != 1:
                self.assign_new_color(same_neighbours_list)
            vertices_list = [x for x in vertices_list if x not in same_neighbours_list]


    def assign_new_color(self, vertices_list):
        new_color = len(self.color_to_vertex.keys())

        while new_color in self.taken_colors:
            new_color += 1
        self.this_iteration_color_change.append((vertices_list, new_color))

        # self.colors[new_color] = vertices_list
        # for vertex in vertices_list:
        #     vertex.set_color(new_color)

        self.taken_colors.add(new_color)

    def execute_color_changes(self):
        if not self.this_iteration_color_change:
            return
        for change in self.this_iteration_color_change:
            list_to_change = change[0]
            color_to_change = change[1]
            self.color_to_vertex[color_to_change] = list_to_change
            for vertex in list_to_change:
                vertex.set_color(color_to_change)
        self.this_iteration_color_change = list()

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
        return 1 if is_bijection else -1

    def reset_color_dict(self):
        for vertex in self.vertices:
            if vertex.color not in self.color_to_vertex:
                self.color_to_vertex[vertex.color] = []
                self.taken_colors.add(vertex.color)
            self.color_to_vertex[vertex.color].append(vertex)

    def reset_colors_with_dict(self):
        for color in self.color_to_vertex.keys():
            for vertex in self.color_to_vertex[color]:
                vertex.set_color(color)

    def count_isomorphism(self, previous_x_y):
        check = self.check_bijection_or_unbalanced()
        if check != -1:
            return check
        color_class = self.get_color_class()
        x = self.color_to_vertex[color_class][0]
        y = [vertex for vertex in self.color_to_vertex[color_class][1:] if vertex.graph != x.graph]
        num = 0
        for y_vertex in y:
            this_x_y = previous_x_y + [(x, y_vertex)]
            new_coloring = Coloring(self.vertices)
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
