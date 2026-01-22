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
DRAGON_ADOLESCENT = (80, 160, 110)
DRAGON_ADULT = (60, 140, 90)
DRAGON_WING = (80, 150, 110)
DRAGON_WING_MEMBRANE = (100, 180, 130)  # Slightly lighter for wing membranes
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

# Seasonal color palettes (for zone rendering adjustments)
SEASON_COLORS = {
    'spring': {
        'grass': (100, 180, 80),      # Bright green
        'leaves': (80, 160, 60),      # Fresh green
        'sky_tint': (200, 220, 255),  # Light blue
        'accent': (255, 180, 200),    # Pink blossoms
    },
    'summer': {
        'grass': (120, 160, 60),      # Yellow-green
        'leaves': (60, 140, 50),      # Deep green
        'sky_tint': (180, 200, 255),  # Clear blue
        'accent': (255, 220, 100),    # Golden
    },
    'autumn': {
        'grass': (140, 140, 80),      # Faded green
        'leaves': (200, 120, 60),     # Orange-brown
        'sky_tint': (220, 200, 180),  # Warm haze
        'accent': (180, 80, 40),      # Deep red
    },
    'winter': {
        'grass': (160, 170, 180),     # Frost-touched
        'leaves': (100, 110, 120),    # Gray-brown
        'sky_tint': (200, 210, 230),  # Cold blue
        'accent': (240, 245, 255),    # Snow white
    },
}

# Seasonal overlay tint (applied to entire scene, RGBA)
SEASON_OVERLAY = {
    'spring': (255, 240, 245, 10),   # Slight pink
    'summer': (255, 255, 220, 15),   # Warm yellow
    'autumn': (255, 220, 180, 20),   # Orange tint
    'winter': (220, 230, 255, 25),   # Cool blue
}

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

# Seasons
DAYS_PER_SEASON = 7  # BALANCE: Shorter seasons for variety (28-day year)
SEASONS = ['spring', 'summer', 'autumn', 'winter']

# Cafe operating hours
CAFE_OPEN_HOUR = 8   # Opens at 8 AM
CAFE_CLOSE_HOUR = 22  # Closes at 10 PM

# Cafe states
CAFE_STATE_CLOSED = 'closed'
CAFE_STATE_PREP = 'prep'
CAFE_STATE_SERVICE = 'service'
CAFE_STATE_CLEANUP = 'cleanup'

# Service periods
SERVICE_PERIOD_MORNING = 'morning'
SERVICE_PERIOD_EVENING = 'evening'

# Morning service (breakfast/lunch)
CAFE_MORNING_SERVICE_START = 10   # Service starts at 10 AM
CAFE_MORNING_SERVICE_END = 14     # Service ends at 2 PM
CAFE_MORNING_PREP_START = 9       # Prep starts at 9 AM
CAFE_MORNING_CLEANUP_END = 15     # Cleanup ends at 3 PM

# Evening service (dinner)
CAFE_EVENING_SERVICE_START = 17   # Service starts at 5 PM
CAFE_EVENING_SERVICE_END = 21     # Service ends at 9 PM
CAFE_EVENING_PREP_START = 16      # Prep starts at 4 PM
CAFE_EVENING_CLEANUP_END = 22     # Cleanup ends at 10 PM

# Backwards compatibility aliases
CAFE_SERVICE_START = CAFE_MORNING_SERVICE_START
CAFE_SERVICE_END = CAFE_MORNING_SERVICE_END
CAFE_PREP_DURATION = 1     # 1 hour prep before service
CAFE_CLEANUP_DURATION = 1  # 1 hour cleanup after service

# Service period customer volume multipliers
SERVICE_VOLUME_MULTIPLIER = {
    SERVICE_PERIOD_MORNING: 0.6,   # Lighter morning crowd
    SERVICE_PERIOD_EVENING: 1.0,   # Full evening crowd
}

# Service period category preferences (multiplier for customer wanting that category)
SERVICE_CATEGORY_PREFERENCE = {
    SERVICE_PERIOD_MORNING: {
        'beverage': 1.5,    # Coffee/tea popular in morning
        'appetizer': 1.3,   # Light bites for brunch
        'main': 0.8,        # Less demand for heavy meals
        'dessert': 0.9,     # Moderate dessert demand
    },
    SERVICE_PERIOD_EVENING: {
        'beverage': 0.8,    # Less beverage focus
        'appetizer': 1.0,   # Normal appetizer demand
        'main': 1.4,        # Dinner mains very popular
        'dessert': 1.3,     # Desserts popular after dinner
    },
}

# Menu settings
CAFE_MAX_MENU_ITEMS = 6    # Max dishes on menu at once
CAFE_SKIP_SERVICE_PENALTY = 5   # Reputation penalty for skipping a single service
CAFE_SKIP_DAY_PENALTY = 15      # Reputation penalty for skipping entire day
CAFE_SKIP_REP_PENALTY = 10      # Backwards compatibility

# =============================================================================
# REPUTATION SYSTEM
# =============================================================================
# Reputation range
REPUTATION_MIN = 0
REPUTATION_MAX = 1000  # Extended for Legendary tier

# Reputation levels (tier name, min reputation, max reputation)
REPUTATION_LEVEL_UNKNOWN = 'unknown'
REPUTATION_LEVEL_LOCAL = 'local_favorite'
REPUTATION_LEVEL_TOWN = 'town_attraction'
REPUTATION_LEVEL_REGIONAL = 'regional_fame'
REPUTATION_LEVEL_LEGENDARY = 'legendary'  # Phase 3: 5th tier

REPUTATION_LEVELS = {
    REPUTATION_LEVEL_UNKNOWN: {'min': 0, 'max': 49, 'name': 'Unknown'},
    REPUTATION_LEVEL_LOCAL: {'min': 50, 'max': 149, 'name': 'Local Favorite'},
    REPUTATION_LEVEL_TOWN: {'min': 150, 'max': 299, 'name': 'Town Attraction'},
    REPUTATION_LEVEL_REGIONAL: {'min': 300, 'max': 499, 'name': 'Regional Fame'},
    REPUTATION_LEVEL_LEGENDARY: {'min': 500, 'max': 1000, 'name': 'Legendary'},
}

# Customer count range per reputation level
REPUTATION_CUSTOMER_RANGE = {
    REPUTATION_LEVEL_UNKNOWN: (1, 2),
    REPUTATION_LEVEL_LOCAL: (2, 4),
    REPUTATION_LEVEL_TOWN: (3, 6),
    REPUTATION_LEVEL_REGIONAL: (5, 8),
    REPUTATION_LEVEL_LEGENDARY: (7, 10),  # VIP customer volume
}

# Daily reputation decay (if cafe not operated)
REPUTATION_DAILY_DECAY = 2

# Level up unlocks (reputation level -> list of unlocks)
REPUTATION_UNLOCKS = {
    REPUTATION_LEVEL_LOCAL: ['berry_juice', 'mushroom_skewers'],
    REPUTATION_LEVEL_TOWN: ['forest_fish_plate', 'honey_cake'],
    REPUTATION_LEVEL_REGIONAL: ['game_roast', 'all_recipes'],
    REPUTATION_LEVEL_LEGENDARY: ['legendary_dragon_feast', 'mythic_tea_ceremony'],
}

# Legendary tier bonus (25% tip bonus)
LEGENDARY_TIP_BONUS = 0.25

# =============================================================================
# CHARACTER AFFINITY SYSTEM
# =============================================================================
# Affinity range (per character)
AFFINITY_MIN = 0
AFFINITY_MAX = 100

# Affinity level thresholds
AFFINITY_LEVEL_ACQUAINTANCE = 'acquaintance'  # 0-24
AFFINITY_LEVEL_FRIENDLY = 'friendly'          # 25-49
AFFINITY_LEVEL_CLOSE = 'close'                # 50-74
AFFINITY_LEVEL_BEST_FRIEND = 'best_friend'    # 75-100

AFFINITY_LEVELS = {
    AFFINITY_LEVEL_ACQUAINTANCE: {'min': 0, 'max': 24, 'name': 'Acquaintance'},
    AFFINITY_LEVEL_FRIENDLY: {'min': 25, 'max': 49, 'name': 'Friendly'},
    AFFINITY_LEVEL_CLOSE: {'min': 50, 'max': 74, 'name': 'Close'},
    AFFINITY_LEVEL_BEST_FRIEND: {'min': 75, 'max': 100, 'name': 'Best Friend'},
}

# Affinity gains from interactions
AFFINITY_COOK_BASE = 5           # Base cooking for character
AFFINITY_COOK_QUALITY_BONUS = 5  # Extra for high quality (4-5 stars)
AFFINITY_COOK_FAVORITE = 15      # Cooking their favorite recipe
AFFINITY_COOK_LIKED = 8          # Cooking a liked recipe
AFFINITY_COOK_DISLIKED = -5      # Cooking a disliked recipe

AFFINITY_DIALOGUE_POSITIVE = 8   # Positive dialogue choice
AFFINITY_DIALOGUE_NEGATIVE = -5  # Negative dialogue choice

AFFINITY_GIFT_MIN = 3            # Minimum gift bonus
AFFINITY_GIFT_MAX = 15           # Maximum gift bonus (preferred items)

# Affinity unlock thresholds
AFFINITY_UNLOCK_PERSONAL_STORY = 25   # Personal stories unlock
AFFINITY_UNLOCK_SECRET_RECIPE = 50    # Secret recipes unlock
AFFINITY_UNLOCK_SPECIAL_EVENT = 75    # Special events unlock

