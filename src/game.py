"""
Main Game class for Dragon Haven Cafe.
Handles the game loop, pygame initialization, and state management.
"""

import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BLACK


class Game:
    """
    Main game class that runs the game loop and manages core systems.

    Attributes:
        screen: The main pygame display surface
        clock: pygame Clock for framerate control
        state_manager: StateManager for handling game states (set later)
        running: Whether the game loop should continue
        dt: Delta time in seconds since last frame
    """

    def __init__(self):
        """Initialize pygame and game systems."""
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        # Create clock for FPS control
        self.clock = pygame.time.Clock()

        # Game state
        self.running = True
        self.dt = 0.0  # Delta time in seconds

        # State manager (will be set by register_state_manager or use placeholder)
        self.state_manager = None

        # Placeholder font for when no state manager is set
        self._placeholder_font = pygame.font.Font(None, 36)

    def register_state_manager(self, state_manager):
        """
        Register the state manager.

        Args:
            state_manager: StateManager instance to use
        """
        self.state_manager = state_manager

    def register_state(self, name, state):
        """
        Register a game state with the state manager.

        Args:
            name: String identifier for the state
            state: BaseState instance
        """
        if self.state_manager:
            self.state_manager.register(name, state)

    def set_initial_state(self, name):
        """
        Set the initial state to run.

        Args:
            name: Name of the state to start with
        """
        if self.state_manager:
            self.state_manager.set_state(name)

    def run(self):
        """
        Run the main game loop.

        Handles events, updates, and rendering at the target FPS.
        Uses delta time for frame-independent movement.
        """
        while self.running:
            # Calculate delta time (in seconds)
            self.dt = self.clock.tick(FPS) / 1000.0

            # Cap delta time to prevent spiral of death
            # (e.g., if game freezes, don't try to simulate huge time jumps)
            if self.dt > 0.1:
                self.dt = 0.1

            # Handle events
            self._handle_events()

            # Update
            self._update()

            # Draw
            self._draw()

        # Cleanup
        self._quit()

    def _handle_events(self):
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.state_manager is None:
                    # Only allow ESC to quit when no state manager (placeholder mode)
                    self.running = False

            # Pass event to state manager if available
            if self.state_manager:
                self.state_manager.handle_event(event)

    def _update(self):
        """Update game logic."""
        if self.state_manager:
            # Update state manager and check if it requests quit
            result = self.state_manager.update(self.dt)
            if result is False:
                self.running = False

    def _draw(self):
        """Render the current frame."""
        # Clear screen
        self.screen.fill(BLACK)

        # Draw current state
        if self.state_manager:
            self.state_manager.draw(self.screen)
        else:
            # Draw placeholder when no state manager
            self._draw_placeholder()

        # Update display
        pygame.display.flip()

    def _draw_placeholder(self):
        """Draw placeholder content when no state manager is set."""
        text = self._placeholder_font.render(
            "Dragon Haven Cafe - Game Engine Ready",
            True,
            (255, 255, 255)
        )
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(text, rect)

        hint_text = self._placeholder_font.render(
            "Register states with game.register_state_manager()",
            True,
            (150, 150, 150)
        )
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(hint_text, hint_rect)

        esc_text = self._placeholder_font.render(
            "Press ESC to exit",
            True,
            (100, 100, 100)
        )
        esc_rect = esc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(esc_text, esc_rect)

    def _quit(self):
        """Clean up and exit."""
        pygame.quit()
        sys.exit()

    def quit(self):
        """Request the game to quit."""
        self.running = False

    @property
    def delta_time(self):
        """Get the current delta time in seconds."""
        return self.dt
