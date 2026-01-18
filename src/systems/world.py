"""
World/Zone System for Dragon Haven Cafe.
Manages exploration zones, navigation, weather, and tile maps.
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from constants import (
    ZONE_CAFE_GROUNDS, ZONE_MEADOW_FIELDS, ZONE_FOREST_DEPTHS,
    ALL_ZONES, ZONE_UNLOCK_REQUIREMENTS, ZONE_CONNECTIONS,
    ZONE_WIDTH, ZONE_HEIGHT, TILE_SIZE,
    WEATHER_SUNNY, WEATHER_CLOUDY, WEATHER_RAINY,
    ALL_WEATHER, WEATHER_PROBABILITIES, WEATHER_RESOURCE_MULTIPLIER,
    DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE
)


# =============================================================================
# TILE TYPES
# =============================================================================

class TileType:
    """Tile type constants."""
    GRASS = 'grass'
    DIRT = 'dirt'
    WATER = 'water'
    STONE = 'stone'
    TREE = 'tree'
    BUSH = 'bush'
    FLOWER = 'flower'
    BUILDING = 'building'

    # Walkable tiles
    WALKABLE = {GRASS, DIRT, FLOWER}
    BLOCKING = {WATER, STONE, TREE, BUSH, BUILDING}


@dataclass
class ResourcePoint:
    """A resource gathering point in a zone."""
    id: str
    name: str
    x: int  # Tile x
    y: int  # Tile y
    resource_type: str  # e.g., 'berry', 'herb', 'mushroom'
    max_quantity: int = 3
    current_quantity: int = 3
    respawn_days: int = 1

    def harvest(self, amount: int = 1) -> int:
        """Harvest from this point. Returns actual amount harvested."""
        actual = min(amount, self.current_quantity)
        self.current_quantity -= actual
        return actual

    def is_depleted(self) -> bool:
        return self.current_quantity <= 0

    def respawn(self):
        """Respawn resources."""
        self.current_quantity = self.max_quantity

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'resource_type': self.resource_type,
            'max_quantity': self.max_quantity,
            'current_quantity': self.current_quantity,
            'respawn_days': self.respawn_days
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResourcePoint':
        return cls(**data)


@dataclass
class Zone:
    """
    Represents an explorable zone in the game world.
    """
    id: str
    name: str
    description: str = ""
    unlock_requirement: Optional[str] = None  # Dragon stage required
    connections: List[str] = field(default_factory=list)
    resource_points: List[ResourcePoint] = field(default_factory=list)
    tile_map: List[List[str]] = field(default_factory=list)
    width: int = ZONE_WIDTH
    height: int = ZONE_HEIGHT

    def __post_init__(self):
        """Initialize tile map if not provided."""
        if not self.tile_map:
            self.tile_map = self._generate_default_map()

    def _generate_default_map(self) -> List[List[str]]:
        """Generate a default tile map."""
        # Simple procedural generation based on zone type
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Border is mostly blocking
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    tile = random.choice([TileType.TREE, TileType.STONE, TileType.BUSH])
                else:
                    # Interior is mostly walkable with some obstacles
                    r = random.random()
                    if r < 0.7:
                        tile = TileType.GRASS
                    elif r < 0.8:
                        tile = TileType.DIRT
                    elif r < 0.85:
                        tile = TileType.FLOWER
                    elif r < 0.9:
                        tile = TileType.TREE
                    elif r < 0.95:
                        tile = TileType.BUSH
                    else:
                        tile = TileType.STONE
                row.append(tile)
            tiles.append(row)
        return tiles

    def get_tile(self, x: int, y: int) -> Optional[str]:
        """Get tile type at position."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tile_map[y][x]
        return None

    def is_walkable(self, x: int, y: int) -> bool:
        """Check if a tile is walkable."""
        tile = self.get_tile(x, y)
        return tile in TileType.WALKABLE if tile else False

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_resource_at(self, x: int, y: int) -> Optional[ResourcePoint]:
        """Get resource point at position."""
        for rp in self.resource_points:
            if rp.x == x and rp.y == y:
                return rp
        return None

    def respawn_resources(self):
        """Respawn all depleted resources."""
        for rp in self.resource_points:
            if rp.is_depleted():
                rp.respawn()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'unlock_requirement': self.unlock_requirement,
            'connections': self.connections,
            'resource_points': [rp.to_dict() for rp in self.resource_points],
            'tile_map': self.tile_map,
            'width': self.width,
            'height': self.height
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Zone':
        rp_list = [ResourcePoint.from_dict(rp) for rp in data.get('resource_points', [])]
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            unlock_requirement=data.get('unlock_requirement'),
            connections=data.get('connections', []),
            resource_points=rp_list,
            tile_map=data.get('tile_map', []),
            width=data.get('width', ZONE_WIDTH),
            height=data.get('height', ZONE_HEIGHT)
        )


