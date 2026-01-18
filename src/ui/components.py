"""
Reusable UI Components for Dragon Haven Cafe.
Includes sliders, toggles, selectors, and buttons.
"""

import pygame
from typing import Callable, Optional, List, Any
from constants import (
    UI_BG, UI_PANEL, UI_BORDER, UI_HIGHLIGHT,
    UI_TEXT, UI_TEXT_DIM, WHITE, BLACK,
    CAFE_WARM, CAFE_CREAM,
)


class Slider:
    """
    A horizontal slider for numeric values.

    Usage:
        slider = Slider(x, y, 200, 0, 100, 80, on_change=my_callback)
        slider.handle_event(event)
        slider.draw(screen)
    """

    def __init__(self, x: int, y: int, width: int, min_val: float, max_val: float,
                 value: float, label: str = "", on_change: Optional[Callable[[float], None]] = None):
        """
        Initialize the slider.

        Args:
            x, y: Position
            width: Width of the slider track
            min_val: Minimum value
            max_val: Maximum value
            value: Initial value
            label: Label text to display
            on_change: Callback when value changes
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.min_val = min_val
        self.max_val = max_val
        self._value = value
        self.label = label
        self.on_change = on_change

        # Track and handle
        self.track_rect = pygame.Rect(x, y, width, self.height)
        self.handle_width = 16
        self.handle_height = 24

        # State
        self.dragging = False
        self.hover = False

        # Fonts
        self.font = pygame.font.Font(None, 28)

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, val: float):
        old_val = self._value
        self._value = max(self.min_val, min(self.max_val, val))
        if self._value != old_val and self.on_change:
            self.on_change(self._value)

    def _get_handle_x(self) -> int:
        """Get handle x position based on value."""
        ratio = (self._value - self.min_val) / (self.max_val - self.min_val)
        return int(self.x + ratio * (self.width - self.handle_width))

    def _get_handle_rect(self) -> pygame.Rect:
        """Get handle rectangle."""
        handle_x = self._get_handle_x()
        handle_y = self.y - (self.handle_height - self.height) // 2
        return pygame.Rect(handle_x, handle_y, self.handle_width, self.handle_height)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input event. Returns True if event was consumed."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_rect = self._get_handle_rect()
                if handle_rect.collidepoint(event.pos):
                    self.dragging = True
                    return True
                elif self.track_rect.collidepoint(event.pos):
                    # Click on track - jump to position
                    self._set_from_mouse_x(event.pos[0])
                    self.dragging = True
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                return True

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._set_from_mouse_x(event.pos[0])
                return True
            else:
                # Check hover
                handle_rect = self._get_handle_rect()
                self.hover = handle_rect.collidepoint(event.pos) or self.track_rect.collidepoint(event.pos)

        return False

    def _set_from_mouse_x(self, mouse_x: int):
        """Set value based on mouse x position."""
        relative_x = mouse_x - self.x
        ratio = max(0, min(1, relative_x / self.width))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)

    def draw(self, surface: pygame.Surface):
        """Draw the slider."""
        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, UI_TEXT)
            label_rect = label_surface.get_rect(right=self.x - 15, centery=self.y + self.height // 2)
            surface.blit(label_surface, label_rect)

        # Draw track background
        track_color = UI_PANEL if not self.hover else UI_HIGHLIGHT
        pygame.draw.rect(surface, track_color, self.track_rect, border_radius=4)
        pygame.draw.rect(surface, UI_BORDER, self.track_rect, 2, border_radius=4)

        # Draw filled portion
        ratio = (self._value - self.min_val) / (self.max_val - self.min_val)
        fill_width = int(ratio * self.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.x, self.y, fill_width, self.height)
            pygame.draw.rect(surface, CAFE_WARM, fill_rect, border_radius=4)

        # Draw handle
        handle_rect = self._get_handle_rect()
        handle_color = CAFE_CREAM if (self.dragging or self.hover) else UI_TEXT
        pygame.draw.rect(surface, handle_color, handle_rect, border_radius=4)
        pygame.draw.rect(surface, UI_BORDER, handle_rect, 2, border_radius=4)

        # Draw value text
        value_text = f"{int(self._value)}"
        value_surface = self.font.render(value_text, True, UI_TEXT)
        value_rect = value_surface.get_rect(left=self.x + self.width + 15, centery=self.y + self.height // 2)
        surface.blit(value_surface, value_rect)


class Toggle:
    """
    A toggle switch for boolean values.
    """

    def __init__(self, x: int, y: int, value: bool = False, label: str = "",
                 on_change: Optional[Callable[[bool], None]] = None):
        """
        Initialize the toggle.

        Args:
            x, y: Position
            value: Initial state
            label: Label text
            on_change: Callback when toggled
        """
        self.x = x
        self.y = y
        self.width = 50
        self.height = 26
        self._value = value
        self.label = label
        self.on_change = on_change

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.hover = False

        self.font = pygame.font.Font(None, 28)

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, val: bool):
        old_val = self._value
        self._value = val
        if self._value != old_val and self.on_change:
            self.on_change(self._value)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input event."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.value = not self._value
                return True

        elif event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the toggle."""
        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, UI_TEXT)
            label_rect = label_surface.get_rect(right=self.x - 15, centery=self.y + self.height // 2)
            surface.blit(label_surface, label_rect)

        # Draw track
        track_color = CAFE_WARM if self._value else UI_PANEL
        if self.hover:
            track_color = tuple(min(255, c + 30) for c in track_color)
        pygame.draw.rect(surface, track_color, self.rect, border_radius=self.height // 2)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 2, border_radius=self.height // 2)

        # Draw handle
        handle_radius = (self.height - 6) // 2
        handle_x = self.x + self.width - handle_radius - 4 if self._value else self.x + handle_radius + 4
        handle_y = self.y + self.height // 2
        pygame.draw.circle(surface, CAFE_CREAM if self._value else UI_TEXT_DIM,
                          (handle_x, handle_y), handle_radius)

        # Draw status text
        status_text = "ON" if self._value else "OFF"
        status_surface = self.font.render(status_text, True, UI_TEXT_DIM)
        status_rect = status_surface.get_rect(left=self.x + self.width + 15, centery=self.y + self.height // 2)
        surface.blit(status_surface, status_rect)


class Selector:
    """
    A selector for choosing from multiple options.
    """

    def __init__(self, x: int, y: int, width: int, options: List[Any], labels: List[str],
                 selected: int = 0, label: str = "",
                 on_change: Optional[Callable[[Any], None]] = None):
        """
        Initialize the selector.

        Args:
            x, y: Position
            width: Width of selector
            options: List of option values
            labels: Display labels for options
            selected: Index of initially selected option
            label: Label text
            on_change: Callback when selection changes
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = 32
        self.options = options
        self.labels = labels
        self._selected = selected
        self.label = label
        self.on_change = on_change

        self.rect = pygame.Rect(x, y, width, self.height)
        self.hover = False

        # Arrow button rects
        self.arrow_width = 30
        self.left_rect = pygame.Rect(x, y, self.arrow_width, self.height)
        self.right_rect = pygame.Rect(x + width - self.arrow_width, y, self.arrow_width, self.height)

        self.font = pygame.font.Font(None, 28)

    @property
    def selected(self) -> int:
        return self._selected

    @selected.setter
    def selected(self, idx: int):
        old_idx = self._selected
        self._selected = idx % len(self.options)
        if self._selected != old_idx and self.on_change:
            self.on_change(self.options[self._selected])

    @property
    def value(self) -> Any:
        return self.options[self._selected]

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input event."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.left_rect.collidepoint(event.pos):
                    self.selected = (self._selected - 1) % len(self.options)
                    return True
                elif self.right_rect.collidepoint(event.pos):
                    self.selected = (self._selected + 1) % len(self.options)
                    return True

        elif event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the selector."""
        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, UI_TEXT)
            label_rect = label_surface.get_rect(right=self.x - 15, centery=self.y + self.height // 2)
            surface.blit(label_surface, label_rect)

        # Draw background
        bg_color = UI_HIGHLIGHT if self.hover else UI_PANEL
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 2, border_radius=4)

        # Draw left arrow
        arrow_color = CAFE_WARM if self.left_rect.collidepoint(pygame.mouse.get_pos()) else UI_TEXT
        pygame.draw.polygon(surface, arrow_color, [
            (self.x + 20, self.y + self.height // 2),
            (self.x + 10, self.y + self.height // 2 - 8),
            (self.x + 10, self.y + self.height // 2 + 8),
        ])

        # Draw right arrow
        arrow_color = CAFE_WARM if self.right_rect.collidepoint(pygame.mouse.get_pos()) else UI_TEXT
        pygame.draw.polygon(surface, arrow_color, [
            (self.x + self.width - 20, self.y + self.height // 2),
            (self.x + self.width - 10, self.y + self.height // 2 - 8),
            (self.x + self.width - 10, self.y + self.height // 2 + 8),
        ])

        # Draw current option label
        current_label = self.labels[self._selected]
        text_surface = self.font.render(current_label, True, UI_TEXT)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)


class Button:
    """
    A clickable button.
    """

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 on_click: Optional[Callable[[], None]] = None):
        """
        Initialize the button.

        Args:
            x, y: Position
            width, height: Size
            text: Button text
            on_click: Callback when clicked
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.on_click = on_click

        self.rect = pygame.Rect(x, y, width, height)
        self.hover = False
        self.pressed = False

        self.font = pygame.font.Font(None, 32)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input event."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:
                self.pressed = False
                if self.rect.collidepoint(event.pos) and self.on_click:
                    self.on_click()
                return True

        elif event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the button."""
        # Background
        if self.pressed:
            bg_color = CAFE_WARM
        elif self.hover:
            bg_color = UI_HIGHLIGHT
        else:
            bg_color = UI_PANEL

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 2, border_radius=6)

        # Text
        text_color = CAFE_CREAM if self.pressed or self.hover else UI_TEXT
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
