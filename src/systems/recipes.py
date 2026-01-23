"""
Recipe System for Dragon Haven Cafe.
Manages recipes, cooking requirements, and mastery progression.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from constants import (
    RECIPES, DEFAULT_UNLOCKED_RECIPES, ALL_RECIPE_CATEGORIES,
    RECIPE_CATEGORY_APPETIZER, RECIPE_CATEGORY_MAIN,
    RECIPE_CATEGORY_DESSERT, RECIPE_CATEGORY_BEVERAGE,
    RECIPE_BASE_QUALITY, RECIPE_MASTERY_COOK_COUNT, RECIPE_MASTERY_PERFECT_COUNT,
    UNLOCK_TYPE_DEFAULT, UNLOCK_TYPE_REPUTATION,
    UNLOCK_TYPE_STORY, UNLOCK_TYPE_DISCOVERY, UNLOCK_TYPE_SEASONAL,
    QUALITY_MIN, QUALITY_MAX,
)


@dataclass
class IngredientRequirement:
    """
    Represents an ingredient requirement for a recipe.
    """
    item_id: str       # ID of the ingredient
    quantity: int      # How many needed
    quality_min: int   # Minimum quality required (1-5)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'item_id': self.item_id,
            'quantity': self.quantity,
            'quality_min': self.quality_min,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IngredientRequirement':
        return cls(
            item_id=data['item_id'],
            quantity=data['quantity'],
            quality_min=data.get('quality_min', 1),
        )

    @classmethod
    def from_tuple(cls, data: Tuple[str, int, int]) -> 'IngredientRequirement':
        """Create from tuple format: (item_id, quantity, quality_min)"""
        return cls(
            item_id=data[0],
            quantity=data[1],
            quality_min=data[2] if len(data) > 2 else 1,
        )


@dataclass
class Recipe:
    """
    Represents a recipe that can be cooked in the cafe.
    """
    id: str
    name: str
    description: str
    category: str
    difficulty: int                              # 1-5 stars
    base_price: int
    ingredients: List[IngredientRequirement]
    color_influence: Tuple[float, float, float]  # RGB modifiers for dragon
    unlock_type: str = UNLOCK_TYPE_DEFAULT
    unlock_requirement: Any = None               # e.g., reputation level or story chapter

    def get_base_quality(self) -> int:
        """Get the base quality for this recipe based on difficulty."""
        return RECIPE_BASE_QUALITY.get(self.difficulty, 3)

    def get_ingredient_ids(self) -> List[str]:
        """Get list of all ingredient IDs needed."""
        return [ing.item_id for ing in self.ingredients]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'base_price': self.base_price,
            'ingredients': [ing.to_dict() for ing in self.ingredients],
            'color_influence': self.color_influence,
            'unlock_type': self.unlock_type,
            'unlock_requirement': self.unlock_requirement,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recipe':
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            category=data['category'],
            difficulty=data.get('difficulty', 1),
            base_price=data.get('base_price', 10),
            ingredients=[IngredientRequirement.from_dict(ing) for ing in data['ingredients']],
            color_influence=tuple(data.get('color_influence', (0.5, 0.5, 0.5))),
            unlock_type=data.get('unlock_type', UNLOCK_TYPE_DEFAULT),
            unlock_requirement=data.get('unlock_requirement'),
        )

    @classmethod
    def from_definition(cls, recipe_id: str, data: Dict[str, Any]) -> 'Recipe':
        """Create a Recipe from the RECIPES constant format."""
        unlock_data = data.get('unlock', {'type': UNLOCK_TYPE_DEFAULT})
        # Handle requirement field - could be 'requirement' or 'event' for seasonal
        unlock_req = unlock_data.get('requirement') or unlock_data.get('event')
        return cls(
            id=recipe_id,
            name=data['name'],
            description=data.get('description', ''),
            category=data['category'],
            difficulty=data.get('difficulty', 1),
            base_price=data.get('base_price', 10),
            ingredients=[
                IngredientRequirement.from_tuple(ing)
                for ing in data.get('ingredients', [])
            ],
            color_influence=tuple(data.get('color_influence', (0.5, 0.5, 0.5))),
            unlock_type=unlock_data.get('type', UNLOCK_TYPE_DEFAULT),
            unlock_requirement=unlock_req,
        )


@dataclass
class RecipeMastery:
    """
    Tracks mastery progress for a single recipe.
    """
    recipe_id: str
    cook_count: int = 0         # Total times cooked
    perfect_count: int = 0      # Times cooked with 5-star quality
    is_mastered: bool = False   # True when fully mastered

    def record_cook(self, quality: int) -> bool:
        """
        Record a cook and check for mastery.

        Args:
            quality: Quality of the cooked dish (1-5)

        Returns:
            True if this cook achieved mastery
        """
        self.cook_count += 1
        if quality >= QUALITY_MAX:
            self.perfect_count += 1

        # Check mastery conditions
        if not self.is_mastered:
            if (self.cook_count >= RECIPE_MASTERY_COOK_COUNT and
                    self.perfect_count >= RECIPE_MASTERY_PERFECT_COUNT):
                self.is_mastered = True
                return True
        return False

    def get_progress(self) -> Dict[str, Any]:
        """Get mastery progress as percentages."""
        cook_progress = min(100, (self.cook_count / RECIPE_MASTERY_COOK_COUNT) * 100)
        perfect_progress = min(100, (self.perfect_count / RECIPE_MASTERY_PERFECT_COUNT) * 100)
        return {
            'cook_count': self.cook_count,
            'cook_required': RECIPE_MASTERY_COOK_COUNT,
            'cook_progress': cook_progress,
            'perfect_count': self.perfect_count,
            'perfect_required': RECIPE_MASTERY_PERFECT_COUNT,
            'perfect_progress': perfect_progress,
            'is_mastered': self.is_mastered,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            'recipe_id': self.recipe_id,
            'cook_count': self.cook_count,
            'perfect_count': self.perfect_count,
            'is_mastered': self.is_mastered,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RecipeMastery':
        return cls(
            recipe_id=data['recipe_id'],
            cook_count=data.get('cook_count', 0),
            perfect_count=data.get('perfect_count', 0),
            is_mastered=data.get('is_mastered', False),
        )


class RecipeManager:
    """
    Manages all recipes, unlocks, and mastery tracking.
    """

    def __init__(self):
        """Initialize the recipe manager."""
        # Load all recipes from definitions
        self._recipes: Dict[str, Recipe] = {}
        for recipe_id, data in RECIPES.items():
            self._recipes[recipe_id] = Recipe.from_definition(recipe_id, data)

        # Track unlocked recipes
        self._unlocked: List[str] = list(DEFAULT_UNLOCKED_RECIPES)

        # Track mastery for each unlocked recipe
        self._mastery: Dict[str, RecipeMastery] = {}

        # Track discovered (but not yet unlocked) recipes
        self._discovered: List[str] = []

        # Story progress tracking (set externally)
        self._story_progress: List[str] = []

    # =========================================================================
    # RECIPE ACCESS
    # =========================================================================

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        """Get a recipe by ID."""
        return self._recipes.get(recipe_id)

    def get_all_recipes(self) -> List[Recipe]:
        """Get all recipes in the game."""
        return list(self._recipes.values())

    def get_recipes_by_category(self, category: str) -> List[Recipe]:
        """Get all recipes in a category."""
        return [r for r in self._recipes.values() if r.category == category]

    def get_unlocked_recipes(self) -> List[Recipe]:
        """Get all unlocked recipes."""
        return [self._recipes[rid] for rid in self._unlocked if rid in self._recipes]

    def get_unlocked_by_category(self, category: str) -> List[Recipe]:
        """Get unlocked recipes in a category."""
        return [r for r in self.get_unlocked_recipes() if r.category == category]

    def is_unlocked(self, recipe_id: str) -> bool:
        """Check if a recipe is unlocked."""
        return recipe_id in self._unlocked

    # =========================================================================
    # COOKING CHECKS
    # =========================================================================

    def can_cook(self, recipe_id: str, inventory) -> Dict[str, Any]:
        """
        Check if a recipe can be cooked with current inventory.

        Args:
            recipe_id: Recipe to check
            inventory: Inventory instance to check against

        Returns:
            Dict with 'can_cook', 'missing_ingredients', 'quality_issues'
        """
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return {'can_cook': False, 'error': 'Recipe not found'}

        if not self.is_unlocked(recipe_id):
            return {'can_cook': False, 'error': 'Recipe not unlocked'}

        missing = []
        quality_issues = []

        for ing in recipe.ingredients:
            count = inventory.get_count(ing.item_id, check_all=True)
            if count < ing.quantity:
                missing.append({
                    'item_id': ing.item_id,
                    'needed': ing.quantity,
                    'have': count,
                })
            # Note: Quality check would require examining individual items
            # For now, we assume any item can be used

        can_cook = len(missing) == 0
        return {
            'can_cook': can_cook,
            'missing_ingredients': missing,
            'quality_issues': quality_issues,
        }

    def get_available_recipes(self, inventory) -> List[Recipe]:
        """
        Get all recipes that can currently be cooked.

        Args:
            inventory: Inventory instance to check against

        Returns:
            List of cookable recipes
        """
        available = []
        for recipe_id in self._unlocked:
            result = self.can_cook(recipe_id, inventory)
            if result.get('can_cook', False):
                available.append(self._recipes[recipe_id])
        return available

    def get_available_by_category(self, category: str, inventory) -> List[Recipe]:
        """Get available recipes in a category."""
        return [r for r in self.get_available_recipes(inventory) if r.category == category]

    # =========================================================================
    # UNLOCKING
    # =========================================================================

    def unlock_recipe(self, recipe_id: str) -> bool:
        """
        Unlock a recipe.

        Returns:
            True if newly unlocked, False if already unlocked or doesn't exist
        """
        if recipe_id not in self._recipes:
            return False
        if recipe_id in self._unlocked:
            return False

        self._unlocked.append(recipe_id)
        # Remove from discovered if it was there
        if recipe_id in self._discovered:
            self._discovered.remove(recipe_id)
        return True

    def discover_recipe(self, recipe_id: str) -> bool:
        """
        Discover a recipe (mark as found but not unlocked).
        Used for discovery-type unlocks.

        Returns:
            True if newly discovered
        """
        if recipe_id not in self._recipes:
            return False
        if recipe_id in self._unlocked or recipe_id in self._discovered:
            return False

        recipe = self._recipes[recipe_id]
        if recipe.unlock_type == UNLOCK_TYPE_DISCOVERY:
            self._discovered.append(recipe_id)
            # Auto-unlock discovery recipes when discovered
            self.unlock_recipe(recipe_id)
            return True
        return False

    def check_unlock_conditions(self, reputation: int = 0) -> List[str]:
        """
        Check for recipes that can be unlocked based on current conditions.

        Args:
            reputation: Current reputation level

        Returns:
            List of newly unlocked recipe IDs
        """
        newly_unlocked = []

        for recipe_id, recipe in self._recipes.items():
            if recipe_id in self._unlocked:
                continue

            should_unlock = False

            if recipe.unlock_type == UNLOCK_TYPE_REPUTATION:
                if reputation >= (recipe.unlock_requirement or 0):
                    should_unlock = True

            elif recipe.unlock_type == UNLOCK_TYPE_STORY:
                if recipe.unlock_requirement in self._story_progress:
                    should_unlock = True

            if should_unlock:
                self.unlock_recipe(recipe_id)
                newly_unlocked.append(recipe_id)

        return newly_unlocked

    def set_story_progress(self, chapters: List[str]):
        """Set the current story progress for unlock checks."""
        self._story_progress = list(chapters)

    def add_story_chapter(self, chapter: str):
        """Add a completed story chapter."""
        if chapter not in self._story_progress:
            self._story_progress.append(chapter)

    # =========================================================================
    # SEASONAL RECIPES (Phase 4)
    # =========================================================================

    def get_seasonal_recipes(self) -> List[Recipe]:
        """Get all seasonal recipes."""
        return [r for r in self._recipes.values()
                if r.unlock_type == UNLOCK_TYPE_SEASONAL]

    def get_seasonal_recipes_for_event(self, event_id: str) -> List[Recipe]:
        """Get seasonal recipes available during a specific event."""
        return [r for r in self._recipes.values()
                if r.unlock_type == UNLOCK_TYPE_SEASONAL
                and r.unlock_requirement == event_id]

    def is_seasonal_recipe_available(self, recipe_id: str) -> bool:
        """
        Check if a seasonal recipe is currently available.

        Args:
            recipe_id: Recipe to check

        Returns:
            True if the event for this recipe is currently active
        """
        recipe = self.get_recipe(recipe_id)
        if not recipe or recipe.unlock_type != UNLOCK_TYPE_SEASONAL:
            return False

        # Check with event manager
        from systems.events import get_event_manager
        event_mgr = get_event_manager()
        active_event = event_mgr.get_active_event()

        if active_event and active_event.event_id == recipe.unlock_requirement:
            return True
        return False

    def get_available_seasonal_recipes(self) -> List[Recipe]:
        """
        Get seasonal recipes available during the current event.

        Returns:
            List of available seasonal recipes
        """
        from systems.events import get_event_manager
        event_mgr = get_event_manager()
        active_event = event_mgr.get_active_event()

        if not active_event:
            return []

        return self.get_seasonal_recipes_for_event(active_event.event_id)

    def can_cook_seasonal(self, recipe_id: str, inventory) -> Dict[str, Any]:
        """
        Check if a seasonal recipe can be cooked.
        First checks if the seasonal event is active.

        Args:
            recipe_id: Recipe to check
            inventory: Inventory instance

        Returns:
            Dict with 'can_cook', 'error', etc.
        """
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return {'can_cook': False, 'error': 'Recipe not found'}

        if recipe.unlock_type == UNLOCK_TYPE_SEASONAL:
            if not self.is_seasonal_recipe_available(recipe_id):
                return {'can_cook': False, 'error': 'Seasonal event not active'}

        # Now check ingredients
        missing = []
        for ing in recipe.ingredients:
            count = inventory.get_count(ing.item_id, check_all=True)
            if count < ing.quantity:
                missing.append({
                    'item_id': ing.item_id,
                    'needed': ing.quantity,
                    'have': count,
                })

        can_cook = len(missing) == 0
        return {
            'can_cook': can_cook,
            'missing_ingredients': missing,
        }

    # =========================================================================
    # MASTERY
    # =========================================================================

    def get_mastery(self, recipe_id: str) -> Optional[RecipeMastery]:
        """Get mastery data for a recipe."""
        return self._mastery.get(recipe_id)

    def record_cook(self, recipe_id: str, quality: int) -> Dict[str, Any]:
        """
        Record cooking a recipe and update mastery.

        Args:
            recipe_id: Recipe that was cooked
            quality: Quality of the result (1-5)

        Returns:
            Dict with 'mastery_progress', 'newly_mastered'
        """
        if recipe_id not in self._recipes:
            return {'error': 'Recipe not found'}

        # Create mastery entry if needed
        if recipe_id not in self._mastery:
            self._mastery[recipe_id] = RecipeMastery(recipe_id=recipe_id)

        mastery = self._mastery[recipe_id]
        newly_mastered = mastery.record_cook(quality)

        return {
            'mastery_progress': mastery.get_progress(),
            'newly_mastered': newly_mastered,
        }

    def is_mastered(self, recipe_id: str) -> bool:
        """Check if a recipe is fully mastered."""
        mastery = self._mastery.get(recipe_id)
        return mastery.is_mastered if mastery else False

    def get_mastered_recipes(self) -> List[str]:
        """Get list of mastered recipe IDs."""
        return [rid for rid, m in self._mastery.items() if m.is_mastered]

    # =========================================================================
    # DRAGON COLOR INFLUENCE
    # =========================================================================

    def get_color_influence(self, recipe_id: str) -> Tuple[float, float, float]:
        """
        Get the dragon color influence for a recipe.

        Returns:
            (r, g, b) tuple of color modifiers (0.0-1.0)
        """
        recipe = self.get_recipe(recipe_id)
        if recipe:
            return recipe.color_influence
        return (0.5, 0.5, 0.5)  # Neutral default

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get complete state for saving."""
        return {
            'unlocked': self._unlocked.copy(),
            'discovered': self._discovered.copy(),
            'mastery': {rid: m.to_dict() for rid, m in self._mastery.items()},
            'story_progress': self._story_progress.copy(),
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._unlocked = state.get('unlocked', list(DEFAULT_UNLOCKED_RECIPES))
        self._discovered = state.get('discovered', [])
        self._story_progress = state.get('story_progress', [])

        self._mastery = {}
        for rid, mdata in state.get('mastery', {}).items():
            self._mastery[rid] = RecipeMastery.from_dict(mdata)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_recipe_manager: Optional[RecipeManager] = None


def get_recipe_manager() -> RecipeManager:
    """Get the global recipe manager instance."""
    global _recipe_manager
    if _recipe_manager is None:
        _recipe_manager = RecipeManager()
    return _recipe_manager


def reset_recipe_manager():
    """Reset the recipe manager (for new game)."""
    global _recipe_manager
    _recipe_manager = RecipeManager()
