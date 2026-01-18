"""
Main Menu Screen for Dragon Haven Cafe.
The first screen players see when launching the game.
"""

import pygame
import math
import random
from states.base_state import BaseScreen
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_PANEL, UI_BORDER, UI_HIGHLIGHT,
    UI_TEXT, UI_TEXT_DIM, WHITE, BLACK,
    CAFE_WARM, CAFE_WOOD, CAFE_CREAM,
    DRAGON_HATCHLING, DRAGON_WING,
    VERSION,
)
from sound_manager import get_sound_manager


class MenuItem:
    """A menu option with hover state."""

    def __init__(self, text: str, action: str, y: int):
        """
        Initialize a menu item.

        Args:
            text: Display text
            action: Action identifier (e.g., 'new_game', 'continue')
            y: Y position on screen
        """
        self.text = text
        self.action = action
        self.y = y
        self.x = SCREEN_WIDTH // 2
        self.hover = False
        self.hover_time = 0.0

        # Pre-render text
        self.font = pygame.font.Font(None, 42)
        self.normal_surface = self.font.render(text, True, UI_TEXT)
        self.hover_surface = self.font.render(text, True, CAFE_CREAM)
        self.rect = self.normal_surface.get_rect(center=(self.x, self.y))

        # Expanded hitbox for easier clicking
        self.hitbox = self.rect.inflate(40, 10)

    def update(self, dt: float, mouse_pos: tuple):
        """Update hover state."""
        was_hover = self.hover
        self.hover = self.hitbox.collidepoint(mouse_pos)

        if self.hover:
            self.hover_time += dt
        else:
            self.hover_time = 0.0

        return self.hover and not was_hover  # Return True on hover enter

    def draw(self, surface: pygame.Surface):
        """Draw the menu item."""
        # Hover animation - slight scale and glow effect
        if self.hover:
            # Draw glow behind
            glow_surf = pygame.Surface((self.rect.width + 20, self.rect.height + 10), pygame.SRCALPHA)
            glow_color = (*CAFE_WARM[:3], 100)
            pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=5)
            glow_rect = glow_surf.get_rect(center=(self.x, self.y))
            surface.blit(glow_surf, glow_rect)

            # Draw highlight bar
            bar_width = self.rect.width + 40
            bar_height = 4
            bar_y = self.y + self.rect.height // 2 + 5
            pygame.draw.rect(surface, CAFE_WARM,
                           (self.x - bar_width // 2, bar_y, bar_width, bar_height),
                           border_radius=2)

            # Draw text
            surface.blit(self.hover_surface, self.rect)
        else:
            surface.blit(self.normal_surface, self.rect)


class Particle:
    """A floating particle for background ambiance."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset particle to initial state."""
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.uniform(2, 6)
        self.speed_x = random.uniform(-20, 20)
        self.speed_y = random.uniform(-30, -10)
        self.alpha = random.randint(50, 150)
        self.lifetime = random.uniform(3, 8)
        self.age = 0
        self.color = random.choice([CAFE_WARM, DRAGON_HATCHLING, CAFE_CREAM])

    def update(self, dt: float) -> bool:
        """Update particle. Returns False when dead."""
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        self.age += dt

        # Fade out near end of life
        life_progress = self.age / self.lifetime
        if life_progress > 0.7:
            fade_progress = (life_progress - 0.7) / 0.3
            self.alpha = int(self.alpha * (1 - fade_progress))

        return self.age < self.lifetime

    def draw(self, surface: pygame.Surface):
        """Draw the particle."""
        if self.alpha > 0:
            particle_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            color_with_alpha = (*self.color[:3], min(255, self.alpha))
            pygame.draw.circle(particle_surf, color_with_alpha,
                             (int(self.size), int(self.size)), int(self.size))
            surface.blit(particle_surf, (int(self.x - self.size), int(self.y - self.size)))


class MainMenuState(BaseScreen):
    """
    Main menu screen state.

    Displays title, menu options, and animated background.
    """

    def __init__(self, game):
        """Initialize the main menu state."""
        super().__init__(game)
        self.title = ""  # We'll draw custom title
        self.background_color = UI_BG

        # Menu items
        self.menu_items: list[MenuItem] = []
        self.selected_index = 0

        # Particles for background
        self.particles: list[Particle] = []

        # Animation timers
        self.time_elapsed = 0.0
        self.title_bob = 0.0

        # Sound manager
        self.sound = get_sound_manager()

    def enter(self, previous_state=None):
        """Initialize menu when entering state."""
        super().enter(previous_state)

        # Create menu items
        menu_y_start = 380
        menu_spacing = 60
        menu_options = [
            ("New Game", "new_game"),
            ("Continue", "continue"),
            ("Settings", "settings"),
            ("Quit", "quit"),
        ]

        self.menu_items = []
        for i, (text, action) in enumerate(menu_options):
            y = menu_y_start + i * menu_spacing
            self.menu_items.append(MenuItem(text, action, y))

        # Initialize particles
        self.particles = [Particle() for _ in range(30)]

        # Create title font
        self.title_font_large = pygame.font.Font(None, 72)
        self.title_font_small = pygame.font.Font(None, 36)

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._move_selection(-1)
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._select_current()
            elif event.key == pygame.K_ESCAPE:
                self._do_action("quit")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for item in self.menu_items:
                    if item.hover:
                        self._do_action(item.action)
                        break

    def _move_selection(self, direction: int):
        """Move menu selection up or down."""
        self.selected_index = (self.selected_index + direction) % len(self.menu_items)

        # Update hover states
        for i, item in enumerate(self.menu_items):
            item.hover = (i == self.selected_index)

        # Play sound
        self.sound.play('ui_hover')

    def _select_current(self):
        """Select the currently highlighted menu item."""
        if 0 <= self.selected_index < len(self.menu_items):
            self._do_action(self.menu_items[self.selected_index].action)

    def _do_action(self, action: str):
        """Execute a menu action."""
        self.sound.play('ui_confirm')

        if action == "new_game":
            # Initialize fresh game state
            from game_state import get_game_state_manager
            game_state_mgr = get_game_state_manager()
            game_state_mgr.new_game()
            self.fade_to_state("exploration")

        elif action == "continue":
            # Go to save/load screen in load mode
            # First check if any saves exist
            from save_manager import get_save_manager
            save_mgr = get_save_manager()
            if save_mgr.has_any_saves():
                # Would transition to load screen, for now go to most recent
                most_recent = save_mgr.get_most_recent_slot()
                if most_recent:
                    from game_state import get_game_state_manager
                    game_state_mgr = get_game_state_manager()
                    if game_state_mgr.load_game(most_recent):
                        self.fade_to_state("exploration")
                        return
            # No saves or load failed - start new game instead
            from game_state import get_game_state_manager
            game_state_mgr = get_game_state_manager()
            game_state_mgr.new_game()
            self.fade_to_state("exploration")

        elif action == "settings":
            self.fade_to_state("settings")

        elif action == "quit":
            self.request_quit()

    def update(self, dt):
        """Update menu animations."""
        super().update(dt)

        self.time_elapsed += dt
        self.title_bob = math.sin(self.time_elapsed * 2) * 5

        # Update particles
        mouse_pos = pygame.mouse.get_pos()
        for particle in self.particles:
            if not particle.update(dt):
                particle.reset()
                particle.y = SCREEN_HEIGHT + 10  # Start from bottom

        # Update menu items
        for i, item in enumerate(self.menu_items):
            hover_entered = item.update(dt, mouse_pos)
            if hover_entered:
                self.selected_index = i
                self.sound.play('ui_hover', 0.5)

        # Keep keyboard selection synced
        if not any(item.hover for item in self.menu_items):
            # No mouse hover, use keyboard selection
            for i, item in enumerate(self.menu_items):
                item.hover = (i == self.selected_index)

        return True

    def draw(self, screen):
        """Draw the main menu."""
        # Background
        screen.fill(self.background_color)

        # Draw particles behind everything
        for particle in self.particles:
            particle.draw(screen)

        # Draw decorative dragon silhouette
        self._draw_dragon_silhouette(screen)

        # Draw title
        self._draw_title(screen)

        # Draw menu items
        for item in self.menu_items:
            item.draw(screen)

        # Draw version number
        version_font = pygame.font.Font(None, 24)
        version_text = version_font.render(f"v{VERSION}", True, UI_TEXT_DIM)
        version_rect = version_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        screen.blit(version_text, version_rect)

        # Draw fade overlay last
        self.draw_fade_overlay(screen)

    def _draw_title(self, screen):
        """Draw the game title with styling."""
        # Title: "Dragon Haven Cafe"
        title_y = 150 + self.title_bob

        # Main title
        title_surface = self.title_font_large.render("Dragon Haven Cafe", True, CAFE_CREAM)
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH // 2, centery=title_y)

        # Draw shadow
        shadow_surface = self.title_font_large.render("Dragon Haven Cafe", True, (30, 25, 35))
        shadow_rect = shadow_surface.get_rect(centerx=SCREEN_WIDTH // 2 + 3, centery=title_y + 3)
        screen.blit(shadow_surface, shadow_rect)

        # Draw main title
        screen.blit(title_surface, title_rect)

        # Subtitle
        subtitle = "A dragon-raising cafe adventure"
        subtitle_surface = self.title_font_small.render(subtitle, True, UI_TEXT_DIM)
        subtitle_rect = subtitle_surface.get_rect(centerx=SCREEN_WIDTH // 2, centery=title_y + 50)
        screen.blit(subtitle_surface, subtitle_rect)

        # Decorative line under title
        line_y = title_y + 80
        line_width = 300
        pygame.draw.line(screen, UI_BORDER,
                        (SCREEN_WIDTH // 2 - line_width // 2, line_y),
                        (SCREEN_WIDTH // 2 + line_width // 2, line_y), 2)

    def _draw_dragon_silhouette(self, screen):
        """Draw a decorative dragon silhouette in the background."""
        # Simple dragon shape on the right side
        dragon_x = SCREEN_WIDTH - 200
        dragon_y = SCREEN_HEIGHT - 250

        # Body (ellipse)
        body_color = (*DRAGON_WING[:3], 40)  # Semi-transparent
        body_surf = pygame.Surface((150, 100), pygame.SRCALPHA)
        pygame.draw.ellipse(body_surf, body_color, (0, 20, 120, 60))
        screen.blit(body_surf, (dragon_x, dragon_y))

        # Head
        head_surf = pygame.Surface((60, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(head_surf, body_color, (0, 0, 50, 40))
        screen.blit(head_surf, (dragon_x + 100, dragon_y - 10))

        # Tail
        tail_surf = pygame.Surface((100, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(tail_surf, body_color, (0, 10, 80, 20))
        screen.blit(tail_surf, (dragon_x - 70, dragon_y + 40))

        # Wing
        wing_color = (*DRAGON_HATCHLING[:3], 30)
        wing_surf = pygame.Surface((100, 80), pygame.SRCALPHA)
        pygame.draw.polygon(wing_surf, wing_color, [(50, 0), (100, 60), (0, 60)])
        screen.blit(wing_surf, (dragon_x + 30, dragon_y - 60))
