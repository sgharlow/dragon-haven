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

# Day length: 24 in-game hours = 12 real minutes (30 sec per hour)
# BALANCE: Faster time allows meaningful progression in 15-30 min session
# At 30 sec/hour: 1 service period (4 hours) = 2 real minutes
REAL_SECONDS_PER_GAME_HOUR = 30.0  # 30 real seconds = 1 game hour
GAME_HOURS_PER_DAY = 24

# Seasons (simplified)
DAYS_PER_SEASON = 7  # BALANCE: Shorter seasons for variety
SEASONS = ['spring', 'summer']

# Cafe operating hours
CAFE_OPEN_HOUR = 8   # Opens at 8 AM
CAFE_CLOSE_HOUR = 22  # Closes at 10 PM

# Cafe states
CAFE_STATE_CLOSED = 'closed'
CAFE_STATE_PREP = 'prep'
CAFE_STATE_SERVICE = 'service'
CAFE_STATE_CLEANUP = 'cleanup'

# Service period (simplified for prototype - single lunch service)
CAFE_SERVICE_START = 10    # Service starts at 10 AM
CAFE_SERVICE_END = 14      # Service ends at 2 PM
CAFE_PREP_DURATION = 1     # 1 hour prep before service
CAFE_CLEANUP_DURATION = 1  # 1 hour cleanup after service

# Menu settings
CAFE_MAX_MENU_ITEMS = 6    # Max dishes on menu at once
CAFE_SKIP_REP_PENALTY = 10  # Reputation penalty for skipping a day

# =============================================================================
# REPUTATION SYSTEM
# =============================================================================
# Reputation range
REPUTATION_MIN = 0
REPUTATION_MAX = 500

# Reputation levels (tier name, min reputation, max reputation)
REPUTATION_LEVEL_UNKNOWN = 'unknown'
REPUTATION_LEVEL_LOCAL = 'local_favorite'
REPUTATION_LEVEL_TOWN = 'town_attraction'
REPUTATION_LEVEL_REGIONAL = 'regional_fame'

REPUTATION_LEVELS = {
    REPUTATION_LEVEL_UNKNOWN: {'min': 0, 'max': 49, 'name': 'Unknown'},
    REPUTATION_LEVEL_LOCAL: {'min': 50, 'max': 149, 'name': 'Local Favorite'},
    REPUTATION_LEVEL_TOWN: {'min': 150, 'max': 299, 'name': 'Town Attraction'},
    REPUTATION_LEVEL_REGIONAL: {'min': 300, 'max': 500, 'name': 'Regional Fame'},
}

# Customer count range per reputation level
REPUTATION_CUSTOMER_RANGE = {
    REPUTATION_LEVEL_UNKNOWN: (1, 2),
    REPUTATION_LEVEL_LOCAL: (2, 4),
    REPUTATION_LEVEL_TOWN: (3, 6),
    REPUTATION_LEVEL_REGIONAL: (5, 8),
}

# Reputation gains/losses
REP_GAIN_SATISFIED = 3      # Satisfied customer (rating 4+)
REP_GAIN_DELIGHTED = 5      # Delighted customer (rating 5)
REP_LOSS_ANGRY = -5         # Angry customer (rating 2-)
REP_LOSS_NEUTRAL = -1       # Neutral customer (rating 2-3)

# Daily reputation decay (if cafe not operated)
REPUTATION_DAILY_DECAY = 2

# Level up unlocks (reputation level -> list of unlocks)
REPUTATION_UNLOCKS = {
    REPUTATION_LEVEL_LOCAL: ['berry_juice', 'mushroom_skewers'],
    REPUTATION_LEVEL_TOWN: ['forest_fish_plate', 'honey_cake'],
    REPUTATION_LEVEL_REGIONAL: ['game_roast', 'all_recipes'],
}

# =============================================================================
# STAFF SYSTEM
# =============================================================================
# Staff roles
STAFF_ROLE_SERVER = 'server'
STAFF_ROLE_CHEF = 'chef'
STAFF_ROLE_BUSSER = 'busser'

# Staff traits
STAFF_TRAIT_ENTHUSIASTIC = 'enthusiastic'  # Works faster but makes mistakes
STAFF_TRAIT_SKILLED = 'skilled'            # High quality but prideful
STAFF_TRAIT_LAZY = 'lazy'                  # Slow but perceptive

