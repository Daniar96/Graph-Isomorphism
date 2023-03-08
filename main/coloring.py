from collections import Counter


class Coloring(object):

    def __repr__(self):
        """
        A programmer-friendly representation of the coloring.
        """
        coloring_String = "Coloring:\n"
        for color in self.colors.keys():
            coloring_String += 'Color = {}, #Vertices = {} \n'.format(color, len(self.colors[color]))
        return coloring_String

    def __init__(self, vertices):
        self.this_iteration_color_change = list()
        self.vertices = vertices
        # Create a new dictionary to hold vertices mapped to colours(#neigbours)
        self.colors = dict()
        self.taken_colors = list()
        self.quick = True

    def is_discrete(self):
        for color in self.colors.keys():
            if len(self.colors[color]) != 1:
                return False
        return True

    def assign_colors(self):
        # For every vertex in the graph
        for vertex in self.vertices:
            # Get number of neighbours(color)
            neighbours_num = len(vertex.neighbours)
            # Set number of neighbours as a color for a vertex
            vertex.set_color(neighbours_num)
            # If there is no color in the dictionary yet
            if neighbours_num not in self.taken_colors:
                # Add a list with a vertex
                self.colors[neighbours_num] = [vertex]
                self.taken_colors.append(neighbours_num)
            # If there is already this color in the dictionary
            else:
                # Add a vertex to list of vertices
                self.colors[neighbours_num].append(vertex)

    def refine_colors(self):
        while not self.is_refined():
            for color in list(self.colors.keys()):
                if 1 == len(self.colors[color]):
                    continue
                self.taken_colors.remove(color)
                self.recolor_by_neighbours(self.colors.pop(color), color)
                self.execute_color_changes()

    def is_refined(self):
        for color in self.colors.keys():
            vertices = self.colors[color]
            if len(vertices) == 1:
                continue
            first_vertex = vertices[0]
            neighbour_colors = [neighbour.get_color() for neighbour in first_vertex.neighbours]
            for vertex in vertices:
                vertex_colors = [neighbour.get_color() for neighbour in vertex.neighbours]
                if Counter(vertex_colors) != Counter(neighbour_colors):
                    return False
        return True

    def recolor_by_neighbours(self, vertices_list, color):
        while vertices_list:
            # Take a vertex
            vertex = vertices_list[0]
            # Remove a vertex so it won't be compared to itself
            vertices_list.remove(vertex)
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

            # Assign new color to all of the vertices with a same color
            if len(same_neighbours_list) != 1:
                self.assign_new_color(same_neighbours_list, sum(neighbour_colors))
            vertices_list = [x for x in vertices_list if x not in same_neighbours_list]

    def assign_new_color(self, vertices_list, new_color):

        while new_color in self.taken_colors:
            new_color += 1
        self.this_iteration_color_change.append((vertices_list, new_color))

        # self.colors[new_color] = vertices_list
        # for vertex in vertices_list:
        #     vertex.set_color(new_color)

        self.taken_colors.append(new_color)

    def execute_color_changes(self):
        if not self.this_iteration_color_change:
            return
        for change in self.this_iteration_color_change:
            list_to_change = change[0]
            color_to_change = change[1]
            self.colors[color_to_change] = list_to_change
            for vertex in list_to_change:
                vertex.set_color(color_to_change)
        self.this_iteration_color_change = list()
