"""
Item Slot UI Component for Dragon Haven Cafe.
Displays an inventory item with quantity, quality, and spoilage.
"""

import pygame
from typing import Optional, Dict, Any, Tuple
from constants import (
    UI_PANEL, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM,
    ITEM_VEGETABLE, ITEM_FRUIT, ITEM_GRAIN, ITEM_MEAT,
    ITEM_SEAFOOD, ITEM_DAIRY, ITEM_SPICE, ITEM_SPECIAL,
)
from systems.inventory import ItemStack


class ItemSlot:
    """
    A single inventory slot displaying an item.

    Usage:
        slot = ItemSlot(x, y, 48)
        slot.set_item(item_stack)
        slot.draw(surface)
    """

    # Category colors for item backgrounds
    CATEGORY_COLORS = {
        ITEM_VEGETABLE: (80, 160, 80),
        ITEM_FRUIT: (180, 100, 120),
        ITEM_GRAIN: (200, 180, 120),
        ITEM_MEAT: (180, 100, 90),
        ITEM_SEAFOOD: (100, 140, 200),
        ITEM_DAIRY: (230, 220, 200),
        ITEM_SPICE: (140, 100, 60),
        ITEM_SPECIAL: (180, 140, 200),
    }

    def __init__(self, x: int, y: int, size: int = 48, index: int = -1):
        """
        Initialize an item slot.

        Args:
            x, y: Position
            size: Slot size (width and height)
            index: Slot index in container (-1 if not applicable)
        """
        self.x = x
        self.y = y
        self.size = size
        self.index = index

        self.rect = pygame.Rect(x, y, size, size)

        # Item reference
        self._item_stack: Optional[ItemStack] = None

        # State
        self.selected = False
        self.hover = False
        self.disabled = False

        # Fonts
        self.quantity_font = pygame.font.Font(None, 18)
        self.quality_font = pygame.font.Font(None, 14)

    def set_item(self, item_stack: Optional[ItemStack]):
        """Set the item in this slot."""
        self._item_stack = item_stack

    def get_item(self) -> Optional[ItemStack]:
        """Get the item in this slot."""
        return self._item_stack

    def is_empty(self) -> bool:
        """Check if slot is empty."""
        return self._item_stack is None

    def contains_point(self, pos: Tuple[int, int]) -> bool:
        """Check if a point is inside this slot."""
        return self.rect.collidepoint(pos)

    def update_hover(self, mouse_pos: Tuple[int, int]):
        """Update hover state based on mouse position."""
        self.hover = self.rect.collidepoint(mouse_pos) and not self.disabled

    def draw(self, surface: pygame.Surface):
        """Draw the item slot."""
        # Background
        if self.selected:
            bg_color = (80, 70, 100)
            border_color = (180, 160, 200)
        elif self.hover:
            bg_color = (60, 55, 80)
            border_color = (120, 110, 140)
        elif self.disabled:
            bg_color = (40, 38, 50)
            border_color = (60, 55, 75)
        else:
            bg_color = UI_PANEL
            border_color = UI_BORDER

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, border_color, self.rect, 1, border_radius=4)

        # Draw item if present
        if self._item_stack and not self._item_stack.is_spoiled():
            self._draw_item(surface)
        elif self._item_stack and self._item_stack.is_spoiled():
            self._draw_spoiled(surface)

    def _draw_item(self, surface: pygame.Surface):
        """Draw the item icon and details."""
        item = self._item_stack.item
        margin = 4

        # Item background based on category
        icon_rect = pygame.Rect(
            self.x + margin,
            self.y + margin,
            self.size - margin * 2 - 10,
            self.size - margin * 2 - 14
        )
        category_color = self.CATEGORY_COLORS.get(item.category, (128, 128, 128))
        pygame.draw.rect(surface, category_color, icon_rect, border_radius=3)

        # Simple item icon based on category
        self._draw_category_icon(surface, icon_rect, item.category)

        # Quantity badge (bottom-right)
        if self._item_stack.quantity > 1:
            qty_text = str(self._item_stack.quantity)
            qty_surface = self.quantity_font.render(qty_text, True, CAFE_CREAM)
            qty_x = self.x + self.size - qty_surface.get_width() - 3
            qty_y = self.y + self.size - qty_surface.get_height() - 2

            # Badge background
            badge_rect = pygame.Rect(qty_x - 2, qty_y - 1,
                                    qty_surface.get_width() + 4,
                                    qty_surface.get_height() + 2)
            pygame.draw.rect(surface, (40, 35, 50), badge_rect, border_radius=2)
            surface.blit(qty_surface, (qty_x, qty_y))

        # Quality stars (bottom-left)
        quality = self._item_stack.item.quality
        stars = min(5, max(1, int(quality * 3)))  # 1-5 stars
        star_x = self.x + 3
        star_y = self.y + self.size - 10
        for i in range(stars):
            pygame.draw.polygon(surface, (255, 220, 60), [
                (star_x + i * 7, star_y - 3),
                (star_x + i * 7 + 2, star_y),
                (star_x + i * 7 + 4, star_y - 3),
                (star_x + i * 7 + 3, star_y + 1),
                (star_x + i * 7 + 4, star_y + 3),
                (star_x + i * 7, star_y + 1),
            ])

        # Spoilage indicator (top-right)
        if self._item_stack.item.spoil_days > 0 and self._item_stack.days_until_spoil > 0:
            days = self._item_stack.days_until_spoil

            # Color based on urgency
            if days <= 1:
                spoil_color = (220, 80, 80)  # Red
            elif days <= 2:
                spoil_color = (220, 180, 60)  # Yellow
            else:
                spoil_color = (100, 180, 100)  # Green

            # Small indicator dot
            pygame.draw.circle(surface, spoil_color,
                             (self.x + self.size - 8, self.y + 8), 4)
            pygame.draw.circle(surface, (40, 35, 50),
                             (self.x + self.size - 8, self.y + 8), 4, 1)

    def _draw_category_icon(self, surface: pygame.Surface, rect: pygame.Rect,
                            category: str):
        """Draw a simple icon based on item category."""
        cx = rect.centerx
        cy = rect.centery

        if category == ITEM_VEGETABLE:
            # Carrot shape
            pygame.draw.polygon(surface, (255, 160, 60), [
                (cx, cy + 10), (cx - 5, cy - 8), (cx + 5, cy - 8)
            ])
            pygame.draw.line(surface, (80, 160, 80), (cx, cy - 8), (cx, cy - 14), 2)

        elif category == ITEM_FRUIT:
            # Apple shape
            pygame.draw.circle(surface, (220, 80, 80), (cx, cy + 2), 10)
            pygame.draw.line(surface, (100, 70, 50), (cx, cy - 8), (cx, cy - 12), 2)

        elif category == ITEM_GRAIN:
            # Wheat shape
            pygame.draw.ellipse(surface, (220, 190, 100), (cx - 4, cy - 8, 8, 16))
            pygame.draw.line(surface, (140, 120, 60), (cx, cy + 8), (cx, cy + 14), 2)

        elif category == ITEM_MEAT:
            # Meat shape
            pygame.draw.ellipse(surface, (200, 120, 100), (cx - 10, cy - 6, 20, 12))
            pygame.draw.circle(surface, (240, 220, 200), (cx - 4, cy), 3)

        elif category == ITEM_SEAFOOD:
            # Fish shape
            pygame.draw.ellipse(surface, (140, 180, 220), (cx - 10, cy - 4, 20, 8))
            pygame.draw.polygon(surface, (140, 180, 220), [
                (cx + 10, cy), (cx + 16, cy - 5), (cx + 16, cy + 5)
            ])

        elif category == ITEM_DAIRY:
            # Milk bottle shape
            pygame.draw.rect(surface, (250, 250, 250), (cx - 6, cy - 4, 12, 14), border_radius=2)
            pygame.draw.rect(surface, (250, 250, 250), (cx - 4, cy - 8, 8, 6))

        elif category == ITEM_SPICE:
            # Spice jar shape
            pygame.draw.rect(surface, (160, 120, 80), (cx - 6, cy - 2, 12, 12), border_radius=2)
            pygame.draw.rect(surface, (100, 70, 50), (cx - 4, cy - 6, 8, 5))

        elif category == ITEM_SPECIAL:
            # Star/crystal shape
            pygame.draw.polygon(surface, (200, 180, 220), [
                (cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy),
                (cx + 3, cy + 3), (cx, cy + 10), (cx - 3, cy + 3),
                (cx - 10, cy), (cx - 3, cy - 3)
            ])

    def _draw_spoiled(self, surface: pygame.Surface):
        """Draw spoiled item indicator."""
        # Gray out the slot
        spoiled_surface = pygame.Surface((self.size - 4, self.size - 4), pygame.SRCALPHA)
        pygame.draw.rect(spoiled_surface, (60, 60, 60, 200), spoiled_surface.get_rect(), border_radius=3)

        # X mark
        pygame.draw.line(spoiled_surface, (180, 80, 80),
                        (5, 5), (self.size - 9, self.size - 9), 3)
        pygame.draw.line(spoiled_surface, (180, 80, 80),
                        (self.size - 9, 5), (5, self.size - 9), 3)

        surface.blit(spoiled_surface, (self.x + 2, self.y + 2))