# Morale settings
STAFF_MORALE_MAX = 100
STAFF_MORALE_START = 70
STAFF_MORALE_DECAY_PER_HOUR = 1.0  # Morale lost per game hour during service
STAFF_TALK_MORALE_BOOST = 15       # Morale gained from talking
STAFF_TALK_COOLDOWN = 2.0          # Hours between talks

# Efficiency settings
STAFF_MIN_EFFICIENCY = 0.5   # Minimum efficiency at 0 morale
STAFF_MAX_EFFICIENCY = 1.2   # Maximum efficiency at 100 morale (with trait bonus)

# Mistake probabilities (base, modified by trait/morale)
STAFF_MISTAKE_BASE_CHANCE = 0.05  # 5% base chance
STAFF_LOW_MORALE_THRESHOLD = 30   # Below this, mistakes more likely

# Staff definitions: (id, name, role, trait, description)
STAFF_DEFINITIONS = {
    'melody': {
        'name': 'Melody',
        'role': STAFF_ROLE_SERVER,
        'trait': STAFF_TRAIT_ENTHUSIASTIC,
        'description': 'Enthusiastic but clumsy. Needs pep talks to stay focused.',
        'mistake_type': 'drops items',
    },
    'bruno': {
        'name': 'Bruno',
        'role': STAFF_ROLE_CHEF,
        'trait': STAFF_TRAIT_SKILLED,
        'description': 'Skilled but prideful. Needs recipe guidance to try new things.',
        'mistake_type': 'refuses unfamiliar recipes',
    },
    'sage': {
        'name': 'Sage',
        'role': STAFF_ROLE_BUSSER,
        'trait': STAFF_TRAIT_LAZY,
        'description': 'Lazy but perceptive. Needs frequent motivation to work.',
        'mistake_type': 'slacks off',
    },
}

# =============================================================================
# CUSTOMER SYSTEM
# =============================================================================
# Customer types
CUSTOMER_TYPE_REGULAR = 'regular'
CUSTOMER_TYPE_STORY = 'story'

# Customer states
CUSTOMER_STATE_WAITING = 'waiting'       # Waiting to be seated
CUSTOMER_STATE_SEATED = 'seated'         # At table, waiting for service
CUSTOMER_STATE_ORDERING = 'ordering'     # Placing order
CUSTOMER_STATE_WAITING_FOOD = 'waiting_food'  # Order placed, waiting
CUSTOMER_STATE_EATING = 'eating'         # Eating food
CUSTOMER_STATE_LEAVING = 'leaving'       # About to leave

# Patience settings (game hours)
# BALANCE: With 30 sec/hour, 2 game hours = 60 real seconds
# Customers should feel urgent but not frustrating
CUSTOMER_PATIENCE_BASE = 2.0             # Base patience = 60 real seconds
CUSTOMER_PATIENCE_VARIATION = 0.5        # +/- 15 real seconds
CUSTOMER_EATING_TIME = 0.5               # 15 real seconds eating

# Spawn rates (customers per hour at different reputation levels)
CUSTOMER_SPAWN_BASE = 2.0                # 2 per hour base
CUSTOMER_SPAWN_REP_BONUS = 0.01          # +1% per reputation point

# Quality expectations (0-5 stars)
CUSTOMER_QUALITY_LOW = 2                 # Easy to please
CUSTOMER_QUALITY_MEDIUM = 3              # Average expectations
CUSTOMER_QUALITY_HIGH = 4                # Demanding

# Satisfaction thresholds
CUSTOMER_SATISFACTION_ANGRY = 2          # Below this = angry
CUSTOMER_SATISFACTION_NEUTRAL = 3        # Below this = neutral
CUSTOMER_SATISFACTION_HAPPY = 4          # At or above = happy

# Satisfaction modifiers
SATISFACTION_QUALITY_WEIGHT = 0.6        # 60% from dish quality
SATISFACTION_SPEED_WEIGHT = 0.3          # 30% from service speed
SATISFACTION_STAFF_WEIGHT = 0.1          # 10% from staff efficiency

# Reputation change from customer feedback
REP_CHANGE_ANGRY = -5
REP_CHANGE_NEUTRAL = 0
REP_CHANGE_HAPPY = 3
REP_CHANGE_DELIGHTED = 5  # Satisfaction = 5

