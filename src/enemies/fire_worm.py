import pygame

from ..utils import load_image, slice_sprite_sheet_row
from ..animation import Animation
from .enemy import Enemy

class FireWormEnemy(Enemy):

    def __init__(self, pos: tuple[int, int]):
        super().__init__()

        attack_sheet = load_image("worm_attack.png")
        death_sheet = load_image("worm_death.png")
        hit_sheet = load_image("worm_hit.png")
        idle_sheet = load_image("worm_idle.png")
        walk_sheet = load_image("worm_walk.png")

        attack_frames = slice_sprite_sheet_row(
            attack_sheet, row=0, frame_w=64, frame_h=64, num_frames=16)
        death_frames = slice_sprite_sheet_row(
            death_sheet, row=0, frame_w=64, frame_h=64, num_frames=8)
        hit_frames = slice_sprite_sheet_row(
            hit_sheet, row=0, frame_w=64, frame_h=64, num_frames=3)
        idle_frames = slice_sprite_sheet_row(
            idle_sheet, row=0, frame_w=64, frame_h=64, num_frames=9)
        walk_frames = slice_sprite_sheet_row(
            walk_sheet, row=0, frame_w=64, frame_h=64, num_frames=9)
        
        attack_anim = Animation(attack_frames, frame_duration=50)
        death_anim = Animation(death_frames, frame_duration=100, loop=False)   
        hit_anim = Animation(hit_frames, frame_duration=100, loop=False)
        idle_anim = Animation(idle_frames, frame_duration=150)
        walk_anim = Animation(walk_frames, frame_duration=100)

        self.animations = {
            "attack": attack_anim,
            "death": death_anim,
            "hit": hit_anim,
            "idle": idle_anim,
            "walk": walk_anim
        }
        self.current_animation = self.animations["idle"]
        self.image = self.current_animation.get_current_frame()
        self.rect = self.image.get_rect(topleft=pos)

        self.health = 30
        



