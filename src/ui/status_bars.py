"""
Status Bar UI Components for Dragon Haven Cafe.
Reusable progress/status bars for HUD and menus.
"""

import pygame
from typing import Tuple, Optional
from constants import (
    STATUS_BAR_WIDTH, STATUS_BAR_HEIGHT,
    HUD_BORDER_COLOR, HUD_PANEL_COLOR,
    HUNGER_ORANGE, STAMINA_YELLOW, HAPPINESS_PINK, HEALTH_GREEN,
    UI_TEXT, UI_TEXT_DIM, WHITE, BLACK,
    DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
    DRAGON_STAGE_ADOLESCENT, DRAGON_STAGE_ADULT,
)


class StatusBar:
    """
    A horizontal status/progress bar for displaying stats.

    Usage:
        bar = StatusBar(x, y, 'Hunger', HUNGER_ORANGE)
        bar.set_value(75)  # 75%
        bar.draw(surface)
    """

    def __init__(self, x: int, y: int, label: str, color: Tuple[int, int, int],
                 width: int = STATUS_BAR_WIDTH, height: int = STATUS_BAR_HEIGHT,
                 show_label: bool = True, show_value: bool = False):
        """
        Initialize a status bar.

        Args:
            x, y: Position
            label: Label text
            color: Fill color when full
            width: Bar width
            height: Bar height
            show_label: Whether to display the label
            show_value: Whether to show numeric value
        """
        self.x = x
        self.y = y
        self.label = label
        self.color = color
        self.width = width
        self.height = height
        self.show_label = show_label
        self.show_value = show_value

        self._value = 1.0  # 0.0 to 1.0
        self._target_value = 1.0  # For smooth animation
        self._warning_threshold = 0.3  # Flash when below this
        self._flash_timer = 0.0

        # Background rect
        self.rect = pygame.Rect(x, y, width, height)

        # Fonts
        self.label_font = pygame.font.Font(None, 20)
        self.value_font = pygame.font.Font(None, 18)

    @property
    def value(self) -> float:
        return self._value

    def set_value(self, value: float, animated: bool = True):
        """
        Set the bar value.

        Args:
            value: New value (0.0-1.0 or 0-100)
            animated: Whether to animate the change
        """
        # Convert from 0-100 to 0-1 if needed
        if value > 1.0:
            value = value / 100.0

        value = max(0.0, min(1.0, value))

        if animated:
            self._target_value = value
        else:
            self._value = value
            self._target_value = value

    def update(self, dt: float):
        """Update animation."""
        # Smooth transition to target
        if self._value != self._target_value:
            diff = self._target_value - self._value
            self._value += diff * min(1.0, dt * 5)

            # Snap if close enough
            if abs(self._value - self._target_value) < 0.01:
                self._value = self._target_value

        # Update flash timer for warning state
        if self._value < self._warning_threshold:
            self._flash_timer += dt
        else:
            self._flash_timer = 0.0

    def draw(self, surface: pygame.Surface):
        """Draw the status bar."""
        # Draw label if enabled
        if self.show_label:
            label_surface = self.label_font.render(self.label, True, UI_TEXT_DIM)
            label_rect = label_surface.get_rect(
                right=self.x - 5,
                centery=self.y + self.height // 2
            )
            surface.blit(label_surface, label_rect)

        # Draw background
        pygame.draw.rect(surface, HUD_PANEL_COLOR, self.rect, border_radius=3)
        pygame.draw.rect(surface, HUD_BORDER_COLOR, self.rect, 1, border_radius=3)

        # Calculate fill width
        fill_width = int(self._value * (self.width - 4))

        if fill_width > 0:
            # Determine color (flash if low)
            if self._value < self._warning_threshold:
                # Flash between normal and warning colors
                flash = (int(self._flash_timer * 4) % 2) == 0
                fill_color = (220, 80, 80) if flash else self.color
            else:
                fill_color = self.color

            # Create gradient effect
            fill_rect = pygame.Rect(self.x + 2, self.y + 2, fill_width, self.height - 4)
            pygame.draw.rect(surface, fill_color, fill_rect, border_radius=2)

            # Add highlight
            highlight_color = tuple(min(255, c + 40) for c in fill_color)
            highlight_rect = pygame.Rect(self.x + 2, self.y + 2, fill_width, (self.height - 4) // 2)
            pygame.draw.rect(surface, highlight_color, highlight_rect, border_radius=2)

        # Draw value if enabled
        if self.show_value:
            value_text = f"{int(self._value * 100)}"
            value_surface = self.value_font.render(value_text, True, WHITE)
            value_rect = value_surface.get_rect(
                left=self.x + self.width + 5,
                centery=self.y + self.height // 2
            )
            surface.blit(value_surface, value_rect)


class DragonStatusBars:
    """
    Grouped status bars for dragon stats (hunger, stamina, happiness).
    """

    def __init__(self, x: int, y: int):
        """
        Initialize dragon status bar group.

        Args:
            x, y: Top-left position of the group
        """
        self.x = x
        self.y = y

        # Create bars
        bar_y = y
        self.hunger_bar = StatusBar(x + 80, bar_y, "Hunger", HUNGER_ORANGE, show_label=True)
        bar_y += STATUS_BAR_HEIGHT + 6
        self.stamina_bar = StatusBar(x + 80, bar_y, "Stamina", STAMINA_YELLOW, show_label=True)
        bar_y += STATUS_BAR_HEIGHT + 6
        self.happiness_bar = StatusBar(x + 80, bar_y, "Happy", HAPPINESS_PINK, show_label=True)

        self.bars = [self.hunger_bar, self.stamina_bar, self.happiness_bar]

        # Dragon name/mood/stage display
        self.dragon_name = "Dragon"
        self.dragon_mood = "content"
        self.dragon_stage = DRAGON_STAGE_EGG

        # Fonts
        self.name_font = pygame.font.Font(None, 24)
        self.mood_font = pygame.font.Font(None, 20)

    def set_dragon_stats(self, hunger: float, stamina: float, happiness: float,
                         name: str = None, mood: str = None, stage: str = None):
        """
        Update all dragon stats.

        Args:
            hunger: Hunger value (0-100)
            stamina: Stamina value (0-100)
            happiness: Happiness value (0-100)
            name: Dragon name (optional)
            mood: Dragon mood (optional)
            stage: Dragon stage (optional)
        """
        self.hunger_bar.set_value(hunger)
        self.stamina_bar.set_value(stamina)
        self.happiness_bar.set_value(happiness)

        if name:
            self.dragon_name = name
        if mood:
            self.dragon_mood = mood
        if stage:
            self.dragon_stage = stage

    def update(self, dt: float):
        """Update all bars."""
        for bar in self.bars:
            bar.update(dt)

    def draw(self, surface: pygame.Surface):
        """Draw all bars and dragon info."""
        # Draw semi-transparent background panel
        panel_width = 220
        panel_height = 80
        panel_rect = pygame.Rect(self.x - 5, self.y - 25, panel_width, panel_height)

        # Create semi-transparent surface
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (30, 28, 40, 180), panel_surface.get_rect(), border_radius=6)
        pygame.draw.rect(panel_surface, (60, 55, 75, 200), panel_surface.get_rect(), 1, border_radius=6)
        surface.blit(panel_surface, panel_rect)

        # Draw small dragon stage icon
        self._draw_dragon_icon(surface, self.x + 5, self.y - 18)

        # Draw dragon name (offset for icon)
        name_surface = self.name_font.render(self.dragon_name, True, UI_TEXT)
        surface.blit(name_surface, (self.x + 25, self.y - 20))

        # Draw mood indicator
        mood_colors = {
            'happy': HEALTH_GREEN,
            'content': (150, 200, 150),
            'neutral': UI_TEXT_DIM,
            'tired': STAMINA_YELLOW,
            'hungry': HUNGER_ORANGE,
            'sad': (180, 100, 120),
            'incubating': (200, 190, 170),
        }
        mood_color = mood_colors.get(self.dragon_mood, UI_TEXT_DIM)

        mood_text = self.dragon_mood.capitalize()
        mood_surface = self.mood_font.render(mood_text, True, mood_color)
        mood_x = self.x + panel_width - mood_surface.get_width() - 10
        surface.blit(mood_surface, (mood_x, self.y - 18))

        # Draw bars
        for bar in self.bars:
            bar.draw(surface)

    def _draw_dragon_icon(self, surface: pygame.Surface, x: int, y: int):
        """Draw a small dragon stage icon."""
        if self.dragon_stage == DRAGON_STAGE_EGG:
            # Egg icon
            pygame.draw.ellipse(surface, (200, 180, 160), (x, y - 2, 12, 16))
            pygame.draw.ellipse(surface, (180, 160, 140), (x, y - 2, 12, 16), 1)
            pygame.draw.circle(surface, (170, 150, 130), (x + 4, y + 4), 2)
        elif self.dragon_stage == DRAGON_STAGE_HATCHLING:
            # Tiny dragon head
            pygame.draw.ellipse(surface, (120, 180, 120), (x, y, 14, 12))
            pygame.draw.circle(surface, (255, 255, 255), (x + 9, y + 3), 3)
            pygame.draw.circle(surface, (40, 40, 40), (x + 10, y + 3), 1)
        elif self.dragon_stage == DRAGON_STAGE_JUVENILE:
            # Small dragon with horns
            pygame.draw.ellipse(surface, (100, 160, 200), (x, y, 14, 12))
            pygame.draw.polygon(surface, (80, 140, 180), [(x + 3, y), (x + 2, y - 5), (x + 6, y)])
            pygame.draw.circle(surface, (255, 255, 255), (x + 9, y + 3), 3)
            pygame.draw.circle(surface, (40, 40, 40), (x + 10, y + 3), 1)
        elif self.dragon_stage == DRAGON_STAGE_ADOLESCENT:
            # Larger dragon with wing buds
            pygame.draw.ellipse(surface, (160, 100, 180), (x, y, 16, 12))
            pygame.draw.polygon(surface, (140, 80, 160), [(x + 3, y), (x + 1, y - 6), (x + 7, y)])
            pygame.draw.ellipse(surface, (140, 80, 160), (x - 2, y - 2, 8, 5))  # Wing bud
            pygame.draw.circle(surface, (255, 255, 255), (x + 11, y + 3), 3)
            pygame.draw.circle(surface, (40, 40, 40), (x + 12, y + 3), 1)
        else:  # DRAGON_STAGE_ADULT
            # Majestic dragon with wings
            pygame.draw.ellipse(surface, (200, 80, 80), (x, y, 16, 12))
            pygame.draw.polygon(surface, (180, 60, 60), [(x + 4, y), (x + 2, y - 7), (x + 8, y)])
            pygame.draw.polygon(surface, (180, 100, 100), [(x - 3, y - 3), (x - 6, y - 8), (x + 2, y)])  # Wing
            pygame.draw.circle(surface, (255, 255, 255), (x + 11, y + 3), 3)
            pygame.draw.circle(surface, (180, 50, 50), (x + 11, y + 3), 2)
            pygame.draw.circle(surface, (40, 40, 40), (x + 12, y + 3), 1)
            # Fire glow
            pygame.draw.circle(surface, (255, 150, 50), (x + 16, y + 5), 2)


