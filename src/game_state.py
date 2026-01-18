"""
Game State Management for Dragon Haven Cafe.
Handles collection and application of complete game state for save/load.
"""

from typing import Dict, Any, Optional
from save_manager import get_save_manager, SaveData, SaveMeta

# Import all systems with state
from systems.time_system import get_time_manager
from systems.inventory import get_inventory
from systems.world import get_world_manager
from systems.resources import get_resource_manager
from systems.economy import get_economy
from systems.recipes import get_recipe_manager
from systems.cafe import get_cafe_manager
from systems.dialogue import get_dialogue_manager
from systems.story import get_story_manager
from entities.story_character import get_character_manager

# Note: Dragon and Player are managed per-state, not global singletons
# They'll be accessed through the active gameplay state when needed


class GameStateManager:
    """
    Manages complete game state collection and restoration.

    Aggregates state from all game systems into a unified format
    compatible with SaveManager.

    Usage:
        state_mgr = get_game_state_manager()
        state_mgr.save_game(slot=1)
        state_mgr.load_game(slot=1)
    """

    AUTOSAVE_SLOT = 1  # Use slot 1 for auto-saves

    def __init__(self):
        """Initialize the game state manager."""
        self._playtime_seconds = 0.0
        self._save_manager = get_save_manager()
        self._autosave_enabled = False

    def update_playtime(self, dt: float):
        """Update playtime counter (call each frame)."""
        self._playtime_seconds += dt

    def get_playtime(self) -> float:
        """Get total playtime in seconds."""
        return self._playtime_seconds

    def enable_autosave(self):
        """Enable auto-save at end of each day."""
        if self._autosave_enabled:
            return

        time_mgr = get_time_manager()
        time_mgr.on_new_day(self._on_new_day_autosave)
        self._autosave_enabled = True

    def _on_new_day_autosave(self, day_number: int):
        """Auto-save callback triggered at the start of each new day."""
        # Save to autosave slot
        if self.save_game(self.AUTOSAVE_SLOT):
            print(f"Auto-saved on Day {day_number}")
        else:
            print(f"Warning: Auto-save failed on Day {day_number}")

    def collect_game_state(self) -> Dict[str, Any]:
        """
        Collect complete game state from all systems.

        Returns:
            Dictionary containing all game state
        """
        # Time system
        time_mgr = get_time_manager()
        time_state = time_mgr.get_state()

        # Inventory (includes gold, recipes)
        inventory = get_inventory()
        inventory_state = inventory.get_state()

        # World and resources
        world_mgr = get_world_manager()
        resource_mgr = get_resource_manager()
        world_state = world_mgr.get_state()
        resource_state = resource_mgr.get_state()

        # Economy
        economy = get_economy()
        economy_state = economy.get_state()

        # Cafe
        cafe_mgr = get_cafe_manager()
        cafe_state = cafe_mgr.get_state()

        # Story and characters
        story_mgr = get_story_manager()
        char_mgr = get_character_manager()
        dialogue_mgr = get_dialogue_manager()
        story_state = story_mgr.get_state()
        character_state = char_mgr.get_state()
        dialogue_state = dialogue_mgr.get_state()

        # Recipes
        recipe_mgr = get_recipe_manager()
        recipe_state = recipe_mgr.get_state()

        return {
            'time': time_state,
            'inventory': inventory_state,
            'world': world_state,
            'resources': resource_state,
            'economy': economy_state,
            'cafe': cafe_state,
            'story': story_state,
            'characters': character_state,
            'dialogue': dialogue_state,
            'recipes': recipe_state,
            'playtime_seconds': self._playtime_seconds,
        }

    def apply_game_state(self, state: Dict[str, Any]):
        """
        Apply loaded game state to all systems.

        Args:
            state: Dictionary containing all game state
        """
        # Time system
        if 'time' in state:
            time_mgr = get_time_manager()
            time_mgr.load_state(state['time'])

        # Inventory
        if 'inventory' in state:
            inventory = get_inventory()
            inventory.load_state(state['inventory'])

        # World and resources
        if 'world' in state:
            world_mgr = get_world_manager()
            world_mgr.load_state(state['world'])

        if 'resources' in state:
            resource_mgr = get_resource_manager()
            resource_mgr.load_state(state['resources'])

        # Economy
        if 'economy' in state:
            economy = get_economy()
            economy.load_state(state['economy'])

        # Cafe
        if 'cafe' in state:
            cafe_mgr = get_cafe_manager()
            cafe_mgr.load_state(state['cafe'])

        # Story and characters
        if 'story' in state:
            story_mgr = get_story_manager()
            story_mgr.load_state(state['story'])

        if 'characters' in state:
            char_mgr = get_character_manager()
            char_mgr.load_state(state['characters'])

        if 'dialogue' in state:
            dialogue_mgr = get_dialogue_manager()
            dialogue_mgr.load_state(state['dialogue'])

        # Recipes
        if 'recipes' in state:
            recipe_mgr = get_recipe_manager()
            recipe_mgr.load_state(state['recipes'])

        # Playtime
        self._playtime_seconds = state.get('playtime_seconds', 0.0)

    def save_game(self, slot: int) -> bool:
        """
        Save current game state to a slot.

        Args:
            slot: Save slot number (1-3)

        Returns:
            True if save successful
        """
        # Collect all state
        game_state = self.collect_game_state()

        # Create SaveData with the collected state
        save_data = SaveData()

        # Meta info
        time_mgr = get_time_manager()
        cafe_mgr = get_cafe_manager()

        save_data.meta.playtime_seconds = self._playtime_seconds

        # Player data
        save_data.player.name = "Player"

        # Dragon data - from cafe manager's dragon info
        cafe_state = game_state.get('cafe', {})
        save_data.dragon.name = cafe_state.get('dragon_name', '')
        save_data.dragon.stage = cafe_state.get('dragon_stage', 'egg')
        save_data.dragon.age_days = 0

        # World data
        world_state = game_state.get('world', {})
        save_data.world.current_zone = world_state.get('current_zone', 'cafe_grounds')
        save_data.world.day_number = time_mgr.get_current_day()
        save_data.world.current_time = time_mgr.get_current_hour()

        # Cafe data
        inventory = get_inventory()
        save_data.cafe.gold = inventory.gold
        save_data.cafe.reputation = cafe_state.get('reputation', 0)
        save_data.cafe.level = cafe_state.get('cafe_level', 1)

        # Story data
        story_state = game_state.get('story', {})
        save_data.story.events_completed = story_state.get('completed_events', [])
        save_data.story.dialogue_flags = story_state.get('flags', {})

        # Save using the save manager
        return self._save_manager.save(slot, save_data)

    def load_game(self, slot: int) -> bool:
        """
        Load game state from a slot.

        Args:
            slot: Save slot number (1-3)

        Returns:
            True if load successful
        """
        save_data = self._save_manager.load(slot)
        if not save_data:
            return False

        # Convert to dict and check for full game state
        save_dict = save_data.to_dict()

        # If we have full game state, use it for complete restoration
        if 'full_game_state' in save_dict:
            self.apply_game_state(save_dict['full_game_state'])
        else:
            # Fall back to basic restoration from save data fields
            self._apply_basic_state(save_data)

        return True

    def _apply_basic_state(self, save_data: SaveData):
        """
        Apply basic state from SaveData fields (fallback).

        Args:
            save_data: SaveData instance
        """
        # Time
        time_mgr = get_time_manager()
        time_mgr.load_state({
            'current_day': save_data.world.day_number,
            'current_hour': save_data.world.current_time,
        })

        # Inventory/economy
        inventory = get_inventory()
        inventory.gold = save_data.cafe.gold

        # Cafe reputation
        cafe_mgr = get_cafe_manager()
        cafe_mgr.load_state({
            'reputation': save_data.cafe.reputation,
            'cafe_level': save_data.cafe.level,
        })

        # Story
        story_mgr = get_story_manager()
        story_mgr.load_state({
            'completed_events': save_data.story.events_completed,
            'flags': save_data.story.dialogue_flags,
        })

        # Playtime
        self._playtime_seconds = save_data.meta.playtime_seconds

    def new_game(self):
        """
        Initialize a new game with default state.
        """
        from constants import STARTING_GOLD, DEFAULT_UNLOCKED_RECIPES

        # Reset playtime
        self._playtime_seconds = 0.0

        # Time system starts at Day 1, 8:00 AM
        time_mgr = get_time_manager()
        time_mgr.load_state({
            'current_day': 1,
            'current_hour': 8.0,
            'current_season_index': 0,
            'time_scale': 1.0,
        })

        # Fresh inventory with starting gold
        inventory = get_inventory()
        inventory.load_state({
            'gold': STARTING_GOLD,
            'unlocked_recipes': list(DEFAULT_UNLOCKED_RECIPES),
            'mastered_recipes': {},
        })

        # Reset cafe
        cafe_mgr = get_cafe_manager()
        cafe_mgr.load_state({
            'reputation': 0,
            'cafe_level': 1,
        })

        # Fresh story
        story_mgr = get_story_manager()
        story_mgr.load_state({
            'current_chapter': 'prologue',
            'completed_events': [],
            'flags': {},
        })

        # Reset world
        world_mgr = get_world_manager()
        world_mgr.load_state({
            'current_zone': 'cafe_grounds',
        })

        # Reset characters
        char_mgr = get_character_manager()
        char_mgr.load_state({
            'characters': {},
        })


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_game_state_manager = None


def get_game_state_manager() -> GameStateManager:
    """Get the global game state manager instance."""
    global _game_state_manager
    if _game_state_manager is None:
        _game_state_manager = GameStateManager()
    return _game_state_manager
