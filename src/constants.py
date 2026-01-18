"""
Game constants for Dragon Haven Cafe.
All configurable values in one place for easy tuning.
"""

# =============================================================================
# DISPLAY SETTINGS
# =============================================================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Dragon Haven Cafe"

# =============================================================================
# COLORS (RGB)
# =============================================================================
# Basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# UI colors
UI_BG = (45, 40, 55)
UI_PANEL = (65, 58, 78)
UI_BORDER = (95, 85, 115)
UI_HIGHLIGHT = (125, 110, 150)
UI_TEXT = (240, 235, 245)
UI_TEXT_DIM = (160, 150, 175)

# Game colors - warm cafe palette
CAFE_WARM = (180, 140, 100)
CAFE_WOOD = (120, 80, 50)
CAFE_CREAM = (255, 245, 220)
CAFE_ACCENT = (200, 100, 80)

# Dragon colors (base - will be modified by food)
DRAGON_BASE = (120, 180, 140)
DRAGON_EGG = (200, 190, 170)

# Nature colors
GRASS_GREEN = (100, 160, 80)
FOREST_GREEN = (60, 100, 50)
SKY_BLUE = (135, 180, 220)
WATER_BLUE = (80, 140, 200)

# Status colors
HEALTH_GREEN = (80, 200, 100)
STAMINA_YELLOW = (220, 180, 60)
HUNGER_ORANGE = (220, 140, 60)
HAPPINESS_PINK = (220, 140, 180)

# Dragon stage colors
DRAGON_EGG_SHELL = (220, 210, 190)
DRAGON_EGG_SPOT = (180, 160, 130)
DRAGON_HATCHLING = (140, 200, 160)
DRAGON_JUVENILE = (100, 180, 130)
DRAGON_WING = (80, 150, 110)
DRAGON_EYE = (60, 40, 30)
DRAGON_BELLY = (200, 220, 190)

# Character colors
CHAR_SKIN = (230, 200, 170)
CHAR_HAIR_BROWN = (100, 70, 50)
CHAR_HAIR_BLACK = (40, 35, 35)
CHAR_HAIR_BLONDE = (220, 180, 100)
CHAR_APRON = (255, 250, 240)
CHAR_CLOTHES = (80, 100, 140)

# Ingredient colors
INGREDIENT_BERRY = (180, 60, 80)
INGREDIENT_HERB = (60, 140, 70)
INGREDIENT_MUSHROOM = (180, 150, 120)
INGREDIENT_HONEY = (230, 180, 60)
INGREDIENT_MEAT = (180, 100, 90)
INGREDIENT_FISH = (140, 160, 200)

# Terrain colors
TERRAIN_DIRT = (140, 100, 70)
TERRAIN_STONE = (140, 140, 140)
TERRAIN_SAND = (220, 200, 160)
TERRAIN_FLOWER_RED = (220, 80, 80)
TERRAIN_FLOWER_YELLOW = (240, 220, 80)
TERRAIN_FLOWER_BLUE = (100, 140, 220)

# =============================================================================
# TIME SYSTEM
# =============================================================================
# Time periods (24-hour format)
TIME_MORNING_START = 6    # 6:00 AM
TIME_AFTERNOON_START = 12  # 12:00 PM
TIME_EVENING_START = 18   # 6:00 PM
TIME_NIGHT_START = 0      # 12:00 AM (wraps around)

# Day length: 24 in-game hours = 24 real minutes (1 minute per hour)
REAL_SECONDS_PER_GAME_HOUR = 60.0  # 1 real minute = 1 game hour
GAME_HOURS_PER_DAY = 24

# Seasons (simplified)
DAYS_PER_SEASON = 10
SEASONS = ['spring', 'summer']

# Cafe operating hours
CAFE_OPEN_HOUR = 8   # Opens at 8 AM
CAFE_CLOSE_HOUR = 22  # Closes at 10 PM

# =============================================================================
# DRAGON SYSTEM
# =============================================================================
# Life stages and their day ranges
DRAGON_STAGE_EGG = 'egg'
DRAGON_STAGE_HATCHLING = 'hatchling'
DRAGON_STAGE_JUVENILE = 'juvenile'

# Stage progression (days alive)
DRAGON_EGG_DAYS = 3        # Days 1-3: Egg
DRAGON_HATCHLING_DAYS = 7  # Days 4-10: Hatchling (HATCHLING_END = EGG + HATCHLING)
# Days 11+: Juvenile

# Stat ranges
DRAGON_STAT_MAX = 100.0
DRAGON_BOND_MAX = 1000

# Stat decay rates (per game hour)
DRAGON_HUNGER_DECAY = 2.0    # Loses 2 hunger per hour
DRAGON_HAPPINESS_DECAY = 0.5  # Loses 0.5 happiness per hour
DRAGON_STAMINA_REGEN = 5.0    # Gains 5 stamina per hour (when resting)

