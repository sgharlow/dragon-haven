"""
Save/Load System for Dragon Haven Cafe.
Handles game state persistence with multiple save slots.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from constants import VERSION


# =============================================================================
# SAVE DATA STRUCTURE
# =============================================================================

@dataclass
class PlayerData:
    """Player profile data."""
    name: str = "Player"
    total_gold_earned: int = 0
    total_customers_served: int = 0


@dataclass
class DragonData:
    """Dragon state data (placeholder for future expansion)."""
    name: str = ""
    stage: str = "egg"  # egg, hatchling, juvenile
    age_days: int = 0
    color_shift: tuple = (0, 0, 0)
    # Stats
    hunger: float = 100.0
    happiness: float = 100.0
    energy: float = 100.0
    # Abilities unlocked
    abilities: List[str] = field(default_factory=list)


@dataclass
class CafeData:
    """Cafe state data (placeholder for future expansion)."""
    gold: int = 100
    reputation: int = 0
    level: int = 1
    # Unlocked recipes
    recipes_unlocked: List[str] = field(default_factory=list)
    # Staff hired
    staff_ids: List[str] = field(default_factory=list)


@dataclass
class WorldData:
    """World state data (placeholder for future expansion)."""
    current_zone: str = "cafe_grounds"
    day_number: int = 1
    current_time: float = 8.0  # Hours (8.0 = 8:00 AM)
    weather: str = "sunny"
    # Zones unlocked
    zones_unlocked: List[str] = field(default_factory=lambda: ["cafe_grounds"])
    # Discovered resources/items
    discovered_items: List[str] = field(default_factory=list)


@dataclass
class StoryData:
    """Story progress data (placeholder for future expansion)."""
    current_chapter: int = 1
    events_completed: List[str] = field(default_factory=list)
    character_relationships: Dict[str, int] = field(default_factory=dict)
    dialogue_flags: Dict[str, bool] = field(default_factory=dict)


@dataclass
class InventoryData:
    """Player inventory data (placeholder for future expansion)."""
    items: Dict[str, int] = field(default_factory=dict)  # item_id -> quantity
    max_slots: int = 20


@dataclass
class SaveMeta:
    """Save file metadata."""
    slot: int = 1
    version: str = VERSION
    playtime_seconds: float = 0.0
    last_saved: str = ""
    created_at: str = ""


@dataclass
class SaveData:
    """
    Complete save game data structure.

    Contains all persistent game state organized into sections.
    """
    meta: SaveMeta = field(default_factory=SaveMeta)
    player: PlayerData = field(default_factory=PlayerData)
    dragon: DragonData = field(default_factory=DragonData)
    cafe: CafeData = field(default_factory=CafeData)
    world: WorldData = field(default_factory=WorldData)
    story: StoryData = field(default_factory=StoryData)
    inventory: InventoryData = field(default_factory=InventoryData)

    def to_dict(self) -> Dict[str, Any]:
        """Convert save data to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SaveData':
        """Create SaveData from dictionary."""
        return cls(
            meta=SaveMeta(**data.get('meta', {})),
            player=PlayerData(**data.get('player', {})),
            dragon=DragonData(**data.get('dragon', {})),
            cafe=CafeData(**data.get('cafe', {})),
            world=WorldData(**data.get('world', {})),
            story=StoryData(**data.get('story', {})),
            inventory=InventoryData(**data.get('inventory', {}))
        )


@dataclass
class SaveSlotInfo:
    """Information about a save slot (for save/load UI)."""
    slot: int
    exists: bool
    version: str = ""
    playtime_seconds: float = 0.0
    last_saved: str = ""
    player_name: str = ""
    dragon_name: str = ""
    dragon_stage: str = ""
    day_number: int = 0
    cafe_level: int = 0


# =============================================================================
# SAVE MANAGER
# =============================================================================

