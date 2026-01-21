#!/usr/bin/env python3
"""
Dragon Haven Cafe - Automated Demo for Video Recording
This script runs a 10-minute automated demo showcasing all core gameplay features.

Usage:
1. Run this script
2. It will launch the game and automate gameplay
3. Record your screen while watching
"""

import subprocess
import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import pyautogui
except ImportError:
    print("Installing pyautogui...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyautogui'])
    import pyautogui

# Safety settings
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Small pause between actions

# Game window dimensions (from constants.py)
GAME_WIDTH = 1280
GAME_HEIGHT = 720

def wait(seconds):
    """Wait with countdown display."""
    print(f"  Waiting {seconds}s...", end='', flush=True)
    time.sleep(seconds)
    print(" done")

def press_key(key, times=1, delay=0.3):
    """Press a key multiple times."""
    for _ in range(times):
        pyautogui.press(key)
        time.sleep(delay)

def type_text(text, interval=0.1):
    """Type text character by character."""
    pyautogui.typewrite(text, interval=interval)

def hold_key(key, duration):
    """Hold a key for a duration."""
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def move_character(direction, duration):
    """Move character in a direction."""
    key_map = {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd'}
    key = key_map.get(direction, direction)
    hold_key(key, duration)

def demo_section(name):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"DEMO: {name}")
    print(f"{'='*60}")

def main():
    print("="*60)
    print("DRAGON HAVEN CAFE - 10 MINUTE DEMO RECORDING")
    print("="*60)
    print("\nThis will automate gameplay for video recording.")
    print("Move mouse to top-left corner to abort at any time.")
    print("\nStarting in 5 seconds - switch to watch the game!")
    print("="*60)

    # Countdown
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    # Launch the game
    demo_section("LAUNCHING GAME")
    game_dir = os.path.dirname(os.path.abspath(__file__))
    game_process = subprocess.Popen(
        [sys.executable, 'src/main.py'],
        cwd=game_dir
    )
    print("Game launched, waiting for window...")
    wait(3)

    try:
        # ================================================================
        # MAIN MENU (30 seconds)
        # ================================================================
        demo_section("MAIN MENU")
        wait(2)  # Let menu render

        # Navigate menu to show options
        print("  Showing menu options...")
        press_key('down', 3, 0.5)  # Move through menu items
        press_key('up', 3, 0.5)
        wait(1)

        # Start new game
        print("  Starting new game...")
        press_key('return')  # Select "New Game"
        wait(2)

        # ================================================================
        # INTRO/PROLOGUE (60 seconds)
        # ================================================================
        demo_section("INTRO & PROLOGUE")
        print("  Watching intro dialogue...")

        # Progress through intro dialogue
        for i in range(15):
            wait(2)
            press_key('space')  # Advance dialogue
            print(f"    Dialogue {i+1}/15")

        # ================================================================
        # DRAGON NAMING (30 seconds)
        # ================================================================
        demo_section("DRAGON NAMING")
        wait(2)

        # Check if we're at naming screen and type a name
        print("  Naming the dragon...")
        wait(1)
        # Type dragon name
        pyautogui.typewrite('Ember', interval=0.2)
        wait(1)
        press_key('return')
        wait(2)

        # ================================================================
        # EXPLORATION MODE (120 seconds)
        # ================================================================
        demo_section("EXPLORATION MODE")
        print("  Exploring Cafe Grounds...")

        # Move around the starting zone
        move_character('right', 1.5)
        move_character('up', 1.0)
        move_character('left', 1.0)
        move_character('down', 0.5)
        wait(1)

        # Interact with something
        print("  Interacting with environment...")
        press_key('e')  # Interact
        wait(2)
        press_key('space')  # Dismiss any dialogue
        wait(1)

        # Continue exploring
        print("  Gathering ingredients...")
        move_character('right', 2.0)
        press_key('e')  # Gather
        wait(1)
        move_character('up', 1.5)
        press_key('e')  # Gather
        wait(1)
        move_character('left', 1.0)
        press_key('e')  # Gather
        wait(1)

        # ================================================================
        # INVENTORY SCREEN (30 seconds)
        # ================================================================
        demo_section("INVENTORY")
        print("  Opening inventory...")
        press_key('i')  # Open inventory
        wait(2)

        # Navigate inventory
        press_key('down', 3, 0.4)
        press_key('up', 2, 0.4)
        wait(2)

        press_key('escape')  # Close inventory
        wait(1)

        # ================================================================
        # RECIPE BOOK (30 seconds)
        # ================================================================
        demo_section("RECIPE BOOK")
        print("  Opening recipe book...")
        press_key('r')  # Open recipe book
        wait(2)

        # Browse recipes
        press_key('down', 4, 0.5)
        press_key('up', 2, 0.5)
        press_key('right', 2, 0.5)  # Switch categories
        press_key('left', 1, 0.5)
        wait(2)

        press_key('escape')  # Close
        wait(1)

        # ================================================================
        # DRAGON STATUS (30 seconds)
        # ================================================================
        demo_section("DRAGON STATUS")
        print("  Opening dragon status...")
        press_key('d')  # Open dragon status (or appropriate key)
        wait(3)

        # Look at stats
        press_key('down', 2, 0.5)
        press_key('up', 2, 0.5)
        wait(2)

        press_key('escape')  # Close
        wait(1)

        # ================================================================
        # CAFE MODE (180 seconds)
        # ================================================================
        demo_section("CAFE SERVICE")
        print("  Entering cafe mode...")
        press_key('tab')  # Switch to cafe mode (or walk to cafe)
        wait(2)

        # If there's a menu, navigate it
        press_key('return')  # Start service
        wait(2)

        print("  Serving customers...")
        # Simulate cafe service - select orders and cook
        for customer in range(3):
            print(f"    Customer {customer + 1}/3")
            wait(2)

            # Select customer/order
            press_key('down', 1, 0.3)
            press_key('return')  # Take order
            wait(1)

            # Cooking minigame simulation
            print("      Cooking...")
            press_key('return')  # Start cooking
            wait(1)

            # Hit timing beats (rhythm game)
            for beat in range(8):
                wait(0.4)
                press_key('space')  # Hit beat

            wait(2)
            press_key('space')  # Finish/serve
            wait(1)

        print("  Service complete!")
        wait(2)

        # ================================================================
        # MORE EXPLORATION - MEADOW (60 seconds)
        # ================================================================
        demo_section("EXPLORING MEADOW FIELDS")
        press_key('escape')  # Exit cafe if needed
        wait(1)

        print("  Traveling to Meadow Fields...")
        # Move to zone transition
        move_character('right', 2.0)
        move_character('up', 1.5)
        press_key('e')  # Enter zone transition
        wait(2)
        press_key('return')  # Confirm
        wait(3)

        print("  Exploring meadow...")
        move_character('right', 1.5)
        move_character('down', 1.0)
        press_key('e')  # Gather
        wait(1)
        move_character('left', 2.0)
        press_key('e')  # Gather
        wait(1)

        # ================================================================
        # DRAGON ABILITIES (30 seconds)
        # ================================================================
        demo_section("DRAGON ABILITIES")
        print("  Using dragon abilities...")

        # Try abilities
        press_key('1')  # Ability 1
        wait(1)
        press_key('e')  # Use on target
        wait(2)

        press_key('2')  # Ability 2
        wait(1)
        press_key('e')  # Use
        wait(2)

        # ================================================================
        # STORY EVENT (60 seconds)
        # ================================================================
        demo_section("STORY EVENT")
        print("  Triggering story event...")

        # Move to trigger event
        move_character('up', 1.5)
        move_character('right', 1.0)
        press_key('e')  # Interact
        wait(2)

        # Progress through dialogue with choices
        print("  Story dialogue...")
        for i in range(8):
            wait(2)
            press_key('space')  # Advance
            print(f"    Dialogue {i+1}/8")

        # Make a choice
        print("  Making dialogue choice...")
        press_key('down')  # Select choice
        wait(0.5)
        press_key('return')  # Confirm choice
        wait(2)
        press_key('space')  # Continue
        wait(2)

        # ================================================================
        # SAVE GAME (30 seconds)
        # ================================================================
        demo_section("SAVE GAME")
        print("  Opening pause menu...")
        press_key('escape')
        wait(1)

        print("  Navigating to save...")
        press_key('down', 2, 0.4)  # Navigate to save option
        press_key('return')  # Select save
        wait(2)

        # Select save slot
        press_key('return')  # Save to slot 1
        wait(2)
        print("  Game saved!")

        press_key('escape')  # Close menu
        wait(1)

        # ================================================================
        # FINAL EXPLORATION (remaining time)
        # ================================================================
        demo_section("FINAL SHOWCASE")
        print("  Final exploration showcase...")

        # Quick tour of features
        for _ in range(3):
            move_character('right', 1.0)
            move_character('up', 0.8)
            move_character('left', 1.0)
            move_character('down', 0.8)

        wait(2)

        # Open various menus one more time
        print("  Quick menu showcase...")
        press_key('i')  # Inventory
        wait(2)
        press_key('escape')

        press_key('r')  # Recipes
        wait(2)
        press_key('escape')

        # ================================================================
        # END DEMO
        # ================================================================
        demo_section("DEMO COMPLETE")
        print("\n" + "="*60)
        print("10-MINUTE DEMO RECORDING COMPLETE!")
        print("="*60)
        print("\nYou can stop recording now.")
        print("Press ESC in the game to access the menu.")

        # Keep game running for a bit
        wait(10)

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nDemo error: {e}")
    finally:
        print("\nDemo script finished.")
        print("Close the game window when ready.")


if __name__ == '__main__':
    main()
