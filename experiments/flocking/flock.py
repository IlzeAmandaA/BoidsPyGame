import numpy as np
from experiments.flocking.boid import Boid
from experiments.swarm import Swarm
from experiments import helperfunctions
from experiments.physical_objects import Objects

"""
Specific flock properties, and flocking environment definition 
"""

#General settings for a floccking
RADIUS_VIEW=200

#Define the environment
OBSTACLES = True
OUTSIDE = True
CONVEX = True

class Flock(Swarm): #also access methods from the super class Swarm
    def __init__(self, screen_size):
        super(Flock, self).__init__(screen_size)
        self.objects = Objects()
        self.object_loc = OUTSIDE

    def add_agents(self, pos):
        super(Flock,self).add_agent(Boid(pos=np.array(pos),v=None))


    def initialize(self, num_agents):

        #add obstacle/-s to the environment if present
        if OBSTACLES:
            object_loc = [self.screen[0]/2.,self.screen[1]/2.]

            if OUTSIDE:
                scale = [300,300]
            else:
                scale = [700,700]

            filename = 'experiments/flocking/images/convex.png' if CONVEX else 'experiments/flocking/images/redd.png'

            self.objects.add_obstacle(file= filename, pos=object_loc, scale=scale)

            min_x, max_x = helperfunctions.area(object_loc[0], scale[0])
            min_y, max_y = helperfunctions.area(object_loc[1], scale[1])


        #add obstacles to the swarm for easier functionality
        self.obstacles = self.objects.obstacles

        #add agents to the environment
        for agent in range(num_agents):
            coordinates = helperfunctions.generate_coordinates(self.screen)

            #if obstacles present re-estimate the corrdinates
            if OBSTACLES:
                if OUTSIDE:
                    while coordinates[0]<=max_x and coordinates[0]>=min_x and coordinates[1]<=max_y and coordinates[1]>=min_y:
                        coordinates = helperfunctions.generate_coordinates(self.screen)
                else:
                    while coordinates[0]>=max_x or coordinates[0]<=min_x or coordinates[1]>=max_y or coordinates[1]<=min_y:
                        coordinates = helperfunctions.generate_coordinates(self.screen)

            self.add_agents(coordinates)


    def find_neighbor_velocity(self, neighbors):
        neighbor_sum_v = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_v += list(self.agents)[idx].v
        return neighbor_sum_v


    def find_neighbor_center(self, neighbors):
        neighbor_sum_pos = np.zeros(2)
        for idx in neighbors:
            neighbor_sum_pos += list(self.agents)[idx].pos
        return neighbor_sum_pos


    def find_neighbor_seperation(self,neighbors,boid):
        seperate = np.zeros(2)
        for idx in neighbors:
            neighbor_pos = list(self.agents)[idx].pos
            difference = boid.pos - neighbor_pos
            difference /= helperfunctions.dist(boid.pos, neighbor_pos)
            seperate += difference
        return seperate

    def update(self):
        for boid in self.agents:
            neighbors, count = self.find_neighbors(boid, RADIUS_VIEW)
            if count:
                align_force = self.find_neighbor_velocity(neighbors) / count
                cohesion_force = self.find_neighbor_center(neighbors) / count
                separate_force = self.find_neighbor_seperation(neighbors, boid) / count
            else:
                align_force, cohesion_force, separate_force = (0.,0.), (0.,0.), (0.,0.)

            boid.update_actions(self.obstacles, self.object_loc, align_force, cohesion_force, separate_force)

        self.remain_in_screen()

        self.update_general()
