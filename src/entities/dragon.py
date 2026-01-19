"""
Dragon Entity for Dragon Haven Cafe.
The heart of the game - a dragon companion that grows, eats, and helps at the cafe.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from constants import (
    DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
    DRAGON_STAGE_ADOLESCENT, DRAGON_STAGE_ADULT,
    DRAGON_EGG_DAYS, DRAGON_HATCHLING_DAYS, DRAGON_JUVENILE_DAYS, DRAGON_ADOLESCENT_DAYS,
    DRAGON_STAT_MAX, DRAGON_BOND_MAX, DRAGON_STAGE_STAMINA_MAX,
    DRAGON_HUNGER_DECAY, DRAGON_HAPPINESS_DECAY, DRAGON_STAMINA_REGEN,
    DRAGON_HUNGER_WARNING, DRAGON_HAPPINESS_WARNING, DRAGON_STAMINA_LOW,
    DRAGON_FEED_HUNGER_RESTORE, DRAGON_FEED_HAPPINESS_BONUS, DRAGON_FEED_BOND_BONUS,
    DRAGON_PET_HAPPINESS, DRAGON_PET_BOND,
    DRAGON_COLOR_SHIFT_RATE,
    DRAGON_ABILITY_COSTS, DRAGON_STAGE_ABILITIES,
    DRAGON_NAME_MAX_LENGTH, DRAGON_NAME_DEFAULT,
    REAL_SECONDS_PER_GAME_HOUR
)


@dataclass
class DragonColor:
    """
    RGB color representation for dragon appearance.
    Each channel is 0.0-1.0, representing deviation from base color.
    """
    red: float = 0.0    # -1.0 to 1.0
    green: float = 0.0
    blue: float = 0.0

    def to_shift(self) -> Tuple[int, int, int]:
        """Convert to integer RGB shift values for sprites."""
        return (
            int(self.red * 50),     # Max shift of 50
            int(self.green * 50),
            int(self.blue * 50)
        )

    def apply_food_color(self, food_color: Tuple[float, float, float], rate: float):
        """
        Gradually shift color based on food consumed.

        Args:
            food_color: RGB tuple (0.0-1.0 each) of food's color influence
            rate: How much to shift (0.0-1.0)
        """
        # Blend towards food color
        self.red = self.red * (1 - rate) + (food_color[0] - 0.5) * 2 * rate
        self.green = self.green * (1 - rate) + (food_color[1] - 0.5) * 2 * rate
        self.blue = self.blue * (1 - rate) + (food_color[2] - 0.5) * 2 * rate

        # Clamp values
        self.red = max(-1.0, min(1.0, self.red))
        self.green = max(-1.0, min(1.0, self.green))
        self.blue = max(-1.0, min(1.0, self.blue))

    def to_dict(self) -> Dict[str, float]:
        return {'red': self.red, 'green': self.green, 'blue': self.blue}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'DragonColor':
        return cls(
            red=data.get('red', 0.0),
            green=data.get('green', 0.0),
            blue=data.get('blue', 0.0)
        )


class Dragon:
    """
    The main dragon entity.

    Dragons have stats that need management, grow through life stages,
    develop abilities, and change color based on their diet.

    Usage:
        dragon = Dragon("Ember")
        dragon.update(dt)  # Call each frame
        dragon.feed(recipe)  # Feed with a recipe
        dragon.pet()  # Pet for happiness
        if dragon.can_use_ability('burrow_fetch'):
            dragon.use_ability('burrow_fetch')
    """

    def __init__(self, name: str = DRAGON_NAME_DEFAULT):
        """
        Initialize a new dragon (as an egg).

        Args:
            name: The dragon's name
        """
        self.name = name

        # Life tracking
        self._age_hours = 0.0  # Total hours alive
        self._stage = DRAGON_STAGE_EGG
        self._hatched = False

        # Core stats
        self._hunger = DRAGON_STAT_MAX
        self._happiness = DRAGON_STAT_MAX
        self._stamina = DRAGON_STAT_MAX
        self._bond = 0  # Lifetime bond accumulation

        # Color system
        self._color = DragonColor()

        # State tracking
        self._is_resting = False
        self._last_fed_hour = 0.0
        self._times_fed_today = 0

        # Callbacks for stage change
        self._stage_change_callbacks = []

    # =========================================================================
    # CORE UPDATE
    # =========================================================================

    def update(self, dt: float):
        """
        Update the dragon's state.

        Args:
            dt: Delta time in real seconds
        """
        # Convert to game hours
        game_hours = dt / REAL_SECONDS_PER_GAME_HOUR

        # Update age
        self._age_hours += game_hours

        # Check for stage progression
        self._check_stage_progression()

        # Stat decay (eggs don't have stat decay)
        if self._stage != DRAGON_STAGE_EGG:
            self._update_stats(game_hours)

    def _update_stats(self, game_hours: float):
        """Update stats based on time passed."""
        # Hunger decreases over time
        self._hunger -= DRAGON_HUNGER_DECAY * game_hours
        self._hunger = max(0, self._hunger)

        # Happiness decreases slowly
        # Faster if hungry
        happiness_decay = DRAGON_HAPPINESS_DECAY
        if self._hunger < DRAGON_HUNGER_WARNING:
            happiness_decay *= 2
        self._happiness -= happiness_decay * game_hours
        self._happiness = max(0, self._happiness)

        # Stamina regenerates when resting, decays slowly otherwise
        max_stamina = self.get_max_stamina()
        if self._is_resting:
            self._stamina += DRAGON_STAMINA_REGEN * game_hours
        else:
            self._stamina += DRAGON_STAMINA_REGEN * 0.3 * game_hours  # Slow regen when active

        self._stamina = max(0, min(max_stamina, self._stamina))

    def _check_stage_progression(self):
        """Check and handle stage transitions."""
        days_old = self.get_age_days()
        old_stage = self._stage

        # Calculate stage thresholds
        egg_end = DRAGON_EGG_DAYS
        hatchling_end = egg_end + DRAGON_HATCHLING_DAYS
        juvenile_end = hatchling_end + DRAGON_JUVENILE_DAYS
        adolescent_end = juvenile_end + DRAGON_ADOLESCENT_DAYS

        if days_old <= egg_end:
            self._stage = DRAGON_STAGE_EGG
        elif days_old <= hatchling_end:
            self._stage = DRAGON_STAGE_HATCHLING
            self._hatched = True
        elif days_old <= juvenile_end:
            self._stage = DRAGON_STAGE_JUVENILE
            self._hatched = True
        elif days_old <= adolescent_end:
            self._stage = DRAGON_STAGE_ADOLESCENT
            self._hatched = True
        else:
            self._stage = DRAGON_STAGE_ADULT
            self._hatched = True

        # Trigger callbacks if stage changed
        if old_stage != self._stage:
            for callback in self._stage_change_callbacks:
                try:
                    callback(old_stage, self._stage)
                except Exception as e:
                    print(f"Error in dragon stage callback: {e}")

    # =========================================================================
    # STAT QUERIES
    # =========================================================================

    def get_hunger(self) -> float:
        """Get current hunger (0-100)."""
        return self._hunger

    def get_happiness(self) -> float:
        """Get current happiness (0-100)."""
        return self._happiness

    def get_stamina(self) -> float:
        """Get current stamina (0-max based on stage)."""
        return self._stamina

    def get_max_stamina(self) -> float:
        """Get maximum stamina for current stage."""
        return DRAGON_STAGE_STAMINA_MAX.get(self._stage, DRAGON_STAT_MAX)

    def get_bond(self) -> int:
        """Get lifetime bond level (0-1000)."""
        return self._bond

    def get_stage(self) -> str:
        """Get current life stage."""
        return self._stage

    def get_age_days(self) -> int:
        """Get age in days (1-based)."""
        return int(self._age_hours / 24) + 1

    def get_age_hours(self) -> float:
        """Get total age in game hours."""
        return self._age_hours

    def is_hatched(self) -> bool:
        """Check if the dragon has hatched from egg."""
        return self._hatched

    def is_hungry(self) -> bool:
        """Check if hunger is at warning level."""
        return self._hunger < DRAGON_HUNGER_WARNING

    def is_unhappy(self) -> bool:
        """Check if happiness is at warning level."""
        return self._happiness < DRAGON_HAPPINESS_WARNING

    def is_tired(self) -> bool:
        """Check if stamina is low."""
        return self._stamina < DRAGON_STAMINA_LOW

    def get_color_shift(self) -> Tuple[int, int, int]:
        """Get the RGB color shift for sprite rendering."""
        return self._color.to_shift()

    def get_stat_percentages(self) -> Dict[str, float]:
        """Get all stats as percentages (0.0-1.0)."""
        max_stamina = self.get_max_stamina()
        return {
            'hunger': self._hunger / DRAGON_STAT_MAX,
            'happiness': self._happiness / DRAGON_STAT_MAX,
            'stamina': self._stamina / max_stamina,
            'bond': self._bond / DRAGON_BOND_MAX
        }

    def get_name(self) -> str:
        """Get the dragon's name."""
        return self.name

    def set_name(self, name: str) -> bool:
        """
        Set the dragon's name with validation.

        Args:
            name: The new name (will be stripped of whitespace)

        Returns:
            True if name was valid and set, False otherwise
        """
        # Strip whitespace
        name = name.strip()

        # Validate: not empty
        if not name:
            return False

        # Validate: max length
        if len(name) > DRAGON_NAME_MAX_LENGTH:
            name = name[:DRAGON_NAME_MAX_LENGTH]

        self.name = name
        return True

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """
        Validate a potential dragon name.

        Args:
            name: The name to validate

        Returns:
            Tuple of (is_valid, error_message or validated_name)
        """
        name = name.strip()

        if not name:
            return False, "Name cannot be empty"

        if len(name) > DRAGON_NAME_MAX_LENGTH:
            return False, f"Name cannot exceed {DRAGON_NAME_MAX_LENGTH} characters"

        return True, name

    # =========================================================================
    # INTERACTIONS
    # =========================================================================

    def feed(self, recipe_data: Dict[str, Any] = None) -> bool:
        """
        Feed the dragon with a recipe.

        Args:
            recipe_data: Dict with optional keys:
                - 'hunger_value': How much hunger to restore (default: DRAGON_FEED_HUNGER_RESTORE)
                - 'happiness_bonus': Bonus happiness (default: DRAGON_FEED_HAPPINESS_BONUS)
                - 'color_influence': RGB tuple (0-1) for color shift
                - 'quality': Multiplier for effects (default: 1.0)

        Returns:
            True if feeding was successful
        """
        if self._stage == DRAGON_STAGE_EGG:
            return False  # Can't feed an egg

        recipe_data = recipe_data or {}

        # Base values
        quality = recipe_data.get('quality', 1.0)
        hunger_restore = recipe_data.get('hunger_value', DRAGON_FEED_HUNGER_RESTORE) * quality
        happiness_bonus = recipe_data.get('happiness_bonus', DRAGON_FEED_HAPPINESS_BONUS) * quality

        # Apply stat changes
        self._hunger = min(DRAGON_STAT_MAX, self._hunger + hunger_restore)
        self._happiness = min(DRAGON_STAT_MAX, self._happiness + happiness_bonus)
        self._bond = min(DRAGON_BOND_MAX, self._bond + DRAGON_FEED_BOND_BONUS)

        # Apply color influence if present
        color_influence = recipe_data.get('color_influence')
        if color_influence:
            self._color.apply_food_color(color_influence, DRAGON_COLOR_SHIFT_RATE)

        self._times_fed_today += 1
        return True

    def pet(self) -> bool:
        """
        Pet the dragon to increase happiness and bond.

        Returns:
            True if petting was successful
        """
        if self._stage == DRAGON_STAGE_EGG:
            return False  # Can't pet an egg (but you can warm it - future feature?)

        self._happiness = min(DRAGON_STAT_MAX, self._happiness + DRAGON_PET_HAPPINESS)
        self._bond = min(DRAGON_BOND_MAX, self._bond + DRAGON_PET_BOND)
        return True

    def set_resting(self, resting: bool):
        """Set whether the dragon is resting (faster stamina regen)."""
        self._is_resting = resting

    def reset_daily_counters(self):
        """Reset daily tracking counters (called at start of new day)."""
        self._times_fed_today = 0

    # =========================================================================
    # ABILITIES
    # =========================================================================

    def get_available_abilities(self) -> List[str]:
        """Get list of abilities available at current stage."""
        return DRAGON_STAGE_ABILITIES.get(self._stage, [])

    def can_use_ability(self, ability_name: str) -> bool:
        """
        Check if an ability can be used.

        Args:
            ability_name: Name of the ability

        Returns:
            True if ability is available and stamina is sufficient
        """
        available = self.get_available_abilities()
        if ability_name not in available:
            return False

        cost = DRAGON_ABILITY_COSTS.get(ability_name, 0)
        return self._stamina >= cost

    def use_ability(self, ability_name: str) -> bool:
        """
        Use an ability, consuming stamina.

        Args:
            ability_name: Name of the ability to use

        Returns:
            True if ability was used successfully
        """
        if not self.can_use_ability(ability_name):
            return False

        cost = DRAGON_ABILITY_COSTS.get(ability_name, 0)
        self._stamina -= cost
        return True

    def get_ability_cost(self, ability_name: str) -> int:
        """Get the stamina cost of an ability."""
        return DRAGON_ABILITY_COSTS.get(ability_name, 0)

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def on_stage_change(self, callback):
        """
        Register callback for stage changes.

        Args:
            callback: Function(old_stage, new_stage)
        """
        self._stage_change_callbacks.append(callback)

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get complete state for saving."""
        return {
            'name': self.name,
            'age_hours': self._age_hours,
            'stage': self._stage,
            'hatched': self._hatched,
            'hunger': self._hunger,
            'happiness': self._happiness,
            'stamina': self._stamina,
            'bond': self._bond,
            'color': self._color.to_dict(),
            'is_resting': self._is_resting,
            'times_fed_today': self._times_fed_today
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self.name = state.get('name', 'Dragon')
        self._age_hours = state.get('age_hours', 0.0)
        self._stage = state.get('stage', DRAGON_STAGE_EGG)
        self._hatched = state.get('hatched', False)
        self._hunger = state.get('hunger', DRAGON_STAT_MAX)
        self._happiness = state.get('happiness', DRAGON_STAT_MAX)
        self._stamina = state.get('stamina', DRAGON_STAT_MAX)
        self._bond = state.get('bond', 0)

        color_data = state.get('color', {})
        self._color = DragonColor.from_dict(color_data)

        self._is_resting = state.get('is_resting', False)
        self._times_fed_today = state.get('times_fed_today', 0)

    @classmethod
    def from_state(cls, state: Dict[str, Any]) -> 'Dragon':
        """Create a dragon from saved state."""
        dragon = cls()
        dragon.load_state(state)
        return dragon

    # =========================================================================
    # CONVENIENCE METHODS
    # =========================================================================

    def get_mood(self) -> str:
        """
        Get the dragon's current mood based on stats.

        Returns:
            Mood string: 'happy', 'content', 'tired', 'hungry', 'sad'
        """
        if self._stage == DRAGON_STAGE_EGG:
            return 'incubating'

        if self._happiness >= 80 and self._hunger >= 50:
            return 'happy'
        elif self._hunger < 20:
            return 'hungry'
        elif self._happiness < 20:
            return 'sad'
        elif self._stamina < 20:
            return 'tired'
        elif self._happiness >= 50:
            return 'content'
        else:
            return 'neutral'

    def get_stage_progress(self) -> float:
        """
        Get progress through current life stage (0.0-1.0).

        Returns:
            Progress percentage within current stage
        """
        days = self.get_age_days()

        # Calculate stage thresholds
        egg_end = DRAGON_EGG_DAYS
        hatchling_end = egg_end + DRAGON_HATCHLING_DAYS
        juvenile_end = hatchling_end + DRAGON_JUVENILE_DAYS
        adolescent_end = juvenile_end + DRAGON_ADOLESCENT_DAYS

        if self._stage == DRAGON_STAGE_EGG:
            return min(1.0, days / DRAGON_EGG_DAYS)
        elif self._stage == DRAGON_STAGE_HATCHLING:
            days_in_stage = days - egg_end
            return min(1.0, days_in_stage / DRAGON_HATCHLING_DAYS)
        elif self._stage == DRAGON_STAGE_JUVENILE:
            days_in_stage = days - hatchling_end
            return min(1.0, days_in_stage / DRAGON_JUVENILE_DAYS)
        elif self._stage == DRAGON_STAGE_ADOLESCENT:
            days_in_stage = days - juvenile_end
            return min(1.0, days_in_stage / DRAGON_ADOLESCENT_DAYS)
        else:
            # Adult has no end, show bond progress instead
            return min(1.0, self._bond / DRAGON_BOND_MAX)

    def __repr__(self) -> str:
        return f"Dragon(name='{self.name}', stage={self._stage}, days={self.get_age_days()})"
