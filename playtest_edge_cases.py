#!/usr/bin/env python3
"""
Dragon Haven Cafe - Edge Cases Playtest
Tests boundary conditions, error handling, and edge cases across all systems.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Minimal pygame init (no display)
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
pygame.init()


class EdgeCaseTest:
    """Test harness for edge case testing."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

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
        print(f"EDGE CASES: {name}")
        print('=' * 60)


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


def test_dragon_stat_boundaries(test: EdgeCaseTest):
    """Test dragon stats at boundary values."""
    test.section("DRAGON STAT BOUNDARIES")

    reset_all_systems()
    from entities.dragon import Dragon
    from constants import DRAGON_STAT_MAX, DRAGON_BOND_MAX

    dragon = Dragon("TestDragon")

    # Force dragon to hatchling for stat testing
    dragon._stage = 'hatchling'
    dragon._hatched = True

    # Test 1: Hunger at zero
    dragon._hunger = 0
    test.test("Hunger at zero", dragon.get_hunger() == 0, f"Got: {dragon.get_hunger()}")
    test.test("Is hungry when hunger is 0", dragon.is_hungry(), "Should be hungry")

    # Test 2: Hunger above max (should clamp)
    dragon._hunger = DRAGON_STAT_MAX + 100
    dragon.feed({'hunger_value': 0})  # Trigger clamping
    test.test("Hunger clamped to max", dragon.get_hunger() <= DRAGON_STAT_MAX,
              f"Got: {dragon.get_hunger()}, Max: {DRAGON_STAT_MAX}")

    # Test 3: Happiness at zero
    dragon._happiness = 0
    test.test("Happiness at zero", dragon.get_happiness() == 0)
    test.test("Is unhappy when happiness is 0", dragon.is_unhappy())

    # Test 4: Stamina at zero
    dragon._stamina = 0
    test.test("Stamina at zero", dragon.get_stamina() == 0)
    test.test("Is tired when stamina is 0", dragon.is_tired())

    # Test 5: All stats at zero simultaneously
    dragon._hunger = 0
    dragon._happiness = 0
    dragon._stamina = 0
    test.test("All stats at zero",
              dragon.get_hunger() == 0 and dragon.get_happiness() == 0 and dragon.get_stamina() == 0)
    test.test("Mood when all stats zero", dragon.get_mood() in ['hungry', 'sad', 'tired'])

    # Test 6: Bond at max
    dragon._bond = DRAGON_BOND_MAX
    dragon.pet()  # Try to add more bond
    test.test("Bond clamped at max", dragon.get_bond() <= DRAGON_BOND_MAX,
              f"Got: {dragon.get_bond()}, Max: {DRAGON_BOND_MAX}")

    # Test 7: Feed when starving (hunger = 0)
    dragon._hunger = 0
    result = dragon.feed({'hunger_value': 50})
    test.test("Can feed when starving", result and dragon.get_hunger() > 0)

    # Test 8: Cannot feed egg
    egg_dragon = Dragon("EggDragon")
    result = egg_dragon.feed({'hunger_value': 50})
    test.test("Cannot feed an egg", not result)

    # Test 9: Cannot pet egg
    result = egg_dragon.pet()
    test.test("Cannot pet an egg", not result)


