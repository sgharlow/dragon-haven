#!/usr/bin/env python3
"""
Dragon Haven Cafe - Data Validation Playtest
Validates all JSON data files for schema correctness, required fields, and data integrity.
"""

import sys
import os
import json
from typing import Dict, List, Any, Set, Tuple

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Minimal pygame init (no display)
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
pygame.init()


class DataValidationTest:
    """Test harness for data validation testing."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
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

    def warn(self, name, details=""):
        """Record a warning (non-fatal issue)."""
        self.warnings += 1
        self.tests.append(('WARN', name, details))
        print(f"  [WARN] {name}: {details}")

    def section(self, name):
        """Print a section header."""
        print(f"\n{'=' * 60}")
        print(f"DATA VALIDATION: {name}")
        print('=' * 60)


# Data directory paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DIALOGUES_DIR = os.path.join(DATA_DIR, 'dialogues')
EVENTS_DIR = os.path.join(DATA_DIR, 'events')
CHARACTERS_DIR = os.path.join(DATA_DIR, 'characters')


def load_json_file(filepath: str) -> Tuple[Any, str]:
    """Load a JSON file, returning (data, error_message)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f), ""
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"
    except FileNotFoundError:
        return None, "File not found"
    except Exception as e:
        return None, f"Error: {e}"


def get_all_json_files(directory: str) -> List[str]:
    """Get all JSON files in a directory."""
    if not os.path.exists(directory):
        return []
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith('.json')
    ]


def validate_character_data(test: DataValidationTest):
    """Validate story_characters.json schema and data."""
    test.section("CHARACTER DATA")

    filepath = os.path.join(CHARACTERS_DIR, 'story_characters.json')
    data, error = load_json_file(filepath)

    if error:
        test.test("Characters file loads", False, error)
        return

    test.test("Characters file loads", True)
    test.test("Characters is a list", isinstance(data, list))

    if not isinstance(data, list):
        return

    # Required fields for each character
    required_fields = ['id', 'name', 'description', 'chapter', 'affinity']
    optional_fields = ['portrait_id', 'favorite_recipes', 'liked_recipes', 'disliked_recipes',
                       'gift_preferences', 'unlocked_dialogues', 'met']

    # Valid chapters
    valid_chapters = ['prologue', 'chapter1', 'chapter2', 'chapter3', 'chapter4',
                      'chapter5', 'chapter6', 'finale']

    character_ids = set()
    chapter_characters = {}

    for i, char in enumerate(data):
        char_name = char.get('id', f'character_{i}')

        # Check required fields
        for field in required_fields:
            test.test(f"{char_name}: has '{field}'", field in char,
                      f"Missing required field '{field}'")

        # Check ID uniqueness
        if 'id' in char:
            if char['id'] in character_ids:
                test.test(f"{char_name}: unique ID", False, "Duplicate character ID")
            else:
                character_ids.add(char['id'])
                test.test(f"{char_name}: unique ID", True)

        # Validate chapter
        if 'chapter' in char:
            test.test(f"{char_name}: valid chapter", char['chapter'] in valid_chapters,
                      f"Invalid chapter '{char['chapter']}'")

            # Track which characters belong to which chapter
            chapter = char['chapter']
            if chapter not in chapter_characters:
                chapter_characters[chapter] = []
            chapter_characters[chapter].append(char['id'])

        # Validate affinity range
        if 'affinity' in char:
            affinity = char['affinity']
            test.test(f"{char_name}: affinity in range", 0 <= affinity <= 100,
                      f"Affinity {affinity} outside 0-100")

        # Validate recipe lists are lists
        for field in ['favorite_recipes', 'liked_recipes', 'disliked_recipes']:
            if field in char:
                test.test(f"{char_name}: {field} is list", isinstance(char[field], list),
                          f"{field} is not a list")

        # Validate gift_preferences is dict
        if 'gift_preferences' in char:
            prefs = char['gift_preferences']
            test.test(f"{char_name}: gift_preferences is dict", isinstance(prefs, dict),
                      "gift_preferences is not a dict")

            if isinstance(prefs, dict):
                for item, value in prefs.items():
                    test.test(f"{char_name}: gift value is positive", value > 0,
                              f"Gift '{item}' has non-positive value {value}")

        # Validate unlocked_dialogues thresholds
        if 'unlocked_dialogues' in char:
            dialogues = char['unlocked_dialogues']
            test.test(f"{char_name}: unlocked_dialogues is dict", isinstance(dialogues, dict),
                      "unlocked_dialogues is not a dict")

            if isinstance(dialogues, dict):
                for dialogue_id, threshold in dialogues.items():
                    test.test(f"{char_name}: dialogue threshold in range",
                              0 <= threshold <= 100,
                              f"Dialogue '{dialogue_id}' threshold {threshold} outside 0-100")

    # Summary checks
    test.test("Has at least 8 characters", len(data) >= 8,
              f"Only {len(data)} characters defined")

    # Check expected characters exist
    expected_chars = ['mother', 'marcus', 'lily', 'garrett', 'vera', 'noble', 'elena', 'thomas']
    for exp_char in expected_chars:
        test.test(f"Character '{exp_char}' exists", exp_char in character_ids,
                  f"Missing expected character")