class QuickInventorySlot:
    """
    A single slot in the quick inventory bar.
    """

    def __init__(self, x: int, y: int, size: int, index: int):
        """
        Initialize a quick inventory slot.

        Args:
            x, y: Position
            size: Slot size (width and height)
            index: Slot index (0-7)
        """
        self.x = x
        self.y = y
        self.size = size
        self.index = index

        self.rect = pygame.Rect(x, y, size, size)

        # Slot contents
        self.item_id: Optional[str] = None
        self.item_quantity: int = 0
        self.item_color: Tuple[int, int, int] = (128, 128, 128)

        # State
        self.selected = False
        self.hover = False

        # Font
        self.quantity_font = pygame.font.Font(None, 18)
        self.key_font = pygame.font.Font(None, 16)

    def set_item(self, item_id: Optional[str], quantity: int = 0,
                 color: Tuple[int, int, int] = (128, 128, 128)):
        """Set the slot contents."""
        self.item_id = item_id
        self.item_quantity = quantity
        self.item_color = color

    def clear(self):
        """Clear the slot."""
        self.item_id = None
        self.item_quantity = 0

    def draw(self, surface: pygame.Surface):
        """Draw the slot."""
        # Background
        if self.selected:
            bg_color = (80, 70, 100)
            border_color = (180, 160, 200)
        elif self.hover:
            bg_color = (60, 55, 80)
            border_color = (100, 90, 120)
        else:
            bg_color = HUD_PANEL_COLOR
            border_color = HUD_BORDER_COLOR

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, border_color, self.rect, 1, border_radius=4)

        # Draw item if present
        if self.item_id:
            # Draw item icon (simple colored square for now)
            icon_margin = 6
            icon_rect = pygame.Rect(
                self.x + icon_margin, self.y + icon_margin,
                self.size - icon_margin * 2, self.size - icon_margin * 2 - 8
            )
            pygame.draw.rect(surface, self.item_color, icon_rect, border_radius=3)

            # Draw quantity
            if self.item_quantity > 1:
                qty_text = str(self.item_quantity)
                qty_surface = self.quantity_font.render(qty_text, True, WHITE)
                qty_x = self.x + self.size - qty_surface.get_width() - 4
                qty_y = self.y + self.size - qty_surface.get_height() - 2
                surface.blit(qty_surface, (qty_x, qty_y))

        # Draw slot key hint (1-8)
        key_text = str(self.index + 1)
        key_surface = self.key_font.render(key_text, True, UI_TEXT_DIM)
        surface.blit(key_surface, (self.x + 3, self.y + self.size - 14))