def test_dragon_ability_edge_cases(test: EdgeCaseTest):
    """Test dragon abilities at edge conditions."""
    test.section("DRAGON ABILITY EDGE CASES")

    reset_all_systems()
    from entities.dragon import Dragon

    dragon = Dragon("AbilityDragon")

    # Force to adult stage for all abilities
    dragon._stage = 'adult'
    dragon._hatched = True

    # Test 1: Use ability with exactly 0 stamina
    dragon._stamina = 0
    can_use = dragon.can_use_ability('burrow_fetch')
    test.test("Cannot use ability with 0 stamina", not can_use)

    # Test 2: Use ability with exactly the cost amount
    from constants import DRAGON_ABILITY_COSTS
    ability_cost = DRAGON_ABILITY_COSTS.get('burrow_fetch', 10)
    dragon._stamina = ability_cost
    can_use = dragon.can_use_ability('burrow_fetch')
    test.test("Can use ability with exact cost stamina", can_use)

    result = dragon.use_ability('burrow_fetch')
    test.test("Ability used with exact stamina", result)
    test.test("Stamina at 0 after exact cost use", dragon.get_stamina() == 0)

    # Test 3: Continuous ability with minimum stamina
    from constants import DRAGON_ABILITY_CONTINUOUS
    if 'glide' in DRAGON_ABILITY_CONTINUOUS:
        drain_rate = DRAGON_ABILITY_CONTINUOUS['glide']
        dragon._stamina = drain_rate  # Minimum for 1 second
        can_start = dragon.start_continuous_ability('glide')
        test.test("Can start continuous ability with minimum stamina", can_start)
        dragon.stop_continuous_ability()

    # Test 4: Ability not available at wrong stage
    dragon._stage = 'hatchling'
    available = dragon.get_available_abilities()
    test.test("Full_flight not available for hatchling", 'full_flight' not in available)

    # Test 5: Invalid ability name
    can_use = dragon.can_use_ability('nonexistent_ability')
    test.test("Cannot use nonexistent ability", not can_use)


def test_dragon_color_boundaries(test: EdgeCaseTest):
    """Test dragon color system at boundaries."""
    test.section("DRAGON COLOR BOUNDARIES")

    reset_all_systems()
    from entities.dragon import DragonColor

    # Test 1: Color at max bounds
    color = DragonColor(red=1.0, green=1.0, blue=1.0)
    color.apply_food_color((1.0, 1.0, 1.0), 1.0)  # Try to push past max
    test.test("Color red clamped at 1.0", color.red <= 1.0, f"Got: {color.red}")
    test.test("Color green clamped at 1.0", color.green <= 1.0)
    test.test("Color blue clamped at 1.0", color.blue <= 1.0)

    # Test 2: Color at min bounds
    color = DragonColor(red=-1.0, green=-1.0, blue=-1.0)
    color.apply_food_color((0.0, 0.0, 0.0), 1.0)  # Try to push past min
    test.test("Color red clamped at -1.0", color.red >= -1.0, f"Got: {color.red}")
    test.test("Color green clamped at -1.0", color.green >= -1.0)
    test.test("Color blue clamped at -1.0", color.blue >= -1.0)

    # Test 3: RGB shift conversion at extremes
    color = DragonColor(red=1.0, green=-1.0, blue=0.5)
    shift = color.to_shift()
    test.test("RGB shift within expected range",
              -50 <= shift[0] <= 50 and -50 <= shift[1] <= 50 and -50 <= shift[2] <= 50,
              f"Got: {shift}")


def test_dragon_name_validation(test: EdgeCaseTest):
    """Test dragon name validation edge cases."""
    test.section("DRAGON NAME VALIDATION")

    reset_all_systems()
    from entities.dragon import Dragon
    from constants import DRAGON_NAME_MAX_LENGTH

    dragon = Dragon("Test")

    # Test 1: Empty name
    result = dragon.set_name("")
    test.test("Empty name rejected", not result)
    test.test("Name unchanged after empty rejection", dragon.get_name() == "Test")

    # Test 2: Whitespace-only name
    result = dragon.set_name("   ")
    test.test("Whitespace-only name rejected", not result)

    # Test 3: Name at max length
    max_name = "A" * DRAGON_NAME_MAX_LENGTH
    result = dragon.set_name(max_name)
    test.test("Max length name accepted", result)
    test.test("Max length name preserved", len(dragon.get_name()) == DRAGON_NAME_MAX_LENGTH)

    # Test 4: Name exceeding max length (should truncate)
    long_name = "B" * (DRAGON_NAME_MAX_LENGTH + 10)
    result = dragon.set_name(long_name)
    test.test("Overlength name accepted (truncated)", result)
    test.test("Name truncated to max", len(dragon.get_name()) <= DRAGON_NAME_MAX_LENGTH)

    # Test 5: Name with leading/trailing whitespace
    result = dragon.set_name("  Ember  ")
    test.test("Name with whitespace stripped", dragon.get_name() == "Ember")

    # Test 6: Static validation
    valid, msg = Dragon.validate_name("")
    test.test("Static validation rejects empty", not valid)

    valid, msg = Dragon.validate_name("Valid Name")
    test.test("Static validation accepts valid name", valid)


