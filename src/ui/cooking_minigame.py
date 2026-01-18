"""
Cooking Minigame for Dragon Haven Cafe.
A rhythm-based cooking game where players hit notes in time with patterns.
"""

import pygame
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable

from constants import (
    COOKING_LANES, COOKING_LANE_KEYS, COOKING_LANE_KEYS_ALT,
    TIMING_PERFECT, TIMING_GOOD, TIMING_OK,
    GRADE_PERFECT, GRADE_GOOD, GRADE_OK, GRADE_MISS,
    SCORE_PERFECT, SCORE_GOOD, SCORE_OK, SCORE_MISS,
    COMBO_MULTIPLIER_THRESHOLDS,
    COOKING_NOTE_SPEED, COOKING_NOTE_SPEED_EASY,
    COOKING_NOTE_WIDTH, COOKING_NOTE_HEIGHT, COOKING_HIT_LINE_Y,
    COOKING_DURATION_BASE, COOKING_DURATION_PER_DIFFICULTY,
    COOKING_NOTES_PER_SECOND_BASE, COOKING_NOTES_PER_SECOND_PER_DIFFICULTY,
    QUALITY_SCORE_THRESHOLDS, INGREDIENT_QUALITY_BONUS,
    EASY_MODE_TIMING_MULTIPLIER,
    COOKING_LANE_WIDTH, COOKING_LANE_SPACING, COOKING_LANE_COLORS,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM, WHITE, BLACK,
)


@dataclass
class Note:
    """A single note in the rhythm game."""
    lane: int           # Which lane (0-3)
    target_time: float  # When the note should be hit (in seconds)
    y: float = 0.0      # Current y position
    hit: bool = False   # Has been hit
    missed: bool = False  # Has been missed (passed hit line)
    grade: str = ''     # Grade received if hit


@dataclass
class CookingResult:
    """Result of a cooking minigame session."""
    recipe_id: str
    total_score: int
    max_possible_score: int
    score_percentage: float
    final_quality: int        # 1-5 stars
    perfect_count: int
    good_count: int
    ok_count: int
    miss_count: int
    max_combo: int
    ingredient_quality_bonus: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            'recipe_id': self.recipe_id,
            'total_score': self.total_score,
            'max_possible_score': self.max_possible_score,
            'score_percentage': self.score_percentage,
            'final_quality': self.final_quality,
            'perfect_count': self.perfect_count,
            'good_count': self.good_count,
            'ok_count': self.ok_count,
            'miss_count': self.miss_count,
            'max_combo': self.max_combo,
            'ingredient_quality_bonus': self.ingredient_quality_bonus,
        }