class ItemSlotGrid:
    """
    A grid of item slots for displaying inventory containers.

    Usage:
        grid = ItemSlotGrid(x, y, 5, 4, container)
        grid.draw(surface)
    """

    def __init__(self, x: int, y: int, columns: int, rows: int,
                 slot_size: int = 48, spacing: int = 4):
        """
        Initialize the item slot grid.

        Args:
            x, y: Top-left position
            columns: Number of columns
            rows: Number of rows
            slot_size: Size of each slot
            spacing: Space between slots
        """
        self.x = x
        self.y = y
        self.columns = columns
        self.rows = rows
        self.slot_size = slot_size
        self.spacing = spacing

        # Calculate total size
        self.width = columns * slot_size + (columns - 1) * spacing
        self.height = rows * slot_size + (rows - 1) * spacing

        # Create slots
        self.slots: list[ItemSlot] = []
        for row in range(rows):
            for col in range(columns):
                slot_x = x + col * (slot_size + spacing)
                slot_y = y + row * (slot_size + spacing)
                index = row * columns + col
                slot = ItemSlot(slot_x, slot_y, slot_size, index)
                self.slots.append(slot)

        # Selection
        self._selected_index = -1
        self._scroll_offset = 0

    def set_container(self, container):
        """Set the inventory container to display."""
        # Clear all slots first
        for slot in self.slots:
            slot.set_item(None)
            slot.disabled = False

        # Fill slots from container
        for i, slot in enumerate(self.slots):
            adj_index = i + self._scroll_offset * self.columns
            if container and adj_index < len(container.slots):
                slot.set_item(container.slots[adj_index])
                if adj_index >= container.max_slots:
                    slot.disabled = True
            else:
                slot.disabled = (container is None or
                                adj_index >= container.max_slots)

    def update(self, mouse_pos: Tuple[int, int]):
        """Update slot hover states."""
        for slot in self.slots:
            slot.update_hover(mouse_pos)

    def handle_click(self, pos: Tuple[int, int]) -> int:
        """
        Handle click on the grid.

        Returns:
            Index of clicked slot (-1 if none)
        """
        for i, slot in enumerate(self.slots):
            if slot.contains_point(pos) and not slot.disabled:
                # Update selection
                if self._selected_index >= 0:
                    self.slots[self._selected_index].selected = False
                self._selected_index = i
                slot.selected = True
                return i + self._scroll_offset * self.columns
        return -1

    def clear_selection(self):
        """Clear current selection."""
        if self._selected_index >= 0:
            self.slots[self._selected_index].selected = False
        self._selected_index = -1

    def get_selected_slot(self) -> Optional[ItemSlot]:
        """Get the currently selected slot."""
        if 0 <= self._selected_index < len(self.slots):
            return self.slots[self._selected_index]
        return None

    def draw(self, surface: pygame.Surface):
        """Draw all slots in the grid."""
        for slot in self.slots:
            slot.draw(surface)