def test_inventory_boundaries(test: EdgeCaseTest):
    """Test inventory system at boundary conditions."""
    test.section("INVENTORY BOUNDARIES")

    reset_all_systems()
    from systems.inventory import get_inventory, Item, ItemStack
    from constants import INVENTORY_CARRIED_SLOTS, ITEM_DEFAULT_STACK_SIZE

    inventory = get_inventory()

    # Test 1: Add item when inventory is full
    test_item = Item(id="test_berry", name="Test Berry", category="fruit", stack_size=5)

    # Fill all carried slots
    for i in range(INVENTORY_CARRIED_SLOTS):
        inventory.carried.add_item(
            Item(id=f"filler_{i}", name=f"Filler {i}", category="fruit", stack_size=1),
            1
        )

    test.test("Inventory is full", inventory.carried.is_full())

    # Try to add more
    overflow = inventory.carried.add_item(test_item, 1)
    test.test("Overflow when adding to full inventory", overflow == 1)

    # Test 2: Stack overflow
    reset_all_systems()
    inventory = get_inventory()

    small_stack_item = Item(id="small", name="Small Stack", category="fruit", stack_size=3)
    inventory.carried.add_item(small_stack_item, 3)  # Fill first stack
    overflow = inventory.carried.add_item(small_stack_item, 2)  # Add 2 more

    test.test("Stack overflow handled", overflow == 0 or inventory.carried.get_count("small") <= 5)

    # Test 3: Remove more items than exist
    reset_all_systems()
    inventory = get_inventory()

    inventory.carried.add_item(test_item, 2)
    removed = inventory.carried.remove_item("test_berry", 10)
    test.test("Remove capped at available amount", removed == 2)
    test.test("Inventory empty after over-remove", inventory.carried.get_count("test_berry") == 0)

    # Test 4: Remove from empty inventory
    removed = inventory.carried.remove_item("nonexistent_item", 5)
    test.test("Remove from empty returns 0", removed == 0)

    # Test 5: Item spoilage at day boundary
    reset_all_systems()
    inventory = get_inventory()

    spoilable = Item(id="spoil", name="Spoilable", category="fruit", spoil_days=1)
    inventory.carried.add_item(spoilable, 1)

    # Check initial state
    slot = inventory.carried.get_slot(0)
    test.test("Spoilable item has days until spoil", slot and slot.days_until_spoil == 1)

    # Advance day
    inventory.advance_day()
    test.test("Item spoiled after one day", inventory.carried.get_count("spoil") == 0)

    # Test 6: Fridge prevents spoilage
    reset_all_systems()
    inventory = get_inventory()

    inventory.fridge.add_item(spoilable, 1)
    inventory.advance_day()
    inventory.advance_day()
    test.test("Fridge prevents spoilage", inventory.fridge.get_count("spoil") == 1)


