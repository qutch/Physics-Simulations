import pygame
from pygame import gfxdraw
import random as r
import numpy as np

pygame.init()


screen_height = 720
screen_width = 1280
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

dampeningValue = 0.9


class Particle:
    def __init__(self, pos, vel, acc, radius):
        self.pos = np.asarray(pos, dtype=np.float64)
        self.vel = np.asarray(vel, dtype=np.float64)
        self.acc = np.asarray(acc, dtype=np.float64)
        self.radius = radius


    def draw(self):
        pygame.draw.circle(screen, "white", self.pos, self.radius)
    
    def accelerate(self):
        pass

    def update(self):
        self.accelerate()
        self.pos += self.vel
    
    def calcWallCollision(self):
        if self.pos[1] + self.radius > screen_height:
            self.pos[1] = screen_height - self.radius
            self.vel[1] *= -1 * dampeningValue
        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.vel[1] *= -1 * dampeningValue


running = True

particles = []

while running:    

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            particle = Particle((mouse_x, mouse_y), [r.randint(-5, 5),r.randint(-5, 5)], [0,0], 10)
            particles.append(particle)
    
    screen.fill((33, 33, 33))

    for particle in particles:
        particle.draw()
        particle.calcWallCollision()
        particle.update()

    
    
    pygame.display.update()
    clock.tick(60)