"""
Dialogue Box UI Component for Dragon Haven Cafe.
Displays dialogue with typewriter effect, portraits, and choices.
"""

import pygame
from typing import Optional, List, Tuple, Callable
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_CREAM, CAFE_WARM, BLACK,
)
from systems.dialogue import DialogueNode, DialogueChoice


class DialogueBox:
    """
    A dialogue box UI component with typewriter effect.

    Usage:
        box = DialogueBox()
        box.show_dialogue(node, available_choices)
        box.update(dt)
        box.draw(surface)
        # Handle input:
        if box.handle_click(pos):
            # Clicked to advance
        if box.handle_key(event):
            # Key pressed
    """

    # Layout constants
    BOX_HEIGHT = 180
    BOX_MARGIN = 20
    PORTRAIT_SIZE = 120
    PADDING = 15
    CHOICE_HEIGHT = 35

    # Typewriter speed (characters per second)
    DEFAULT_TYPE_SPEED = 40

    def __init__(self):
        """Initialize the dialogue box."""
        self._visible = False

        # Current content
        self._speaker = ""
        self._portrait_id = ""
        self._full_text = ""
        self._displayed_text = ""
        self._choices: List[DialogueChoice] = []

        # Typewriter state
        self._char_index = 0.0
        self._type_speed = self.DEFAULT_TYPE_SPEED
        self._is_typing = False

        # Choice selection
        self._selected_choice = 0
        self._hover_choice = -1

        # Animation
        self._alpha = 0
        self._target_alpha = 0
        self._fade_speed = 800

        # Callbacks
        self._on_advance: Optional[Callable] = None
        self._on_choice: Optional[Callable[[int], None]] = None

        # Fonts
        self.speaker_font = pygame.font.Font(None, 28)
        self.text_font = pygame.font.Font(None, 24)
        self.choice_font = pygame.font.Font(None, 22)

        # Calculate box rect
        self._box_rect = pygame.Rect(
            self.BOX_MARGIN,
            SCREEN_HEIGHT - self.BOX_HEIGHT - self.BOX_MARGIN,
            SCREEN_WIDTH - self.BOX_MARGIN * 2,
            self.BOX_HEIGHT
        )

        # Portrait rect
        self._portrait_rect = pygame.Rect(
            self._box_rect.x + self.PADDING,
            self._box_rect.y + self.PADDING,
            self.PORTRAIT_SIZE,
            self.PORTRAIT_SIZE - 30
        )

        # Text area
        self._text_x = self._portrait_rect.right + self.PADDING
        self._text_y = self._box_rect.y + 45
        self._text_width = self._box_rect.right - self._text_x - self.PADDING

    def show_dialogue(self, node: DialogueNode, available_choices: List[DialogueChoice] = None):
        """
        Show a dialogue node.

        Args:
            node: The dialogue node to display
            available_choices: Pre-filtered available choices
        """
        self._visible = True
        self._target_alpha = 255

        self._speaker = node.speaker
        self._portrait_id = node.portrait
        self._full_text = node.text
        self._displayed_text = ""
        self._char_index = 0.0
        self._is_typing = True

        self._choices = available_choices or []
        self._selected_choice = 0

    def show_text(self, speaker: str, text: str, portrait: str = "",
                  choices: List[DialogueChoice] = None):
        """
        Show custom text without a node.

        Args:
            speaker: Speaker name
            text: Text to display
            portrait: Portrait ID
            choices: Optional choices
        """
        self._visible = True
        self._target_alpha = 255

        self._speaker = speaker
        self._portrait_id = portrait
        self._full_text = text
        self._displayed_text = ""
        self._char_index = 0.0
        self._is_typing = True

        self._choices = choices or []
        self._selected_choice = 0

    def hide(self):
        """Hide the dialogue box."""
        self._target_alpha = 0

    def is_visible(self) -> bool:
        """Check if dialogue box is visible."""
        return self._visible

    def is_typing(self) -> bool:
        """Check if typewriter effect is still running."""
        return self._is_typing

    def skip_typing(self):
        """Skip typewriter effect and show full text."""
        self._displayed_text = self._full_text
        self._char_index = len(self._full_text)
        self._is_typing = False

    def has_choices(self) -> bool:
        """Check if there are choices to display."""
        return len(self._choices) > 0

    def set_type_speed(self, chars_per_second: float):
        """Set typewriter speed."""
        self._type_speed = chars_per_second

    def on_advance(self, callback: Callable):
        """Set callback for advancing dialogue."""
        self._on_advance = callback

    def on_choice(self, callback: Callable[[int], None]):
        """Set callback for selecting a choice."""
        self._on_choice = callback

    def update(self, dt: float):
        """Update dialogue box state."""
        # Update fade
        if self._alpha < self._target_alpha:
            self._alpha = min(self._target_alpha, self._alpha + self._fade_speed * dt)
        elif self._alpha > self._target_alpha:
            self._alpha = max(self._target_alpha, self._alpha - self._fade_speed * dt)

        if self._alpha <= 0:
            self._visible = False

        # Update typewriter
        if self._is_typing:
            self._char_index += self._type_speed * dt
            chars_to_show = int(self._char_index)
            if chars_to_show >= len(self._full_text):
                self._displayed_text = self._full_text
                self._is_typing = False
            else:
                self._displayed_text = self._full_text[:chars_to_show]

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """
        Handle mouse click.

        Returns:
            True if click was handled
        """
        if not self._visible or self._alpha < 200:
            return False

        # Check if clicking on a choice
        if self.has_choices() and not self._is_typing:
            choice_y = self._box_rect.bottom + 10
            for i, choice in enumerate(self._choices):
                choice_rect = pygame.Rect(
                    self._text_x,
                    choice_y + i * (self.CHOICE_HEIGHT + 5),
                    self._text_width,
                    self.CHOICE_HEIGHT
                )
                if choice_rect.collidepoint(pos):
                    self._selected_choice = i
                    if self._on_choice:
                        self._on_choice(i)
                    return True

        # Check if clicking on dialogue box
        if self._box_rect.collidepoint(pos):
            if self._is_typing:
                self.skip_typing()
            elif not self.has_choices():
                if self._on_advance:
                    self._on_advance()
            return True

        return False

    def handle_key(self, event: pygame.event.Event) -> bool:
        """
        Handle key press.

        Returns:
            True if key was handled
        """
        if not self._visible or self._alpha < 200:
            return False

        if event.type != pygame.KEYDOWN:
            return False

        # Space or Enter to advance/skip
        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
            if self._is_typing:
                self.skip_typing()
                return True
            elif self.has_choices():
                if self._on_choice:
                    self._on_choice(self._selected_choice)
                return True
            else:
                if self._on_advance:
                    self._on_advance()
                return True

        # Arrow keys for choice navigation
        if self.has_choices() and not self._is_typing:
            if event.key == pygame.K_UP:
                self._selected_choice = max(0, self._selected_choice - 1)
                return True
            elif event.key == pygame.K_DOWN:
                self._selected_choice = min(len(self._choices) - 1,
                                           self._selected_choice + 1)
                return True

        return False

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion for hover effects."""
        if not self._visible or not self.has_choices() or self._is_typing:
            self._hover_choice = -1
            return

        choice_y = self._box_rect.bottom + 10
        self._hover_choice = -1
        for i, choice in enumerate(self._choices):
            choice_rect = pygame.Rect(
                self._text_x,
                choice_y + i * (self.CHOICE_HEIGHT + 5),
                self._text_width,
                self.CHOICE_HEIGHT
            )
            if choice_rect.collidepoint(pos):
                self._hover_choice = i
                break

    def draw(self, surface: pygame.Surface):
        """Draw the dialogue box."""
        if not self._visible or self._alpha <= 0:
            return

        alpha = int(self._alpha)

        # Create dialogue surface
        dialogue_surface = pygame.Surface(
            (self._box_rect.width, self._box_rect.height +
             len(self._choices) * (self.CHOICE_HEIGHT + 5) + 20),
            pygame.SRCALPHA
        )

        # Draw main box background
        box_bg = (35, 30, 45, min(230, alpha))
        pygame.draw.rect(dialogue_surface, box_bg,
                        (0, 0, self._box_rect.width, self._box_rect.height),
                        border_radius=10)

        # Draw border
        border_color = (95, 85, 115, alpha)
        pygame.draw.rect(dialogue_surface, border_color,
                        (0, 0, self._box_rect.width, self._box_rect.height),
                        2, border_radius=10)

        # Draw portrait background
        portrait_x = self.PADDING
        portrait_y = self.PADDING
        portrait_bg = (50, 45, 65, alpha)
        pygame.draw.rect(dialogue_surface, portrait_bg,
                        (portrait_x, portrait_y,
                         self.PORTRAIT_SIZE, self.PORTRAIT_SIZE - 30),
                        border_radius=6)

        # Draw portrait placeholder (or actual portrait)
        self._draw_portrait(dialogue_surface, portrait_x, portrait_y, alpha)

        # Draw speaker name
        text_x = self.PORTRAIT_SIZE + self.PADDING * 2
        speaker_color = (255, 245, 220, alpha)
        speaker_surface = self.speaker_font.render(self._speaker, True, speaker_color[:3])
        speaker_surface.set_alpha(alpha)
        dialogue_surface.blit(speaker_surface, (text_x, self.PADDING))

        # Draw text with word wrapping
        text_y = self.PADDING + 30
        text_color = (220, 210, 230, alpha)
        self._draw_wrapped_text(dialogue_surface, self._displayed_text,
                               text_x, text_y, self._text_width, text_color[:3], alpha)

        # Draw continue indicator if not typing and no choices
        if not self._is_typing and not self.has_choices():
            indicator = "Click or press SPACE to continue..."
            ind_surface = pygame.font.Font(None, 18).render(indicator, True, (150, 140, 170))
            ind_surface.set_alpha(int(alpha * (0.5 + 0.5 * abs(pygame.time.get_ticks() / 500 % 2 - 1))))
            dialogue_surface.blit(ind_surface,
                                 (self._box_rect.width - ind_surface.get_width() - 15,
                                  self._box_rect.height - 25))

        # Blit main box
        surface.blit(dialogue_surface, self._box_rect.topleft)

        # Draw choices (below main box)
        if self.has_choices() and not self._is_typing:
            self._draw_choices(surface, alpha)

    def _draw_portrait(self, surface: pygame.Surface, x: int, y: int, alpha: int):
        """Draw the character portrait."""
        # For now, draw a placeholder based on portrait_id
        center_x = x + self.PORTRAIT_SIZE // 2
        center_y = y + (self.PORTRAIT_SIZE - 30) // 2

        if not self._portrait_id:
            # No portrait - draw question mark
            font = pygame.font.Font(None, 48)
            text = font.render("?", True, (100, 95, 115))
            text.set_alpha(alpha)
            text_rect = text.get_rect(center=(center_x, center_y))
            surface.blit(text, text_rect)
            return

        # Draw simple character representation based on portrait ID
        if 'dragon' in self._portrait_id.lower():
            # Dragon portrait
            self._draw_dragon_portrait(surface, center_x, center_y, alpha)
        elif 'player' in self._portrait_id.lower():
            # Player portrait
            self._draw_player_portrait(surface, center_x, center_y, alpha)
        else:
            # Generic NPC portrait
            self._draw_npc_portrait(surface, center_x, center_y, alpha)

    def _draw_dragon_portrait(self, surface: pygame.Surface, cx: int, cy: int, alpha: int):
        """Draw a dragon portrait."""
        color = (100, 180, 120, alpha)
        # Head
        pygame.draw.ellipse(surface, color[:3], (cx - 25, cy - 20, 50, 40))
        # Eyes
        pygame.draw.ellipse(surface, (255, 255, 255), (cx - 15, cy - 15, 12, 10))
        pygame.draw.ellipse(surface, (255, 255, 255), (cx + 3, cy - 15, 12, 10))
        pygame.draw.circle(surface, (40, 40, 40), (cx - 9, cy - 12), 4)
        pygame.draw.circle(surface, (40, 40, 40), (cx + 9, cy - 12), 4)
        # Horns
        pygame.draw.polygon(surface, (80, 140, 100), [
            (cx - 20, cy - 15), (cx - 25, cy - 35), (cx - 10, cy - 15)
        ])
        pygame.draw.polygon(surface, (80, 140, 100), [
            (cx + 10, cy - 15), (cx + 25, cy - 35), (cx + 20, cy - 15)
        ])

    def _draw_player_portrait(self, surface: pygame.Surface, cx: int, cy: int, alpha: int):
        """Draw a player portrait."""
        # Head
        pygame.draw.circle(surface, (240, 200, 160), (cx, cy - 5), 25)
        # Hair
        pygame.draw.ellipse(surface, (100, 70, 50), (cx - 25, cy - 35, 50, 30))
        # Eyes
        pygame.draw.ellipse(surface, (60, 60, 60), (cx - 12, cy - 10, 8, 6))
        pygame.draw.ellipse(surface, (60, 60, 60), (cx + 4, cy - 10, 8, 6))
        # Smile
        pygame.draw.arc(surface, (60, 60, 60), (cx - 10, cy, 20, 12), 3.14, 0, 2)

    def _draw_npc_portrait(self, surface: pygame.Surface, cx: int, cy: int, alpha: int):
        """Draw a generic NPC portrait."""
        # Head
        pygame.draw.circle(surface, (200, 180, 160), (cx, cy - 5), 25)
        # Eyes
        pygame.draw.circle(surface, (60, 60, 60), (cx - 10, cy - 8), 4)
        pygame.draw.circle(surface, (60, 60, 60), (cx + 10, cy - 8), 4)
        # Mouth
        pygame.draw.line(surface, (60, 60, 60), (cx - 8, cy + 8), (cx + 8, cy + 8), 2)

    def _draw_wrapped_text(self, surface: pygame.Surface, text: str,
                          x: int, y: int, max_width: int, color: Tuple, alpha: int):
        """Draw text with word wrapping."""
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = self.text_font.render(word + ' ', True, color)
            word_width = word_surface.get_width()

            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(' '.join(current_line))

        line_height = 24
        for i, line in enumerate(lines[:5]):  # Max 5 lines
            line_surface = self.text_font.render(line, True, color)
            line_surface.set_alpha(alpha)
            surface.blit(line_surface, (x, y + i * line_height))

    def _draw_choices(self, surface: pygame.Surface, alpha: int):
        """Draw choice buttons."""
        choice_y = self._box_rect.bottom + 10

        for i, choice in enumerate(self._choices):
            choice_rect = pygame.Rect(
                self._text_x,
                choice_y + i * (self.CHOICE_HEIGHT + 5),
                self._text_width,
                self.CHOICE_HEIGHT
            )

            # Background
            if i == self._selected_choice:
                bg_color = (80, 70, 100, min(220, alpha))
                border_color = (160, 140, 180, alpha)
            elif i == self._hover_choice:
                bg_color = (60, 55, 80, min(200, alpha))
                border_color = (120, 110, 140, alpha)
            else:
                bg_color = (45, 40, 55, min(200, alpha))
                border_color = (80, 75, 95, alpha)

            choice_surface = pygame.Surface((choice_rect.width, choice_rect.height),
                                           pygame.SRCALPHA)
            pygame.draw.rect(choice_surface, bg_color,
                           (0, 0, choice_rect.width, choice_rect.height),
                           border_radius=6)
            pygame.draw.rect(choice_surface, border_color,
                           (0, 0, choice_rect.width, choice_rect.height),
                           2, border_radius=6)

            # Choice number
            num_color = (180, 160, 200, alpha)
            num_text = f"{i + 1}."
            num_surface = self.choice_font.render(num_text, True, num_color[:3])
            num_surface.set_alpha(alpha)
            choice_surface.blit(num_surface, (10, 8))

            # Choice text
            text_color = (240, 230, 250, alpha) if i == self._selected_choice else (200, 190, 210, alpha)
            text_surface = self.choice_font.render(choice.text, True, text_color[:3])
            text_surface.set_alpha(alpha)
            choice_surface.blit(text_surface, (35, 8))

            surface.blit(choice_surface, choice_rect.topleft)