class WorldManager:
    """
    Manages the game world, zones, weather, and exploration.

    Usage:
        world = get_world_manager()
        world.initialize()
        world.set_zone('meadow_fields', dragon)
    """

    def __init__(self):
        """Initialize the world manager."""
        self._zones: Dict[str, Zone] = {}
        self._current_zone_id: str = ZONE_CAFE_GROUNDS
        self._weather: str = WEATHER_SUNNY
        self._days_since_weather_change: int = 0
        self._unlocked_zones: Set[str] = {ZONE_CAFE_GROUNDS}
        self._discovered_resource_points: Set[str] = set()

        # Player position in current zone
        self._player_x: int = ZONE_WIDTH // 2
        self._player_y: int = ZONE_HEIGHT // 2

        self._initialized = False

    def initialize(self):
        """Initialize all zones."""
        if self._initialized:
            return

        self._create_zones()
        self._initialized = True

    def _create_zones(self):
        """Create all game zones."""
        # Cafe Grounds - always unlocked, home base
        cafe_grounds = Zone(
            id=ZONE_CAFE_GROUNDS,
            name="Cafe Grounds",
            description="The familiar grounds around Dragon Haven Cafe.",
            unlock_requirement=None,
            connections=ZONE_CONNECTIONS[ZONE_CAFE_GROUNDS]
        )
        # Add some basic resource points
        cafe_grounds.resource_points = [
            ResourcePoint('cg_herb_1', 'Garden Herbs', 5, 5, 'herb', 3),
            ResourcePoint('cg_berry_1', 'Berry Bush', 8, 10, 'berry', 2),
            ResourcePoint('cg_flower_1', 'Flower Patch', 15, 7, 'flower', 4),
        ]
        self._zones[ZONE_CAFE_GROUNDS] = cafe_grounds

        # Meadow Fields - requires hatchling
        meadow = Zone(
            id=ZONE_MEADOW_FIELDS,
            name="Meadow Fields",
            description="Open fields with wildflowers and gentle streams.",
            unlock_requirement=ZONE_UNLOCK_REQUIREMENTS[ZONE_MEADOW_FIELDS],
            connections=ZONE_CONNECTIONS[ZONE_MEADOW_FIELDS]
        )
        meadow.resource_points = [
            ResourcePoint('mf_berry_1', 'Wild Berries', 4, 8, 'berry', 5),
            ResourcePoint('mf_honey_1', 'Bee Hive', 12, 3, 'honey', 2),
            ResourcePoint('mf_herb_1', 'Herb Meadow', 16, 12, 'herb', 4),
            ResourcePoint('mf_mushroom_1', 'Mushroom Circle', 7, 14, 'mushroom', 3),
        ]
        self._zones[ZONE_MEADOW_FIELDS] = meadow

        # Forest Depths - requires juvenile
        forest = Zone(
            id=ZONE_FOREST_DEPTHS,
            name="Forest Depths",
            description="A dense forest with rare ingredients and hidden secrets.",
            unlock_requirement=ZONE_UNLOCK_REQUIREMENTS[ZONE_FOREST_DEPTHS],
            connections=ZONE_CONNECTIONS[ZONE_FOREST_DEPTHS]
        )
        forest.resource_points = [
            ResourcePoint('fd_mushroom_1', 'Rare Mushrooms', 6, 6, 'mushroom', 4),
            ResourcePoint('fd_herb_1', 'Forest Herbs', 14, 4, 'herb', 5),
            ResourcePoint('fd_meat_1', 'Hunting Grounds', 10, 11, 'meat', 2),
            ResourcePoint('fd_special_1', 'Crystal Cave', 18, 13, 'crystal', 1),
        ]
        self._zones[ZONE_FOREST_DEPTHS] = forest

    # =========================================================================
    # ZONE MANAGEMENT
    # =========================================================================

    def get_zone(self, zone_id: str) -> Optional[Zone]:
        """Get a zone by ID."""
        return self._zones.get(zone_id)

    def get_current_zone(self) -> Optional[Zone]:
        """Get the current zone."""
        return self._zones.get(self._current_zone_id)

    def get_current_zone_id(self) -> str:
        """Get the current zone ID."""
        return self._current_zone_id

    def can_enter_zone(self, zone_id: str, dragon_stage: str) -> bool:
        """Check if a zone can be entered based on dragon stage."""
        if zone_id not in self._zones:
            return False

        zone = self._zones[zone_id]
        if zone.unlock_requirement is None:
            return True

        # Check dragon stage progression
        stage_order = [DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE]
        required_idx = stage_order.index(zone.unlock_requirement) if zone.unlock_requirement in stage_order else -1
        current_idx = stage_order.index(dragon_stage) if dragon_stage in stage_order else -1

        return current_idx >= required_idx

    def set_zone(self, zone_id: str, dragon_stage: str = None) -> bool:
        """
        Move to a different zone.

        Args:
            zone_id: Zone to move to
            dragon_stage: Current dragon stage (for unlock check)

        Returns:
            True if zone change successful
        """
        if dragon_stage and not self.can_enter_zone(zone_id, dragon_stage):
            return False

        if zone_id not in self._zones:
            return False

        # Check if connected to current zone (or first time setup)
        current_zone = self.get_current_zone()
        if current_zone and zone_id not in current_zone.connections:
            return False

        self._current_zone_id = zone_id
        self._unlocked_zones.add(zone_id)

        # Reset player position to center
        self._player_x = ZONE_WIDTH // 2
        self._player_y = ZONE_HEIGHT // 2

        return True

    def get_unlocked_zones(self) -> List[str]:
        """Get list of unlocked zone IDs."""
        return list(self._unlocked_zones)

    def get_connected_zones(self) -> List[str]:
        """Get zones connected to current zone."""
        zone = self.get_current_zone()
        return zone.connections if zone else []

    # =========================================================================
    # PLAYER MOVEMENT
    # =========================================================================

    def get_player_position(self) -> Tuple[int, int]:
        """Get player tile position."""
        return (self._player_x, self._player_y)

    def set_player_position(self, x: int, y: int) -> bool:
        """
        Set player position if valid.

        Returns:
            True if position is valid and set
        """
        zone = self.get_current_zone()
        if zone and zone.is_walkable(x, y):
            self._player_x = x
            self._player_y = y
            return True
        return False

    def move_player(self, dx: int, dy: int) -> bool:
        """
        Move player by delta.

        Returns:
            True if movement successful
        """
        new_x = self._player_x + dx
        new_y = self._player_y + dy
        return self.set_player_position(new_x, new_y)

    def check_collision(self, x: int, y: int) -> bool:
        """Check if position has collision."""
        zone = self.get_current_zone()
        if not zone:
            return True  # Collide with nothing
        return not zone.is_walkable(x, y)

    # =========================================================================
    # WEATHER
    # =========================================================================

    def get_weather(self) -> str:
        """Get current weather."""
        return self._weather

    def roll_new_weather(self, season: str):
        """
        Roll for new weather based on season probabilities.

        Args:
            season: Current season ('spring' or 'summer')
        """
        probs = WEATHER_PROBABILITIES.get(season, WEATHER_PROBABILITIES['spring'])
        roll = random.random()
        cumulative = 0.0

        for weather_type, prob in probs.items():
            cumulative += prob
            if roll < cumulative:
                self._weather = weather_type
                self._days_since_weather_change = 0
                return

        # Fallback
        self._weather = WEATHER_SUNNY

    def get_resource_multiplier(self) -> float:
        """Get resource spawn multiplier based on weather."""
        return WEATHER_RESOURCE_MULTIPLIER.get(self._weather, 1.0)

    # =========================================================================
    # RESOURCES
    # =========================================================================

    def get_resource_at_player(self) -> Optional[ResourcePoint]:
        """Get resource point at player's current position."""
        zone = self.get_current_zone()
        if zone:
            return zone.get_resource_at(self._player_x, self._player_y)
        return None

    def harvest_resource(self, resource_id: str) -> int:
        """
        Harvest from a resource point.

        Returns:
            Amount harvested
        """
        zone = self.get_current_zone()
        if not zone:
            return 0

        for rp in zone.resource_points:
            if rp.id == resource_id:
                return rp.harvest(1)
        return 0

    def advance_day(self, season: str):
        """Called at the start of a new day."""
        self._days_since_weather_change += 1

        # Roll for new weather (33% chance per day)
        if random.random() < 0.33:
            self.roll_new_weather(season)

        # Respawn resources in all zones
        for zone in self._zones.values():
            zone.respawn_resources()

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'current_zone_id': self._current_zone_id,
            'weather': self._weather,
            'days_since_weather_change': self._days_since_weather_change,
            'unlocked_zones': list(self._unlocked_zones),
            'discovered_resource_points': list(self._discovered_resource_points),
            'player_x': self._player_x,
            'player_y': self._player_y,
            # Save resource point states
            'zone_resource_states': {
                zone_id: [rp.to_dict() for rp in zone.resource_points]
                for zone_id, zone in self._zones.items()
            }
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._current_zone_id = state.get('current_zone_id', ZONE_CAFE_GROUNDS)
        self._weather = state.get('weather', WEATHER_SUNNY)
        self._days_since_weather_change = state.get('days_since_weather_change', 0)
        self._unlocked_zones = set(state.get('unlocked_zones', [ZONE_CAFE_GROUNDS]))
        self._discovered_resource_points = set(state.get('discovered_resource_points', []))
        self._player_x = state.get('player_x', ZONE_WIDTH // 2)
        self._player_y = state.get('player_y', ZONE_HEIGHT // 2)

        # Restore resource point states
        zone_states = state.get('zone_resource_states', {})
        for zone_id, rp_list in zone_states.items():
            if zone_id in self._zones:
                self._zones[zone_id].resource_points = [
                    ResourcePoint.from_dict(rp) for rp in rp_list
                ]


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_world_manager = None


def get_world_manager() -> WorldManager:
    """Get the global world manager instance."""
    global _world_manager
    if _world_manager is None:
        _world_manager = WorldManager()
    return _world_manager


def reset_world_manager():
    """Reset the world manager (for new game)."""
    global _world_manager
    _world_manager = WorldManager()
