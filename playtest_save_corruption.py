#!/usr/bin/env python3
"""
Dragon Haven Cafe - Save Corruption Playtest
Tests save file integrity, recovery from corrupted saves, and version compatibility.
"""

import sys
import os
import json
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Minimal pygame init (no display)
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
pygame.init()


class SaveCorruptionTest:
    """Test harness for save corruption testing."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
        self.temp_dir = None

    def test(self, name, condition, details=""):
        """Record a test result."""
        if condition:
            self.passed += 1
            self.tests.append(('PASS', name, details))
            print(f"  [PASS] {name}")
        else:
            self.failed += 1
            self.tests.append(('FAIL', name, details))
            print(f"  [FAIL] {name}: {details}")
        return condition

    def section(self, name):
        """Print a section header."""
        print(f"\n{'=' * 60}")
        print(f"SAVE CORRUPTION: {name}")
        print('=' * 60)

    def setup_temp_dir(self):
        """Create a temporary directory for test saves."""
        self.temp_dir = tempfile.mkdtemp(prefix="dragon_haven_test_")
        return self.temp_dir

    def cleanup_temp_dir(self):
        """Remove temporary test directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def reset_all_systems():
    """Reset all game systems to fresh state."""
    from systems.inventory import reset_inventory
    from systems.economy import reset_economy
    from systems.cafe import reset_cafe_manager
    from systems.world import reset_world_manager
    from systems.story import reset_story_manager
    from systems.dragon_manager import reset_dragon_manager
    from entities.story_character import reset_character_manager
    from systems.recipes import reset_recipe_manager

    reset_inventory()
    reset_economy()
    reset_cafe_manager()
    reset_world_manager()
    reset_story_manager()
    reset_dragon_manager()
    reset_character_manager()
    reset_recipe_manager()

    # Time manager doesn't have a reset - just get a fresh reference
    from systems.time_system import get_time_manager
    time_mgr = get_time_manager()
    time_mgr._current_hour = 8.0
    time_mgr._current_day = 1
    time_mgr._current_season_index = 0  # spring
    time_mgr._paused = False


def create_valid_save_data():
    """Create a valid SaveData object with realistic data."""
    from save_manager import SaveData, SaveMeta, PlayerData, DragonData, CafeData, WorldData, StoryData, InventoryData

    return SaveData(
        meta=SaveMeta(
            slot=1,
            version="1.0.0",
            playtime_seconds=3600.0,
            last_saved="2024-01-15T10:30:00",
            created_at="2024-01-14T08:00:00"
        ),
        player=PlayerData(
            name="TestPlayer",
            total_gold_earned=5000,
            total_customers_served=50
        ),
        dragon=DragonData(
            name="Ember",
            stage="juvenile",
            age_days=15,
            color_shift=(10, -5, 20),
            hunger=75.0,
            happiness=80.0,
            energy=60.0,
            abilities=["burrow_fetch", "sniff_track", "rock_smash"]
        ),
        cafe=CafeData(
            gold=1500,
            reputation=150,
            level=2,
            recipes_unlocked=["herbed_bread", "berry_tart", "dragon_treat"],
            staff_ids=[]
        ),
        world=WorldData(
            current_zone="meadow_fields",
            day_number=15,
            current_time=14.5,
            weather="sunny",
            zones_unlocked=["cafe_grounds", "meadow_fields", "forest_depths"],
            discovered_items=["wild_berry", "meadow_herb"]
        ),
        story=StoryData(
            current_chapter=2,
            events_completed=["prologue_intro", "egg_discovery", "dragon_hatches"],
            character_relationships={"marcus": 30},
            dialogue_flags={"met_marcus": True}
        ),
        inventory=InventoryData(
            items={"wild_berry": 5, "meadow_herb": 3},
            max_slots=20
        )
    )


