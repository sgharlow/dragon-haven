"""
Game State Management for Dragon Haven Cafe.
Handles collection and application of complete game state for save/load.
"""

from typing import Dict, Any
from save_manager import get_save_manager, SaveData

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
from systems.dragon_manager import get_dragon_manager
from systems.achievements import get_achievement_manager

# Note: Dragon is now managed through DragonManager singleton
# Player is still managed per-state


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
        # New Game+ tracking (Phase 4)
        self._ng_plus_level = 0  # Current NG+ level (0 = normal)
        self._ng_plus_unlocked = False  # True after completing Finale
        self._dragon_names_history = []  # Names of dragons from previous runs

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
        cafe_state = cafe_mgr.get_save_state()

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

        # Dragon
        dragon_mgr = get_dragon_manager()
        dragon_state = dragon_mgr.get_state()

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
            'dragon': dragon_state,
            'playtime_seconds': self._playtime_seconds,
            # New Game+ data (Phase 4)
            'ng_plus_level': self._ng_plus_level,
            'ng_plus_unlocked': self._ng_plus_unlocked,
            'dragon_names_history': self._dragon_names_history,
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

        # Dragon
        if 'dragon' in state:
            dragon_mgr = get_dragon_manager()
            dragon_mgr.load_state(state['dragon'])

        # Playtime
        self._playtime_seconds = state.get('playtime_seconds', 0.0)

        # New Game+ data (Phase 4)
        self._ng_plus_level = state.get('ng_plus_level', 0)
        self._ng_plus_unlocked = state.get('ng_plus_unlocked', False)
        self._dragon_names_history = state.get('dragon_names_history', [])

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
        save_data.meta.ng_plus_level = self._ng_plus_level
        save_data.meta.ng_plus_unlocked = self._ng_plus_unlocked

        # Player data
        save_data.player.name = "Player"

        # Dragon data - from dragon manager
        dragon_mgr = get_dragon_manager()
        dragon = dragon_mgr.get_dragon()
        if dragon:
            save_data.dragon.name = dragon.get_name()
            save_data.dragon.stage = dragon.get_stage()
            save_data.dragon.age_days = dragon.get_age_days()
        else:
            save_data.dragon.name = ''
            save_data.dragon.stage = 'egg'
            save_data.dragon.age_days = 0

        # World data
        cafe_state = game_state.get('cafe', {})
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

        # New Game+ data (Phase 4)
        self._ng_plus_level = save_data.meta.ng_plus_level
        self._ng_plus_unlocked = save_data.meta.ng_plus_unlocked

    # =========================================================================
    # NEW GAME+ METHODS (Phase 4)
    # =========================================================================

    def get_ng_plus_level(self) -> int:
        """Get current New Game+ level (0 = normal game)."""
        return self._ng_plus_level

    def is_ng_plus_unlocked(self) -> bool:
        """Check if New Game+ is unlocked (completed Finale)."""
        return self._ng_plus_unlocked

    def check_ng_plus_unlock(self) -> bool:
        """
        Check if NG+ should be unlocked based on story completion.
        Call this after completing story events.
        """
        from constants import NG_PLUS_UNLOCK_CHAPTER
        story_mgr = get_story_manager()
        story_state = story_mgr.get_state()

        # Check if chapter 8 (Finale) is complete
        completed_events = story_state.get('completed_events', [])
        # Look for finale completion event
        if 'finale_end' in completed_events or 'chapter_8_complete' in completed_events:
            self._ng_plus_unlocked = True
            return True

        # Also check current chapter
        current_chapter = story_state.get('current_chapter', 'prologue')
        if current_chapter == 'complete' or story_state.get('game_complete', False):
            self._ng_plus_unlocked = True
            return True

        return self._ng_plus_unlocked

    def get_dragon_names_history(self) -> list:
        """Get list of dragon names from previous playthroughs."""
        return self._dragon_names_history.copy()

    def can_start_ng_plus(self) -> bool:
        """Check if player can start a New Game+."""
        return self._ng_plus_unlocked

    def new_game(self):
        """
        Initialize a new game with default state.
        Resets NG+ level to 0 (normal game).
        """
        from constants import STARTING_GOLD, DEFAULT_UNLOCKED_RECIPES

        # Reset playtime and NG+ (Phase 4)
        self._playtime_seconds = 0.0
        self._ng_plus_level = 0
        # Note: _ng_plus_unlocked is NOT reset - once unlocked, always available
        # Note: _dragon_names_history is NOT reset - cumulative across all games

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

        # Create fresh dragon
        dragon_mgr = get_dragon_manager()
        dragon_mgr.create_dragon()

    def new_game_plus(self) -> bool:
        """
        Start a New Game+ with carryover from current save.

        Carries over:
        - Unlocked recipes
        - Mastered recipes
        - Achievements
        - Dragon names history
        - Character affinity (50%)
        - Total playtime (cumulative)

        Resets with bonuses:
        - New dragon (egg)
        - Gold: Starting + 500 bonus
        - Reputation: 50 (starting boost)
        - Story: Back to prologue
        - Inventory items: Cleared
        - Zones: Reset to initial

        Returns:
            True if NG+ started successfully, False if not unlocked
        """
        if not self._ng_plus_unlocked:
            return False

        from constants import (
            STARTING_GOLD, DEFAULT_UNLOCKED_RECIPES,
            NG_PLUS_STARTING_GOLD_BONUS, NG_PLUS_STARTING_REPUTATION,
            NG_PLUS_AFFINITY_RETENTION
        )

        # === CAPTURE CARRYOVER DATA ===

        # Recipes: Keep all unlocked and mastery
        recipe_mgr = get_recipe_manager()
        recipe_state = recipe_mgr.get_state()
        carryover_recipes = recipe_state.get('unlocked', [])
        carryover_mastery = recipe_state.get('mastery', {})

        # Achievements: Keep all unlocked
        achievement_mgr = get_achievement_manager()
        # Achievements don't reset - they're cumulative

        # Character affinity: Keep 50%
        char_mgr = get_character_manager()
        char_state = char_mgr.get_state()
        carryover_affinity = {}
        for char_id, char_data in char_state.get('characters', {}).items():
            original_affinity = char_data.get('affinity', 0)
            retained_affinity = int(original_affinity * NG_PLUS_AFFINITY_RETENTION)
            carryover_affinity[char_id] = {
                'affinity': retained_affinity,
                'met': char_data.get('met', False),
            }

        # Dragon name: Add to history
        dragon_mgr = get_dragon_manager()
        dragon = dragon_mgr.get_dragon()
        if dragon:
            dragon_name = dragon.get_name()
            if dragon_name and dragon_name not in self._dragon_names_history:
                self._dragon_names_history.append(dragon_name)

        # Playtime: Keep cumulative
        total_playtime = self._playtime_seconds

        # === INCREMENT NG+ LEVEL ===
        self._ng_plus_level += 1

        # === RESET GAME STATE ===

        # Time system starts at Day 1, 8:00 AM
        time_mgr = get_time_manager()
        time_mgr.load_state({
            'current_day': 1,
            'current_hour': 8.0,
            'current_season_index': 0,
            'time_scale': 1.0,
        })

        # Inventory: Starting gold + NG+ bonus, with carryover recipes
        inventory = get_inventory()
        ng_plus_gold = STARTING_GOLD + NG_PLUS_STARTING_GOLD_BONUS
        inventory.load_state({
            'gold': ng_plus_gold,
            'unlocked_recipes': carryover_recipes,
            'mastered_recipes': carryover_mastery,
        })

        # Cafe: Starting reputation boost
        cafe_mgr = get_cafe_manager()
        cafe_mgr.load_state({
            'reputation': NG_PLUS_STARTING_REPUTATION,
            'cafe_level': 1,
        })

        # Story: Reset to prologue
        story_mgr = get_story_manager()
        story_mgr.load_state({
            'current_chapter': 'prologue',
            'completed_events': [],
            'flags': {},
        })

        # World: Reset to cafe_grounds
        world_mgr = get_world_manager()
        world_mgr.load_state({
            'current_zone': 'cafe_grounds',
        })

        # Characters: Apply carryover affinity
        char_mgr.load_state({
            'characters': carryover_affinity,
        })

        # Create fresh dragon (new egg)
        dragon_mgr.create_dragon()

        # Restore cumulative playtime
        self._playtime_seconds = total_playtime

        return True

    def get_ng_plus_modifier(self, modifier_name: str) -> float:
        """
        Get the current NG+ modifier value for a given system.

        Modifiers scale with NG+ level using:
        base_modifier * (scaling ^ (ng_plus_level - 1))

        Args:
            modifier_name: One of 'customer_expectations', 'service_time',
                          'resource_scarcity', 'gold_bonus', 'reputation_decay'

        Returns:
            Modifier value (1.0 = no change, >1.0 = increase, <1.0 = decrease)
        """
        from constants import NG_PLUS_MODIFIERS, NG_PLUS_SCALING_PER_CYCLE

        if self._ng_plus_level == 0:
            return 1.0  # No modifiers in normal game

        base = NG_PLUS_MODIFIERS.get(modifier_name, 1.0)
        scaling = NG_PLUS_SCALING_PER_CYCLE.get(modifier_name, 1.0)

        # Apply scaling for each NG+ level beyond 1
        if self._ng_plus_level > 1:
            for _ in range(self._ng_plus_level - 1):
                base *= scaling

        return base

    def get_all_ng_plus_modifiers(self) -> Dict[str, float]:
        """
        Get all current NG+ modifiers.

        Returns:
            Dict mapping modifier names to their current values
        """
        from constants import NG_PLUS_MODIFIERS

        if self._ng_plus_level == 0:
            return {name: 1.0 for name in NG_PLUS_MODIFIERS}

        return {
            name: self.get_ng_plus_modifier(name)
            for name in NG_PLUS_MODIFIERS
        }

    def get_ng_plus_carryover_summary(self) -> Dict[str, Any]:
        """
        Get a summary of what will carry over to NG+.
        Useful for displaying to player before starting NG+.
        """
        recipe_mgr = get_recipe_manager()
        recipe_state = recipe_mgr.get_state()

        char_mgr = get_character_manager()
        char_state = char_mgr.get_state()

        achievement_mgr = get_achievement_manager()

        dragon_mgr = get_dragon_manager()
        dragon = dragon_mgr.get_dragon()

        return {
            'ng_plus_level': self._ng_plus_level + 1,  # What it will become
            'recipes_unlocked': len(recipe_state.get('unlocked', [])),
            'recipes_mastered': len(recipe_state.get('mastery', {})),
            'characters_met': sum(
                1 for c in char_state.get('characters', {}).values()
                if c.get('met', False)
            ),
            'achievements_unlocked': len(achievement_mgr._unlocked),
            'dragon_name': dragon.get_name() if dragon else None,
            'dragon_names_history': self._dragon_names_history.copy(),
            'total_playtime': self._playtime_seconds,
        }


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
