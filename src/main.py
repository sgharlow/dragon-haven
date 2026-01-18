"""
Dragon Haven Cafe - Entry Point
A dragon-raising cafe management simulation game.
"""

from game import Game


def main():
    """Main entry point for Dragon Haven Cafe."""
    # Create and run the game
    game = Game()

    # TODO: Register state manager and states here when they're implemented
    # from state_manager import StateManager
    # from states.main_menu_state import MainMenuState
    #
    # state_manager = StateManager()
    # game.register_state_manager(state_manager)
    # game.register_state("menu", MainMenuState(game))
    # game.set_initial_state("menu")

    # Run the game loop
    game.run()


if __name__ == "__main__":
    main()
