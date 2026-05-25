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
        death_sheet = load_image("worm_death.png")
        attack_sheet = load_image("worm_attack.png")
        

        idle_frames = slice_sprite_sheet_row(
            idle_sheet, row=0, frame_w=90, frame_h=90,
            num_frames=9, stride_x=90, start_x=0, start_y=0,
            clamp = True
        )
        death_frames = slice_sprite_sheet_row(
            death_sheet, row=0, frame_w=90, frame_h=90,
            num_frames=8, stride_x=90, start_x=0, start_y=0,
            clamp=True
        )
        attack_frames = slice_sprite_sheet_row(
            attack_sheet, row=0, frame_w=90, frame_h=90,
            num_frames=16, stride_x=90, start_x=0, start_y=0,
            clamp=True
        )
    

        self.state = "IDLE"
        self.idle_anim = Animation(idle_frames, frame_duration=0.25, loop=True)
        self.death_anim = Animation(death_frames, frame_duration=0.2, loop=False)
        self.attack_anim = Animation(attack_frames, frame_duration=0.25, loop=False)
        self.current_anim = self.idle_anim

        self.image = self.current_anim.image
        self.rect = self.image.get_rect(topleft=pos)
        
        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(0.0, 0.0)

        self.health = 30
        self.on_ground = False
        self.facing = 1

        self.base_speed = 20

        self.attack_range = 5
        self.attack_damage = 5

    def change_state(self, new_state: str, new_anim: Animation):
        self.state = new_state
        self.current_anim = new_anim 
        if hasattr(self.current_anim, 'reset'):
            self.current_anim.reset()

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health <= 0 and self.state != "DIE":
            self.change_state("DIE", self.death_anim)
            self.vel.x = 0
    
    def update(self, dt: float, level, player) -> None:
        if self.state == "DIE":
            self.current_anim.update(dt)
            self.image = self.current_anim.image

            if self.current_anim.finished:
                self.kill()

            return
        
        dist_x = player.rect.centerx - self.rect.centerx
        abs_dist = abs(dist_x)
        y_dist = abs(player.rect.centery - self.rect.centery)

        self.facing = 1 if dist_x > 0 else -1

        if self.state == "ATTACK":
            self.vel.x = 0


            if self.current_anim.finished:
                self.change_state("IDLE", self.idle_anim)

            self.current_anim.update(dt)
            self.image = self.current_anim.image
            
            return
        

        if abs_dist <= self.attack_range and y_dist < 40:
            self.change_state("ATTACK", self.attack_anim)
            self.vel.x = 0
        else:
            self.change_state("IDLE", self.idle_anim)
            self.vel.x = self.base_speed * self.facing

        self.pos.x += self.vel.x * dt
        self.rect.x = int(self.pos.x)

        self.current_anim.update(dt)
        self.image = self.current_anim.image

        if self.facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)


        









      
    
   





       