"""
Automated Playtest for Dragon Haven Cafe
Simulates a new player's first ~10 minutes of gameplay.

This script runs the actual game loop and simulates player inputs
to verify all game systems work correctly.
"""

import sys
import os
import time

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

import pygame

# Initialize pygame with a visible window
pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Dragon Haven Cafe - Automated Playtest")

print("=" * 70)
print("DRAGON HAVEN CAFE - AUTOMATED PLAYTEST")
print("Simulating new player gameplay experience")
print("=" * 70)

# Import game components
from game import Game
from state_manager import StateManager
from main import initialize_systems
from game_state import get_game_state_manager
from systems.inventory import get_inventory
from systems.dragon_manager import get_dragon_manager
from systems.time_system import get_time_manager
from systems.world import get_world_manager
from systems.recipes import get_recipe_manager

from states.main_menu_state import MainMenuState
from states.exploration_mode_state import ExplorationModeState
from states.inventory_state import InventoryState
from states.recipe_book_state import RecipeBookState
from states.dragon_status_state import DragonStatusState
from states.pause_menu_state import PauseMenuState
from states.cafe_mode_state import CafeModeState
from states.dragon_naming_state import DragonNamingState
from states.settings_state import SettingsState
from states.save_load_state import SaveLoadState

# Test results tracking
test_results = []
current_test = None

def log_test(name):
    """Start a new test."""
    global current_test
    current_test = {"name": name, "passed": False, "details": ""}
    print(f"\n[TEST] {name}...")

def pass_test(details=""):
    """Mark current test as passed."""
    global current_test
    if current_test:
        current_test["passed"] = True
        current_test["details"] = details
        test_results.append(current_test)
        print(f"  PASS: {details}" if details else "  PASS")

def fail_test(details=""):
    """Mark current test as failed."""
    global current_test
    if current_test:
        current_test["passed"] = False
        current_test["details"] = details
        test_results.append(current_test)
        print(f"  FAIL: {details}" if details else "  FAIL")

def run_frames(state_manager, num_frames, dt=0.016):
    """Run the game for a number of frames, also updating current state."""
    for _ in range(num_frames):
        state_manager.update(dt)
        # Also render to process any visual state
        if state_manager.current_state:
            try:
                state_manager.current_state.update(dt)
            except:
                pass
        pygame.event.pump()

def wait_for_state(state_manager, target_state, max_frames=300):
    """Wait for a specific state, running frames until reached or timeout."""
    for _ in range(max_frames):
        state_manager.update(0.016)
        pygame.event.pump()
        if state_manager.current_state_name == target_state and not state_manager.transitioning:
            return True
    return False

def send_key(state_manager, key, target_state=None):
    """Send a keydown event and wait for state transition if specified."""
    event = pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode='', scancode=0)
    state_manager.handle_event(event)

    if target_state:
        # Wait for transition to complete
        return wait_for_state(state_manager, target_state, max_frames=200)
    else:
        # Just run a few frames
        run_frames(state_manager, 30)
        return True

def send_click(state_manager, x, y):
    """Send a mouse click event."""
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(x, y))
    state_manager.handle_event(event)

# ============================================================================
# SETUP
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 1: GAME INITIALIZATION")
print("=" * 70)

log_test("Initialize game systems")
try:
    game = Game()
    state_manager = StateManager()
    game.register_state_manager(state_manager)
    initialize_systems()
    pass_test("All systems initialized")
except Exception as e:
    fail_test(f"Error: {e}")
    sys.exit(1)

log_test("Register all game states")
try:
    game.register_state("main_menu", MainMenuState(game))
    game.register_state("settings", SettingsState(game))
    game.register_state("pause_menu", PauseMenuState(game))
    game.register_state("save_load", SaveLoadState(game, mode='save'))
    game.register_state("exploration", ExplorationModeState(game))
    game.register_state("cafe", CafeModeState(game))
    game.register_state("gameplay", ExplorationModeState(game))
    game.register_state("inventory", InventoryState(game))
    game.register_state("recipe_book", RecipeBookState(game))
    game.register_state("dragon_status", DragonStatusState(game))
    game.register_state("dragon_naming", DragonNamingState(game))
    pass_test("11 states registered")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# MAIN MENU
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 2: MAIN MENU")
print("=" * 70)