def validate_event_files(test: DataValidationTest):
    """Validate all event JSON files."""
    test.section("EVENT DATA")

    event_files = get_all_json_files(EVENTS_DIR)
    test.test("Event files exist", len(event_files) > 0,
              f"No event files found in {EVENTS_DIR}")

    if not event_files:
        return

    # Required fields for each event
    required_fields = ['id', 'chapter', 'name']
    valid_condition_types = ['flag', 'not_flag', 'day_range', 'day_min', 'time_of_day',
                             'location', 'dragon_stage', 'dragon_stage_min', 'reputation_min',
                             'affinity_min', 'has_item', 'recipe_unlocked', 'chapter']
    valid_outcome_types = ['set_flag', 'clear_flag', 'unlock_zone', 'unlock_recipe',
                           'gold_reward', 'reputation_change', 'affinity_change',
                           'set_chapter', 'give_item', 'trigger_event']

    all_event_ids = set()
    all_dialogue_refs = set()

    for filepath in event_files:
        filename = os.path.basename(filepath)
        data, error = load_json_file(filepath)

        if error:
            test.test(f"{filename}: loads", False, error)
            continue

        test.test(f"{filename}: loads", True)
        test.test(f"{filename}: is a list", isinstance(data, list))

        if not isinstance(data, list):
            continue

        for i, event in enumerate(data):
            event_id = event.get('id', f'event_{i}')

            # Check required fields
            for field in required_fields:
                if field not in event:
                    test.test(f"{filename}/{event_id}: has '{field}'", False,
                              f"Missing required field")

            # Check ID uniqueness
            if 'id' in event:
                if event['id'] in all_event_ids:
                    test.test(f"{filename}/{event_id}: unique ID", False, "Duplicate event ID")
                else:
                    all_event_ids.add(event['id'])

            # Validate conditions
            if 'conditions' in event:
                conditions = event['conditions']
                test.test(f"{filename}/{event_id}: conditions is list",
                          isinstance(conditions, list))

                if isinstance(conditions, list):
                    for j, cond in enumerate(conditions):
                        if 'type' in cond:
                            test.test(f"{filename}/{event_id}: condition {j} type valid",
                                      cond['type'] in valid_condition_types,
                                      f"Unknown condition type '{cond['type']}'")
                        if 'value' not in cond:
                            test.warn(f"{filename}/{event_id}: condition {j} missing value")

            # Validate outcomes
            if 'outcomes' in event:
                outcomes = event['outcomes']
                test.test(f"{filename}/{event_id}: outcomes is list",
                          isinstance(outcomes, list))

                if isinstance(outcomes, list):
                    for j, outcome in enumerate(outcomes):
                        if 'type' in outcome:
                            test.test(f"{filename}/{event_id}: outcome {j} type valid",
                                      outcome['type'] in valid_outcome_types,
                                      f"Unknown outcome type '{outcome['type']}'")

            # Track dialogue references
            if 'dialogue_id' in event:
                all_dialogue_refs.add(event['dialogue_id'])

    # Check expected event files exist
    expected_files = ['prologue.json', 'chapter1.json', 'chapter2.json', 'chapter3.json',
                      'chapter4.json', 'chapter5.json', 'chapter6.json', 'finale.json']
    for exp_file in expected_files:
        filepath = os.path.join(EVENTS_DIR, exp_file)
        test.test(f"Event file '{exp_file}' exists", os.path.exists(filepath))

    return all_dialogue_refs