class CookingMinigame:
    """
    A rhythm-based cooking minigame.

    Notes fall from the top of the screen and players must press
    the correct key when the note reaches the hit line.
    """

    # Game states
    STATE_READY = 'ready'
    STATE_PLAYING = 'playing'
    STATE_FINISHED = 'finished'
    STATE_RESULTS = 'results'

    def __init__(self, easy_mode: bool = False):
        """
        Initialize the cooking minigame.

        Args:
            easy_mode: If True, use wider timing windows and slower notes
        """
        self.easy_mode = easy_mode
        self._state = self.STATE_READY

        # Game settings
        self._note_speed = COOKING_NOTE_SPEED_EASY if easy_mode else COOKING_NOTE_SPEED
        self._timing_multiplier = EASY_MODE_TIMING_MULTIPLIER if easy_mode else 1.0

        # Current recipe info
        self._recipe_id: str = ''
        self._recipe_difficulty: int = 1
        self._ingredient_quality: int = 3  # Average quality

        # Notes
        self._notes: List[Note] = []
        self._generated_note_count: int = 0

        # Timing
        self._game_duration: float = 0.0
        self._start_time: float = 0.0
        self._current_time: float = 0.0
        self._notes_per_second: float = 0.0
        self._next_note_time: float = 0.0

        # Scoring
        self._score: int = 0
        self._combo: int = 0
        self._max_combo: int = 0
        self._perfect_count: int = 0
        self._good_count: int = 0
        self._ok_count: int = 0
        self._miss_count: int = 0

        # Visual feedback
        self._hit_effects: List[Dict] = []  # Visual effects for hits
        self._last_grade: str = ''
        self._last_grade_time: float = 0.0

        # Lane layout
        self._lane_x_positions: List[int] = []
        self._calculate_lane_positions()

        # Callbacks
        self._on_hit: Optional[Callable[[str], None]] = None  # Called on note hit
        self._on_complete: Optional[Callable[[CookingResult], None]] = None

        # Sound manager reference (set externally)
        self._sound_manager = None

    def _calculate_lane_positions(self):
        """Calculate x positions for each lane."""
        total_width = (COOKING_LANES * COOKING_LANE_WIDTH +
                      (COOKING_LANES - 1) * COOKING_LANE_SPACING)
        start_x = (SCREEN_WIDTH - total_width) // 2

        self._lane_x_positions = []
        for i in range(COOKING_LANES):
            x = start_x + i * (COOKING_LANE_WIDTH + COOKING_LANE_SPACING)
            self._lane_x_positions.append(x)

    def set_sound_manager(self, sound_manager):
        """Set the sound manager for audio feedback."""
        self._sound_manager = sound_manager

    def set_on_hit_callback(self, callback: Callable[[str], None]):
        """Set callback for when a note is hit (receives grade)."""
        self._on_hit = callback

    def set_on_complete_callback(self, callback: Callable[[CookingResult], None]):
        """Set callback for when minigame completes."""
        self._on_complete = callback

    # =========================================================================
    # GAME SETUP
    # =========================================================================

    def setup(self, recipe_id: str, difficulty: int, ingredient_quality: int = 3):
        """
        Set up a new cooking session.

        Args:
            recipe_id: ID of the recipe being cooked
            difficulty: Recipe difficulty (1-5)
            ingredient_quality: Average quality of ingredients (1-5)
        """
        self._recipe_id = recipe_id
        self._recipe_difficulty = max(1, min(5, difficulty))
        self._ingredient_quality = max(1, min(5, ingredient_quality))

        # Calculate game duration based on difficulty
        self._game_duration = (COOKING_DURATION_BASE +
                              COOKING_DURATION_PER_DIFFICULTY * self._recipe_difficulty)

        # Calculate notes per second
        self._notes_per_second = (COOKING_NOTES_PER_SECOND_BASE +
                                 COOKING_NOTES_PER_SECOND_PER_DIFFICULTY * self._recipe_difficulty)

        # Reset state
        self._notes = []
        self._generated_note_count = 0
        self._score = 0
        self._combo = 0
        self._max_combo = 0
        self._perfect_count = 0
        self._good_count = 0
        self._ok_count = 0
        self._miss_count = 0
        self._hit_effects = []
        self._last_grade = ''
        self._state = self.STATE_READY

    def start(self):
        """Start the minigame."""
        if self._state != self.STATE_READY:
            return

        self._state = self.STATE_PLAYING
        self._start_time = time.time()
        self._current_time = 0.0

        # Pre-generate first few notes
        self._generate_initial_notes()

    def _generate_initial_notes(self):
        """Generate notes for the beginning of the song."""
        # Calculate travel time from top to hit line
        travel_time = COOKING_HIT_LINE_Y / self._note_speed

        # Generate notes that will arrive within the first 2 seconds
        lead_time = travel_time + 2.0
        self._generate_notes_until(lead_time)

    def _generate_notes_until(self, until_time: float):
        """Generate notes up to a specific target time."""
        while self._next_note_time < until_time and self._next_note_time < self._game_duration:
            # Generate a note at this time
            lane = self._pick_lane()
            note = Note(
                lane=lane,
                target_time=self._next_note_time,
            )
            self._notes.append(note)
            self._generated_note_count += 1

            # Calculate next note time with some randomness
            base_interval = 1.0 / self._notes_per_second
            variation = base_interval * 0.3  # ±30% variation
            interval = base_interval + random.uniform(-variation, variation)
            self._next_note_time += max(0.2, interval)  # Minimum 0.2s between notes

    def _pick_lane(self) -> int:
        """Pick a lane for the next note, avoiding repetition."""
        # Simple algorithm: avoid putting too many notes in the same lane
        if not self._notes:
            return random.randint(0, COOKING_LANES - 1)

        # Get last few lanes used
        recent_lanes = [n.lane for n in self._notes[-3:]]

        # Prefer lanes that weren't used recently
        weights = [1.0] * COOKING_LANES
        for lane in recent_lanes:
            weights[lane] *= 0.5

        # Normalize and pick
        total = sum(weights)
        r = random.uniform(0, total)
        cumulative = 0
        for i, w in enumerate(weights):
            cumulative += w
            if r <= cumulative:
                return i
        return random.randint(0, COOKING_LANES - 1)

    # =========================================================================
    # GAME UPDATE
    # =========================================================================

    def update(self, dt: float):
        """
        Update the minigame state.

        Args:
            dt: Delta time in seconds
        """
        if self._state != self.STATE_PLAYING:
            return

        self._current_time = time.time() - self._start_time

        # Check if game is over
        if self._current_time >= self._game_duration:
            self._finish_game()
            return

        # Generate more notes as needed
        travel_time = COOKING_HIT_LINE_Y / self._note_speed
        look_ahead = self._current_time + travel_time + 1.0
        self._generate_notes_until(look_ahead)

        # Update note positions
        for note in self._notes:
            if not note.hit and not note.missed:
                # Calculate y position based on how close to target time
                time_until_hit = note.target_time - self._current_time
                note.y = COOKING_HIT_LINE_Y - (time_until_hit * self._note_speed)

                # Check for auto-miss (note passed hit line)
                timing_window = TIMING_OK * self._timing_multiplier
                if note.y > COOKING_HIT_LINE_Y + timing_window:
                    self._miss_note(note)

        # Update hit effects
        self._hit_effects = [
            e for e in self._hit_effects
            if time.time() - e['time'] < 0.5
        ]

    def handle_input(self, key: int):
        """
        Handle a key press.

        Args:
            key: pygame key code
        """
        if self._state != self.STATE_PLAYING:
            return

        # Determine which lane was pressed
        lane = self._key_to_lane(key)
        if lane < 0:
            return

        # Find the closest note in this lane
        closest_note = None
        closest_timing = float('inf')

        for note in self._notes:
            if note.lane == lane and not note.hit and not note.missed:
                timing = abs(note.target_time - self._current_time) * 1000  # in ms
                if timing < closest_timing:
                    closest_timing = timing
                    closest_note = note

        if closest_note:
            # Apply timing multiplier for easy mode
            adjusted_timing = closest_timing / self._timing_multiplier
            grade = self._get_timing_grade(adjusted_timing)

            if grade != GRADE_MISS:
                self._hit_note(closest_note, grade)
            else:
                # Too early or late
                self._miss_note(closest_note)

    def _key_to_lane(self, key: int) -> int:
        """Convert a pygame key to a lane index (-1 if not a lane key)."""
        key_name = pygame.key.name(key).lower()

        # Check main keys (A, S, D, F)
        if key_name in COOKING_LANE_KEYS:
            return COOKING_LANE_KEYS.index(key_name)

        # Check arrow keys
        if key_name in COOKING_LANE_KEYS_ALT:
            return COOKING_LANE_KEYS_ALT.index(key_name)

        return -1

    def _get_timing_grade(self, timing_ms: float) -> str:
        """Get the grade for a timing in milliseconds."""
        if timing_ms <= TIMING_PERFECT:
            return GRADE_PERFECT
        elif timing_ms <= TIMING_GOOD:
            return GRADE_GOOD
        elif timing_ms <= TIMING_OK:
            return GRADE_OK
        else:
            return GRADE_MISS

    def _hit_note(self, note: Note, grade: str):
        """Process a successful note hit."""
        note.hit = True
        note.grade = grade

        # Update combo
        self._combo += 1
        self._max_combo = max(self._max_combo, self._combo)

        # Calculate score with combo multiplier
        base_score = {
            GRADE_PERFECT: SCORE_PERFECT,
            GRADE_GOOD: SCORE_GOOD,
            GRADE_OK: SCORE_OK,
        }.get(grade, 0)

        multiplier = self._get_combo_multiplier()
        score = int(base_score * multiplier)
        self._score += score

        # Update grade counts
        if grade == GRADE_PERFECT:
            self._perfect_count += 1
        elif grade == GRADE_GOOD:
            self._good_count += 1
        elif grade == GRADE_OK:
            self._ok_count += 1

        # Visual feedback
        self._last_grade = grade
        self._last_grade_time = time.time()
        self._hit_effects.append({
            'lane': note.lane,
            'grade': grade,
            'time': time.time(),
        })

        # Sound feedback
        if self._sound_manager:
            if grade == GRADE_PERFECT:
                self._sound_manager.play('ui_confirm', 0.8)
            elif grade == GRADE_GOOD:
                self._sound_manager.play('ui_click', 0.7)
            else:
                self._sound_manager.play('ui_click', 0.5)

        # Callback
        if self._on_hit:
            self._on_hit(grade)

    def _miss_note(self, note: Note):
        """Process a missed note."""
        note.missed = True
        note.grade = GRADE_MISS
        self._miss_count += 1
        self._combo = 0  # Break combo

        # Sound feedback
        if self._sound_manager:
            self._sound_manager.play('ui_cancel', 0.5)

    def _get_combo_multiplier(self) -> float:
        """Get the current combo score multiplier."""
        multiplier = 1.0
        for threshold, mult in sorted(COMBO_MULTIPLIER_THRESHOLDS.items()):
            if self._combo >= threshold:
                multiplier = mult
        return multiplier

    def _finish_game(self):
        """Finish the game and calculate results."""
        self._state = self.STATE_FINISHED

        # Mark any remaining notes as missed
        for note in self._notes:
            if not note.hit and not note.missed:
                self._miss_note(note)

        # Calculate final score
        total_notes = self._perfect_count + self._good_count + self._ok_count + self._miss_count
        max_possible = total_notes * SCORE_PERFECT * 2.5  # Max combo multiplier

        # Apply ingredient quality bonus
        quality_bonus = INGREDIENT_QUALITY_BONUS.get(self._ingredient_quality, 1.0)
        final_score = int(self._score * quality_bonus)

        # Calculate score percentage
        score_percentage = final_score / max_possible if max_possible > 0 else 0.0

        # Determine final quality (1-5 stars)
        final_quality = 1
        for quality, threshold in sorted(QUALITY_SCORE_THRESHOLDS.items()):
            if score_percentage >= threshold:
                final_quality = quality

        # Create result
        result = CookingResult(
            recipe_id=self._recipe_id,
            total_score=final_score,
            max_possible_score=int(max_possible),
            score_percentage=score_percentage,
            final_quality=final_quality,
            perfect_count=self._perfect_count,
            good_count=self._good_count,
            ok_count=self._ok_count,
            miss_count=self._miss_count,
            max_combo=self._max_combo,
            ingredient_quality_bonus=quality_bonus,
        )

        self._state = self.STATE_RESULTS

        # Play completion sound
        if self._sound_manager:
            self._sound_manager.play('cooking_complete')

        # Callback
        if self._on_complete:
            self._on_complete(result)

        return result

    # =========================================================================
    # DRAWING
    # =========================================================================

    def draw(self, surface: pygame.Surface):
        """
        Draw the minigame to the screen.

        Args:
            surface: Pygame surface to draw on
        """
        # Background
        surface.fill(UI_BG)

        if self._state == self.STATE_READY:
            self._draw_ready_screen(surface)
        elif self._state == self.STATE_PLAYING:
            self._draw_gameplay(surface)
        elif self._state in (self.STATE_FINISHED, self.STATE_RESULTS):
            self._draw_results(surface)

    def _draw_ready_screen(self, surface: pygame.Surface):
        """Draw the ready/countdown screen."""
        font = pygame.font.Font(None, 48)
        text = font.render("Press SPACE to start cooking!", True, UI_TEXT)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(text, rect)

        # Instructions
        font_small = pygame.font.Font(None, 32)
        instructions = [
            f"Use {', '.join(COOKING_LANE_KEYS).upper()} or Arrow keys",
            f"Difficulty: {'★' * self._recipe_difficulty}",
            f"Easy Mode: {'ON' if self.easy_mode else 'OFF'}",
        ]
        for i, text in enumerate(instructions):
            rendered = font_small.render(text, True, UI_TEXT_DIM)
            rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60 + i * 30))
            surface.blit(rendered, rect)

    def _draw_gameplay(self, surface: pygame.Surface):
        """Draw the main gameplay."""
        # Draw lanes
        for i, x in enumerate(self._lane_x_positions):
            # Lane background
            pygame.draw.rect(surface, UI_PANEL,
                           (x, 50, COOKING_LANE_WIDTH, SCREEN_HEIGHT - 100))
            # Lane border
            pygame.draw.rect(surface, UI_BORDER,
                           (x, 50, COOKING_LANE_WIDTH, SCREEN_HEIGHT - 100), 2)

        # Draw hit line
        for i, x in enumerate(self._lane_x_positions):
            pygame.draw.rect(surface, COOKING_LANE_COLORS[i],
                           (x, COOKING_HIT_LINE_Y - 5, COOKING_LANE_WIDTH, 10))

        # Draw notes
        for note in self._notes:
            if not note.hit and not note.missed:
                if 0 <= note.y <= SCREEN_HEIGHT:
                    self._draw_note(surface, note)

        # Draw hit effects
        for effect in self._hit_effects:
            self._draw_hit_effect(surface, effect)

        # Draw HUD
        self._draw_hud(surface)

        # Draw last grade
        if self._last_grade and time.time() - self._last_grade_time < 0.5:
            self._draw_grade_popup(surface)

    def _draw_note(self, surface: pygame.Surface, note: Note):
        """Draw a single note."""
        x = self._lane_x_positions[note.lane]
        y = int(note.y)

        # Note body
        color = COOKING_LANE_COLORS[note.lane]
        pygame.draw.rect(surface, color,
                        (x + 5, y - COOKING_NOTE_HEIGHT // 2,
                         COOKING_LANE_WIDTH - 10, COOKING_NOTE_HEIGHT),
                        border_radius=4)

        # Highlight
        lighter = tuple(min(255, c + 60) for c in color)
        pygame.draw.rect(surface, lighter,
                        (x + 5, y - COOKING_NOTE_HEIGHT // 2,
                         COOKING_LANE_WIDTH - 10, 4),
                        border_radius=2)

    def _draw_hit_effect(self, surface: pygame.Surface, effect: Dict):
        """Draw a hit effect animation."""
        elapsed = time.time() - effect['time']
        alpha = int(255 * (1 - elapsed / 0.5))
        size = int(30 + elapsed * 100)

        x = self._lane_x_positions[effect['lane']] + COOKING_LANE_WIDTH // 2
        y = COOKING_HIT_LINE_Y

        # Grade-based color
        if effect['grade'] == GRADE_PERFECT:
            color = (255, 215, 0)  # Gold
        elif effect['grade'] == GRADE_GOOD:
            color = (100, 255, 100)  # Green
        else:
            color = (100, 200, 255)  # Blue

        # Draw expanding circle
        if alpha > 0:
            circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*color, alpha), (size, size), size, 3)
            surface.blit(circle_surface, (x - size, y - size))

    def _draw_hud(self, surface: pygame.Surface):
        """Draw the heads-up display."""
        font = pygame.font.Font(None, 36)

        # Score
        score_text = font.render(f"Score: {self._score}", True, UI_TEXT)
        surface.blit(score_text, (20, 10))

        # Combo
        if self._combo > 0:
            combo_text = font.render(f"Combo: {self._combo}x", True, UI_TEXT)
            surface.blit(combo_text, (SCREEN_WIDTH - 150, 10))

            # Show multiplier if active
            mult = self._get_combo_multiplier()
            if mult > 1.0:
                mult_text = pygame.font.Font(None, 28).render(f"({mult:.1f}x)", True, (255, 215, 0))
                surface.blit(mult_text, (SCREEN_WIDTH - 60, 40))

        # Time remaining
        time_left = max(0, self._game_duration - self._current_time)
        time_text = font.render(f"Time: {time_left:.1f}s", True, UI_TEXT)
        rect = time_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
        surface.blit(time_text, rect)

    def _draw_grade_popup(self, surface: pygame.Surface):
        """Draw the grade popup."""
        font = pygame.font.Font(None, 56)

        # Grade text and color
        grade_display = {
            GRADE_PERFECT: ('PERFECT!', (255, 215, 0)),
            GRADE_GOOD: ('GOOD!', (100, 255, 100)),
            GRADE_OK: ('OK', (100, 200, 255)),
            GRADE_MISS: ('MISS', (255, 80, 80)),
        }

        text, color = grade_display.get(self._last_grade, ('', WHITE))
        rendered = font.render(text, True, color)

        # Animate: scale up and fade
        elapsed = time.time() - self._last_grade_time
        scale = 1.0 + elapsed * 0.5
        alpha = int(255 * (1 - elapsed / 0.5))

        # Apply scale (simplified - just position offset)
        y_offset = int(-elapsed * 50)

        rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))

        if alpha > 0:
            # Create surface with alpha
            text_surface = pygame.Surface(rendered.get_size(), pygame.SRCALPHA)
            text_surface.blit(rendered, (0, 0))
            text_surface.set_alpha(alpha)
            surface.blit(text_surface, rect)

    def _draw_results(self, surface: pygame.Surface):
        """Draw the results screen."""
        font_large = pygame.font.Font(None, 56)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        y = 100

        # Title
        title = font_large.render("Cooking Complete!", True, UI_TEXT)
        rect = title.get_rect(centerx=SCREEN_WIDTH // 2, top=y)
        surface.blit(title, rect)
        y += 80

        # Final quality stars
        total_notes = self._perfect_count + self._good_count + self._ok_count + self._miss_count
        max_possible = total_notes * SCORE_PERFECT * 2.5
        quality_bonus = INGREDIENT_QUALITY_BONUS.get(self._ingredient_quality, 1.0)
        score_percentage = (self._score * quality_bonus) / max_possible if max_possible > 0 else 0

        final_quality = 1
        for quality, threshold in sorted(QUALITY_SCORE_THRESHOLDS.items()):
            if score_percentage >= threshold:
                final_quality = quality

        stars = "★" * final_quality + "☆" * (5 - final_quality)
        stars_text = font_large.render(stars, True, (255, 215, 0))
        rect = stars_text.get_rect(centerx=SCREEN_WIDTH // 2, top=y)
        surface.blit(stars_text, rect)
        y += 60

        # Score breakdown
        score_text = font_medium.render(f"Final Score: {int(self._score * quality_bonus)}", True, UI_TEXT)
        rect = score_text.get_rect(centerx=SCREEN_WIDTH // 2, top=y)
        surface.blit(score_text, rect)
        y += 50

        # Grade breakdown
        breakdown = [
            (f"Perfect: {self._perfect_count}", (255, 215, 0)),
            (f"Good: {self._good_count}", (100, 255, 100)),
            (f"OK: {self._ok_count}", (100, 200, 255)),
            (f"Miss: {self._miss_count}", (255, 80, 80)),
        ]

        for text, color in breakdown:
            rendered = font_small.render(text, True, color)
            rect = rendered.get_rect(centerx=SCREEN_WIDTH // 2, top=y)
            surface.blit(rendered, rect)
            y += 30

        y += 20

        # Max combo
        combo_text = font_medium.render(f"Max Combo: {self._max_combo}x", True, UI_TEXT)
        rect = combo_text.get_rect(centerx=SCREEN_WIDTH // 2, top=y)
        surface.blit(combo_text, rect)
        y += 40

        # Ingredient bonus
        if quality_bonus != 1.0:
            bonus_text = font_small.render(f"Ingredient Quality Bonus: {quality_bonus:.0%}", True, UI_TEXT_DIM)
            rect = bonus_text.get_rect(centerx=SCREEN_WIDTH // 2, top=y)
            surface.blit(bonus_text, rect)
            y += 40

        # Continue prompt
        continue_text = font_medium.render("Press SPACE to continue", True, UI_TEXT_DIM)
        rect = continue_text.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 50)
        surface.blit(continue_text, rect)

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def get_state(self) -> str:
        """Get current game state."""
        return self._state

    def get_score(self) -> int:
        """Get current score."""
        return self._score

    def get_combo(self) -> int:
        """Get current combo."""
        return self._combo

    def is_playing(self) -> bool:
        """Check if game is actively playing."""
        return self._state == self.STATE_PLAYING

    def is_finished(self) -> bool:
        """Check if game is finished (results showing)."""
        return self._state == self.STATE_RESULTS

    def get_result(self) -> Optional[CookingResult]:
        """Get the cooking result (only available after finishing)."""
        if self._state != self.STATE_RESULTS:
            return None

        total_notes = self._perfect_count + self._good_count + self._ok_count + self._miss_count
        max_possible = total_notes * SCORE_PERFECT * 2.5
        quality_bonus = INGREDIENT_QUALITY_BONUS.get(self._ingredient_quality, 1.0)
        final_score = int(self._score * quality_bonus)
        score_percentage = final_score / max_possible if max_possible > 0 else 0

        final_quality = 1
        for quality, threshold in sorted(QUALITY_SCORE_THRESHOLDS.items()):
            if score_percentage >= threshold:
                final_quality = quality

        return CookingResult(
            recipe_id=self._recipe_id,
            total_score=final_score,
            max_possible_score=int(max_possible),
            score_percentage=score_percentage,
            final_quality=final_quality,
            perfect_count=self._perfect_count,
            good_count=self._good_count,
            ok_count=self._ok_count,
            miss_count=self._miss_count,
            max_combo=self._max_combo,
            ingredient_quality_bonus=quality_bonus,
        )