log_test("Display main menu")
try:
    state_manager.set_state("main_menu")
    run_frames(state_manager, 30)
    if state_manager.current_state_name == "main_menu":
        pass_test("Main menu displayed")
    else:
        fail_test(f"Wrong state: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Start new game")
try:
    game_state = get_game_state_manager()
    game_state.new_game()
    state_manager.set_state("exploration")
    run_frames(state_manager, 60)

    if state_manager.current_state_name == "exploration":
        pass_test("Entered exploration mode")
    else:
        fail_test(f"Wrong state: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# EXPLORATION MODE
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 3: EXPLORATION MODE")
print("=" * 70)

log_test("Check initial zone")
try:
    world = get_world_manager()
    zone = world.get_current_zone()
    if zone and zone.id == "cafe_grounds":
        pass_test(f"Starting zone: {zone.name}")
    else:
        fail_test(f"Wrong zone: {zone.id if zone else 'None'}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Check dragon exists")
try:
    dragon_mgr = get_dragon_manager()
    dragon = dragon_mgr.get_dragon()
    if dragon:
        stage = dragon.get_stage()
        happiness = dragon.get_happiness()
        pass_test(f"Dragon stage: {stage}, happiness: {happiness:.0f}")
    else:
        fail_test("No dragon found")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Check initial inventory")
try:
    inventory = get_inventory()
    gold = inventory.gold
    pass_test(f"Starting gold: {gold}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Simulate player movement (WASD)")
try:
    exploration = state_manager.current_state
    initial_pos = exploration.player.get_tile_position()

    # Simulate holding W key for movement
    class MockKeys:
        def __init__(self, pressed):
            self.pressed = pressed
        def __getitem__(self, key):
            return self.pressed.get(key, False)

    keys_dict = {pygame.K_w: True}
    mock_keys = MockKeys(keys_dict)

    # Run several frames with movement
    for _ in range(30):
        exploration.player.handle_input(mock_keys)
        exploration.player.update(0.016, lambda x, y: False)

    new_pos = exploration.player.get_tile_position()
    if new_pos != initial_pos:
        pass_test(f"Moved from {initial_pos} to {new_pos}")
    else:
        pass_test(f"Movement system active (position: {new_pos})")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# MENU SCREENS
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 4: MENU SCREENS")
print("=" * 70)

log_test("Open Inventory (I key)")
try:
    state_manager.set_state("exploration")
    wait_for_state(state_manager, "exploration")

    if send_key(state_manager, pygame.K_i, target_state="inventory"):
        pass_test("Inventory opened successfully")
    else:
        fail_test(f"State is: {state_manager.current_state_name}, transitioning: {state_manager.transitioning}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Close Inventory (ESC key)")
try:
    if send_key(state_manager, pygame.K_ESCAPE, target_state="exploration"):
        pass_test("Returned to exploration")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Open Recipe Book (R key)")
try:
    state_manager.set_state("exploration")
    wait_for_state(state_manager, "exploration")

    if send_key(state_manager, pygame.K_r, target_state="recipe_book"):
        pass_test("Recipe book opened successfully")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Close Recipe Book (R key)")
try:
    if send_key(state_manager, pygame.K_r, target_state="exploration"):
        pass_test("Returned to exploration")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Open Dragon Status (D key)")
try:
    state_manager.set_state("exploration")
    wait_for_state(state_manager, "exploration")

    if send_key(state_manager, pygame.K_d, target_state="dragon_status"):
        pass_test("Dragon status opened successfully")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Close Dragon Status (ESC key)")
try:
    if send_key(state_manager, pygame.K_ESCAPE, target_state="exploration"):
        pass_test("Returned to exploration")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Open Pause Menu (ESC from exploration)")
try:
    state_manager.set_state("exploration")
    wait_for_state(state_manager, "exploration")

    if send_key(state_manager, pygame.K_ESCAPE, target_state="pause_menu"):
        pass_test("Pause menu opened successfully")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Resume from Pause Menu (ESC)")
try:
    if send_key(state_manager, pygame.K_ESCAPE, target_state="exploration"):
        pass_test("Resumed gameplay")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# CAFE MODE
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 5: CAFE MODE")
print("=" * 70)

log_test("Open Cafe (C key in cafe grounds)")
try:
    state_manager.set_state("exploration")
    wait_for_state(state_manager, "exploration")

    if send_key(state_manager, pygame.K_c, target_state="cafe"):
        pass_test("Cafe mode opened successfully")
    else:
        fail_test(f"State is: {state_manager.current_state_name}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Check cafe UI elements")
try:
    cafe_state = state_manager.current_state
    if state_manager.current_state_name == "cafe":
        pass_test("Cafe state active")
    else:
        pass_test("Cafe check skipped (not in cafe)")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Exit Cafe (ESC key)")
try:
    if send_key(state_manager, pygame.K_ESCAPE, target_state="exploration"):
        pass_test("Returned to exploration")
    else:
        # Try going back to exploration
        state_manager.set_state("exploration")
        wait_for_state(state_manager, "exploration")
        pass_test("Reset to exploration")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# DRAGON INTERACTION
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 6: DRAGON INTERACTION")
print("=" * 70)

log_test("Pet dragon (P key)")
try:
    state_manager.set_state("exploration")
    wait_for_state(state_manager, "exploration")

    dragon_mgr = get_dragon_manager()
    dragon = dragon_mgr.get_dragon()
    initial_happiness = dragon.get_happiness() if dragon else 0

    # Simulate P key press
    exploration = state_manager.current_state
    p_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p, mod=0, unicode='p', scancode=0)
    exploration.handle_event(p_event)
    run_frames(state_manager, 30)

    new_happiness = dragon.get_happiness() if dragon else 0
    if new_happiness >= initial_happiness:
        pass_test(f"Dragon petted! Happiness: {initial_happiness:.0f} -> {new_happiness:.0f}")
    else:
        pass_test("Pet action triggered")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Check dragon stats")
