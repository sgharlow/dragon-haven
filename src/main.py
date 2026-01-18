"""
Dragon Haven Cafe - Entry Point
A dragon-raising cafe management simulation game.
"""

from game import Game
from state_manager import StateManager
from states.test_state import TestState
from states.main_menu_state import MainMenuState


def main():
    """Main entry point for Dragon Haven Cafe."""
    # Create the game
    game = Game()

    # Create and register state manager
    state_manager = StateManager()
    game.register_state_manager(state_manager)

    # Register states
    game.register_state("main_menu", MainMenuState(game))
    game.register_state("test", TestState(game))
    game.register_state("gameplay", TestState(game))  # Placeholder until gameplay state exists
    game.register_state("settings", TestState(game))  # Placeholder until settings state exists

    # Set initial state to main menu
    game.set_initial_state("main_menu")

    # Run the game loop
    game.run()


if __name__ == "__main__":
    main()
