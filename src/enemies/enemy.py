# enemies/enemy.py
from __future__ import annotations
import pygame
from ..animation import Animation


class Enemy(pygame.sprite.Sprite):
    """Base enemy class.

    Provides:
    * health + take_damage()
    * current_anim handling + facing flip
    * face_player() helper
    """

    def __init__(self):
        super().__init__()
        self.health = 1
        self.facing = 1  # 1 right, -1 left

        self.current_anim: Animation | None = None
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect

        self.original_image = self.image.copy()
        self.hit_flash_timer = 0.0

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        self.hit_flash_timer = 0.5
        if self.health <= 0:
            self.kill()

    def apply_anim(self, dt: float) -> None:
        """Advance current animation and apply facing flip."""
        if not self.current_anim:
            return
        self.current_anim.update(dt)
        img = self.current_anim.image
        if self.facing == -1:
            img = pygame.transform.flip(img, True, False)
        self.image = img

    def face_player(self, player) -> int:
        self.facing = 1 if player.rect.centerx > self.rect.centerx else -1
        return self.facing
    
    def update(self, dt):
        self.hit_flash_timer -=dt
        if self.hit_flash_timer > 0:
            # Flash white when hit
            flash = self.original_image.copy()
            flash.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
            self.image = flash
        else:
            self.image = self.original_image.copy()