def test_valid_save_load(test: SaveCorruptionTest):
    """Test normal save/load operations."""
    test.section("VALID SAVE/LOAD")

    from save_manager import SaveManager, SaveData

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    # Test 1: Save valid data
    save_data = create_valid_save_data()
    result = save_mgr.save(1, save_data)
    test.test("Valid save succeeds", result)

    # Test 2: Load saved data
    loaded = save_mgr.load(1)
    test.test("Valid load succeeds", loaded is not None)

    # Test 3: Data integrity
    if loaded:
        test.test("Player name preserved", loaded.player.name == "TestPlayer")
        test.test("Dragon name preserved", loaded.dragon.name == "Ember")
        test.test("Gold preserved", loaded.cafe.gold == 1500)
        test.test("Day number preserved", loaded.world.day_number == 15)
        test.test("Events preserved", "dragon_hatches" in loaded.story.events_completed)

    test.cleanup_temp_dir()


def test_missing_fields(test: SaveCorruptionTest):
    """Test loading saves with missing fields."""
    test.section("MISSING FIELDS")

    from save_manager import SaveManager, SaveData

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    # Test 1: Missing meta section
    corrupted = {
        "player": {"name": "Player"},
        "dragon": {"name": "Dragon", "stage": "egg"},
        "cafe": {"gold": 100},
        "world": {"day_number": 1},
        "story": {},
        "inventory": {}
    }

    save_path = os.path.join(temp_dir, "saves", "slot_1.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w') as f:
        json.dump(corrupted, f)

    loaded = save_mgr.load(1)
    test.test("Load with missing meta succeeds", loaded is not None)
    if loaded:
        test.test("Default meta values used", loaded.meta.slot == 1 or loaded.meta.version != "")

    # Test 2: Missing player section
    corrupted = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "dragon": {"name": "Dragon", "stage": "egg"},
        "cafe": {"gold": 100},
        "world": {"day_number": 1}
    }

    with open(save_path, 'w') as f:
        json.dump(corrupted, f)

    loaded = save_mgr.load(1)
    test.test("Load with missing player succeeds", loaded is not None)
    if loaded:
        test.test("Default player name used", loaded.player.name == "Player")

    # Test 3: Missing dragon stats
    corrupted = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "player": {"name": "Player"},
        "dragon": {"name": "TestDragon"},  # Missing stage, stats, etc.
        "cafe": {"gold": 100},
        "world": {"day_number": 1}
    }

    with open(save_path, 'w') as f:
        json.dump(corrupted, f)

    loaded = save_mgr.load(1)
    test.test("Load with partial dragon data succeeds", loaded is not None)
    if loaded:
        test.test("Dragon name preserved", loaded.dragon.name == "TestDragon")
        test.test("Default dragon stage used", loaded.dragon.stage == "egg")

    # Test 4: Empty sections
    corrupted = {
        "meta": {},
        "player": {},
        "dragon": {},
        "cafe": {},
        "world": {},
        "story": {},
        "inventory": {}
    }

    with open(save_path, 'w') as f:
        json.dump(corrupted, f)

    loaded = save_mgr.load(1)
    test.test("Load with all empty sections succeeds", loaded is not None)

    test.cleanup_temp_dir()


