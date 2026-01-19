"""
World/Zone System for Dragon Haven Cafe.
Manages exploration zones, navigation, weather, and tile maps.
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from constants import (
    ZONE_CAFE_GROUNDS, ZONE_MEADOW_FIELDS, ZONE_FOREST_DEPTHS,
    ZONE_COASTAL_SHORE, ZONE_MOUNTAIN_PASS, ZONE_ANCIENT_RUINS,
    ZONE_SKY_ISLANDS,
    ALL_ZONES, ZONE_UNLOCK_REQUIREMENTS, ZONE_CONNECTIONS,
    ZONE_WIDTH, ZONE_HEIGHT, TILE_SIZE,
    WEATHER_SUNNY, WEATHER_CLOUDY, WEATHER_RAINY, WEATHER_STORMY, WEATHER_SPECIAL,
    ALL_WEATHER, WEATHER_PROBABILITIES, WEATHER_RESOURCE_MULTIPLIER,
    WEATHER_CLOSES_CAFE, WEATHER_DANGER_LEVEL,
    SPECIAL_WEATHER_EVENTS, SPECIAL_WEATHER_DESCRIPTIONS,
    DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
    DRAGON_STAGE_ADOLESCENT, DRAGON_STAGE_ADULT
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
    # Coastal tiles
    SAND = 'sand'
    SHALLOW_WATER = 'shallow_water'
    SEAWEED = 'seaweed'
    TIDAL_POOL = 'tidal_pool'
    # Mountain tiles
    ROCK = 'rock'
    SNOW = 'snow'
    ALPINE_FLOWER = 'alpine_flower'
    HOT_SPRING = 'hot_spring'
    # Ancient Ruins tiles
    RUIN_FLOOR = 'ruin_floor'
    RUIN_WALL = 'ruin_wall'
    CRYSTAL_CLUSTER = 'crystal_cluster'
    OVERGROWN = 'overgrown'
    ANCIENT_PATH = 'ancient_path'
    # Sky Islands tiles
    CLOUD = 'cloud'
    SKY_CRYSTAL = 'sky_crystal'
    FLOATING_GRASS = 'floating_grass'
    STARLIGHT_POOL = 'starlight_pool'
    WIND_STREAM = 'wind_stream'
    VOID = 'void'

    # Walkable tiles
    WALKABLE = {GRASS, DIRT, FLOWER, SAND, SHALLOW_WATER, SEAWEED, TIDAL_POOL, ROCK, SNOW, ALPINE_FLOWER, HOT_SPRING, RUIN_FLOOR, OVERGROWN, ANCIENT_PATH, CLOUD, FLOATING_GRASS, STARLIGHT_POOL, WIND_STREAM}
    BLOCKING = {WATER, STONE, TREE, BUSH, BUILDING, RUIN_WALL, CRYSTAL_CLUSTER, SKY_CRYSTAL, VOID}


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

        # Special weather event tracking
        self._special_weather_event: Optional[str] = None
        self._pending_weather: Optional[str] = None  # For storm warnings
        self._hours_until_weather_change: int = 0

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

        # Coastal Shore - requires juvenile (same as forest)
        coastal = Zone(
            id=ZONE_COASTAL_SHORE,
            name="Coastal Shore",
            description="A sandy beach with tidal pools and ocean breezes.",
            unlock_requirement=ZONE_UNLOCK_REQUIREMENTS[ZONE_COASTAL_SHORE],
            connections=ZONE_CONNECTIONS[ZONE_COASTAL_SHORE]
        )
        coastal.resource_points = [
            ResourcePoint('cs_salt_1', 'Salt Flats', 4, 6, 'salt', 4),
            ResourcePoint('cs_seaweed_1', 'Seaweed Bed', 8, 10, 'seaweed', 5),
            ResourcePoint('cs_crab_1', 'Crab Rocks', 6, 12, 'crab', 2),
            ResourcePoint('cs_oyster_1', 'Pearl Beds', 16, 5, 'oyster', 2),
            ResourcePoint('cs_clam_1', 'Tidal Pool', 10, 4, 'clam', 3),
            ResourcePoint('cs_berry_1', 'Dune Shrubs', 3, 14, 'berry', 3),
        ]
        # Generate coastal-themed tile map
        coastal.tile_map = self._generate_coastal_map()
        self._zones[ZONE_COASTAL_SHORE] = coastal

        # Mountain Pass - requires adolescent
        mountain = Zone(
            id=ZONE_MOUNTAIN_PASS,
            name="Mountain Pass",
            description="A high mountain path with alpine flora and hot springs.",
            unlock_requirement=ZONE_UNLOCK_REQUIREMENTS[ZONE_MOUNTAIN_PASS],
            connections=ZONE_CONNECTIONS[ZONE_MOUNTAIN_PASS]
        )
        mountain.resource_points = [
            ResourcePoint('mp_herb_1', 'Alpine Meadow', 5, 5, 'herb', 4),
            ResourcePoint('mp_honey_1', 'Rock Hive', 10, 8, 'honey', 2),
            ResourcePoint('mp_crystal_1', 'Crystal Vein', 18, 10, 'crystal', 2),
            ResourcePoint('mp_flower_1', 'Alpine Garden', 7, 12, 'flower', 4),
            ResourcePoint('mp_moss_1', 'Mossy Rocks', 3, 9, 'moss', 3),
            ResourcePoint('mp_egg_1', 'Hot Springs', 12, 14, 'egg', 2),
        ]
        # Generate mountain-themed tile map
        mountain.tile_map = self._generate_mountain_map()
        self._zones[ZONE_MOUNTAIN_PASS] = mountain

        # Ancient Ruins - requires adolescent
        ruins = Zone(
            id=ZONE_ANCIENT_RUINS,
            name="Ancient Ruins",
            description="Mysterious ruins from a forgotten civilization, overgrown with magical flora.",
            unlock_requirement=ZONE_UNLOCK_REQUIREMENTS[ZONE_ANCIENT_RUINS],
            connections=ZONE_CONNECTIONS[ZONE_ANCIENT_RUINS]
        )
        ruins.resource_points = [
            ResourcePoint('ar_spice_1', 'Sealed Storage', 5, 5, 'spice', 3),
            ResourcePoint('ar_moss_1', 'Overgrown Wall', 8, 8, 'moss', 4),
            ResourcePoint('ar_crystal_1', 'Crystal Garden', 10, 6, 'crystal', 2),
            ResourcePoint('ar_herb_1', 'Dragon Shrine', 4, 12, 'herb', 3),
            ResourcePoint('ar_grain_1', 'Ancient Granary', 12, 10, 'grain', 3),
            ResourcePoint('ar_mushroom_1', 'Glowing Cellar', 6, 14, 'mushroom', 2),
            ResourcePoint('ar_honey_1', 'Amber Chamber', 15, 5, 'honey', 2),
        ]
        # Generate ruins-themed tile map
        ruins.tile_map = self._generate_ruins_map()
        self._zones[ZONE_ANCIENT_RUINS] = ruins

        # Sky Islands - requires adult (flight capability)
        sky = Zone(
            id=ZONE_SKY_ISLANDS,
            name="Sky Islands",
            description="Floating islands among the clouds, home to legendary ingredients and celestial wonders.",
            unlock_requirement=ZONE_UNLOCK_REQUIREMENTS[ZONE_SKY_ISLANDS],
            connections=ZONE_CONNECTIONS[ZONE_SKY_ISLANDS]
        )
        sky.resource_points = [
            ResourcePoint('si_cloud_1', 'Cloud Bank', 5, 5, 'cloud', 3),
            ResourcePoint('si_crystal_1', 'Crystal Spire', 10, 4, 'crystal', 2),
            ResourcePoint('si_berry_1', 'Star Garden', 4, 10, 'berry', 3),
            ResourcePoint('si_flower_1', 'Wind Terrace', 12, 8, 'flower', 3),
            ResourcePoint('si_nectar_1', 'Starlight Pool', 8, 12, 'nectar', 2),
            ResourcePoint('si_tear_1', 'Dragon Shrine', 6, 6, 'tear', 1),
            ResourcePoint('si_feather_1', 'Phoenix Nest', 14, 6, 'feather', 1),
            ResourcePoint('si_honey_1', 'Sky Hive', 3, 14, 'honey', 2),
        ]
        # Generate sky-themed tile map
        sky.tile_map = self._generate_sky_map()
        self._zones[ZONE_SKY_ISLANDS] = sky

    def _generate_coastal_map(self) -> List[List[str]]:
        """Generate a coastal-themed tile map."""
        tiles = []
        for y in range(ZONE_HEIGHT):
            row = []
            for x in range(ZONE_WIDTH):
                # Ocean on the right side
                if x >= ZONE_WIDTH - 3:
                    tile = TileType.WATER
                elif x >= ZONE_WIDTH - 5:
                    # Shallow water / tidal zone
                    r = random.random()
                    if r < 0.4:
                        tile = TileType.SHALLOW_WATER
                    elif r < 0.6:
                        tile = TileType.TIDAL_POOL
                    elif r < 0.8:
                        tile = TileType.SEAWEED
                    else:
                        tile = TileType.SAND
                elif x == 0 or y == 0 or y == ZONE_HEIGHT - 1:
                    # Left/top/bottom border
                    tile = random.choice([TileType.BUSH, TileType.STONE, TileType.TREE])
                else:
                    # Sandy beach area
                    r = random.random()
                    if r < 0.7:
                        tile = TileType.SAND
                    elif r < 0.85:
                        tile = TileType.GRASS
                    elif r < 0.92:
                        tile = TileType.BUSH
                    else:
                        tile = TileType.STONE
                row.append(tile)
            tiles.append(row)
        return tiles

    def _generate_mountain_map(self) -> List[List[str]]:
        """Generate a mountain-themed tile map."""
        tiles = []
        for y in range(ZONE_HEIGHT):
            row = []
            for x in range(ZONE_WIDTH):
                # Border is rocky
                if x == 0 or x == ZONE_WIDTH - 1 or y == 0 or y == ZONE_HEIGHT - 1:
                    tile = TileType.STONE
                else:
                    # Mountain terrain
                    r = random.random()
                    if r < 0.4:
                        tile = TileType.ROCK
                    elif r < 0.6:
                        tile = TileType.DIRT
                    elif r < 0.7:
                        tile = TileType.GRASS
                    elif r < 0.8:
                        tile = TileType.ALPINE_FLOWER
                    elif r < 0.85:
                        tile = TileType.SNOW
                    elif r < 0.9:
                        tile = TileType.HOT_SPRING
                    else:
                        tile = TileType.STONE
                row.append(tile)
            tiles.append(row)
        return tiles

    def _generate_ruins_map(self) -> List[List[str]]:
        """Generate an ancient ruins-themed tile map."""
        tiles = []
        for y in range(ZONE_HEIGHT):
            row = []
            for x in range(ZONE_WIDTH):
                # Border is ruined walls
                if x == 0 or x == ZONE_WIDTH - 1 or y == 0 or y == ZONE_HEIGHT - 1:
                    tile = TileType.RUIN_WALL
                else:
                    # Ancient ruins terrain
                    r = random.random()
                    if r < 0.35:
                        tile = TileType.RUIN_FLOOR
                    elif r < 0.50:
                        tile = TileType.OVERGROWN
                    elif r < 0.60:
                        tile = TileType.ANCIENT_PATH
                    elif r < 0.70:
                        tile = TileType.GRASS
                    elif r < 0.80:
                        tile = TileType.DIRT
                    elif r < 0.88:
                        tile = TileType.RUIN_WALL
                    elif r < 0.94:
                        tile = TileType.CRYSTAL_CLUSTER
                    else:
                        tile = TileType.STONE
                row.append(tile)
            tiles.append(row)
        return tiles

    def _generate_sky_map(self) -> List[List[str]]:
        """Generate a sky islands-themed tile map with floating platforms."""
        tiles = []
        for y in range(ZONE_HEIGHT):
            row = []
            for x in range(ZONE_WIDTH):
                # Create floating island pattern - void around edges and between islands
                # Main island cluster in center-left
                in_main_island = (3 <= x <= 8 and 3 <= y <= 10)
                # Secondary island cluster top-right
                in_secondary_island = (10 <= x <= 14 and 2 <= y <= 7)
                # Third island cluster bottom-right
                in_third_island = (11 <= x <= 15 and 10 <= y <= 14)
                # Bridge connections (wind streams)
                on_bridge = ((y == 5 and 8 <= x <= 10) or
                            (x == 11 and 7 <= y <= 10))

                if on_bridge:
                    tile = TileType.WIND_STREAM
                elif in_main_island or in_secondary_island or in_third_island:
                    # Island interior terrain
                    r = random.random()
                    if r < 0.35:
                        tile = TileType.CLOUD
                    elif r < 0.55:
                        tile = TileType.FLOATING_GRASS
                    elif r < 0.70:
                        tile = TileType.STARLIGHT_POOL
                    elif r < 0.80:
                        tile = TileType.WIND_STREAM
                    elif r < 0.90:
                        tile = TileType.SKY_CRYSTAL
                    else:
                        tile = TileType.CLOUD
                else:
                    # Void between islands (impassable)
                    tile = TileType.VOID
                row.append(tile)
            tiles.append(row)
        return tiles

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
        stage_order = [DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE, DRAGON_STAGE_ADOLESCENT, DRAGON_STAGE_ADULT]
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

    def roll_new_weather(self, season: str, with_warning: bool = False) -> Optional[str]:
        """
        Roll for new weather based on season probabilities.

        Args:
            season: Current season
            with_warning: If True, schedule storm with warning instead of immediate change

        Returns:
            The new weather type, or None if scheduled for later
        """
        probs = WEATHER_PROBABILITIES.get(season, WEATHER_PROBABILITIES['spring'])
        roll = random.random()
        cumulative = 0.0

        new_weather = WEATHER_SUNNY  # Default fallback

        for weather_type, prob in probs.items():
            cumulative += prob
            if roll < cumulative:
                new_weather = weather_type
                break

        # If rolling stormy weather and warnings enabled, schedule it
        if with_warning and new_weather == WEATHER_STORMY:
            self.schedule_weather_change(new_weather, 1, season)  # 1 hour warning
            return None

        # If special weather, pick a random event for the season
        if new_weather == WEATHER_SPECIAL:
            events = SPECIAL_WEATHER_EVENTS.get(season, ['rainbow'])
            self._special_weather_event = random.choice(events)
        else:
            self._special_weather_event = None

        self._weather = new_weather
        self._days_since_weather_change = 0
        return new_weather

    def get_resource_multiplier(self) -> float:
        """Get resource spawn multiplier based on weather."""
        return WEATHER_RESOURCE_MULTIPLIER.get(self._weather, 1.0)

    def is_cafe_closed_by_weather(self) -> bool:
        """Check if cafe should be closed due to weather."""
        return WEATHER_CLOSES_CAFE.get(self._weather, False)

    def get_weather_danger_level(self) -> int:
        """Get the danger level of current weather (0 = safe, 2 = dangerous)."""
        return WEATHER_DANGER_LEVEL.get(self._weather, 0)

    def is_stormy(self) -> bool:
        """Check if current weather is stormy."""
        return self._weather == WEATHER_STORMY

    def is_special_weather(self) -> bool:
        """Check if current weather is special."""
        return self._weather == WEATHER_SPECIAL

    def get_special_weather_event(self) -> Optional[str]:
        """Get the current special weather event name."""
        return self._special_weather_event

    def get_special_weather_description(self) -> Optional[str]:
        """Get the description for the current special weather event."""
        if self._special_weather_event:
            return SPECIAL_WEATHER_DESCRIPTIONS.get(self._special_weather_event)
        return None

    def get_pending_storm_warning(self) -> Optional[Tuple[str, int]]:
        """
        Get pending storm warning info.

        Returns:
            Tuple of (weather_type, hours_until) or None if no pending storm
        """
        if self._pending_weather == WEATHER_STORMY and self._hours_until_weather_change > 0:
            return (self._pending_weather, self._hours_until_weather_change)
        return None

    def schedule_weather_change(self, weather: str, hours: int, season: str):
        """
        Schedule a weather change (for storm warnings).

        Args:
            weather: The weather type to change to
            hours: Hours until the change
            season: Current season (for special event selection)
        """
        self._pending_weather = weather
        self._hours_until_weather_change = hours

        # If special weather, pick a random event for the season
        if weather == WEATHER_SPECIAL:
            events = SPECIAL_WEATHER_EVENTS.get(season, ['rainbow'])
            self._special_weather_event = random.choice(events)

    def apply_pending_weather(self):
        """Apply the pending weather change."""
        if self._pending_weather:
            self._weather = self._pending_weather
            self._days_since_weather_change = 0
            self._pending_weather = None
            self._hours_until_weather_change = 0

    def tick_weather_countdown(self):
        """Tick down the weather change countdown (called hourly)."""
        if self._hours_until_weather_change > 0:
            self._hours_until_weather_change -= 1
            if self._hours_until_weather_change <= 0:
                self.apply_pending_weather()

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

        # Roll for new weather (33% chance per day, with storm warnings)
        if random.random() < 0.33:
            self.roll_new_weather(season, with_warning=True)

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
            'special_weather_event': self._special_weather_event,
            'pending_weather': self._pending_weather,
            'hours_until_weather_change': self._hours_until_weather_change,
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
        self._special_weather_event = state.get('special_weather_event', None)
        self._pending_weather = state.get('pending_weather', None)
        self._hours_until_weather_change = state.get('hours_until_weather_change', 0)
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
