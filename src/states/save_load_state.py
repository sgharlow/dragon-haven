"""
Save/Load State for Dragon Haven Cafe.
Screen for selecting save slots to save or load games.
"""

import pygame
from typing import Optional, List
from datetime import datetime
from states.base_state import BaseScreen
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_PANEL, UI_BORDER, UI_HIGHLIGHT,
    UI_TEXT, UI_TEXT_DIM, CAFE_WARM, CAFE_CREAM, WHITE,
    DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
)
from save_manager import get_save_manager, SaveSlotInfo, SaveData
from ui.components import Button
from sound_manager import get_sound_manager


class SaveSlotCard:
    """Visual representation of a save slot."""

    def __init__(self, slot_info: SaveSlotInfo, x: int, y: int, width: int, height: int):
        """
        Initialize the save slot card.

        Args:
            slot_info: Information about this save slot
            x, y: Position
            width, height: Size
        """
        self.slot_info = slot_info
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        self.hover = False
        self.selected = False

        # Fonts
        self.title_font = pygame.font.Font(None, 32)
        self.body_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

    def update(self, mouse_pos: tuple) -> bool:
        """Update hover state. Returns True on hover enter."""
        was_hover = self.hover
        self.hover = self.rect.collidepoint(mouse_pos)
        return self.hover and not was_hover

    def draw(self, surface: pygame.Surface):
        """Draw the save slot card."""
        # Background
        if self.selected:
            bg_color = CAFE_WARM
        elif self.hover:
            bg_color = UI_HIGHLIGHT
        else:
            bg_color = UI_PANEL

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 2, border_radius=8)

        if self.slot_info.exists:
            self._draw_filled_slot(surface)
        else:
            self._draw_empty_slot(surface)

    def _draw_empty_slot(self, surface: pygame.Surface):
        """Draw an empty save slot."""
        # Slot number
        text = f"Slot {self.slot_info.slot} - Empty"
        text_surface = self.title_font.render(text, True, UI_TEXT_DIM)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def _draw_filled_slot(self, surface: pygame.Surface):
        """Draw a filled save slot with game info."""
        info = self.slot_info
        text_color = CAFE_CREAM if self.selected else UI_TEXT

        # Slot number and player name
        title = f"Slot {info.slot}: {info.player_name}"
        title_surface = self.title_font.render(title, True, text_color)
        surface.blit(title_surface, (self.x + 15, self.y + 12))

        # Dragon info with stage icon
        dragon_text = f"Dragon: {info.dragon_name or 'No Name'} ({info.dragon_stage})"
        dragon_surface = self.body_font.render(dragon_text, True, text_color)
        surface.blit(dragon_surface, (self.x + 15, self.y + 42))

        # Day and cafe level
        progress_text = f"Day {info.day_number} | Cafe Level {info.cafe_level}"
        progress_surface = self.body_font.render(progress_text, True, text_color)
        surface.blit(progress_surface, (self.x + 15, self.y + 66))

        # Playtime
        hours = int(info.playtime_seconds // 3600)
        minutes = int((info.playtime_seconds % 3600) // 60)
        playtime_text = f"Playtime: {hours}h {minutes}m"
        playtime_surface = self.small_font.render(playtime_text, True, UI_TEXT_DIM)
        surface.blit(playtime_surface, (self.x + self.width - 120, self.y + 15))

        # Last saved time
        if info.last_saved:
            try:
                saved_dt = datetime.fromisoformat(info.last_saved)
                saved_str = saved_dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                saved_str = "Unknown"
            saved_surface = self.small_font.render(saved_str, True, UI_TEXT_DIM)
            surface.blit(saved_surface, (self.x + self.width - 120, self.y + 35))

        # Draw mini dragon icon
        self._draw_dragon_icon(surface, info.dragon_stage)

    def _draw_dragon_icon(self, surface: pygame.Surface, stage: str):
        """Draw a small dragon icon based on stage."""
        icon_x = self.x + self.width - 50
        icon_y = self.y + self.height - 45
        icon_size = 30

        if stage == "egg":
            # Egg shape
            pygame.draw.ellipse(surface, CAFE_CREAM,
                              (icon_x, icon_y, icon_size * 0.7, icon_size), 0)
            pygame.draw.ellipse(surface, UI_BORDER,
                              (icon_x, icon_y, icon_size * 0.7, icon_size), 1)
        elif stage == "hatchling":
            # Small dragon head
            pygame.draw.circle(surface, (100, 180, 100),
                             (icon_x + icon_size // 2, icon_y + icon_size // 2),
                             icon_size // 3)
            # Eyes
            pygame.draw.circle(surface, WHITE,
                             (icon_x + icon_size // 2 - 3, icon_y + icon_size // 2 - 2), 3)
            pygame.draw.circle(surface, WHITE,
                             (icon_x + icon_size // 2 + 3, icon_y + icon_size // 2 - 2), 3)
        else:  # juvenile
            # Larger dragon head
            pygame.draw.circle(surface, (80, 160, 80),
                             (icon_x + icon_size // 2, icon_y + icon_size // 2),
                             icon_size // 2.5)
            # Horns
            pygame.draw.polygon(surface, (60, 140, 60), [
                (icon_x + 5, icon_y + 8),
                (icon_x + 10, icon_y),
                (icon_x + 12, icon_y + 10),
            ])


class ConfirmDeleteDialog:
    """Dialog to confirm save deletion."""

    def __init__(self, slot: int, on_confirm, on_cancel):
        """Initialize the dialog."""
        self.slot = slot
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        # Dialog dimensions
        self.width = 350
        self.height = 150
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Buttons
        btn_width = 100
        btn_height = 40
        btn_y = self.y + self.height - btn_height - 20
        self.confirm_btn = Button(
            self.x + 40, btn_y, btn_width, btn_height,
            "Delete", on_click=on_confirm
        )
        self.cancel_btn = Button(
            self.x + self.width - btn_width - 40, btn_y, btn_width, btn_height,
            "Cancel", on_click=on_cancel
        )

        self.font = pygame.font.Font(None, 28)

    def handle_event(self, event) -> bool:
        """Handle input events."""
        if self.confirm_btn.handle_event(event):
            return True
        if self.cancel_btn.handle_event(event):
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_cancel()
                return True
        return False

    def draw(self, surface: pygame.Surface):
        """Draw the dialog."""
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        # Dialog background
        pygame.draw.rect(surface, UI_BG, self.rect, border_radius=10)
        pygame.draw.rect(surface, UI_BORDER, self.rect, 3, border_radius=10)

        # Message
        message = f"Delete save in Slot {self.slot}?"
        text_surface = self.font.render(message, True, UI_TEXT)
        text_rect = text_surface.get_rect(centerx=self.x + self.width // 2, y=self.y + 30)
        surface.blit(text_surface, text_rect)

        warning = "This cannot be undone!"
        warn_surface = self.font.render(warning, True, CAFE_WARM)
        warn_rect = warn_surface.get_rect(centerx=self.x + self.width // 2, y=self.y + 60)
        surface.blit(warn_surface, warn_rect)

        # Buttons
        self.confirm_btn.draw(surface)
        self.cancel_btn.draw(surface)


class SaveLoadState(BaseScreen):
    """
    Save/Load screen for managing game saves.

    Features:
    - 3 save slots
    - Save current game to slot
    - Load game from slot
    - Delete saves
    - Shows save info (playtime, day, dragon stage)

    Mode can be 'save' or 'load'.
    """

    def __init__(self, game, mode: str = 'save'):
        """
        Initialize the save/load screen.

        Args:
            game: Game instance
            mode: 'save' or 'load'
        """
        super().__init__(game)
        self.mode = mode
        self.title = "Save Game" if mode == 'save' else "Load Game"
        self.background_color = UI_BG

        # State
        self.save_manager = get_save_manager()
        self.slot_cards: List[SaveSlotCard] = []
        self.selected_slot: Optional[int] = None
        self.confirm_dialog: Optional[ConfirmDeleteDialog] = None

        # Buttons
        self.action_btn: Optional[Button] = None
        self.delete_btn: Optional[Button] = None
        self.back_btn: Optional[Button] = None

        # Sound
        self.sound = get_sound_manager()

        # Fonts
        self.hint_font = None

    def enter(self, previous_state=None):
        """Initialize screen when entering."""
        super().enter(previous_state)

        # Initialize save manager if needed
        if not self.save_manager._initialized:
            self.save_manager.initialize()

        # Initialize fonts
        self.hint_font = pygame.font.Font(None, 24)

        # Load slot info
        self._refresh_slots()

        # Create buttons
        btn_y = SCREEN_HEIGHT - 80
        btn_width = 140
        btn_height = 45

        # Action button (Save/Load)
        action_text = "Save" if self.mode == 'save' else "Load"
        self.action_btn = Button(
            SCREEN_WIDTH // 2 - btn_width - 80, btn_y,
            btn_width, btn_height, action_text,
            on_click=self._do_action
        )

        # Delete button
        self.delete_btn = Button(
            SCREEN_WIDTH // 2 + 80, btn_y,
            btn_width, btn_height, "Delete",
            on_click=self._do_delete
        )

        # Back button
        self.back_btn = Button(
            50, btn_y, 100, btn_height, "Back",
            on_click=self._go_back
        )

    def _refresh_slots(self):
        """Refresh save slot information and cards."""
        slots = self.save_manager.list_saves()

        # Create slot cards
        card_width = 400
        card_height = 100
        card_x = (SCREEN_WIDTH - card_width) // 2
        card_y_start = 120
        card_spacing = 120

        self.slot_cards = []
        for i, slot_info in enumerate(slots):
            y = card_y_start + i * card_spacing
            card = SaveSlotCard(slot_info, card_x, y, card_width, card_height)
            self.slot_cards.append(card)

        # Select first slot by default
        if self.slot_cards:
            self.selected_slot = 1
            self.slot_cards[0].selected = True

    def handle_event(self, event):
        """Handle input events."""
        # Handle confirm dialog first
        if self.confirm_dialog:
            self.confirm_dialog.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._go_back()
            elif event.key == pygame.K_UP:
                self._select_slot(self.selected_slot - 1 if self.selected_slot else 1)
            elif event.key == pygame.K_DOWN:
                self._select_slot(self.selected_slot + 1 if self.selected_slot else 1)
            elif event.key == pygame.K_RETURN:
                self._do_action()
            elif event.key == pygame.K_DELETE:
                self._do_delete()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check slot card clicks
                for card in self.slot_cards:
                    if card.rect.collidepoint(event.pos):
                        self._select_slot(card.slot_info.slot)
                        break

        # Handle button events
        if self.action_btn:
            self.action_btn.handle_event(event)
        if self.delete_btn:
            self.delete_btn.handle_event(event)
        if self.back_btn:
            self.back_btn.handle_event(event)

    def _select_slot(self, slot: int):
        """Select a save slot."""
        if 1 <= slot <= 3:
            self.selected_slot = slot
            for card in self.slot_cards:
                card.selected = (card.slot_info.slot == slot)
            self.sound.play('ui_hover')

    def _do_action(self):
        """Perform the save or load action."""
        if not self.selected_slot:
            return

        slot_info = self.slot_cards[self.selected_slot - 1].slot_info

        if self.mode == 'save':
            self._save_to_slot(self.selected_slot)
        else:  # load
            if slot_info.exists:
                self._load_from_slot(self.selected_slot)

    def _save_to_slot(self, slot: int):
        """Save current game to slot."""
        # TODO: Get current game state from game systems
        # For now, create placeholder save data
        save_data = SaveData()
        save_data.player.name = "Player"
        save_data.dragon.name = "Ember"
        save_data.dragon.stage = "hatchling"
        save_data.world.day_number = 3
        save_data.cafe.level = 1

        if self.save_manager.save(slot, save_data):
            self.sound.play('ui_confirm')
            self._refresh_slots()
            # Show success message (could add a notification)
        else:
            self.sound.play('error')

    def _load_from_slot(self, slot: int):
        """Load game from slot."""
        save_data = self.save_manager.load(slot)
        if save_data:
            self.sound.play('ui_confirm')
            # TODO: Apply save data to game systems
            # For now, just go to exploration
            self.fade_to_state("exploration")
        else:
            self.sound.play('error')

    def _do_delete(self):
        """Show delete confirmation dialog."""
        if not self.selected_slot:
            return

        slot_info = self.slot_cards[self.selected_slot - 1].slot_info
        if not slot_info.exists:
            return

        self.confirm_dialog = ConfirmDeleteDialog(
            self.selected_slot,
            on_confirm=self._confirm_delete,
            on_cancel=self._cancel_delete
        )

    def _confirm_delete(self):
        """Confirmed deletion of save."""
        if self.selected_slot:
            self.save_manager.delete_save(self.selected_slot)
            self.sound.play('ui_confirm')
            self._refresh_slots()
        self.confirm_dialog = None

    def _cancel_delete(self):
        """Cancelled deletion."""
        self.confirm_dialog = None

    def _go_back(self):
        """Go back to previous screen."""
        self.fade_to_state("pause_menu")

    def update(self, dt):
        """Update the screen."""
        super().update(dt)

        # Update slot card hover states
        mouse_pos = pygame.mouse.get_pos()
        for card in self.slot_cards:
            card.update(mouse_pos)

        return True

    def draw(self, screen):
        """Draw the save/load screen."""
        super().draw(screen)

        # Draw slot cards
        for card in self.slot_cards:
            card.draw(screen)

        # Draw buttons
        if self.action_btn:
            self.action_btn.draw(screen)
        if self.delete_btn:
            self.delete_btn.draw(screen)
        if self.back_btn:
            self.back_btn.draw(screen)

        # Draw hints
        hints = "↑↓: Select Slot | Enter: Confirm | Del: Delete | Esc: Back"
        hint_surface = self.hint_font.render(hints, True, UI_TEXT_DIM)
        hint_rect = hint_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 25)
        screen.blit(hint_surface, hint_rect)

        # Draw confirm dialog if active
        if self.confirm_dialog:
            self.confirm_dialog.draw(screen)

        # Draw fade overlay
        self.draw_fade_overlay(screen)