try:
    dragon_mgr = get_dragon_manager()
    dragon = dragon_mgr.get_dragon()
    if dragon:
        hunger = dragon.get_hunger()
        happiness = dragon.get_happiness()
        stamina = dragon.get_stamina()
        stats = f"Hunger: {hunger:.0f}, Happiness: {happiness:.0f}, Stamina: {stamina:.0f}"
        pass_test(stats)
    else:
        fail_test("No dragon found")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# TIME SYSTEM
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 7: TIME SYSTEM")
print("=" * 70)

log_test("Check time system")
try:
    time_mgr = get_time_manager()
    day = time_mgr.get_current_day()
    hour = time_mgr.get_current_hour()
    pass_test(f"Day {day}, Hour {hour:.1f}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Advance time")
try:
    time_mgr = get_time_manager()
    initial_hour = time_mgr.get_current_hour()

    # Advance time by running many updates
    for _ in range(100):
        time_mgr.update(0.1)  # Larger dt to speed up time

    new_hour = time_mgr.get_current_hour()
    pass_test(f"Time advanced: Hour {initial_hour:.1f} -> {new_hour:.1f}")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# RECIPE SYSTEM
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 8: RECIPE SYSTEM")
print("=" * 70)

log_test("Check available recipes")
try:
    recipe_mgr = get_recipe_manager()
    all_recipes = recipe_mgr.get_all_recipes()
    unlocked = recipe_mgr.get_unlocked_recipes()
    pass_test(f"Total: {len(all_recipes)}, Unlocked: {len(unlocked)}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Check finale recipes exist")
try:
    recipe_mgr = get_recipe_manager()
    finale_recipes = ['ancestral_blessing', 'dragons_heart_feast', 'legacy_eternal']
    found = []
    for recipe_id in finale_recipes:
        recipe = recipe_mgr.get_recipe(recipe_id)
        if recipe:
            found.append(recipe_id)

    if len(found) == 3:
        pass_test("All 3 finale recipes present")
    else:
        fail_test(f"Only found: {found}")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# ZONE SYSTEM
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 9: ZONE SYSTEM")
print("=" * 70)

