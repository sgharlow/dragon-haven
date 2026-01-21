"""
Creature Entity for Dragon Haven Cafe.
Wildlife creatures that inhabit exploration zones and interact with dragon abilities.
"""

import random
import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from constants import (
    TILE_SIZE,
    CREATURE_BEHAVIOR_PATROL, CREATURE_BEHAVIOR_FLEE,
    CREATURE_BEHAVIOR_GUARD, CREATURE_BEHAVIOR_FOLLOW,
    CREATURE_BEHAVIOR_STATIONARY,
    CREATURE_DATA, CREATURE_SPAWN_POINTS,
    CREATURE_FEED_BOND_BONUS, CREATURE_SCARE_STAMINA_COST,
    CREATURE_RESPAWN_HOURS,
    ALL_CREATURE_TYPES,
)


@dataclass
class Creature:
    """
    A wildlife creature in the exploration world.

    Creatures have different behaviors and can interact with dragon abilities.

    Usage:
        creature = Creature('forest_sprite', 10, 8, 'forest_01')
        creature.update(dt, player_pos, dragon_nearby)
        creature.draw(surface, camera_offset)
    """
    creature_type: str
    tile_x: int
    tile_y: int
    zone_id: str
    id: str = field(default_factory=lambda: f"creature_{random.randint(1000, 9999)}")

    # Runtime state (not serialized directly)
    pixel_x: float = field(init=False, default=0.0)
    pixel_y: float = field(init=False, default=0.0)
    _state: str = field(init=False, default='idle')
    _scared: bool = field(init=False, default=False)
    _scared_timer: float = field(init=False, default=0.0)
    _patrol_target: Optional[Tuple[int, int]] = field(init=False, default=None)
    _animation_timer: float = field(init=False, default=0.0)
    _facing: str = field(init=False, default='down')

    def __post_init__(self):
        """Initialize runtime state."""
        self.pixel_x = self.tile_x * TILE_SIZE + TILE_SIZE // 2
        self.pixel_y = self.tile_y * TILE_SIZE + TILE_SIZE // 2
        self._home_x = self.tile_x
        self._home_y = self.tile_y

    @property
    def data(self) -> Dict[str, Any]:
        """Get creature type data from constants."""
        return CREATURE_DATA.get(self.creature_type, {})

    @property
    def name(self) -> str:
        return self.data.get('name', 'Unknown Creature')

    @property
    def behavior(self) -> str:
        return self.data.get('behavior', CREATURE_BEHAVIOR_STATIONARY)

    @property
    def hostile(self) -> bool:
        return self.data.get('hostile', False)

    @property
    def speed(self) -> float:
        return self.data.get('speed', 1.0)

    @property
    def color(self) -> Tuple[int, int, int]:
        return self.data.get('color', (128, 128, 128))

    @property
    def dragon_ability(self) -> Optional[str]:
        return self.data.get('dragon_ability')

    @property
    def drops(self) -> List[str]:
        return self.data.get('drops', [])

    @property
    def is_scared(self) -> bool:
        return self._scared

    @property
    def is_active(self) -> bool:
        """Creature is active (not scared away)."""
        return not self._scared

    def get_tile_position(self) -> Tuple[int, int]:
        """Get current tile position."""
        return (
            int(self.pixel_x // TILE_SIZE),
            int(self.pixel_y // TILE_SIZE)
        )

    def get_pixel_position(self) -> Tuple[float, float]:
        """Get pixel position."""
        return (self.pixel_x, self.pixel_y)

    # =========================================================================
    # AI BEHAVIORS
    # =========================================================================

    def update(self, dt: float, player_pos: Tuple[float, float],
               dragon_nearby: bool = False) -> Optional[Dict[str, Any]]:
        """
        Update creature AI and movement.

        Args:
            dt: Delta time in seconds
            player_pos: Player's pixel position (x, y)
            dragon_nearby: Whether dragon is near this creature

        Returns:
            Optional event dict if something happened (e.g., dropped item)
        """
        # Handle scared state recovery
        if self._scared:
            self._scared_timer -= dt
            if self._scared_timer <= 0:
                self._scared = False
                self._reset_to_home()
            return None

        # Update animation
        self._animation_timer += dt

        # Behavior-specific updates
        if self.behavior == CREATURE_BEHAVIOR_PATROL:
            self._update_patrol(dt, player_pos)
        elif self.behavior == CREATURE_BEHAVIOR_FLEE:
            self._update_flee(dt, player_pos, dragon_nearby)
        elif self.behavior == CREATURE_BEHAVIOR_GUARD:
            self._update_guard(dt, player_pos)
        elif self.behavior == CREATURE_BEHAVIOR_FOLLOW:
            self._update_follow(dt, player_pos)
        # STATIONARY does nothing

        return None

    def _update_patrol(self, dt: float, player_pos: Tuple[float, float]):
        """Patrol behavior: wander around home area."""
        # Pick new patrol target if needed
        if self._patrol_target is None or self._reached_target():
            # Random nearby tile
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            self._patrol_target = (
                self._home_x + offset_x,
                self._home_y + offset_y
            )

        # Move toward target
        self._move_toward_target(dt, self._patrol_target)

    def _update_flee(self, dt: float, player_pos: Tuple[float, float],
                     dragon_nearby: bool):
        """Flee behavior: run from player/dragon."""
        dist = self._distance_to(player_pos)

        if dist < 100 or dragon_nearby:  # Within flee range
            self._state = 'fleeing'
            # Move away from player
            dx = self.pixel_x - player_pos[0]
            dy = self.pixel_y - player_pos[1]
            length = math.sqrt(dx * dx + dy * dy)
            if length > 0:
                dx /= length
                dy /= length
                self.pixel_x += dx * self.speed * TILE_SIZE * dt
                self.pixel_y += dy * self.speed * TILE_SIZE * dt
                self._update_facing(dx, dy)
        else:
            self._state = 'idle'
            # Return to home slowly
            self._move_toward_target(dt, (self._home_x, self._home_y), 0.5)

    def _update_guard(self, dt: float, player_pos: Tuple[float, float]):
        """Guard behavior: block access, face player."""
        dist = self._distance_to(player_pos)

        if dist < 80:  # Close to player
            self._state = 'alert'
            # Face the player
            dx = player_pos[0] - self.pixel_x
            dy = player_pos[1] - self.pixel_y
            self._update_facing(dx, dy)
        else:
            self._state = 'idle'

    def _update_follow(self, dt: float, player_pos: Tuple[float, float]):
        """Follow behavior: accompany player at a distance."""
        dist = self._distance_to(player_pos)

        if dist > 50:  # Follow if too far
            self._state = 'following'
            # Move toward player
            target_tile = (
                int(player_pos[0] // TILE_SIZE),
                int(player_pos[1] // TILE_SIZE)
            )
            self._move_toward_target(dt, target_tile)
        else:
            self._state = 'idle'

    def _move_toward_target(self, dt: float, target: Tuple[int, int],
                            speed_mult: float = 1.0):
        """Move toward a tile target."""
        target_px = target[0] * TILE_SIZE + TILE_SIZE // 2
        target_py = target[1] * TILE_SIZE + TILE_SIZE // 2

        dx = target_px - self.pixel_x
        dy = target_py - self.pixel_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 2:  # Not at target
            dx /= dist
            dy /= dist
            self.pixel_x += dx * self.speed * speed_mult * TILE_SIZE * dt
            self.pixel_y += dy * self.speed * speed_mult * TILE_SIZE * dt
            self._update_facing(dx, dy)

    def _reached_target(self) -> bool:
        """Check if reached patrol target."""
        if self._patrol_target is None:
            return True
        target_px = self._patrol_target[0] * TILE_SIZE + TILE_SIZE // 2
        target_py = self._patrol_target[1] * TILE_SIZE + TILE_SIZE // 2
        dist = math.sqrt(
            (self.pixel_x - target_px) ** 2 +
            (self.pixel_y - target_py) ** 2
        )
        return dist < TILE_SIZE // 2

    def _distance_to(self, pos: Tuple[float, float]) -> float:
        """Calculate distance to a position."""
        return math.sqrt(
            (self.pixel_x - pos[0]) ** 2 +
            (self.pixel_y - pos[1]) ** 2
        )

    def _update_facing(self, dx: float, dy: float):
        """Update facing direction based on movement."""
        if abs(dx) > abs(dy):
            self._facing = 'right' if dx > 0 else 'left'
        else:
            self._facing = 'down' if dy > 0 else 'up'

    def _reset_to_home(self):
        """Reset creature to home position."""
        self.tile_x = self._home_x
        self.tile_y = self._home_y
        self.pixel_x = self._home_x * TILE_SIZE + TILE_SIZE // 2
        self.pixel_y = self._home_y * TILE_SIZE + TILE_SIZE // 2
        self._state = 'idle'
        self._patrol_target = None

    # =========================================================================
    # INTERACTIONS
    # =========================================================================

    def scare(self, respawn_hours: float = CREATURE_RESPAWN_HOURS) -> Dict[str, Any]:
        """
        Scare this creature away (using dragon ability).

        Returns:
            Dict with 'success', 'drops' list, 'message'
        """
        if self._scared:
            return {'success': False, 'message': 'Creature already scared'}

        self._scared = True
        self._scared_timer = respawn_hours * 3600  # Convert to seconds (game time)

        # Drop items
        dropped = []
        if self.drops and random.random() < 0.5:  # 50% drop chance
            dropped.append(random.choice(self.drops))

        return {
            'success': True,
            'drops': dropped,
            'message': f'{self.name} was scared away!'
        }

    def interact(self, item_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Interact with this creature.

        Args:
            item_id: Optional item to give to creature (for feeding)

        Returns:
            Dict with interaction result
        """
        if self._scared:
            return {'success': False, 'message': 'Creature is not here'}

        if self.hostile:
            return {
                'success': False,
                'message': f'{self.name} is hostile! Use dragon ability to clear.',
                'hostile': True
            }

        # Friendly creature - can feed for bonuses
        if item_id:
            return {
                'success': True,
                'message': f'Fed {self.name}!',
                'bond_bonus': CREATURE_FEED_BOND_BONUS,
                'item_consumed': item_id
            }

        return {
            'success': True,
            'message': f'{self.name} chirps happily!',
        }

    def can_use_ability(self, ability: str) -> bool:
        """Check if a dragon ability affects this creature."""
        return self.dragon_ability == ability

    # =========================================================================
    # RENDERING
    # =========================================================================

    def draw(self, surface, camera_x: int, camera_y: int):
        """
        Draw the creature.

        Args:
            surface: Pygame surface to draw on
            camera_x, camera_y: Camera offset
        """
        import pygame

        if self._scared:
            return  # Don't draw scared creatures

        screen_x = int(self.pixel_x - camera_x)
        screen_y = int(self.pixel_y - camera_y)

        # Simple creature sprite based on type
        color = self.color
        size = 16

        # Body
        pygame.draw.ellipse(surface, color,
                           (screen_x - size // 2, screen_y - size // 2,
                            size, size * 0.8))

        # Eyes
        eye_offset = 3 if self._facing in ['down', 'left'] else -3
        pygame.draw.circle(surface, (255, 255, 255),
                          (screen_x - 3 + eye_offset, screen_y - 2), 3)
        pygame.draw.circle(surface, (255, 255, 255),
                          (screen_x + 3 + eye_offset, screen_y - 2), 3)
        pygame.draw.circle(surface, (40, 40, 40),
                          (screen_x - 3 + eye_offset, screen_y - 2), 1)
        pygame.draw.circle(surface, (40, 40, 40),
                          (screen_x + 3 + eye_offset, screen_y - 2), 1)

        # Hostile indicator
        if self.hostile and self._state == 'alert':
            pygame.draw.polygon(surface, (220, 60, 60), [
                (screen_x, screen_y - size),
                (screen_x - 4, screen_y - size - 8),
                (screen_x + 4, screen_y - size - 8),
            ])

        # Animation bob
        if self._state == 'fleeing':
            bob = int(math.sin(self._animation_timer * 10) * 2)
            # Redraw slightly bobbed
            pass

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def to_dict(self) -> Dict[str, Any]:
        """Serialize creature state."""
        return {
            'id': self.id,
            'creature_type': self.creature_type,
            'tile_x': self.tile_x,
            'tile_y': self.tile_y,
            'zone_id': self.zone_id,
            'scared': self._scared,
            'scared_timer': self._scared_timer,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Creature':
        """Deserialize creature state."""
        creature = cls(
            creature_type=data['creature_type'],
            tile_x=data['tile_x'],
            tile_y=data['tile_y'],
            zone_id=data['zone_id'],
            id=data['id']
        )
        creature._scared = data.get('scared', False)
        creature._scared_timer = data.get('scared_timer', 0.0)
        return creature


# =============================================================================
# CREATURE MANAGER SINGLETON
# =============================================================================

class CreatureManager:
    """
    Manages all creatures in the game world.

    Usage:
        manager = get_creature_manager()
        manager.spawn_zone_creatures('forest_depths')
        manager.update(dt, player_pos, dragon_pos)
        manager.draw(surface, camera_offset)
    """

    def __init__(self):
        """Initialize creature manager."""
        self._creatures: Dict[str, Creature] = {}
        self._creatures_by_zone: Dict[str, List[str]] = {}

    def spawn_zone_creatures(self, zone_id: str):
        """
        Spawn creatures for a zone based on spawn point data.

        Args:
            zone_id: Zone identifier
        """
        spawn_points = CREATURE_SPAWN_POINTS.get(zone_id, [])

        for creature_type, x, y in spawn_points:
            creature_id = f"{zone_id}_{creature_type}_{x}_{y}"

            # Don't respawn if already exists
            if creature_id in self._creatures:
                continue

            creature = Creature(
                creature_type=creature_type,
                tile_x=x,
                tile_y=y,
                zone_id=zone_id,
                id=creature_id
            )
            self._creatures[creature_id] = creature

            # Track by zone
            if zone_id not in self._creatures_by_zone:
                self._creatures_by_zone[zone_id] = []
            self._creatures_by_zone[zone_id].append(creature_id)

    def get_zone_creatures(self, zone_id: str) -> List[Creature]:
        """Get all creatures in a zone."""
        creature_ids = self._creatures_by_zone.get(zone_id, [])
        return [self._creatures[cid] for cid in creature_ids
                if cid in self._creatures]

    def get_active_zone_creatures(self, zone_id: str) -> List[Creature]:
        """Get active (not scared) creatures in a zone."""
        return [c for c in self.get_zone_creatures(zone_id) if c.is_active]

    def get_creature(self, creature_id: str) -> Optional[Creature]:
        """Get a specific creature by ID."""
        return self._creatures.get(creature_id)

    def get_creature_at_tile(self, zone_id: str, tile_x: int,
                             tile_y: int) -> Optional[Creature]:
        """Get creature at a specific tile."""
        for creature in self.get_active_zone_creatures(zone_id):
            cx, cy = creature.get_tile_position()
            if cx == tile_x and cy == tile_y:
                return creature
        return None

    def get_nearby_creature(self, zone_id: str, pixel_x: float,
                            pixel_y: float, radius: float = 50) -> Optional[Creature]:
        """Get nearest active creature within radius."""
        nearest = None
        nearest_dist = radius

        for creature in self.get_active_zone_creatures(zone_id):
            cx, cy = creature.get_pixel_position()
            dist = math.sqrt((cx - pixel_x) ** 2 + (cy - pixel_y) ** 2)
            if dist < nearest_dist:
                nearest = creature
                nearest_dist = dist

        return nearest

    def update(self, dt: float, zone_id: str, player_pos: Tuple[float, float],
               dragon_pos: Optional[Tuple[float, float]] = None):
        """
        Update all creatures in a zone.

        Args:
            dt: Delta time in seconds
            zone_id: Current zone
            player_pos: Player pixel position
            dragon_pos: Dragon pixel position (if present)
        """
        dragon_nearby = dragon_pos is not None

        for creature in self.get_zone_creatures(zone_id):
            creature.update(dt, player_pos, dragon_nearby)

    def use_ability_on_creatures(self, zone_id: str, ability: str,
                                 pixel_x: float, pixel_y: float,
                                 radius: float = 80) -> List[Dict[str, Any]]:
        """
        Use a dragon ability on nearby creatures.

        Args:
            zone_id: Current zone
            ability: Ability name (e.g., 'creature_scare')
            pixel_x, pixel_y: Center of ability effect
            radius: Effect radius

        Returns:
            List of result dicts from affected creatures
        """
        results = []

        for creature in self.get_active_zone_creatures(zone_id):
            if not creature.can_use_ability(ability):
                continue

            cx, cy = creature.get_pixel_position()
            dist = math.sqrt((cx - pixel_x) ** 2 + (cy - pixel_y) ** 2)

            if dist <= radius:
                result = creature.scare()
                result['creature_id'] = creature.id
                result['creature_name'] = creature.name
                results.append(result)

        return results

    def draw(self, surface, zone_id: str, camera_x: int, camera_y: int):
        """Draw all active creatures in a zone."""
        for creature in self.get_active_zone_creatures(zone_id):
            creature.draw(surface, camera_x, camera_y)

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_save_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'creatures': {
                cid: c.to_dict()
                for cid, c in self._creatures.items()
            }
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._creatures.clear()
        self._creatures_by_zone.clear()

        creatures_data = state.get('creatures', {})
        for cid, cdata in creatures_data.items():
            creature = Creature.from_dict(cdata)
            self._creatures[cid] = creature

            zone_id = creature.zone_id
            if zone_id not in self._creatures_by_zone:
                self._creatures_by_zone[zone_id] = []
            self._creatures_by_zone[zone_id].append(cid)

    def reset(self):
        """Reset all creature state."""
        self._creatures.clear()
        self._creatures_by_zone.clear()


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_creature_manager: Optional[CreatureManager] = None


def get_creature_manager() -> CreatureManager:
    """Get the global creature manager instance."""
    global _creature_manager
    if _creature_manager is None:
        _creature_manager = CreatureManager()
    return _creature_manager


def reset_creature_manager():
    """Reset the creature manager (for new game)."""
    global _creature_manager
    _creature_manager = CreatureManager()
