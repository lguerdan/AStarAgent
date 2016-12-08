import collections, heapq

# Used in bfs
class Queue:
   def __init__(self):
      self.elements = collections.deque()

   def empty(self):
      return len(self.elements) == 0

   def set(self, x):
      self.elements.append(x)

   def next(self):
      return self.elements.popleft()

# Used in a star to mantain set of min-distance nodes
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

   #Utility function to return valid adjacent nodes to current position
   def get_neighbors(self, position):
      (x, y) = position
      neighbors = [(x + 1, y), (x - 1, y), (x, y+ 1), (x, y - 1), (x - 1, y - 1), (x + 1, y + 1), (x-1, y + 1), (x + 1, y - 1)]
      neighbors = filter(self.in_graph, neighbors)
      return neighbors

   # Helper function to return cost of visiting 2 nodes
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


# Wrapper for object state and behavior
class Obstical(SquareGraph):
   def __init__(self, location, speed, direction, graph):
      self.location = location
      self.location_next = None
      self.graph = graph
      self.speed = speed
      self.direction = direction
      self.roomsize = graph.size

   # obsticle driver function, incraments movement by one time interval
   def move(self):
      num_moves = self.speed

      # If speed greater than once, break up movement interval for proper movement
      while (num_moves > 0):

         #init location_next on first iteration
         if (self.location_next == None):
            self.location_next = self.next()
            self.correct_next()

         # Update location to next position and correct if necessary
         self.location = self.location_next
         self.location_next = self.next()
         self.correct_next()
         num_moves -= 1

   # iterater-style function to get next location on current trajectory
   def next(self):
      direction_x, direction_y = self.direction
      x, y = self.location
      pos_x = direction_x  + x
      pos_y = direction_y  + y
      return (pos_x, pos_y)

   #given next obsticle location, correct trajectory by changing direction if out of bounds
   def correct_next(self):
      if (not self.in_graph(self.location_next)):
         next_x, next_y = self.location_next
         dir_x, dir_y = self.direction

         if (next_y < 1):
            dir_y = abs(dir_y)

         if(next_y > self.roomsize):
            dir_y = -1 * dir_y

         if (next_x < 1):
            dir_x = abs(dir_x)

         if (next_x > self.roomsize):
            dir_x = -1 * dir_x

         self.direction = (dir_x, dir_y)
         self.location_next = self.next()

# Returns a boolean value based on whether the provided location is within the square room
   def in_graph(self,position):
      (x, y) = position
      return 1 <= x <= self.roomsize and 1 <= y <= self.roomsize

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

# Optimized search from start to finsih, uses heuristic and dijkstras algorithm.
def a_star_search(graph, start, goal):
   # Mantain set of next nodes to visit
   frontier = PriorityQueue()
   frontier.put(start, 0)
   came_from = {}
   cost_so_far = {}
   came_from[start] = None
   cost_so_far[start] = 0

   #While nodes unvisited, keep visiting frontier nodes
   while not frontier.isempty():
      current = frontier.get()
      if current == goal:
         break

      for next in graph.get_neighbors(current):

         #Store current cost for later features like walls if added
         new_cost = cost_so_far[current] + graph.get_cost(next, current)
         if next not in cost_so_far or new_cost < cost_so_far[next]:
            cost_so_far[next] = new_cost
            # Set priority based on manhattan distance
            priority = new_cost + heuristic(goal, next)
            frontier.put(next, priority)
            came_from[next] = current

   #Return verticies came from
   return came_from
