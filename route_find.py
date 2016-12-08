from obstacle_avoidance import *
import sys, getopt, glob, os, argparse

# Wrapper class for entire program. Has access to two obsticles, agent, and room functions
class ObsticleAvoidanceScenario:
   def __init__(self, input_file, launcher=False, speedbump=False):

      print launcher
      self.validate_input_file(input_file)
      self.load_initial_state(input_file, launcher, speedbump)
      self.agent_path = []
      self.game_states = []# temp for checking collisions

   # a helper function for validate_input_file()
   def raise_error(self, error):
      if  (error == 0): print "Input error in first line"
      elif(error == 1): print "Input error in second line"
      elif(error == 2): print "Input error in third line"
      elif(error == 3): print "Input error in fourth line"
      elif(error == 4): print "Input error in fifth line"
      elif(error == 5): print "Input error in sixth line"
      elif(error == 6): print "Input error in seventh line"
      elif(error == 7): print "Input error in eighth line"
      elif(error == 8): print "Input error in ninth line"
      elif(error == 9): print "Input error: incorrect filesize"
      else: print "Something went wrong..."
      exit()

   def validate_integer(self, num, min, line):
      if( num.isdigit() ):
         val = int(num)
         if (val < min): self.raise_error(line)
      else:
         self.raise_error(line)

   # helper function for validate_input_file()
   def validate_tuple(self, tuple, line):
      if(not tuple.endswith(")",4)):
         self.raise_error(line)
      if( tuple[0] != '(' ): self.raise_error(line)
      c = 1
      while tuple[c].isdigit(): c += 1
      if( c == 1 ): self.raise_error(line)
      if( tuple[c] != ',' ): self.raise_error(line)
      c += 1
      d = 0
      while tuple[c].isdigit():
         c += 1
         d = d * 10 + int(tuple[c-1])
      if( d == 0 ): self.raise_error(line)
      end = str(d) + ')'
      if(not tuple.endswith(end,3)): self.raise_error(line)

   def validate_dir_tuple(self, tuple, line):
      if(not tuple.endswith(")",4)):
         self.raise_error(line)
      if( tuple[0] != '(' ): self.raise_error(line)
      a = 0
      c = 1
      if( tuple[c] == '+' or tuple[c] == '-' ):
         a = 1
         c += 1
      if( tuple[c].isdigit() ):
         if( int(tuple[c]) != a ):
            self.raise_error(line)
         c += 1
      else:
         self.raise_error(line)
      if( tuple[c] != ',' ): self.raise_error(line)
      a = 0
      c += 1
      if( tuple[c] == '+' or tuple[c] == '-' ):
         a = 1
         c += 1
      if( tuple[c].isdigit() ):
         if( int(tuple[c]) != a ):
            self.raise_error(line)
      else:
         self.raise_error(line)
      end = str(a) + ')'
      if(not tuple.endswith(end,3)): self.raise_error(line)

   def validate_input_file(self, input_file):
      with open(input_file) as f:
         in_file = [line.rstrip('\n') for line in open(input_file)]
         if (len(in_file) != 9): self.raise_error(9)
      # check each line of input
         self.validate_integer(in_file[0], 2, 0)
         self.validate_tuple(in_file[1], 1)
         self.validate_tuple(in_file[2], 2)
         self.validate_tuple(in_file[3], 3)
         self.validate_integer(in_file[4], 0, 4)
         self.validate_dir_tuple(in_file[5], 5)
         self.validate_tuple(in_file[6], 6)
         self.validate_integer(in_file[7], 0, 7)
         self.validate_dir_tuple(in_file[8], 8)

   def load_initial_state(self, input_file, launcher, speedbump):
      with open(input_file) as f:
         in_file = [line.rstrip('\n') for line in open(input_file)]

      # Agent
      self.roomsize = int(in_file[0])
      self.room = SquareGraph(self.roomsize)

      #Speedbump and launcher
      # randomly generate launcher. Speeds by 1 or two when hit
      if (launcher == True):
         self.launcher = (randint(1,self.roomsize), randint(1,self.roomsize))
         self.launchspeed = randint(1,2)
         print "Launcher speed " + str(self.launchspeed) + " placed at " + str(self.launcher)
      else:
         self.launcher = (-1, -1)
         self.launchspeed = 0

      # randomly generate speed bump. Slows obsticles -1 speed when hit
      if (speedbump == True):
         self.speedbump = (randint(1,self.roomsize), randint(1,self.roomsize))
         print "Speedbump placed at " + str(self.speedbump)
      else:
         self.speedbump = (1,-1)

      self.agent_sl = self.instring_to_tuple(in_file[1])
      self.agent_fl= self.instring_to_tuple(in_file[2])
      self.agent_location = self.agent_sl
      self.agent_waits = 0

      # Obsticle 1
      obsticle1_sl = self.instring_to_tuple(in_file[3])
      obsticle1_speed = int(in_file[4])
      obsticle1_direction = self.instring_to_tuple(in_file[5])
      self.obsticle1 = Obstical(obsticle1_sl, obsticle1_speed, obsticle1_direction, self.room, self.launcher, self.launchspeed, self.speedbump)

      # Obsticle 2
      obsticle2_sl = self.instring_to_tuple(in_file[6])
      obsticle2_speed = int(in_file[7])
      obsticle2_direction = self.instring_to_tuple(in_file[8])
      self.obsticle2 = Obstical(obsticle2_sl, obsticle2_speed, obsticle2_direction, self.room, self.launcher, self.launchspeed, self.speedbump)



   # helper function to check for collisions:
   def test_collisions(self):
      for state in self.game_states:
         if (state[0] == state[1] or state[0] == state[2]):
            print "Colision\n: agent:  %s  obs1:  %s obs2:  %s" %(state[0], state[1], state[2])
      else:
         print "No collisions detected"

   def pathfind(self, optimized=True):

      if (optimized is True):

         self.room.weight[self.obsticle1.location] = 1000
         self.room.weight[self.obsticle2.location] = 1000
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

      while self.agent_location != self.agent_fl and self.agent_waits < 6:
         self.obsticle1.move()
         self.obsticle2.move()

         # check for collision
         next_position = came_from[self.agent_location]

         if (evading == True):
            print "Evasion logic being run"

            if self.obsticle1.location in came_from_temp:
                self.agent_location = came_from_temp[self.obsticle1.location]
                del came_from_temp[self.obsticle1.location]
            elif self.obsticle2.location in came_from_temp:
                self.agent_location = came_from_temp[self.obsticle2.location]
                del came_from_temp[self.obsticle2.location]
            else:
                print "There has been an evasion error"

            evading = False

         if (next_position != self.obsticle1.location and next_position != self.obsticle2.location):
            self.agent_location = next_position
            print "Proceeding as planned..."

         else:
            print "colision detected.. Adjusting movement"

            # halt for time cycle if possible
            if(self.agent_location != self.obsticle1.location and self.agent_location != self.obsticle2.location):
               print "Waiting it out.. Staying at current location this interval"
               self.agent_waits += 1
               pass

            else:
               while(self.agent_location == self.obsticle1.location or self.agent_location == self.obsticle2.location):
                   gen = (detour for detour in escape_sequence if evading != True)
                   for detour in gen:
                        offset = tuple(map(lambda x, y: x + y, self.agent_location, detour))
                        print "Considering moving to %s" % (offset,)
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

      #self.print_graph_with_path()
      if( self.agent_waits >= 6 ):
         print "Robot is unable to reach the finish"
         exit()
      else:
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

            elif((i,j) == self.launcher):
               row_out += " " + str(self.launchspeed) + " "

            elif((i,j) == self.speedbump):
               row_out += " ~ "

            else:
               row_out += " - "
         print row_out
      print "\n"


def main(argv):
   inputfile = ''

   # Set up argument parser
   ap = argparse.ArgumentParser()

   ap.add_argument("fname", help="name of room file")
   ap.add_argument("nieve", nargs='?', default=True, help="'False' for nonoptimized search")
   ap.add_argument("speedbump", nargs='?', default=False, help="'True' for randomly generated speed bump")
   ap.add_argument("launcher", nargs='?', default=False, help="'True' for randomly generated launcher")

   a = ap.parse_args()

   # check for read access, else error. With closes automatically because of context
   try:
      with open(a.fname) as fp:
         pass

   except IOError:
       print "Could not read file."
       exit(2)

   a.speedbump = (False if(a.speedbump == "False") else True)
   a.launcher = (False if(a.launcher == "False") else True)
   scenario = ObsticleAvoidanceScenario(a.fname, a.speedbump, a.launcher)


   a.nieve = (False if(a.nieve == "False") else True)
   scenario.pathfind(a.nieve)
   scenario.test_collisions()


if __name__ == "__main__":
   main(sys.argv[1:])

