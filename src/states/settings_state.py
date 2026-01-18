"""
Settings Screen for Dragon Haven Cafe.
Allows players to adjust game options.
"""

import pygame
import json
import os
from states.base_state import BaseScreen
from ui.components import Slider, Toggle, Selector, Button
from sound_manager import get_sound_manager
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_WARM, CAFE_CREAM,
    DEFAULT_SETTINGS, SETTINGS_FILE,
    GAME_SPEED_OPTIONS, GAME_SPEED_LABELS,
    COOKING_DIFFICULTY_OPTIONS, COOKING_DIFFICULTY_LABELS,
)


class SettingsState(BaseScreen):
    """
    Settings screen for adjusting game options.
    """

    def __init__(self, game):
        """Initialize the settings state."""
        super().__init__(game)
        self.title = "Settings"

        # Current settings (loaded from file or defaults)
        self.settings = dict(DEFAULT_SETTINGS)

        # UI components
        self.sliders: list[Slider] = []
        self.toggles: list[Toggle] = []
        self.selectors: list[Selector] = []
        self.buttons: list[Button] = []

        # Track which screen we came from
        self.previous_screen = "main_menu"

        # Sound manager
        self.sound = get_sound_manager()

    def enter(self, previous_state=None):
        """Initialize settings screen."""
        super().enter(previous_state)

        # Remember where we came from
        if previous_state:
            self.previous_screen = previous_state

        # Load settings
        self.load_settings()

        # Create UI components
        self._create_ui()

    def _create_ui(self):
        """Create all UI components."""
        self.sliders = []
        self.toggles = []
        self.selectors = []
        self.buttons = []

        # Layout
        label_x = 320  # Right edge of labels
        control_x = 340  # Left edge of controls
        y_start = 150
        y_spacing = 60

        y = y_start

        # === AUDIO SECTION ===
        # Section header drawn in draw()

        # Master Volume
        self.sliders.append(Slider(
            control_x, y, 200, 0, 100, self.settings['master_volume'],
            label="Master Volume",
            on_change=lambda v: self._on_setting_change('master_volume', v)
        ))
        y += y_spacing

        # SFX Volume
        self.sliders.append(Slider(
            control_x, y, 200, 0, 100, self.settings['sfx_volume'],
            label="SFX Volume",
            on_change=lambda v: self._on_setting_change('sfx_volume', v)
        ))
        y += y_spacing

        # Music Volume
        self.sliders.append(Slider(
            control_x, y, 200, 0, 100, self.settings['music_volume'],
            label="Music Volume",
            on_change=lambda v: self._on_setting_change('music_volume', v)
        ))
        y += y_spacing + 20  # Extra spacing before next section

        # === GAMEPLAY SECTION ===

        # Game Speed
        speed_idx = GAME_SPEED_OPTIONS.index(self.settings['game_speed']) if self.settings['game_speed'] in GAME_SPEED_OPTIONS else 1
        self.selectors.append(Selector(
            control_x, y, 200, GAME_SPEED_OPTIONS, GAME_SPEED_LABELS,
            selected=speed_idx, label="Game Speed",
            on_change=lambda v: self._on_setting_change('game_speed', v)
        ))
        y += y_spacing

        # Cooking Difficulty
        diff_idx = COOKING_DIFFICULTY_OPTIONS.index(self.settings['cooking_difficulty']) if self.settings['cooking_difficulty'] in COOKING_DIFFICULTY_OPTIONS else 1
        self.selectors.append(Selector(
            control_x, y, 200, COOKING_DIFFICULTY_OPTIONS, COOKING_DIFFICULTY_LABELS,
            selected=diff_idx, label="Cooking Difficulty",
            on_change=lambda v: self._on_setting_change('cooking_difficulty', v)
        ))
        y += y_spacing + 20

        # === DISPLAY SECTION ===

        # Fullscreen Toggle
        self.toggles.append(Toggle(
            control_x, y, self.settings['fullscreen'],
            label="Fullscreen",
            on_change=lambda v: self._on_setting_change('fullscreen', v)
        ))
        y += y_spacing + 40

        # === BUTTONS ===

        button_y = SCREEN_HEIGHT - 120
        button_width = 150
        button_height = 45
        button_spacing = 20

        # Calculate centered position for 3 buttons
        total_width = button_width * 3 + button_spacing * 2
        start_x = (SCREEN_WIDTH - total_width) // 2

        # Reset to Defaults
        self.buttons.append(Button(
            start_x, button_y, button_width, button_height,
            "Reset Defaults",
            on_click=self._reset_defaults
        ))

        # Apply & Save
        self.buttons.append(Button(
            start_x + button_width + button_spacing, button_y, button_width, button_height,
            "Apply",
            on_click=self._apply_settings
        ))

        # Back
        self.buttons.append(Button(
            start_x + (button_width + button_spacing) * 2, button_y, button_width, button_height,
            "Back",
            on_click=self._go_back
        ))

    def _on_setting_change(self, key: str, value):
        """Handle setting change."""
        self.settings[key] = value
        self._apply_preview()
        self.sound.play('ui_click', 0.5)

    def _apply_preview(self):
        """Apply settings preview (before saving)."""
        # Apply volume changes immediately
        master = self.settings['master_volume'] / 100
        sfx = self.settings['sfx_volume'] / 100
        music = self.settings['music_volume'] / 100

        self.sound.set_volume('master', master)
        self.sound.set_volume('ui', sfx)
        self.sound.set_volume('cooking', sfx)
        self.sound.set_volume('dragon', sfx)
        self.sound.set_volume('ambient', music)

    def _apply_settings(self):
        """Apply and save settings."""
        self.save_settings()
        self.sound.play('ui_confirm')

    def _reset_defaults(self):
        """Reset all settings to defaults."""
        self.settings = dict(DEFAULT_SETTINGS)
        self._create_ui()  # Recreate UI with new values
        self._apply_preview()
        self.sound.play('ui_cancel')

    def _go_back(self):
        """Return to previous screen."""
        self.save_settings()
        self.sound.play('ui_confirm')
        self.fade_to_state(self.previous_screen)

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._go_back()
                return

        # Pass to UI components
        for slider in self.sliders:
            if slider.handle_event(event):
                return

        for toggle in self.toggles:
            if toggle.handle_event(event):
                return

        for selector in self.selectors:
            if selector.handle_event(event):
                return

        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self, dt):
        """Update settings screen."""
        super().update(dt)
        return True

    def draw(self, screen):
        """Draw the settings screen."""
        # Background
        screen.fill(self.background_color)

        # Title
        title_font = pygame.font.Font(None, 56)
        title_surface = title_font.render("Settings", True, CAFE_CREAM)
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=50)
        screen.blit(title_surface, title_rect)

        # Section headers
        section_font = pygame.font.Font(None, 36)

        # Audio section
        audio_y = 130
        audio_text = section_font.render("Audio", True, CAFE_WARM)
        screen.blit(audio_text, (100, audio_y))

        # Gameplay section
        gameplay_y = 130 + 60 * 3 + 10
        gameplay_text = section_font.render("Gameplay", True, CAFE_WARM)
        screen.blit(gameplay_text, (100, gameplay_y))

        # Display section
        display_y = gameplay_y + 60 * 2 + 10
        display_text = section_font.render("Display", True, CAFE_WARM)
        screen.blit(display_text, (100, display_y))

        # Draw UI components
        for slider in self.sliders:
            slider.draw(screen)

        for toggle in self.toggles:
            toggle.draw(screen)

        for selector in self.selectors:
            selector.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        # Draw fade overlay
        self.draw_fade_overlay(screen)

    # =========================================================================
    # SETTINGS PERSISTENCE
    # =========================================================================

    def load_settings(self):
        """Load settings from file."""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults (in case new settings were added)
                    for key, value in loaded.items():
                        if key in self.settings:
                            self.settings[key] = value
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load settings: {e}")
            self.settings = dict(DEFAULT_SETTINGS)

        self._apply_preview()

    def save_settings(self):
        """Save settings to file."""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")
