from obstacle_avoidance import *


# graph = SquareGraph(30)
# start = (1,1)
# end = (8,9)
# agent_path_locations = []
# nieve_path_forward(graph, start, end)


# graph = SquareGraph(30)
# start = (1,1)
# end = (8,9)
# agent_path_locations = []
# came_from = informed_path_forward(graph, start, end)

# Wrapper class for entire program. Has access to two obsticles, agent, and room functions
class ObsticleAvoidanceScenario:
   def __init__(self, input_file):
      self.load_initial_state(input_file)
      self.room = SquareGraph(self.roomsize)
      self.agent_path = []

   def load_initial_state(self, input_file):
      with open(input_file) as f:
         in_file = [line.rstrip('\n') for line in open(input_file)]

      # Agent
      self.roomsize = int(in_file[0])
      self.agent_sl = self.instring_to_tuple(in_file[1])
      self.agent_fl= self.instring_to_tuple(in_file[2])
      self.agent_location = self.agent_sl

      # Obsticle 1
      obsticle1_sl = self.instring_to_tuple(in_file[3])
      obsticle1_speed = int(in_file[4])
      obsticle1_velocity = self.instring_to_tuple(in_file[5])
      self.obsticle1 = Obstical(obsticle1_sl, obsticle1_speed, obsticle1_velocity, self.roomsize)

      # Obsticle 2
      obsticle2_sl = self.instring_to_tuple(in_file[6])
      obsticle2_speed = int(in_file[7])
      obsticle2_velocity = self.instring_to_tuple(in_file[8])
      self.obsticle2 = Obstical(obsticle2_sl, obsticle2_speed, obsticle2_velocity, self.roomsize)

   def pathfind_optimized(self):
      came_from = a_star_search(self.room, self.agent_fl, self.agent_sl)

      while self.agent_location != self.agent_fl:
         self.print_graph_with_path()
         self.agent_location = came_from[self.agent_location]

      print self.agent_location
      self.print_graph_with_path()

      print "Total number nodes visited in optimized implementation: %d" % (len(came_from))
      return came_from

   def pathfind_nieve(self):
      came_from = breadth_first_search_modified(self.room, self.agent_fl)

      while self.agent_location != None:
         self.print_graph_with_path()
         self.agent_location = came_from[self.agent_location]

      print "Total number nodes visited in nieve implementation: %d" % (len(came_from))

   # Helper function for laoding tuples
   def instring_to_tuple(self,instring):
      striped = map(int, instring.split('(')[1].split(')')[0].split(','))
      return striped[0], striped[1]

   # Helper function to show state of room
   def print_graph_with_path(self):
      print "\nAgent location: %s\nObsticle 1 location: %s\nObsticle 2 location: %s" % (str(self.agent_location), str(self.obsticle1.location), str(self.obsticle2.location))

      for i in range(1, self.roomsize + 1):
         row_out = ""
         for j in range(1, self.roomsize + 1):

            if ((i, j) == self.agent_location):
               row_out += " O "
               self.agent_path.append((i,j))

            elif((i,j) in self.agent_path):
               row_out += " O "
            elif ((i, j) == self.obsticle1.location or (i, j) == self.obsticle2.location):
               row_out += " X "
            else:
               row_out += " - "
         print row_out


# initializeing a scenario and accessing it's attributes
scenario = ObsticleAvoidanceScenario('room.txt')
print scenario.agent_sl
print scenario.agent_fl
print scenario.obsticle1.location
print scenario.obsticle2.velocity
# scenario.pathfind_optimized()
scenario.pathfind_nieve()
