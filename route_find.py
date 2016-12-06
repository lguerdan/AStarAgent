from obstacle_avoidance import *

# Wrapper class for entire program. Has access to two obsticles, agent, and room functions
class ObsticleAvoidanceScenario:
   def __init__(self, input_file):
      self.load_initial_state(input_file)
      self.agent_path = []
      self.obsticle_path = []
      self.game_states = []# temp for checking collisions

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
          
          # NEXT: make comparison account for velocity of obstacles!!! *****
         position1 = self.obsticle1.location
         print "position 1: %s" % (str(position1))
         # It doesn't seem to like this line of code... *****
         # Wait. Fixed it. See the "correct_next" function in obstacle_avoidance.py for changes made
         position2 = self.obsticle1.correct_next()
         print "position 2: %s" % (str(position2))
         if(position1 == position2):
            print "Stationary object"
            self.room.weight[self.obsticle1.location] = 1000
         
#         position1 = self.obsticle2.location
#         position2 = self.obsticle2.next()
#         if(position1 == position2):
#            print "Stationary object"
#            self.room.weight[self.obsticle2.location] = 1000

          
          
          # FIGURE THIS PART OUT! *****
#         self.room.weight[self.obsticle1.location] = 1000
#         self.room.weight[self.obsticle2.location] = 1000
         came_from = a_star_search(self.room, self.agent_fl, self.agent_sl)
         print "Total number nodes visited in optimized implementation: %d" % (len(came_from))

      else:
         came_from = breadth_first_search_modified(self.room, self.agent_fl)
         print "Total number nodes visited in nieve implementation: %d" % (len(came_from))

      # when collision detected check step in cardinal directions
      escape_sequence = [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
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
            print "Evasion logic being run"
            # Only accounts for obstacle 1 *****
            #self.agent_location = came_from_temp[self.obsticle1.location]
            
            # THIS PART PROBABY NEEDS SOME FINE-TUNING, considering that I don't fully understand what's going on here... *****
            if self.obsticle1.location in came_from_temp:
                self.agent_location = came_from_temp[self.obsticle1.location]
                del came_from_temp[self.obsticle1.location]
            elif self.obsticle2.location in came_from_temp:
                self.agent_location = came_from_temp[self.obsticle2.location]
                del came_from_temp[self.obsticle2.location]
            else:
                print "There has been an evasion error"
            
            # Otherwise, evading would remain True until termination *****
            evading = False

         if (next_position != self.obsticle1.location and next_position != self.obsticle2.location):
            self.agent_location = next_position
            print "Proceeding as planned..."

         else:
            print "colision detected.. Adjusting movement"

            # halt for time cycle if possible
            # Perhaps change this "or" to an "and" iot have the robot evade when necessary *****
            if(self.agent_location != self.obsticle1.location and self.agent_location != self.obsticle2.location):
               print "Waiting it out.. Staying at current location this interval"
               pass

            else:
               while(self.agent_location == self.obsticle1.location or self.agent_location == self.obsticle2.location):
                # HOLY SHIT I CAN'T BELIEVE THAT THAT LINE OF CODE ACTUALLY FIXED THE PROBLEM!!!*****
                   gen = (detour for detour in escape_sequence if evading != True)
                   for detour in gen:
                        #This line creates a tuple with four values, making offset incompatible with in_graph*****
                        #offset = next_position + detour
                   
                        #This line effectively adds the two tuples together, resulting offset being a tuple with only two values which represents the coordinates of the escape space being moved to. This allows offset to be compatible with in_graph *****
                        offset = tuple(map(lambda x, y: x + y, self.agent_location, detour))
                        #~~~~~~~~~~~~
                        print "Considering moving to %s" % (offset,)
                        #~~~~~~~~~~~~
                        # replaced this with two if statements iot give feedback as to why a considered escape may not be chosen *****
                        #if (self.room.in_graph(offset) and (offset != self.obsticle2.location and offset != self.obsticle1.location)):
                        if (not self.room.in_graph(offset)):
                            print ", but %s not in room" % (offset,)
                        elif (offset == self.obsticle2.location or offset == self.obsticle1.location):
                            print ", but %s would lead to collision" % (offset,)
                        else:
                            print "Taking detour.. Moving to position %s" % (offset,)
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

            if((i,j) == self.obsticle1.location or (i,j) == self.obsticle2.location):
                # self.obsticle_path.append((i,j))
                row_out += " O "
            
            elif ((i, j) == self.agent_location):
                row_out += " R "
                self.agent_path.append((i,j))

            elif((i,j) == self.agent_sl):
               row_out += " F "

            elif((i,j) == self.agent_fl):
               row_out += " L "

            elif((i,j) in self.agent_path):
               row_out += " + "
            
            #This line would have caused the print to display the path that was planned out from the initial a-star search, but it's a shitshow whenever I try to get it working, so I give up... *****
#            elif((i,j) in came_from):
#               row_out += " = "

#            elif ((i, j) == self.obsticle1.location or (i, j) == self.obsticle2.location):
#               # self.obsticle_path.append((i,j))
#               row_out += " O "

            elif ((i, j) in self.obsticle_path):
               row_out += " O "

            else:
               row_out += " - "
         print row_out
      print "\n"

# initializeing a scenario and accessing it's attributes
scenario1 = ObsticleAvoidanceScenario('room16.txt')
# scenario2 = ObsticleAvoidanceScenario('room.txt')

# scenario1.pathfind_nieve()
scenario1.pathfind_optimized()
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