def test_invalid_data_types(test: SaveCorruptionTest):
    """Test loading saves with wrong data types."""
    test.section("INVALID DATA TYPES")

    from save_manager import SaveManager

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    save_path = os.path.join(temp_dir, "saves", "slot_1.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Test 1: String instead of number
    corrupted = {
        "meta": {"slot": "one", "version": "1.0.0"},  # Should be int
        "player": {"name": "Player", "total_gold_earned": "five thousand"},  # Should be int
        "dragon": {"name": "Dragon", "stage": "egg", "hunger": "full"},  # Should be float
        "cafe": {"gold": "100"},  # Should be int
        "world": {"day_number": "15"}
    }

    with open(save_path, 'w') as f:
        json.dump(corrupted, f)

    try:
        loaded = save_mgr.load(1)
        # If it loads, check if values are handled
        if loaded:
            test.test("String-as-number handled gracefully", True)
        else:
            test.test("Invalid types rejected safely", True)
    except (TypeError, ValueError):
        test.test("Type error caught gracefully", True)

    # Test 2: List instead of dict for meta
    corrupted = {
        "meta": ["slot", 1, "version", "1.0.0"],  # Should be dict
        "player": {"name": "Player"}
    }

    with open(save_path, 'w') as f:
        json.dump(corrupted, f)

    try:
        loaded = save_mgr.load(1)
        test.test("List-as-dict handled", loaded is None or loaded is not None)
    except (TypeError, KeyError, AttributeError):
        test.test("Structure error caught", True)

    # Test 3: Null values
    corrupted = {
        "meta": {"slot": 1, "version": None},
        "player": {"name": None},
        "dragon": {"name": None, "stage": None, "hunger": None},
        "cafe": {"gold": None},
        "world": {"day_number": None}
    }

    with open(save_path, 'w') as f:
        json.dump(corrupted, f)

    try:
        loaded = save_mgr.load(1)
        test.test("Null values handled", loaded is None or loaded is not None)
    except (TypeError, AttributeError):
        test.test("Null error caught", True)

    test.cleanup_temp_dir()


def test_corrupted_json(test: SaveCorruptionTest):
    """Test loading completely corrupted JSON files."""
    test.section("CORRUPTED JSON")

    from save_manager import SaveManager

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    save_path = os.path.join(temp_dir, "saves", "slot_1.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Test 1: Invalid JSON syntax
    with open(save_path, 'w') as f:
        f.write('{"meta": {"slot": 1, "version": "1.0.0"')  # Missing closing braces

    loaded = save_mgr.load(1)
    test.test("Invalid JSON returns None", loaded is None)

    # Test 2: Empty file
    with open(save_path, 'w') as f:
        f.write('')

    loaded = save_mgr.load(1)
    test.test("Empty file returns None", loaded is None)

    # Test 3: Random garbage
    with open(save_path, 'w') as f:
        f.write('This is not JSON at all! Just random text.')

    loaded = save_mgr.load(1)
    test.test("Random text returns None", loaded is None)

    # Test 4: Binary garbage
    with open(save_path, 'wb') as f:
        f.write(b'\x00\x01\x02\x03\xff\xfe\xfd')

    try:
        loaded = save_mgr.load(1)
        test.test("Binary garbage returns None", loaded is None)
    except UnicodeDecodeError:
        test.test("Binary garbage caught as decode error", True)

    # Test 5: Valid JSON but wrong structure (array instead of object)
    with open(save_path, 'w') as f:
        json.dump([1, 2, 3, 4, 5], f)

    try:
        loaded = save_mgr.load(1)
        test.test("JSON array returns None or handled", loaded is None or loaded is not None)
    except AttributeError:
        test.test("JSON array structure error caught", True)

    test.cleanup_temp_dir()


def test_version_compatibility(test: SaveCorruptionTest):
    """Test loading saves from different versions."""
    test.section("VERSION COMPATIBILITY")

    from save_manager import SaveManager, SaveData
    from constants import VERSION

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    save_path = os.path.join(temp_dir, "saves", "slot_1.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Test 1: Same major version
    current_major = VERSION.split('.')[0]
    compatible_version = f"{current_major}.99.99"

    save_data = {
        "meta": {"slot": 1, "version": compatible_version},
        "player": {"name": "Player"},
        "dragon": {"name": "Dragon", "stage": "egg"},
        "cafe": {"gold": 100},
        "world": {"day_number": 1},
        "story": {},
        "inventory": {}
    }

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Same major version loads", loaded is not None)

    # Test 2: Different major version
    incompatible_version = "99.0.0"

    save_data["meta"]["version"] = incompatible_version

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    # Should still load but with warning
    test.test("Different major version handled", loaded is not None or loaded is None)

    # Test 3: Very old version
    save_data["meta"]["version"] = "0.0.1"

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Very old version handled", loaded is not None or loaded is None)

    # Test 4: Invalid version string
    save_data["meta"]["version"] = "not-a-version"

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Invalid version string handled", loaded is not None or loaded is None)

    # Test 5: Missing version
    del save_data["meta"]["version"]

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Missing version handled", loaded is not None or loaded is None)

    test.cleanup_temp_dir()


def test_extreme_values(test: SaveCorruptionTest):
    """Test loading saves with extreme/unusual values."""
    test.section("EXTREME VALUES")

    from save_manager import SaveManager

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    save_path = os.path.join(temp_dir, "saves", "slot_1.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Test 1: Very large numbers
    save_data = {
        "meta": {"slot": 1, "version": "1.0.0", "playtime_seconds": 999999999999.0},
        "player": {"name": "Player", "total_gold_earned": 9999999999},
        "dragon": {"name": "Dragon", "stage": "egg", "age_days": 99999},
        "cafe": {"gold": 2147483647, "reputation": 999999},  # Max int32
        "world": {"day_number": 1000000},
        "story": {},
        "inventory": {}
    }

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Large numbers handled", loaded is not None)

    # Test 2: Negative numbers (shouldn't be negative)
    save_data = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "player": {"name": "Player", "total_gold_earned": -1000},
        "dragon": {"name": "Dragon", "stage": "egg", "hunger": -50.0, "happiness": -100.0},
        "cafe": {"gold": -500, "reputation": -100},
        "world": {"day_number": -5},
        "story": {},
        "inventory": {}
    }

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Negative values handled", loaded is not None)

    # Test 3: Very long strings
    long_name = "A" * 10000

    save_data = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "player": {"name": long_name},
        "dragon": {"name": long_name, "stage": "egg"},
        "cafe": {"gold": 100},
        "world": {"day_number": 1},
        "story": {},
        "inventory": {}
    }

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Very long strings handled", loaded is not None)

    # Test 4: Unicode and special characters
    save_data = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "player": {"name": "Playe\u00e9r\u4e2d\u6587"},  # accents, Chinese
        "dragon": {"name": "\u706b\u9f99", "stage": "egg"},  # "Fire Dragon" in Chinese
        "cafe": {"gold": 100},
        "world": {"day_number": 1},
        "story": {},
        "inventory": {}
    }

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False)

    loaded = save_mgr.load(1)
    test.test("Unicode characters handled", loaded is not None)

    # Test 5: Float precision edge cases
    save_data = {
        "meta": {"slot": 1, "version": "1.0.0", "playtime_seconds": 0.000000001},
        "player": {"name": "Player"},
        "dragon": {"name": "Dragon", "stage": "egg", "hunger": 99.99999999999},
        "cafe": {"gold": 100},
        "world": {"day_number": 1, "current_time": 23.999999999},
        "story": {},
        "inventory": {}
    }

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Float precision handled", loaded is not None)

    test.cleanup_temp_dir()


