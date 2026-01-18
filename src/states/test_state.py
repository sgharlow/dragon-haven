"""
Test state to verify the state machine system works.
This is a temporary state for testing - will be replaced by real screens.
"""

import pygame
from states.base_state import BaseScreen
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, UI_BG, UI_TEXT, UI_TEXT_DIM


class TestState(BaseScreen):
    """
    A simple test state to verify the state machine works.

    Displays a message and responds to key presses.
    """

    def __init__(self, game):
        """Initialize the test state."""
        super().__init__(game)
        self.title = "State Machine Test"
        self.background_color = UI_BG
        self.message = "Press SPACE to transition, ESC to quit"
        self.counter = 0

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.request_quit()
            elif event.key == pygame.K_SPACE:
                # Transition to self (with fade) to test transitions
                self.counter += 1
                self.fade_to_state('test')

    def update(self, dt):
        """Update state logic."""
        super().update(dt)
        return True

    def draw(self, screen):
        """Draw the test state."""
        # Draw base (background, title)
        super().draw(screen)

        # Draw message
        msg_surface = self.body_font.render(self.message, True, UI_TEXT_DIM)
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(msg_surface, msg_rect)

        # Draw counter
        counter_text = f"Transitions: {self.counter}"
        counter_surface = self.body_font.render(counter_text, True, UI_TEXT)
        counter_rect = counter_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(counter_surface, counter_rect)

        # Draw fade overlay last
        self.draw_fade_overlay(screen)
