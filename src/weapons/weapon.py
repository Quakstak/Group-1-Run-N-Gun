# weapon.py
# Generic weapon framework with "spread burst" shots.
#
# New behaviour:
# - When a weapon fires, it spawns N bullets at once (a burst / spread).
# - Each weapon defines:
#     * burst_bullets: number of bullets spawned per trigger pull
#     * spread_deg: maximum spread angle from horizontal (degrees)
#     * cooldown: time before the weapon can fire again (seconds)
#
# Spread rule:
# - One bullet is fired horizontally (0 degrees).
# - Remaining bullets are distributed as evenly as possible across [-spread_deg, +spread_deg].
#
# This supports:
# - Pistol: burst_bullets=1, spread_deg=0, short cooldown
# - Shotgun: burst_bullets=7, spread_deg=18, longer cooldown
# - SMG: burst_bullets=3, spread_deg=8, longer cooldown than pistol, etc.

from __future__ import annotations
import math
import pygame
from .. import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, vel: pygame.Vector2):
        super().__init__()
        self.image = pygame.Surface((10, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 230, 120), (0, 0, 10, 4))
        self.rect = self.image.get_rect(center=(pos.x, pos.y))

        self.vel = pygame.Vector2(vel)
        self.lifetime = settings.BULLET_LIFETIME
        self.alive_time = 0.0

    def update(self, dt: float, level) -> None:
        # Move
        self.rect.x += int(self.vel.x * dt)
        self.rect.y += int(self.vel.y * dt)

        # Despawn after lifetime
        self.alive_time += dt
        if self.alive_time >= self.lifetime:
            self.kill()
            return

        # Collide with solid tiles
        if level.rect_collides_solid(self.rect):
            self.kill()

# Ben: added a new bullet type for the charge attack, its a adifferent color and size
class ChargeBullet(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, vel: pygame.Vector2):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 15, 15))
        self.rect = self.image.get_rect(center=(pos.x, pos.y))

        self.vel = pygame.Vector2(vel)
        self.lifetime = settings.BULLET_LIFETIME
        self.alive_time = 0.0

    def update(self, dt: float, level) -> None:
        # Move
        self.rect.x += int(self.vel.x * dt)
        self.rect.y += int(self.vel.y * dt)

        # Despawn after lifetime
        self.alive_time += dt
        if self.alive_time >= self.lifetime:
            self.kill()
            return

        # Collide with solid tiles
        if level.rect_collides_solid(self.rect):
            self.kill()
class Weapon:
    """Generic weapon that fires a spread/burst then enters a cooldown."""

    def __init__(
        self,
        burst_bullets: int = 1,
        spread_deg: float = 0.0,
        cooldown: float = 0.15,
        charge_cooldown: float = 1.0, # Ben: added a separate cooldown for the charge attack
        bullet_speed: float | None = None,
    ):
        if burst_bullets < 1:
            raise ValueError("burst_bullets must be >= 1")
        if spread_deg < 0:
            raise ValueError("spread_deg must be >= 0")
        if cooldown < 0:
            raise ValueError("cooldown must be >= 0")

        self.burst_bullets = burst_bullets
        self.spread_deg = spread_deg
        self.cooldown = cooldown
        self.charge_cooldown = charge_cooldown # Ben: store the charge attack cooldown
        self.bullet_speed = float(bullet_speed) if bullet_speed is not None else float(settings.BULLET_SPEED)

        self.cooldown_timer = 0.0
        self.charge_cooldown_timer = 0.0 # Ben: timer for the charge attack cooldown

    def update(self, dt: float) -> None:
        if self.cooldown_timer > 0.0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)
        if self.charge_cooldown_timer > 0.0:
            self.charge_cooldown_timer = max(0.0, self.charge_cooldown_timer - dt)

    def can_shoot(self) -> bool:
        return self.cooldown_timer <= 0.0
    
    # Ben: added a method to check if the charge attack can be used
    def can_charge_shoot(self) -> bool:
        return self.charge_cooldown_timer <= 0.0

    def _start_cooldown(self) -> None:
        self.cooldown_timer = self.cooldown

    # Ben: added a method to start the charge attack cooldown
    def _start_charge_cooldown(self) -> None:
        self.charge_cooldown_timer = self.charge_cooldown

    def _compute_angles(self) -> list[float]:
        """Return a list of angles in degrees for this burst.

        Ensures one bullet is exactly 0 degrees.
        """
        n = self.burst_bullets
        if n == 1 or self.spread_deg == 0.0:
            return [0.0]

        # Even spacing across [-spread, +spread]
        # Ensure one exact 0 deg shot by snapping the closest-to-zero entry.
        angles = [(-self.spread_deg + (2 * self.spread_deg) * (i / (n - 1))) for i in range(n)]
        # snap closest to 0
        idx = min(range(n), key=lambda i: abs(angles[i]))
        angles[idx] = 0.0
        return angles

    def shoot(self, bullets_group: pygame.sprite.Group, pos: pygame.Vector2, direction: int) -> None:
        """Fire a burst spread if not on cooldown."""
        if not self.can_shoot():
            return

        for deg in self._compute_angles():
            rad = math.radians(deg)
            vx = math.cos(rad) * self.bullet_speed * direction
            vy = -math.sin(rad) * self.bullet_speed  # up is negative y
            bullets_group.add(Bullet(pos, pygame.Vector2(vx, vy)))

        self._start_cooldown()

    # Ben: added a charge shoot method for a stronger attack with a longer cooldown
    def charge_shoot(self, bullets_group: pygame.sprite.Group, pos: pygame.Vector2, direction: int) -> None:
        """Fire a stronger burst spread if not on cooldown."""
        if not self.can_charge_shoot():
            return

        # For simplicity, let's just double the bullet speed and use the same angles.
        for deg in self._compute_angles():
            rad = math.radians(deg)
            vx = math.cos(rad) * self.bullet_speed * .5 * direction
            vy = -math.sin(rad) * self.bullet_speed * .5  # up is negative y
            bullets_group.add(ChargeBullet(pos, pygame.Vector2(vx, vy)))

        # Start cooldown (could be longer than regular shoot)
        self._start_charge_cooldown()