# Secret recipes unlocked at Close affinity (50+)
CHARACTER_SECRET_RECIPES = {
    'mother': 'mothers_comfort_stew',
    'marcus': 'wanderers_secret_blend',
    'lily': 'lilys_perfect_souffle',
    'garrett': 'garretts_memory_bread',
    'vera': 'captains_treasure_catch',
    'noble': 'royal_midnight_feast',
    'elena': 'elenas_reconciliation_tea',
    'thomas': 'thomas_humble_pie',
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
# Life stages (5-stage progression)
DRAGON_STAGE_EGG = 'egg'
DRAGON_STAGE_HATCHLING = 'hatchling'
DRAGON_STAGE_JUVENILE = 'juvenile'
DRAGON_STAGE_ADOLESCENT = 'adolescent'
DRAGON_STAGE_ADULT = 'adult'

# All stages in order (for iteration)
DRAGON_STAGES = [
    DRAGON_STAGE_EGG,
    DRAGON_STAGE_HATCHLING,
    DRAGON_STAGE_JUVENILE,
    DRAGON_STAGE_ADOLESCENT,
    DRAGON_STAGE_ADULT,
]

# Stage progression (days alive)
# BALANCE: Adjusted for prototype pacing (full growth in ~2 hours real time)
# At 12 real min/day: Full adult in ~2 hours of play
DRAGON_EGG_DAYS = 1          # Day 1: Egg (hatches quickly!)
DRAGON_HATCHLING_DAYS = 2    # Days 2-3: Hatchling (small, cute)
DRAGON_JUVENILE_DAYS = 2     # Days 4-5: Juvenile (cat-sized, playful)
DRAGON_ADOLESCENT_DAYS = 4   # Days 6-9: Adolescent (horse-sized, wing buds)
# Days 10+: Adult (full wingspan, majestic)

# Stat ranges
DRAGON_STAT_MAX = 100.0
DRAGON_BOND_MAX = 500  # BALANCE: Lower max for achievable progression

# Max stamina scales by stage (allows longer exploration as dragon grows)
DRAGON_STAGE_STAMINA_MAX = {
    DRAGON_STAGE_EGG: 100,        # Eggs don't use stamina
    DRAGON_STAGE_HATCHLING: 100,  # Base stamina
    DRAGON_STAGE_JUVENILE: 100,   # Still base stamina
    DRAGON_STAGE_ADOLESCENT: 125, # 25% increase
    DRAGON_STAGE_ADULT: 150,      # 50% increase
}

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

# Dragon naming
DRAGON_NAME_MAX_LENGTH = 20
DRAGON_NAME_DEFAULT = "Dragon"

# Ability stamina costs (one-time cost for instant abilities)
DRAGON_ABILITY_COSTS = {
    'burrow_fetch': 20,   # Hatchling+: Dig up buried items
    'sniff_track': 15,    # Hatchling+: Find hidden resources
    'rock_smash': 30,     # Juvenile+: Break rocks for minerals
    'creature_scare': 20, # Juvenile+: Frighten hostile creatures
    'ember_breath': 25,   # Adolescent+: Light torches, clear brambles
    'fire_breath': 40,    # Adolescent+: Cook items, clear obstacles
    'flight_scout': 50,   # Adult: Reveal resources in adjacent zones
    'fire_stream': 40,    # Adult: Clear major obstacles
}

# Continuous abilities drain stamina per second while active
DRAGON_ABILITY_CONTINUOUS = {
    'glide': 3,           # Adolescent+: Descend safely from heights
    'full_flight': 5,     # Adult: Fast travel, access flight-only areas
}

# All abilities combined for validation
DRAGON_ALL_ABILITIES = list(DRAGON_ABILITY_COSTS.keys()) + list(DRAGON_ABILITY_CONTINUOUS.keys())

# Abilities unlocked per stage
DRAGON_STAGE_ABILITIES = {
    DRAGON_STAGE_EGG: [],
    DRAGON_STAGE_HATCHLING: ['burrow_fetch', 'sniff_track'],
    DRAGON_STAGE_JUVENILE: ['burrow_fetch', 'sniff_track', 'rock_smash', 'creature_scare'],
    DRAGON_STAGE_ADOLESCENT: ['burrow_fetch', 'sniff_track', 'rock_smash', 'creature_scare',
                              'ember_breath', 'fire_breath', 'glide'],
    DRAGON_STAGE_ADULT: ['burrow_fetch', 'sniff_track', 'rock_smash', 'creature_scare',
                         'ember_breath', 'fire_breath', 'glide', 'flight_scout',
                         'full_flight', 'fire_stream'],
}

# Ability descriptions for UI
DRAGON_ABILITY_DESCRIPTIONS = {
    'burrow_fetch': "Dig up buried items",
    'sniff_track': "Find hidden resources",
    'rock_smash': "Break rocks for minerals",
    'creature_scare': "Frighten hostile creatures",
    'ember_breath': "Light torches, clear brambles",
    'fire_breath': "Cook items, clear obstacles",
    'flight_scout': "Reveal distant resources",
    'fire_stream': "Clear major obstacles",
    'glide': "Descend safely from heights",
    'full_flight': "Fast travel, access sky areas",
}

# Stage descriptions for UI
DRAGON_STAGE_DESCRIPTIONS = {
    DRAGON_STAGE_EGG: "A mysterious dragon egg, warm to the touch.",
    DRAGON_STAGE_HATCHLING: "A tiny hatchling, curious and playful.",
    DRAGON_STAGE_JUVENILE: "A cat-sized dragon, eager to explore.",
    DRAGON_STAGE_ADOLESCENT: "A horse-sized dragon with growing wing buds.",
    DRAGON_STAGE_ADULT: "A majestic adult dragon with full wingspan.",
}

# Stage sizes for rendering (scale multiplier)
DRAGON_STAGE_SIZES = {
    DRAGON_STAGE_EGG: 1.0,
    DRAGON_STAGE_HATCHLING: 1.0,
    DRAGON_STAGE_JUVENILE: 1.2,
    DRAGON_STAGE_ADOLESCENT: 1.6,
    DRAGON_STAGE_ADULT: 2.0,
}

# =============================================================================
# CREATURE SYSTEM (Phase 3)
# =============================================================================
# Creature types
CREATURE_FOREST_SPRITE = 'forest_sprite'
CREATURE_WILD_BOAR = 'wild_boar'
CREATURE_CLIFF_BIRD = 'cliff_bird'
CREATURE_SHORE_CRAB = 'shore_crab'
CREATURE_CAVE_BAT = 'cave_bat'
# Sky Islands creatures (Phase 3)
CREATURE_SKY_SERPENT = 'sky_serpent'
CREATURE_CLOUD_WISP = 'cloud_wisp'
CREATURE_STORM_HAWK = 'storm_hawk'

ALL_CREATURE_TYPES = [
    CREATURE_FOREST_SPRITE, CREATURE_WILD_BOAR, CREATURE_CLIFF_BIRD,
    CREATURE_SHORE_CRAB, CREATURE_CAVE_BAT,
    CREATURE_SKY_SERPENT, CREATURE_CLOUD_WISP, CREATURE_STORM_HAWK
]

# Creature behavior types
CREATURE_BEHAVIOR_PATROL = 'patrol'       # Wander between waypoints
CREATURE_BEHAVIOR_FLEE = 'flee'           # Run from player/dragon
CREATURE_BEHAVIOR_GUARD = 'guard'         # Block until cleared
CREATURE_BEHAVIOR_FOLLOW = 'follow'       # Accompany player temporarily
CREATURE_BEHAVIOR_STATIONARY = 'stationary'  # Stay in place

# Creature definitions: name, behavior, hostile, zones, drops, dragon_ability
# Note: zones use strings to avoid forward reference issues
CREATURE_DATA = {
    CREATURE_FOREST_SPRITE: {
        'name': 'Forest Sprite',
        'behavior': CREATURE_BEHAVIOR_PATROL,
        'hostile': False,
        'zones': ['forest_depths', 'meadow_fields'],
        'drops': ['rare_flower', 'golden_honey'],
        'dragon_ability': None,  # Friendly - feed for bonuses
        'color': (140, 220, 180),  # Soft green glow
        'speed': 1.5,
    },
    CREATURE_WILD_BOAR: {
        'name': 'Wild Boar',
        'behavior': CREATURE_BEHAVIOR_GUARD,
        'hostile': True,
        'zones': ['forest_depths', 'mountain_pass'],
        'drops': ['wild_game'],
        'dragon_ability': 'creature_scare',
        'color': (120, 80, 60),  # Brown
        'speed': 2.0,
    },
    CREATURE_CLIFF_BIRD: {
        'name': 'Cliff Bird',
        'behavior': CREATURE_BEHAVIOR_FLEE,
        'hostile': False,
        'zones': ['mountain_pass', 'coastal_shore'],
        'drops': ['rare_flower', 'alpine_flower'],
        'dragon_ability': 'glide',  # Need glide to reach nests
        'color': (200, 180, 140),  # Tan feathers
        'speed': 3.0,
    },
    CREATURE_SHORE_CRAB: {
        'name': 'Shore Crab',
        'behavior': CREATURE_BEHAVIOR_GUARD,
        'hostile': True,
        'zones': ['coastal_shore'],
        'drops': ['coastal_crab', 'pearl_oyster'],
        'dragon_ability': 'rock_smash',
        'color': (180, 100, 80),  # Reddish shell
        'speed': 1.0,
    },
    CREATURE_CAVE_BAT: {
        'name': 'Cave Bat',
        'behavior': CREATURE_BEHAVIOR_FLEE,
        'hostile': False,
        'zones': ['ancient_ruins'],
        'drops': ['rare_mushroom', 'crystal_shard'],
        'dragon_ability': 'ember_breath',  # Light reveals them
        'color': (80, 70, 90),  # Dark purple
        'speed': 2.5,
    },
    # Sky Islands creatures
    CREATURE_SKY_SERPENT: {
        'name': 'Sky Serpent',
        'behavior': CREATURE_BEHAVIOR_PATROL,
        'hostile': False,
        'zones': ['sky_islands'],
        'drops': ['cloud_essence', 'sky_crystal'],
        'dragon_ability': None,  # Majestic, non-hostile
        'color': (180, 200, 255),  # Iridescent blue
        'speed': 2.0,
    },
    CREATURE_CLOUD_WISP: {
        'name': 'Cloud Wisp',
        'behavior': CREATURE_BEHAVIOR_FOLLOW,
        'hostile': False,
        'zones': ['sky_islands'],
        'drops': ['starlight_nectar', 'rainbow_essence'],
        'dragon_ability': None,  # Guides to resources
        'color': (255, 255, 230),  # Glowing white-gold
        'speed': 1.5,
    },
    CREATURE_STORM_HAWK: {
        'name': 'Storm Hawk',
        'behavior': CREATURE_BEHAVIOR_GUARD,
        'hostile': True,
        'zones': ['sky_islands'],
        'drops': ['phoenix_feather', 'lightning_crystal'],
        'dragon_ability': 'fire_breath',  # Challenge for rewards
        'color': (100, 80, 120),  # Stormy purple
        'speed': 3.5,
    },
}

# Creature spawn settings per zone (using string zone IDs)
CREATURE_SPAWN_POINTS = {
    'meadow_fields': [
        (CREATURE_FOREST_SPRITE, 8, 6),
        (CREATURE_FOREST_SPRITE, 14, 12),
    ],
    'forest_depths': [
        (CREATURE_FOREST_SPRITE, 5, 8),
        (CREATURE_WILD_BOAR, 12, 10),
        (CREATURE_WILD_BOAR, 18, 14),
    ],
    'coastal_shore': [
        (CREATURE_CLIFF_BIRD, 16, 4),
        (CREATURE_SHORE_CRAB, 8, 12),
        (CREATURE_SHORE_CRAB, 14, 15),
    ],
    'mountain_pass': [
        (CREATURE_WILD_BOAR, 10, 8),
        (CREATURE_CLIFF_BIRD, 6, 4),
        (CREATURE_CLIFF_BIRD, 18, 6),
    ],
    'ancient_ruins': [
        (CREATURE_CAVE_BAT, 8, 10),
        (CREATURE_CAVE_BAT, 14, 8),
        (CREATURE_CAVE_BAT, 10, 14),
    ],
    'sky_islands': [
        (CREATURE_SKY_SERPENT, 7, 5),
        (CREATURE_SKY_SERPENT, 12, 12),
        (CREATURE_CLOUD_WISP, 4, 8),
        (CREATURE_CLOUD_WISP, 10, 6),
        (CREATURE_STORM_HAWK, 8, 14),
    ],
}

# Creature interaction rewards
CREATURE_FEED_BOND_BONUS = 5      # Bond bonus for feeding friendly creatures
CREATURE_SCARE_STAMINA_COST = 20  # Stamina to scare hostile creatures
CREATURE_RESPAWN_HOURS = 4        # Hours until scared creatures return

# =============================================================================
# ACHIEVEMENTS SYSTEM (Phase 3)
# =============================================================================
# Achievement categories
ACHIEVEMENT_CAT_DRAGON = 'dragon'
ACHIEVEMENT_CAT_CAFE = 'cafe'
ACHIEVEMENT_CAT_EXPLORATION = 'exploration'
ACHIEVEMENT_CAT_STORY = 'story'

# Achievement definitions: id -> {name, description, category, condition, reward}
ACHIEVEMENTS = {
    # Dragon Milestones (5)
    'dragon_first_steps': {
        'name': 'First Steps',
        'description': 'Hatch your dragon egg',
        'category': ACHIEVEMENT_CAT_DRAGON,
        'condition': {'type': 'dragon_stage', 'value': 'hatchling'},
        'reward': {'gold': 50},
    },
    'dragon_growing_up': {
        'name': 'Growing Up',
        'description': 'Raise your dragon to Juvenile stage',
        'category': ACHIEVEMENT_CAT_DRAGON,
        'condition': {'type': 'dragon_stage', 'value': 'juvenile'},
        'reward': {'gold': 100},
    },
    'dragon_coming_of_age': {
        'name': 'Coming of Age',
        'description': 'Raise your dragon to Adolescent stage',
        'category': ACHIEVEMENT_CAT_DRAGON,
        'condition': {'type': 'dragon_stage', 'value': 'adolescent'},
        'reward': {'gold': 200},
    },
    'dragon_full_grown': {
        'name': 'Full Grown',
        'description': 'Raise your dragon to Adult stage',
        'category': ACHIEVEMENT_CAT_DRAGON,
        'condition': {'type': 'dragon_stage', 'value': 'adult'},
        'reward': {'gold': 500},
    },
    'dragon_best_friends': {
        'name': 'Best Friends',
        'description': 'Reach maximum bond level (100) with your dragon',
        'category': ACHIEVEMENT_CAT_DRAGON,
        'condition': {'type': 'dragon_bond', 'value': 100},
        'reward': {'gold': 300},
    },

    # Cafe Milestones (6)
    'cafe_grand_opening': {
        'name': 'Grand Opening',
        'description': 'Complete your first cafe service',
        'category': ACHIEVEMENT_CAT_CAFE,
        'condition': {'type': 'service_count', 'value': 1},
        'reward': {'gold': 25},
    },
    'cafe_rising_star': {
        'name': 'Rising Star',
        'description': 'Reach 100 reputation',
        'category': ACHIEVEMENT_CAT_CAFE,
        'condition': {'type': 'reputation', 'value': 100},
        'reward': {'gold': 100},
    },
    'cafe_expert_chef': {
        'name': 'Expert Chef',
        'description': 'Reach 200 reputation',
        'category': ACHIEVEMENT_CAT_CAFE,
        'condition': {'type': 'reputation', 'value': 200},
        'reward': {'gold': 200},
    },
    'cafe_master_chef': {
        'name': 'Master Chef',
        'description': 'Reach 350 reputation',
        'category': ACHIEVEMENT_CAT_CAFE,
        'condition': {'type': 'reputation', 'value': 350},
        'reward': {'gold': 300},
    },
    'cafe_legendary': {
        'name': 'Legendary Status',
        'description': 'Reach 500 reputation (Legendary tier)',
        'category': ACHIEVEMENT_CAT_CAFE,
        'condition': {'type': 'reputation', 'value': 500},
        'reward': {'gold': 500},
    },
    'cafe_recipe_collector': {
        'name': 'Recipe Collector',
        'description': 'Unlock 50 recipes',
        'category': ACHIEVEMENT_CAT_CAFE,
        'condition': {'type': 'recipes_unlocked', 'value': 50},
        'reward': {'gold': 250},
    },

    # Exploration Milestones (4)
    'explore_all_zones': {
        'name': 'Explorer',
        'description': 'Visit all exploration zones',
        'category': ACHIEVEMENT_CAT_EXPLORATION,
        'condition': {'type': 'zones_visited', 'value': 7},
        'reward': {'gold': 200},
    },
    'explore_gatherer': {
        'name': 'Gatherer',
        'description': 'Collect 100 ingredients total',
        'category': ACHIEVEMENT_CAT_EXPLORATION,
        'condition': {'type': 'ingredients_gathered', 'value': 100},
        'reward': {'gold': 150},
    },
    'explore_treasure_hunter': {
        'name': 'Treasure Hunter',
        'description': 'Find 10 rare resources',
        'category': ACHIEVEMENT_CAT_EXPLORATION,
        'condition': {'type': 'rare_found', 'value': 10},
        'reward': {'gold': 300},
    },
    'explore_dragon_master': {
        'name': 'Dragon Master',
        'description': 'Unlock all dragon abilities',
        'category': ACHIEVEMENT_CAT_EXPLORATION,
        'condition': {'type': 'abilities_unlocked', 'value': 10},
        'reward': {'gold': 400},
    },

    # Story Milestones (9)
    'story_chapter_1': {
        'name': 'Chapter I Complete',
        'description': 'Complete Chapter 1 of the story',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 1},
        'reward': {'gold': 50},
    },
    'story_chapter_2': {
        'name': 'Chapter II Complete',
        'description': 'Complete Chapter 2 of the story',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 2},
        'reward': {'gold': 75},
    },
    'story_chapter_3': {
        'name': 'Chapter III Complete',
        'description': 'Complete Chapter 3 of the story',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 3},
        'reward': {'gold': 100},
    },
    'story_chapter_4': {
        'name': 'Chapter IV Complete',
        'description': 'Complete Chapter 4 of the story',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 4},
        'reward': {'gold': 125},
    },
    'story_chapter_5': {
        'name': 'Chapter V Complete',
        'description': 'Complete Chapter 5 of the story',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 5},
        'reward': {'gold': 150},
    },
    'story_chapter_6': {
        'name': 'Chapter VI Complete',
        'description': 'Complete Chapter 6 of the story',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 6},
        'reward': {'gold': 175},
    },
    'story_chapter_7': {
        'name': 'Chapter VII Complete',
        'description': 'Complete Chapter 7 of the story',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 7},
        'reward': {'gold': 200},
    },
    'story_chapter_8': {
        'name': 'Chapter VIII Complete',
        'description': 'Complete the final chapter',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'chapter_complete', 'value': 8},
        'reward': {'gold': 500},
    },
    'story_true_friend': {
        'name': 'True Friend',
        'description': 'Reach maximum affinity with any character',
        'category': ACHIEVEMENT_CAT_STORY,
        'condition': {'type': 'max_affinity', 'value': True},
        'reward': {'gold': 250},
    },
}

