"""
Item Tooltip UI Component for Dragon Haven Cafe.
Displays detailed item information on hover or click.
"""

import pygame
from typing import Optional, Tuple
from constants import (
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM, BLACK,
    ITEM_CATEGORIES,
)
from systems.inventory import ItemStack


class ItemTooltip:
    """
    A tooltip popup showing detailed item information.

    Usage:
        tooltip = ItemTooltip()
        tooltip.show(item_stack, x, y)
        tooltip.draw(surface)
    """

    # Minimum tooltip dimensions
    MIN_WIDTH = 200
    MIN_HEIGHT = 120

    def __init__(self):
        """Initialize the tooltip."""
        self._visible = False
        self._item_stack: Optional[ItemStack] = None
        self._x = 0
        self._y = 0
        self._width = self.MIN_WIDTH
        self._height = self.MIN_HEIGHT

        # Animation
        self._alpha = 0
        self._target_alpha = 0
        self._fade_speed = 1500  # Alpha per second

        # Fonts
        self.title_font = pygame.font.Font(None, 24)
        self.text_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 18)

    def show(self, item_stack: ItemStack, x: int, y: int,
             screen_width: int = 1280, screen_height: int = 720):
        """
        Show the tooltip for an item.

        Args:
            item_stack: The item to display
            x, y: Position to show at (will adjust to fit screen)
            screen_width, screen_height: Screen dimensions for clamping
        """
        self._item_stack = item_stack
        self._visible = True
        self._target_alpha = 255

        # Calculate tooltip size based on content
        self._calculate_size()

        # Position tooltip (avoid going off-screen)
        self._x = x + 10  # Offset from cursor
        self._y = y + 10

        # Clamp to screen
        if self._x + self._width > screen_width - 10:
            self._x = x - self._width - 10
        if self._y + self._height > screen_height - 10:
            self._y = screen_height - self._height - 10

        self._x = max(10, self._x)
        self._y = max(10, self._y)

    def hide(self):
        """Hide the tooltip."""
        self._target_alpha = 0

    def is_visible(self) -> bool:
        """Check if tooltip is visible."""
        return self._visible

    def update(self, dt: float):
        """Update tooltip animation."""
        if self._alpha < self._target_alpha:
            self._alpha = min(self._target_alpha, self._alpha + self._fade_speed * dt)
        elif self._alpha > self._target_alpha:
            self._alpha = max(self._target_alpha, self._alpha - self._fade_speed * dt)

        if self._alpha <= 0:
            self._visible = False

    def _calculate_size(self):
        """Calculate tooltip size based on content."""
        if not self._item_stack:
            return

        # Calculate width based on longest text line
        item = self._item_stack.item
        lines = [
            item.name,
            f"Category: {item.category.title()}",
            f"Quality: {'★' * int(item.quality * 3)} ({item.quality:.1f})",
        ]

        if item.description:
            lines.append(item.description)

        if self._item_stack.item.spoil_days > 0:
            lines.append(f"Spoils in: {self._item_stack.days_until_spoil} days")

        lines.append(f"Sell: {item.get_sell_price()}g")

        max_width = max(self.text_font.size(line)[0] for line in lines)
        self._width = max(self.MIN_WIDTH, max_width + 40)
        self._height = 20 + len(lines) * 22 + 20

    def draw(self, surface: pygame.Surface):
        """Draw the tooltip."""
        if not self._visible or not self._item_stack or self._alpha <= 0:
            return

        item = self._item_stack.item
        alpha = int(self._alpha)

        # Create tooltip surface
        tooltip_surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)

        # Background
        bg_color = (45, 40, 55, min(240, alpha))
        pygame.draw.rect(tooltip_surface, bg_color, tooltip_surface.get_rect(), border_radius=6)

        # Border
        border_color = (95, 85, 115, alpha)
        pygame.draw.rect(tooltip_surface, border_color, tooltip_surface.get_rect(), 2, border_radius=6)

        y_offset = 10

        # Title (item name)
        title_color = (255, 245, 220, alpha)
        title_surface = self.title_font.render(item.name, True, title_color[:3])
        title_surface.set_alpha(alpha)
        tooltip_surface.blit(title_surface, (15, y_offset))
        y_offset += 28

        # Category
        cat_color = (180, 170, 195, alpha)
        cat_text = f"Category: {item.category.title()}"
        cat_surface = self.text_font.render(cat_text, True, cat_color[:3])
        cat_surface.set_alpha(alpha)
        tooltip_surface.blit(cat_surface, (15, y_offset))
        y_offset += 22

        # Quality
        quality_stars = int(item.quality * 3)
        quality_text = "Quality: "
        qual_surface = self.text_font.render(quality_text, True, cat_color[:3])
        qual_surface.set_alpha(alpha)
        tooltip_surface.blit(qual_surface, (15, y_offset))

        # Draw stars
        star_x = 15 + qual_surface.get_width()
        for i in range(quality_stars):
            star_color = (255, 220, 60, alpha)
            pygame.draw.polygon(tooltip_surface, star_color[:3], [
                (star_x + i * 14, y_offset + 8 - 5),
                (star_x + i * 14 + 4, y_offset + 8 + 2),
                (star_x + i * 14 + 8, y_offset + 8 - 5),
                (star_x + i * 14 + 6, y_offset + 8 + 5),
                (star_x + i * 14 + 8, y_offset + 8 + 8),
                (star_x + i * 14 + 4, y_offset + 8 + 6),
                (star_x + i * 14, y_offset + 8 + 8),
                (star_x + i * 14 + 2, y_offset + 8 + 5),
            ])
        y_offset += 22

        # Description
        if item.description:
            desc_color = (160, 150, 175, alpha)
            desc_surface = self.small_font.render(item.description, True, desc_color[:3])
            desc_surface.set_alpha(alpha)
            tooltip_surface.blit(desc_surface, (15, y_offset))
            y_offset += 22

        # Spoilage
        if item.spoil_days > 0:
            days = self._item_stack.days_until_spoil
            if days <= 1:
                spoil_color = (220, 80, 80, alpha)
            elif days <= 2:
                spoil_color = (220, 180, 60, alpha)
            else:
                spoil_color = (100, 180, 100, alpha)

            spoil_text = f"Spoils in: {days} day{'s' if days != 1 else ''}"
            spoil_surface = self.text_font.render(spoil_text, True, spoil_color[:3])
            spoil_surface.set_alpha(alpha)
            tooltip_surface.blit(spoil_surface, (15, y_offset))
            y_offset += 22
        else:
            # Non-perishable
            np_text = "Non-perishable"
            np_surface = self.small_font.render(np_text, True, (100, 180, 100)[:3])
            np_surface.set_alpha(alpha)
            tooltip_surface.blit(np_surface, (15, y_offset))
            y_offset += 22

        # Price
        price_text = f"Sell: {item.get_sell_price()}g"
        price_surface = self.text_font.render(price_text, True, (220, 180, 60))
        price_surface.set_alpha(alpha)
        tooltip_surface.blit(price_surface, (15, y_offset))

        # Blit tooltip to main surface
        surface.blit(tooltip_surface, (self._x, self._y))


