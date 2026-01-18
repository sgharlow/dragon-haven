"""
Recipe Book State for Dragon Haven Cafe.
Displays discovered recipes with details, ingredients, and mastery progress.
"""

import pygame
from typing import Optional, List
from states.base_state import BaseScreen
from systems.recipes import get_recipe_manager, Recipe
from systems.inventory import get_inventory
from ui.recipe_card import RecipeCard, RecipeDetailPanel
from ui.components import Button
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM, BLACK,
    ALL_RECIPE_CATEGORIES,
    RECIPE_CATEGORY_APPETIZER, RECIPE_CATEGORY_MAIN,
    RECIPE_CATEGORY_DESSERT, RECIPE_CATEGORY_BEVERAGE,
)


class RecipeBookState(BaseScreen):
    """
    Recipe book screen showing all discovered recipes.

    Features:
    - Category tabs
    - Recipe list with icons
    - Detailed recipe view
    - Mastery progress
    - Filter by cookable/mastered
    """

    # Tab categories
    TAB_ALL = 'all'
    TAB_APPETIZER = RECIPE_CATEGORY_APPETIZER
    TAB_MAIN = RECIPE_CATEGORY_MAIN
    TAB_DESSERT = RECIPE_CATEGORY_DESSERT
    TAB_BEVERAGE = RECIPE_CATEGORY_BEVERAGE

    TABS = [
        (TAB_ALL, "All"),
        (TAB_APPETIZER, "Appetizers"),
        (TAB_MAIN, "Mains"),
        (TAB_DESSERT, "Desserts"),
        (TAB_BEVERAGE, "Beverages"),
    ]

    # Filter options
    FILTER_ALL = 'all'
    FILTER_CAN_COOK = 'can_cook'
    FILTER_MASTERED = 'mastered'

    FILTERS = [
        (FILTER_ALL, "All"),
        (FILTER_CAN_COOK, "Can Cook"),
        (FILTER_MASTERED, "Mastered"),
    ]

    def __init__(self, game):
        """Initialize the recipe book state."""
        super().__init__(game)
        self.title = "Recipe Book"

        # Get systems
        self.recipe_manager = get_recipe_manager()
        self.inventory = get_inventory()

        # Current selections
        self._current_tab = self.TAB_ALL
        self._current_filter = self.FILTER_ALL
        self._selected_index = -1
        self._scroll_offset = 0

        # UI components (initialized in enter)
        self._recipe_cards: List[RecipeCard] = []
        self._detail_panel: Optional[RecipeDetailPanel] = None
        self._tab_buttons: List[Button] = []
        self._filter_buttons: List[Button] = []
        self._close_button: Optional[Button] = None

        # Layout
        self._list_x = 50
        self._list_y = 130
        self._list_width = 350
        self._list_height = 500

        self._detail_x = 420
        self._detail_y = 130
        self._detail_width = 400
        self._detail_height = 500

        # Fonts
        self._tab_font = None
        self._filter_font = None

    def enter(self, previous_state=None):
        """Initialize UI when entering state."""
        super().enter(previous_state)

        # Initialize fonts
        self._tab_font = pygame.font.Font(None, 22)
        self._filter_font = pygame.font.Font(None, 20)

        # Create tab buttons
        self._create_tab_buttons()

        # Create filter buttons
        self._create_filter_buttons()

        # Create detail panel
        self._detail_panel = RecipeDetailPanel(
            self._detail_x, self._detail_y,
            self._detail_width, self._detail_height
        )

        # Create close button
        self._close_button = Button(
            SCREEN_WIDTH - 110, 20, 90, 35, "Close", self._on_close
        )

        # Load recipes
        self._refresh_recipe_list()

    def _create_tab_buttons(self):
        """Create category tab buttons."""
        self._tab_buttons = []
        x = self._list_x
        for tab_id, tab_name in self.TABS:
            width = max(70, len(tab_name) * 10 + 20)
            btn = Button(x, 85, width, 30, tab_name,
                        lambda t=tab_id: self._on_tab_select(t))
            self._tab_buttons.append((tab_id, btn))
            x += width + 5

    def _create_filter_buttons(self):
        """Create filter buttons."""
        self._filter_buttons = []
        x = self._detail_x
        for filter_id, filter_name in self.FILTERS:
            width = max(60, len(filter_name) * 9 + 15)
            btn = Button(x, 85, width, 30, filter_name,
                        lambda f=filter_id: self._on_filter_select(f))
            self._filter_buttons.append((filter_id, btn))
            x += width + 5

    def _refresh_recipe_list(self):
        """Refresh the list of recipes based on current tab and filter."""
        self._recipe_cards = []
        self._selected_index = -1

        # Get all recipes
        if self._current_tab == self.TAB_ALL:
            all_recipes = self.recipe_manager.get_all_recipes()
        else:
            all_recipes = self.recipe_manager.get_recipes_by_category(self._current_tab)

        # Build card list
        card_y = self._list_y
        card_index = 0

        for recipe in all_recipes:
            is_unlocked = self.recipe_manager.is_unlocked(recipe.id)

            # Apply filter
            if self._current_filter == self.FILTER_CAN_COOK:
                if not is_unlocked:
                    continue
                result = self.recipe_manager.can_cook(recipe.id, self.inventory)
                if not result.get('can_cook', False):
                    continue
            elif self._current_filter == self.FILTER_MASTERED:
                if not self.recipe_manager.is_mastered(recipe.id):
                    continue

            # Create card
            card = RecipeCard(
                self._list_x, card_y, self._list_width,
                recipe, is_unlocked, card_index
            )

            # Set status indicators
            if is_unlocked:
                result = self.recipe_manager.can_cook(recipe.id, self.inventory)
                card.can_cook = result.get('can_cook', False)
                card.is_mastered = self.recipe_manager.is_mastered(recipe.id)

            self._recipe_cards.append(card)
            card_y += 65
            card_index += 1

        # Update detail panel
        self._update_detail_panel()

    def _update_detail_panel(self):
        """Update detail panel with selected recipe."""
        if 0 <= self._selected_index < len(self._recipe_cards):
            card = self._recipe_cards[self._selected_index]
            if card.is_unlocked and card.recipe:
                mastery = self.recipe_manager.get_mastery(card.recipe.id)
                can_cook_result = self.recipe_manager.can_cook(
                    card.recipe.id, self.inventory
                )
                self._detail_panel.set_recipe(
                    card.recipe, mastery, can_cook_result, self.inventory
                )
            else:
                self._detail_panel.set_recipe(None)
        else:
            self._detail_panel.set_recipe(None)

    def _on_tab_select(self, tab_id: str):
        """Handle tab selection."""
        self._current_tab = tab_id
        self._scroll_offset = 0
        self._refresh_recipe_list()

    def _on_filter_select(self, filter_id: str):
        """Handle filter selection."""
        self._current_filter = filter_id
        self._scroll_offset = 0
        self._refresh_recipe_list()

    def _on_close(self):
        """Handle close button."""
        self.fade_to_state('gameplay')

    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_close()
                return

            # Arrow key navigation
            if event.key == pygame.K_UP:
                if self._selected_index > 0:
                    self._recipe_cards[self._selected_index].selected = False
                    self._selected_index -= 1
                    self._recipe_cards[self._selected_index].selected = True
                    self._update_detail_panel()
            elif event.key == pygame.K_DOWN:
                if self._selected_index < len(self._recipe_cards) - 1:
                    if self._selected_index >= 0:
                        self._recipe_cards[self._selected_index].selected = False
                    self._selected_index += 1
                    self._recipe_cards[self._selected_index].selected = True
                    self._update_detail_panel()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = event.pos

                # Check tab buttons
                for tab_id, btn in self._tab_buttons:
                    if btn.rect.collidepoint(pos):
                        self._on_tab_select(tab_id)
                        return

                # Check filter buttons
                for filter_id, btn in self._filter_buttons:
                    if btn.rect.collidepoint(pos):
                        self._on_filter_select(filter_id)
                        return

                # Check close button
                if self._close_button and self._close_button.rect.collidepoint(pos):
                    self._on_close()
                    return

                # Check recipe cards
                for i, card in enumerate(self._recipe_cards):
                    if card.contains_point(pos):
                        # Deselect previous
                        if self._selected_index >= 0:
                            self._recipe_cards[self._selected_index].selected = False
                        # Select new
                        self._selected_index = i
                        card.selected = True
                        self._update_detail_panel()
                        return

            elif event.button == 4:  # Scroll up
                self._scroll_offset = max(0, self._scroll_offset - 1)
                self._update_card_positions()
            elif event.button == 5:  # Scroll down
                max_scroll = max(0, len(self._recipe_cards) - 7)
                self._scroll_offset = min(max_scroll, self._scroll_offset + 1)
                self._update_card_positions()

    def _update_card_positions(self):
        """Update card positions based on scroll."""
        for i, card in enumerate(self._recipe_cards):
            card_y = self._list_y + (i - self._scroll_offset) * 65
            card.set_position(self._list_x, card_y)

    def update(self, dt):
        """Update state."""
        super().update(dt)

        # Update hover states
        mouse_pos = pygame.mouse.get_pos()
        for card in self._recipe_cards:
            card.update_hover(mouse_pos)

        return True

    def draw(self, screen):
        """Draw the recipe book."""
        super().draw(screen)

        # Draw tabs
        self._draw_tabs(screen)

        # Draw filters
        self._draw_filters(screen)

        # Draw recipe list area
        list_rect = pygame.Rect(self._list_x - 5, self._list_y - 5,
                               self._list_width + 10, self._list_height + 10)
        pygame.draw.rect(screen, (35, 30, 45), list_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, list_rect, 2, border_radius=8)

        # Draw recipes (with clipping)
        clip_rect = pygame.Rect(self._list_x, self._list_y,
                               self._list_width, self._list_height)
        screen.set_clip(clip_rect)
        for card in self._recipe_cards:
            if self._list_y - 70 < card.y < self._list_y + self._list_height:
                card.draw(screen)
        screen.set_clip(None)

        # Draw recipe count
        count_text = f"{len(self._recipe_cards)} recipes"
        count_surface = self._filter_font.render(count_text, True, UI_TEXT_DIM)
        screen.blit(count_surface,
                   (self._list_x, self._list_y + self._list_height + 15))

        # Draw scroll indicator if needed
        if len(self._recipe_cards) > 7:
            self._draw_scroll_indicator(screen)

        # Draw detail panel
        if self._detail_panel:
            self._detail_panel.draw(screen)

        # Draw close button
        if self._close_button:
            self._close_button.draw(screen)

        # Draw fade overlay
        self.draw_fade_overlay(screen)

    def _draw_tabs(self, screen):
        """Draw category tabs."""
        for tab_id, btn in self._tab_buttons:
            # Highlight active tab
            is_active = (tab_id == self._current_tab)
            if is_active:
                pygame.draw.rect(screen, (80, 70, 100), btn.rect, border_radius=4)
            else:
                pygame.draw.rect(screen, UI_PANEL, btn.rect, border_radius=4)
            pygame.draw.rect(screen, UI_BORDER, btn.rect, 1, border_radius=4)

            # Draw text
            text_color = CAFE_CREAM if is_active else UI_TEXT
            text_surface = self._tab_font.render(btn.text, True, text_color)
            text_rect = text_surface.get_rect(center=btn.rect.center)
            screen.blit(text_surface, text_rect)

    def _draw_filters(self, screen):
        """Draw filter buttons."""
        # Label
        label = self._filter_font.render("Filter:", True, UI_TEXT_DIM)
        screen.blit(label, (self._detail_x, 70))

        for filter_id, btn in self._filter_buttons:
            # Highlight active filter
            is_active = (filter_id == self._current_filter)
            if is_active:
                pygame.draw.rect(screen, (70, 100, 70), btn.rect, border_radius=4)
            else:
                pygame.draw.rect(screen, UI_PANEL, btn.rect, border_radius=4)
            pygame.draw.rect(screen, UI_BORDER, btn.rect, 1, border_radius=4)

            # Draw text
            text_color = CAFE_CREAM if is_active else UI_TEXT
            text_surface = self._filter_font.render(btn.text, True, text_color)
            text_rect = text_surface.get_rect(center=btn.rect.center)
            screen.blit(text_surface, text_rect)

    def _draw_scroll_indicator(self, screen):
        """Draw scroll position indicator."""
        total = len(self._recipe_cards)
        visible = 7
        if total <= visible:
            return

        # Scrollbar track
        track_x = self._list_x + self._list_width + 5
        track_y = self._list_y
        track_height = self._list_height
        pygame.draw.rect(screen, (50, 45, 60),
                        (track_x, track_y, 8, track_height), border_radius=4)

        # Scrollbar thumb
        thumb_height = max(30, track_height * visible / total)
        thumb_y = track_y + (track_height - thumb_height) * self._scroll_offset / (total - visible)
        pygame.draw.rect(screen, UI_BORDER,
                        (track_x, int(thumb_y), 8, int(thumb_height)), border_radius=4)
