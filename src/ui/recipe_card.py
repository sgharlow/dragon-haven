"""
Recipe Card UI Component for Dragon Haven Cafe.
Displays a recipe in a list with icon, name, and status indicators.
"""

import pygame
from typing import Optional, Tuple
from constants import (
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM, BLACK,
    RECIPE_CATEGORY_APPETIZER, RECIPE_CATEGORY_MAIN,
    RECIPE_CATEGORY_DESSERT, RECIPE_CATEGORY_BEVERAGE,
)


class RecipeCard:
    """
    A compact card displaying a recipe in a list.

    Usage:
        card = RecipeCard(x, y, 300, recipe, is_unlocked=True)
        card.draw(surface)
    """

    # Category colors for recipe icons
    CATEGORY_COLORS = {
        RECIPE_CATEGORY_APPETIZER: (180, 200, 120),  # Light green
        RECIPE_CATEGORY_MAIN: (200, 140, 100),       # Warm brown
        RECIPE_CATEGORY_DESSERT: (220, 180, 200),    # Pink
        RECIPE_CATEGORY_BEVERAGE: (140, 180, 220),   # Blue
    }

    # Category icons (simple shapes)
    CATEGORY_ICONS = {
        RECIPE_CATEGORY_APPETIZER: 'leaf',
        RECIPE_CATEGORY_MAIN: 'plate',
        RECIPE_CATEGORY_DESSERT: 'cake',
        RECIPE_CATEGORY_BEVERAGE: 'cup',
    }

    def __init__(self, x: int, y: int, width: int, recipe,
                 is_unlocked: bool = True, index: int = 0):
        """
        Initialize a recipe card.

        Args:
            x, y: Position
            width: Card width
            recipe: Recipe object (or None for locked)
            is_unlocked: Whether recipe is unlocked
            index: Index in list for selection
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = 60
        self.recipe = recipe
        self.is_unlocked = is_unlocked
        self.index = index

        self.rect = pygame.Rect(x, y, width, self.height)

        # State
        self.selected = False
        self.hover = False
        self.can_cook = False
        self.is_mastered = False

        # Fonts
        self.name_font = pygame.font.Font(None, 24)
        self.detail_font = pygame.font.Font(None, 18)

    def set_position(self, x: int, y: int):
        """Update card position."""
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def contains_point(self, pos: Tuple[int, int]) -> bool:
        """Check if point is inside card."""
        return self.rect.collidepoint(pos)

    def update_hover(self, mouse_pos: Tuple[int, int]):
        """Update hover state."""
        self.hover = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface):
        """Draw the recipe card."""
        # Background
        if self.selected:
            bg_color = (80, 70, 100)
            border_color = (180, 160, 200)
        elif self.hover:
            bg_color = (60, 55, 80)
            border_color = (120, 110, 140)
        else:
            bg_color = UI_PANEL
            border_color = UI_BORDER

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=6)

        if self.is_unlocked and self.recipe:
            self._draw_unlocked(surface)
        else:
            self._draw_locked(surface)

    def _draw_unlocked(self, surface: pygame.Surface):
        """Draw an unlocked recipe card."""
        # Icon area
        icon_rect = pygame.Rect(self.x + 8, self.y + 8, 44, 44)
        category_color = self.CATEGORY_COLORS.get(
            self.recipe.category, (150, 150, 150)
        )
        pygame.draw.rect(surface, category_color, icon_rect, border_radius=4)

        # Draw category icon
        self._draw_category_icon(surface, icon_rect, self.recipe.category)

        # Recipe name
        name_color = CAFE_CREAM if self.selected else UI_TEXT
        name_surface = self.name_font.render(self.recipe.name, True, name_color)
        surface.blit(name_surface, (self.x + 60, self.y + 10))

        # Difficulty stars
        star_x = self.x + 60
        star_y = self.y + 35
        for i in range(self.recipe.difficulty):
            self._draw_star(surface, star_x + i * 14, star_y, (255, 220, 60))

        # Empty stars for remaining
        for i in range(self.recipe.difficulty, 5):
            self._draw_star(surface, star_x + i * 14, star_y, (80, 75, 95))

        # Status indicators (right side)
        indicator_x = self.x + self.width - 60

        # Can cook indicator
        if self.can_cook:
            pygame.draw.circle(surface, (80, 180, 80), (indicator_x, self.y + 25), 8)
            check_color = (255, 255, 255)
            pygame.draw.line(surface, check_color,
                           (indicator_x - 4, self.y + 25),
                           (indicator_x - 1, self.y + 28), 2)
            pygame.draw.line(surface, check_color,
                           (indicator_x - 1, self.y + 28),
                           (indicator_x + 5, self.y + 21), 2)

        # Mastered badge
        if self.is_mastered:
            badge_x = indicator_x + 25
            pygame.draw.circle(surface, (220, 180, 60), (badge_x, self.y + 25), 10)
            # Crown shape
            crown_color = (255, 255, 255)
            pygame.draw.polygon(surface, crown_color, [
                (badge_x - 6, self.y + 29),
                (badge_x - 4, self.y + 22),
                (badge_x, self.y + 26),
                (badge_x + 4, self.y + 22),
                (badge_x + 6, self.y + 29),
            ])

    def _draw_locked(self, surface: pygame.Surface):
        """Draw a locked recipe card."""
        # Gray icon area
        icon_rect = pygame.Rect(self.x + 8, self.y + 8, 44, 44)
        pygame.draw.rect(surface, (60, 55, 70), icon_rect, border_radius=4)

        # Question marks
        font = pygame.font.Font(None, 32)
        qmark = font.render("?", True, (100, 95, 115))
        surface.blit(qmark, (self.x + 22, self.y + 16))

        # Locked text
        locked_text = self.name_font.render("??? Locked Recipe ???", True, UI_TEXT_DIM)
        surface.blit(locked_text, (self.x + 60, self.y + 12))

        # Hint text
        hint = "Unlock requirements unknown"
        if self.recipe and self.recipe.unlock_type == 'reputation':
            hint = f"Requires reputation level {self.recipe.unlock_requirement}"
        elif self.recipe and self.recipe.unlock_type == 'story':
            hint = "Complete story to unlock"

        hint_surface = self.detail_font.render(hint, True, (120, 110, 140))
        surface.blit(hint_surface, (self.x + 60, self.y + 35))

    def _draw_category_icon(self, surface: pygame.Surface, rect: pygame.Rect,
                            category: str):
        """Draw a simple icon based on recipe category."""
        cx = rect.centerx
        cy = rect.centery

        if category == RECIPE_CATEGORY_APPETIZER:
            # Leaf shape
            pygame.draw.ellipse(surface, (100, 140, 80),
                              (cx - 8, cy - 10, 16, 20))
            pygame.draw.line(surface, (70, 100, 50),
                           (cx, cy - 10), (cx, cy + 10), 2)

        elif category == RECIPE_CATEGORY_MAIN:
            # Plate with food
            pygame.draw.ellipse(surface, (220, 210, 200),
                              (cx - 14, cy - 4, 28, 12))
            pygame.draw.ellipse(surface, (180, 120, 80),
                              (cx - 8, cy - 10, 16, 12))

        elif category == RECIPE_CATEGORY_DESSERT:
            # Cupcake shape
            pygame.draw.rect(surface, (200, 160, 120),
                           (cx - 8, cy - 2, 16, 14), border_radius=2)
            pygame.draw.ellipse(surface, (240, 200, 220),
                              (cx - 10, cy - 12, 20, 14))
            pygame.draw.circle(surface, (220, 80, 80), (cx, cy - 10), 3)

        elif category == RECIPE_CATEGORY_BEVERAGE:
            # Cup shape
            pygame.draw.rect(surface, (200, 200, 220),
                           (cx - 8, cy - 6, 16, 18), border_radius=2)
            pygame.draw.arc(surface, (180, 180, 200),
                          (cx + 4, cy - 2, 10, 10), -1.5, 1.5, 2)
            # Steam
            pygame.draw.arc(surface, (180, 180, 200),
                          (cx - 4, cy - 14, 8, 8), 0, 3.14, 1)

    def _draw_star(self, surface: pygame.Surface, x: int, y: int, color: Tuple):
        """Draw a small star at position."""
        points = [
            (x, y - 5),
            (x + 2, y - 1),
            (x + 6, y - 1),
            (x + 3, y + 2),
            (x + 4, y + 6),
            (x, y + 4),
            (x - 4, y + 6),
            (x - 3, y + 2),
            (x - 6, y - 1),
            (x - 2, y - 1),
        ]
        pygame.draw.polygon(surface, color, points)


class RecipeDetailPanel:
    """
    A panel showing detailed information about a selected recipe.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize the detail panel."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        self._recipe = None
        self._mastery = None
        self._can_cook_result = None
        self._inventory = None

        # Fonts
        self.title_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 22)
        self.small_font = pygame.font.Font(None, 18)

    def set_recipe(self, recipe, mastery=None, can_cook_result=None, inventory=None):
        """Set the recipe to display."""
        self._recipe = recipe
        self._mastery = mastery
        self._can_cook_result = can_cook_result
        self._inventory = inventory

    def draw(self, surface: pygame.Surface):
        """Draw the detail panel."""
        # Background
        pygame.draw.rect(surface, UI_PANEL, self.rect, border_radius=8)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 2, border_radius=8)

        if not self._recipe:
            # No recipe selected
            hint = self.text_font.render("Select a recipe to view details",
                                        True, UI_TEXT_DIM)
            hint_rect = hint.get_rect(center=self.rect.center)
            surface.blit(hint, hint_rect)
            return

        y_offset = self.y + 15

        # Recipe name
        name_surface = self.title_font.render(self._recipe.name, True, CAFE_CREAM)
        surface.blit(name_surface, (self.x + 15, y_offset))
        y_offset += 35

        # Description
        if self._recipe.description:
            desc_surface = self.text_font.render(self._recipe.description,
                                                True, UI_TEXT_DIM)
            surface.blit(desc_surface, (self.x + 15, y_offset))
            y_offset += 28

        # Difficulty
        diff_text = "Difficulty: "
        diff_surface = self.text_font.render(diff_text, True, UI_TEXT)
        surface.blit(diff_surface, (self.x + 15, y_offset))
        star_x = self.x + 15 + diff_surface.get_width()
        for i in range(5):
            color = (255, 220, 60) if i < self._recipe.difficulty else (80, 75, 95)
            self._draw_star(surface, star_x + i * 16, y_offset + 8, color)
        y_offset += 30

        # Separator
        pygame.draw.line(surface, UI_BORDER,
                        (self.x + 15, y_offset), (self.x + self.width - 15, y_offset))
        y_offset += 15

        # Ingredients
        ing_label = self.text_font.render("Ingredients:", True, CAFE_CREAM)
        surface.blit(ing_label, (self.x + 15, y_offset))
        y_offset += 25

        for ing in self._recipe.ingredients:
            # Get owned count from inventory
            owned = 0
            if self._inventory:
                owned = self._inventory.get_count(ing.item_id, check_all=True)

            # Color based on availability
            if owned >= ing.quantity:
                ing_color = (100, 180, 100)  # Green - have enough
            else:
                ing_color = (180, 100, 100)  # Red - need more

            ing_text = f"  {ing.item_id.replace('_', ' ').title()} x{ing.quantity}"
            if self._inventory:
                ing_text += f" ({owned}/{ing.quantity})"

            ing_surface = self.text_font.render(ing_text, True, ing_color)
            surface.blit(ing_surface, (self.x + 15, y_offset))
            y_offset += 22

        y_offset += 10

        # Dragon color effect
        pygame.draw.line(surface, UI_BORDER,
                        (self.x + 15, y_offset), (self.x + self.width - 15, y_offset))
        y_offset += 15

        color_label = self.text_font.render("Dragon Color Effect:", True, CAFE_CREAM)
        surface.blit(color_label, (self.x + 15, y_offset))
        y_offset += 25

        # Draw color preview circle
        r, g, b = self._recipe.color_influence
        preview_color = (int(r * 255), int(g * 255), int(b * 255))
        pygame.draw.circle(surface, preview_color, (self.x + 50, y_offset + 20), 25)
        pygame.draw.circle(surface, UI_BORDER, (self.x + 50, y_offset + 20), 25, 2)

        # Color description
        color_desc = self._get_color_description(r, g, b)
        color_surface = self.small_font.render(color_desc, True, UI_TEXT_DIM)
        surface.blit(color_surface, (self.x + 85, y_offset + 12))
        y_offset += 55

        # Mastery progress
        pygame.draw.line(surface, UI_BORDER,
                        (self.x + 15, y_offset), (self.x + self.width - 15, y_offset))
        y_offset += 15

        mastery_label = self.text_font.render("Mastery:", True, CAFE_CREAM)
        surface.blit(mastery_label, (self.x + 15, y_offset))
        y_offset += 25

        if self._mastery:
            progress = self._mastery.get_progress()

            # Cook count bar
            cook_text = f"Cooked: {progress['cook_count']}/{progress['cook_required']}"
            cook_surface = self.small_font.render(cook_text, True, UI_TEXT)
            surface.blit(cook_surface, (self.x + 25, y_offset))
            y_offset += 18

            bar_width = self.width - 60
            bar_rect = pygame.Rect(self.x + 25, y_offset, bar_width, 8)
            pygame.draw.rect(surface, (60, 55, 70), bar_rect, border_radius=4)
            fill_width = int(bar_width * progress['cook_progress'] / 100)
            if fill_width > 0:
                fill_rect = pygame.Rect(self.x + 25, y_offset, fill_width, 8)
                pygame.draw.rect(surface, (100, 160, 100), fill_rect, border_radius=4)
            y_offset += 18

            # Perfect count bar
            perf_text = f"Perfect: {progress['perfect_count']}/{progress['perfect_required']}"
            perf_surface = self.small_font.render(perf_text, True, UI_TEXT)
            surface.blit(perf_surface, (self.x + 25, y_offset))
            y_offset += 18

            bar_rect = pygame.Rect(self.x + 25, y_offset, bar_width, 8)
            pygame.draw.rect(surface, (60, 55, 70), bar_rect, border_radius=4)
            fill_width = int(bar_width * progress['perfect_progress'] / 100)
            if fill_width > 0:
                fill_rect = pygame.Rect(self.x + 25, y_offset, fill_width, 8)
                pygame.draw.rect(surface, (220, 180, 60), fill_rect, border_radius=4)

            if progress['is_mastered']:
                y_offset += 25
                mastered_text = self.text_font.render("MASTERED!", True, (220, 180, 60))
                surface.blit(mastered_text, (self.x + 25, y_offset))
        else:
            never_cooked = self.small_font.render("Not yet cooked", True, UI_TEXT_DIM)
            surface.blit(never_cooked, (self.x + 25, y_offset))

    def _draw_star(self, surface: pygame.Surface, x: int, y: int, color: Tuple):
        """Draw a star at position."""
        points = [
            (x, y - 6),
            (x + 2, y - 2),
            (x + 6, y - 2),
            (x + 4, y + 2),
            (x + 5, y + 6),
            (x, y + 4),
            (x - 5, y + 6),
            (x - 4, y + 2),
            (x - 6, y - 2),
            (x - 2, y - 2),
        ]
        pygame.draw.polygon(surface, color, points)

    def _get_color_description(self, r: float, g: float, b: float) -> str:
        """Get a text description of the color influence."""
        if r > 0.7 and g < 0.4 and b < 0.4:
            return "Warm red tones"
        elif r < 0.4 and g > 0.7 and b < 0.4:
            return "Earthy green tones"
        elif r < 0.4 and g < 0.4 and b > 0.7:
            return "Cool blue tones"
        elif r > 0.6 and g > 0.6 and b < 0.4:
            return "Golden yellow tones"
        elif r > 0.6 and g < 0.4 and b > 0.6:
            return "Mystical purple tones"
        elif r < 0.4 and g > 0.6 and b > 0.6:
            return "Aqua cyan tones"
        elif r > 0.5 and g > 0.5 and b > 0.5:
            return "Balanced neutral"
        else:
            return "Mixed color influence"