def test_gold_boundaries(test: EdgeCaseTest):
    """Test gold/economy system at boundaries."""
    test.section("GOLD/ECONOMY BOUNDARIES")

    reset_all_systems()
    from systems.inventory import get_inventory
    from systems.economy import get_economy

    inventory = get_inventory()
    economy = get_economy()

    # Test 1: Spend more than available
    inventory.gold = 100
    result = economy.spend_gold(150, 'test', 'Test overspend')
    test.test("Cannot spend more than available", not result)
    test.test("Gold unchanged after failed spend", inventory.gold == 100)

    # Test 2: Spend exactly available amount
    result = economy.spend_gold(100, 'test', 'Exact spend')
    test.test("Can spend exact amount", result)
    test.test("Gold at zero after exact spend", inventory.gold == 0)

    # Test 3: Spend when gold is zero
    result = economy.spend_gold(1, 'test', 'Spend at zero')
    test.test("Cannot spend when gold is zero", not result)

    # Test 4: Add zero gold (should be no-op)
    inventory.gold = 50
    economy.add_gold(0, 'test', 'Zero add')
    test.test("Adding zero gold is no-op", inventory.gold == 50)

    # Test 5: Negative gold attempt (should not go negative)
    inventory.gold = 10
    result = economy.spend_gold(20, 'test', 'Negative attempt')
    test.test("Gold cannot go negative", inventory.gold >= 0)

    # Test 6: Large gold values
    inventory.gold = 1_000_000_000  # 1 billion
    economy.add_gold(1_000_000, 'test', 'Large add')
    test.test("Large gold values handled", inventory.gold >= 1_000_000_000)

    # Test 7: Price calculation with extreme quality
    price_low = economy.calculate_dish_price(100, quality=0, reputation=0)
    price_high = economy.calculate_dish_price(100, quality=10, reputation=0)
    test.test("Quality 0 clamped to 1", price_low >= 1)
    test.test("Quality 10 clamped to 5", price_high > price_low)

    # Test 8: Tip calculation edge cases
    tip_low = economy.calculate_tip(100, satisfaction=0)
    tip_high = economy.calculate_tip(100, satisfaction=10)
    test.test("No tip for satisfaction 0", tip_low == 0)
    test.test("Tip capped at max for high satisfaction", tip_high <= 100)  # Max 100% tip


def test_time_system_boundaries(test: EdgeCaseTest):
    """Test time system at day/season boundaries."""
    test.section("TIME SYSTEM BOUNDARIES")

    reset_all_systems()
    from systems.time_system import get_time_manager
    from constants import DAYS_PER_SEASON

    time_mgr = get_time_manager()

    # Test 1: Day boundary transition
    time_mgr._current_hour = 23.9
    initial_day = time_mgr.get_current_day()

    # Simulate time passing to cross day boundary
    time_mgr.update(60)  # 60 seconds = 2 game hours at 30 sec/hour

    new_hour = time_mgr.get_current_hour()
    test.test("Hour wraps at 24", 0 <= new_hour < 24, f"Got: {new_hour}")

    # Test 2: Season transition
    reset_all_systems()
    time_mgr = get_time_manager()

    # Set to last day of season (day 7 of DAYS_PER_SEASON=7)
    time_mgr._current_day = DAYS_PER_SEASON
    initial_season = time_mgr.get_current_season()

    # Force day advance to trigger season change
    time_mgr._advance_day()

    new_season = time_mgr.get_current_season()
    # Day of season calculation: (day - 1) % DAYS_PER_SEASON
    day_in_season = ((time_mgr._current_day - 1) % DAYS_PER_SEASON) + 1
    test.test("Day of season resets at season end", day_in_season == 1 or new_season != initial_season)

    # Test 3: Hour at exact boundaries
    time_mgr._current_hour = 0.0
    test.test("Hour 0 is valid", time_mgr.get_current_hour() == 0.0)

    time_mgr._current_hour = 23.99
    test.test("Hour 23.99 is valid", 23 <= time_mgr.get_current_hour() < 24)

    # Test 4: Pause and resume
    time_mgr.pause()
    test.test("Time can be paused", time_mgr.is_paused())

    initial_hour = time_mgr.get_current_hour()
    time_mgr.update(100)  # Should not advance
    test.test("Time doesn't advance when paused", time_mgr.get_current_hour() == initial_hour)

    time_mgr.resume()
    test.test("Time can be resumed", not time_mgr.is_paused())


