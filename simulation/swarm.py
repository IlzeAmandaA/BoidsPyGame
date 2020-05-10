import pygame
from simulation import helperfunctions

"""
General swarm class that defines general swarm properties, which are common across different swarm types
"""

#superclass
class Swarm(pygame.sprite.Sprite):

    def __init__(self,screen_size):
        super(Swarm,self).__init__()
        self.agents = pygame.sprite.Group()
        self.screen = screen_size
        self.obstacles = None

    def add_agent(self,agent):
        self.agents.add(agent)

    def find_neighbors(self, agent, radius):
        agents = list(self.agents).copy()
        neighbors = []
        for j, neighbor in enumerate(agents):
            if agent == neighbor:
                continue
            elif helperfunctions.dist(agent.pos, neighbor.pos) < radius:
                neighbors.append(j)
        return neighbors, len(neighbors)

    def remain_in_screen(self):
        for agent in self.agents:
            if agent.pos[0] > self.screen[0]:
                agent.pos[0]=0.
            if agent.pos[0] < 0:
                agent.pos[0] = float(self.screen[0])
            if agent.pos[1] < 0:
                agent.pos[1] = float(self.screen[1])
            if agent.pos[1] > self.screen[1]:
                agent.pos[1]=0.

    def update_general(self):
        for agent in self.agents:
            agent.update()

    def display(self, screen):
        for obstacle in self.obstacles:
            obstacle.display(screen)

        for agent in self.agents:
            agent.display(screen)

        for agent in self.agents:
            agent.reset_frame()
