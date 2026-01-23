"""
Dragon Status State for Dragon Haven Cafe.
Displays detailed dragon information, stats, abilities, and preferences.
"""

import pygame
from typing import Optional, Dict, List, Tuple
from states.base_state import BaseScreen
from entities.dragon import Dragon
from ui.components import Button
from ui.status_bars import StatusBar
from systems.dragon_manager import get_dragon_manager
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM, BLACK,
    DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
    DRAGON_STAGE_ADOLESCENT, DRAGON_STAGE_ADULT,
    DRAGON_EGG_DAYS, DRAGON_HATCHLING_DAYS, DRAGON_JUVENILE_DAYS, DRAGON_ADOLESCENT_DAYS,
    DRAGON_STAT_MAX, DRAGON_BOND_MAX, DRAGON_STAGE_STAMINA_MAX,
    DRAGON_ABILITY_COSTS, DRAGON_ABILITY_CONTINUOUS, DRAGON_STAGE_ABILITIES,
    DRAGON_STAGE_DESCRIPTIONS, DRAGON_ABILITY_DESCRIPTIONS,
)


class DragonStatusState(BaseScreen):
    """
    Dragon status screen showing detailed dragon information.

    Features:
    - Large dragon portrait with animation
    - Stats panel (hunger, happiness, stamina, bond)
    - Info panel (name, stage, age)
    - Abilities panel
    - Preferences panel
    - Color breakdown
    - Feed and Pet buttons
    """

    # Panel positions
    PORTRAIT_X = 420
    PORTRAIT_Y = 120
    PORTRAIT_SIZE = 200

    def __init__(self, game):
        """Initialize the dragon status state."""
        super().__init__(game)
        self.title = "Dragon Status"

        # Dragon reference
        self._dragon: Optional[Dragon] = None

        # UI state
        self._editing_name = False
        self._name_input = ""
        self._animation_time = 0.0

        # Discovered preferences (would be persisted in full implementation)
        self._favorite_foods: List[str] = []
        self._disliked_foods: List[str] = []

        # UI components
        self._feed_button: Optional[Button] = None
        self._pet_button: Optional[Button] = None
        self._customize_button: Optional[Button] = None
        self._close_button: Optional[Button] = None

        # Status bars
        self._hunger_bar: Optional[StatusBar] = None
        self._happiness_bar: Optional[StatusBar] = None
        self._stamina_bar: Optional[StatusBar] = None
        self._bond_bar: Optional[StatusBar] = None

        # Fonts
        self._name_font = None
        self._stat_font = None
        self._label_font = None
        self._small_font = None

    def set_dragon(self, dragon: Dragon):
        """Set the dragon reference."""
        self._dragon = dragon
        if dragon:
            self._name_input = dragon.name

    def enter(self, previous_state=None):
        """Initialize UI when entering state."""
        super().enter(previous_state)

        # Get dragon from dragon manager
        dragon_mgr = get_dragon_manager()
        if dragon_mgr.has_dragon():
            self._dragon = dragon_mgr.get_dragon()
            self._name_input = self._dragon.get_name()

        # Initialize fonts
        self._name_font = pygame.font.Font(None, 36)
        self._stat_font = pygame.font.Font(None, 24)
        self._label_font = pygame.font.Font(None, 22)
        self._small_font = pygame.font.Font(None, 18)

        # Create status bars
        bar_x = 50
        bar_y = 150
        bar_width = 180
        bar_height = 20

        self._hunger_bar = StatusBar(bar_x, bar_y, "Hunger", (180, 100, 80), bar_width, bar_height)
        self._happiness_bar = StatusBar(bar_x, bar_y + 50, "Happiness", (220, 180, 60), bar_width, bar_height)
        self._stamina_bar = StatusBar(bar_x, bar_y + 100, "Stamina", (80, 160, 80), bar_width, bar_height)
        self._bond_bar = StatusBar(bar_x, bar_y + 150, "Bond", (160, 100, 180), bar_width, bar_height)

        # Create buttons
        self._feed_button = Button(50, SCREEN_HEIGHT - 100, 100, 40, "Feed", self._on_feed)
        self._pet_button = Button(170, SCREEN_HEIGHT - 100, 100, 40, "Pet", self._on_pet)
        self._customize_button = Button(290, SCREEN_HEIGHT - 100, 120, 40, "Customize", self._on_customize)
        self._close_button = Button(SCREEN_WIDTH - 110, 20, 90, 35, "Close", self._on_close)

    def _on_feed(self):
        """Handle feed button click."""
        # In full implementation, would open food selection
        if self._dragon and self._dragon.get_stage() != DRAGON_STAGE_EGG:
            # Quick feed with default values
            self._dragon.feed()

    def _on_pet(self):
        """Handle pet button click."""
        if self._dragon and self._dragon.get_stage() != DRAGON_STAGE_EGG:
            self._dragon.pet()

    def _on_customize(self):
        """Handle customize button click - open customization screen."""
        if self._dragon and self._dragon.get_stage() != DRAGON_STAGE_EGG:
            self.transition_to('customization')

    def _on_close(self):
        """Handle close button click."""
        self.fade_to_state('gameplay')

    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self._editing_name:
                    self._editing_name = False
                else:
                    self._on_close()
                return

            # Handle name editing
            if self._editing_name:
                if event.key == pygame.K_RETURN:
                    # Save name using validation
                    if self._dragon and len(self._name_input) > 0:
                        dragon_mgr = get_dragon_manager()
                        dragon_mgr.set_dragon_name(self._name_input)
                    self._editing_name = False
                elif event.key == pygame.K_BACKSPACE:
                    self._name_input = self._name_input[:-1]
                elif event.unicode.isprintable() and len(self._name_input) < 20:
                    self._name_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = event.pos

                # Check buttons
                if self._feed_button and self._feed_button.rect.collidepoint(pos):
                    self._on_feed()
                    return
                if self._pet_button and self._pet_button.rect.collidepoint(pos):
                    self._on_pet()
                    return
                if self._customize_button and self._customize_button.rect.collidepoint(pos):
                    self._on_customize()
                    return
                if self._close_button and self._close_button.rect.collidepoint(pos):
                    self._on_close()
                    return

                # Check name click for editing
                name_rect = pygame.Rect(self.PORTRAIT_X - 50, 340, 300, 40)
                if name_rect.collidepoint(pos) and self._dragon:
                    self._editing_name = True
                    self._name_input = self._dragon.name

    def update(self, dt):
        """Update state."""
        super().update(dt)

        # Update animation
        self._animation_time += dt

        # Update status bars if dragon exists
        if self._dragon:
            stats = self._dragon.get_stat_percentages()
            self._hunger_bar.set_value(stats['hunger'])
            self._happiness_bar.set_value(stats['happiness'])
            self._stamina_bar.set_value(stats['stamina'])
            self._bond_bar.set_value(stats['bond'])

        return True

    def draw(self, screen):
        """Draw the dragon status screen."""
        super().draw(screen)

        if not self._dragon:
            # No dragon message
            no_dragon = self._stat_font.render("No dragon yet!", True, UI_TEXT_DIM)
            screen.blit(no_dragon, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2))
            self._close_button.draw(screen)
            self.draw_fade_overlay(screen)
            return

        # Draw portrait area
        self._draw_portrait(screen)

        # Draw stats panel (left side)
        self._draw_stats_panel(screen)

        # Draw info panel (under portrait)
        self._draw_info_panel(screen)

        # Draw abilities panel (right side - expanded for all 10 abilities)
        self._draw_abilities_panel(screen)

        # Note: Preferences panel removed due to expanded abilities panel

        # Draw color breakdown
        self._draw_color_panel(screen)

        # Draw buttons
        if self._dragon.get_stage() != DRAGON_STAGE_EGG:
            self._feed_button.draw(screen)
            self._pet_button.draw(screen)
            self._customize_button.draw(screen)
        self._close_button.draw(screen)

        # Draw fade overlay
        self.draw_fade_overlay(screen)

    def _draw_portrait(self, screen):
        """Draw the dragon portrait."""
        # Portrait background
        portrait_rect = pygame.Rect(
            self.PORTRAIT_X - self.PORTRAIT_SIZE // 2,
            self.PORTRAIT_Y,
            self.PORTRAIT_SIZE,
            self.PORTRAIT_SIZE
        )
        pygame.draw.rect(screen, (40, 35, 50), portrait_rect, border_radius=12)
        pygame.draw.rect(screen, UI_BORDER, portrait_rect, 2, border_radius=12)

        # Draw dragon based on stage
        stage = self._dragon.get_stage()
        color_shift = self._dragon.get_color_shift()
        cx = self.PORTRAIT_X
        cy = self.PORTRAIT_Y + self.PORTRAIT_SIZE // 2

        # Animation bob
        bob = int(4 * abs((self._animation_time * 2) % 2 - 1))

        if stage == DRAGON_STAGE_EGG:
            self._draw_egg(screen, cx, cy + bob, color_shift)
        elif stage == DRAGON_STAGE_HATCHLING:
            self._draw_hatchling(screen, cx, cy + bob, color_shift)
        elif stage == DRAGON_STAGE_JUVENILE:
            self._draw_juvenile(screen, cx, cy + bob, color_shift)
        elif stage == DRAGON_STAGE_ADOLESCENT:
            self._draw_adolescent(screen, cx, cy + bob, color_shift)
        else:
            self._draw_adult(screen, cx, cy + bob, color_shift)

        # Dragon name (clickable for editing)
        name_y = self.PORTRAIT_Y + self.PORTRAIT_SIZE + 20
        if self._editing_name:
            # Draw input box
            input_rect = pygame.Rect(self.PORTRAIT_X - 100, name_y, 200, 36)
            pygame.draw.rect(screen, (50, 45, 65), input_rect, border_radius=4)
            pygame.draw.rect(screen, CAFE_WARM, input_rect, 2, border_radius=4)

            # Draw text with cursor
            display_text = self._name_input
            if int(self._animation_time * 2) % 2 == 0:
                display_text += "|"
            name_surface = self._name_font.render(display_text, True, CAFE_CREAM)
            name_rect = name_surface.get_rect(center=input_rect.center)
            screen.blit(name_surface, name_rect)
        else:
            # Draw name with edit hint
            name_surface = self._name_font.render(self._dragon.name, True, CAFE_CREAM)
            name_rect = name_surface.get_rect(centerx=self.PORTRAIT_X, y=name_y)
            screen.blit(name_surface, name_rect)

            # Edit hint
            hint = self._small_font.render("(click to edit)", True, UI_TEXT_DIM)
            hint_rect = hint.get_rect(centerx=self.PORTRAIT_X, y=name_y + 30)
            screen.blit(hint, hint_rect)

    def _draw_egg(self, screen, cx, cy, color_shift):
        """Draw egg stage dragon."""
        base_color = (200 + color_shift[0], 180 + color_shift[1], 160 + color_shift[2])
        base_color = tuple(max(0, min(255, c)) for c in base_color)

        # Large egg
        pygame.draw.ellipse(screen, base_color, (cx - 40, cy - 50, 80, 100))

        # Spots
        spot_color = (base_color[0] - 30, base_color[1] - 30, base_color[2] - 30)
        spot_color = tuple(max(0, c) for c in spot_color)
        pygame.draw.circle(screen, spot_color, (cx - 15, cy - 20), 10)
        pygame.draw.circle(screen, spot_color, (cx + 20, cy), 8)
        pygame.draw.circle(screen, spot_color, (cx - 5, cy + 25), 12)

        # Shine
        pygame.draw.ellipse(screen, (255, 255, 255, 100), (cx - 25, cy - 40, 15, 20))

    def _draw_hatchling(self, screen, cx, cy, color_shift):
        """Draw hatchling stage dragon."""
        base_color = (120 + color_shift[0], 180 + color_shift[1], 120 + color_shift[2])
        base_color = tuple(max(0, min(255, c)) for c in base_color)
        dark_color = tuple(max(0, c - 40) for c in base_color)

        # Body
        pygame.draw.ellipse(screen, base_color, (cx - 35, cy - 20, 70, 50))

        # Head
        pygame.draw.ellipse(screen, base_color, (cx + 15, cy - 50, 45, 40))

        # Eyes
        pygame.draw.ellipse(screen, (255, 255, 255), (cx + 30, cy - 45, 18, 14))
        pygame.draw.circle(screen, (40, 40, 40), (cx + 38, cy - 40), 5)

        # Tiny wings
        pygame.draw.ellipse(screen, dark_color, (cx - 30, cy - 35, 25, 20))

        # Tail
        pygame.draw.arc(screen, base_color, (cx - 55, cy - 10, 40, 40), 0, 2, 6)

        # Belly
        belly_color = (min(255, base_color[0] + 40), min(255, base_color[1] + 40), min(255, base_color[2] + 30))
        pygame.draw.ellipse(screen, belly_color, (cx - 20, cy, 40, 25))

    def _draw_juvenile(self, screen, cx, cy, color_shift):
        """Draw juvenile stage dragon."""
        base_color = (100 + color_shift[0], 160 + color_shift[1], 200 + color_shift[2])
        base_color = tuple(max(0, min(255, c)) for c in base_color)
        dark_color = tuple(max(0, c - 40) for c in base_color)

        # Body
        pygame.draw.ellipse(screen, base_color, (cx - 50, cy - 25, 100, 60))

        # Neck
        pygame.draw.ellipse(screen, base_color, (cx + 25, cy - 50, 35, 50))

        # Head
        pygame.draw.ellipse(screen, base_color, (cx + 35, cy - 75, 55, 40))

        # Eyes
        pygame.draw.ellipse(screen, (255, 255, 255), (cx + 55, cy - 70, 20, 16))
        pygame.draw.circle(screen, (40, 40, 40), (cx + 65, cy - 65), 6)

        # Horns
        pygame.draw.polygon(screen, dark_color, [
            (cx + 45, cy - 80), (cx + 40, cy - 100), (cx + 55, cy - 80)
        ])
        pygame.draw.polygon(screen, dark_color, [
            (cx + 65, cy - 82), (cx + 70, cy - 100), (cx + 75, cy - 80)
        ])

        # Wings
        pygame.draw.ellipse(screen, dark_color, (cx - 45, cy - 60, 60, 40))
        pygame.draw.ellipse(screen, dark_color, (cx - 35, cy - 55, 50, 35))

        # Tail
        pygame.draw.arc(screen, base_color, (cx - 80, cy - 20, 60, 50), 0, 2, 8)
        # Tail tip
        pygame.draw.polygon(screen, dark_color, [
            (cx - 75, cy + 10), (cx - 95, cy + 5), (cx - 90, cy + 20), (cx - 70, cy + 20)
        ])

        # Belly
        belly_color = (min(255, base_color[0] + 40), min(255, base_color[1] + 40), min(255, base_color[2] + 30))
        pygame.draw.ellipse(screen, belly_color, (cx - 30, cy, 60, 30))

        # Legs
        pygame.draw.ellipse(screen, base_color, (cx - 35, cy + 15, 20, 30))
        pygame.draw.ellipse(screen, base_color, (cx + 15, cy + 15, 20, 30))

    def _draw_adolescent(self, screen, cx, cy, color_shift):
        """Draw adolescent stage dragon - horse-sized with wing buds."""
        base_color = (160 + color_shift[0], 100 + color_shift[1], 180 + color_shift[2])
        base_color = tuple(max(0, min(255, c)) for c in base_color)
        dark_color = tuple(max(0, c - 50) for c in base_color)

        # Larger body
        pygame.draw.ellipse(screen, base_color, (cx - 55, cy - 30, 110, 70))

        # Longer neck
        pygame.draw.ellipse(screen, base_color, (cx + 30, cy - 65, 40, 65))

        # Head with more detail
        pygame.draw.ellipse(screen, base_color, (cx + 40, cy - 90, 60, 45))

        # Snout
        pygame.draw.ellipse(screen, base_color, (cx + 80, cy - 80, 25, 20))

        # Eyes
        pygame.draw.ellipse(screen, (255, 255, 255), (cx + 60, cy - 85, 22, 18))
        pygame.draw.circle(screen, (40, 40, 40), (cx + 70, cy - 78), 7)
        # Eye highlight
        pygame.draw.circle(screen, (255, 255, 255), (cx + 67, cy - 82), 2)

        # Larger horns
        pygame.draw.polygon(screen, dark_color, [
            (cx + 50, cy - 95), (cx + 42, cy - 120), (cx + 60, cy - 95)
        ])
        pygame.draw.polygon(screen, dark_color, [
            (cx + 72, cy - 97), (cx + 80, cy - 120), (cx + 88, cy - 95)
        ])

        # Spines down neck
        for i in range(4):
            spine_x = cx + 35 + i * 8
            spine_y = cy - 55 + i * 8
            pygame.draw.polygon(screen, dark_color, [
                (spine_x - 4, spine_y), (spine_x, spine_y - 12), (spine_x + 4, spine_y)
            ])

        # Wing buds (small but visible)
        pygame.draw.ellipse(screen, dark_color, (cx - 50, cy - 65, 70, 45))
        pygame.draw.ellipse(screen, base_color, (cx - 40, cy - 55, 55, 35))

        # Muscular tail
        pygame.draw.arc(screen, base_color, (cx - 90, cy - 25, 70, 60), 0, 2, 10)
        # Tail spines
        pygame.draw.polygon(screen, dark_color, [
            (cx - 85, cy + 15), (cx - 100, cy + 5), (cx - 95, cy + 25), (cx - 80, cy + 25)
        ])

        # Belly
        belly_color = (min(255, base_color[0] + 40), min(255, base_color[1] + 50), min(255, base_color[2] + 30))
        pygame.draw.ellipse(screen, belly_color, (cx - 35, cy + 5, 70, 35))

        # Stronger legs
        pygame.draw.ellipse(screen, base_color, (cx - 40, cy + 20, 25, 35))
        pygame.draw.ellipse(screen, base_color, (cx + 20, cy + 20, 25, 35))

        # Claws
        for leg_x in [cx - 35, cx + 25]:
            for j in range(3):
                claw_x = leg_x + j * 6
                pygame.draw.line(screen, dark_color, (claw_x, cy + 50), (claw_x, cy + 58), 2)

    def _draw_adult(self, screen, cx, cy, color_shift):
        """Draw adult stage dragon - majestic with full wingspan."""
        base_color = (200 + color_shift[0], 80 + color_shift[1], 80 + color_shift[2])
        base_color = tuple(max(0, min(255, c)) for c in base_color)
        dark_color = tuple(max(0, c - 60) for c in base_color)

        # Majestic body
        pygame.draw.ellipse(screen, base_color, (cx - 50, cy - 25, 100, 65))

        # Long elegant neck
        pygame.draw.ellipse(screen, base_color, (cx + 25, cy - 70, 45, 75))

        # Noble head
        pygame.draw.ellipse(screen, base_color, (cx + 35, cy - 95, 65, 50))

        # Snout with nostrils
        pygame.draw.ellipse(screen, base_color, (cx + 80, cy - 85, 30, 25))
        # Fire glow nostrils
        pygame.draw.circle(screen, (255, 150, 50), (cx + 100, cy - 78), 4)
        pygame.draw.circle(screen, (255, 200, 100), (cx + 100, cy - 78), 2)
        pygame.draw.circle(screen, (255, 150, 50), (cx + 100, cy - 68), 4)
        pygame.draw.circle(screen, (255, 200, 100), (cx + 100, cy - 68), 2)

        # Majestic eyes
        pygame.draw.ellipse(screen, (255, 255, 255), (cx + 55, cy - 90, 25, 20))
        pygame.draw.circle(screen, (180, 50, 50), (cx + 67, cy - 82), 8)
        pygame.draw.circle(screen, (40, 40, 40), (cx + 67, cy - 82), 4)
        pygame.draw.circle(screen, (255, 255, 255), (cx + 63, cy - 86), 3)

        # Crown of horns
        pygame.draw.polygon(screen, dark_color, [
            (cx + 45, cy - 100), (cx + 35, cy - 130), (cx + 55, cy - 100)
        ])
        pygame.draw.polygon(screen, dark_color, [
            (cx + 65, cy - 102), (cx + 70, cy - 135), (cx + 82, cy - 100)
        ])
        pygame.draw.polygon(screen, dark_color, [
            (cx + 85, cy - 98), (cx + 95, cy - 120), (cx + 98, cy - 95)
        ])

        # Spines down neck and back
        for i in range(6):
            spine_x = cx + 30 + i * 10
            spine_y = cy - 60 + i * 10
            spine_height = 15 - i * 2
            pygame.draw.polygon(screen, dark_color, [
                (spine_x - 5, spine_y), (spine_x, spine_y - spine_height), (spine_x + 5, spine_y)
            ])

        # Full wingspan
        # Left wing membrane
        wing_color = (base_color[0] - 20, base_color[1] + 20, base_color[2] + 40)
        wing_color = tuple(max(0, min(255, c)) for c in wing_color)
        pygame.draw.polygon(screen, wing_color, [
            (cx - 30, cy - 40),
            (cx - 95, cy - 80),
            (cx - 90, cy - 50),
            (cx - 75, cy - 30),
            (cx - 50, cy - 20),
        ])
        # Wing bones
        pygame.draw.line(screen, dark_color, (cx - 30, cy - 40), (cx - 95, cy - 80), 4)
        pygame.draw.line(screen, dark_color, (cx - 30, cy - 40), (cx - 75, cy - 30), 3)
        pygame.draw.line(screen, dark_color, (cx - 30, cy - 40), (cx - 50, cy - 20), 3)

        # Powerful tail
        pygame.draw.arc(screen, base_color, (cx - 85, cy - 20, 70, 55), 0, 2, 12)
        # Tail flame tip
        pygame.draw.polygon(screen, dark_color, [
            (cx - 80, cy + 18), (cx - 110, cy + 10), (cx - 100, cy + 30), (cx - 75, cy + 30)
        ])

        # Armored belly
        belly_color = (min(255, base_color[0] + 30), min(255, base_color[1] + 60), min(255, base_color[2] + 50))
        pygame.draw.ellipse(screen, belly_color, (cx - 30, cy + 10, 65, 35))
        # Belly scales
        for i in range(3):
            scale_y = cy + 18 + i * 10
            pygame.draw.arc(screen, dark_color, (cx - 20 + i * 5, scale_y, 30, 12), 3.14, 6.28, 1)

        # Powerful legs
        pygame.draw.ellipse(screen, base_color, (cx - 38, cy + 25, 28, 40))
        pygame.draw.ellipse(screen, base_color, (cx + 18, cy + 25, 28, 40))

        # Sharp claws
        for leg_x in [cx - 32, cx + 24]:
            for j in range(4):
                claw_x = leg_x + j * 5
                pygame.draw.line(screen, (60, 60, 60), (claw_x, cy + 60), (claw_x - 2, cy + 70), 3)

    def _draw_stats_panel(self, screen):
        """Draw the stats panel."""
        panel_rect = pygame.Rect(30, 120, 230, 230)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Panel title
        title = self._label_font.render("Stats", True, CAFE_CREAM)
        screen.blit(title, (50, 125))

        # Draw status bars
        self._hunger_bar.draw(screen)
        self._happiness_bar.draw(screen)
        self._stamina_bar.draw(screen)
        self._bond_bar.draw(screen)

    def _draw_info_panel(self, screen):
        """Draw the info panel."""
        panel_x = 30
        panel_y = 370
        panel_rect = pygame.Rect(panel_x, panel_y, 230, 180)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Panel title
        title = self._label_font.render("Info", True, CAFE_CREAM)
        screen.blit(title, (panel_x + 20, panel_y + 10))

        y = panel_y + 40

        # Stage
        stage_name = self._dragon.get_stage().replace('_', ' ').title()
        stage_text = self._stat_font.render(f"Stage: {stage_name}", True, UI_TEXT)
        screen.blit(stage_text, (panel_x + 20, y))
        y += 28

        # Days alive
        days = self._dragon.get_age_days()
        days_text = self._stat_font.render(f"Days Alive: {days}", True, UI_TEXT)
        screen.blit(days_text, (panel_x + 20, y))
        y += 28

        # Days in current stage
        stage = self._dragon.get_stage()
        egg_end = DRAGON_EGG_DAYS
        hatchling_end = egg_end + DRAGON_HATCHLING_DAYS
        juvenile_end = hatchling_end + DRAGON_JUVENILE_DAYS
        adolescent_end = juvenile_end + DRAGON_ADOLESCENT_DAYS

        if stage == DRAGON_STAGE_EGG:
            days_in_stage = days
            days_until_next = max(0, egg_end - days + 1)
        elif stage == DRAGON_STAGE_HATCHLING:
            days_in_stage = days - egg_end
            days_until_next = max(0, DRAGON_HATCHLING_DAYS - days_in_stage + 1)
        elif stage == DRAGON_STAGE_JUVENILE:
            days_in_stage = days - hatchling_end
            days_until_next = max(0, DRAGON_JUVENILE_DAYS - days_in_stage + 1)
        elif stage == DRAGON_STAGE_ADOLESCENT:
            days_in_stage = days - juvenile_end
            days_until_next = max(0, DRAGON_ADOLESCENT_DAYS - days_in_stage + 1)
        else:
            days_in_stage = days - adolescent_end
            days_until_next = -1  # Adult - no next stage

        stage_days = self._stat_font.render(f"In Stage: {days_in_stage} days", True, UI_TEXT)
        screen.blit(stage_days, (panel_x + 20, y))
        y += 28

        # Days until next stage
        if days_until_next >= 0:
            next_text = self._stat_font.render(f"Next Stage: {days_until_next} days", True, (100, 180, 100))
        else:
            next_text = self._stat_font.render("Fully Grown!", True, (220, 180, 60))
        screen.blit(next_text, (panel_x + 20, y))

        # Mood
        y += 35
        mood = self._dragon.get_mood().title()
        mood_text = self._stat_font.render(f"Mood: {mood}", True, CAFE_WARM)
        screen.blit(mood_text, (panel_x + 20, y))

    def _draw_abilities_panel(self, screen):
        """Draw the abilities panel."""
        panel_x = SCREEN_WIDTH - 280
        panel_y = 120
        panel_rect = pygame.Rect(panel_x, panel_y, 250, 430)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Panel title
        title = self._label_font.render("Abilities", True, CAFE_CREAM)
        screen.blit(title, (panel_x + 20, panel_y + 10))

        y = panel_y + 35

        # Get all possible abilities and current abilities
        current_abilities = self._dragon.get_available_abilities()
        # All abilities in unlock order
        all_abilities = [
            'burrow_fetch', 'sniff_track',  # Hatchling
            'rock_smash', 'creature_scare',  # Juvenile
            'ember_breath', 'fire_breath', 'glide',  # Adolescent
            'flight_scout', 'full_flight', 'fire_stream',  # Adult
        ]

        for ability in all_abilities:
            is_unlocked = ability in current_abilities
            is_continuous = ability in DRAGON_ABILITY_CONTINUOUS
            can_use = self._dragon.can_use_ability(ability)

            ability_name = ability.replace('_', ' ').title()

            if is_unlocked:
                # Unlocked ability
                if can_use:
                    name_color = UI_TEXT
                    cost_color = (100, 180, 100)
                else:
                    name_color = UI_TEXT_DIM
                    cost_color = (180, 100, 100)

                name_surface = self._stat_font.render(ability_name, True, name_color)
                screen.blit(name_surface, (panel_x + 20, y))

                # Cost display (different for continuous abilities)
                if is_continuous:
                    cost = DRAGON_ABILITY_CONTINUOUS.get(ability, 0)
                    cost_text = f"{cost}/sec"
                else:
                    cost = DRAGON_ABILITY_COSTS.get(ability, 0)
                    cost_text = f"{cost} stamina"

                cost_surface = self._small_font.render(cost_text, True, cost_color)
                screen.blit(cost_surface, (panel_x + 160, y + 2))

                # Usage hint
                hint = DRAGON_ABILITY_DESCRIPTIONS.get(ability, "Use in exploration")
                hint_surface = self._small_font.render(hint, True, UI_TEXT_DIM)
                screen.blit(hint_surface, (panel_x + 25, y + 20))
            else:
                # Locked ability
                locked_name = self._stat_font.render(f"??? {ability_name}", True, (80, 75, 95))
                screen.blit(locked_name, (panel_x + 20, y))

                # Unlock condition
                unlock_stage = self._get_ability_unlock_stage(ability)
                unlock_surface = self._small_font.render(f"({unlock_stage})", True, (100, 95, 115))
                screen.blit(unlock_surface, (panel_x + 160, y + 2))

            y += 40

    def _get_ability_unlock_stage(self, ability: str) -> str:
        """Get the stage that unlocks an ability."""
        for stage, abilities in DRAGON_STAGE_ABILITIES.items():
            if ability in abilities:
                return stage.replace('_', ' ').title()
        return "Unknown"

    def _draw_preferences_panel(self, screen):
        """Draw the preferences panel."""
        panel_x = SCREEN_WIDTH - 280
        panel_y = 390
        panel_rect = pygame.Rect(panel_x, panel_y, 250, 160)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Panel title
        title = self._label_font.render("Preferences", True, CAFE_CREAM)
        screen.blit(title, (panel_x + 20, panel_y + 10))

        y = panel_y + 40

        # Favorite foods
        fav_label = self._stat_font.render("Favorites:", True, (100, 180, 100))
        screen.blit(fav_label, (panel_x + 20, y))
        y += 25

        if self._favorite_foods:
            fav_text = ", ".join(self._favorite_foods[:3])
        else:
            fav_text = "??? (Feed to discover)"
        fav_surface = self._small_font.render(fav_text, True, UI_TEXT_DIM)
        screen.blit(fav_surface, (panel_x + 30, y))
        y += 30

        # Disliked foods
        dis_label = self._stat_font.render("Dislikes:", True, (180, 100, 100))
        screen.blit(dis_label, (panel_x + 20, y))
        y += 25

        if self._disliked_foods:
            dis_text = ", ".join(self._disliked_foods[:3])
        else:
            dis_text = "??? (Feed to discover)"
        dis_surface = self._small_font.render(dis_text, True, UI_TEXT_DIM)
        screen.blit(dis_surface, (panel_x + 30, y))

    def _draw_color_panel(self, screen):
        """Draw the color breakdown panel."""
        panel_x = 280
        panel_y = 570
        panel_rect = pygame.Rect(panel_x, panel_y, 300, 80)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Panel title
        title = self._label_font.render("Color", True, CAFE_CREAM)
        screen.blit(title, (panel_x + 20, panel_y + 10))

        # Get color values
        r, g, b = self._dragon.get_color_shift()

        # Color preview circle
        preview_color = (
            max(0, min(255, 128 + r * 2)),
            max(0, min(255, 128 + g * 2)),
            max(0, min(255, 128 + b * 2))
        )
        pygame.draw.circle(screen, preview_color, (panel_x + 60, panel_y + 50), 25)
        pygame.draw.circle(screen, UI_BORDER, (panel_x + 60, panel_y + 50), 25, 2)

        # RGB values
        x = panel_x + 100
        y = panel_y + 35

        r_text = self._small_font.render(f"R: {r:+d}", True, (200, 100, 100))
        screen.blit(r_text, (x, y))

        g_text = self._small_font.render(f"G: {g:+d}", True, (100, 200, 100))
        screen.blit(g_text, (x + 60, y))

        b_text = self._small_font.render(f"B: {b:+d}", True, (100, 100, 200))
        screen.blit(b_text, (x + 120, y))

        # Description
        desc = "Feed recipes to shift dragon color"
        desc_surface = self._small_font.render(desc, True, UI_TEXT_DIM)
        screen.blit(desc_surface, (x, y + 20))
