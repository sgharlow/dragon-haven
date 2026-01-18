"""
Base state classes for Dragon Haven Cafe.
Provides the foundation for all game screens and states.
"""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BG, UI_TEXT


class BaseState:
    """
    Base class for all game states.

    States handle a specific mode of the game (menu, gameplay, etc.).
    Override the lifecycle methods to implement state-specific behavior.
    """

    def __init__(self, game):
        """
        Initialize the state.

        Args:
            game: Reference to the main Game instance
        """
        self.game = game
        self.next_state = None  # Set to transition to another state
        self.done = False  # Set True to signal state completion

    def enter(self, previous_state=None):
        """
        Called when entering this state.

        Args:
            previous_state: Name of the state we came from (or None)
        """
        pass

    def exit(self):
        """Called when leaving this state."""
        pass

    def handle_event(self, event):
        """
        Handle a pygame event.

        Args:
            event: pygame event to process
        """
        pass

    def update(self, dt):
        """
        Update state logic.

        Args:
            dt: Delta time in seconds

        Returns:
            True to continue, False to quit the game
        """
        return True

    def draw(self, screen):
        """
        Draw the state.

        Args:
            screen: pygame surface to draw on
        """
        pass

    def transition_to(self, state_name):
        """
        Request transition to another state.

        Args:
            state_name: Name of the state to transition to
        """
        self.next_state = state_name

    def request_quit(self):
        """Request the game to quit."""
        self.game.quit()


class BaseScreen(BaseState):
    """
    Extended base class for screen-type states.

    Provides common functionality for game screens like
    background drawing, title display, and fade transitions.
    """

    def __init__(self, game):
        """Initialize the screen."""
        super().__init__(game)

        # Screen properties
        self.background_color = UI_BG
        self.title = ""
        self.title_font = None
        self.body_font = None

        # Fade transition
        self.fade_alpha = 0
        self.fade_target = 0
        self.fade_speed = 500  # Alpha units per second
        self.fading_in = False
        self.fading_out = False
        self.fade_callback = None

    def enter(self, previous_state=None):
        """Initialize fonts and start fade in."""
        super().enter(previous_state)

        # Initialize fonts if not already done
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 48)
        if self.body_font is None:
            self.body_font = pygame.font.Font(None, 32)

        # Start fade in
        self.start_fade_in()

    def start_fade_in(self):
        """Start fading in from black."""
        self.fade_alpha = 255
        self.fade_target = 0
        self.fading_in = True
        self.fading_out = False

    def start_fade_out(self, callback=None):
        """
        Start fading out to black.

        Args:
            callback: Function to call when fade completes
        """
        self.fade_alpha = 0
        self.fade_target = 255
        self.fading_out = True
        self.fading_in = False
        self.fade_callback = callback

    def fade_to_state(self, state_name):
        """
        Fade out then transition to another state.

        Args:
            state_name: Name of state to transition to
        """
        def on_fade_complete():
            self.transition_to(state_name)
        self.start_fade_out(on_fade_complete)

    def update(self, dt):
        """Update fade effect."""
        # Update fade
        if self.fading_in or self.fading_out:
            if self.fade_alpha < self.fade_target:
                self.fade_alpha = min(self.fade_target,
                                     self.fade_alpha + self.fade_speed * dt)
            elif self.fade_alpha > self.fade_target:
                self.fade_alpha = max(self.fade_target,
                                     self.fade_alpha - self.fade_speed * dt)

            # Check if fade complete
            if abs(self.fade_alpha - self.fade_target) < 1:
                self.fade_alpha = self.fade_target
                if self.fading_out and self.fade_callback:
                    self.fade_callback()
                    self.fade_callback = None
                self.fading_in = False
                self.fading_out = False

        return True

    def draw(self, screen):
        """Draw background and fade overlay."""
        # Draw background
        screen.fill(self.background_color)

        # Draw title if set
        if self.title:
            title_surface = self.title_font.render(self.title, True, UI_TEXT)
            title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
            screen.blit(title_surface, title_rect)

        # Subclasses should call super().draw(screen) then draw their content

    def draw_fade_overlay(self, screen):
        """
        Draw the fade overlay. Call this LAST in draw().

        Args:
            screen: pygame surface
        """
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.fade_alpha))
            screen.blit(fade_surface, (0, 0))
