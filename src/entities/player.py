"""
Player Entity for Dragon Haven Cafe.
Represents the player character in exploration mode.
"""

import pygame
import math
from typing import Dict, Any, Optional, Tuple, List
from constants import (
    TILE_SIZE, ZONE_WIDTH, ZONE_HEIGHT,
    CHAR_SKIN, CHAR_HAIR_BROWN, CHAR_APRON, CHAR_CLOTHES,
    SCREEN_WIDTH, SCREEN_HEIGHT
)


class Player:
    """
    Player character for exploration mode.

    Handles movement, animation, and interaction with the world.

    Usage:
        player = Player(x, y)
        player.handle_input(keys)
        player.update(dt, collision_check)
        player.draw(surface, camera_offset)
    """

    # Movement speed (tiles per second)
    MOVE_SPEED = 4.0

    # Animation timings
    WALK_FRAME_DURATION = 0.15  # Seconds per animation frame
    IDLE_BOB_SPEED = 2.0        # Idle bob frequency

    def __init__(self, x: int = 0, y: int = 0):
        """
        Initialize the player.

        Args:
            x: Starting tile x position
            y: Starting tile y position
        """
        # Position (in pixels)
        self._tile_x = x
        self._tile_y = y
        self.pixel_x = x * TILE_SIZE + TILE_SIZE // 2
        self.pixel_y = y * TILE_SIZE + TILE_SIZE // 2

        # Movement
        self._velocity_x = 0.0
        self._velocity_y = 0.0
        self._moving = False
        self._facing = 'down'  # down, up, left, right

        # Animation
        self._walk_frame = 0
        self._walk_timer = 0.0
        self._idle_timer = 0.0

        # Interaction
        self._interacting = False
        self._interact_cooldown = 0.0

        # Sprite size
        self.width = 24
        self.height = 32

        # Collision box (smaller than sprite)
        self.collision_width = 16
        self.collision_height = 12

    # =========================================================================
    # POSITION
    # =========================================================================

    def get_tile_position(self) -> Tuple[int, int]:
        """Get current tile position."""
        return (
            int(self.pixel_x // TILE_SIZE),
            int(self.pixel_y // TILE_SIZE)
        )

    def set_tile_position(self, x: int, y: int):
        """Set position to a specific tile."""
        self._tile_x = x
        self._tile_y = y
        self.pixel_x = x * TILE_SIZE + TILE_SIZE // 2
        self.pixel_y = y * TILE_SIZE + TILE_SIZE // 2

    def get_pixel_position(self) -> Tuple[float, float]:
        """Get pixel position."""
        return (self.pixel_x, self.pixel_y)

    def get_facing_tile(self) -> Tuple[int, int]:
        """Get the tile the player is facing."""
        tx, ty = self.get_tile_position()
        if self._facing == 'up':
            ty -= 1
        elif self._facing == 'down':
            ty += 1
        elif self._facing == 'left':
            tx -= 1
        elif self._facing == 'right':
            tx += 1
        return (tx, ty)

    # =========================================================================
    # INPUT HANDLING
    # =========================================================================

    def handle_input(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle keyboard input for movement.

        Args:
            keys: pygame key state
        """
        # Reset velocity
        self._velocity_x = 0.0
        self._velocity_y = 0.0

        # WASD or arrow keys for movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self._velocity_y = -1.0
            self._facing = 'up'
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self._velocity_y = 1.0
            self._facing = 'down'
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self._velocity_x = -1.0
            self._facing = 'left'
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self._velocity_x = 1.0
            self._facing = 'right'

        # Normalize diagonal movement
        if self._velocity_x != 0 and self._velocity_y != 0:
            length = math.sqrt(self._velocity_x ** 2 + self._velocity_y ** 2)
            self._velocity_x /= length
            self._velocity_y /= length

        self._moving = (self._velocity_x != 0 or self._velocity_y != 0)

    def is_interact_pressed(self, keys: pygame.key.ScancodeWrapper) -> bool:
        """Check if interact key is pressed (E or Space)."""
        return keys[pygame.K_e] or keys[pygame.K_SPACE]

    def is_ability_pressed(self, keys: pygame.key.ScancodeWrapper) -> Optional[int]:
        """
        Check if an ability key is pressed (1-9, 0 for ability 10).

        Returns:
            Ability index (0-9) or None
        """
        # Keys 1-9 map to abilities 0-8
        ability_keys = [
            pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0,
        ]
        for idx, key in enumerate(ability_keys):
            if keys[key]:
                return idx
        return None

    # =========================================================================
    # UPDATE
    # =========================================================================

    def update(self, dt: float, collision_check=None):
        """
        Update player state.

        Args:
            dt: Delta time in seconds
            collision_check: Function(tile_x, tile_y) -> bool for collision
        """
        # Update interaction cooldown
        if self._interact_cooldown > 0:
            self._interact_cooldown -= dt

        # Update movement
        if self._moving:
            speed = self.MOVE_SPEED * TILE_SIZE * dt
            new_x = self.pixel_x + self._velocity_x * speed
            new_y = self.pixel_y + self._velocity_y * speed

            # Collision detection
            if collision_check:
                # Check horizontal movement
                if self._velocity_x != 0:
                    test_tile_x = int(new_x // TILE_SIZE)
                    test_tile_y = int(self.pixel_y // TILE_SIZE)
                    if collision_check(test_tile_x, test_tile_y):
                        new_x = self.pixel_x  # Block horizontal

                # Check vertical movement
                if self._velocity_y != 0:
                    test_tile_x = int(self.pixel_x // TILE_SIZE)
                    test_tile_y = int(new_y // TILE_SIZE)
                    if collision_check(test_tile_x, test_tile_y):
                        new_y = self.pixel_y  # Block vertical

            # Apply movement
            self.pixel_x = new_x
            self.pixel_y = new_y

            # Clamp to zone bounds
            max_x = ZONE_WIDTH * TILE_SIZE - TILE_SIZE // 2
            max_y = ZONE_HEIGHT * TILE_SIZE - TILE_SIZE // 2
            self.pixel_x = max(TILE_SIZE // 2, min(max_x, self.pixel_x))
            self.pixel_y = max(TILE_SIZE // 2, min(max_y, self.pixel_y))

            # Update walk animation
            self._walk_timer += dt
            if self._walk_timer >= self.WALK_FRAME_DURATION:
                self._walk_timer = 0
                self._walk_frame = (self._walk_frame + 1) % 4
        else:
            # Reset walk animation
            self._walk_frame = 0
            self._walk_timer = 0

        # Update idle animation
        self._idle_timer += dt * self.IDLE_BOB_SPEED

    def try_interact(self) -> bool:
        """
        Try to interact.

        Returns:
            True if interaction is allowed (cooldown passed)
        """
        if self._interact_cooldown <= 0:
            self._interact_cooldown = 0.3  # 300ms cooldown
            return True
        return False

    # =========================================================================
    # DRAWING
    # =========================================================================

    def draw(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """
        Draw the player.

        Args:
            surface: Surface to draw on
            camera_x, camera_y: Camera offset
        """
        # Calculate screen position
        screen_x = int(self.pixel_x - camera_x)
        screen_y = int(self.pixel_y - camera_y)

        # Idle bob effect
        bob_offset = 0
        if not self._moving:
            bob_offset = int(math.sin(self._idle_timer) * 2)

        # Walk bob effect
        walk_bob = 0
        if self._moving:
            walk_bob = abs(int(math.sin(self._walk_frame * math.pi / 2) * 2))

        y_offset = screen_y - self.height // 2 + bob_offset - walk_bob
        x_offset = screen_x - self.width // 2

        # Draw shadow
        shadow_rect = pygame.Rect(
            x_offset + 4,
            screen_y + self.height // 2 - 4,
            self.width - 8,
            6
        )
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 50), shadow_surface.get_rect())
        surface.blit(shadow_surface, shadow_rect)

        # Draw body based on facing direction
        self._draw_character(surface, x_offset, y_offset)

    def _draw_character(self, surface: pygame.Surface, x: int, y: int):
        """Draw the player character sprite."""
        # Body (clothes)
        body_rect = pygame.Rect(x + 4, y + 10, 16, 18)
        pygame.draw.rect(surface, CHAR_CLOTHES, body_rect, border_radius=3)

        # Apron
        apron_rect = pygame.Rect(x + 6, y + 14, 12, 12)
        pygame.draw.rect(surface, CHAR_APRON, apron_rect, border_radius=2)

        # Head
        head_x = x + self.width // 2
        head_y = y + 8
        pygame.draw.circle(surface, CHAR_SKIN, (head_x, head_y), 8)

        # Hair
        hair_rect = pygame.Rect(head_x - 7, head_y - 8, 14, 7)
        pygame.draw.rect(surface, CHAR_HAIR_BROWN, hair_rect, border_radius=3)

        # Eyes based on facing
        eye_y = head_y
        if self._facing == 'down':
            pygame.draw.circle(surface, (40, 35, 35), (head_x - 3, eye_y), 2)
            pygame.draw.circle(surface, (40, 35, 35), (head_x + 3, eye_y), 2)
        elif self._facing == 'up':
            # Back of head - no eyes visible
            pass
        elif self._facing == 'left':
            pygame.draw.circle(surface, (40, 35, 35), (head_x - 4, eye_y), 2)
        elif self._facing == 'right':
            pygame.draw.circle(surface, (40, 35, 35), (head_x + 4, eye_y), 2)

        # Legs (simple animation)
        leg_y = y + 26
        leg_offset = 0
        if self._moving:
            leg_offset = int(math.sin(self._walk_frame * math.pi / 2) * 3)

        # Left leg
        pygame.draw.rect(surface, CHAR_CLOTHES,
                        (x + 6 - leg_offset, leg_y, 5, 6), border_radius=2)
        # Right leg
        pygame.draw.rect(surface, CHAR_CLOTHES,
                        (x + 13 + leg_offset, leg_y, 5, 6), border_radius=2)

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'tile_x': self._tile_x,
            'tile_y': self._tile_y,
            'pixel_x': self.pixel_x,
            'pixel_y': self.pixel_y,
            'facing': self._facing,
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._tile_x = state.get('tile_x', 0)
        self._tile_y = state.get('tile_y', 0)
        self.pixel_x = state.get('pixel_x', self._tile_x * TILE_SIZE + TILE_SIZE // 2)
        self.pixel_y = state.get('pixel_y', self._tile_y * TILE_SIZE + TILE_SIZE // 2)
        self._facing = state.get('facing', 'down')