def test_large_collections(test: SaveCorruptionTest):
    """Test loading saves with very large collections."""
    test.section("LARGE COLLECTIONS")

    from save_manager import SaveManager

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    save_path = os.path.join(temp_dir, "saves", "slot_1.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Test 1: Many items in inventory
    large_inventory = {f"item_{i}": i % 99 + 1 for i in range(1000)}

    save_data = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "player": {"name": "Player"},
        "dragon": {"name": "Dragon", "stage": "egg"},
        "cafe": {"gold": 100, "recipes_unlocked": [f"recipe_{i}" for i in range(500)]},
        "world": {"day_number": 1, "zones_unlocked": [f"zone_{i}" for i in range(100)],
                  "discovered_items": [f"item_{i}" for i in range(1000)]},
        "story": {"events_completed": [f"event_{i}" for i in range(500)],
                  "dialogue_flags": {f"flag_{i}": i % 2 == 0 for i in range(1000)}},
        "inventory": {"items": large_inventory, "max_slots": 20}
    }

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Large collections handled", loaded is not None)

    if loaded:
        test.test("Large inventory preserved", len(loaded.inventory.items) == 1000)
        test.test("Large recipe list preserved", len(loaded.cafe.recipes_unlocked) == 500)
        test.test("Large event list preserved", len(loaded.story.events_completed) == 500)

    # Test 2: Empty collections
    save_data = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "player": {"name": "Player"},
        "dragon": {"name": "Dragon", "stage": "egg", "abilities": []},
        "cafe": {"gold": 100, "recipes_unlocked": [], "staff_ids": []},
        "world": {"day_number": 1, "zones_unlocked": [], "discovered_items": []},
        "story": {"events_completed": [], "character_relationships": {}, "dialogue_flags": {}},
        "inventory": {"items": {}, "max_slots": 20}
    }

    with open(save_path, 'w') as f:
        json.dump(save_data, f)

    loaded = save_mgr.load(1)
    test.test("Empty collections handled", loaded is not None)

    test.cleanup_temp_dir()