# Total achievement count for validation
ACHIEVEMENT_COUNT = len(ACHIEVEMENTS)  # Should be 24

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
ZONE_COASTAL_SHORE = 'coastal_shore'
ZONE_MOUNTAIN_PASS = 'mountain_pass'
ZONE_ANCIENT_RUINS = 'ancient_ruins'
ZONE_SKY_ISLANDS = 'sky_islands'

# All zones for iteration
ALL_ZONES = [
    ZONE_CAFE_GROUNDS, ZONE_MEADOW_FIELDS, ZONE_FOREST_DEPTHS,
    ZONE_COASTAL_SHORE, ZONE_MOUNTAIN_PASS, ZONE_ANCIENT_RUINS,
    ZONE_SKY_ISLANDS,
]

# Zone unlock requirements (dragon stage)
ZONE_UNLOCK_REQUIREMENTS = {
    ZONE_CAFE_GROUNDS: None,  # Always unlocked
    ZONE_MEADOW_FIELDS: DRAGON_STAGE_HATCHLING,
    ZONE_FOREST_DEPTHS: DRAGON_STAGE_JUVENILE,
    ZONE_COASTAL_SHORE: DRAGON_STAGE_JUVENILE,  # Same as Forest
    ZONE_MOUNTAIN_PASS: DRAGON_STAGE_ADOLESCENT,  # Requires Adolescent
    ZONE_ANCIENT_RUINS: DRAGON_STAGE_ADOLESCENT,  # Requires Adolescent
    ZONE_SKY_ISLANDS: DRAGON_STAGE_ADULT,  # Requires Adult (flight)
}

# Zone connections (which zones connect to which)
ZONE_CONNECTIONS = {
    ZONE_CAFE_GROUNDS: [ZONE_MEADOW_FIELDS],
    ZONE_MEADOW_FIELDS: [ZONE_CAFE_GROUNDS, ZONE_FOREST_DEPTHS, ZONE_MOUNTAIN_PASS],
    ZONE_FOREST_DEPTHS: [ZONE_MEADOW_FIELDS, ZONE_COASTAL_SHORE, ZONE_ANCIENT_RUINS],
    ZONE_COASTAL_SHORE: [ZONE_FOREST_DEPTHS],
    ZONE_MOUNTAIN_PASS: [ZONE_MEADOW_FIELDS, ZONE_SKY_ISLANDS],
    ZONE_ANCIENT_RUINS: [ZONE_FOREST_DEPTHS],
    ZONE_SKY_ISLANDS: [ZONE_MOUNTAIN_PASS],
}

# Zone map sizes (tiles)
ZONE_WIDTH = 20
ZONE_HEIGHT = 15
TILE_SIZE = 32

# Weather types
WEATHER_SUNNY = 'sunny'
WEATHER_CLOUDY = 'cloudy'
WEATHER_RAINY = 'rainy'
WEATHER_STORMY = 'stormy'
WEATHER_SPECIAL = 'special'

ALL_WEATHER = [WEATHER_SUNNY, WEATHER_CLOUDY, WEATHER_RAINY, WEATHER_STORMY, WEATHER_SPECIAL]

# Weather probabilities per season (must sum to 1.0)
# Stormy: ~10%, Special: ~5% (varies by season)
WEATHER_PROBABILITIES = {
    'spring': {
        WEATHER_SUNNY: 0.35, WEATHER_CLOUDY: 0.30, WEATHER_RAINY: 0.20,
        WEATHER_STORMY: 0.10, WEATHER_SPECIAL: 0.05,
    },
    'summer': {
        WEATHER_SUNNY: 0.50, WEATHER_CLOUDY: 0.25, WEATHER_RAINY: 0.08,
        WEATHER_STORMY: 0.12, WEATHER_SPECIAL: 0.05,  # More summer storms
    },
    'autumn': {
        WEATHER_SUNNY: 0.30, WEATHER_CLOUDY: 0.32, WEATHER_RAINY: 0.20,
        WEATHER_STORMY: 0.12, WEATHER_SPECIAL: 0.06,  # Autumn is magical
    },
    'winter': {
        WEATHER_SUNNY: 0.22, WEATHER_CLOUDY: 0.40, WEATHER_RAINY: 0.20,
        WEATHER_STORMY: 0.10, WEATHER_SPECIAL: 0.08,  # Winter special events
    },
}

# Weather effects on resource spawn rates
WEATHER_RESOURCE_MULTIPLIER = {
    WEATHER_SUNNY: 1.0,
    WEATHER_CLOUDY: 1.1,  # Slightly more resources
    WEATHER_RAINY: 1.3,   # Best for foraging
    WEATHER_STORMY: 1.5,  # Rare storm resources appear
    WEATHER_SPECIAL: 2.0,  # Legendary resources appear
}

