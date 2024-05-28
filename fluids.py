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
    def __init__(self, pos, vel, acc, mass, radius):
        """
        1. Add mass to this simulation
        2. Follow proper physics formulas for collisons and stuff
        3. Try adding forming of liquids or something like slime
        """
        self.pos = np.asarray(pos, dtype=np.float64)
        self.vel = np.asarray(vel, dtype=np.float64)
        self.acc = np.asarray(acc, dtype=np.float64)
        self.mass = mass
        self.radius = radius


    def draw(self):
        pygame.draw.circle(screen, "white", self.pos, self.radius)
    
    def accelerate(self):
        self.acc[1] += 9.8 * 0.0166


    def update(self):
        particle.calcWallCollision()
        self.accelerate()
        self.vel += self.acc
        self.pos += self.vel * 0.0166  # Will probably need to change this!
    
    def calcWallCollision(self):
        if self.pos[1] + self.radius > screen_height: # Floor Collision
            self.pos[1] = screen_height - self.radius - 1
            self.vel[1] *= -1 * dampeningValue
        if self.pos[1] - self.radius < 0: # Ceiling Collision
            self.pos[1] = self.radius + 1
            self.vel[1] *= -1 * dampeningValue
        if self.pos[0] + self.radius > screen_width: # Right Wall Collision
            self.pos[0] = screen_width - self.radius
            self.vel[0] *= -1 * 0.8
        if self.pos[0] - self.radius < 0: # Left Wall Collision
            self.pos[0] = self.radius
            self.vel[0] *= -1 * 0.8
    
    def calcParticleCollision(self, particles):
        for other in particles:
            if other != self:
                distance = np.linalg.norm(other.pos - self.pos)
                minDistance = self.radius + other.radius

                if distance < minDistance:
                    overlap = float(self.radius + other.radius - distance)

                    self.pos += overlap
                    other.pos -= overlap
                    
                    """NEED TO ACTUALLY IMPLEMENT THIS COLLISION!!!"""
                    other.vel *= -1 
            else: pass


running = True

particles = []

while running:    

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            particle = Particle((mouse_x, mouse_y), [r.choice([-2, -1, 1, 2]), r.choice([-2, -1, 1, 2])], [0,0], 10, 10)
            particles.append(particle)
    
    screen.fill((33, 33, 33))

    for particle in particles:
        particle.calcParticleCollision(particles)
        particle.update()
        particle.draw()

    
    pygame.display.update()
    clock.tick(60)