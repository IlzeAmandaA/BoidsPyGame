import pygame
from experiments.flocking.flock import Flock


"""
General simulation pipeline, suitable for all experiments 
"""

ITER=10000 #define

class Simulation():
    def __init__(self, num_agents, screen_size, swarm_type, iterations):


        #general settings
        self.screensize = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.sim_background = pygame.Color('gray21')
        self.iter = iterations

        #swarm settings
        self.num_agents = num_agents
        self.swarm = Flock(screen_size) if swarm_type == 'Flock' else None

        #update
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.running = True



    def display(self):
        for sprite in self.to_display:
            sprite.display(self.screen)

    def update(self):
        self.to_update.update()


    def initialize(self):

        #initialize a swarm type specific environment
        self.swarm.initialize(self.num_agents, self.swarm)

        #add all agents/objects to the update
        self.to_update = pygame.sprite.Group(self.swarm)

        #add all agents/objects to display
        self.to_display = pygame.sprite.Group(
            self.to_update
        )

    def simulate(self):
        self.screen.fill(self.sim_background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.update()
        self.display()
        pygame.display.flip()



    def run(self):
        #initialize the environment and agent/obstacle positions
        self.initialize()

        #the simulation loop, infinite until the user exists the simulation
        #finite time parameter or infinite
        if self.iter == -1:
            while self.running:
                self.simulate()
        else:
            for i in range(self.iter):
                self.simulate()