# Order preferences (categories)
ORDER_CATEGORY_APPETIZER = 'appetizer'
ORDER_CATEGORY_MAIN = 'main'
ORDER_CATEGORY_DESSERT = 'dessert'
ORDER_CATEGORY_DRINK = 'drink'

# =============================================================================
# DRAGON SYSTEM
# =============================================================================
# Life stages and their day ranges
DRAGON_STAGE_EGG = 'egg'
DRAGON_STAGE_HATCHLING = 'hatchling'
DRAGON_STAGE_JUVENILE = 'juvenile'

# Stage progression (days alive)
# BALANCE: Faster growth for shorter play sessions (15-30 min target)
# At 12 real min/day: Egg hatches in 12 min, Juvenile at 36 min
DRAGON_EGG_DAYS = 1        # Day 1: Egg (hatches quickly!)
DRAGON_HATCHLING_DAYS = 3  # Days 2-4: Hatchling
# Days 5+: Juvenile

# Stat ranges
DRAGON_STAT_MAX = 100.0
DRAGON_BOND_MAX = 500  # BALANCE: Lower max for achievable progression

# Stat decay rates (per game hour)
# BALANCE: With 30 sec/hour, decay is 2x faster in real-time
# Hunger: 3/hour = full hunger depletes in ~33 hours (16 min real)
# Happiness: 1/hour = full happiness depletes in 100 hours (50 min real)
DRAGON_HUNGER_DECAY = 3.0    # Loses 3 hunger per hour - needs regular feeding
DRAGON_HAPPINESS_DECAY = 1.0  # Loses 1 happiness per hour - needs attention
DRAGON_STAMINA_REGEN = 8.0    # Gains 8 stamina per hour (when resting)

# Stat thresholds
DRAGON_HUNGER_WARNING = 40.0  # BALANCE: Earlier warning
DRAGON_HAPPINESS_WARNING = 40.0
DRAGON_STAMINA_LOW = 25.0

# Feeding effects - generous to feel rewarding
DRAGON_FEED_HUNGER_RESTORE = 35.0
DRAGON_FEED_HAPPINESS_BONUS = 12.0
DRAGON_FEED_BOND_BONUS = 8

# Petting effects
DRAGON_PET_HAPPINESS = 18.0  # BALANCE: More rewarding
DRAGON_PET_BOND = 5

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

# Starting gold - enough to get started without feeling poor
STARTING_GOLD = 150

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
# ECONOMY SYSTEM
# =============================================================================
# Quality multipliers for pricing (1-5 stars)
QUALITY_PRICE_MULTIPLIERS = {
    1: 0.6,   # Poor quality
    2: 0.8,   # Below average
    3: 1.0,   # Average
    4: 1.25,  # Good
    5: 1.5,   # Excellent
}

# Reputation bonus tiers (every 100 reputation points)
REPUTATION_PRICE_BONUS = 0.05  # +5% per reputation tier

# Tip calculation
TIP_BASE_PERCENT = 0.10        # 10% base tip
TIP_SATISFACTION_BONUS = 0.05  # +5% per satisfaction level above 3
TIP_MAX_PERCENT = 0.30         # 30% max tip

# Upgrade definitions: (name, cost, type, amount)
UPGRADE_CARRIED_SLOTS = 'upgrade_carried'
UPGRADE_STORAGE_SLOTS = 'upgrade_storage'
UPGRADE_FRIDGE_SLOTS = 'upgrade_fridge'

UPGRADES = {
    UPGRADE_CARRIED_SLOTS: {
        'name': 'Expand Backpack',
        'description': 'Carry 5 more items while exploring',
        'cost': 500,
        'amount': 5,
        'max_purchases': 4,  # Can buy up to 4 times (20 + 20 = 40 slots max)
    },
    UPGRADE_STORAGE_SLOTS: {
        'name': 'Expand Storage',
        'description': 'Store 50 more items in cafe storage',
        'cost': 1000,
        'amount': 50,
        'max_purchases': 4,  # Can buy up to 4 times (100 + 200 = 300 slots max)
    },
    UPGRADE_FRIDGE_SLOTS: {
        'name': 'Expand Fridge',
        'description': 'Keep 10 more items fresh',
        'cost': 750,
        'amount': 10,
        'max_purchases': 5,  # Can buy up to 5 times (30 + 50 = 80 slots max)
    },
}

