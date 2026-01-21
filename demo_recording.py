#!/usr/bin/env python3
"""
Dragon Haven Cafe - Automated Demo for Video Recording
Uses keyboard library for better key holding support.
"""

import subprocess
import time
import sys
import os

# Install and import required packages
try:
    import keyboard
    import pygetwindow as gw
except ImportError:
    print("Installing required packages...", flush=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'keyboard', 'pygetwindow'])
    import keyboard
    import pygetwindow as gw

game_window = None

def log(msg):
    """Print with immediate flush."""
    print(msg, flush=True)

def focus_game():
    """Focus the game window."""
    global game_window
    try:
        windows = gw.getWindowsWithTitle('Dragon Haven')
        if not windows:
            windows = gw.getWindowsWithTitle('pygame')
        if windows:
            game_window = windows[0]
            try:
                game_window.activate()
            except Exception:
                pass
            time.sleep(0.1)
            return True
    except Exception as e:
        log(f"  Focus error: {e}")
    return False

def wait(seconds):
    """Wait for specified seconds."""
    time.sleep(seconds)

def press_key(key, times=1, delay=0.2):
    """Press a key multiple times."""
    for _ in range(times):
        focus_game()
        keyboard.press_and_release(key)
        log(f"    [KEY] {key}")
        time.sleep(delay)

def type_text(text, interval=0.15):
    """Type text."""
    focus_game()
    log(f"    [TYPE] {text}")
    for char in text.lower():
        keyboard.press_and_release(char)
        time.sleep(interval)

def move_character(direction, duration):
    """Move character using arrow keys (avoids WASD menu conflicts)."""
    # Use arrow keys instead of WASD to avoid menu key conflicts
    key_map = {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right'}
    key = key_map.get(direction, direction)

    log(f"    [MOVE] {direction} for {duration}s")
    focus_game()

    # Hold key down for the duration
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)
    time.sleep(0.1)

def demo_section(name):
    """Print section header."""
    log(f"\n{'='*60}")
    log(f"DEMO: {name}")
    log(f"{'='*60}")
    focus_game()