# Stat thresholds
DRAGON_HUNGER_WARNING = 30.0
DRAGON_HAPPINESS_WARNING = 30.0
DRAGON_STAMINA_LOW = 20.0

# Feeding effects
DRAGON_FEED_HUNGER_RESTORE = 30.0
DRAGON_FEED_HAPPINESS_BONUS = 10.0
DRAGON_FEED_BOND_BONUS = 5

# Petting effects
DRAGON_PET_HAPPINESS = 15.0
DRAGON_PET_BOND = 3

# Color shift rate (how fast color changes from food)
DRAGON_COLOR_SHIFT_RATE = 0.05

# Ability stamina costs
DRAGON_ABILITY_COSTS = {
    'burrow_fetch': 20,
    'sniff_track': 15,
    'rock_smash': 30,
}

# Abilities unlocked per stage
DRAGON_STAGE_ABILITIES = {
    DRAGON_STAGE_EGG: [],
    DRAGON_STAGE_HATCHLING: ['burrow_fetch', 'sniff_track'],
    DRAGON_STAGE_JUVENILE: ['burrow_fetch', 'sniff_track', 'rock_smash'],
}

# =============================================================================
# INVENTORY SYSTEM
# =============================================================================
# Item categories
ITEM_VEGETABLE = 'vegetable'
ITEM_FRUIT = 'fruit'
ITEM_GRAIN = 'grain'
ITEM_MEAT = 'meat'
ITEM_SEAFOOD = 'seafood'
ITEM_DAIRY = 'dairy'
ITEM_SPICE = 'spice'
ITEM_SPECIAL = 'special'

# All categories for iteration
ITEM_CATEGORIES = [
    ITEM_VEGETABLE, ITEM_FRUIT, ITEM_GRAIN, ITEM_MEAT,
    ITEM_SEAFOOD, ITEM_DAIRY, ITEM_SPICE, ITEM_SPECIAL
]

# Inventory capacities
INVENTORY_CARRIED_SLOTS = 20
INVENTORY_STORAGE_SLOTS = 100
INVENTORY_FRIDGE_SLOTS = 30

# Item defaults
ITEM_DEFAULT_STACK_SIZE = 10
ITEM_DEFAULT_SPOIL_DAYS = 3  # Days until item spoils (0 = never)

# Starting gold
STARTING_GOLD = 100

# =============================================================================
# WORLD/ZONE SYSTEM
# =============================================================================
# Zone IDs
ZONE_CAFE_GROUNDS = 'cafe_grounds'
ZONE_MEADOW_FIELDS = 'meadow_fields'
ZONE_FOREST_DEPTHS = 'forest_depths'

# All zones for iteration
ALL_ZONES = [ZONE_CAFE_GROUNDS, ZONE_MEADOW_FIELDS, ZONE_FOREST_DEPTHS]

# Zone unlock requirements (dragon stage)
ZONE_UNLOCK_REQUIREMENTS = {
    ZONE_CAFE_GROUNDS: None,  # Always unlocked
    ZONE_MEADOW_FIELDS: DRAGON_STAGE_HATCHLING,
    ZONE_FOREST_DEPTHS: DRAGON_STAGE_JUVENILE,
}

# Zone connections (which zones connect to which)
ZONE_CONNECTIONS = {
    ZONE_CAFE_GROUNDS: [ZONE_MEADOW_FIELDS],
    ZONE_MEADOW_FIELDS: [ZONE_CAFE_GROUNDS, ZONE_FOREST_DEPTHS],
    ZONE_FOREST_DEPTHS: [ZONE_MEADOW_FIELDS],
}

# Zone map sizes (tiles)
ZONE_WIDTH = 20
ZONE_HEIGHT = 15
TILE_SIZE = 32

# Weather types
WEATHER_SUNNY = 'sunny'
WEATHER_CLOUDY = 'cloudy'
WEATHER_RAINY = 'rainy'

ALL_WEATHER = [WEATHER_SUNNY, WEATHER_CLOUDY, WEATHER_RAINY]

# Weather probabilities per season (must sum to 1.0)
WEATHER_PROBABILITIES = {
    'spring': {WEATHER_SUNNY: 0.4, WEATHER_CLOUDY: 0.35, WEATHER_RAINY: 0.25},
    'summer': {WEATHER_SUNNY: 0.6, WEATHER_CLOUDY: 0.3, WEATHER_RAINY: 0.1},
}

# Weather effects on resource spawn rates
WEATHER_RESOURCE_MULTIPLIER = {
    WEATHER_SUNNY: 1.0,
    WEATHER_CLOUDY: 1.1,  # Slightly more resources
    WEATHER_RAINY: 1.3,   # Best for foraging
}

# =============================================================================
# GAME VERSION
# =============================================================================
VERSION = "0.1.0"
