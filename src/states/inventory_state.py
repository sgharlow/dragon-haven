"""
Inventory State for Dragon Haven Cafe.
Screen for viewing and managing player inventory.
"""

import pygame
from typing import Optional, List, Tuple
from states.base_state import BaseScreen
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_PANEL, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM,
    INVENTORY_CARRIED_SLOTS, INVENTORY_STORAGE_SLOTS, INVENTORY_FRIDGE_SLOTS,
)
from systems.inventory import get_inventory, Inventory, ItemStack, Item
from ui.item_slot import ItemSlot, ItemSlotGrid
from ui.item_tooltip import ItemTooltip, ConfirmDialog
from ui.components import Button


class InventoryState(BaseScreen):
    """
    Inventory screen for managing items.

    Features:
    - Tab navigation (Carried, Storage, Fridge)
    - Grid display of items
    - Item details on click
    - Transfer between containers
    - Sort options
    - Discard with confirmation

    Usage:
        state = InventoryState(game)
        game.state_manager.push_state(state)
    """

    # Tab identifiers
    TAB_CARRIED = 'carried'
    TAB_STORAGE = 'storage'
    TAB_FRIDGE = 'fridge'

    # Sort options
    SORT_NAME = 'name'
    SORT_CATEGORY = 'category'
    SORT_QUALITY = 'quality'
    SORT_SPOIL = 'spoilage'

    # Grid configuration
    GRID_COLUMNS = 5
    GRID_ROWS = 4
    SLOT_SIZE = 52
    SLOT_SPACING = 6

    def __init__(self, game):
        """Initialize the inventory screen."""
        super().__init__(game)
        self.title = "Inventory"
        self.background_color = UI_BG

        # Get inventory
        self.inventory = get_inventory()

        # Current state
        self._current_tab = self.TAB_CARRIED
        self._current_sort = self.SORT_NAME
        self._selected_slot_index = -1

        # Calculate layout
        self._panel_width = 400
        self._panel_height = 450
        self._panel_x = (SCREEN_WIDTH - self._panel_width) // 2
        self._panel_y = 80

        # Tab buttons
        tab_y = self._panel_y + 10
        tab_width = 100
        tab_spacing = 10
        tabs_start_x = self._panel_x + 20

        self._tab_buttons = {
            self.TAB_CARRIED: pygame.Rect(tabs_start_x, tab_y, tab_width, 30),
            self.TAB_STORAGE: pygame.Rect(tabs_start_x + tab_width + tab_spacing, tab_y, tab_width, 30),
            self.TAB_FRIDGE: pygame.Rect(tabs_start_x + 2 * (tab_width + tab_spacing), tab_y, tab_width, 30),
        }

        # Item grid
        grid_x = self._panel_x + (self._panel_width - self.GRID_COLUMNS * (self.SLOT_SIZE + self.SLOT_SPACING)) // 2
        grid_y = self._panel_y + 60
        self._item_grid = ItemSlotGrid(
            grid_x, grid_y,
            self.GRID_COLUMNS, self.GRID_ROWS,
            self.SLOT_SIZE, self.SLOT_SPACING
        )

        # Action buttons
        button_y = self._panel_y + 320
        button_width = 80
        button_spacing = 15
        buttons_start_x = self._panel_x + 30

        self._transfer_button = Button(
            buttons_start_x, button_y, button_width, 32,
            "Transfer", self._on_transfer_click
        )
        self._sort_button = Button(
            buttons_start_x + button_width + button_spacing, button_y, button_width, 32,
            "Sort", self._on_sort_click
        )
        self._discard_button = Button(
            buttons_start_x + 2 * (button_width + button_spacing), button_y, button_width, 32,
            "Discard", self._on_discard_click
        )

        # Close button
        self._close_button = Button(
            self._panel_x + self._panel_width - 90, self._panel_y + self._panel_height - 50,
            70, 30, "Close", self._on_close_click
        )

        # Tooltip
        self._tooltip = ItemTooltip()

        # Confirm dialog
        self._confirm_dialog = ConfirmDialog(
            "Discard Item",
            "Are you sure you want to discard this item?"
        )

        # Sort options popup
        self._sort_popup_visible = False
        self._sort_popup_rect = pygame.Rect(
            buttons_start_x + button_width + button_spacing,
            button_y - 120, 100, 110
        )

        # Fonts
        self.title_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

    def enter(self, previous_state=None):
        """Enter the inventory screen."""
        super().enter(previous_state)
        self._update_grid()

    def _update_grid(self):
        """Update the item grid with current container."""
        container = self._get_current_container()
        self._item_grid.set_container(container)
        self._item_grid.clear_selection()
        self._selected_slot_index = -1

    def _get_current_container(self):
        """Get the current inventory container."""
        if self._current_tab == self.TAB_CARRIED:
            return self.inventory.carried
        elif self._current_tab == self.TAB_STORAGE:
            return self.inventory.storage
        elif self._current_tab == self.TAB_FRIDGE:
            return self.inventory.fridge
        return None

    def _get_container_info(self) -> Tuple[int, int, str]:
        """Get (used_slots, max_slots, name) for current container."""
        container = self._get_current_container()
        if not container:
            return (0, 0, "Unknown")

        if self._current_tab == self.TAB_CARRIED:
            return (container.get_used_slots(), INVENTORY_CARRIED_SLOTS, "Backpack")
        elif self._current_tab == self.TAB_STORAGE:
            return (container.get_used_slots(), INVENTORY_STORAGE_SLOTS, "Storage")
        elif self._current_tab == self.TAB_FRIDGE:
            return (container.get_used_slots(), INVENTORY_FRIDGE_SLOTS, "Fridge")
        return (0, 0, "Unknown")

    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        # Handle confirm dialog first
        if self._confirm_dialog.is_visible():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                result = self._confirm_dialog.handle_click(event.pos)
                if result == 'yes':
                    self._do_discard()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self._sort_popup_visible:
                    self._sort_popup_visible = False
                else:
                    self.fade_to_state('exploration')
                return

            if event.key == pygame.K_i:
                self.fade_to_state('exploration')
                return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_click(event.pos)

        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_move(event.pos)

    def _handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click."""
        # Sort popup
        if self._sort_popup_visible:
            sort_options = [
                (self.SORT_NAME, "Name"),
                (self.SORT_CATEGORY, "Category"),
                (self.SORT_QUALITY, "Quality"),
                (self.SORT_SPOIL, "Spoilage"),
            ]
            for i, (sort_id, _) in enumerate(sort_options):
                option_rect = pygame.Rect(
                    self._sort_popup_rect.x + 5,
                    self._sort_popup_rect.y + 5 + i * 26,
                    self._sort_popup_rect.width - 10, 24
                )
                if option_rect.collidepoint(pos):
                    self._current_sort = sort_id
                    self._sort_popup_visible = False
                    self._apply_sort()
                    return

            # Click outside closes popup
            if not self._sort_popup_rect.collidepoint(pos):
                self._sort_popup_visible = False
            return

        # Tab buttons
        for tab_id, rect in self._tab_buttons.items():
            if rect.collidepoint(pos):
                self._current_tab = tab_id
                self._update_grid()
                self._tooltip.hide()
                return

        # Item grid
        clicked_index = self._item_grid.handle_click(pos)
        if clicked_index >= 0:
            self._selected_slot_index = clicked_index
            # Show tooltip for selected item
            slot = self._item_grid.get_selected_slot()
            if slot and slot.get_item():
                self._tooltip.show(slot.get_item(), pos[0], pos[1])
            return

        # Action buttons
        if self._transfer_button.handle_click(pos):
            return
        if self._sort_button.handle_click(pos):
            return
        if self._discard_button.handle_click(pos):
            return
        if self._close_button.handle_click(pos):
            return

    def _handle_mouse_move(self, pos: Tuple[int, int]):
        """Handle mouse movement."""
        self._item_grid.update(pos)

        # Update button hover states
        for tab_id, rect in self._tab_buttons.items():
            pass  # Tab buttons handled visually

    def _on_transfer_click(self):
        """Handle transfer button click."""
        if self._selected_slot_index < 0:
            return

        container = self._get_current_container()
        if not container:
            return

        stack = container.get_slot(self._selected_slot_index)
        if not stack:
            return

        # Transfer based on current tab
        item_id = stack.item.id
        if self._current_tab == self.TAB_CARRIED:
            # Transfer to storage
            self.inventory.transfer_to_storage(item_id, stack.quantity)
        else:
            # Transfer to carried
            from_fridge = (self._current_tab == self.TAB_FRIDGE)
            self.inventory.transfer_from_storage(item_id, stack.quantity, from_fridge)

        self._update_grid()
        self._tooltip.hide()

    def _on_sort_click(self):
        """Handle sort button click."""
        self._sort_popup_visible = not self._sort_popup_visible

    def _apply_sort(self):
        """Apply current sort to the container."""
        container = self._get_current_container()
        if not container:
            return

        # Get all non-None slots
        items = [(i, slot) for i, slot in enumerate(container.slots) if slot is not None]

        # Sort based on current sort option
        if self._current_sort == self.SORT_NAME:
            items.sort(key=lambda x: x[1].item.name)
        elif self._current_sort == self.SORT_CATEGORY:
            items.sort(key=lambda x: x[1].item.category)
        elif self._current_sort == self.SORT_QUALITY:
            items.sort(key=lambda x: x[1].item.quality, reverse=True)
        elif self._current_sort == self.SORT_SPOIL:
            items.sort(key=lambda x: (x[1].item.spoil_days == 0, x[1].days_until_spoil))

        # Rearrange slots
        new_slots = [None] * container.max_slots
        for new_idx, (_, slot) in enumerate(items):
            if new_idx < container.max_slots:
                new_slots[new_idx] = slot
        container.slots = new_slots

        self._update_grid()

    def _on_discard_click(self):
        """Handle discard button click."""
        if self._selected_slot_index < 0:
            return

        container = self._get_current_container()
        if not container:
            return

        stack = container.get_slot(self._selected_slot_index)
        if not stack:
            return

        # Show confirmation dialog
        self._confirm_dialog.show()

    def _do_discard(self):
        """Actually discard the selected item."""
        container = self._get_current_container()
        if not container or self._selected_slot_index < 0:
            return

        # Remove the item
        container.slots[self._selected_slot_index] = None
        self._update_grid()
        self._tooltip.hide()

    def _on_close_click(self):
        """Handle close button click."""
        self.fade_to_state('exploration')

    def update(self, dt: float) -> bool:
        """Update the inventory screen."""
        super().update(dt)
        self._tooltip.update(dt)
        return True

    def draw(self, screen: pygame.Surface):
        """Draw the inventory screen."""
        # Draw background
        screen.fill(self.background_color)

        # Draw main panel
        panel_rect = pygame.Rect(self._panel_x, self._panel_y,
                                self._panel_width, self._panel_height)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Draw title
        title_surface = self.title_font.render("Inventory", True, CAFE_CREAM)
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 30))

        # Draw tabs
        for tab_id, rect in self._tab_buttons.items():
            is_active = (tab_id == self._current_tab)
            bg_color = UI_HIGHLIGHT if is_active else UI_PANEL
            border_color = CAFE_WARM if is_active else UI_BORDER

            pygame.draw.rect(screen, bg_color, rect, border_radius=4)
            pygame.draw.rect(screen, border_color, rect, 2, border_radius=4)

            tab_names = {
                self.TAB_CARRIED: "Backpack",
                self.TAB_STORAGE: "Storage",
                self.TAB_FRIDGE: "Fridge",
            }
            text_color = CAFE_CREAM if is_active else UI_TEXT_DIM
            tab_text = self.small_font.render(tab_names[tab_id], True, text_color)
            text_rect = tab_text.get_rect(center=rect.center)
            screen.blit(tab_text, text_rect)

        # Draw item grid
        self._item_grid.draw(screen)

        # Draw slot count
        used, max_slots, name = self._get_container_info()
        count_text = f"{used}/{max_slots} slots used"
        count_surface = self.small_font.render(count_text, True, UI_TEXT_DIM)
        screen.blit(count_surface, (self._panel_x + 20, self._panel_y + 290))

        # Draw gold
        gold_text = f"Gold: {self.inventory.gold}"
        gold_surface = self.text_font.render(gold_text, True, (220, 180, 60))
        screen.blit(gold_surface, (self._panel_x + self._panel_width - 120, self._panel_y + 290))

        # Draw action buttons
        self._transfer_button.draw(screen)
        self._sort_button.draw(screen)
        self._discard_button.draw(screen)
        self._close_button.draw(screen)

        # Draw selected item info
        if self._selected_slot_index >= 0:
            container = self._get_current_container()
            if container:
                stack = container.get_slot(self._selected_slot_index)
                if stack:
                    info_y = self._panel_y + 365
                    name_surface = self.text_font.render(stack.item.name, True, CAFE_CREAM)
                    screen.blit(name_surface, (self._panel_x + 20, info_y))

                    qty_text = f"x{stack.quantity}"
                    qty_surface = self.small_font.render(qty_text, True, UI_TEXT_DIM)
                    screen.blit(qty_surface, (self._panel_x + 20 + name_surface.get_width() + 10, info_y + 3))

        # Draw sort popup
        if self._sort_popup_visible:
            self._draw_sort_popup(screen)

        # Draw tooltip
        self._tooltip.draw(screen)

        # Draw confirm dialog
        self._confirm_dialog.draw(screen)

        # Draw controls hint
        hint_text = "I: Close  |  Click item for details  |  ESC: Back"
        hint_surface = self.small_font.render(hint_text, True, UI_TEXT_DIM)
        screen.blit(hint_surface, (SCREEN_WIDTH // 2 - hint_surface.get_width() // 2,
                                  SCREEN_HEIGHT - 30))

        # Draw fade overlay
        self.draw_fade_overlay(screen)

    def _draw_sort_popup(self, screen: pygame.Surface):
        """Draw the sort options popup."""
        # Background
        pygame.draw.rect(screen, UI_PANEL, self._sort_popup_rect, border_radius=4)
        pygame.draw.rect(screen, UI_BORDER, self._sort_popup_rect, 1, border_radius=4)

        sort_options = [
            (self.SORT_NAME, "Name"),
            (self.SORT_CATEGORY, "Category"),
            (self.SORT_QUALITY, "Quality"),
            (self.SORT_SPOIL, "Spoilage"),
        ]

        for i, (sort_id, label) in enumerate(sort_options):
            option_rect = pygame.Rect(
                self._sort_popup_rect.x + 5,
                self._sort_popup_rect.y + 5 + i * 26,
                self._sort_popup_rect.width - 10, 24
            )

            is_active = (sort_id == self._current_sort)
            if is_active:
                pygame.draw.rect(screen, UI_HIGHLIGHT, option_rect, border_radius=2)

            text_color = CAFE_CREAM if is_active else UI_TEXT
            text_surface = self.small_font.render(label, True, text_color)
            screen.blit(text_surface, (option_rect.x + 8, option_rect.y + 4))