def main():
    log("="*60)
    log("DRAGON HAVEN CAFE - 10 MINUTE DEMO RECORDING")
    log("="*60)
    log("\nUsing keyboard library for better key holding.")
    log("NOTE: This requires admin privileges on Windows.")
    log("\nStarting in 5 seconds!")
    log("="*60)

    # Countdown
    for i in range(5, 0, -1):
        log(f"  {i}...")
        time.sleep(1)

    # Launch the game
    demo_section("LAUNCHING GAME")
    game_dir = os.path.dirname(os.path.abspath(__file__))
    game_process = subprocess.Popen(
        [sys.executable, 'src/main.py'],
        cwd=game_dir
    )
    log("Game launched, waiting for window...")
    wait(5)

    # Focus game
    log("Focusing game window...")
    for attempt in range(10):
        if focus_game():
            log(f"  Focused on attempt {attempt + 1}!")
            break
        time.sleep(0.5)

    wait(2)

    try:
        # ================================================================
        # MAIN MENU
        # ================================================================
        demo_section("MAIN MENU")
        log("  At main menu")
        wait(2)

        log("  Navigating menu...")
        press_key('down', 2, 0.5)
        press_key('up', 2, 0.5)
        wait(1)

        log("  Starting new game...")
        press_key('enter')
        wait(3)

        # ================================================================
        # DRAGON NAMING
        # ================================================================
        demo_section("DRAGON NAMING")
        log("  Naming screen...")
        wait(2)

        log("  Typing name: Ember")
        type_text('Ember', 0.2)
        wait(1)

        log("  Confirming...")
        press_key('enter')
        wait(2)

        # ================================================================
        # EXPLORATION MODE
        # ================================================================
        demo_section("EXPLORATION")
        log("  In exploration mode")
        wait(2)

        log("  Moving around...")
        move_character('right', 1.5)
        move_character('up', 1.0)
        move_character('left', 0.8)
        move_character('down', 0.5)
        wait(0.5)

        log("  Interacting...")
        press_key('e')
        wait(1)
        press_key('e')
        wait(1)

        move_character('right', 1.0)
        press_key('e')
        wait(1)

        # ================================================================
        # INVENTORY
        # ================================================================
        demo_section("INVENTORY")
        log("  Opening inventory (I)...")
        press_key('i')
        wait(3)

        press_key('down', 3, 0.3)
        press_key('up', 2, 0.3)
        wait(2)

        log("  Closing...")
        press_key('escape')
        wait(1)

        # ================================================================
        # RECIPE BOOK
        # ================================================================
        demo_section("RECIPE BOOK")
        log("  Opening recipes (R)...")
        press_key('r')
        wait(3)

        press_key('down', 4, 0.3)
        press_key('up', 2, 0.3)
        wait(2)

        log("  Closing...")
        press_key('escape')
        wait(1)

        # ================================================================
        # DRAGON STATUS
        # ================================================================
        demo_section("DRAGON STATUS")
        log("  Opening dragon status (D)...")
        press_key('d')
        wait(3)

        press_key('down', 2, 0.4)
        press_key('up', 2, 0.4)
        wait(2)

        log("  Closing...")
        press_key('escape')
        wait(1)

        # ================================================================
        # PET DRAGON
        # ================================================================
        demo_section("PET DRAGON")
        log("  Petting dragon (P)...")
        press_key('p')
        wait(2)
        press_key('p')
        wait(2)

        # ================================================================
        # CAFE MODE
        # ================================================================
        demo_section("CAFE MODE")
        log("  Entering cafe (C)...")
        press_key('c')
        wait(3)

        log("  Starting service...")
        press_key('enter')
        wait(2)

        log("  Serving customers...")
        for customer in range(2):
            log(f"    Customer {customer + 1}/2")
            wait(1)
            press_key('down', 1, 0.3)
            press_key('enter')
            wait(1)

            log("      Cooking...")
            for _ in range(5):
                wait(0.4)
                press_key('space')
            wait(1)
            press_key('space')
            wait(1)

        log("  Exiting cafe...")
        press_key('escape')
        wait(2)

        # ================================================================
        # MORE EXPLORATION
        # ================================================================
        demo_section("MORE EXPLORATION")
        log("  Exploring more...")

        move_character('right', 1.5)
        move_character('up', 1.0)
        press_key('e')
        wait(1)

        move_character('down', 0.8)
        move_character('left', 1.0)
        wait(1)

        # ================================================================
        # FINAL SHOWCASE
        # ================================================================
        demo_section("FINAL SHOWCASE")
        log("  Final showcase...")

        # Movement demo
        for _ in range(2):
            move_character('right', 0.6)
            move_character('up', 0.4)
            move_character('left', 0.6)
            move_character('down', 0.4)

        log("  Quick menu tour...")
        press_key('i')
        wait(2)
        press_key('escape')
        wait(0.5)

        press_key('r')
        wait(2)
        press_key('escape')
        wait(0.5)

        press_key('d')
        wait(2)
        press_key('escape')
        wait(1)

        # ================================================================
        # END DEMO
        # ================================================================
        demo_section("DEMO COMPLETE")
        log("\n" + "="*60)
        log("DEMO RECORDING COMPLETE!")
        log("="*60)
        log("\nYou can stop recording now.")

        wait(10)

    except KeyboardInterrupt:
        log("\n\nDemo interrupted.")
    except Exception as e:
        log(f"\n\nDemo error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        log("\nDemo finished.")
        # Make sure all keys are released
        try:
            keyboard.release('up')
            keyboard.release('down')
            keyboard.release('left')
            keyboard.release('right')
        except:
            pass


if __name__ == '__main__':
    main()
