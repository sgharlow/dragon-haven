"""
HUD (Heads-Up Display) for Dragon Haven Cafe.
Displays vital information during gameplay without cluttering the screen.
"""

import pygame
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    HUD_MODE_EXPLORATION, HUD_MODE_CAFE,
    HUD_MARGIN, HUD_PLAYER_X, HUD_PLAYER_Y,
    HUD_TIME_X, HUD_TIME_Y,
    HUD_NOTIFICATION_X, HUD_NOTIFICATION_Y, HUD_NOTIFICATION_MAX, HUD_NOTIFICATION_DURATION,
    HUD_DRAGON_X, HUD_DRAGON_Y,
    HUD_MINIMAP_X, HUD_MINIMAP_Y, HUD_MINIMAP_SIZE,
    HUD_QUICK_INV_Y, HUD_QUICK_INV_SLOTS, HUD_QUICK_INV_SLOT_SIZE, HUD_QUICK_INV_SPACING,
    HUD_BG_ALPHA, HUD_PANEL_COLOR, HUD_BORDER_COLOR,
    NOTIFICATION_INFO, NOTIFICATION_SUCCESS, NOTIFICATION_WARNING, NOTIFICATION_ERROR,
    NOTIFICATION_COLORS,
    SEASON_ICONS, WEATHER_ICONS, MOOD_FACES,
    UI_TEXT, UI_TEXT_DIM, WHITE, CAFE_CREAM, CAFE_WARM,
    WEATHER_SUNNY, WEATHER_CLOUDY, WEATHER_RAINY, WEATHER_STORMY, WEATHER_SPECIAL,
)
import math
from ui.status_bars import DragonStatusBars, QuickInventoryBar


@dataclass
class Notification:
    """A HUD notification message."""
    message: str
    notification_type: str = NOTIFICATION_INFO
    duration: float = HUD_NOTIFICATION_DURATION
    elapsed: float = 0.0
    alpha: float = 1.0