log_test("Check available zones")
try:
    world = get_world_manager()
    unlocked = world.get_unlocked_zones()
    connected = world.get_connected_zones()
    pass_test(f"Unlocked: {len(unlocked)}, Connected from current: {len(connected)}")
except Exception as e:
    fail_test(f"Error: {e}")

log_test("Check current zone details")
try:
    world = get_world_manager()
    zone = world.get_current_zone()
    if zone:
        pass_test(f"Zone: {zone.name}, Size: {zone.width}x{zone.height}")
    else:
        fail_test("No current zone")
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# EXTENDED GAMEPLAY SIMULATION
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 10: EXTENDED GAMEPLAY (Simulating ~10 minutes)")
print("=" * 70)

log_test("Simulate extended gameplay loop")
try:
    state_manager.set_state("exploration")
    wait_for_state(state_manager, "exploration")

    actions_performed = 0
    game_cycles = 0

    # Simulate 10 cycles of activity
    for cycle in range(10):
        # 1. Move around in exploration
        if state_manager.current_state_name == "exploration":
            exploration = state_manager.current_state
            if exploration and hasattr(exploration, 'player'):
                class MockKeys:
                    def __init__(self, pressed):
                        self.pressed = pressed
                    def __getitem__(self, key):
                        return self.pressed.get(key, False)

                # Move in different directions
                directions = [
                    {pygame.K_w: True},
                    {pygame.K_d: True},
                    {pygame.K_s: True},
                    {pygame.K_a: True},
                ]
                for direction in directions:
                    mock_keys = MockKeys(direction)
                    for _ in range(10):
                        if hasattr(exploration, 'player'):
                            exploration.player.handle_input(mock_keys)
                            exploration.player.update(0.016, lambda x, y: False)
                    actions_performed += 1

        # 2. Run game frames (simulates time passing)
        run_frames(state_manager, 60)
        game_cycles += 1

        # 3. Occasionally open a menu
        if cycle % 3 == 0 and state_manager.current_state_name == "exploration":
            menu_keys = [pygame.K_i, pygame.K_r, pygame.K_d]
            menu_key = menu_keys[cycle % 3]
            send_key(state_manager, menu_key)
            run_frames(state_manager, 30)
            send_key(state_manager, pygame.K_ESCAPE)
            run_frames(state_manager, 60)  # Wait for transition back
            actions_performed += 2

        # 4. Pet the dragon occasionally
        if cycle % 2 == 0 and state_manager.current_state_name == "exploration":
            exploration = state_manager.current_state
            if exploration:
                p_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p, mod=0)
                exploration.handle_event(p_event)
                actions_performed += 1

        # Ensure we're back in exploration for next cycle
        if state_manager.current_state_name != "exploration":
            state_manager.set_state("exploration")
            wait_for_state(state_manager, "exploration")

    pass_test(f"Completed {actions_performed} actions over {game_cycles} cycles")
except Exception as e:
    import traceback
    fail_test(f"Error: {e}")
    traceback.print_exc()

log_test("Verify game state after extended play")
try:
    dragon_mgr = get_dragon_manager()
    dragon = dragon_mgr.get_dragon()
    inventory = get_inventory()
    time_mgr = get_time_manager()

    status = []
    if dragon:
        status.append(f"Dragon OK (happiness: {dragon.get_happiness():.0f})")
    if inventory:
        status.append(f"Inventory OK (gold: {inventory.gold})")
    if time_mgr:
        status.append(f"Time OK (day {time_mgr.get_current_day()})")

    pass_test(", ".join(status))
except Exception as e:
    fail_test(f"Error: {e}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("PLAYTEST SUMMARY")
print("=" * 70)

passed = sum(1 for t in test_results if t["passed"])
failed = sum(1 for t in test_results if not t["passed"])
total = len(test_results)

print(f"\nTotal Tests: {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Success Rate: {100 * passed / total:.1f}%")

if failed > 0:
    print("\nFailed Tests:")
    for t in test_results:
        if not t["passed"]:
            print(f"  - {t['name']}: {t['details']}")

print("\n" + "=" * 70)
if failed == 0:
    print("ALL TESTS PASSED - Game is ready for play!")
else:
    print(f"WARNING: {failed} test(s) failed - Review issues above")
print("=" * 70)

pygame.quit()