# =============================================================================
# RECIPE SYSTEM
# =============================================================================
# Recipe categories
RECIPE_CATEGORY_APPETIZER = 'appetizer'
RECIPE_CATEGORY_MAIN = 'main'
RECIPE_CATEGORY_DESSERT = 'dessert'
RECIPE_CATEGORY_BEVERAGE = 'beverage'

ALL_RECIPE_CATEGORIES = [
    RECIPE_CATEGORY_APPETIZER,
    RECIPE_CATEGORY_MAIN,
    RECIPE_CATEGORY_DESSERT,
    RECIPE_CATEGORY_BEVERAGE,
]

# Difficulty levels (1-5 stars)
RECIPE_DIFFICULTY_MIN = 1
RECIPE_DIFFICULTY_MAX = 5

# Base quality per difficulty
RECIPE_BASE_QUALITY = {
    1: 2,  # Easy recipes start at 2-star quality
    2: 2,
    3: 3,  # Medium recipes start at 3-star
    4: 3,
    5: 4,  # Hard recipes start at 4-star (harder but better base)
}

# Mastery requirements
RECIPE_MASTERY_COOK_COUNT = 10  # Cook 10 times to progress
RECIPE_MASTERY_PERFECT_COUNT = 5  # Need 5 perfect (5-star) cooks for full mastery

# Recipe unlock types
UNLOCK_TYPE_DEFAULT = 'default'       # Available from start
UNLOCK_TYPE_REPUTATION = 'reputation'  # Requires reputation level
UNLOCK_TYPE_STORY = 'story'           # Requires story progress
UNLOCK_TYPE_DISCOVERY = 'discovery'   # Found through exploration

# Recipe definitions
# Format: id -> {name, description, category, difficulty, base_price, ingredients, color_influence, unlock}
# ingredients: list of (item_id, quantity, min_quality)
# color_influence: (r, g, b) modifiers for dragon color (0.0-1.0)
# unlock: {type, requirement} - e.g., {type: 'reputation', requirement: 50}