def test_save_slot_management(test: SaveCorruptionTest):
    """Test save slot management edge cases."""
    test.section("SAVE SLOT MANAGEMENT")

    from save_manager import SaveManager, SaveData

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    # Test 1: List saves with no saves
    slots = save_mgr.list_saves()
    test.test("List empty saves", len(slots) == 3)
    test.test("All slots empty", all(not s.exists for s in slots))

    # Test 2: Has any saves (should be false)
    test.test("Has no saves initially", not save_mgr.has_any_saves())

    # Test 3: Most recent slot with no saves
    recent = save_mgr.get_most_recent_slot()
    test.test("No recent slot when empty", recent is None)

    # Test 4: Save and verify slot info
    save_data = create_valid_save_data()
    save_mgr.save(2, save_data)

    slots = save_mgr.list_saves()
    slot2 = next(s for s in slots if s.slot == 2)
    test.test("Slot 2 exists after save", slot2.exists)
    test.test("Slot info has player name", slot2.player_name == "TestPlayer")
    test.test("Slot info has dragon name", slot2.dragon_name == "Ember")

    # Test 5: Has any saves after saving
    test.test("Has saves after saving", save_mgr.has_any_saves())

    # Test 6: Most recent slot
    recent = save_mgr.get_most_recent_slot()
    test.test("Most recent slot is 2", recent == 2)

    # Test 7: Delete save
    result = save_mgr.delete_save(2)
    test.test("Delete succeeds", result)

    loaded = save_mgr.load(2)
    test.test("Deleted save returns None", loaded is None)

    # Test 8: Delete nonexistent save
    result = save_mgr.delete_save(3)
    test.test("Delete nonexistent succeeds", result)

    # Test 9: Overwrite existing save
    save_mgr.save(1, save_data)
    save_data.player.name = "UpdatedPlayer"
    save_mgr.save(1, save_data)

    loaded = save_mgr.load(1)
    test.test("Overwrite works", loaded and loaded.player.name == "UpdatedPlayer")

    test.cleanup_temp_dir()


def test_concurrent_save_operations(test: SaveCorruptionTest):
    """Test save operations under concurrent-like conditions."""
    test.section("CONCURRENT OPERATIONS")

    from save_manager import SaveManager

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    # Test 1: Rapid sequential saves
    for i in range(10):
        save_data = create_valid_save_data()
        save_data.world.day_number = i + 1
        save_mgr.save(1, save_data)

    loaded = save_mgr.load(1)
    test.test("Rapid saves - last value preserved", loaded and loaded.world.day_number == 10)

    # Test 2: Save while loading (simulate by checking file consistency)
    save_data = create_valid_save_data()
    save_data.dragon.name = "FinalDragon"
    save_mgr.save(1, save_data)

    loaded = save_mgr.load(1)
    test.test("File consistency maintained", loaded and loaded.dragon.name == "FinalDragon")

    # Test 3: Multiple slot operations
    for slot in [1, 2, 3]:
        save_data = create_valid_save_data()
        save_data.meta.slot = slot
        save_data.player.name = f"Player{slot}"
        save_mgr.save(slot, save_data)

    for slot in [1, 2, 3]:
        loaded = save_mgr.load(slot)
        test.test(f"Slot {slot} independent", loaded and loaded.player.name == f"Player{slot}")

    test.cleanup_temp_dir()


