"""
Seasonal Decorations System for Dragon Haven Cafe.
Manages visual decorations that appear during seasonal events.
Phase 4 Feature.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import math


# =============================================================================
# DECORATION TYPES
# =============================================================================

class DecorationType(Enum):
    """Types of decorations."""
    HANGING = "hanging"      # Suspended from ceiling/top
    FLOOR = "floor"          # Placed on ground
    WALL = "wall"            # Attached to walls
    TABLE = "table"          # On tables/counters
    AMBIENT = "ambient"      # Floating/particle effects


class DecorationZone(Enum):
    """Where decorations can appear."""
    CAFE = "cafe"            # Inside cafe
    CAFE_EXTERIOR = "cafe_exterior"  # Outside cafe
    ALL_ZONES = "all_zones"  # In exploration zones


# =============================================================================
# DECORATION DEFINITIONS
# =============================================================================

@dataclass
class DecorationDef:
    """Definition of a seasonal decoration."""
    decoration_id: str
    name: str
    deco_type: DecorationType
    zone: DecorationZone
    color_primary: Tuple[int, int, int]
    color_secondary: Tuple[int, int, int]
    size: Tuple[int, int]  # Width, height
    animation_type: str  # 'static', 'sway', 'float', 'sparkle'
    layer: int  # Draw order (0=background, higher=foreground)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'decoration_id': self.decoration_id,
            'name': self.name,
            'deco_type': self.deco_type.value,
            'zone': self.zone.value,
            'color_primary': self.color_primary,
            'color_secondary': self.color_secondary,
            'size': self.size,
            'animation_type': self.animation_type,
            'layer': self.layer,
        }


# Spring Festival Decorations
SPRING_DECORATIONS: Dict[str, DecorationDef] = {
    'cherry_blossoms': DecorationDef(
        decoration_id='cherry_blossoms',
        name='Cherry Blossoms',
        deco_type=DecorationType.HANGING,
        zone=DecorationZone.CAFE,
        color_primary=(255, 182, 193),  # Light pink
        color_secondary=(255, 105, 180),  # Hot pink
        size=(60, 40),
        animation_type='sway',
        layer=3,
    ),
    'egg_banners': DecorationDef(
        decoration_id='egg_banners',
        name='Egg Banners',
        deco_type=DecorationType.WALL,
        zone=DecorationZone.CAFE,
        color_primary=(144, 238, 144),  # Light green
        color_secondary=(255, 215, 0),  # Gold
        size=(30, 50),
        animation_type='static',
        layer=1,
    ),
    'spring_flowers': DecorationDef(
        decoration_id='spring_flowers',
        name='Spring Flower Pots',
        deco_type=DecorationType.TABLE,
        zone=DecorationZone.CAFE,
        color_primary=(255, 255, 100),  # Yellow
        color_secondary=(50, 205, 50),  # Lime green
        size=(25, 30),
        animation_type='static',
        layer=2,
    ),
}

# Summer Feast Decorations
SUMMER_DECORATIONS: Dict[str, DecorationDef] = {
    'harvest_wreaths': DecorationDef(
        decoration_id='harvest_wreaths',
        name='Harvest Wreaths',
        deco_type=DecorationType.WALL,
        zone=DecorationZone.CAFE,
        color_primary=(218, 165, 32),  # Goldenrod
        color_secondary=(139, 69, 19),  # Saddle brown
        size=(50, 50),
        animation_type='static',
        layer=1,
    ),
    'lanterns': DecorationDef(
        decoration_id='lanterns',
        name='Summer Lanterns',
        deco_type=DecorationType.HANGING,
        zone=DecorationZone.CAFE,
        color_primary=(255, 200, 100),  # Warm yellow
        color_secondary=(255, 140, 0),  # Dark orange
        size=(25, 35),
        animation_type='float',
        layer=3,
    ),
    'fruit_displays': DecorationDef(
        decoration_id='fruit_displays',
        name='Fruit Displays',
        deco_type=DecorationType.TABLE,
        zone=DecorationZone.CAFE,
        color_primary=(255, 99, 71),  # Tomato red
        color_secondary=(255, 165, 0),  # Orange
        size=(40, 25),
        animation_type='static',
        layer=2,
    ),
}

# Autumn Lantern Festival Decorations
AUTUMN_DECORATIONS: Dict[str, DecorationDef] = {
    'paper_lanterns': DecorationDef(
        decoration_id='paper_lanterns',
        name='Paper Lanterns',
        deco_type=DecorationType.HANGING,
        zone=DecorationZone.ALL_ZONES,
        color_primary=(255, 69, 0),  # Orange red
        color_secondary=(255, 215, 0),  # Gold
        size=(30, 40),
        animation_type='sway',
        layer=3,
    ),
    'autumn_leaves': DecorationDef(
        decoration_id='autumn_leaves',
        name='Autumn Leaf Garlands',
        deco_type=DecorationType.HANGING,
        zone=DecorationZone.CAFE,
        color_primary=(205, 92, 0),  # Dark orange
        color_secondary=(178, 34, 34),  # Firebrick
        size=(80, 20),
        animation_type='sway',
        layer=2,
    ),
    'candle_arrangements': DecorationDef(
        decoration_id='candle_arrangements',
        name='Candle Arrangements',
        deco_type=DecorationType.TABLE,
        zone=DecorationZone.CAFE,
        color_primary=(255, 250, 205),  # Lemon chiffon
        color_secondary=(255, 140, 0),  # Dark orange
        size=(30, 35),
        animation_type='sparkle',
        layer=2,
    ),
}

# Winter Celebration Decorations
WINTER_DECORATIONS: Dict[str, DecorationDef] = {
    'snowflakes': DecorationDef(
        decoration_id='snowflakes',
        name='Paper Snowflakes',
        deco_type=DecorationType.HANGING,
        zone=DecorationZone.CAFE,
        color_primary=(255, 255, 255),  # White
        color_secondary=(200, 230, 255),  # Light blue
        size=(35, 35),
        animation_type='float',
        layer=3,
    ),
    'warm_lights': DecorationDef(
        decoration_id='warm_lights',
        name='Warm String Lights',
        deco_type=DecorationType.HANGING,
        zone=DecorationZone.CAFE,
        color_primary=(255, 223, 186),  # Peach puff
        color_secondary=(255, 200, 100),  # Warm yellow
        size=(100, 15),
        animation_type='sparkle',
        layer=4,
    ),
    'frost_crystals': DecorationDef(
        decoration_id='frost_crystals',
        name='Frost Crystal Display',
        deco_type=DecorationType.TABLE,
        zone=DecorationZone.CAFE,
        color_primary=(173, 216, 230),  # Light blue
        color_secondary=(135, 206, 250),  # Light sky blue
        size=(30, 40),
        animation_type='sparkle',
        layer=2,
    ),
    'gift_boxes': DecorationDef(
        decoration_id='gift_boxes',
        name='Gift Box Stack',
        deco_type=DecorationType.FLOOR,
        zone=DecorationZone.CAFE,
        color_primary=(220, 20, 60),  # Crimson
        color_secondary=(34, 139, 34),  # Forest green
        size=(45, 50),
        animation_type='static',
        layer=1,
    ),
}

# Combined lookup
ALL_DECORATIONS: Dict[str, DecorationDef] = {
    **SPRING_DECORATIONS,
    **SUMMER_DECORATIONS,
    **AUTUMN_DECORATIONS,
    **WINTER_DECORATIONS,
}

# Map event decorations to decoration IDs
EVENT_DECORATIONS: Dict[str, List[str]] = {
    'spring_festival': ['cherry_blossoms', 'egg_banners', 'spring_flowers'],
    'summer_feast': ['harvest_wreaths', 'lanterns', 'fruit_displays'],
    'autumn_lantern': ['paper_lanterns', 'autumn_leaves', 'candle_arrangements'],
    'winter_celebration': ['snowflakes', 'warm_lights', 'frost_crystals', 'gift_boxes'],
}


# =============================================================================
# DECORATION INSTANCE
# =============================================================================

@dataclass
class DecorationInstance:
    """An active decoration placed in the world."""
    decoration_id: str
    position: Tuple[int, int]  # x, y
    animation_offset: float  # Random offset for animation variation
    scale: float = 1.0  # Size multiplier

    def to_dict(self) -> Dict[str, Any]:
        return {
            'decoration_id': self.decoration_id,
            'position': self.position,
            'animation_offset': self.animation_offset,
            'scale': self.scale,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DecorationInstance':
        return cls(
            decoration_id=data['decoration_id'],
            position=tuple(data['position']),
            animation_offset=data.get('animation_offset', 0.0),
            scale=data.get('scale', 1.0),
        )


# =============================================================================
# DECORATION MANAGER
# =============================================================================

class DecorationManager:
    """
    Manages seasonal decorations for the cafe and exploration zones.

    Usage:
        decos = get_decoration_manager()
        decos.activate_event_decorations('spring_festival')
        cafe_decos = decos.get_decorations_for_zone(DecorationZone.CAFE)
    """

    # Default decoration placement positions for cafe
    CAFE_POSITIONS = {
        DecorationType.HANGING: [
            (200, 50), (400, 60), (600, 50), (800, 55),
            (300, 70), (500, 65), (700, 70),
        ],
        DecorationType.WALL: [
            (100, 150), (1100, 150), (100, 350), (1100, 350),
        ],
        DecorationType.TABLE: [
            (250, 450), (450, 420), (650, 440), (850, 430),
        ],
        DecorationType.FLOOR: [
            (150, 550), (1050, 550),
        ],
        DecorationType.AMBIENT: [
            (640, 360),  # Center of screen
        ],
    }

    def __init__(self):
        self._active_event: Optional[str] = None
        self._active_decorations: List[DecorationInstance] = []
        self._animation_time = 0.0

    def activate_event_decorations(self, event_id: str):
        """
        Activate decorations for a seasonal event.

        Args:
            event_id: ID of the seasonal event
        """
        if event_id == self._active_event:
            return  # Already active

        self._active_event = event_id
        self._active_decorations = []

        if event_id not in EVENT_DECORATIONS:
            return

        import random
        decoration_ids = EVENT_DECORATIONS[event_id]

        for deco_id in decoration_ids:
            deco_def = ALL_DECORATIONS.get(deco_id)
            if not deco_def:
                continue

            # Get positions for this decoration type
            positions = self.CAFE_POSITIONS.get(deco_def.deco_type, [])

            for pos in positions:
                # Create instance with random variation
                instance = DecorationInstance(
                    decoration_id=deco_id,
                    position=pos,
                    animation_offset=random.random() * 2 * math.pi,
                    scale=0.8 + random.random() * 0.4,  # 0.8 to 1.2
                )
                self._active_decorations.append(instance)

    def deactivate_decorations(self):
        """Remove all active decorations."""
        self._active_event = None
        self._active_decorations = []

    def update(self, dt: float):
        """Update decoration animations."""
        self._animation_time += dt

    def get_animation_time(self) -> float:
        """Get current animation time for rendering."""
        return self._animation_time

    def is_event_active(self) -> bool:
        """Check if decorations are active."""
        return self._active_event is not None

    def get_active_event(self) -> Optional[str]:
        """Get the currently active event ID."""
        return self._active_event

    def get_decorations_for_zone(self, zone: DecorationZone) -> List[Tuple[DecorationInstance, DecorationDef]]:
        """
        Get all decorations applicable to a zone.

        Args:
            zone: The zone to get decorations for

        Returns:
            List of (instance, definition) tuples
        """
        result = []
        for instance in self._active_decorations:
            deco_def = ALL_DECORATIONS.get(instance.decoration_id)
            if deco_def:
                # Check if decoration applies to this zone
                if deco_def.zone == zone or deco_def.zone == DecorationZone.ALL_ZONES:
                    result.append((instance, deco_def))

        # Sort by layer for proper draw order
        result.sort(key=lambda x: x[1].layer)
        return result

    def get_decoration_render_data(self, instance: DecorationInstance,
                                   deco_def: DecorationDef) -> Dict[str, Any]:
        """
        Get render data for a decoration including animation state.

        Args:
            instance: The decoration instance
            deco_def: The decoration definition

        Returns:
            Dictionary with position, size, colors, and animation state
        """
        x, y = instance.position
        w, h = deco_def.size
        w = int(w * instance.scale)
        h = int(h * instance.scale)

        # Calculate animation offset
        anim_x, anim_y = 0, 0
        anim_alpha = 255

        t = self._animation_time + instance.animation_offset

        if deco_def.animation_type == 'sway':
            # Gentle side-to-side swaying
            anim_x = int(math.sin(t * 1.5) * 5)
        elif deco_def.animation_type == 'float':
            # Gentle up-down floating
            anim_y = int(math.sin(t * 0.8) * 8)
        elif deco_def.animation_type == 'sparkle':
            # Brightness pulsing
            pulse = (math.sin(t * 3) + 1) / 2  # 0 to 1
            anim_alpha = int(180 + pulse * 75)  # 180 to 255

        return {
            'x': x + anim_x,
            'y': y + anim_y,
            'width': w,
            'height': h,
            'color_primary': deco_def.color_primary,
            'color_secondary': deco_def.color_secondary,
            'alpha': anim_alpha,
            'decoration_type': deco_def.deco_type.value,
            'layer': deco_def.layer,
        }

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'active_event': self._active_event,
            'animation_time': self._animation_time,
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._animation_time = state.get('animation_time', 0.0)
        event_id = state.get('active_event')
        if event_id:
            self.activate_event_decorations(event_id)
        else:
            self.deactivate_decorations()


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_decoration_manager: Optional[DecorationManager] = None


def get_decoration_manager() -> DecorationManager:
    """Get the global decoration manager instance."""
    global _decoration_manager
    if _decoration_manager is None:
        _decoration_manager = DecorationManager()
    return _decoration_manager
