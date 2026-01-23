"""
Dragon Customization State for Dragon Haven Cafe.
Allows players to view unlocked customizations and equip them on their dragon.
Phase 4 Feature.
"""

import pygame
from typing import Optional, List, Tuple
from states.base_state import BaseScreen
from ui.components import Button
from systems.customization import (
    get_customization_manager, CustomizationSlot, CustomizationType,
    CustomizationItem, ALL_CUSTOMIZATIONS, ACCESSORIES, PATTERNS, EFFECTS
)
from systems.dragon_manager import get_dragon_manager
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM, UI_HIGHLIGHT,
    CAFE_CREAM, CAFE_WARM, BLACK, WHITE, GRAY,
    DRAGON_STAGE_EGG,
)


class CustomizationState(BaseScreen):
    """
    Dragon customization screen for equipping accessories, patterns, and effects.

    Features:
    - Dragon preview with equipped items
    - Tab navigation (Accessories, Patterns, Effects)
    - Item grid showing unlocked items
    - Equip/Unequip functionality
    - Item descriptions and unlock requirements
    """

    # Layout constants
    PREVIEW_X = 200
    PREVIEW_Y = 200
    PREVIEW_SIZE = 180

    PANEL_X = 450
    PANEL_Y = 80
    PANEL_WIDTH = 780
    PANEL_HEIGHT = 560

    TAB_HEIGHT = 40
    ITEM_SIZE = 80
    ITEMS_PER_ROW = 6

    def __init__(self, game):
        """Initialize the customization state."""
        super().__init__(game)
        self.title = "Dragon Customization"

        # Managers
        self._customization_mgr = None
        self._dragon_mgr = None

        # UI state
        self._active_tab = 0  # 0=Accessories, 1=Patterns, 2=Effects
        self._selected_item: Optional[str] = None
        self._hover_item: Optional[str] = None
        self._animation_time = 0.0

        # Tab definitions
        self._tabs = [
            ("Accessories", CustomizationType.ACCESSORY),
            ("Patterns", CustomizationType.PATTERN),
            ("Effects", CustomizationType.EFFECT),
        ]

        # UI components
        self._tab_buttons: List[Button] = []
        self._item_buttons: List[Tuple[pygame.Rect, str]] = []
        self._equip_button: Optional[Button] = None
        self._unequip_button: Optional[Button] = None
        self._close_button: Optional[Button] = None

        # Fonts
        self._title_font = None
        self._tab_font = None
        self._item_font = None
        self._desc_font = None
        self._small_font = None

    def enter(self, previous_state=None):
        """Initialize when entering state."""
        super().enter(previous_state)

        # Get managers
        self._customization_mgr = get_customization_manager()
        self._dragon_mgr = get_dragon_manager()

        # Initialize fonts
        self._title_font = pygame.font.Font(None, 36)
        self._tab_font = pygame.font.Font(None, 26)
        self._item_font = pygame.font.Font(None, 20)
        self._desc_font = pygame.font.Font(None, 22)
        self._small_font = pygame.font.Font(None, 18)

        # Create close button
        self._close_button = Button(
            SCREEN_WIDTH - 120, 20, 100, 35, "Close",
            callback=self._on_close
        )

        # Create tab buttons
        self._create_tab_buttons()

        # Create action buttons
        btn_y = self.PANEL_Y + self.PANEL_HEIGHT - 50
        self._equip_button = Button(
            self.PANEL_X + 200, btn_y, 120, 35, "Equip",
            callback=self._on_equip
        )
        self._unequip_button = Button(
            self.PANEL_X + 340, btn_y, 120, 35, "Unequip",
            callback=self._on_unequip
        )

    def _create_tab_buttons(self):
        """Create tab navigation buttons."""
        self._tab_buttons = []
        tab_width = self.PANEL_WIDTH // len(self._tabs)

        for i, (label, _) in enumerate(self._tabs):
            btn = Button(
                self.PANEL_X + i * tab_width, self.PANEL_Y,
                tab_width, self.TAB_HEIGHT, label,
                callback=lambda idx=i: self._set_tab(idx)
            )
            self._tab_buttons.append(btn)

    def _set_tab(self, index: int):
        """Switch to a different tab."""
        self._active_tab = index
        self._selected_item = None
        self._hover_item = None

    def _on_close(self):
        """Handle close button."""
        self.transition_to('dragon_status')

    def _on_equip(self):
        """Handle equip button."""
        if self._selected_item:
            self._customization_mgr.equip_item(self._selected_item)

    def _on_unequip(self):
        """Handle unequip button."""
        if self._selected_item:
            item = ALL_CUSTOMIZATIONS.get(self._selected_item)
            if item:
                if item.item_type == CustomizationType.PATTERN:
                    self._customization_mgr.get_customization().unequip_pattern()
                else:
                    self._customization_mgr.unequip_slot(item.slot)

    def handle_event(self, event):
        """Process input events."""
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check close button
                if self._close_button and self._close_button.rect.collidepoint(event.pos):
                    self._close_button.callback()
                    return

                # Check tab buttons
                for i, btn in enumerate(self._tab_buttons):
                    if btn.rect.collidepoint(event.pos):
                        self._set_tab(i)
                        return

                # Check item grid
                for rect, item_id in self._item_buttons:
                    if rect.collidepoint(event.pos):
                        self._selected_item = item_id
                        return

                # Check action buttons
                if self._equip_button and self._equip_button.rect.collidepoint(event.pos):
                    self._on_equip()
                    return
                if self._unequip_button and self._unequip_button.rect.collidepoint(event.pos):
                    self._on_unequip()
                    return

        elif event.type == pygame.MOUSEMOTION:
            # Update hover state
            self._hover_item = None
            for rect, item_id in self._item_buttons:
                if rect.collidepoint(event.pos):
                    self._hover_item = item_id
                    break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_close()

    def update(self, dt: float):
        """Update state."""
        super().update(dt)
        self._animation_time += dt

    def draw(self, screen: pygame.Surface):
        """Render the customization screen."""
        # Background
        screen.fill(UI_PANEL)

        # Draw title
        title = self._title_font.render("Dragon Customization", True, UI_TEXT)
        screen.blit(title, (50, 30))

        # Draw dragon preview
        self._draw_dragon_preview(screen)

        # Draw main panel
        self._draw_panel(screen)

        # Draw tabs
        self._draw_tabs(screen)

        # Draw item grid
        self._draw_item_grid(screen)

        # Draw selected item info
        self._draw_item_info(screen)

        # Draw buttons
        if self._close_button:
            self._draw_button(screen, self._close_button)

        # Draw action buttons if item selected
        if self._selected_item:
            if self._equip_button:
                self._draw_button(screen, self._equip_button)
            if self._unequip_button:
                self._draw_button(screen, self._unequip_button)

    def _draw_button(self, screen: pygame.Surface, button: Button):
        """Draw a button."""
        color = UI_HIGHLIGHT if button.rect.collidepoint(pygame.mouse.get_pos()) else UI_BORDER
        pygame.draw.rect(screen, color, button.rect)
        pygame.draw.rect(screen, UI_TEXT, button.rect, 2)

        text = self._tab_font.render(button.text, True, UI_TEXT)
        text_rect = text.get_rect(center=button.rect.center)
        screen.blit(text, text_rect)

    def _draw_dragon_preview(self, screen: pygame.Surface):
        """Draw the dragon preview with equipped items."""
        # Preview background
        preview_rect = pygame.Rect(
            self.PREVIEW_X - self.PREVIEW_SIZE // 2,
            self.PREVIEW_Y - self.PREVIEW_SIZE // 2,
            self.PREVIEW_SIZE, self.PREVIEW_SIZE
        )
        pygame.draw.rect(screen, CAFE_CREAM, preview_rect, border_radius=10)
        pygame.draw.rect(screen, UI_BORDER, preview_rect, 3, border_radius=10)

        # Draw dragon (simplified)
        dragon = self._dragon_mgr.get_dragon() if self._dragon_mgr else None
        if dragon and dragon.get_stage() != DRAGON_STAGE_EGG:
            # Draw dragon body (circle)
            dragon_color = (100, 180, 140)  # Base green
            pygame.draw.circle(screen, dragon_color,
                             (self.PREVIEW_X, self.PREVIEW_Y), 60)

            # Draw equipped accessories indicators
            customization = self._customization_mgr.get_customization()

            # Draw neck item indicator
            if customization.equipped.get('neck'):
                pygame.draw.circle(screen, (200, 60, 60),
                                 (self.PREVIEW_X, self.PREVIEW_Y + 40), 15)

            # Draw head item indicator
            if customization.equipped.get('head'):
                pygame.draw.rect(screen, (255, 255, 255),
                               (self.PREVIEW_X - 20, self.PREVIEW_Y - 80, 40, 30))

            # Draw pattern indicator
            if customization.active_pattern:
                pattern = ALL_CUSTOMIZATIONS.get(customization.active_pattern)
                if pattern and pattern.visual_data.get('pattern_type') == 'spots':
                    # Draw spots
                    for offset in [(-20, -10), (15, 5), (-5, 25)]:
                        pygame.draw.circle(screen, (80, 140, 110),
                                         (self.PREVIEW_X + offset[0],
                                          self.PREVIEW_Y + offset[1]), 8)
        else:
            # Dragon not available or is egg
            text = self._desc_font.render("Dragon", True, UI_TEXT_DIM)
            text_rect = text.get_rect(center=(self.PREVIEW_X, self.PREVIEW_Y))
            screen.blit(text, text_rect)

        # Label
        label = self._small_font.render("Preview", True, UI_TEXT_DIM)
        screen.blit(label, (self.PREVIEW_X - 25, self.PREVIEW_Y + self.PREVIEW_SIZE // 2 + 10))

    def _draw_panel(self, screen: pygame.Surface):
        """Draw the main panel background."""
        panel_rect = pygame.Rect(
            self.PANEL_X, self.PANEL_Y,
            self.PANEL_WIDTH, self.PANEL_HEIGHT
        )
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=5)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=5)

    def _draw_tabs(self, screen: pygame.Surface):
        """Draw tab buttons."""
        for i, btn in enumerate(self._tab_buttons):
            is_active = i == self._active_tab
            color = UI_HIGHLIGHT if is_active else UI_BORDER

            pygame.draw.rect(screen, color, btn.rect)
            if is_active:
                # Draw bottom border to connect to panel
                pygame.draw.line(screen, color,
                               (btn.rect.left, btn.rect.bottom),
                               (btn.rect.right, btn.rect.bottom), 2)

            pygame.draw.rect(screen, UI_TEXT, btn.rect, 2)

            text = self._tab_font.render(btn.text, True, UI_TEXT)
            text_rect = text.get_rect(center=btn.rect.center)
            screen.blit(text, text_rect)

    def _draw_item_grid(self, screen: pygame.Surface):
        """Draw the grid of customization items."""
        self._item_buttons = []

        # Get items for current tab
        _, item_type = self._tabs[self._active_tab]
        customization = self._customization_mgr.get_customization()

        # Get all items of this type
        all_items = [item for item in ALL_CUSTOMIZATIONS.values()
                    if item.item_type == item_type]

        # Grid layout
        grid_x = self.PANEL_X + 20
        grid_y = self.PANEL_Y + self.TAB_HEIGHT + 20
        spacing = 10

        for i, item in enumerate(all_items):
            row = i // self.ITEMS_PER_ROW
            col = i % self.ITEMS_PER_ROW

            x = grid_x + col * (self.ITEM_SIZE + spacing)
            y = grid_y + row * (self.ITEM_SIZE + spacing)

            rect = pygame.Rect(x, y, self.ITEM_SIZE, self.ITEM_SIZE)
            self._item_buttons.append((rect, item.item_id))

            # Determine item state
            is_unlocked = customization.is_unlocked(item.item_id)
            is_equipped = (
                item.item_id == customization.equipped.get(item.slot.value) or
                item.item_id == customization.active_pattern
            )
            is_selected = item.item_id == self._selected_item
            is_hovered = item.item_id == self._hover_item

            # Draw item box
            if is_equipped:
                bg_color = (80, 140, 80)  # Green for equipped
            elif is_selected:
                bg_color = UI_HIGHLIGHT
            elif is_hovered and is_unlocked:
                bg_color = (80, 75, 95)
            elif is_unlocked:
                bg_color = UI_BORDER
            else:
                bg_color = (50, 45, 55)  # Darker for locked

            pygame.draw.rect(screen, bg_color, rect, border_radius=5)
            pygame.draw.rect(screen, UI_TEXT if is_unlocked else UI_TEXT_DIM,
                           rect, 2, border_radius=5)

            # Draw item icon (simplified - colored square)
            if is_unlocked:
                icon_color = item.visual_data.get('color', (150, 150, 150))
                if isinstance(icon_color, tuple) and len(icon_color) == 3:
                    icon_rect = pygame.Rect(x + 15, y + 15, 50, 50)
                    pygame.draw.rect(screen, icon_color, icon_rect, border_radius=3)
            else:
                # Locked indicator
                lock_text = self._small_font.render("?", True, UI_TEXT_DIM)
                lock_rect = lock_text.get_rect(center=rect.center)
                screen.blit(lock_text, lock_rect)

            # Draw equipped indicator
            if is_equipped:
                indicator = self._small_font.render("E", True, WHITE)
                screen.blit(indicator, (x + 5, y + 5))

    def _draw_item_info(self, screen: pygame.Surface):
        """Draw information about the selected item."""
        info_y = self.PANEL_Y + self.PANEL_HEIGHT - 150

        item_id = self._selected_item or self._hover_item
        if not item_id:
            # No item selected
            hint = self._desc_font.render("Select an item to view details", True, UI_TEXT_DIM)
            screen.blit(hint, (self.PANEL_X + 20, info_y))
            return

        item = ALL_CUSTOMIZATIONS.get(item_id)
        if not item:
            return

        customization = self._customization_mgr.get_customization()
        is_unlocked = customization.is_unlocked(item_id)

        # Item name
        name_color = UI_TEXT if is_unlocked else UI_TEXT_DIM
        name = self._tab_font.render(item.name, True, name_color)
        screen.blit(name, (self.PANEL_X + 20, info_y))

        # Item description
        if is_unlocked:
            desc = self._desc_font.render(item.description, True, UI_TEXT)
        else:
            # Show unlock condition
            cond = item.unlock_condition
            cond_type = cond.get('type', 'unknown')
            value = cond.get('value', '?')
            unlock_text = f"Unlock: {cond_type} - {value}"
            desc = self._desc_font.render(unlock_text, True, UI_TEXT_DIM)

        screen.blit(desc, (self.PANEL_X + 20, info_y + 30))

        # Slot info
        slot_text = f"Slot: {item.slot.value.title()}"
        slot = self._small_font.render(slot_text, True, UI_TEXT_DIM)
        screen.blit(slot, (self.PANEL_X + 20, info_y + 55))

        # Equipped status
        is_equipped = (
            item_id == customization.equipped.get(item.slot.value) or
            item_id == customization.active_pattern
        )
        if is_equipped:
            status = self._small_font.render("Currently Equipped", True, (80, 200, 80))
            screen.blit(status, (self.PANEL_X + 150, info_y + 55))
