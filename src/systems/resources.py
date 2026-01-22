"""
Resource Spawning System for Dragon Haven Cafe.
Manages spawn points, respawn timers, quality variation, and gathering.
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set

from constants import (
    ZONE_CAFE_GROUNDS, ZONE_MEADOW_FIELDS, ZONE_FOREST_DEPTHS,
    ALL_ZONES, ZONE_SPAWN_POINTS, INGREDIENTS,
    SPAWN_RARITY_COMMON, SPAWN_RARITY_UNCOMMON, SPAWN_RARITY_RARE,
    SPAWN_CHANCE, RESPAWN_DAYS,
    QUALITY_MIN, QUALITY_MAX, QUALITY_SEASON_BONUS, QUALITY_WEATHER_BONUS,
    WEATHER_SUNNY, WEATHER_CLOUDY, WEATHER_RAINY, WEATHER_RESOURCE_MULTIPLIER,
    ITEM_VEGETABLE, ITEM_FRUIT, ITEM_SPICE, ITEM_SPECIAL
)
from systems.inventory import Item, get_inventory


@dataclass
class SpawnPoint:
    """
    A resource gathering point in a zone.

    Handles spawn probability, respawn timers, quality variation,
    and dragon ability requirements.
    """
    id: str                          # Unique identifier
    name: str                        # Display name
    x: int                           # Tile x position
    y: int                           # Tile y position
    ingredient_id: str               # ID of ingredient this spawns
    rarity: str = SPAWN_RARITY_COMMON  # Rarity tier
    requires_ability: Optional[str] = None  # Dragon ability needed

    # State
    is_available: bool = True        # Whether resources are present
    days_until_respawn: int = 0      # Days until respawn (0 = ready)
    current_quality: int = 3         # Quality of current spawn (1-5)
    current_quantity: int = 1        # How many can be gathered

    def get_spawn_chance(self) -> float:
        """Get the daily spawn probability based on rarity."""
        return SPAWN_CHANCE.get(self.rarity, 1.0)

    def get_respawn_days(self) -> int:
        """Get the respawn time based on rarity."""
        return RESPAWN_DAYS.get(self.rarity, 1)

    def can_gather(self, dragon_abilities: List[str] = None) -> bool:
        """
        Check if this spawn point can be gathered from.

        Args:
            dragon_abilities: List of abilities the dragon has

        Returns:
            True if gathering is possible
        """
        if not self.is_available:
            return False

        if self.requires_ability:
            if not dragon_abilities or self.requires_ability not in dragon_abilities:
                return False

        return True

    def gather(self, dragon_abilities: List[str] = None) -> Optional[Item]:
        """
        Gather from this spawn point.

        Args:
            dragon_abilities: List of abilities the dragon has

        Returns:
            Item gathered, or None if gathering failed
        """
        if not self.can_gather(dragon_abilities):
            return None

        # Get ingredient data
        if self.ingredient_id not in INGREDIENTS:
            return None

        name, category, base_price, spoil_days, color_influence = INGREDIENTS[self.ingredient_id]

        # Create item with quality modifier
        quality_mod = (self.current_quality - 3) * 0.15 + 1.0  # 0.7 to 1.3

        item = Item(
            id=self.ingredient_id,
            name=name,
            category=category,
            quality=quality_mod,
            spoil_days=spoil_days,
            base_price=base_price,
            color_influence=color_influence
        )

        # Decrease quantity
        self.current_quantity -= 1
        if self.current_quantity <= 0:
            self.is_available = False
            self.days_until_respawn = self.get_respawn_days()

        return item

    def try_respawn(self, weather: str = WEATHER_SUNNY, season: str = 'spring') -> bool:
        """
        Try to respawn this point if depleted.

        Args:
            weather: Current weather
            season: Current season

        Returns:
            True if respawned
        """
        if self.is_available:
            return False

        # Decrease respawn timer
        if self.days_until_respawn > 0:
            self.days_until_respawn -= 1
            return False

        # Roll for spawn based on rarity
        spawn_chance = self.get_spawn_chance()

        # Weather multiplier for rare items
        if self.rarity == SPAWN_RARITY_RARE:
            spawn_chance *= WEATHER_RESOURCE_MULTIPLIER.get(weather, 1.0)

        # NG+ resource scarcity (Phase 4) - reduces spawn chance
        from game_state import get_game_state_manager
        scarcity_modifier = get_game_state_manager().get_ng_plus_modifier('resource_scarcity')
        spawn_chance *= scarcity_modifier

        if random.random() > spawn_chance:
            return False

        # Spawn succeeded - calculate quality
        self.is_available = True
        self.current_quality = self._calculate_quality(weather, season)
        self.current_quantity = self._calculate_quantity()

        return True

    def _calculate_quality(self, weather: str, season: str) -> int:
        """Calculate quality for a new spawn."""
        # Base quality (random 2-4)
        quality = random.randint(2, 4)

        # Get ingredient type for bonuses
        ing_type = self._get_ingredient_type()

        # Season bonus
        season_bonuses = QUALITY_SEASON_BONUS.get(season, {})
        quality += season_bonuses.get(ing_type, 0)

        # Weather bonus
        weather_bonuses = QUALITY_WEATHER_BONUS.get(weather, {})
        quality += weather_bonuses.get(ing_type, 0)

        # Random variance (-1 to +1)
        quality += random.randint(-1, 1)

        # Clamp to valid range
        return max(QUALITY_MIN, min(QUALITY_MAX, quality))

    def _calculate_quantity(self) -> int:
        """Calculate quantity for a new spawn based on rarity."""
        if self.rarity == SPAWN_RARITY_COMMON:
            return random.randint(2, 3)
        elif self.rarity == SPAWN_RARITY_UNCOMMON:
            return random.randint(1, 2)
        else:  # Rare
            return 1

    def _get_ingredient_type(self) -> str:
        """Get the general type of ingredient for quality bonuses."""
        if self.ingredient_id not in INGREDIENTS:
            return ''

        name = INGREDIENTS[self.ingredient_id][0].lower()

        if 'berry' in name:
            return 'berry'
        elif 'herb' in name:
            return 'herb'
        elif 'flower' in name:
            return 'flower'
        elif 'mushroom' in name or 'fungi' in name:
            return 'mushroom'
        elif 'honey' in name:
            return 'honey'
        elif 'fish' in name:
            return 'fish'
        else:
            return ''

    def force_spawn(self, quality: int = 3, quantity: int = 1):
        """Force spawn for testing/initialization."""
        self.is_available = True
        self.current_quality = max(QUALITY_MIN, min(QUALITY_MAX, quality))
        self.current_quantity = max(1, quantity)
        self.days_until_respawn = 0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'ingredient_id': self.ingredient_id,
            'rarity': self.rarity,
            'requires_ability': self.requires_ability,
            'is_available': self.is_available,
            'days_until_respawn': self.days_until_respawn,
            'current_quality': self.current_quality,
            'current_quantity': self.current_quantity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpawnPoint':
        """Deserialize from dictionary."""
        sp = cls(
            id=data['id'],
            name=data['name'],
            x=data['x'],
            y=data['y'],
            ingredient_id=data['ingredient_id'],
            rarity=data.get('rarity', SPAWN_RARITY_COMMON),
            requires_ability=data.get('requires_ability'),
        )
        sp.is_available = data.get('is_available', True)
        sp.days_until_respawn = data.get('days_until_respawn', 0)
        sp.current_quality = data.get('current_quality', 3)
        sp.current_quantity = data.get('current_quantity', 1)
        return sp


class ResourceManager:
    """
    Manages all resource spawn points across zones.

    Usage:
        resources = get_resource_manager()
        resources.initialize()

        # Get available resources in current zone
        points = resources.get_zone_spawn_points('cafe_grounds')

        # Gather from a point
        item = resources.gather('cg_herb_1', dragon_abilities=['burrow_fetch'])
    """

    def __init__(self):
        """Initialize the resource manager."""
        self._spawn_points: Dict[str, SpawnPoint] = {}
        self._zone_spawn_ids: Dict[str, List[str]] = {zone: [] for zone in ALL_ZONES}
        self._initialized = False

    def initialize(self):
        """Initialize all spawn points from configuration."""
        if self._initialized:
            return

        for zone_id, spawn_defs in ZONE_SPAWN_POINTS.items():
            for sp_id, name, x, y, ing_id, rarity, ability in spawn_defs:
                sp = SpawnPoint(
                    id=sp_id,
                    name=name,
                    x=x,
                    y=y,
                    ingredient_id=ing_id,
                    rarity=rarity,
                    requires_ability=ability,
                )
                # Initial spawn
                sp.force_spawn(quality=random.randint(2, 4))

                self._spawn_points[sp_id] = sp
                self._zone_spawn_ids[zone_id].append(sp_id)

        self._initialized = True

    # =========================================================================
    # SPAWN POINT ACCESS
    # =========================================================================

    def get_spawn_point(self, spawn_id: str) -> Optional[SpawnPoint]:
        """Get a spawn point by ID."""
        return self._spawn_points.get(spawn_id)

    def get_zone_spawn_points(self, zone_id: str) -> List[SpawnPoint]:
        """Get all spawn points in a zone."""
        ids = self._zone_spawn_ids.get(zone_id, [])
        return [self._spawn_points[sp_id] for sp_id in ids if sp_id in self._spawn_points]

    def get_spawn_at_position(self, zone_id: str, x: int, y: int) -> Optional[SpawnPoint]:
        """Get spawn point at a specific position in a zone."""
        for sp in self.get_zone_spawn_points(zone_id):
            if sp.x == x and sp.y == y:
                return sp
        return None

    def get_available_spawns(self, zone_id: str, dragon_abilities: List[str] = None) -> List[SpawnPoint]:
        """Get all gatherable spawn points in a zone."""
        return [
            sp for sp in self.get_zone_spawn_points(zone_id)
            if sp.can_gather(dragon_abilities)
        ]

    def get_all_spawn_points(self) -> List[SpawnPoint]:
        """Get all spawn points."""
        return list(self._spawn_points.values())

    # =========================================================================
    # GATHERING
    # =========================================================================

    def gather(self, spawn_id: str, dragon_abilities: List[str] = None,
               add_to_inventory: bool = True) -> Optional[Item]:
        """
        Gather from a spawn point.

        Args:
            spawn_id: ID of spawn point to gather from
            dragon_abilities: Dragon's available abilities
            add_to_inventory: If True, automatically add to player inventory

        Returns:
            Item gathered, or None if failed
        """
        sp = self._spawn_points.get(spawn_id)
        if not sp:
            return None

        item = sp.gather(dragon_abilities)
        if item and add_to_inventory:
            inventory = get_inventory()
            overflow = inventory.add_item(item, 1, to_carried=True)
            if overflow > 0:
                # Inventory full - put it back
                sp.current_quantity += 1
                sp.is_available = True
                return None

        return item

    def can_gather_at(self, zone_id: str, x: int, y: int,
                      dragon_abilities: List[str] = None) -> bool:
        """Check if there's a gatherable resource at a position."""
        sp = self.get_spawn_at_position(zone_id, x, y)
        return sp.can_gather(dragon_abilities) if sp else False

    def gather_at(self, zone_id: str, x: int, y: int,
                  dragon_abilities: List[str] = None) -> Optional[Item]:
        """Gather from the spawn point at a position."""
        sp = self.get_spawn_at_position(zone_id, x, y)
        if not sp:
            return None
        return self.gather(sp.id, dragon_abilities)

    # =========================================================================
    # DAILY UPDATES
    # =========================================================================

    def advance_day(self, weather: str = WEATHER_SUNNY, season: str = 'spring'):
        """
        Process daily respawn logic.

        Args:
            weather: Current weather
            season: Current season
        """
        respawned = []

        for sp in self._spawn_points.values():
            if sp.try_respawn(weather, season):
                respawned.append(sp.id)

        return respawned

    def get_respawn_info(self) -> Dict[str, Tuple[int, bool]]:
        """Get respawn status for all points: {id: (days_remaining, is_available)}"""
        return {
            sp.id: (sp.days_until_respawn, sp.is_available)
            for sp in self._spawn_points.values()
        }

    # =========================================================================
    # VISUAL INDICATORS
    # =========================================================================

    def get_visual_indicator(self, spawn_id: str) -> Dict[str, Any]:
        """
        Get visual indicator data for a spawn point.

        Returns dict with:
            - visible: bool (whether to show indicator)
            - available: bool (whether resources present)
            - quality: int (1-5 stars)
            - locked: bool (requires ability player doesn't have)
            - ingredient_name: str
        """
        sp = self._spawn_points.get(spawn_id)
        if not sp:
            return {'visible': False}

        ing_name = ''
        if sp.ingredient_id in INGREDIENTS:
            ing_name = INGREDIENTS[sp.ingredient_id][0]

        return {
            'visible': True,
            'available': sp.is_available,
            'quality': sp.current_quality if sp.is_available else 0,
            'quantity': sp.current_quantity if sp.is_available else 0,
            'locked': sp.requires_ability is not None,
            'required_ability': sp.requires_ability,
            'ingredient_name': ing_name,
            'name': sp.name,
            'rarity': sp.rarity,
            'days_until_respawn': sp.days_until_respawn,
        }

    def get_zone_indicators(self, zone_id: str, dragon_abilities: List[str] = None) -> List[Dict[str, Any]]:
        """Get visual indicators for all spawn points in a zone."""
        indicators = []
        for sp in self.get_zone_spawn_points(zone_id):
            ind = self.get_visual_indicator(sp.id)
            ind['x'] = sp.x
            ind['y'] = sp.y
            # Check if player can actually gather
            ind['can_gather'] = sp.can_gather(dragon_abilities)
            indicators.append(ind)
        return indicators

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'spawn_points': {
                sp_id: sp.to_dict()
                for sp_id, sp in self._spawn_points.items()
            }
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        if not self._initialized:
            self.initialize()

        saved_points = state.get('spawn_points', {})
        for sp_id, sp_data in saved_points.items():
            if sp_id in self._spawn_points:
                # Update existing spawn point with saved state
                sp = self._spawn_points[sp_id]
                sp.is_available = sp_data.get('is_available', True)
                sp.days_until_respawn = sp_data.get('days_until_respawn', 0)
                sp.current_quality = sp_data.get('current_quality', 3)
                sp.current_quantity = sp_data.get('current_quantity', 1)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_resource_manager = None


def get_resource_manager() -> ResourceManager:
    """Get the global resource manager instance."""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager


def reset_resource_manager():
    """Reset the resource manager (for new game)."""
    global _resource_manager
    _resource_manager = ResourceManager()
