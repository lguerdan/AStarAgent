from implementation import *
class GridNode:
   def __init__(self, x, y):
      self.x = x
      self.y = y

class Obstical:
   def __init__(self, location, velocity):
      self.location = location
      self.velocity = velocity


class SquareGraph:
   def __init__(self, size):
      self.edges = {}
      self.size = size

   # def neighbors(self, id):
   #      return self.edges[id]

   def in_graph(self, position):
      (x, y) = position
      return 1 <= x <= self.size and 1 <= y <= self.size

   # def passable(self, position):
   #    return position not in self.walls

   def get_neighbors(self, position):
      (x, y) = position
      neighbors = [(x + 1, y), (x - 1, y), (x, y+ 1), (x, y - 1), (x - 1, y - 1), (x + 1, y + 1), (x-1, y + 1), (x + 1, y - 1)]
      neighbors = filter(self.in_graph, neighbors)
      return neighbors

   # def grid_to_graph(self):

   #    for i in range(0, self.size):
   #       edges[i] = {}

   #       for j in range(0, self.size):
   #          grid_node = GridNode(i,j)
   #          edges[i][j] = grid_node

   #          #add adjacent horizontal nodes
   #          if i < self.size:
   #             add adjacent horizontal nodes
   #             (ij), (i+1, j)

   #          #add adjacent vertical nodes
   #          if j < self.size:
   #             add adjacent vertical nodes
   #             (ij), (i, j+1)

   #          #add diagnol nodes
   #          if (i < self.size and j < self.size):
   #             (ij)(i+ 1, j+ 1)
   #             (i+ 1,j) (i, j+ 1)


def print_graph(graph):
   for i in range(1, graph.size + 1):
      for j in range(1, graph.size + 1):

         print str(i) + str(j) + ":  " + str(graph.get_neighbors((i, j)))

graph = SquareGraph(5)
print_graph(graph)


import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


def breadth_first_search_2(graph, start):
    # return "came_from"
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()
        for next in graph.get_neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from

came_from = breadth_first_search_2(graph, (1,1))
for key, val in came_from.items():
   print key, val

draw_grid(diagram4, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))