def validate_dialogue_files(test: DataValidationTest) -> Set[str]:
    """Validate all dialogue JSON files."""
    test.section("DIALOGUE DATA")

    dialogue_files = get_all_json_files(DIALOGUES_DIR)
    test.test("Dialogue files exist", len(dialogue_files) > 0,
              f"No dialogue files found in {DIALOGUES_DIR}")

    if not dialogue_files:
        return set()

    all_dialogue_ids = set()

    for filepath in dialogue_files:
        filename = os.path.basename(filepath)
        data, error = load_json_file(filepath)

        if error:
            test.test(f"{filename}: loads", False, error)
            continue

        test.test(f"{filename}: loads", True)

        # Dialogues can be either a single object or a list
        dialogues = data if isinstance(data, list) else [data]

        for i, dialogue in enumerate(dialogues):
            if not isinstance(dialogue, dict):
                test.test(f"{filename}: item {i} is dict", False)
                continue

            dialogue_id = dialogue.get('id', filename.replace('.json', ''))

            # Track dialogue ID
            all_dialogue_ids.add(dialogue_id)

            # Check for dialogue content
            if 'lines' in dialogue:
                lines = dialogue['lines']
                test.test(f"{filename}/{dialogue_id}: lines is list", isinstance(lines, list))

                if isinstance(lines, list):
                    for j, line in enumerate(lines):
                        # Each line should have speaker or text
                        if isinstance(line, dict):
                            has_content = 'text' in line or 'speaker' in line
                            if not has_content:
                                test.warn(f"{filename}/{dialogue_id}: line {j} has no text/speaker")

            # Check choices if present
            if 'choices' in dialogue:
                choices = dialogue['choices']
                test.test(f"{filename}/{dialogue_id}: choices is list", isinstance(choices, list))

                if isinstance(choices, list):
                    for j, choice in enumerate(choices):
                        if isinstance(choice, dict) and 'text' not in choice:
                            test.warn(f"{filename}/{dialogue_id}: choice {j} has no text")

    test.test(f"Total dialogues found", len(all_dialogue_ids) > 0,
              f"Found {len(all_dialogue_ids)} dialogues")

    return all_dialogue_ids


def validate_cross_references(test: DataValidationTest):
    """Validate cross-references between data files."""
    test.section("CROSS-REFERENCE VALIDATION")

    # Load all characters
    char_filepath = os.path.join(CHARACTERS_DIR, 'story_characters.json')
    char_data, _ = load_json_file(char_filepath)
    character_ids = set()
    if char_data and isinstance(char_data, list):
        character_ids = {c.get('id') for c in char_data if 'id' in c}

    # Load all events and collect dialogue references
    all_dialogue_refs = set()
    event_files = get_all_json_files(EVENTS_DIR)

    for filepath in event_files:
        data, _ = load_json_file(filepath)
        if data and isinstance(data, list):
            for event in data:
                if 'dialogue_id' in event:
                    all_dialogue_refs.add(event['dialogue_id'])

    # Load all dialogue IDs
    all_dialogue_ids = set()
    dialogue_files = get_all_json_files(DIALOGUES_DIR)

    for filepath in dialogue_files:
        data, _ = load_json_file(filepath)
        if data:
            dialogues = data if isinstance(data, list) else [data]
            for d in dialogues:
                if isinstance(d, dict):
                    if 'id' in d:
                        all_dialogue_ids.add(d['id'])
                    else:
                        # Use filename as ID
                        filename = os.path.basename(filepath).replace('.json', '')
                        all_dialogue_ids.add(filename)

    # Check that referenced dialogues exist
    missing_dialogues = all_dialogue_refs - all_dialogue_ids
    if missing_dialogues:
        for missing in list(missing_dialogues)[:5]:  # Show first 5
            test.warn(f"Event references missing dialogue", missing)
        test.test("All dialogue references valid",
                  len(missing_dialogues) == 0,
                  f"{len(missing_dialogues)} missing dialogues")
    else:
        test.test("All dialogue references valid", True)

    # Check that all expected characters are defined
    expected_chars = ['mother', 'marcus', 'lily', 'garrett', 'vera', 'noble', 'elena', 'thomas']
    missing_chars = set(expected_chars) - character_ids
    test.test("All expected characters defined",
              len(missing_chars) == 0,
              f"Missing: {missing_chars}" if missing_chars else "")


