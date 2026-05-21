from __future__ import annotations
import pygame

from ..utils import load_image, slice_sprite_sheet_row
from ..animation import Animation
from .. import settings
from .enemy import Enemy

class FireWormEnemy(Enemy):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()


        idle_sheet = load_image("worm_idle.png")
        die_sheet = load_image("worm_death.png")
        attack_sheet = load_image("worm_attack.png")


        idle_frames = slice_sprite_sheet_row(
            idle_sheet, row=0, frame_w=20, frame_h=31,
            num_frames=8, stride_x=21, start_x=0, start_y=0,
            clamp = True
        )
        die_frames = slice_sprite_sheet_row(
            die_sheet, row=0, frame_w=20, frame_h=31,
            num_frames=8, stride_x=21, start_x=0, start_y=0,
            clamp = True
        )
        attack_frames = slice_sprite_sheet_row(
            attack_sheet, row=0, frame_w=20, frame_h=31,
            num_frames=8, stride_x=21, start_x=0, start_y=0
            clamp= True
        )

        self.state = "IDLE"
        self.idle_anim = Animation(idle_frames, frame_duration=0.25, loop = True)
        self.current_anim = self.idle_anim

        self.image = self.current_anim.image
        self.rect = self.image.get_rect(topleft=pos)
        
        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(0.0, 0.0)
        self.on_ground = False

    def update(self, dt: float, level, player) -> None:
        self.vel.y += settings.GRAVITY * dt

        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        self.on_ground = False
        hits = level.get_solid_hits(self.rect)
        for tile_rect in hits:
            if self.vel.y > 0:
                self.rect.bottom = tile_rect.top
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:
                self.rect.top = tile_rect.bottom
                self.vel.y = 0
            self.pos.y = self.rect.y

        self.apply_anim(dt)



      
    
   





       