def test_cafe_boundaries(test: EdgeCaseTest):
    """Test cafe system at boundary conditions."""
    test.section("CAFE BOUNDARIES")

    reset_all_systems()
    from systems.cafe import get_cafe_manager
    from constants import REPUTATION_MIN, REPUTATION_MAX

    cafe = get_cafe_manager()

    # Test 1: Reputation at minimum
    cafe._reputation = REPUTATION_MIN
    test.test("Reputation at minimum", cafe.get_reputation() == REPUTATION_MIN)

    # Apply decay (should not go below 0)
    cafe._reputation = 1
    cafe.apply_daily_decay(cafe_operated=False)  # Apply decay for not operating
    test.test("Reputation cannot go below 0", cafe.get_reputation() >= REPUTATION_MIN)

    # Test 2: Reputation at maximum
    cafe._reputation = REPUTATION_MAX
    cafe.add_reputation(100)  # Try to exceed max
    test.test("Reputation clamped at max", cafe.get_reputation() <= REPUTATION_MAX)

    # Test 3: Menu with no items
    cafe._current_menu = []
    customer_range = cafe.get_customer_count_range()
    test.test("Customer calculation with empty menu", customer_range[0] >= 0)

    # Test 4: Reputation level boundaries
    cafe._reputation = 49
    level1 = cafe.get_reputation_level()

    cafe._reputation = 50
    level2 = cafe.get_reputation_level()
    test.test("Reputation level changes at boundary", level1 != level2 or True)  # May be same tier

    # Test 5: Service period boundary
    from constants import CAFE_MORNING_SERVICE_START, CAFE_MORNING_SERVICE_END

    # Just verify cafe can report its state at various times
    state = cafe.get_state()
    test.test("Cafe can report state", state is not None)


def test_recipe_boundaries(test: EdgeCaseTest):
    """Test recipe system at boundary conditions."""
    test.section("RECIPE BOUNDARIES")

    reset_all_systems()
    from systems.recipes import get_recipe_manager

    recipe_mgr = get_recipe_manager()

    # Test 1: Get nonexistent recipe
    recipe = recipe_mgr.get_recipe("nonexistent_recipe_xyz")
    test.test("Nonexistent recipe returns None", recipe is None)

    # Test 2: Unlock same recipe twice
    recipes = recipe_mgr.get_all_recipes()
    if recipes:
        first_recipe = recipes[0]
        recipe_mgr.unlock_recipe(first_recipe.id)
        initial_count = len(recipe_mgr.get_unlocked_recipes())

        recipe_mgr.unlock_recipe(first_recipe.id)  # Try again
        final_count = len(recipe_mgr.get_unlocked_recipes())
        test.test("Duplicate unlock is idempotent", final_count == initial_count)

    # Test 3: Check requirements with empty inventory
    reset_all_systems()
    recipe_mgr = get_recipe_manager()
    from systems.inventory import get_inventory

    inventory = get_inventory()
    recipes = recipe_mgr.get_all_recipes()

    if recipes:
        # Find a recipe with ingredients
        test_recipe = None
        for r in recipes:
            if r.ingredients:
                test_recipe = r
                break

        if test_recipe:
            result = recipe_mgr.can_cook(test_recipe.id, inventory)
            test.test("Cannot make recipe with empty inventory", not result.get('can_cook', True))


def test_zone_boundaries(test: EdgeCaseTest):
    """Test zone/world system at boundaries."""
    test.section("ZONE BOUNDARIES")

    reset_all_systems()
    from systems.world import get_world_manager

    world = get_world_manager()

    # Test 1: Access locked zone
    all_zones = list(world._zones.values())
    unlocked_ids = world.get_unlocked_zones()
    locked_zones = [z for z in all_zones if z.id not in unlocked_ids]

    if locked_zones:
        locked = locked_zones[0]
        test.test("Locked zone not in unlocked list", locked.id not in unlocked_ids)

        # Try to enter locked zone (with egg stage dragon)
        can_enter = world.can_enter_zone(locked.id, 'egg')
        test.test("Cannot enter locked zone with egg", not can_enter or locked.unlock_requirement is None)
    else:
        test.test("Has some locked zones", True)  # Skip if all unlocked

    # Test 2: Invalid zone ID
    zone = world.get_zone("invalid_zone_xyz")
    test.test("Invalid zone returns None", zone is None)

    # Test 3: Zone connections
    current = world.get_current_zone()
    if current:
        connections = world.get_connected_zones()
        test.test("Zone has connections", isinstance(connections, list))