class HUD:
    """
    Main HUD class that manages all on-screen UI elements during gameplay.

    Usage:
        hud = HUD()
        hud.set_mode(HUD_MODE_EXPLORATION)
        hud.update(dt)
        hud.draw(screen)
    """

    def __init__(self):
        """Initialize the HUD."""
        self._mode = HUD_MODE_EXPLORATION
        self._visible = True
        self._fade_alpha = 1.0  # For fading HUD elements

        # Player info
        self._gold = 0
        self._location_name = "Cafe Grounds"

        # Time info
        self._time_string = "8:00 AM"
        self._day_number = 1
        self._season = "spring"
        self._weather = WEATHER_SUNNY

        # Dragon status bars (bottom-left)
        self.dragon_bars = DragonStatusBars(HUD_DRAGON_X, HUD_DRAGON_Y)

        # Quick inventory bar (bottom-center)
        self.quick_inventory = QuickInventoryBar(
            SCREEN_WIDTH // 2,
            HUD_QUICK_INV_Y,
            HUD_QUICK_INV_SLOTS,
            HUD_QUICK_INV_SLOT_SIZE,
            HUD_QUICK_INV_SPACING
        )

        # Notifications
        self._notifications: List[Notification] = []

        # Fonts
        self.title_font = pygame.font.Font(None, 28)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.time_font = pygame.font.Font(None, 32)
        self.notification_font = pygame.font.Font(None, 24)

        # Minimap placeholder state
        self._show_minimap = False

    # =========================================================================
    # MODE AND VISIBILITY
    # =========================================================================

    def set_mode(self, mode: str):
        """
        Set HUD mode (exploration or cafe).

        Args:
            mode: HUD_MODE_EXPLORATION or HUD_MODE_CAFE
        """
        self._mode = mode

    def get_mode(self) -> str:
        """Get current HUD mode."""
        return self._mode

    def toggle_visibility(self):
        """Toggle HUD visibility."""
        self._visible = not self._visible

    def show(self):
        """Show the HUD."""
        self._visible = True

    def hide(self):
        """Hide the HUD."""
        self._visible = False

    def is_visible(self) -> bool:
        """Check if HUD is visible."""
        return self._visible

    # =========================================================================
    # DATA UPDATES
    # =========================================================================

    def set_player_info(self, gold: int, location: str):
        """
        Update player info display.

        Args:
            gold: Current gold amount
            location: Current location name
        """
        self._gold = gold
        self._location_name = location

    def set_time_info(self, time_string: str, day: int, season: str, weather: str):
        """
        Update time display.

        Args:
            time_string: Formatted time (e.g., "8:00 AM")
            day: Current day number
            season: Current season name
            weather: Current weather type
        """
        self._time_string = time_string
        self._day_number = day
        self._season = season
        self._weather = weather

    def set_dragon_stats(self, hunger: float, stamina: float, happiness: float,
                         name: str = None, mood: str = None, stage: str = None):
        """
        Update dragon status display.

        Args:
            hunger: Hunger value (0-100)
            stamina: Stamina value (0-100)
            happiness: Happiness value (0-100)
            name: Dragon name (optional)
            mood: Dragon mood (optional)
            stage: Dragon stage (optional)
        """
        self.dragon_bars.set_dragon_stats(hunger, stamina, happiness, name, mood, stage)

    def set_quick_inventory(self, items: List[Dict[str, Any]]):
        """
        Update quick inventory display.

        Args:
            items: List of item dicts with keys: id, quantity, color
        """
        self.quick_inventory.clear_all()
        for i, item in enumerate(items[:HUD_QUICK_INV_SLOTS]):
            if item:
                self.quick_inventory.set_slot_item(
                    i,
                    item.get('id'),
                    item.get('quantity', 0),
                    item.get('color', (128, 128, 128))
                )

    # =========================================================================
    # NOTIFICATIONS
    # =========================================================================

    def add_notification(self, message: str, notification_type: str = NOTIFICATION_INFO,
                        duration: float = HUD_NOTIFICATION_DURATION):
        """
        Add a notification to display.

        Args:
            message: Notification text
            notification_type: NOTIFICATION_INFO, SUCCESS, WARNING, or ERROR
            duration: How long to display (seconds)
        """
        notification = Notification(
            message=message,
            notification_type=notification_type,
            duration=duration
        )

        # Add to front of list
        self._notifications.insert(0, notification)

        # Limit max notifications
        while len(self._notifications) > HUD_NOTIFICATION_MAX:
            self._notifications.pop()

    def clear_notifications(self):
        """Clear all notifications."""
        self._notifications.clear()

    # =========================================================================
    # INPUT HANDLING
    # =========================================================================

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle input events.

        Returns:
            True if event was consumed
        """
        if event.type == pygame.KEYDOWN:
            # Tab toggles HUD visibility
            if event.key == pygame.K_TAB:
                self.toggle_visibility()
                return True

            # M toggles minimap (placeholder)
            if event.key == pygame.K_m:
                self._show_minimap = not self._show_minimap
                return True

        # Pass to quick inventory
        if self._visible and self._mode == HUD_MODE_EXPLORATION:
            if self.quick_inventory.handle_event(event):
                return True

        return False

    # =========================================================================
    # UPDATE
    # =========================================================================

    def update(self, dt: float):
        """
        Update HUD state.

        Args:
            dt: Delta time in seconds
        """
        # Update dragon bars
        self.dragon_bars.update(dt)

        # Update notifications
        expired = []
        for notification in self._notifications:
            notification.elapsed += dt

            # Fade out in last second
            remaining = notification.duration - notification.elapsed
            if remaining < 1.0:
                notification.alpha = max(0.0, remaining)

            if notification.elapsed >= notification.duration:
                expired.append(notification)

        for notification in expired:
            self._notifications.remove(notification)

    # =========================================================================
    # DRAWING
    # =========================================================================

    def draw(self, surface: pygame.Surface):
        """
        Draw the entire HUD.

        Args:
            surface: Surface to draw on
        """
        if not self._visible:
            return

        # Draw based on mode
        self._draw_player_info(surface)
        self._draw_time_display(surface)
        self._draw_notifications(surface)

        if self._mode == HUD_MODE_EXPLORATION:
            self.dragon_bars.draw(surface)
            self.quick_inventory.draw(surface)
            if self._show_minimap:
                self._draw_minimap_placeholder(surface)

        elif self._mode == HUD_MODE_CAFE:
            # Cafe mode has different layout
            self._draw_cafe_info(surface)

    def _draw_player_info(self, surface: pygame.Surface):
        """Draw player info (top-left)."""
        # Panel background
        panel_width = 180
        panel_height = 55
        panel_rect = pygame.Rect(HUD_PLAYER_X, HUD_PLAYER_Y, panel_width, panel_height)

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (30, 28, 40, HUD_BG_ALPHA), panel_surface.get_rect(), border_radius=6)
        pygame.draw.rect(panel_surface, (60, 55, 75, 200), panel_surface.get_rect(), 1, border_radius=6)
        surface.blit(panel_surface, panel_rect)

        # Location name
        location_surface = self.text_font.render(self._location_name, True, UI_TEXT)
        surface.blit(location_surface, (HUD_PLAYER_X + 10, HUD_PLAYER_Y + 8))

        # Gold display
        gold_text = f"Gold: {self._gold}"
        gold_surface = self.text_font.render(gold_text, True, CAFE_CREAM)
        surface.blit(gold_surface, (HUD_PLAYER_X + 10, HUD_PLAYER_Y + 30))

        # Draw gold coin icon
        coin_x = HUD_PLAYER_X + 10 + gold_surface.get_width() + 5
        coin_y = HUD_PLAYER_Y + 34
        pygame.draw.circle(surface, (220, 180, 60), (coin_x + 8, coin_y + 6), 8)
        pygame.draw.circle(surface, (180, 140, 40), (coin_x + 8, coin_y + 6), 8, 2)

    def _draw_time_display(self, surface: pygame.Surface):
        """Draw time/date display (top-right)."""
        # Panel background
        panel_width = 160
        panel_height = 70
        panel_x = HUD_TIME_X - panel_width
        panel_rect = pygame.Rect(panel_x, HUD_TIME_Y, panel_width, panel_height)

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (30, 28, 40, HUD_BG_ALPHA), panel_surface.get_rect(), border_radius=6)
        pygame.draw.rect(panel_surface, (60, 55, 75, 200), panel_surface.get_rect(), 1, border_radius=6)
        surface.blit(panel_surface, panel_rect)

        # Time display
        time_surface = self.time_font.render(self._time_string, True, CAFE_CREAM)
        time_rect = time_surface.get_rect(centerx=panel_x + panel_width // 2, y=HUD_TIME_Y + 8)
        surface.blit(time_surface, time_rect)

        # Day display
        day_text = f"Day {self._day_number}"
        day_surface = self.text_font.render(day_text, True, UI_TEXT)
        surface.blit(day_surface, (panel_x + 10, HUD_TIME_Y + 38))

        # Season and weather icons (right side)
        icon_x = panel_x + panel_width - 45
        icon_y = HUD_TIME_Y + 42

        # Draw season icon
        self._draw_season_icon(surface, icon_x, icon_y, self._season)

        # Draw weather icon
        self._draw_weather_icon(surface, icon_x + 22, icon_y, self._weather)

    def _draw_season_icon(self, surface: pygame.Surface, x: int, y: int, season: str):
        """Draw a simple season icon."""
        if season == 'spring':
            # Flower icon
            pygame.draw.circle(surface, (220, 100, 140), (x, y), 6)
            pygame.draw.circle(surface, (255, 200, 100), (x, y), 3)
        elif season == 'summer':
            # Sun icon
            pygame.draw.circle(surface, (255, 220, 80), (x, y), 6)
            # Sun rays
            for i in range(8):
                import math
                angle = i * math.pi / 4
                ray_x = x + int(math.cos(angle) * 9)
                ray_y = y + int(math.sin(angle) * 9)
                pygame.draw.line(surface, (255, 220, 80), (x, y), (ray_x, ray_y), 1)

    def _draw_weather_icon(self, surface: pygame.Surface, x: int, y: int, weather: str):
        """Draw a simple weather icon."""
        if weather == WEATHER_SUNNY:
            pygame.draw.circle(surface, (255, 200, 60), (x, y), 5)
        elif weather == WEATHER_CLOUDY:
            pygame.draw.ellipse(surface, (180, 180, 190), (x - 6, y - 3, 12, 8))
            pygame.draw.ellipse(surface, (160, 160, 170), (x - 8, y, 10, 6))
        elif weather == WEATHER_RAINY:
            # Cloud
            pygame.draw.ellipse(surface, (120, 130, 150), (x - 6, y - 5, 12, 6))
            # Rain drops
            pygame.draw.line(surface, (100, 140, 200), (x - 3, y + 2), (x - 4, y + 6), 1)
            pygame.draw.line(surface, (100, 140, 200), (x + 2, y + 2), (x + 1, y + 6), 1)
        elif weather == WEATHER_STORMY:
            # Dark cloud
            pygame.draw.ellipse(surface, (80, 70, 100), (x - 7, y - 5, 14, 7))
            pygame.draw.ellipse(surface, (60, 50, 80), (x - 9, y - 2, 12, 6))
            # Lightning bolt
            pygame.draw.line(surface, (255, 255, 100), (x, y + 2), (x - 2, y + 5), 2)
            pygame.draw.line(surface, (255, 255, 100), (x - 2, y + 5), (x + 1, y + 5), 2)
            pygame.draw.line(surface, (255, 255, 100), (x + 1, y + 5), (x - 1, y + 9), 2)
        elif weather == WEATHER_SPECIAL:
            # Magical star/sparkle
            star_color = (220, 200, 255)
            # Draw a simple star shape
            pygame.draw.line(surface, star_color, (x, y - 6), (x, y + 6), 2)
            pygame.draw.line(surface, star_color, (x - 6, y), (x + 6, y), 2)
            # Diagonal lines for sparkle effect
            pygame.draw.line(surface, (255, 220, 255), (x - 4, y - 4), (x + 4, y + 4), 1)
            pygame.draw.line(surface, (255, 220, 255), (x + 4, y - 4), (x - 4, y + 4), 1)

    def _draw_notifications(self, surface: pygame.Surface):
        """Draw notification messages (top-center)."""
        if not self._notifications:
            return

        y_offset = 0
        for notification in self._notifications:
            color = NOTIFICATION_COLORS.get(notification.notification_type, NOTIFICATION_COLORS[NOTIFICATION_INFO])

            # Apply alpha
            alpha = int(notification.alpha * 255)

            # Render text
            text_surface = self.notification_font.render(notification.message, True, color)
            text_rect = text_surface.get_rect(centerx=HUD_NOTIFICATION_X, y=HUD_NOTIFICATION_Y + y_offset)

            # Background
            bg_rect = text_rect.inflate(20, 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_color = (30, 28, 40, int(alpha * 0.8))
            pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=4)
            surface.blit(bg_surface, bg_rect)

            # Text with alpha
            text_with_alpha = text_surface.copy()
            text_with_alpha.set_alpha(alpha)
            surface.blit(text_with_alpha, text_rect)

            y_offset += 35

    def _draw_minimap_placeholder(self, surface: pygame.Surface):
        """Draw minimap placeholder (bottom-right)."""
        panel_rect = pygame.Rect(HUD_MINIMAP_X, HUD_MINIMAP_Y, HUD_MINIMAP_SIZE, HUD_MINIMAP_SIZE)

        # Background
        panel_surface = pygame.Surface((HUD_MINIMAP_SIZE, HUD_MINIMAP_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (30, 28, 40, HUD_BG_ALPHA), panel_surface.get_rect(), border_radius=6)
        pygame.draw.rect(panel_surface, (60, 55, 75, 200), panel_surface.get_rect(), 1, border_radius=6)
        surface.blit(panel_surface, panel_rect)

        # Placeholder text
        text_surface = self.small_font.render("Minimap", True, UI_TEXT_DIM)
        text_rect = text_surface.get_rect(center=panel_rect.center)
        surface.blit(text_surface, text_rect)

        # Simple indicator dot for player position
        dot_x = panel_rect.centerx
        dot_y = panel_rect.centery + 10
        pygame.draw.circle(surface, CAFE_WARM, (dot_x, dot_y), 4)

    def _draw_cafe_info(self, surface: pygame.Surface):
        """Draw cafe-specific HUD elements (cafe mode only)."""
        # Bottom-left: Service status instead of dragon bars
        panel_width = 200
        panel_height = 60
        panel_x = HUD_DRAGON_X
        panel_y = HUD_DRAGON_Y

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (30, 28, 40, HUD_BG_ALPHA), panel_surface.get_rect(), border_radius=6)
        pygame.draw.rect(panel_surface, (60, 55, 75, 200), panel_surface.get_rect(), 1, border_radius=6)
        surface.blit(panel_surface, (panel_x, panel_y))

        # Cafe mode text
        text = "Cafe Mode"
        text_surface = self.text_font.render(text, True, CAFE_CREAM)
        surface.blit(text_surface, (panel_x + 10, panel_y + 10))

        hint = "Press TAB to toggle HUD"
        hint_surface = self.small_font.render(hint, True, UI_TEXT_DIM)
        surface.blit(hint_surface, (panel_x + 10, panel_y + 35))