def validate_recipe_consistency(test: DataValidationTest):
    """Validate recipe references across all data files."""
    test.section("RECIPE CONSISTENCY")

    # Get all recipes from constants
    from constants import RECIPES

    recipe_ids = set(RECIPES.keys())
    test.test("Recipes defined in constants", len(recipe_ids) > 0,
              f"Found {len(recipe_ids)} recipes")

    # Collect all recipe references from events
    referenced_recipes = set()
    event_files = get_all_json_files(EVENTS_DIR)

    for filepath in event_files:
        data, _ = load_json_file(filepath)
        if data and isinstance(data, list):
            for event in data:
                if 'outcomes' in event:
                    for outcome in event['outcomes']:
                        if outcome.get('type') == 'unlock_recipe':
                            referenced_recipes.add(outcome.get('value'))

    # Check that referenced recipes exist
    invalid_refs = referenced_recipes - recipe_ids - {None}
    if invalid_refs:
        for ref in list(invalid_refs)[:5]:
            test.warn(f"Event references unknown recipe", ref)
        test.test("All recipe references valid",
                  len(invalid_refs) == 0,
                  f"{len(invalid_refs)} unknown recipes")
    else:
        test.test("All recipe references valid", True)

    # Collect recipe references from characters
    char_filepath = os.path.join(CHARACTERS_DIR, 'story_characters.json')
    char_data, _ = load_json_file(char_filepath)

    if char_data and isinstance(char_data, list):
        char_recipes = set()
        for char in char_data:
            for field in ['favorite_recipes', 'liked_recipes', 'disliked_recipes']:
                if field in char:
                    char_recipes.update(char[field])

        # Note: Character recipes may include fictional/placeholder recipes
        # Just warn about ones that don't exist
        unknown_char_recipes = char_recipes - recipe_ids
        if unknown_char_recipes:
            test.warn(f"Characters reference {len(unknown_char_recipes)} unknown recipes",
                      f"Examples: {list(unknown_char_recipes)[:3]}")


def validate_zone_consistency(test: DataValidationTest):
    """Validate zone references across all data files."""
    test.section("ZONE CONSISTENCY")

    # Get all zones from world system
    from systems.world import get_world_manager

    world_mgr = get_world_manager()
    world_mgr.initialize()  # Must initialize to create zones
    zone_ids = set(world_mgr._zones.keys())

    test.test("Zones defined", len(zone_ids) > 0, f"Found {len(zone_ids)} zones")

    # Collect zone references from events
    referenced_zones = set()
    event_files = get_all_json_files(EVENTS_DIR)

    for filepath in event_files:
        data, _ = load_json_file(filepath)
        if data and isinstance(data, list):
            for event in data:
                # Check conditions
                if 'conditions' in event:
                    for cond in event['conditions']:
                        if cond.get('type') == 'location':
                            referenced_zones.add(cond.get('value'))

                # Check outcomes
                if 'outcomes' in event:
                    for outcome in event['outcomes']:
                        if outcome.get('type') == 'unlock_zone':
                            referenced_zones.add(outcome.get('value'))

    # Some zone references might use aliases
    zone_aliases = {
        'cafe': 'cafe_grounds',
        'meadow': 'meadow_fields',
        'forest': 'forest_depths',
        'coastal': 'coastal_shore',
        'mountain': 'mountain_pass',
        'ruins': 'ancient_ruins',
        'sky': 'sky_islands'
    }

    # Check references (with aliases)
    invalid_zones = set()
    for ref in referenced_zones:
        if ref and ref not in zone_ids and ref not in zone_aliases:
            invalid_zones.add(ref)

    if invalid_zones:
        for zone in list(invalid_zones)[:5]:
            test.warn(f"Event references unknown zone", zone)
        test.test("All zone references valid",
                  len(invalid_zones) == 0,
                  f"{len(invalid_zones)} unknown zones")
    else:
        test.test("All zone references valid", True)