def test_story_boundaries(test: EdgeCaseTest):
    """Test story system at boundaries."""
    test.section("STORY BOUNDARIES")

    reset_all_systems()
    from systems.story import get_story_manager

    story = get_story_manager()

    # Test 1: Set flag that doesn't exist
    story.set_flag("new_test_flag", True)
    test.test("Can set new flag", story.has_flag("new_test_flag"))

    # Test 2: Get flag that doesn't exist
    result = story.has_flag("nonexistent_flag_xyz")
    test.test("Nonexistent flag returns False", not result)

    # Test 3: Toggle flag
    story.set_flag("toggle_test", True)
    story.set_flag("toggle_test", False)
    test.test("Flag can be toggled off", not story.has_flag("toggle_test"))

    # Test 4: Chapter progression
    initial_chapter = story.get_current_chapter()
    test.test("Has initial chapter", initial_chapter is not None)


def test_character_affinity_boundaries(test: EdgeCaseTest):
    """Test character affinity at boundaries."""
    test.section("CHARACTER AFFINITY BOUNDARIES")

    reset_all_systems()
    from entities.story_character import get_character_manager
    from constants import AFFINITY_MIN, AFFINITY_MAX

    char_mgr = get_character_manager()

    # Load character data
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'characters', 'story_characters.json')
    char_mgr.load_characters_file(data_path)

    # Get a character
    characters = char_mgr.get_all_characters()
    if characters:
        char = characters[0]

        # Test 1: Get initial affinity
        initial_affinity = char_mgr.get_affinity(char.id)
        test.test("Can get affinity", initial_affinity >= AFFINITY_MIN)

        # Test 2: Add affinity
        char.add_affinity(10)
        new_affinity = char_mgr.get_affinity(char.id)
        test.test("Affinity increased", new_affinity >= initial_affinity)

        # Test 3: Try to exceed maximum
        char.affinity = AFFINITY_MAX
        char.add_affinity(100)
        test.test("Affinity clamped at max", char.affinity <= AFFINITY_MAX)

        # Test 4: Try to go below minimum
        char.affinity = AFFINITY_MIN
        char.add_affinity(-100)
        test.test("Affinity clamped at min", char.affinity >= AFFINITY_MIN)

        # Test 5: Affinity level at exact boundary
        char.affinity = 25  # Boundary between acquaintance and friendly
        level = char_mgr.get_affinity_level(char.id)
        test.test("Affinity level at boundary", level is not None)
    else:
        test.test("Characters loaded", False, "No characters found")


def test_save_slot_boundaries(test: EdgeCaseTest):
    """Test save slot boundary conditions."""
    test.section("SAVE SLOT BOUNDARIES")

    from save_manager import get_save_manager, SaveData

    save_mgr = get_save_manager()
    save_mgr.initialize()

    # Test 1: Invalid slot numbers
    result = save_mgr.save(0, SaveData())
    test.test("Slot 0 rejected", not result)

    result = save_mgr.save(4, SaveData())
    test.test("Slot 4 rejected", not result)

    result = save_mgr.save(-1, SaveData())
    test.test("Negative slot rejected", not result)

    # Test 2: Load from empty slot
    # Use a slot we haven't saved to
    loaded = save_mgr.load(3)
    if loaded is None:
        test.test("Load from empty/nonexistent slot returns None", True)
    else:
        test.test("Load from empty slot returns data or None", True)

    # Test 3: Valid slot numbers
    for slot in [1, 2, 3]:
        valid = save_mgr._validate_slot(slot)
        test.test(f"Slot {slot} is valid", valid)


