"""
Dragon Naming State for Dragon Haven Cafe.
Modal popup for naming the dragon during hatching or from dragon status.
"""

import pygame
from typing import Optional
from states.base_state import BaseState
from systems.dragon_manager import get_dragon_manager
from entities.dragon import Dragon
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM, BLACK,
    DRAGON_NAME_MAX_LENGTH, DRAGON_NAME_DEFAULT,
)


class DragonNamingState(BaseState):
    """
    Modal popup state for naming the dragon.

    Features:
    - Text input for dragon name
    - Validation feedback
    - Confirms name on Enter
    - Cancels with Escape (uses default name)
    """

    def __init__(self, game):
        """Initialize the naming state."""
        super().__init__(game)

        # Input state
        self._name_input = ""
        self._cursor_visible = True
        self._cursor_timer = 0.0

        # Error message
        self._error_message = ""

        # Previous state to return to
        self._previous_state: Optional[str] = None

        # Fonts (initialized in enter)
        self._title_font = None
        self._input_font = None
        self._hint_font = None
        self._error_font = None

        # Animation
        self._fade_alpha = 0

    def enter(self, previous_state=None):
        """Enter the naming state."""
        super().enter(previous_state)
        self._previous_state = previous_state

        # Initialize fonts
        self._title_font = pygame.font.Font(None, 48)
        self._input_font = pygame.font.Font(None, 36)
        self._hint_font = pygame.font.Font(None, 24)
        self._error_font = pygame.font.Font(None, 22)

        # Get current dragon name or default
        dragon_mgr = get_dragon_manager()
        dragon = dragon_mgr.get_dragon()
        if dragon:
            self._name_input = dragon.get_name()
            if self._name_input == DRAGON_NAME_DEFAULT:
                self._name_input = ""  # Start empty for new naming
        else:
            self._name_input = ""

        self._error_message = ""
        self._fade_alpha = 0

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._confirm_name()
            elif event.key == pygame.K_ESCAPE:
                self._cancel_naming()
            elif event.key == pygame.K_BACKSPACE:
                self._name_input = self._name_input[:-1]
                self._error_message = ""
            elif event.unicode.isprintable():
                if len(self._name_input) < DRAGON_NAME_MAX_LENGTH:
                    self._name_input += event.unicode
                    self._error_message = ""

    def _confirm_name(self):
        """Confirm the entered name."""
        dragon_mgr = get_dragon_manager()

        # Validate name
        is_valid, result = Dragon.validate_name(self._name_input)

        if not is_valid:
            self._error_message = result
            return

        # Set the name
        if dragon_mgr.set_dragon_name(result):
            dragon_mgr.complete_naming()
            self._return_to_previous()
        else:
            self._error_message = "Failed to set name"

    def _cancel_naming(self):
        """Cancel naming and use default."""
        dragon_mgr = get_dragon_manager()

        # If name is empty, use default
        if not self._name_input.strip():
            dragon_mgr.set_dragon_name(DRAGON_NAME_DEFAULT)

        dragon_mgr.cancel_naming()
        self._return_to_previous()

    def _return_to_previous(self):
        """Return to the previous state."""
        if self._previous_state:
            self.transition_to(self._previous_state)
        else:
            self.transition_to('gameplay')

    def update(self, dt):
        """Update animation."""
        # Cursor blink
        self._cursor_timer += dt
        if self._cursor_timer >= 0.5:
            self._cursor_timer = 0.0
            self._cursor_visible = not self._cursor_visible

        # Fade in
        if self._fade_alpha < 200:
            self._fade_alpha = min(200, self._fade_alpha + 600 * dt)

        return True

    def draw(self, screen):
        """Draw the naming popup."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(self._fade_alpha)))
        screen.blit(overlay, (0, 0))

        # Popup box
        popup_width = 500
        popup_height = 250
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2

        # Background
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(screen, UI_PANEL, popup_rect, border_radius=12)
        pygame.draw.rect(screen, UI_BORDER, popup_rect, 3, border_radius=12)

        # Title
        title_text = "Name Your Dragon"
        title_surface = self._title_font.render(title_text, True, CAFE_CREAM)
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=popup_y + 30)
        screen.blit(title_surface, title_rect)

        # Input box
        input_width = 350
        input_height = 45
        input_x = (SCREEN_WIDTH - input_width) // 2
        input_y = popup_y + 90

        input_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        pygame.draw.rect(screen, (40, 35, 50), input_rect, border_radius=6)
        pygame.draw.rect(screen, CAFE_WARM, input_rect, 2, border_radius=6)

        # Input text with cursor
        display_text = self._name_input
        if self._cursor_visible:
            display_text += "|"

        if display_text:
            text_surface = self._input_font.render(display_text, True, CAFE_CREAM)
            text_rect = text_surface.get_rect(centery=input_y + input_height // 2, x=input_x + 15)
            screen.blit(text_surface, text_rect)
        else:
            # Placeholder
            placeholder = self._input_font.render("Enter a name...", True, UI_TEXT_DIM)
            placeholder_rect = placeholder.get_rect(centery=input_y + input_height // 2, x=input_x + 15)
            screen.blit(placeholder, placeholder_rect)

        # Error message
        if self._error_message:
            error_surface = self._error_font.render(self._error_message, True, (220, 100, 100))
            error_rect = error_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=input_y + input_height + 10)
            screen.blit(error_surface, error_rect)

        # Character count
        char_count = f"{len(self._name_input)}/{DRAGON_NAME_MAX_LENGTH}"
        count_color = UI_TEXT_DIM if len(self._name_input) < DRAGON_NAME_MAX_LENGTH else (220, 180, 100)
        count_surface = self._hint_font.render(char_count, True, count_color)
        count_rect = count_surface.get_rect(right=input_x + input_width - 10, y=input_y + input_height + 10)
        screen.blit(count_surface, count_rect)

        # Hints
        hints_y = popup_y + popup_height - 55

        confirm_hint = "[Enter] Confirm"
        confirm_surface = self._hint_font.render(confirm_hint, True, (100, 180, 100))
        confirm_rect = confirm_surface.get_rect(centerx=SCREEN_WIDTH // 2 - 80, y=hints_y)
        screen.blit(confirm_surface, confirm_rect)

        cancel_hint = "[Esc] Skip"
        cancel_surface = self._hint_font.render(cancel_hint, True, UI_TEXT_DIM)
        cancel_rect = cancel_surface.get_rect(centerx=SCREEN_WIDTH // 2 + 80, y=hints_y)
        screen.blit(cancel_surface, cancel_rect)
