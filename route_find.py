from obstacle_avoidance import *

# Wrapper class for entire program. Has access to two obsticles, agent, and room functions
class ObsticleAvoidanceScenario:
   def __init__(self, input_file):
      self.validate_input_file(input_file)
      self.load_initial_state(input_file)
      self.agent_path = []
      self.obsticle_path = []
      self.game_states = []# temp for checking collisions

   def validate_input_file(self, input_file):
      with open(input_file) as f:
         in_file = [line.rstrip('\n') for line in open(input_file)]
         if (len(in_file) != 9):
            print "not correct size"



   def load_initial_state(self, input_file):
      with open(input_file) as f:
         in_file = [line.rstrip('\n') for line in open(input_file)]

      # Agent
      self.roomsize = int(in_file[0])
      self.room = SquareGraph(self.roomsize)

      self.agent_sl = self.instring_to_tuple(in_file[1])
      self.agent_fl= self.instring_to_tuple(in_file[2])
      self.agent_location = self.agent_sl

      # Obsticle 1
      obsticle1_sl = self.instring_to_tuple(in_file[3])
      obsticle1_speed = int(in_file[4])
      obsticle1_direction = self.instring_to_tuple(in_file[5])
      self.obsticle1 = Obstical(obsticle1_sl, obsticle1_speed, obsticle1_direction, self.room)

      # Obsticle 2
      obsticle2_sl = self.instring_to_tuple(in_file[6])
      obsticle2_speed = int(in_file[7])
      obsticle2_direction = self.instring_to_tuple(in_file[8])
      self.obsticle2 = Obstical(obsticle2_sl, obsticle2_speed, obsticle2_direction, self.room)

   # helper function to check for collisions:
   def test_collisions(self):
      for state in self.game_states:
         if (state[0] == state[1] or state[0] == state[2]):
            print "Colision\n: agent:  %s  obs1:  %s obs2:  %s" %(state[0], state[1], state[2])
      else:
         print "No collisions detected"

   def pathfind_optimized(self, optimized=True):

      if (optimized is True):
         self.room.weight[self.obsticle1.location] = 1000
         self.room.weight[self.obsticle2.location] = 1000
         came_from = a_star_search(self.room, self.agent_fl, self.agent_sl)
         print "Total number nodes visited in optimized implementation: %d" % (len(came_from))

      else:
         came_from = breadth_first_search_modified(self.room, self.agent_fl)
         print "Total number nodes visited in nieve implementation: %d" % (len(came_from))

      # when collision detected check step in cardinal directions
      escape_sequence = [(1, 0), (-1,0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
      came_from_temp = {}
      evading = False

      self.print_graph_with_path()
      print self.agent_location

      while self.agent_location != self.agent_fl:
         self.obsticle1.move()
         self.obsticle2.move()

         # check for collision
         next_position = came_from[self.agent_location]

         if (evading == True):
            self.agent_location = came_from_temp[self.obsticle1.location]
            if self.obsticle1.location in came_from_temp: del ame_from_temp[self.obsticle1.location]

         if (next_position != self.obsticle1.location and next_position != self.obsticle2.location):
            self.agent_location = next_position

         else:
            print "colision detected.. Adjusting movement"

            # halt for time cycle if possible
            if(self.agent_location != self.obsticle1.location or self.agent_location != self.obsticle2.location):
               print "Waiting it out.. Staying at current location this interval"
               pass

            else:
               for detour in escape_sequence:
                  offset = next_position + detour
                  if (self.in_graph(offset) and (offset != self.obsticle2.location and offset != self.obsticle1.location)):
                     print "Taking detour.. Moving to position %s" % (offset)
                     came_from_temp[offset] = self.agent_location
                     self.agent_location = offset
                     evading = True

         self.game_states.append([self.agent_location, self.obsticle1.location, self.obsticle2.location])
         self.print_graph_with_path()

      self.print_graph_with_path()

      return came_from


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

            if((i,j) == self.agent_sl):
               row_out += " F "

            elif((i,j) == self.agent_fl):
               row_out += " L "

            elif ((i, j) == self.agent_location):
               row_out += " R "
               self.agent_path.append((i,j))

            elif((i,j) in self.agent_path):
               row_out += " R "

            elif ((i, j) == self.obsticle1.location or (i, j) == self.obsticle2.location):
               # self.obsticle_path.append((i,j))
               row_out += " O "

            elif ((i, j) in self.obsticle_path):
               row_out += " O "

            else:
               row_out += " - "
         print row_out

# initializeing a scenario and accessing it's attributes
scenario1 = ObsticleAvoidanceScenario('room.txt')
# scenario2 = ObsticleAvoidanceScenario('room.txt')

# scenario1.pathfind_nieve()
scenario1.pathfind_optimized(False)
scenario1.test_collisions()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()

# scenario1.print_graph_with_path()
# scenario1.obsticle2.move()
# scenario1.obsticle1.move()








