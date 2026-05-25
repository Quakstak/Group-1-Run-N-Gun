from __future__ import annotations
import pygame
from ..utils import load_image
from ..weapons.shotgun import Shotgun


class ShotgunPickup(pygame.sprite.Sprite):
    PICKUP_NAME ="shotgun"
    def __init__(self, x: int, y: int):
        super().__init__()

        self.image = load_image("Shotgun.png")
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.rect = self.image.get_rect(topleft=(x, y))

    def apply(self, player) -> None:
        player.weapon = Shotgun()

    def update(self, dt: float, *_args) -> None:
        pass