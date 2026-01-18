"""
Pause Menu State for Dragon Haven Cafe.
An overlay menu that appears during gameplay.
"""

import pygame
from typing import Optional, Callable
from states.base_state import BaseState
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_PANEL, UI_BORDER, UI_HIGHLIGHT,
    UI_TEXT, UI_TEXT_DIM, CAFE_WARM, CAFE_CREAM,
)
from ui.components import Button
from sound_manager import get_sound_manager


class PauseMenuItem:
    """A single menu item in the pause menu."""

    def __init__(self, text: str, action: str, y: int, width: int = 200):
        """
        Initialize a pause menu item.

        Args:
            text: Display text
            action: Action identifier
            y: Y position
            width: Button width
        """
        self.text = text
        self.action = action
        self.x = SCREEN_WIDTH // 2 - width // 2
        self.y = y
        self.width = width
        self.height = 44
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover = False
        self.font = pygame.font.Font(None, 32)

    def update(self, mouse_pos: tuple) -> bool:
        """Update hover state. Returns True if hover state changed to True."""
        was_hover = self.hover
        self.hover = self.rect.collidepoint(mouse_pos)
        return self.hover and not was_hover

    def draw(self, surface: pygame.Surface):
        """Draw the menu item."""
        # Background
        bg_color = UI_HIGHLIGHT if self.hover else UI_PANEL
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 2, border_radius=6)

        # Text
        text_color = CAFE_CREAM if self.hover else UI_TEXT
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class ConfirmDialog:
    """A simple confirmation dialog."""

    def __init__(self, message: str, on_confirm: Callable, on_cancel: Callable):
        """Initialize the confirm dialog."""
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        # Dialog dimensions
        self.width = 350
        self.height = 150
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Buttons
        btn_width = 100
        btn_height = 40
        btn_y = self.y + self.height - btn_height - 20
        self.confirm_btn = Button(
            self.x + 40, btn_y, btn_width, btn_height,
            "Yes", on_click=on_confirm
        )
        self.cancel_btn = Button(
            self.x + self.width - btn_width - 40, btn_y, btn_width, btn_height,
            "No", on_click=on_cancel
        )

        self.font = pygame.font.Font(None, 28)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events."""
        if self.confirm_btn.handle_event(event):
            return True
        if self.cancel_btn.handle_event(event):
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.on_confirm()
                return True
            elif event.key == pygame.K_ESCAPE:
                self.on_cancel()
                return True
        return False

    def draw(self, surface: pygame.Surface):
        """Draw the dialog."""
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        # Dialog background
        pygame.draw.rect(surface, UI_BG, self.rect, border_radius=10)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 3, border_radius=10)

        # Message
        text_surface = self.font.render(self.message, True, UI_TEXT)
        text_rect = text_surface.get_rect(centerx=self.x + self.width // 2, y=self.y + 30)
        surface.blit(text_surface, text_rect)

        # Buttons
        self.confirm_btn.draw(surface)
        self.cancel_btn.draw(surface)


class PauseMenuState(BaseState):
    """
    Pause menu that overlays gameplay.

    Features:
    - Resume game
    - Quick access to Inventory, Recipes, Dragon Status
    - Save game
    - Return to main menu

    This state is transparent and shows the game behind it with a dark overlay.
    """

    def __init__(self, game):
        """Initialize the pause menu."""
        super().__init__(game)

        # Menu items
        self.menu_items: list[PauseMenuItem] = []
        self.selected_index = 0

        # State
        self.previous_state_name: Optional[str] = None
        self.confirm_dialog: Optional[ConfirmDialog] = None

        # Sound
        self.sound = get_sound_manager()

        # Fonts
        self.title_font = None
        self.hint_font = None

    def enter(self, previous_state=None):
        """Initialize menu when entering state."""
        super().enter(previous_state)
        self.previous_state_name = previous_state

        # Initialize fonts
        self.title_font = pygame.font.Font(None, 48)
        self.hint_font = pygame.font.Font(None, 24)

        # Create menu items
        menu_y_start = 220
        menu_spacing = 55
        menu_options = [
            ("Resume", "resume"),
            ("Inventory", "inventory"),
            ("Recipes", "recipes"),
            ("Dragon Status", "dragon"),
            ("Save Game", "save"),
            ("Settings", "settings"),
            ("Main Menu", "main_menu"),
        ]

        self.menu_items = []
        for i, (text, action) in enumerate(menu_options):
            y = menu_y_start + i * menu_spacing
            self.menu_items.append(PauseMenuItem(text, action, y))

        self.selected_index = 0
        self.confirm_dialog = None

    def handle_event(self, event):
        """Handle input events."""
        # Handle confirm dialog if active
        if self.confirm_dialog:
            self.confirm_dialog.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._do_action("resume")
            elif event.key == pygame.K_UP:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._select_current()
            # Shortcuts
            elif event.key == pygame.K_i:
                self._do_action("inventory")
            elif event.key == pygame.K_r:
                self._do_action("recipes")
            elif event.key == pygame.K_d:
                self._do_action("dragon")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for item in self.menu_items:
                    if item.hover:
                        self._do_action(item.action)
                        break

    def _move_selection(self, direction: int):
        """Move menu selection."""
        self.selected_index = (self.selected_index + direction) % len(self.menu_items)
        for i, item in enumerate(self.menu_items):
            item.hover = (i == self.selected_index)
        self.sound.play('ui_hover')

    def _select_current(self):
        """Select current menu item."""
        if 0 <= self.selected_index < len(self.menu_items):
            self._do_action(self.menu_items[self.selected_index].action)

    def _do_action(self, action: str):
        """Execute a menu action."""
        self.sound.play('ui_confirm')

        if action == "resume":
            # Return to gameplay
            if self.previous_state_name:
                self.transition_to(self.previous_state_name)
            else:
                self.transition_to("exploration")

        elif action == "inventory":
            self.transition_to("inventory")

        elif action == "recipes":
            self.transition_to("recipe_book")

        elif action == "dragon":
            self.transition_to("dragon_status")

        elif action == "save":
            self.transition_to("save_load")

        elif action == "settings":
            self.transition_to("settings")

        elif action == "main_menu":
            # Show confirmation dialog
            self.confirm_dialog = ConfirmDialog(
                "Return to main menu?",
                on_confirm=self._confirm_main_menu,
                on_cancel=self._cancel_dialog
            )

    def _confirm_main_menu(self):
        """Confirmed return to main menu."""
        self.confirm_dialog = None
        self.transition_to("main_menu")

    def _cancel_dialog(self):
        """Cancel the dialog."""
        self.confirm_dialog = None

    def update(self, dt):
        """Update the pause menu."""
        # Update menu item hover states
        mouse_pos = pygame.mouse.get_pos()
        for i, item in enumerate(self.menu_items):
            hover_entered = item.update(mouse_pos)
            if hover_entered:
                self.selected_index = i
                self.sound.play('ui_hover', 0.5)

        return True

    def draw(self, screen):
        """Draw the pause menu overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Panel background
        panel_width = 280
        panel_height = 480
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = 100
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        pygame.draw.rect(screen, UI_BG, panel_rect, border_radius=12)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 3, border_radius=12)

        # Title
        title_surface = self.title_font.render("Paused", True, CAFE_CREAM)
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=panel_y + 30)
        screen.blit(title_surface, title_rect)

        # Menu items
        for item in self.menu_items:
            item.draw(screen)

        # Keyboard hints
        hints = "ESC: Resume | I: Inventory | R: Recipes | D: Dragon"
        hint_surface = self.hint_font.render(hints, True, UI_TEXT_DIM)
        hint_rect = hint_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 40)
        screen.blit(hint_surface, hint_rect)

        # Draw confirm dialog if active
        if self.confirm_dialog:
            self.confirm_dialog.draw(screen)