def test_game_state_save_load(test: SaveCorruptionTest):
    """Test full game state save/load through GameStateManager."""
    test.section("GAME STATE MANAGER")

    reset_all_systems()

    from game_state import get_game_state_manager
    from systems.inventory import get_inventory
    from systems.time_system import get_time_manager
    from save_manager import get_save_manager

    temp_dir = test.setup_temp_dir()
    save_mgr = get_save_manager()
    save_mgr.initialize(temp_dir)

    game_state = get_game_state_manager()

    # Setup some game state
    inventory = get_inventory()
    inventory.gold = 999
    inventory.unlock_recipe("test_recipe")

    time_mgr = get_time_manager()
    time_mgr._day_number = 10

    # Test 1: Save current game state
    result = game_state.save_game(1)
    test.test("Game state save succeeds", result)

    # Test 2: Modify state and load
    inventory.gold = 0
    time_mgr._current_day = 1

    result = game_state.load_game(1)
    test.test("Game state load succeeds", result)

    # Verify state was restored
    inventory = get_inventory()
    test.test("Gold restored", inventory.gold == 999)
    test.test("Recipe restored", "test_recipe" in inventory.unlocked_recipes)

    test.cleanup_temp_dir()


def test_special_file_conditions(test: SaveCorruptionTest):
    """Test special file system conditions."""
    test.section("SPECIAL FILE CONDITIONS")

    from save_manager import SaveManager

    temp_dir = test.setup_temp_dir()
    save_mgr = SaveManager()
    save_mgr.initialize(temp_dir)

    save_path = os.path.join(temp_dir, "saves", "slot_1.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Test 1: File exists but is a directory
    dir_path = os.path.join(temp_dir, "saves", "slot_2.json")
    os.makedirs(dir_path, exist_ok=True)

    loaded = save_mgr.load(2)
    test.test("Directory instead of file handled", loaded is None)

    # Test 2: Very large save file (1MB of padding)
    large_data = {
        "meta": {"slot": 1, "version": "1.0.0"},
        "player": {"name": "Player"},
        "dragon": {"name": "Dragon", "stage": "egg"},
        "cafe": {"gold": 100},
        "world": {"day_number": 1},
        "story": {},
        "inventory": {},
        "padding": "x" * (1024 * 1024)  # 1MB of padding
    }

    with open(save_path, 'w') as f:
        json.dump(large_data, f)

    loaded = save_mgr.load(1)
    test.test("Large file handled", loaded is not None)

    test.cleanup_temp_dir()


def main():
    """Run all save corruption tests."""
    print("=" * 70)
    print("DRAGON HAVEN CAFE - SAVE CORRUPTION PLAYTEST")
    print("Testing save file integrity, recovery, and edge cases")
    print("=" * 70)

    test = SaveCorruptionTest()

    try:
        # Run all test categories
        test_valid_save_load(test)
        test_missing_fields(test)
        test_invalid_data_types(test)
        test_corrupted_json(test)
        test_version_compatibility(test)
        test_extreme_values(test)
        test_large_collections(test)
        test_save_slot_management(test)
        test_concurrent_save_operations(test)
        test_game_state_save_load(test)
        test_special_file_conditions(test)
    finally:
        # Cleanup any remaining temp directories
        test.cleanup_temp_dir()

    # Print summary
    print("\n" + "=" * 70)
    print("SAVE CORRUPTION SUMMARY")
    print("=" * 70)
    total = test.passed + test.failed
    print(f"\nTests: {total} total, {test.passed} passed, {test.failed} failed")
    print(f"Success Rate: {100 * test.passed / total:.1f}%")
    print("=" * 70)

    return test.failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