class QuickInventoryBar:
    """
    Quick access inventory bar at the bottom of the screen.
    """

    def __init__(self, x: int, y: int, slot_count: int = 8, slot_size: int = 45, spacing: int = 5):
        """
        Initialize the quick inventory bar.

        Args:
            x: Center x position
            y: Y position
            slot_count: Number of slots
            slot_size: Size of each slot
            spacing: Space between slots
        """
        self.slot_count = slot_count
        self.slot_size = slot_size
        self.spacing = spacing

        # Calculate total width and starting x
        total_width = slot_count * slot_size + (slot_count - 1) * spacing
        start_x = x - total_width // 2

        self.x = start_x
        self.y = y

        # Create slots
        self.slots = []
        for i in range(slot_count):
            slot_x = start_x + i * (slot_size + spacing)
            slot = QuickInventorySlot(slot_x, y, slot_size, i)
            self.slots.append(slot)

        self.selected_index = 0

    def select_slot(self, index: int):
        """Select a slot by index."""
        if 0 <= index < self.slot_count:
            # Deselect old
            self.slots[self.selected_index].selected = False
            # Select new
            self.selected_index = index
            self.slots[self.selected_index].selected = True

    def set_slot_item(self, index: int, item_id: Optional[str], quantity: int = 0,
                      color: Tuple[int, int, int] = (128, 128, 128)):
        """Set item in a specific slot."""
        if 0 <= index < self.slot_count:
            self.slots[index].set_item(item_id, quantity, color)

    def clear_all(self):
        """Clear all slots."""
        for slot in self.slots:
            slot.clear()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events. Returns True if event was consumed."""
        if event.type == pygame.KEYDOWN:
            # Number keys 1-8 select slots
            if pygame.K_1 <= event.key <= pygame.K_8:
                index = event.key - pygame.K_1
                if index < self.slot_count:
                    self.select_slot(index)
                    return True

        elif event.type == pygame.MOUSEMOTION:
            # Update hover states
            for slot in self.slots:
                slot.hover = slot.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for i, slot in enumerate(self.slots):
                    if slot.rect.collidepoint(event.pos):
                        self.select_slot(i)
                        return True

        return False

    def draw(self, surface: pygame.Surface):
        """Draw the quick inventory bar."""
        # Draw semi-transparent background
        total_width = self.slot_count * self.slot_size + (self.slot_count - 1) * self.spacing + 16
        bg_rect = pygame.Rect(self.x - 8, self.y - 4, total_width, self.slot_size + 8)

        bg_surface = pygame.Surface((total_width, self.slot_size + 8), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (30, 28, 40, 180), bg_surface.get_rect(), border_radius=6)
        surface.blit(bg_surface, bg_rect)

        # Draw slots
        for slot in self.slots:
            slot.draw(surface)