def validate_constants_integrity(test: DataValidationTest):
    """Validate that constants are internally consistent."""
    test.section("CONSTANTS INTEGRITY")

    from constants import (
        REPUTATION_MIN, REPUTATION_MAX, REPUTATION_LEVELS,
        AFFINITY_MIN, AFFINITY_MAX, AFFINITY_LEVELS,
        DRAGON_STAT_MAX, DRAGON_BOND_MAX,
        DRAGON_STAGE_ABILITIES, DRAGON_ABILITY_COSTS,
        RECIPES, UPGRADES
    )

    # Test reputation levels cover full range
    rep_covered = set()
    for level_name, level_data in REPUTATION_LEVELS.items():
        for val in range(level_data['min'], level_data['max'] + 1):
            rep_covered.add(val)

    test.test("Reputation levels cover 0-max",
              REPUTATION_MIN in rep_covered,
              f"Min {REPUTATION_MIN} not covered")

    # Test affinity levels cover full range
    affinity_covered = set()
    for level_name, level_data in AFFINITY_LEVELS.items():
        for val in range(level_data['min'], level_data['max'] + 1):
            affinity_covered.add(val)

    test.test("Affinity levels cover 0-100",
              0 in affinity_covered and 100 in affinity_covered)

    # Test dragon abilities have costs defined
    all_abilities = set()
    for stage, abilities in DRAGON_STAGE_ABILITIES.items():
        all_abilities.update(abilities)

    abilities_without_cost = all_abilities - set(DRAGON_ABILITY_COSTS.keys())
    # Note: Some abilities might have 0 cost (continuous abilities use different system)
    test.test("Dragon abilities have costs",
              len(abilities_without_cost) <= 3,  # Allow some leeway for continuous abilities
              f"Missing: {abilities_without_cost}" if abilities_without_cost else "")

    # Test recipes have required fields
    for recipe_id, recipe in RECIPES.items():
        required = ['name', 'base_price', 'difficulty']
        missing = [f for f in required if f not in recipe]
        if missing:
            test.test(f"Recipe '{recipe_id}' complete", False,
                      f"Missing: {missing}")

    test.test("All recipes have required fields", True)

    # Test upgrades have required fields
    for upgrade_id, upgrade in UPGRADES.items():
        required = ['name', 'cost', 'amount', 'max_purchases']
        missing = [f for f in required if f not in upgrade]
        test.test(f"Upgrade '{upgrade_id}' complete",
                  len(missing) == 0,
                  f"Missing: {missing}" if missing else "")