class ConfirmDialog:
    """
    A confirmation dialog for actions like discarding items.

    Usage:
        dialog = ConfirmDialog("Discard item?", "Are you sure?")
        dialog.show()
        # In event loop:
        result = dialog.handle_click(pos)
        if result == 'yes': ...
    """

    def __init__(self, title: str, message: str, width: int = 300, height: int = 150):
        """
        Initialize the dialog.

        Args:
            title: Dialog title
            message: Dialog message
            width, height: Dialog dimensions
        """
        self.title = title
        self.message = message
        self.width = width
        self.height = height

        self._visible = False
        self._x = 0
        self._y = 0

        # Buttons
        button_width = 80
        button_height = 30
        button_y = height - 50
        self.yes_rect = pygame.Rect(width // 2 - button_width - 10, button_y,
                                    button_width, button_height)
        self.no_rect = pygame.Rect(width // 2 + 10, button_y,
                                   button_width, button_height)

        # Fonts
        self.title_font = pygame.font.Font(None, 28)
        self.text_font = pygame.font.Font(None, 22)
        self.button_font = pygame.font.Font(None, 22)

    def show(self, screen_width: int = 1280, screen_height: int = 720):
        """Show the dialog centered on screen."""
        self._visible = True
        self._x = (screen_width - self.width) // 2
        self._y = (screen_height - self.height) // 2

    def hide(self):
        """Hide the dialog."""
        self._visible = False

    def is_visible(self) -> bool:
        """Check if dialog is visible."""
        return self._visible

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Handle click event.

        Returns:
            'yes', 'no', or None if no button clicked
        """
        if not self._visible:
            return None

        # Adjust position relative to dialog
        rel_x = pos[0] - self._x
        rel_y = pos[1] - self._y

        if self.yes_rect.collidepoint(rel_x, rel_y):
            self.hide()
            return 'yes'
        elif self.no_rect.collidepoint(rel_x, rel_y):
            self.hide()
            return 'no'

        return None

    def draw(self, surface: pygame.Surface):
        """Draw the dialog."""
        if not self._visible:
            return

        # Darken background
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # Dialog box
        dialog_rect = pygame.Rect(self._x, self._y, self.width, self.height)
        pygame.draw.rect(surface, UI_PANEL, dialog_rect, border_radius=8)
        pygame.draw.rect(surface, UI_BORDER, dialog_rect, 2, border_radius=8)

        # Title
        title_surface = self.title_font.render(self.title, True, CAFE_CREAM)
        title_rect = title_surface.get_rect(centerx=self._x + self.width // 2,
                                            y=self._y + 15)
        surface.blit(title_surface, title_rect)

        # Message
        msg_surface = self.text_font.render(self.message, True, UI_TEXT)
        msg_rect = msg_surface.get_rect(centerx=self._x + self.width // 2,
                                        y=self._y + 55)
        surface.blit(msg_surface, msg_rect)

        # Buttons
        # Yes button
        yes_rect_abs = self.yes_rect.move(self._x, self._y)
        pygame.draw.rect(surface, (80, 160, 80), yes_rect_abs, border_radius=4)
        pygame.draw.rect(surface, (60, 140, 60), yes_rect_abs, 1, border_radius=4)
        yes_text = self.button_font.render("Yes", True, (255, 255, 255))
        surface.blit(yes_text, yes_text.get_rect(center=yes_rect_abs.center))

        # No button
        no_rect_abs = self.no_rect.move(self._x, self._y)
        pygame.draw.rect(surface, (180, 80, 80), no_rect_abs, border_radius=4)
        pygame.draw.rect(surface, (160, 60, 60), no_rect_abs, 1, border_radius=4)
        no_text = self.button_font.render("No", True, (255, 255, 255))
        surface.blit(no_text, no_text.get_rect(center=no_rect_abs.center))