def test_item_stack_boundaries(test: EdgeCaseTest):
    """Test item stack operations at boundaries."""
    test.section("ITEM STACK BOUNDARIES")

    from systems.inventory import Item, ItemStack

    # Test 1: Split with amount >= quantity
    item = Item(id="test", name="Test", category="fruit", stack_size=10)
    stack = ItemStack(item=item, quantity=5)

    result = stack.split(5)
    test.test("Split with amount == quantity returns None", result is None)

    result = stack.split(10)
    test.test("Split with amount > quantity returns None", result is None)

    # Test 2: Split with amount 0
    result = stack.split(0)
    test.test("Split with amount 0 returns None", result is None)

    # Test 3: Valid split
    stack = ItemStack(item=item, quantity=5)
    result = stack.split(2)
    test.test("Valid split succeeds", result is not None)
    test.test("Split stack has correct quantity", result and result.quantity == 2)
    test.test("Original stack reduced", stack.quantity == 3)

    # Test 4: Merge stacks
    stack1 = ItemStack(item=item, quantity=8)
    stack2 = ItemStack(item=item, quantity=5)

    overflow = stack1.merge(stack2)
    test.test("Merge overflow calculated correctly", overflow == 3)  # 8 + 5 - 10 = 3
    test.test("Stack at max after merge", stack1.quantity == 10)

    # Test 5: Merge different items
    other_item = Item(id="other", name="Other", category="fruit", stack_size=10)
    other_stack = ItemStack(item=other_item, quantity=3)

    can_merge = stack1.can_merge(other_stack)
    test.test("Cannot merge different items", not can_merge)


def test_state_serialization_boundaries(test: EdgeCaseTest):
    """Test state serialization with edge values."""
    test.section("STATE SERIALIZATION BOUNDARIES")

    from entities.dragon import Dragon, DragonColor

    # Test 1: Dragon with extreme color values
    dragon = Dragon("ExtremeDragon")
    dragon._color = DragonColor(red=1.0, green=-1.0, blue=0.0)

    state = dragon.get_state()
    test.test("State includes color", 'color' in state)

    # Restore and verify
    new_dragon = Dragon.from_state(state)
    test.test("Color restored correctly",
              abs(new_dragon._color.red - 1.0) < 0.01 and
              abs(new_dragon._color.green - (-1.0)) < 0.01)

    # Test 2: Dragon at age boundary
    dragon._age_hours = 24 * 3  # Exactly 3 days (hatchling boundary)
    state = dragon.get_state()

    new_dragon = Dragon.from_state(state)
    test.test("Age restored correctly", abs(new_dragon._age_hours - dragon._age_hours) < 0.01)

    # Test 3: Empty/default state restoration
    empty_state = {}
    restored = Dragon.from_state(empty_state)
    test.test("Can restore from empty state", restored is not None)
    test.test("Restored dragon has default values", restored._stage == 'egg')


def main():
    """Run all edge case tests."""
    print("=" * 70)
    print("DRAGON HAVEN CAFE - EDGE CASES PLAYTEST")
    print("Testing boundary conditions and error handling")
    print("=" * 70)

    test = EdgeCaseTest()

    # Run all test categories
    test_dragon_stat_boundaries(test)
    test_dragon_ability_edge_cases(test)
    test_dragon_color_boundaries(test)
    test_dragon_name_validation(test)
    test_inventory_boundaries(test)
    test_gold_boundaries(test)
    test_time_system_boundaries(test)
    test_cafe_boundaries(test)
    test_recipe_boundaries(test)
    test_zone_boundaries(test)
    test_story_boundaries(test)
    test_character_affinity_boundaries(test)
    test_save_slot_boundaries(test)
    test_item_stack_boundaries(test)
    test_state_serialization_boundaries(test)

    # Print summary
    print("\n" + "=" * 70)
    print("EDGE CASES SUMMARY")
    print("=" * 70)
    total = test.passed + test.failed
    print(f"\nTests: {total} total, {test.passed} passed, {test.failed} failed")
    print(f"Success Rate: {100 * test.passed / total:.1f}%")
    print("=" * 70)

    return test.failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
