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
# RESOURCE SPAWNING SYSTEM
# =============================================================================
# Spawn rarity tiers (daily spawn chance)
SPAWN_RARITY_COMMON = 'common'       # 100% spawn chance
SPAWN_RARITY_UNCOMMON = 'uncommon'   # 50% spawn chance
SPAWN_RARITY_RARE = 'rare'           # 25% spawn chance

SPAWN_CHANCE = {
    SPAWN_RARITY_COMMON: 1.0,
    SPAWN_RARITY_UNCOMMON: 0.5,
    SPAWN_RARITY_RARE: 0.25,
}

# Default respawn times (days)
RESPAWN_DAYS = {
    SPAWN_RARITY_COMMON: 1,
    SPAWN_RARITY_UNCOMMON: 2,
    SPAWN_RARITY_RARE: 3,
}

# Quality range (1-5 stars)
QUALITY_MIN = 1
QUALITY_MAX = 5

# Quality bonuses
QUALITY_SEASON_BONUS = {
    'spring': {'herb': 1, 'flower': 1, 'berry': 0},
    'summer': {'berry': 1, 'honey': 1, 'herb': 0},
}

QUALITY_WEATHER_BONUS = {
    WEATHER_SUNNY: {'honey': 1, 'berry': 0},
    WEATHER_CLOUDY: {'mushroom': 1, 'herb': 0},
    WEATHER_RAINY: {'herb': 1, 'mushroom': 1, 'fish': 1},
}

# Dragon ability requirements for certain spawn points
ABILITY_BURROW = 'burrow_fetch'
ABILITY_SNIFF = 'sniff_track'
ABILITY_SMASH = 'rock_smash'

# =============================================================================
# INGREDIENT DEFINITIONS
# =============================================================================
# Base ingredients with: (name, category, base_price, spoil_days, color_influence)
INGREDIENTS = {
    # Cafe Grounds - Basic ingredients
    'garden_herb': ('Garden Herb', ITEM_SPICE, 5, 2, (0.3, 0.7, 0.3)),
    'wild_berry': ('Wild Berry', ITEM_FRUIT, 8, 2, (0.8, 0.2, 0.4)),
    'edible_flower': ('Edible Flower', ITEM_SPECIAL, 10, 1, (0.6, 0.4, 0.7)),

    # Meadow Fields - Mid-tier ingredients
    'meadow_berry': ('Meadow Berry', ITEM_FRUIT, 12, 3, (0.7, 0.3, 0.5)),
    'golden_honey': ('Golden Honey', ITEM_SPECIAL, 25, 0, (0.9, 0.7, 0.2)),  # Never spoils
    'wild_herb': ('Wild Herb', ITEM_SPICE, 10, 3, (0.2, 0.8, 0.3)),
    'field_mushroom': ('Field Mushroom', ITEM_VEGETABLE, 15, 2, (0.5, 0.4, 0.3)),
    'buried_root': ('Buried Root', ITEM_VEGETABLE, 18, 4, (0.6, 0.4, 0.2)),

    # Forest Depths - Rare ingredients
    'rare_mushroom': ('Rare Mushroom', ITEM_VEGETABLE, 30, 2, (0.4, 0.3, 0.6)),
    'forest_herb': ('Forest Herb', ITEM_SPICE, 20, 3, (0.1, 0.6, 0.2)),
    'wild_game': ('Wild Game', ITEM_MEAT, 35, 1, (0.8, 0.3, 0.2)),
    'forest_fish': ('Forest Fish', ITEM_SEAFOOD, 28, 1, (0.3, 0.5, 0.8)),
    'crystal_shard': ('Crystal Shard', ITEM_SPECIAL, 50, 0, (0.5, 0.5, 0.9)),  # Never spoils
    'hidden_truffle': ('Hidden Truffle', ITEM_SPECIAL, 45, 2, (0.4, 0.3, 0.2)),
}

# Spawn point definitions per zone: list of (id, name, x, y, ingredient_id, rarity, ability_required)
ZONE_SPAWN_POINTS = {
    ZONE_CAFE_GROUNDS: [
        ('cg_herb_1', 'Garden Patch', 5, 5, 'garden_herb', SPAWN_RARITY_COMMON, None),
        ('cg_herb_2', 'Herb Garden', 3, 8, 'garden_herb', SPAWN_RARITY_COMMON, None),
        ('cg_berry_1', 'Berry Bush', 8, 10, 'wild_berry', SPAWN_RARITY_COMMON, None),
        ('cg_flower_1', 'Flower Bed', 15, 7, 'edible_flower', SPAWN_RARITY_UNCOMMON, None),
        ('cg_flower_2', 'Window Box', 12, 3, 'edible_flower', SPAWN_RARITY_UNCOMMON, None),
    ],
    ZONE_MEADOW_FIELDS: [
        ('mf_berry_1', 'Wild Berry Thicket', 4, 8, 'meadow_berry', SPAWN_RARITY_COMMON, None),
        ('mf_berry_2', 'Sunlit Berries', 16, 5, 'meadow_berry', SPAWN_RARITY_COMMON, None),
        ('mf_honey_1', 'Bee Hive', 12, 3, 'golden_honey', SPAWN_RARITY_RARE, None),
        ('mf_herb_1', 'Herb Meadow', 16, 12, 'wild_herb', SPAWN_RARITY_COMMON, None),
        ('mf_mushroom_1', 'Mushroom Circle', 7, 14, 'field_mushroom', SPAWN_RARITY_UNCOMMON, None),
        ('mf_mushroom_2', 'Shady Spot', 3, 11, 'field_mushroom', SPAWN_RARITY_UNCOMMON, None),
        ('mf_root_1', 'Buried Treasure', 10, 6, 'buried_root', SPAWN_RARITY_UNCOMMON, ABILITY_BURROW),
        ('mf_root_2', 'Deep Soil', 14, 10, 'buried_root', SPAWN_RARITY_RARE, ABILITY_BURROW),
    ],
    ZONE_FOREST_DEPTHS: [
        ('fd_mushroom_1', 'Rare Fungi', 6, 6, 'rare_mushroom', SPAWN_RARITY_UNCOMMON, None),
        ('fd_mushroom_2', 'Hidden Grove', 14, 4, 'rare_mushroom', SPAWN_RARITY_RARE, ABILITY_SNIFF),
        ('fd_herb_1', 'Forest Floor', 10, 8, 'forest_herb', SPAWN_RARITY_COMMON, None),
        ('fd_herb_2', 'Mossy Bank', 4, 12, 'forest_herb', SPAWN_RARITY_UNCOMMON, None),
        ('fd_game_1', 'Hunting Grounds', 10, 11, 'wild_game', SPAWN_RARITY_RARE, ABILITY_SNIFF),
        ('fd_fish_1', 'Forest Stream', 17, 9, 'forest_fish', SPAWN_RARITY_UNCOMMON, None),
        ('fd_crystal_1', 'Crystal Cave', 18, 13, 'crystal_shard', SPAWN_RARITY_RARE, ABILITY_SMASH),
        ('fd_truffle_1', 'Truffle Spot', 8, 3, 'hidden_truffle', SPAWN_RARITY_RARE, ABILITY_SNIFF),
    ],
}

# =============================================================================
# GAME VERSION
# =============================================================================
VERSION = "0.1.0"
