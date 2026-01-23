"""
Dragon Customization System for Dragon Haven Cafe.
Manages unlockable accessories, color patterns, and special effects for the dragon.
Phase 4 Feature.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from enum import Enum


# =============================================================================
# CUSTOMIZATION TYPES
# =============================================================================

class CustomizationSlot(Enum):
    """Slots where customizations can be equipped."""
    HEAD = "head"           # Hats, crowns, flowers
    NECK = "neck"           # Scarves, collars, pendants
    BACK = "back"           # Wings decorations, capes
    EFFECT = "effect"       # Particle effects, auras


class CustomizationType(Enum):
    """Types of customization items."""
    ACCESSORY = "accessory"  # Physical items (hat, scarf)
    PATTERN = "pattern"      # Color patterns (spots, stripes)
    EFFECT = "effect"        # Particle effects (sparkle, glow)


# =============================================================================
# CUSTOMIZATION ITEMS
# =============================================================================

@dataclass
class CustomizationItem:
    """Definition of a customization item."""
    item_id: str
    name: str
    description: str
    item_type: CustomizationType
    slot: CustomizationSlot
    unlock_condition: Dict[str, Any]  # How to unlock this item
    visual_data: Dict[str, Any] = field(default_factory=dict)  # Rendering info

    def to_dict(self) -> Dict[str, Any]:
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type.value,
            'slot': self.slot.value,
            'unlock_condition': self.unlock_condition,
            'visual_data': self.visual_data,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomizationItem':
        return cls(
            item_id=data['item_id'],
            name=data['name'],
            description=data['description'],
            item_type=CustomizationType(data['item_type']),
            slot=CustomizationSlot(data['slot']),
            unlock_condition=data.get('unlock_condition', {}),
            visual_data=data.get('visual_data', {}),
        )


# =============================================================================
# ITEM DEFINITIONS
# =============================================================================

# Accessories (Task 062)
ACCESSORIES: Dict[str, CustomizationItem] = {
    'red_scarf': CustomizationItem(
        item_id='red_scarf',
        name='Red Scarf',
        description='A cozy red scarf that shows your dragon is well-loved.',
        item_type=CustomizationType.ACCESSORY,
        slot=CustomizationSlot.NECK,
        unlock_condition={'type': 'reputation', 'value': 100},
        visual_data={'color': (200, 60, 60), 'style': 'wrap'},
    ),
    'chef_hat': CustomizationItem(
        item_id='chef_hat',
        name='Chef Hat',
        description='A tiny toque for your culinary companion.',
        item_type=CustomizationType.ACCESSORY,
        slot=CustomizationSlot.HEAD,
        unlock_condition={'type': 'recipes_mastered', 'value': 10},
        visual_data={'color': (255, 255, 255), 'style': 'toque'},
    ),
    'flower_crown': CustomizationItem(
        item_id='flower_crown',
        name='Flower Crown',
        description='A delicate crown of wildflowers, earned through friendship.',
        item_type=CustomizationType.ACCESSORY,
        slot=CustomizationSlot.HEAD,
        unlock_condition={'type': 'all_characters_befriended', 'value': True},
        visual_data={'colors': [(255, 180, 200), (255, 255, 150), (180, 220, 255)], 'style': 'crown'},
    ),
    'crystal_pendant': CustomizationItem(
        item_id='crystal_pendant',
        name='Crystal Pendant',
        description='A glowing crystal from the Ancient Ruins.',
        item_type=CustomizationType.ACCESSORY,
        slot=CustomizationSlot.NECK,
        unlock_condition={'type': 'zone_completed', 'value': 'ancient_ruins'},
        visual_data={'color': (150, 200, 255), 'glow': True, 'style': 'pendant'},
    ),
    'cloud_wings': CustomizationItem(
        item_id='cloud_wings',
        name='Cloud Wings',
        description='Ethereal wing decorations from the Sky Islands.',
        item_type=CustomizationType.ACCESSORY,
        slot=CustomizationSlot.BACK,
        unlock_condition={'type': 'zone_visits', 'zone': 'sky_islands', 'value': 10},
        visual_data={'color': (240, 240, 255), 'alpha': 180, 'style': 'ethereal'},
    ),
    'golden_collar': CustomizationItem(
        item_id='golden_collar',
        name='Golden Collar',
        description='An ornate collar showing your prosperity.',
        item_type=CustomizationType.ACCESSORY,
        slot=CustomizationSlot.NECK,
        unlock_condition={'type': 'total_gold_earned', 'value': 10000},
        visual_data={'color': (255, 215, 0), 'style': 'ornate'},
    ),
}

# Color Patterns (Task 063)
PATTERNS: Dict[str, CustomizationItem] = {
    'spots': CustomizationItem(
        item_id='spots',
        name='Spotted Pattern',
        description='Cute spots appear on your dragon\'s scales.',
        item_type=CustomizationType.PATTERN,
        slot=CustomizationSlot.EFFECT,  # Patterns apply globally
        unlock_condition={'type': 'dragon_stage', 'value': 'juvenile'},
        visual_data={'pattern_type': 'spots', 'density': 0.3},
    ),
    'stripes': CustomizationItem(
        item_id='stripes',
        name='Tiger Stripes',
        description='Bold stripes mark your dragon as fierce.',
        item_type=CustomizationType.PATTERN,
        slot=CustomizationSlot.EFFECT,
        unlock_condition={'type': 'dragon_stage', 'value': 'adolescent'},
        visual_data={'pattern_type': 'stripes', 'width': 3},
    ),
    'gradient': CustomizationItem(
        item_id='gradient',
        name='Color Gradient',
        description='A beautiful color fade across your dragon\'s body.',
        item_type=CustomizationType.PATTERN,
        slot=CustomizationSlot.EFFECT,
        unlock_condition={'type': 'dragon_stage', 'value': 'adult'},
        visual_data={'pattern_type': 'gradient', 'direction': 'vertical'},
    ),
    'starlight': CustomizationItem(
        item_id='starlight',
        name='Starlight Scales',
        description='Your dragon sparkles with collected starlight.',
        item_type=CustomizationType.PATTERN,
        slot=CustomizationSlot.EFFECT,
        unlock_condition={'type': 'item_collected', 'item': 'starlight_crystal', 'value': 50},
        visual_data={'pattern_type': 'sparkle', 'intensity': 0.5},
    ),
    'flame': CustomizationItem(
        item_id='flame',
        name='Ember Trail',
        description='Tiny embers follow your dragon\'s movements.',
        item_type=CustomizationType.PATTERN,
        slot=CustomizationSlot.EFFECT,
        unlock_condition={'type': 'ability_uses', 'ability': 'fire_stream', 'value': 100},
        visual_data={'pattern_type': 'ember', 'particle_count': 5},
    ),
}

# Special Effects (Task 064)
EFFECTS: Dict[str, CustomizationItem] = {
    'sparkle_trail': CustomizationItem(
        item_id='sparkle_trail',
        name='Sparkle Trail',
        description='Leave a trail of sparkles wherever you go.',
        item_type=CustomizationType.EFFECT,
        slot=CustomizationSlot.EFFECT,
        unlock_condition={'type': 'achievement', 'value': 'best_friends'},
        visual_data={'effect_type': 'trail', 'particle': 'sparkle', 'rate': 3},
    ),
    'glow_aura': CustomizationItem(
        item_id='glow_aura',
        name='Legendary Glow',
        description='A soft glow surrounds your legendary dragon.',
        item_type=CustomizationType.EFFECT,
        slot=CustomizationSlot.EFFECT,
        unlock_condition={'type': 'achievement', 'value': 'legendary_status'},
        visual_data={'effect_type': 'aura', 'color': (255, 240, 200), 'radius': 20},
    ),
    'mini_crown': CustomizationItem(
        item_id='mini_crown',
        name='Floating Crown',
        description='A tiny crown floats above your dragon.',
        item_type=CustomizationType.EFFECT,
        slot=CustomizationSlot.HEAD,
        unlock_condition={'type': 'achievement', 'value': 'recipe_master'},
        visual_data={'effect_type': 'floating', 'item': 'crown', 'bob_speed': 1.5},
    ),
}

# Combined lookup
ALL_CUSTOMIZATIONS: Dict[str, CustomizationItem] = {
    **ACCESSORIES,
    **PATTERNS,
    **EFFECTS,
}


# =============================================================================
# CUSTOMIZATION STATE
# =============================================================================

@dataclass
class DragonCustomization:
    """
    Tracks a dragon's customization state.

    Stores:
    - Unlocked customization items
    - Currently equipped items per slot
    - Active pattern and effects
    """
    unlocked_items: Set[str] = field(default_factory=set)
    equipped: Dict[str, Optional[str]] = field(default_factory=lambda: {
        CustomizationSlot.HEAD.value: None,
        CustomizationSlot.NECK.value: None,
        CustomizationSlot.BACK.value: None,
        CustomizationSlot.EFFECT.value: None,
    })
    active_pattern: Optional[str] = None

    def unlock_item(self, item_id: str) -> bool:
        """
        Unlock a customization item.

        Returns:
            True if newly unlocked, False if already unlocked
        """
        if item_id not in ALL_CUSTOMIZATIONS:
            return False
        if item_id in self.unlocked_items:
            return False
        self.unlocked_items.add(item_id)
        return True

    def is_unlocked(self, item_id: str) -> bool:
        """Check if an item is unlocked."""
        return item_id in self.unlocked_items

    def equip(self, item_id: str) -> bool:
        """
        Equip an item to its appropriate slot.

        Returns:
            True if equipped successfully
        """
        if item_id not in self.unlocked_items:
            return False

        item = ALL_CUSTOMIZATIONS.get(item_id)
        if not item:
            return False

        # Handle patterns specially
        if item.item_type == CustomizationType.PATTERN:
            self.active_pattern = item_id
            return True

        # Regular equipment
        self.equipped[item.slot.value] = item_id
        return True

    def unequip(self, slot: CustomizationSlot) -> Optional[str]:
        """
        Unequip item from a slot.

        Returns:
            The unequipped item_id, or None
        """
        slot_key = slot.value
        previous = self.equipped.get(slot_key)
        self.equipped[slot_key] = None
        return previous

    def unequip_pattern(self) -> Optional[str]:
        """Remove active pattern."""
        previous = self.active_pattern
        self.active_pattern = None
        return previous

    def get_equipped(self, slot: CustomizationSlot) -> Optional[CustomizationItem]:
        """Get the item equipped in a slot."""
        item_id = self.equipped.get(slot.value)
        if item_id:
            return ALL_CUSTOMIZATIONS.get(item_id)
        return None

    def get_active_pattern(self) -> Optional[CustomizationItem]:
        """Get the currently active pattern."""
        if self.active_pattern:
            return ALL_CUSTOMIZATIONS.get(self.active_pattern)
        return None

    def get_all_equipped(self) -> List[CustomizationItem]:
        """Get list of all currently equipped items."""
        items = []
        for slot_value, item_id in self.equipped.items():
            if item_id:
                item = ALL_CUSTOMIZATIONS.get(item_id)
                if item:
                    items.append(item)
        if self.active_pattern:
            pattern = ALL_CUSTOMIZATIONS.get(self.active_pattern)
            if pattern:
                items.append(pattern)
        return items

    def get_unlocked_by_type(self, item_type: CustomizationType) -> List[CustomizationItem]:
        """Get all unlocked items of a specific type."""
        items = []
        for item_id in self.unlocked_items:
            item = ALL_CUSTOMIZATIONS.get(item_id)
            if item and item.item_type == item_type:
                items.append(item)
        return items

    def to_dict(self) -> Dict[str, Any]:
        return {
            'unlocked_items': list(self.unlocked_items),
            'equipped': self.equipped.copy(),
            'active_pattern': self.active_pattern,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DragonCustomization':
        customization = cls()
        customization.unlocked_items = set(data.get('unlocked_items', []))
        customization.equipped = data.get('equipped', {
            CustomizationSlot.HEAD.value: None,
            CustomizationSlot.NECK.value: None,
            CustomizationSlot.BACK.value: None,
            CustomizationSlot.EFFECT.value: None,
        })
        customization.active_pattern = data.get('active_pattern')
        return customization


# =============================================================================
# CUSTOMIZATION MANAGER
# =============================================================================

class CustomizationManager:
    """
    Manages customization unlocks and checks conditions.

    Usage:
        manager = get_customization_manager()
        manager.check_unlocks()  # Call periodically to unlock earned items
        manager.get_available_for_slot(CustomizationSlot.HEAD)
    """

    def __init__(self):
        self._customization: DragonCustomization = DragonCustomization()
        self._pending_unlocks: List[str] = []  # Items unlocked but not yet shown

    def get_customization(self) -> DragonCustomization:
        """Get the dragon's customization state."""
        return self._customization

    def check_unlocks(self) -> List[str]:
        """
        Check all conditions and unlock eligible items.

        Returns:
            List of newly unlocked item_ids
        """
        newly_unlocked = []

        for item_id, item in ALL_CUSTOMIZATIONS.items():
            if item_id in self._customization.unlocked_items:
                continue

            if self._check_condition(item.unlock_condition):
                self._customization.unlock_item(item_id)
                newly_unlocked.append(item_id)
                self._pending_unlocks.append(item_id)

        return newly_unlocked

    def _check_condition(self, condition: Dict[str, Any]) -> bool:
        """Check if an unlock condition is met."""
        cond_type = condition.get('type')
        value = condition.get('value')

        if cond_type == 'reputation':
            from systems.cafe import get_cafe_manager
            return get_cafe_manager().get_reputation() >= value

        elif cond_type == 'recipes_mastered':
            from systems.recipes import get_recipe_manager
            mastery = get_recipe_manager().get_state().get('mastery', {})
            mastered_count = sum(1 for m in mastery.values() if m.get('level', 0) >= 3)
            return mastered_count >= value

        elif cond_type == 'all_characters_befriended':
            from entities.story_character import get_character_manager
            manager = get_character_manager()
            state = manager.get_state()
            characters = state.get('characters', {})
            # Consider befriended at affinity >= 80
            befriended = all(c.get('affinity', 0) >= 80 for c in characters.values())
            return befriended and len(characters) >= 3

        elif cond_type == 'zone_completed':
            from systems.achievements import get_achievement_manager
            achievements = get_achievement_manager()
            # Check for zone-specific achievement
            zone_achievement = f"explore_{value}"
            return achievements.is_unlocked(zone_achievement)

        elif cond_type == 'zone_visits':
            # This would need tracking in world manager
            # For now, approximate with zone unlock
            from systems.world import get_world_manager
            zone = condition.get('zone')
            visits = condition.get('value', 10)
            # Simplified: check if zone is unlocked
            return get_world_manager().is_zone_unlocked(zone)

        elif cond_type == 'total_gold_earned':
            from systems.economy import get_economy
            return get_economy()._total_earned >= value

        elif cond_type == 'dragon_stage':
            from systems.dragon_manager import get_dragon_manager
            dragon = get_dragon_manager().get_dragon()
            if dragon:
                return dragon.get_stage() == value
            return False

        elif cond_type == 'item_collected':
            # Would need inventory tracking
            # Simplified for now
            return False

        elif cond_type == 'ability_uses':
            # Would need ability tracking
            # Simplified for now
            return False

        elif cond_type == 'achievement':
            from systems.achievements import get_achievement_manager
            return get_achievement_manager().is_unlocked(value)

        return False

    def get_pending_unlocks(self) -> List[CustomizationItem]:
        """Get items that were unlocked but not yet shown to player."""
        items = []
        for item_id in self._pending_unlocks:
            item = ALL_CUSTOMIZATIONS.get(item_id)
            if item:
                items.append(item)
        return items

    def clear_pending_unlocks(self):
        """Clear the pending unlocks list after showing to player."""
        self._pending_unlocks.clear()

    def equip_item(self, item_id: str) -> bool:
        """Equip an item."""
        return self._customization.equip(item_id)

    def unequip_slot(self, slot: CustomizationSlot) -> Optional[str]:
        """Unequip from a slot."""
        return self._customization.unequip(slot)

    def get_available_for_slot(self, slot: CustomizationSlot) -> List[CustomizationItem]:
        """Get all unlocked items that can be equipped in a slot."""
        items = []
        for item_id in self._customization.unlocked_items:
            item = ALL_CUSTOMIZATIONS.get(item_id)
            if item and item.slot == slot:
                items.append(item)
        return items

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'customization': self._customization.to_dict(),
            'pending_unlocks': self._pending_unlocks.copy(),
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        if 'customization' in state:
            self._customization = DragonCustomization.from_dict(state['customization'])
        self._pending_unlocks = state.get('pending_unlocks', [])


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_customization_manager: Optional[CustomizationManager] = None


def get_customization_manager() -> CustomizationManager:
    """Get the global customization manager instance."""
    global _customization_manager
    if _customization_manager is None:
        _customization_manager = CustomizationManager()
    return _customization_manager