# Weather behavior flags
WEATHER_CLOSES_CAFE = {
    WEATHER_SUNNY: False,
    WEATHER_CLOUDY: False,
    WEATHER_RAINY: False,
    WEATHER_STORMY: True,   # Cafe closes during storms
    WEATHER_SPECIAL: False,  # Cafe stays open for special events
}

WEATHER_DANGER_LEVEL = {
    WEATHER_SUNNY: 0,    # Safe
    WEATHER_CLOUDY: 0,   # Safe
    WEATHER_RAINY: 0,    # Safe
    WEATHER_STORMY: 2,   # Dangerous - warnings shown
    WEATHER_SPECIAL: 0,  # Safe
}

# Special weather event types (for WEATHER_SPECIAL)
SPECIAL_WEATHER_EVENTS = {
    'spring': ['rainbow', 'blossom_shower'],
    'summer': ['meteor_shower', 'golden_hour'],
    'autumn': ['aurora', 'harvest_moon'],
    'winter': ['northern_lights', 'diamond_dust'],
}

# Special weather event descriptions
SPECIAL_WEATHER_DESCRIPTIONS = {
    'rainbow': 'A beautiful rainbow arches across the sky!',
    'blossom_shower': 'Flower petals drift gently through the air.',
    'meteor_shower': 'Shooting stars streak across the night sky!',
    'golden_hour': 'The world is bathed in magical golden light.',
    'aurora': 'Mystical lights dance on the horizon.',
    'harvest_moon': 'A giant amber moon illuminates the land.',
    'northern_lights': 'Ethereal ribbons of light shimmer above.',
    'diamond_dust': 'Tiny ice crystals sparkle like diamonds.',
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

# Quality bonuses per season (ingredient type -> bonus stars)
QUALITY_SEASON_BONUS = {
    'spring': {'herb': 1, 'flower': 1, 'berry': 0},
    'summer': {'berry': 1, 'honey': 1, 'herb': 0},
    'autumn': {'mushroom': 1, 'root': 1, 'grain': 1},
    'winter': {'preserved': 1, 'meat': 1, 'fish': 0},
}

# Popular dish types per season (affects customer preferences)
SEASON_POPULAR_DISHES = {
    'spring': ['salad', 'tea', 'light'],
    'summer': ['cold', 'refreshing', 'fruit'],
    'autumn': ['soup', 'stew', 'hearty'],
    'winter': ['warm', 'roasted', 'comfort'],
}

QUALITY_WEATHER_BONUS = {
    WEATHER_SUNNY: {'honey': 1, 'berry': 0},
    WEATHER_CLOUDY: {'mushroom': 1, 'herb': 0},
    WEATHER_RAINY: {'herb': 1, 'mushroom': 1, 'fish': 1},
    WEATHER_STORMY: {'storm': 2, 'crystal': 1},  # Storm-exclusive resources get bonus
    WEATHER_SPECIAL: {'legendary': 2, 'crystal': 1},  # Legendary items get bonus
}

# Dragon ability requirements for certain spawn points
ABILITY_BURROW = 'burrow_fetch'
ABILITY_SNIFF = 'sniff_track'
ABILITY_SMASH = 'rock_smash'
ABILITY_GLIDE = 'glide'
ABILITY_FLIGHT = 'full_flight'

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

    # Storm-exclusive ingredients (only spawn during stormy weather)
    'storm_flower': ('Storm Flower', ITEM_SPECIAL, 60, 2, (0.3, 0.4, 0.9)),  # Electric blue
    'lightning_crystal': ('Lightning Crystal', ITEM_SPECIAL, 80, 0, (0.9, 0.9, 0.4)),  # Never spoils

    # Special weather legendary ingredients (only spawn during special weather)
    'stardust_petal': ('Stardust Petal', ITEM_SPECIAL, 100, 3, (0.8, 0.6, 0.9)),  # Meteor shower
    'rainbow_essence': ('Rainbow Essence', ITEM_SPECIAL, 120, 0, (0.7, 0.7, 0.7)),  # Rainbow, never spoils
    'moonbeam_honey': ('Moonbeam Honey', ITEM_SPECIAL, 90, 0, (0.6, 0.7, 0.9)),  # Harvest moon, never spoils

    # Coastal Shore ingredients - Seafood and beach finds
    'sea_salt': ('Sea Salt', ITEM_SPICE, 12, 0, (0.9, 0.9, 0.9)),  # Never spoils
    'fresh_seaweed': ('Fresh Seaweed', ITEM_VEGETABLE, 15, 2, (0.2, 0.5, 0.3)),
    'coastal_crab': ('Coastal Crab', ITEM_SEAFOOD, 35, 1, (0.8, 0.4, 0.3)),
    'pearl_oyster': ('Pearl Oyster', ITEM_SEAFOOD, 50, 1, (0.7, 0.7, 0.8)),
    'tidal_clam': ('Tidal Clam', ITEM_SEAFOOD, 25, 1, (0.6, 0.5, 0.5)),
    'beach_berry': ('Beach Berry', ITEM_FRUIT, 18, 2, (0.6, 0.2, 0.4)),

    # Mountain Pass ingredients - Rare herbs and minerals
    'mountain_herb': ('Mountain Herb', ITEM_SPICE, 28, 3, (0.3, 0.7, 0.5)),
    'rock_honey': ('Rock Honey', ITEM_SPECIAL, 40, 0, (0.8, 0.6, 0.2)),  # Never spoils
    'mineral_crystal': ('Mineral Crystal', ITEM_SPECIAL, 55, 0, (0.6, 0.8, 0.9)),  # Never spoils
    'alpine_flower': ('Alpine Flower', ITEM_SPECIAL, 35, 2, (0.9, 0.5, 0.7)),
    'mountain_moss': ('Mountain Moss', ITEM_VEGETABLE, 22, 3, (0.4, 0.6, 0.3)),
    'hot_spring_egg': ('Hot Spring Egg', ITEM_SPECIAL, 45, 0, (0.9, 0.9, 0.7)),  # Never spoils

    # Ancient Ruins ingredients - Magical and preserved
    'ancient_spice': ('Ancient Spice', ITEM_SPICE, 45, 0, (0.7, 0.5, 0.3)),  # Preserved, never spoils
    'ruin_moss': ('Ruin Moss', ITEM_VEGETABLE, 35, 3, (0.3, 0.5, 0.4)),  # Magical moss
    'crystal_flower': ('Crystal Flower', ITEM_SPECIAL, 65, 0, (0.7, 0.8, 0.9)),  # Grows from crystal, never spoils
    'dragon_scale_herb': ('Dragon Scale Herb', ITEM_SPICE, 55, 2, (0.6, 0.4, 0.3)),  # Resembles scales
    'forgotten_grain': ('Forgotten Grain', ITEM_VEGETABLE, 40, 4, (0.8, 0.7, 0.5)),  # Ancient grain variety
    'mystic_mushroom': ('Mystic Mushroom', ITEM_VEGETABLE, 50, 2, (0.5, 0.4, 0.7)),  # Glowing mushroom
    'ancient_honey': ('Ancient Honey', ITEM_SPECIAL, 70, 0, (0.9, 0.6, 0.3)),  # Crystallized, never spoils
    'ruin_berry': ('Ruin Berry', ITEM_FRUIT, 38, 2, (0.6, 0.3, 0.5)),  # Wild berries in ruins

    # Sky Islands ingredients - Legendary and mythical
    'cloud_essence': ('Cloud Essence', ITEM_SPECIAL, 150, 0, (0.9, 0.95, 1.0)),  # Never spoils
    'sky_crystal': ('Sky Crystal', ITEM_SPECIAL, 180, 0, (0.7, 0.85, 1.0)),  # Never spoils
    'celestial_berry': ('Celestial Berry', ITEM_FRUIT, 120, 3, (0.8, 0.7, 0.9)),  # Floating island berries
    'wind_flower': ('Wind Flower', ITEM_SPECIAL, 140, 2, (0.9, 0.9, 1.0)),  # Flowers on air currents
    'starlight_nectar': ('Starlight Nectar', ITEM_SPECIAL, 200, 0, (1.0, 0.95, 0.8)),  # Never spoils
    'dragon_tear': ('Dragon Tear', ITEM_SPECIAL, 250, 0, (0.6, 0.8, 1.0)),  # Legendary, never spoils
    'phoenix_feather': ('Phoenix Feather', ITEM_SPECIAL, 300, 0, (1.0, 0.6, 0.3)),  # Mythical, never spoils
    'sky_honey': ('Sky Honey', ITEM_SPECIAL, 160, 0, (1.0, 0.9, 0.6)),  # Never spoils

    # Common cooking ingredients - Used across many recipes
    'honey': ('Honey', ITEM_SPECIAL, 15, 0, (0.9, 0.7, 0.2)),  # Generic honey, never spoils
    'herb': ('Herb', ITEM_SPICE, 8, 3, (0.3, 0.7, 0.3)),  # Generic cooking herb
    'berry': ('Berry', ITEM_FRUIT, 10, 2, (0.8, 0.2, 0.4)),  # Generic berry
    'mushroom': ('Mushroom', ITEM_VEGETABLE, 12, 2, (0.5, 0.4, 0.3)),  # Generic mushroom
    'flour': ('Flour', ITEM_VEGETABLE, 8, 0, (0.95, 0.95, 0.9)),  # Never spoils
    'grain': ('Grain', ITEM_VEGETABLE, 6, 0, (0.8, 0.7, 0.4)),  # Never spoils
    'egg': ('Egg', ITEM_SPECIAL, 12, 2, (0.95, 0.9, 0.8)),  # Fresh egg
    'butter': ('Butter', ITEM_SPECIAL, 15, 2, (1.0, 0.95, 0.7)),  # Dairy butter
    'cream': ('Cream', ITEM_SPECIAL, 18, 1, (0.98, 0.98, 0.95)),  # Fresh cream
    'bread': ('Bread', ITEM_VEGETABLE, 10, 2, (0.8, 0.6, 0.4)),  # Baked bread
    'wild_meat': ('Wild Meat', ITEM_MEAT, 25, 1, (0.7, 0.3, 0.3)),  # Hunted game meat
    'wild_mushroom': ('Wild Mushroom', ITEM_VEGETABLE, 20, 2, (0.5, 0.4, 0.35)),  # Foraged mushroom
    'root_vegetable': ('Root Vegetable', ITEM_VEGETABLE, 12, 4, (0.7, 0.5, 0.3)),  # Carrot, potato, etc.
    'exotic_spice': ('Exotic Spice', ITEM_SPICE, 35, 0, (0.8, 0.4, 0.2)),  # Imported spice, never spoils
    'fire_pepper': ('Fire Pepper', ITEM_SPICE, 28, 3, (0.9, 0.2, 0.1)),  # Spicy hot pepper
    'rare_flower': ('Rare Flower', ITEM_SPECIAL, 40, 2, (0.9, 0.5, 0.7)),  # Decorative/edible flower
    'premium_tea': ('Premium Tea', ITEM_SPICE, 30, 0, (0.4, 0.6, 0.3)),  # Fine tea leaves, never spoils
    'premium_ingredient': ('Premium Ingredient', ITEM_SPECIAL, 50, 2, (0.8, 0.7, 0.6)),  # High-quality ingredient
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
    ZONE_COASTAL_SHORE: [
        ('cs_salt_1', 'Salt Flats', 4, 6, 'sea_salt', SPAWN_RARITY_COMMON, None),
        ('cs_seaweed_1', 'Seaweed Bed', 8, 10, 'fresh_seaweed', SPAWN_RARITY_COMMON, None),
        ('cs_seaweed_2', 'Kelp Grove', 14, 8, 'fresh_seaweed', SPAWN_RARITY_UNCOMMON, None),
        ('cs_crab_1', 'Crab Rocks', 6, 12, 'coastal_crab', SPAWN_RARITY_UNCOMMON, ABILITY_SNIFF),
        ('cs_oyster_1', 'Pearl Beds', 16, 5, 'pearl_oyster', SPAWN_RARITY_RARE, ABILITY_BURROW),
        ('cs_clam_1', 'Tidal Pool', 10, 4, 'tidal_clam', SPAWN_RARITY_UNCOMMON, None),
        ('cs_clam_2', 'Sandy Shallows', 18, 12, 'tidal_clam', SPAWN_RARITY_COMMON, None),
        ('cs_berry_1', 'Dune Shrubs', 3, 14, 'beach_berry', SPAWN_RARITY_UNCOMMON, None),
    ],
    ZONE_MOUNTAIN_PASS: [
        ('mp_herb_1', 'Alpine Meadow', 5, 5, 'mountain_herb', SPAWN_RARITY_COMMON, None),
        ('mp_herb_2', 'Cliff Edge', 15, 3, 'mountain_herb', SPAWN_RARITY_UNCOMMON, None),
        ('mp_honey_1', 'Rock Hive', 10, 8, 'rock_honey', SPAWN_RARITY_RARE, ABILITY_SMASH),
        ('mp_crystal_1', 'Crystal Vein', 18, 10, 'mineral_crystal', SPAWN_RARITY_RARE, ABILITY_SMASH),
        ('mp_flower_1', 'Alpine Garden', 7, 12, 'alpine_flower', SPAWN_RARITY_UNCOMMON, None),
        ('mp_flower_2', 'Summit Bloom', 14, 6, 'alpine_flower', SPAWN_RARITY_RARE, ABILITY_GLIDE),
        ('mp_moss_1', 'Mossy Rocks', 3, 9, 'mountain_moss', SPAWN_RARITY_COMMON, None),
        ('mp_egg_1', 'Hot Springs', 12, 14, 'hot_spring_egg', SPAWN_RARITY_RARE, None),
    ],
    ZONE_ANCIENT_RUINS: [
        ('ar_spice_1', 'Sealed Storage', 5, 5, 'ancient_spice', SPAWN_RARITY_UNCOMMON, ABILITY_SMASH),
        ('ar_spice_2', 'Crumbling Pantry', 14, 3, 'ancient_spice', SPAWN_RARITY_RARE, None),
        ('ar_moss_1', 'Overgrown Wall', 8, 8, 'ruin_moss', SPAWN_RARITY_COMMON, None),
        ('ar_moss_2', 'Temple Steps', 16, 12, 'ruin_moss', SPAWN_RARITY_UNCOMMON, None),
        ('ar_crystal_1', 'Crystal Garden', 10, 6, 'crystal_flower', SPAWN_RARITY_RARE, ABILITY_SNIFF),
        ('ar_herb_1', 'Dragon Shrine', 4, 12, 'dragon_scale_herb', SPAWN_RARITY_UNCOMMON, None),
        ('ar_herb_2', 'Scale Grove', 18, 8, 'dragon_scale_herb', SPAWN_RARITY_RARE, ABILITY_SNIFF),
        ('ar_grain_1', 'Ancient Granary', 12, 10, 'forgotten_grain', SPAWN_RARITY_UNCOMMON, ABILITY_BURROW),
        ('ar_mushroom_1', 'Glowing Cellar', 6, 14, 'mystic_mushroom', SPAWN_RARITY_RARE, None),
        ('ar_honey_1', 'Amber Chamber', 15, 5, 'ancient_honey', SPAWN_RARITY_RARE, ABILITY_SMASH),
        ('ar_berry_1', 'Courtyard Vines', 3, 9, 'ruin_berry', SPAWN_RARITY_COMMON, None),
    ],
    ZONE_SKY_ISLANDS: [
        ('si_cloud_1', 'Cloud Bank', 5, 5, 'cloud_essence', SPAWN_RARITY_UNCOMMON, None),
        ('si_cloud_2', 'Misty Peak', 15, 3, 'cloud_essence', SPAWN_RARITY_RARE, ABILITY_GLIDE),
        ('si_crystal_1', 'Sky Spire', 10, 7, 'sky_crystal', SPAWN_RARITY_RARE, ABILITY_SMASH),
        ('si_crystal_2', 'Crystal Clouds', 18, 10, 'sky_crystal', SPAWN_RARITY_RARE, None),
        ('si_berry_1', 'Floating Garden', 6, 10, 'celestial_berry', SPAWN_RARITY_UNCOMMON, None),
        ('si_berry_2', 'Star Orchard', 14, 12, 'celestial_berry', SPAWN_RARITY_RARE, ABILITY_GLIDE),
        ('si_flower_1', 'Wind Terrace', 8, 4, 'wind_flower', SPAWN_RARITY_UNCOMMON, None),
        ('si_flower_2', 'Breeze Garden', 16, 8, 'wind_flower', SPAWN_RARITY_RARE, ABILITY_GLIDE),
        ('si_nectar_1', 'Starlight Pool', 12, 6, 'starlight_nectar', SPAWN_RARITY_RARE, ABILITY_SNIFF),
        ('si_tear_1', 'Dragon Sanctuary', 10, 12, 'dragon_tear', SPAWN_RARITY_RARE, ABILITY_SNIFF),
        ('si_feather_1', 'Phoenix Nest', 4, 8, 'phoenix_feather', SPAWN_RARITY_RARE, ABILITY_GLIDE),
        ('si_honey_1', 'Sky Hive', 17, 5, 'sky_honey', SPAWN_RARITY_RARE, ABILITY_SMASH),
    ],
}

