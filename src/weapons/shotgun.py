from __future__ import annotations
import math
import pygame
from .weapon import Bullet
from .. import settings


class Shotgun:
    def __init__(self):
        self.cooldown = 0.6
        self.time_since_shot = 999.0
        self.pellets = 5
        self.spread_deg = 20
        self.shots_left = 3

    def update(self, dt):
        self.time_since_shot += dt

    def shoot(self, bullets_group, pos, direction):
        if self.shots_left <= 0:
            return
        if self.time_since_shot < self.cooldown:
            return

        self.time_since_shot = 0
        self.shots_left -= 1

        angles = [(-self.spread_deg + (2 * self.spread_deg) * (i / (self.pellets - 1))) for i in range(self.pellets)]

        for deg in angles:
            rad = math.radians(deg)
            vx = math.cos(rad) * settings.BULLET_SPEED * direction
            vy = -math.sin(rad) * settings.BULLET_SPEED
            bullets_group.add(Bullet(pos, pygame.Vector2(vx, vy)))

    def charge_shoot(self, bullets_group, pos, direction):
        
        pass    