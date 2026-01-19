"""
Story Character System for Dragon Haven Cafe.
Manages story characters, relationships, and affinity tracking.
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

from constants import (
    AFFINITY_MIN, AFFINITY_MAX,
    AFFINITY_LEVEL_ACQUAINTANCE, AFFINITY_LEVEL_FRIENDLY,
    AFFINITY_LEVEL_CLOSE, AFFINITY_LEVEL_BEST_FRIEND,
    AFFINITY_LEVELS,
    AFFINITY_COOK_BASE, AFFINITY_COOK_QUALITY_BONUS,
    AFFINITY_COOK_FAVORITE, AFFINITY_COOK_LIKED, AFFINITY_COOK_DISLIKED,
    AFFINITY_UNLOCK_PERSONAL_STORY, AFFINITY_UNLOCK_SECRET_RECIPE,
    AFFINITY_UNLOCK_SPECIAL_EVENT,
    CHARACTER_SECRET_RECIPES,
)


@dataclass
class StoryCharacter:
    """
    A story character with relationship tracking.

    Attributes:
        id: Unique identifier
        name: Display name
        portrait_id: ID for portrait display
        description: Character description
        chapter: Chapter they appear in
        affinity: Current affinity value (0-100)
        favorite_recipes: List of recipe IDs they love
        liked_recipes: List of recipe IDs they like
        disliked_recipes: List of recipe IDs they dislike
        gift_preferences: Dict of item_id to affinity bonus
        unlocked_dialogues: List of dialogue IDs unlocked by affinity
        met: Whether the player has met this character
    """
    id: str
    name: str
    portrait_id: str = ""
    description: str = ""
    chapter: str = "prologue"
    affinity: int = 0
    favorite_recipes: List[str] = field(default_factory=list)
    liked_recipes: List[str] = field(default_factory=list)
    disliked_recipes: List[str] = field(default_factory=list)
    gift_preferences: Dict[str, int] = field(default_factory=dict)
    unlocked_dialogues: Dict[str, int] = field(default_factory=dict)  # dialogue_id: affinity_required
    met: bool = False

    def get_affinity_level(self) -> str:
        """Get the affinity level as a string."""
        for level_id, level_data in AFFINITY_LEVELS.items():
            if level_data['min'] <= self.affinity <= level_data['max']:
                return level_id
        return AFFINITY_LEVEL_ACQUAINTANCE

    def get_affinity_level_name(self) -> str:
        """Get the affinity level display name."""
        level = self.get_affinity_level()
        return AFFINITY_LEVELS.get(level, {}).get('name', 'Unknown')

    def get_affinity_percent(self) -> float:
        """Get affinity as a percentage (0.0-1.0)."""
        return self.affinity / 100.0

    def add_affinity(self, amount: int) -> int:
        """
        Add affinity points.

        Args:
            amount: Points to add (can be negative)

        Returns:
            New affinity value
        """
        self.affinity = max(AFFINITY_MIN, min(AFFINITY_MAX, self.affinity + amount))
        return self.affinity

    def get_recipe_reaction(self, recipe_id: str) -> str:
        """
        Get reaction to a cooked recipe.

        Returns:
            'favorite', 'liked', 'disliked', or 'neutral'
        """
        if recipe_id in self.favorite_recipes:
            return 'favorite'
        elif recipe_id in self.liked_recipes:
            return 'liked'
        elif recipe_id in self.disliked_recipes:
            return 'disliked'
        return 'neutral'

    def get_cook_affinity_bonus(self, recipe_id: str, quality: int = 3) -> int:
        """
        Calculate affinity bonus for cooking a recipe.

        Args:
            recipe_id: ID of cooked recipe
            quality: Quality of the dish (1-5)

        Returns:
            Affinity points earned
        """
        reaction = self.get_recipe_reaction(recipe_id)

        # Base amounts from constants
        if reaction == 'favorite':
            base = AFFINITY_COOK_FAVORITE
        elif reaction == 'liked':
            base = AFFINITY_COOK_LIKED
        elif reaction == 'disliked':
            base = AFFINITY_COOK_DISLIKED
        else:
            base = AFFINITY_COOK_BASE

        # Quality bonus for high quality (4-5 stars)
        quality_bonus = AFFINITY_COOK_QUALITY_BONUS if quality >= 4 else 0

        return base + quality_bonus

    def get_gift_affinity_bonus(self, item_id: str) -> int:
        """
        Get affinity bonus for giving a gift.

        Args:
            item_id: ID of the item being gifted

        Returns:
            Affinity points earned
        """
        return self.gift_preferences.get(item_id, 2)  # Default +2 for any gift

    def get_available_dialogues(self) -> List[str]:
        """Get list of dialogues unlocked by current affinity."""
        return [
            dialogue_id for dialogue_id, required in self.unlocked_dialogues.items()
            if self.affinity >= required
        ]

    def can_unlock_personal_story(self) -> bool:
        """Check if personal stories are unlocked (Friendly level)."""
        return self.affinity >= AFFINITY_UNLOCK_PERSONAL_STORY

    def can_unlock_secret_recipe(self) -> bool:
        """Check if secret recipe is unlocked (Close level)."""
        return self.affinity >= AFFINITY_UNLOCK_SECRET_RECIPE

    def can_unlock_special_event(self) -> bool:
        """Check if special events are unlocked (Best Friend level)."""
        return self.affinity >= AFFINITY_UNLOCK_SPECIAL_EVENT

    def get_secret_recipe(self) -> Optional[str]:
        """Get the character's secret recipe ID if unlocked."""
        if self.can_unlock_secret_recipe():
            return CHARACTER_SECRET_RECIPES.get(self.id)
        return None

    def mark_met(self):
        """Mark that the player has met this character."""
        self.met = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for saving."""
        return {
            'id': self.id,
            'name': self.name,
            'portrait_id': self.portrait_id,
            'description': self.description,
            'chapter': self.chapter,
            'affinity': self.affinity,
            'favorite_recipes': self.favorite_recipes,
            'liked_recipes': self.liked_recipes,
            'disliked_recipes': self.disliked_recipes,
            'gift_preferences': self.gift_preferences,
            'unlocked_dialogues': self.unlocked_dialogues,
            'met': self.met,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StoryCharacter':
        """Create from dict."""
        return cls(
            id=data['id'],
            name=data.get('name', ''),
            portrait_id=data.get('portrait_id', ''),
            description=data.get('description', ''),
            chapter=data.get('chapter', 'prologue'),
            affinity=data.get('affinity', 0),
            favorite_recipes=data.get('favorite_recipes', []),
            liked_recipes=data.get('liked_recipes', []),
            disliked_recipes=data.get('disliked_recipes', []),
            gift_preferences=data.get('gift_preferences', {}),
            unlocked_dialogues=data.get('unlocked_dialogues', {}),
            met=data.get('met', False),
        )


class CharacterManager:
    """
    Manages all story characters and relationships.

    Usage:
        manager = get_character_manager()
        manager.load_characters_from_directory('data/characters/')

        # When cooking for a character
        bonus = manager.record_cook('marcus', 'herbed_bread', quality=4)

        # Check relationship level
        level = manager.get_affinity_level('marcus')
    """

    def __init__(self):
        """Initialize the character manager."""
        self._characters: Dict[str, StoryCharacter] = {}

    def load_character(self, character: StoryCharacter):
        """Load a character into the manager."""
        self._characters[character.id] = character

    def load_character_dict(self, data: Dict[str, Any]):
        """Load a character from dict data."""
        character = StoryCharacter.from_dict(data)
        self.load_character(character)

    def load_characters_file(self, filepath: str) -> int:
        """
        Load characters from a JSON file.

        Returns:
            Number of characters loaded
        """
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Character file not found: {filepath}")
                return 0

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            count = 0
            if isinstance(data, list):
                for char_data in data:
                    self.load_character_dict(char_data)
                    count += 1
            else:
                self.load_character_dict(data)
                count = 1

            return count
        except Exception as e:
            print(f"Error loading characters: {e}")
            return 0

    def load_characters_from_directory(self, directory: str) -> int:
        """
        Load all character files from a directory.

        Returns:
            Total characters loaded
        """
        count = 0
        path = Path(directory)
        if not path.exists():
            return 0

        for file in path.glob('*.json'):
            count += self.load_characters_file(str(file))

        return count

    def get_character(self, character_id: str) -> Optional[StoryCharacter]:
        """Get a character by ID."""
        return self._characters.get(character_id)

    def get_all_characters(self) -> List[StoryCharacter]:
        """Get all characters."""
        return list(self._characters.values())

    def get_characters_by_chapter(self, chapter: str) -> List[StoryCharacter]:
        """Get characters that appear in a chapter."""
        return [c for c in self._characters.values() if c.chapter == chapter]

    def get_met_characters(self) -> List[StoryCharacter]:
        """Get all characters the player has met."""
        return [c for c in self._characters.values() if c.met]

    # =========================================================================
    # AFFINITY INTERACTIONS
    # =========================================================================

    def record_cook(self, character_id: str, recipe_id: str, quality: int = 3) -> int:
        """
        Record cooking a dish for a character.

        Args:
            character_id: Target character
            recipe_id: Recipe that was cooked
            quality: Quality of the dish (1-5)

        Returns:
            Affinity points earned
        """
        character = self.get_character(character_id)
        if not character:
            return 0

        bonus = character.get_cook_affinity_bonus(recipe_id, quality)
        character.add_affinity(bonus)
        return bonus

    def record_gift(self, character_id: str, item_id: str) -> int:
        """
        Record giving a gift to a character.

        Args:
            character_id: Target character
            item_id: Item being gifted

        Returns:
            Affinity points earned
        """
        character = self.get_character(character_id)
        if not character:
            return 0

        bonus = character.get_gift_affinity_bonus(item_id)
        character.add_affinity(bonus)
        return bonus

    def record_dialogue_choice(self, character_id: str, choice_affinity: int) -> int:
        """
        Record a dialogue choice affecting affinity.

        Args:
            character_id: Target character
            choice_affinity: Points from the choice

        Returns:
            New affinity value
        """
        character = self.get_character(character_id)
        if not character:
            return 0

        return character.add_affinity(choice_affinity)

    def meet_character(self, character_id: str) -> bool:
        """
        Mark a character as met.

        Returns:
            True if character exists
        """
        character = self.get_character(character_id)
        if character:
            character.mark_met()
            return True
        return False

    # =========================================================================
    # QUERIES
    # =========================================================================

    def get_affinity(self, character_id: str) -> int:
        """Get affinity value for a character."""
        character = self.get_character(character_id)
        return character.affinity if character else 0

    def get_affinity_level(self, character_id: str) -> str:
        """Get affinity level string for a character."""
        character = self.get_character(character_id)
        return character.get_affinity_level() if character else "low"

    def get_available_dialogues(self, character_id: str) -> List[str]:
        """Get dialogues unlocked by current affinity."""
        character = self.get_character(character_id)
        return character.get_available_dialogues() if character else []

    def get_relationship_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of all relationships."""
        return {
            char.id: {
                'name': char.name,
                'met': char.met,
                'affinity': char.affinity,
                'level': char.get_affinity_level(),
            }
            for char in self._characters.values()
        }

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'characters': {
                char_id: {
                    'affinity': char.affinity,
                    'met': char.met,
                }
                for char_id, char in self._characters.items()
            }
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        for char_id, char_state in state.get('characters', {}).items():
            character = self.get_character(char_id)
            if character:
                character.affinity = char_state.get('affinity', 0)
                character.met = char_state.get('met', False)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_character_manager: Optional[CharacterManager] = None


def get_character_manager() -> CharacterManager:
    """Get the global character manager instance."""
    global _character_manager
    if _character_manager is None:
        _character_manager = CharacterManager()
    return _character_manager


def reset_character_manager():
    """Reset the character manager (for new game)."""
    global _character_manager
    _character_manager = CharacterManager()