# Weather-conditional spawn points (only appear during specific weather)
# Format: (id, name, x, y, ingredient_id, rarity, ability_required, weather_required)
WEATHER_SPAWN_POINTS = {
    ZONE_CAFE_GROUNDS: [
        ('cg_storm_1', 'Storm-touched Patch', 10, 10, 'storm_flower', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
    ],
    ZONE_MEADOW_FIELDS: [
        ('mf_storm_1', 'Lightning Strike Site', 8, 6, 'storm_flower', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('mf_storm_2', 'Charged Ground', 15, 10, 'lightning_crystal', SPAWN_RARITY_RARE, None, WEATHER_STORMY),
        ('mf_special_1', 'Starfall Meadow', 10, 8, 'stardust_petal', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
    ],
    ZONE_FOREST_DEPTHS: [
        ('fd_storm_1', 'Storm Clearing', 12, 7, 'storm_flower', SPAWN_RARITY_COMMON, None, WEATHER_STORMY),
        ('fd_storm_2', 'Thunder Tree', 5, 10, 'lightning_crystal', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('fd_special_1', 'Rainbow Pool', 16, 6, 'rainbow_essence', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
        ('fd_special_2', 'Moonlit Hollow', 3, 8, 'moonbeam_honey', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
    ],
    ZONE_COASTAL_SHORE: [
        ('cs_storm_1', 'Storm Surge Pool', 8, 8, 'storm_flower', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('cs_storm_2', 'Lightning Tide', 14, 10, 'lightning_crystal', SPAWN_RARITY_RARE, None, WEATHER_STORMY),
        ('cs_special_1', 'Moonlit Cove', 6, 5, 'moonbeam_honey', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
    ],
    ZONE_MOUNTAIN_PASS: [
        ('mp_storm_1', 'Thunder Peak', 10, 4, 'lightning_crystal', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('mp_storm_2', 'Storm Ridge', 16, 8, 'storm_flower', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('mp_special_1', 'Starlit Summit', 12, 2, 'stardust_petal', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
        ('mp_special_2', 'Aurora Pool', 8, 12, 'rainbow_essence', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
    ],
    ZONE_ANCIENT_RUINS: [
        ('ar_storm_1', 'Lightning Altar', 10, 5, 'lightning_crystal', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('ar_storm_2', 'Thunder Sanctum', 5, 10, 'storm_flower', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('ar_special_1', 'Moonlit Chamber', 12, 8, 'moonbeam_honey', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
        ('ar_special_2', 'Starfall Ruins', 16, 4, 'stardust_petal', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
    ],
    ZONE_SKY_ISLANDS: [
        ('si_storm_1', 'Thunder Cloud', 8, 6, 'lightning_crystal', SPAWN_RARITY_UNCOMMON, None, WEATHER_STORMY),
        ('si_storm_2', 'Storm Eye', 14, 4, 'storm_flower', SPAWN_RARITY_RARE, None, WEATHER_STORMY),
        ('si_special_1', 'Aurora Gate', 10, 8, 'rainbow_essence', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
        ('si_special_2', 'Celestial Throne', 12, 3, 'stardust_petal', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
        ('si_special_3', 'Moonrise Platform', 6, 12, 'moonbeam_honey', SPAWN_RARITY_RARE, None, WEATHER_SPECIAL),
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
RECIPE_CATEGORY_SPECIAL = 'special'  # Legendary/story recipes

ALL_RECIPE_CATEGORIES = [
    RECIPE_CATEGORY_APPETIZER,
    RECIPE_CATEGORY_MAIN,
    RECIPE_CATEGORY_DESSERT,
    RECIPE_CATEGORY_BEVERAGE,
    RECIPE_CATEGORY_SPECIAL,
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
UNLOCK_TYPE_AFFINITY = 'affinity'     # Requires character affinity (secret recipes)
UNLOCK_TYPE_EVENT = 'event'           # Requires specific story event

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

    # =========================================================================
    # SEAFOOD RECIPES (6) - Coastal Shore ingredients
    # =========================================================================
    'seaweed_salad': {
        'name': 'Seaweed Salad',
        'description': 'Fresh ocean seaweed with a light sea salt dressing.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 35,
        'ingredients': [
            ('fresh_seaweed', 2, 1),
            ('sea_salt', 1, 1),
        ],
        'color_influence': (0.2, 0.5, 0.4),  # Sea green
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'grilled_oysters': {
        'name': 'Grilled Pearl Oysters',
        'description': 'Succulent oysters grilled with herbs and sea salt.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 2,
        'base_price': 65,
        'ingredients': [
            ('pearl_oyster', 2, 2),
            ('sea_salt', 1, 1),
            ('garden_herb', 1, 1),
        ],
        'color_influence': (0.7, 0.7, 0.8),  # Pearl white
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 40},
    },
    'coastal_chowder': {
        'name': 'Coastal Chowder',
        'description': 'Rich, creamy chowder with fresh coastal catches.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 90,
        'ingredients': [
            ('tidal_clam', 2, 2),
            ('sea_salt', 1, 1),
            ('wild_herb', 1, 1),
        ],
        'color_influence': (0.8, 0.7, 0.6),  # Creamy
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'crab_cakes': {
        'name': 'Coastal Crab Cakes',
        'description': 'Delicate crab cakes with herb seasoning.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 105,
        'ingredients': [
            ('coastal_crab', 2, 2),
            ('garden_herb', 1, 1),
            ('sea_salt', 1, 1),
        ],
        'color_influence': (0.8, 0.5, 0.4),  # Crab orange
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 45},
    },
    'ocean_medley': {
        'name': 'Ocean Medley Platter',
        'description': 'A luxurious selection of the finest coastal ingredients.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 160,
        'ingredients': [
            ('coastal_crab', 1, 3),
            ('pearl_oyster', 1, 2),
            ('tidal_clam', 1, 2),
            ('fresh_seaweed', 1, 2),
        ],
        'color_influence': (0.4, 0.6, 0.8),  # Ocean blue
        'unlock': {'type': UNLOCK_TYPE_STORY, 'requirement': 'chapter_2'},
    },
    'salt_crusted_fish': {
        'name': 'Salt-Crusted Fish',
        'description': 'Tender fish baked in a sea salt crust with herbs.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 95,
        'ingredients': [
            ('forest_fish', 1, 2),
            ('sea_salt', 2, 2),
            ('forest_herb', 1, 1),
        ],
        'color_influence': (0.9, 0.9, 0.8),  # Salt white
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 35},
    },

    # =========================================================================
    # MOUNTAIN RECIPES (5) - Mountain Pass ingredients
    # =========================================================================
    'alpine_tea': {
        'name': 'Alpine Herb Tea',
        'description': 'Fragrant tea brewed from rare mountain herbs.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 1,
        'base_price': 30,
        'ingredients': [
            ('mountain_herb', 1, 1),
            ('alpine_flower', 1, 1),
        ],
        'color_influence': (0.5, 0.7, 0.5),  # Alpine green
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'mountain_stew': {
        'name': 'Hearty Mountain Stew',
        'description': 'A warming stew with mountain herbs and moss.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 85,
        'ingredients': [
            ('mountain_herb', 2, 2),
            ('mountain_moss', 1, 1),
            ('buried_root', 1, 2),
        ],
        'color_influence': (0.4, 0.5, 0.4),  # Mountain green
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'honey_glazed_game': {
        'name': 'Rock Honey Glazed Game',
        'description': 'Wild game glazed with precious rock honey.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 145,
        'ingredients': [
            ('wild_game', 1, 3),
            ('rock_honey', 1, 2),
            ('mountain_herb', 1, 2),
        ],
        'color_influence': (0.8, 0.6, 0.3),  # Honey gold
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 60},
    },
    'rock_honey_pastry': {
        'name': 'Rock Honey Pastry',
        'description': 'Flaky pastry filled with crystallized rock honey.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 2,
        'base_price': 55,
        'ingredients': [
            ('rock_honey', 1, 2),
            ('alpine_flower', 1, 1),
        ],
        'color_influence': (0.9, 0.7, 0.3),  # Honey amber
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'crystal_infused_dessert': {
        'name': 'Crystal-Infused Delicacy',
        'description': 'A magical dessert sparkling with mineral crystals.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 4,
        'base_price': 130,
        'ingredients': [
            ('mineral_crystal', 1, 3),
            ('rock_honey', 1, 2),
            ('alpine_flower', 1, 2),
        ],
        'color_influence': (0.6, 0.8, 0.9),  # Crystal blue
        'unlock': {'type': UNLOCK_TYPE_STORY, 'requirement': 'chapter_3'},
    },

    # =========================================================================
    # SEASONAL RECIPES (6) - Autumn/Winter comfort foods
    # =========================================================================
    'autumn_harvest_soup': {
        'name': 'Autumn Harvest Soup',
        'description': 'Warm soup celebrating the autumn harvest.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 55,
        'ingredients': [
            ('buried_root', 2, 1),
            ('field_mushroom', 1, 1),
            ('wild_herb', 1, 1),
        ],
        'color_influence': (0.7, 0.5, 0.3),  # Autumn orange
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'mushroom_medley': {
        'name': 'Forest Mushroom Medley',
        'description': 'A rich dish featuring various forest mushrooms.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 80,
        'ingredients': [
            ('rare_mushroom', 1, 2),
            ('field_mushroom', 2, 2),
            ('mountain_moss', 1, 1),
        ],
        'color_influence': (0.5, 0.4, 0.4),  # Mushroom brown
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 35},
    },
    'winter_warmer': {
        'name': 'Winter Warmer',
        'description': 'A spiced hot drink to ward off the winter chill.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 2,
        'base_price': 35,
        'ingredients': [
            ('mountain_herb', 1, 1),
            ('golden_honey', 1, 1),
            ('wild_berry', 1, 1),
        ],
        'color_influence': (0.7, 0.4, 0.3),  # Warm red
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 20},
    },
    'hearty_root_stew': {
        'name': 'Hearty Root Stew',
        'description': 'A filling stew packed with nutritious roots.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 75,
        'ingredients': [
            ('buried_root', 3, 2),
            ('wild_herb', 1, 1),
            ('field_mushroom', 1, 1),
        ],
        'color_influence': (0.6, 0.4, 0.3),  # Earthy brown
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 30},
    },
    'spiced_berry_cider': {
        'name': 'Spiced Berry Cider',
        'description': 'Warm cider infused with berries and mountain herbs.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 2,
        'base_price': 40,
        'ingredients': [
            ('meadow_berry', 2, 1),
            ('beach_berry', 1, 1),
            ('mountain_herb', 1, 1),
        ],
        'color_influence': (0.7, 0.3, 0.4),  # Berry pink
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'comfort_casserole': {
        'name': 'Comfort Casserole',
        'description': 'A hearty casserole perfect for cold days.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 90,
        'ingredients': [
            ('wild_game', 1, 2),
            ('buried_root', 1, 2),
            ('field_mushroom', 1, 1),
            ('wild_herb', 1, 1),
        ],
        'color_influence': (0.6, 0.4, 0.3),  # Comfort brown
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 40},
    },

    # =========================================================================
    # SECRET RECIPES - Unlocked through character affinity (Close level: 50+)
    # =========================================================================
    'mothers_comfort_stew': {
        'name': "Mother's Comfort Stew",
        'description': 'A secret family recipe passed down through generations. Warm, comforting, and made with love.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 110,
        'ingredients': [
            ('buried_root', 2, 2),
            ('wild_herb', 2, 2),
            ('golden_honey', 1, 2),
            ('field_mushroom', 1, 2),
        ],
        'color_influence': (0.6, 0.5, 0.4),  # Warm earthy
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'mother'},
    },
    'wanderers_secret_blend': {
        'name': "Wanderer's Secret Blend",
        'description': "Marcus's special spice blend from his travels. The exact ingredients are a closely guarded secret.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 135,
        'ingredients': [
            ('mountain_herb', 2, 2),
            ('forest_herb', 1, 2),
            ('wild_game', 1, 3),
            ('rare_mushroom', 1, 2),
        ],
        'color_influence': (0.5, 0.4, 0.3),  # Exotic brown
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'marcus'},
    },
    'lilys_perfect_souffle': {
        'name': "Lily's Perfect Soufflé",
        'description': "A recipe that took Lily years to perfect. Light as air with an impossibly delicate texture.",
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 5,
        'base_price': 150,
        'ingredients': [
            ('edible_flower', 2, 3),
            ('golden_honey', 2, 2),
            ('alpine_flower', 1, 2),
            ('crystal_shard', 1, 2),
        ],
        'color_influence': (0.8, 0.7, 0.6),  # Golden delicate
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'lily'},
    },
    'garretts_memory_bread': {
        'name': "Garrett's Memory Bread",
        'description': "An old family recipe that Garrett's late wife used to make. Simple ingredients, profound meaning.",
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 2,
        'base_price': 65,
        'ingredients': [
            ('golden_honey', 1, 2),
            ('garden_herb', 2, 2),
            ('wild_herb', 1, 2),
        ],
        'color_influence': (0.7, 0.6, 0.4),  # Warm golden brown
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'garrett'},
    },
    'captains_treasure_catch': {
        'name': "Captain's Treasure Catch",
        'description': "Vera's legendary seafood dish, said to bring good fortune to those who taste it.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 175,
        'ingredients': [
            ('coastal_crab', 1, 3),
            ('pearl_oyster', 2, 2),
            ('tidal_clam', 1, 2),
            ('sea_salt', 1, 2),
            ('forest_fish', 1, 2),
        ],
        'color_influence': (0.4, 0.6, 0.8),  # Ocean blue
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'vera'},
    },
    'royal_midnight_feast': {
        'name': 'Royal Midnight Feast',
        'description': "The Masked Noble's secret recipe from the royal kitchens. Extraordinarily decadent.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 5,
        'base_price': 200,
        'ingredients': [
            ('hidden_truffle', 1, 3),
            ('rare_mushroom', 2, 2),
            ('wild_game', 1, 3),
            ('mineral_crystal', 1, 2),
            ('rock_honey', 1, 2),
        ],
        'color_influence': (0.4, 0.3, 0.5),  # Regal purple
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'noble'},
    },
    'elenas_reconciliation_tea': {
        'name': "Elena's Reconciliation Tea",
        'description': "A delicate blend passed down through generations. Elena shares it only with those she trusts.",
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 3,
        'base_price': 85,
        'ingredients': [
            ('wild_herb', 2, 2),
            ('garden_herb', 1, 2),
            ('rare_flower', 1, 3),
            ('golden_honey', 1, 2),
        ],
        'color_influence': (0.6, 0.5, 0.7),  # Soft lavender
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'elena'},
    },
    'thomas_humble_pie': {
        'name': "Thomas's Humble Pie",
        'description': "A hearty, unpretentious pie. Thomas learned that sometimes the simplest gesture means the most.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 90,
        'ingredients': [
            ('wild_game', 1, 2),
            ('garden_herb', 2, 2),
            ('root_vegetable', 2, 2),
            ('wild_mushroom', 1, 2),
        ],
        'color_influence': (0.6, 0.5, 0.4),  # Warm rustic brown
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'thomas'},
    },

    # Ancient Ruins discovery recipes
    'ancient_elixir': {
        'name': 'Ancient Elixir',
        'description': "A mystical beverage recreated from inscriptions found in the ruins. Said to grant clarity of mind.",
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 4,
        'base_price': 120,
        'ingredients': [
            ('ancient_spice', 1, 2),
            ('crystal_flower', 1, 3),
            ('ancient_honey', 1, 2),
            ('wild_herb', 1, 2),
        ],
        'color_influence': (0.6, 0.7, 0.8),  # Mystical blue-silver
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY, 'zone': 'ancient_ruins'},
    },
    'dragon_scale_stew': {
        'name': 'Dragon Scale Stew',
        'description': "A hearty stew featuring herbs that resemble dragon scales. Ancient dragons were said to favor this dish.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 130,
        'ingredients': [
            ('dragon_scale_herb', 2, 2),
            ('forgotten_grain', 1, 2),
            ('mystic_mushroom', 1, 2),
            ('ruin_moss', 1, 2),
        ],
        'color_influence': (0.5, 0.4, 0.3),  # Earthy dragon tones
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY, 'zone': 'ancient_ruins'},
    },
    'ruins_mystery_bread': {
        'name': 'Ruins Mystery Bread',
        'description': "Bread made with ancient grains and honey preserved for centuries. Surprisingly delicious.",
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 3,
        'base_price': 95,
        'ingredients': [
            ('forgotten_grain', 2, 2),
            ('ancient_honey', 1, 2),
            ('ruin_berry', 1, 2),
        ],
        'color_influence': (0.7, 0.6, 0.4),  # Golden ancient
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY, 'zone': 'ancient_ruins'},
    },

    # Sky Islands legendary recipes
    'celestial_ambrosia': {
        'name': 'Celestial Ambrosia',
        'description': "A divine dessert said to be the food of sky spirits. Grants a sense of peaceful euphoria.",
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 5,
        'base_price': 350,
        'ingredients': [
            ('starlight_nectar', 1, 3),
            ('celestial_berry', 2, 2),
            ('sky_honey', 1, 2),
            ('cloud_essence', 1, 2),
        ],
        'color_influence': (0.9, 0.85, 1.0),  # Ethereal white-gold
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY, 'zone': 'sky_islands'},
    },
    'dragon_tear_elixir': {
        'name': 'Dragon Tear Elixir',
        'description': "An impossibly rare beverage made from crystallized dragon tears. Said to grant visions.",
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 5,
        'base_price': 400,
        'ingredients': [
            ('dragon_tear', 1, 3),
            ('starlight_nectar', 1, 2),
            ('wind_flower', 1, 2),
        ],
        'color_influence': (0.6, 0.75, 1.0),  # Iridescent blue
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY, 'zone': 'sky_islands'},
    },
    'phoenix_rebirth_cake': {
        'name': 'Phoenix Rebirth Cake',
        'description': "A legendary dessert that seems to glow with inner warmth. Customers feel renewed after eating it.",
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 5,
        'base_price': 500,
        'ingredients': [
            ('phoenix_feather', 1, 3),
            ('sky_crystal', 1, 2),
            ('celestial_berry', 1, 2),
            ('sky_honey', 1, 2),
        ],
        'color_influence': (1.0, 0.7, 0.4),  # Phoenix flame colors
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY, 'zone': 'sky_islands'},
    },
    'cloud_walker_soup': {
        'name': 'Cloud Walker Soup',
        'description': "A light, airy soup that leaves diners feeling like they could float away. Perfect for adventurers.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 280,
        'ingredients': [
            ('cloud_essence', 2, 2),
            ('wind_flower', 1, 2),
            ('sky_crystal', 1, 2),
        ],
        'color_influence': (0.85, 0.9, 1.0),  # Soft cloud white
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY, 'zone': 'sky_islands'},
    },

    # =========================================================================
    # CHARACTER & STORY RECIPES
    # Recipes unlocked through story events and character interactions
    # =========================================================================
    'dragon_treat': {
        'name': 'Dragon Treat',
        'description': "A special snack infused with warmth and care, perfect for bonding with your dragon.",
        'category': RECIPE_CATEGORY_SPECIAL,
        'difficulty': 1,
        'base_price': 25,
        'ingredients': [
            ('honey', 1, 1),
            ('berry', 1, 1),
        ],
        'color_influence': (0.8, 0.6, 0.7),
        'unlock': {'type': UNLOCK_TYPE_STORY, 'requirement': 'dragon_hatched'},
    },
    'traveler_stew': {
        'name': "Traveler's Stew",
        'description': "A hearty, warming stew favored by wanderers and adventurers. Perfect after a long journey.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 45,
        'ingredients': [
            ('wild_meat', 1, 2),
            ('root_vegetable', 2, 2),
            ('herb', 1, 1),
        ],
        'color_influence': (0.6, 0.4, 0.3),
        'unlock': {'type': UNLOCK_TYPE_STORY, 'requirement': 'chapter1_unlocked'},
    },
    'wanderers_feast': {
        'name': "Wanderer's Feast",
        'description': "A legendary dish that Marcus remembers from his guild days. Complex and deeply nostalgic.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 150,
        'ingredients': [
            ('wild_meat', 2, 3),
            ('forest_herb', 2, 2),
            ('exotic_spice', 1, 2),
            ('root_vegetable', 1, 2),
        ],
        'color_influence': (0.5, 0.4, 0.3),
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'marcus'},
    },
    'comfort_stew': {
        'name': 'Comfort Stew',
        'description': "Your mother's signature dish. Warm, nourishing, and full of love.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 55,
        'ingredients': [
            ('root_vegetable', 2, 2),
            ('herb', 2, 2),
            ('honey', 1, 1),
        ],
        'color_influence': (0.7, 0.5, 0.4),
        'unlock': {'type': UNLOCK_TYPE_STORY, 'requirement': 'received_mothers_advice'},
    },
    'gourmet_special': {
        'name': 'Gourmet Special',
        'description': "An elegant dish that showcases technical perfection. Lily's standard for excellence.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 180,
        'ingredients': [
            ('premium_ingredient', 1, 3),
            ('exotic_spice', 1, 2),
            ('forest_herb', 1, 2),
            ('butter', 1, 2),
        ],
        'color_influence': (0.9, 0.8, 0.6),
        'unlock': {'type': UNLOCK_TYPE_AFFINITY, 'character': 'lily'},
    },
    'herbal_tea': {
        'name': 'Herbal Tea',
        'description': "A soothing blend of fresh herbs. Perfect for relaxation and conversation.",
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 1,
        'base_price': 20,
        'ingredients': [
            ('herb', 2, 1),
        ],
        'color_influence': (0.4, 0.6, 0.4),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'delicate_pastry': {
        'name': 'Delicate Pastry',
        'description': "A light, flaky pastry that demands precision. A test of any chef's skill.",
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 3,
        'base_price': 75,
        'ingredients': [
            ('flour', 2, 2),
            ('butter', 1, 2),
            ('honey', 1, 1),
        ],
        'color_influence': (0.9, 0.85, 0.7),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 35},
    },
    'refined_tea': {
        'name': 'Refined Tea',
        'description': "An elegant tea blend favored by nobility. Subtle flavors for sophisticated palates.",
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 2,
        'base_price': 45,
        'ingredients': [
            ('premium_tea', 1, 2),
            ('honey', 1, 1),
        ],
        'color_influence': (0.7, 0.6, 0.5),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 25},
    },
    'campfire_bread': {
        'name': 'Campfire Bread',
        'description': "Simple, rustic bread that reminds travelers of nights under the stars.",
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 15,
        'ingredients': [
            ('flour', 1, 1),
            ('herb', 1, 1),
        ],
        'color_influence': (0.6, 0.5, 0.3),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'cream_puff': {
        'name': 'Cream Puff',
        'description': "A delicate choux pastry filled with sweet cream. Light as a cloud.",
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 3,
        'base_price': 60,
        'ingredients': [
            ('flour', 1, 2),
            ('cream', 1, 2),
            ('honey', 1, 1),
        ],
        'color_influence': (0.95, 0.9, 0.8),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 30},
    },
    'garden_salad': {
        'name': 'Garden Salad',
        'description': "Fresh greens and vegetables from the local garden. Simple and refreshing.",
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 20,
        'ingredients': [
            ('herb', 1, 1),
            ('berry', 1, 1),
        ],
        'color_influence': (0.4, 0.7, 0.3),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'hearty_breakfast': {
        'name': 'Hearty Breakfast',
        'description': "A filling morning meal to start the day right. Popular with working folk.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 40,
        'ingredients': [
            ('egg', 2, 1),
            ('wild_meat', 1, 2),
            ('bread', 1, 1),
        ],
        'color_influence': (0.8, 0.7, 0.4),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'meat_pie': {
        'name': 'Meat Pie',
        'description': "A savory pie filled with seasoned meat. Comfort food at its finest.",
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 50,
        'ingredients': [
            ('wild_meat', 2, 2),
            ('flour', 1, 1),
            ('herb', 1, 1),
        ],
        'color_influence': (0.6, 0.4, 0.3),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 15},
    },
    'honey_biscuits': {
        'name': 'Honey Biscuits',
        'description': 'Sweet, golden biscuits drizzled with fresh honey. A comforting treat.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 1,
        'base_price': 30,
        'ingredients': [
            ('flour', 1, 1),
            ('honey', 1, 1),
        ],
        'color_influence': (0.9, 0.8, 0.5),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'herbed_bread': {
        'name': 'Herbed Bread',
        'description': 'Freshly baked bread infused with aromatic herbs.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 25,
        'ingredients': [
            ('flour', 1, 1),
            ('herb', 1, 1),
        ],
        'color_influence': (0.7, 0.6, 0.4),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'mushroom_soup': {
        'name': 'Mushroom Soup',
        'description': 'A rich, earthy soup made from forest mushrooms.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 40,
        'ingredients': [
            ('mushroom', 2, 2),
            ('herb', 1, 1),
        ],
        'color_influence': (0.6, 0.5, 0.4),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'spicy_curry': {
        'name': 'Spicy Curry',
        'description': 'A fiery dish that packs quite a punch. Not for the faint of heart.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 3,
        'base_price': 65,
        'ingredients': [
            ('wild_meat', 1, 1),
            ('fire_pepper', 2, 2),
            ('exotic_spice', 1, 1),
        ],
        'color_influence': (0.9, 0.4, 0.2),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 40},
    },
    'fire_pepper_wrap': {
        'name': 'Fire Pepper Wrap',
        'description': 'Grilled meat wrapped with fire peppers. Intensely spicy.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 2,
        'base_price': 55,
        'ingredients': [
            ('wild_meat', 1, 1),
            ('fire_pepper', 1, 2),
            ('flour', 1, 1),
        ],
        'color_influence': (0.8, 0.3, 0.2),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 30},
    },
    'adventure_ale': {
        'name': "Adventurer's Ale",
        'description': 'A hearty brew favored by travelers and adventurers.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 2,
        'base_price': 35,
        'ingredients': [
            ('grain', 2, 2),
            ('honey', 1, 1),
        ],
        'color_influence': (0.7, 0.5, 0.3),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 20},
    },
    'trail_mix': {
        'name': 'Trail Mix',
        'description': 'A portable snack mix perfect for long journeys.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 20,
        'ingredients': [
            ('berry', 1, 1),
            ('grain', 1, 1),
        ],
        'color_influence': (0.6, 0.5, 0.4),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'fancy_dessert': {
        'name': 'Fancy Dessert',
        'description': 'An elaborate confection decorated with edible flowers.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 4,
        'base_price': 120,
        'ingredients': [
            ('flour', 1, 1),
            ('honey', 2, 2),
            ('rare_flower', 1, 1),
            ('cream', 1, 1),
        ],
        'color_influence': (0.95, 0.85, 0.9),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 50},
    },
    'burnt_toast': {
        'name': 'Burnt Toast',
        'description': 'Overcooked bread. Some say it has character.',
        'category': RECIPE_CATEGORY_APPETIZER,
        'difficulty': 1,
        'base_price': 5,
        'ingredients': [
            ('flour', 1, 1),
        ],
        'color_influence': (0.3, 0.2, 0.1),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'simple_gruel': {
        'name': 'Simple Gruel',
        'description': 'Basic porridge. Filling but not exciting.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 1,
        'base_price': 10,
        'ingredients': [
            ('grain', 1, 1),
        ],
        'color_influence': (0.7, 0.7, 0.6),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'overcooked_meat': {
        'name': 'Overcooked Meat',
        'description': 'Tough and chewy. A culinary mishap.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 1,
        'base_price': 15,
        'ingredients': [
            ('wild_meat', 1, 1),
        ],
        'color_influence': (0.4, 0.3, 0.2),
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'exotic_blend': {
        'name': 'Exotic Blend Tea',
        'description': 'A bold tea made from rare imported spices.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 3,
        'base_price': 70,
        'ingredients': [
            ('exotic_spice', 2, 2),
            ('herb', 1, 1),
        ],
        'color_influence': (0.8, 0.5, 0.3),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 45},
    },
    'spiced_fusion': {
        'name': 'Spiced Fusion',
        'description': 'A daring combination of multiple exotic spices.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 4,
        'base_price': 90,
        'ingredients': [
            ('exotic_spice', 2, 2),
            ('fire_pepper', 1, 1),
            ('wild_meat', 1, 1),
        ],
        'color_influence': (0.9, 0.5, 0.3),
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 55},
    },

    # =========================================================================
    # FINALE - LEGACY RECIPES
    # Unlocked through story events in the finale chapter
    # =========================================================================
    'ancestral_blessing': {
        'name': 'Ancestral Blessing',
        'description': "Elara's original recipe, passed down through generations. Said to strengthen the bond between dragon and bonded.",
        'category': RECIPE_CATEGORY_SPECIAL,
        'difficulty': 5,
        'base_price': 500,
        'ingredients': [
            ('dragon_tear', 1, 3),
            ('starlight_nectar', 2, 3),
            ('celestial_berry', 2, 2),
            ('honey', 1, 2),
        ],
        'color_influence': (0.9, 0.85, 1.0),  # Ethereal purple
        'unlock': {'type': UNLOCK_TYPE_EVENT, 'event': 'finale_dragon_bond'},
    },
    'dragons_heart_feast': {
        'name': "Dragon's Heart Feast",
        'description': "The sacred feast of the Dragon's Heart lineage. Only a true guardian can prepare this legendary meal.",
        'category': RECIPE_CATEGORY_SPECIAL,
        'difficulty': 5,
        'base_price': 750,
        'ingredients': [
            ('phoenix_feather', 1, 3),
            ('dragon_tear', 1, 3),
            ('cloud_essence', 2, 2),
            ('ancient_honey', 1, 3),
            ('celestial_berry', 2, 2),
        ],
        'color_influence': (1.0, 0.7, 0.5),  # Warm golden orange
        'unlock': {'type': UNLOCK_TYPE_EVENT, 'event': 'finale_acceptance'},
    },
    'legacy_eternal': {
        'name': 'Legacy Eternal',
        'description': "The ultimate expression of the cafe's heritage. A dish that embodies three centuries of dragon-human friendship.",
        'category': RECIPE_CATEGORY_SPECIAL,
        'difficulty': 5,
        'base_price': 1000,
        'ingredients': [
            ('phoenix_feather', 1, 3),
            ('dragon_tear', 2, 3),
            ('starlight_nectar', 2, 3),
            ('sky_crystal', 1, 3),
            ('ancient_spice', 2, 3),
        ],
        'color_influence': (1.0, 0.95, 0.8),  # Radiant gold
        'unlock': {'type': UNLOCK_TYPE_EVENT, 'event': 'finale_end'},
    },

    # =========================================================================
    # LEGENDARY TIER RECIPES (6) - Phase 3 Polish
    # =========================================================================
    'legendary_dragon_feast': {
        'name': 'Legendary Dragon Feast',
        'description': 'An extravagant multi-course meal featuring dragon-touched ingredients. Only the most renowned chefs dare attempt this legendary dish.',
        'category': RECIPE_CATEGORY_MAIN,
        'difficulty': 5,
        'base_price': 500,
        'ingredients': [
            ('dragon_scale_herb', 2, 3),
            ('wild_game', 1, 3),
            ('exotic_spice', 2, 3),
            ('golden_honey', 1, 2),
        ],
        'color_influence': (0.8, 0.3, 0.2),  # Fiery red-orange
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 500},
    },
    'mythic_tea_ceremony': {
        'name': 'Mythic Tea Ceremony',
        'description': 'An ancient tea ritual passed down through generations. The ethereal blend calms even the most troubled spirit.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 4,
        'base_price': 300,
        'ingredients': [
            ('premium_tea', 2, 3),
            ('rare_flower', 1, 3),
            ('golden_honey', 1, 2),
            ('moonbeam_honey', 1, 3),
        ],
        'color_influence': (0.5, 0.8, 0.9),  # Serene blue-teal
        'unlock': {'type': UNLOCK_TYPE_REPUTATION, 'requirement': 500},
    },
    'ancient_relic_cake': {
        'name': 'Ancient Relic Cake',
        'description': 'A recipe discovered in the Ancient Ruins, featuring spices lost to time. Each bite tells a story of civilizations past.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 4,
        'base_price': 250,
        'ingredients': [
            ('ancient_spice', 2, 3),
            ('flour', 2, 1),
            ('ancient_honey', 1, 3),
            ('egg', 2, 1),
        ],
        'color_influence': (0.7, 0.6, 0.4),  # Ancient gold-brown
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'cloud_puffs': {
        'name': 'Cloud Puffs',
        'description': 'Light-as-air pastries that melt on the tongue. Said to taste like floating among the clouds.',
        'category': RECIPE_CATEGORY_DESSERT,
        'difficulty': 3,
        'base_price': 85,
        'ingredients': [
            ('cream', 2, 2),
            ('egg', 2, 1),
            ('flour', 2, 1),
            ('golden_honey', 1, 1),
        ],
        'color_influence': (0.95, 0.95, 1.0),  # Fluffy white
        'unlock': {'type': UNLOCK_TYPE_DEFAULT},
    },
    'storm_brew': {
        'name': 'Storm Brew',
        'description': 'A electrifying herbal drink that crackles with energy. Brewers say it captures the essence of a thunderstorm.',
        'category': RECIPE_CATEGORY_BEVERAGE,
        'difficulty': 3,
        'base_price': 75,
        'ingredients': [
            ('storm_flower', 2, 2),
            ('golden_honey', 1, 2),
            ('wild_herb', 1, 1),
        ],
        'color_influence': (0.4, 0.3, 0.7),  # Electric purple
        'unlock': {'type': UNLOCK_TYPE_DISCOVERY},
    },
    'founders_original': {
        'name': "Founder's Original Recipe",
        'description': "The secret recipe that made Dragon Haven Cafe famous. Mother's masterpiece, now passed down to you.",
        'category': RECIPE_CATEGORY_SPECIAL,
        'difficulty': 5,
        'base_price': 400,
        'ingredients': [
            ('dragon_scale_herb', 1, 3),
            ('moonbeam_honey', 2, 3),
            ('premium_tea', 1, 2),
            ('rare_flower', 1, 3),
            ('ancient_spice', 1, 3),
        ],
        'color_influence': (0.9, 0.8, 0.6),  # Warm nostalgic gold
        'unlock': {'type': UNLOCK_TYPE_STORY, 'chapter': 8},
    },
}

# Default unlocked recipes (available from game start)
DEFAULT_UNLOCKED_RECIPES = [
    'herb_salad',
    'berry_toast',
    'herb_stew',
    'berry_tart',
    'herb_tea',
    'autumn_harvest_soup',  # Seasonal comfort food
    'cloud_puffs',  # Phase 3: Light fluffy dessert
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

# Season/Weather icons (for procedural drawing)
SEASON_ICONS = {
    'spring': 'flower',
    'summer': 'sun',
    'autumn': 'leaf',
    'winter': 'snowflake',
}

WEATHER_ICONS = {
    WEATHER_SUNNY: 'sun',
    WEATHER_CLOUDY: 'cloud',
    WEATHER_RAINY: 'rain',
    WEATHER_STORMY: 'storm',
    WEATHER_SPECIAL: 'star',
}

# Weather colors for visual effects
WEATHER_COLORS = {
    WEATHER_SUNNY: (255, 240, 200),    # Warm yellow
    WEATHER_CLOUDY: (180, 180, 190),   # Gray
    WEATHER_RAINY: (120, 140, 180),    # Blue-gray
    WEATHER_STORMY: (80, 70, 100),     # Dark purple
    WEATHER_SPECIAL: (200, 180, 255),  # Soft purple/magical
}

# Weather overlay tints (RGBA)
WEATHER_OVERLAY = {
    WEATHER_SUNNY: (255, 255, 220, 5),     # Slight warm
    WEATHER_CLOUDY: (180, 180, 200, 20),   # Gray tint
    WEATHER_RAINY: (100, 120, 150, 30),    # Blue-gray
    WEATHER_STORMY: (60, 50, 80, 50),      # Dark dramatic
    WEATHER_SPECIAL: (220, 200, 255, 25),  # Magical purple
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

# =============================================================================
# NEW GAME+ SYSTEM (Phase 4)
# =============================================================================

# NG+ Unlock condition
NG_PLUS_UNLOCK_CHAPTER = 8  # Must complete chapter 8 (Finale)
NG_PLUS_UNLOCK_ACHIEVEMENT = 'story_chapter_8'

# NG+ Starting bonuses
NG_PLUS_STARTING_GOLD_BONUS = 500  # Extra gold at start
NG_PLUS_STARTING_REPUTATION = 50  # Start with some reputation
NG_PLUS_AFFINITY_RETENTION = 0.5  # Keep 50% of character affinity

# NG+ Difficulty modifiers (applied as multipliers)
NG_PLUS_MODIFIERS = {
    'customer_expectations': 1.2,   # 20% higher quality required
    'service_time': 0.9,            # 10% shorter service periods
    'resource_scarcity': 0.8,       # 20% fewer resource spawns
    'gold_bonus': 1.25,             # 25% more gold from sales
    'reputation_decay': 0.8,        # 20% slower reputation decay
}

# NG+ scaling per cycle (stacks multiplicatively)
NG_PLUS_SCALING_PER_CYCLE = {
    'customer_expectations': 1.05,  # +5% per NG+ level
    'service_time': 0.98,           # -2% per NG+ level
    'resource_scarcity': 0.95,      # -5% per NG+ level
    'gold_bonus': 1.05,             # +5% per NG+ level
}

# Maximum NG+ level (for display purposes, no hard cap on mechanics)
NG_PLUS_MAX_DISPLAY = 99

# What carries over to NG+
NG_PLUS_CARRYOVER = {
    'unlocked_recipes': True,       # All unlocked recipes
    'mastered_recipes': True,       # Recipe mastery levels
    'achievements': True,           # All achievements
    'dragon_names_history': True,   # Previous dragon names
    'character_affinity': True,     # Partial affinity (50%)
    'total_playtime': True,         # Cumulative playtime
}

# What resets in NG+
NG_PLUS_RESET = {
    'dragon': True,                 # New egg
    'gold': False,                  # Gets bonus instead
    'reputation': False,            # Gets starting boost
    'story_progress': True,         # Replay from beginning
    'inventory_items': True,        # Empty inventory
    'zones_unlocked': True,         # Re-unlock zones
}
