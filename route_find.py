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

   def load_initial_state(self, input_file):
      with open(input_file) as f:
         in_file = [line.rstrip('\n') for line in open(input_file)]

      # Agent
      self.roomsize = int(in_file[0])
      self.agent_sl = self.instring_to_tuple(in_file[1])
      self.agent_fl= self.instring_to_tuple(in_file[2])

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


   def instring_to_tuple(self,instring):
      striped = map(int, instring.split('(')[1].split(')')[0].split(','))
      return striped[0], striped[1]


# initializeing a scenario and accessing it's attributes
scenario = ObsticleAvoidanceAgent('room.txt')
print scenario.agent_sl
print scenario.agent_fl
print scenario.obsticle1.location
print scenario.obsticle2.velocity
