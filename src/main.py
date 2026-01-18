"""
Dragon Haven Cafe - Entry Point
A dragon-raising cafe management simulation game.
"""

from game import Game
from state_manager import StateManager
from states.test_state import TestState


def main():
    """Main entry point for Dragon Haven Cafe."""
    # Create the game
    game = Game()

    # Create and register state manager
    state_manager = StateManager()
    game.register_state_manager(state_manager)

    # Register states
    # TODO: Replace test state with real game states as they're implemented
    game.register_state("test", TestState(game))

    # Set initial state
    game.set_initial_state("test")

    # Run the game loop
    game.run()


if __name__ == "__main__":
    main()
