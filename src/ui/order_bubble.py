"""
Order Bubble UI Component for Dragon Haven Cafe.
Displays customer orders above their heads.
"""

import pygame
from typing import Optional, Tuple
from constants import (
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM,
    RECIPE_CATEGORY_APPETIZER, RECIPE_CATEGORY_MAIN,
    RECIPE_CATEGORY_DESSERT, RECIPE_CATEGORY_BEVERAGE,
)


class OrderBubble:
    """
    A speech bubble that shows a customer's order.

    Usage:
        bubble = OrderBubble(x, y)
        bubble.set_order('main', 'berry_tart')
        bubble.draw(surface)
    """

    # Category colors
    CATEGORY_COLORS = {
        RECIPE_CATEGORY_APPETIZER: (100, 180, 100),  # Green
        RECIPE_CATEGORY_MAIN: (220, 140, 80),        # Orange
        RECIPE_CATEGORY_DESSERT: (220, 120, 180),    # Pink
        RECIPE_CATEGORY_BEVERAGE: (100, 160, 220),   # Blue
    }

    # Category icons (simple shapes)
    CATEGORY_ICONS = {
        RECIPE_CATEGORY_APPETIZER: 'leaf',
        RECIPE_CATEGORY_MAIN: 'plate',
        RECIPE_CATEGORY_DESSERT: 'cake',
        RECIPE_CATEGORY_BEVERAGE: 'cup',
    }

    def __init__(self, x: int, y: int, width: int = 60, height: int = 40):
        """
        Initialize an order bubble.

        Args:
            x, y: Position (center-bottom of bubble, above character head)
            width: Bubble width
            height: Bubble height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Order info
        self._category: Optional[str] = None
        self._recipe_id: Optional[str] = None
        self._recipe_name: Optional[str] = None

        # Animation
        self._bob_offset = 0.0
        self._bob_timer = 0.0
        self._visible = False
        self._alpha = 255

        # Font
        self.font = pygame.font.Font(None, 18)

    def set_order(self, category: str, recipe_id: str = None, recipe_name: str = None):
        """
        Set the order to display.

        Args:
            category: Order category (appetizer, main, dessert, drink)
            recipe_id: Specific recipe ID (optional)
            recipe_name: Display name for recipe (optional)
        """
        self._category = category
        self._recipe_id = recipe_id
        self._recipe_name = recipe_name
        self._visible = True

    def clear(self):
        """Clear the order display."""
        self._category = None
        self._recipe_id = None
        self._recipe_name = None
        self._visible = False

    def set_position(self, x: int, y: int):
        """Update bubble position."""
        self.x = x
        self.y = y

    def is_visible(self) -> bool:
        """Check if bubble is visible."""
        return self._visible

    def update(self, dt: float):
        """Update animation."""
        # Bobbing animation
        self._bob_timer += dt * 2
        import math
        self._bob_offset = math.sin(self._bob_timer) * 3

    def draw(self, surface: pygame.Surface):
        """Draw the order bubble."""
        if not self._visible or not self._category:
            return

        # Calculate bubble position with bob
        bubble_x = self.x - self.width // 2
        bubble_y = self.y - self.height + int(self._bob_offset)

        # Draw bubble background
        bubble_rect = pygame.Rect(bubble_x, bubble_y, self.width, self.height)
        pygame.draw.rect(surface, UI_PANEL, bubble_rect, border_radius=8)
        pygame.draw.rect(surface, UI_BORDER, bubble_rect, 2, border_radius=8)

        # Draw speech bubble pointer (triangle at bottom)
        pointer_points = [
            (self.x - 6, bubble_y + self.height),
            (self.x + 6, bubble_y + self.height),
            (self.x, bubble_y + self.height + 8 + int(self._bob_offset))
        ]
        pygame.draw.polygon(surface, UI_PANEL, pointer_points)
        # Border lines for pointer
        pygame.draw.line(surface, UI_BORDER, pointer_points[0], pointer_points[2], 2)
        pygame.draw.line(surface, UI_BORDER, pointer_points[1], pointer_points[2], 2)

        # Draw category icon
        icon_color = self.CATEGORY_COLORS.get(self._category, (150, 150, 150))
        icon_x = bubble_x + self.width // 2
        icon_y = bubble_y + self.height // 2 - 5

        self._draw_category_icon(surface, icon_x, icon_y, self._category, icon_color)

        # Draw category text
        if self._recipe_name:
            text = self._recipe_name[:10]  # Truncate long names
        else:
            text = self._category.capitalize()[:8]

        text_surface = self.font.render(text, True, UI_TEXT_DIM)
        text_rect = text_surface.get_rect(centerx=bubble_x + self.width // 2,
                                          y=bubble_y + self.height - 14)
        surface.blit(text_surface, text_rect)

    def _draw_category_icon(self, surface: pygame.Surface, x: int, y: int,
                           category: str, color: Tuple[int, int, int]):
        """Draw a simple category icon."""
        if category == RECIPE_CATEGORY_APPETIZER:
            # Leaf shape
            pygame.draw.ellipse(surface, color, (x - 8, y - 4, 16, 8))
            pygame.draw.line(surface, (80, 120, 80), (x, y - 4), (x, y + 6), 2)

        elif category == RECIPE_CATEGORY_MAIN:
            # Plate with food
            pygame.draw.ellipse(surface, color, (x - 10, y - 3, 20, 8))
            pygame.draw.ellipse(surface, (255, 255, 255), (x - 8, y - 2, 16, 6), 1)
            pygame.draw.circle(surface, (180, 100, 80), (x, y - 2), 4)

        elif category == RECIPE_CATEGORY_DESSERT:
            # Cake slice
            pygame.draw.polygon(surface, color, [
                (x - 8, y + 6), (x + 8, y + 6), (x, y - 8)
            ])
            pygame.draw.line(surface, (255, 200, 200), (x - 4, y), (x + 4, y), 2)

        elif category == RECIPE_CATEGORY_BEVERAGE:
            # Cup
            pygame.draw.rect(surface, color, (x - 6, y - 4, 12, 14), border_radius=2)
            pygame.draw.rect(surface, (100, 160, 220), (x - 4, y - 2, 8, 8), border_radius=1)


class PatienceMeter:
    """
    A small meter showing customer patience.
    """

    def __init__(self, x: int, y: int, width: int = 40, height: int = 6):
        """
        Initialize patience meter.

        Args:
            x, y: Center position
            width: Meter width
            height: Meter height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self._patience = 1.0  # 0.0-1.0

    def set_patience(self, patience: float):
        """Set patience value (0.0-1.0)."""
        self._patience = max(0.0, min(1.0, patience))

    def set_position(self, x: int, y: int):
        """Update meter position."""
        self.x = x
        self.y = y

    def draw(self, surface: pygame.Surface):
        """Draw the patience meter."""
        # Background
        bg_rect = pygame.Rect(
            self.x - self.width // 2, self.y,
            self.width, self.height
        )
        pygame.draw.rect(surface, (40, 35, 50), bg_rect, border_radius=2)

        # Fill based on patience
        fill_width = int(self._patience * (self.width - 2))
        if fill_width > 0:
            # Color gradient from green to red
            if self._patience > 0.6:
                color = (80, 180, 100)  # Green
            elif self._patience > 0.3:
                color = (220, 180, 60)  # Yellow
            else:
                color = (220, 80, 80)  # Red

            fill_rect = pygame.Rect(
                self.x - self.width // 2 + 1, self.y + 1,
                fill_width, self.height - 2
            )
            pygame.draw.rect(surface, color, fill_rect, border_radius=1)

        # Border
        pygame.draw.rect(surface, UI_BORDER, bg_rect, 1, border_radius=2)
