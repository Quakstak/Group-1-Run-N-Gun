import pygame
from ..animation import Animation

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=200):
        super().__init__()

        self.direction = direction
        self.speed = 200
        self.exploding = False

