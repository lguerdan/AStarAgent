import collections, heapq
agent_path_locations = []
class Queue:
   def __init__(self):
      self.elements = collections.deque()

   def empty(self):
      return len(self.elements) == 0

   def set(self, x):
      self.elements.append(x)

   def next(self):
      return self.elements.popleft()

class PriorityQueue:
   def __init__(self):
      self.elements = []

   def isempty(self):
      if(len(self.elements) == 0):
         return 0

   def put(self, item, priority):
      heapq.heappush(self.elements, (priority, item))

   def get(self):
      return heapq.heappop(self.elements)[1]

class SquareGraph:
   def __init__(self, size):
      self.size = size
      self.weight = {}

   def in_graph(self, position):
      (x, y) = position
      return 1 <= x <= self.size and 1 <= y <= self.size

   def get_neighbors(self, position):
      (x, y) = position
      neighbors = [(x + 1, y), (x - 1, y), (x, y+ 1), (x, y - 1), (x - 1, y - 1), (x + 1, y + 1), (x-1, y + 1), (x + 1, y - 1)]
      neighbors = filter(self.in_graph, neighbors)
      return neighbors

   def get_cost(self, to_node, from_node):
      if (to_node in self.weight):
         return self.weight[to_node]
      else:
         return 1

   # Helper function to show adjacency list of graph
   def print_adj_graph(self, graph):
      for i in range(1, graph.size + 1):
         for j in range(1, graph.size + 1):

            print str(i) + str(j) + ":  " + str(graph.get_neighbors((i, j)))


class Obstical(SquareGraph): # inherits from square graph so we can use in_graph method
   def __init__(self, location, speed, velocity, graph):
      self.location = location
      self.location_next = self.move()
      self.graph = graph
      self.speed = speed
      self.velocity = velocity
      self.roomsize = graph.size
      #also state for t + 1 location here

   def move(self):
      x, y = self.location
      velocity_x, velocity_y = self.velocity
      speed_x, speed_y = self.speed
      pos_x = (velocity_x * speed_x) + x
      pos_y = (velocity_y * speed_y) + y
      print pos_x, pos_y


      '''
      # obstical logic here.
      1) Check graph size and boundaries (using in_graph method)
      2) next position based on current velocity
      3) We will also need to store state of t + 1 position to Check for collisions
      '''


# distance-based cost function for dijkstras
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


'''Here is a demo traversal technique using only bfs with the came_from attribute.
We run BFS from the finish vertex and follow the came_from
from the start until we hit none (the source/finish vertex). Not really optimal though because BFS will visit all nodes first'''
def breadth_first_search_modified(graph, start):
   boundary = Queue()
   boundary.set(start)
   came_from = {}
   came_from[start] = None

   while not boundary.empty():
      current = boundary.next()
      for next in graph.get_neighbors(current):
         if next not in came_from:
            boundary.set(next)
            came_from[next] = current

   return came_from

def nieve_path_forward(graph, start, finish):
   came_from = breadth_first_search_modified(graph, finish)
   #Lets try swapping came from to go_to by exchanging keys and values
   # go_to = dict((v,k) for k,v in came_from.iteritems())

   agent_position = start
   while agent_position != None:
      print agent_position
      print_visual_graph_with_path(graph, agent_position)
      agent_position = came_from[agent_position]

   print "Total number nodes visited in nieve implementation: %d" % (len(came_from))


def a_star_search(graph, start, goal):
   frontier = PriorityQueue()
   frontier.put(start, 0)
   came_from = {}
   cost_so_far = {}
   came_from[start] = None
   cost_so_far[start] = 0

   while not frontier.isempty():
      current = frontier.get()
      if current == goal:
         break

      for next in graph.get_neighbors(current):
         new_cost = cost_so_far[current] + graph.get_cost(next, current)
         if next not in cost_so_far or new_cost < cost_so_far[next]:
            cost_so_far[next] = new_cost
            priority = new_cost + heuristic(goal, next)
            frontier.put(next, priority)
            came_from[next] = current

   return came_from