class SaveManager:
    """
    Manages save/load operations for the game.

    Usage:
        saves = get_save_manager()
        saves.initialize()

        # Save current game
        save_data = SaveData()
        saves.save(1, save_data)

        # Load game
        loaded = saves.load(1)

        # List saves
        slots = saves.list_saves()
    """

    NUM_SLOTS = 3
    SAVE_DIR = "saves"

    def __init__(self):
        """Initialize the save manager."""
        self._initialized = False
        self._save_dir = None

    def initialize(self, base_path: str = None):
        """
        Initialize the save manager and create save directory.

        Args:
            base_path: Optional base path for saves directory
        """
        if base_path:
            self._save_dir = os.path.join(base_path, self.SAVE_DIR)
        else:
            # Default to saves/ in current working directory
            self._save_dir = self.SAVE_DIR

        # Create saves directory if it doesn't exist
        if not os.path.exists(self._save_dir):
            os.makedirs(self._save_dir)

        self._initialized = True

    def _get_save_path(self, slot: int) -> str:
        """Get the file path for a save slot."""
        return os.path.join(self._save_dir, f"slot_{slot}.json")

    def _validate_slot(self, slot: int) -> bool:
        """Check if slot number is valid."""
        return 1 <= slot <= self.NUM_SLOTS

    def save(self, slot: int, data: SaveData) -> bool:
        """
        Save game data to a slot.

        Args:
            slot: Save slot number (1-3)
            data: SaveData instance to save

        Returns:
            True if save successful, False otherwise
        """
        if not self._initialized:
            print("Warning: SaveManager not initialized")
            return False

        if not self._validate_slot(slot):
            print(f"Warning: Invalid save slot {slot}")
            return False

        try:
            # Update metadata
            data.meta.slot = slot
            data.meta.version = VERSION
            data.meta.last_saved = datetime.now().isoformat()
            if not data.meta.created_at:
                data.meta.created_at = data.meta.last_saved

            # Serialize to JSON
            save_path = self._get_save_path(slot)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data.to_dict(), f, indent=2)

            return True

        except (IOError, TypeError, ValueError) as e:
            print(f"Error saving to slot {slot}: {e}")
            return False

    def load(self, slot: int) -> Optional[SaveData]:
        """
        Load game data from a slot.

        Args:
            slot: Save slot number (1-3)

        Returns:
            SaveData instance if successful, None otherwise
        """
        if not self._initialized:
            print("Warning: SaveManager not initialized")
            return None

        if not self._validate_slot(slot):
            print(f"Warning: Invalid save slot {slot}")
            return None

        save_path = self._get_save_path(slot)
        if not os.path.exists(save_path):
            return None

        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            # Version compatibility check
            saved_version = raw_data.get('meta', {}).get('version', '0.0.0')
            if not self._check_version_compatible(saved_version):
                print(f"Warning: Save version {saved_version} may not be compatible with {VERSION}")
                # Still try to load, but warn

            return SaveData.from_dict(raw_data)

        except (IOError, json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Error loading slot {slot}: {e}")
            return None

    def _check_version_compatible(self, saved_version: str) -> bool:
        """
        Check if a saved version is compatible with current version.

        For now, we use simple major version checking.
        """
        try:
            saved_major = int(saved_version.split('.')[0])
            current_major = int(VERSION.split('.')[0])
            return saved_major == current_major
        except (ValueError, IndexError):
            return False

    def list_saves(self) -> List[SaveSlotInfo]:
        """
        Get information about all save slots.

        Returns:
            List of SaveSlotInfo for all slots
        """
        if not self._initialized:
            return [SaveSlotInfo(slot=i, exists=False) for i in range(1, self.NUM_SLOTS + 1)]

        slots = []
        for slot in range(1, self.NUM_SLOTS + 1):
            save_path = self._get_save_path(slot)

            if not os.path.exists(save_path):
                slots.append(SaveSlotInfo(slot=slot, exists=False))
                continue

            try:
                with open(save_path, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)

                meta = raw_data.get('meta', {})
                player = raw_data.get('player', {})
                dragon = raw_data.get('dragon', {})
                world = raw_data.get('world', {})
                cafe = raw_data.get('cafe', {})

                slots.append(SaveSlotInfo(
                    slot=slot,
                    exists=True,
                    version=meta.get('version', ''),
                    playtime_seconds=meta.get('playtime_seconds', 0),
                    last_saved=meta.get('last_saved', ''),
                    player_name=player.get('name', 'Unknown'),
                    dragon_name=dragon.get('name', 'No Dragon'),
                    dragon_stage=dragon.get('stage', 'egg'),
                    day_number=world.get('day_number', 1),
                    cafe_level=cafe.get('level', 1)
                ))
            except (IOError, json.JSONDecodeError, KeyError):
                slots.append(SaveSlotInfo(slot=slot, exists=False))

        return slots

    def delete_save(self, slot: int) -> bool:
        """
        Delete a save slot.

        Args:
            slot: Save slot number (1-3)

        Returns:
            True if deleted successfully, False otherwise
        """
        if not self._initialized:
            return False

        if not self._validate_slot(slot):
            return False

        save_path = self._get_save_path(slot)
        if not os.path.exists(save_path):
            return True  # Already doesn't exist

        try:
            os.remove(save_path)
            return True
        except IOError as e:
            print(f"Error deleting slot {slot}: {e}")
            return False

    def has_any_saves(self) -> bool:
        """Check if any save files exist."""
        return any(info.exists for info in self.list_saves())

    def get_most_recent_slot(self) -> Optional[int]:
        """Get the slot number of the most recently saved game."""
        slots = self.list_saves()
        existing = [s for s in slots if s.exists and s.last_saved]
        if not existing:
            return None

        # Sort by last_saved date
        existing.sort(key=lambda s: s.last_saved, reverse=True)
        return existing[0].slot


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_save_manager = None


def get_save_manager() -> SaveManager:
    """Get the global save manager instance."""
    global _save_manager
    if _save_manager is None:
        _save_manager = SaveManager()
    return _save_manager