RECIPES = {
    # =========================================================================
    # APPETIZERS (4) - Difficulty 1-2
    # =========================================================================
    'herb_salad': {
        'name': 'Fresh Herb Salad',
        'description': 'A light salad with garden herbs. Simple but refreshing.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 25,
        'ingredients': [
            ('garden_herb', 2, 1),
            ('edible_flower', 1, 1),
        ],
        'color_influence': (0.3, 0.7, 0.4),  # Green-heavy
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'berry_toast': {
        'name': 'Berry Toast',
        'description': 'Toasted bread topped with fresh wild berries.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 30,
        'ingredients': [
            ('wild_berry', 2, 1),
        ],
        'color_influence': (0.7, 0.3, 0.5),  # Red-pink
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'mushroom_skewers': {
        'name': 'Mushroom Skewers',
        'description': 'Grilled mushrooms on wooden skewers with herbs.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 2,
        'base_price': 40,
        'ingredients': [
            ('field_mushroom', 2, 2),
            ('wild_herb', 1, 1),
        ],
        'color_influence': (0.5, 0.5, 0.4),  # Earthy brown
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 20},
    },
    'honey_bites': {
        'name': 'Honey Glazed Bites',
        'description': 'Sweet bites glazed with golden honey.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 2,
        'base_price': 50,
        'ingredients': [
            ('golden_honey', 1, 1),
            ('meadow_berry', 1, 2),
        ],
        'color_influence': (0.8, 0.6, 0.3),  # Golden
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },

    # =========================================================================
    # MAINS (5) - Difficulty 2-4
    # =========================================================================
    'herb_stew': {
        'name': 'Garden Herb Stew',
        'description': 'A warm, comforting stew with fresh herbs and root vegetables.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 60,
        'ingredients': [
            ('garden_herb', 2, 1),
            ('wild_herb', 1, 1),
            ('buried_root', 1, 1),
        ],
        'color_influence': (0.4, 0.6, 0.3),  # Herby green
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'forest_fish_plate': {
        'name': 'Forest Stream Fish',
        'description': 'Pan-seared fish from the forest streams.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 85,
        'ingredients': [
            ('forest_fish', 1, 2),
            ('forest_herb', 1, 1),
            ('wild_herb', 1, 1),
        ],
        'color_influence': (0.3, 0.5, 0.7),  # Bluish
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 30},
    },
    'game_roast': {
        'name': 'Roasted Wild Game',
        'description': 'Tender wild game roasted with forest herbs.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 120,
        'ingredients': [
            ('wild_game', 1, 3),
            ('forest_herb', 2, 2),
            ('buried_root', 1, 2),
        ],
        'color_influence': (0.7, 0.4, 0.3),  # Meaty red-brown
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 50},
    },
    'mushroom_risotto': {
        'name': 'Rare Mushroom Risotto',
        'description': 'Creamy risotto with rare forest mushrooms.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 95,
        'ingredients': [
            ('rare_mushroom', 2, 2),
            ('field_mushroom', 1, 1),
            ('wild_herb', 1, 1),
        ],
        'color_influence': (0.5, 0.4, 0.5),  # Purple-brown
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'truffle_special': {
        'name': 'Truffle Special',
        'description': 'The cafe signature dish featuring hidden truffles.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 150,
        'ingredients': [
            ('hidden_truffle', 1, 3),
            ('rare_mushroom', 1, 2),
            ('golden_honey', 1, 2),
        ],
        'color_influence': (0.5, 0.4, 0.3),  # Earthy luxury
        'unlock': {'type': UNLOCK_TYPE_STORY, 'requirement': 'chapter_2'},
    },

    # =========================================================================
    # DESSERTS (4) - Difficulty 2-3
    # =========================================================================
    'berry_tart': {
        'name': 'Wild Berry Tart',
        'description': 'Sweet tart filled with fresh wild berries.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 2,
        'base_price': 45,
        'ingredients': [
            ('wild_berry', 2, 2),
            ('meadow_berry', 1, 1),
        ],
        'color_influence': (0.7, 0.2, 0.5),  # Berry purple-red
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'honey_cake': {
        'name': 'Golden Honey Cake',
        'description': 'Moist cake drizzled with golden honey.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 2,
        'base_price': 55,
        'ingredients': [
            ('golden_honey', 1, 2),
            ('edible_flower', 1, 1),
        ],
        'color_influence': (0.9, 0.7, 0.3),  # Golden yellow
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 25},
    },
    'flower_pudding': {
        'name': 'Flower Petal Pudding',
        'description': 'Delicate pudding with edible flower petals.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 3,
        'base_price': 65,
        'ingredients': [
            ('edible_flower', 3, 2),
            ('golden_honey', 1, 1),
        ],
        'color_influence': (0.6, 0.5, 0.7),  # Floral purple
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'crystal_sorbet': {
        'name': 'Crystal Sorbet',
        'description': 'Magical sorbet infused with crystal essence.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 3,
        'base_price': 100,
        'ingredients': [
            ('crystal_shard', 1, 2),
            ('meadow_berry', 2, 2),
            ('golden_honey', 1, 1),
        ],
        'color_influence': (0.5, 0.6, 0.9),  # Crystal blue
        'unlock': {'type': UNLOCK_TYPE_STORY, 'requirement': 'chapter_1'},
    },

    # =========================================================================
    # BEVERAGES (2) - Difficulty 1
    # =========================================================================
    'herb_tea': {
        'name': 'Herbal Tea',
        'description': 'Soothing tea brewed from fresh garden herbs.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 1,
        'base_price': 15,
        'ingredients': [
            ('garden_herb', 1, 1),
        ],
        'color_influence': (0.3, 0.6, 0.3),  # Green
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'berry_juice': {
        'name': 'Fresh Berry Juice',
        'description': 'Refreshing juice made from wild berries.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 1,
        'base_price': 20,
        'ingredients': [
            ('wild_berry', 2, 1),
            ('meadow_berry', 1, 1),
        ],
        'color_influence': (0.7, 0.3, 0.4),  # Berry red
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 10},
    },
}

# Default unlocked recipes (available from game start)
DEFAULT_UNLOCKED_RECIPES = [
    'herb_salad',
    'berry_toast',
    'herb_stew',
    'berry_tart',
    'herb_tea',
]

# =============================================================================
# COOKING MINIGAME
# =============================================================================
# Lane configuration (4 lanes)
COOKING_LANES = 4
COOKING_LANE_KEYS = ['a', 's', 'd', 'f']  # Keyboard keys for lanes
COOKING_LANE_KEYS_ALT = ['left', 'down', 'up', 'right']  # Arrow keys

# Timing windows (milliseconds)
# BALANCE: Generous windows for casual enjoyment, skill rewarded at PERFECT
TIMING_PERFECT = 75     # ±75ms for PERFECT (tight but achievable)
TIMING_GOOD = 125       # ±125ms for GOOD (comfortable)
TIMING_OK = 180         # ±180ms for OK (forgiving)
# Beyond ±180ms = MISS

# Timing grades
GRADE_PERFECT = 'perfect'
GRADE_GOOD = 'good'
GRADE_OK = 'ok'
GRADE_MISS = 'miss'

# Scoring - OK gives meaningful points, PERFECT highly rewarded
SCORE_PERFECT = 100
SCORE_GOOD = 65
SCORE_OK = 35
SCORE_MISS = 0

# Combo multipliers - achievable thresholds
COMBO_MULTIPLIER_THRESHOLDS = {
    3: 1.1,    # 3+ combo = 1.1x (early reward)
    7: 1.3,    # 7+ combo = 1.3x
    12: 1.6,   # 12+ combo = 1.6x
    20: 2.0,   # 20+ combo = 2.0x (skilled players)
}

# Note speed (pixels per second)
# BALANCE: Slower notes = more readable, less frantic
COOKING_NOTE_SPEED = 250
COOKING_NOTE_SPEED_EASY = 180  # Easy mode - very readable

# Note dimensions
COOKING_NOTE_WIDTH = 64  # Slightly wider for easier hits
COOKING_NOTE_HEIGHT = 22
COOKING_HIT_LINE_Y = 580  # Y position of hit line

# Game duration based on difficulty (seconds)
# BALANCE: Keep minigames short and snappy
COOKING_DURATION_BASE = 12  # 12 second base
COOKING_DURATION_PER_DIFFICULTY = 2  # +2 seconds per difficulty level

# Notes per second based on difficulty
# BALANCE: Lower density = more forgiving
COOKING_NOTES_PER_SECOND_BASE = 1.2
COOKING_NOTES_PER_SECOND_PER_DIFFICULTY = 0.25

# Quality score thresholds (percentage of max possible score)
# BALANCE: More forgiving thresholds for casual players
QUALITY_SCORE_THRESHOLDS = {
    1: 0.0,    # 0-29% = 1 star (really bad)
    2: 0.3,    # 30-49% = 2 stars (struggling)
    3: 0.5,    # 50-69% = 3 stars (decent - most players land here)
    4: 0.7,    # 70-84% = 4 stars (good!)
    5: 0.85,   # 85%+ = 5 stars (excellent)
}

# Ingredient quality bonus (multiplier to final score)
# BALANCE: Quality matters but doesn't punish harshly
INGREDIENT_QUALITY_BONUS = {
    1: 0.85,  # Poor ingredients = -15%
    2: 0.92,  # Below average = -8%
    3: 1.0,   # Average = no bonus
    4: 1.08,  # Good = +8%
    5: 1.15,  # Excellent = +15%
}

# Easy mode multiplier for timing windows
# BALANCE: Easy mode is significantly easier - 75% wider windows
EASY_MODE_TIMING_MULTIPLIER = 1.75

# Visual settings
COOKING_LANE_WIDTH = 80
COOKING_LANE_SPACING = 10
COOKING_LANE_COLORS = [
    (220, 80, 80),    # Red
    (80, 180, 80),    # Green
    (80, 120, 220),   # Blue
    (220, 180, 80),   # Yellow
]

# =============================================================================
# SETTINGS SYSTEM
# =============================================================================
# Volume settings (0-100)
DEFAULT_MASTER_VOLUME = 80
DEFAULT_SFX_VOLUME = 80
DEFAULT_MUSIC_VOLUME = 60

# Game speed options
GAME_SPEED_SLOW = 0.75
GAME_SPEED_NORMAL = 1.0
GAME_SPEED_FAST = 1.25
GAME_SPEED_OPTIONS = [GAME_SPEED_SLOW, GAME_SPEED_NORMAL, GAME_SPEED_FAST]
GAME_SPEED_LABELS = ['Slow (0.75x)', 'Normal (1x)', 'Fast (1.25x)']

# Cooking difficulty options
COOKING_DIFFICULTY_EASY = 'easy'
COOKING_DIFFICULTY_NORMAL = 'normal'
COOKING_DIFFICULTY_OPTIONS = [COOKING_DIFFICULTY_EASY, COOKING_DIFFICULTY_NORMAL]
COOKING_DIFFICULTY_LABELS = ['Easy', 'Normal']

# Display settings
DEFAULT_FULLSCREEN = False

# Settings file path
SETTINGS_FILE = 'settings.json'

# Default settings dict
DEFAULT_SETTINGS = {
    'master_volume': DEFAULT_MASTER_VOLUME,
    'sfx_volume': DEFAULT_SFX_VOLUME,
    'music_volume': DEFAULT_MUSIC_VOLUME,
    'game_speed': GAME_SPEED_NORMAL,
    'cooking_difficulty': COOKING_DIFFICULTY_NORMAL,
    'fullscreen': DEFAULT_FULLSCREEN,
}

# =============================================================================
# HUD SYSTEM
# =============================================================================
# HUD modes
HUD_MODE_EXPLORATION = 'exploration'
HUD_MODE_CAFE = 'cafe'

# HUD layout positions (screen coordinates)
HUD_MARGIN = 15  # Margin from screen edges

# Top-left: Player info
HUD_PLAYER_X = HUD_MARGIN
HUD_PLAYER_Y = HUD_MARGIN

# Top-right: Time/Date display
HUD_TIME_X = SCREEN_WIDTH - HUD_MARGIN
HUD_TIME_Y = HUD_MARGIN

# Top-center: Notifications
HUD_NOTIFICATION_X = SCREEN_WIDTH // 2
HUD_NOTIFICATION_Y = HUD_MARGIN + 10
HUD_NOTIFICATION_MAX = 3  # Max notifications shown
HUD_NOTIFICATION_DURATION = 5.0  # Seconds to display

# Bottom-left: Dragon status
HUD_DRAGON_X = HUD_MARGIN
HUD_DRAGON_Y = SCREEN_HEIGHT - HUD_MARGIN - 100

# Bottom-right: Minimap placeholder
HUD_MINIMAP_X = SCREEN_WIDTH - HUD_MARGIN - 100
HUD_MINIMAP_Y = SCREEN_HEIGHT - HUD_MARGIN - 100
HUD_MINIMAP_SIZE = 100

# Bottom-center: Quick inventory
HUD_QUICK_INV_Y = SCREEN_HEIGHT - HUD_MARGIN - 50
HUD_QUICK_INV_SLOTS = 8
HUD_QUICK_INV_SLOT_SIZE = 45
HUD_QUICK_INV_SPACING = 5

# Status bar dimensions
STATUS_BAR_WIDTH = 120
STATUS_BAR_HEIGHT = 12
STATUS_BAR_SPACING = 8

# HUD colors
HUD_BG_ALPHA = 180  # Background transparency
HUD_PANEL_COLOR = (30, 28, 40)
HUD_BORDER_COLOR = (60, 55, 75)

# Notification types and colors
NOTIFICATION_INFO = 'info'
NOTIFICATION_SUCCESS = 'success'
NOTIFICATION_WARNING = 'warning'
NOTIFICATION_ERROR = 'error'

NOTIFICATION_COLORS = {
    NOTIFICATION_INFO: (100, 140, 180),
    NOTIFICATION_SUCCESS: (80, 180, 100),
    NOTIFICATION_WARNING: (220, 180, 60),
    NOTIFICATION_ERROR: (220, 80, 80),
}

# Season/Weather icons (unicode characters for procedural drawing)
SEASON_ICONS = {
    'spring': 'flower',
    'summer': 'sun',
}

WEATHER_ICONS = {
    WEATHER_SUNNY: 'sun',
    WEATHER_CLOUDY: 'cloud',
    WEATHER_RAINY: 'rain',
}

# Mood face icons
MOOD_FACES = {
    'happy': ':D',
    'content': ':)',
    'neutral': ':|',
    'tired': ':/',
    'hungry': ':(',
    'sad': ':(',
    'incubating': 'o',
}

# =============================================================================
# GAME VERSION
# =============================================================================
VERSION = "0.1.0"