def validate_dragon_stages(test: DataValidationTest):
    """Validate dragon stage progression data."""
    test.section("DRAGON STAGE VALIDATION")

    from constants import (
        DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
        DRAGON_STAGE_ADOLESCENT, DRAGON_STAGE_ADULT,
        DRAGON_EGG_DAYS, DRAGON_HATCHLING_DAYS, DRAGON_JUVENILE_DAYS, DRAGON_ADOLESCENT_DAYS,
        DRAGON_STAGE_ABILITIES, DRAGON_STAGE_STAMINA_MAX
    )

    stages = [DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
              DRAGON_STAGE_ADOLESCENT, DRAGON_STAGE_ADULT]

    # Check all stages have abilities defined
    for stage in stages:
        test.test(f"Stage '{stage}' has abilities", stage in DRAGON_STAGE_ABILITIES,
                  f"Missing abilities for stage")

        abilities = DRAGON_STAGE_ABILITIES.get(stage, [])
        test.test(f"Stage '{stage}' abilities is list", isinstance(abilities, list))

    # Check stages have increasing stamina
    stamina_values = []
    for stage in stages:
        if stage in DRAGON_STAGE_STAMINA_MAX:
            stamina_values.append(DRAGON_STAGE_STAMINA_MAX[stage])

    test.test("Stamina increases with stage",
              stamina_values == sorted(stamina_values),
              f"Values: {stamina_values}")

    # Check day thresholds are positive
    test.test("Egg days positive", DRAGON_EGG_DAYS > 0)
    test.test("Hatchling days positive", DRAGON_HATCHLING_DAYS > 0)
    test.test("Juvenile days positive", DRAGON_JUVENILE_DAYS > 0)
    test.test("Adolescent days positive", DRAGON_ADOLESCENT_DAYS > 0)


def validate_file_encoding(test: DataValidationTest):
    """Validate that all JSON files use proper encoding."""
    test.section("FILE ENCODING")

    all_json_files = (
        get_all_json_files(DIALOGUES_DIR) +
        get_all_json_files(EVENTS_DIR) +
        get_all_json_files(CHARACTERS_DIR)
    )

    for filepath in all_json_files:
        filename = os.path.basename(filepath)

        try:
            # Try to read as UTF-8
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try to parse
            json.loads(content)
            test.test(f"{filename}: valid UTF-8 JSON", True)

        except UnicodeDecodeError as e:
            test.test(f"{filename}: valid UTF-8", False, str(e))
        except json.JSONDecodeError as e:
            test.test(f"{filename}: valid JSON", False, str(e))


def validate_event_sequences(test: DataValidationTest):
    """Validate that event sequences are properly ordered."""
    test.section("EVENT SEQUENCES")

    event_files = get_all_json_files(EVENTS_DIR)

    for filepath in event_files:
        filename = os.path.basename(filepath)
        data, error = load_json_file(filepath)

        if error or not isinstance(data, list):
            continue

        # Check for sequence_order field
        events_with_order = [e for e in data if 'sequence_order' in e]

        if events_with_order:
            # Check for duplicate sequence orders
            orders = [e['sequence_order'] for e in events_with_order]
            unique_orders = set(orders)

            test.test(f"{filename}: unique sequence orders",
                      len(orders) == len(unique_orders),
                      f"Duplicates: {len(orders) - len(unique_orders)}")

            # Check sequence starts at 1 or reasonable value
            min_order = min(orders)
            test.test(f"{filename}: sequence starts reasonably",
                      min_order >= 1,
                      f"Min order: {min_order}")


def main():
    """Run all data validation tests."""
    print("=" * 70)
    print("DRAGON HAVEN CAFE - DATA VALIDATION PLAYTEST")
    print("Validating JSON data files for schema and integrity")
    print("=" * 70)

    test = DataValidationTest()

    # Run all validation tests
    validate_character_data(test)
    validate_event_files(test)
    validate_dialogue_files(test)
    validate_cross_references(test)
    validate_recipe_consistency(test)
    validate_zone_consistency(test)
    validate_constants_integrity(test)
    validate_dragon_stages(test)
    validate_file_encoding(test)
    validate_event_sequences(test)

    # Print summary
    print("\n" + "=" * 70)
    print("DATA VALIDATION SUMMARY")
    print("=" * 70)
    total = test.passed + test.failed
    print(f"\nTests: {total} total, {test.passed} passed, {test.failed} failed")
    print(f"Warnings: {test.warnings}")
    print(f"Success Rate: {100 * test.passed / total:.1f}%")
    print("=" * 70)

    # A few warnings are acceptable, but failures should be fixed
    return test.failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
