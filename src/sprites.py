"""
Procedural sprite generation system for Dragon Haven Cafe.
All game sprites are generated using pygame.draw functions.
No external image files required.
"""

import pygame
import math
from constants import (
    # Dragon colors
    DRAGON_EGG_SHELL, DRAGON_EGG_SPOT, DRAGON_HATCHLING, DRAGON_JUVENILE,
    DRAGON_WING, DRAGON_EYE, DRAGON_BELLY,
    # Character colors
    CHAR_SKIN, CHAR_HAIR_BROWN, CHAR_HAIR_BLACK, CHAR_HAIR_BLONDE,
    CHAR_APRON, CHAR_CLOTHES,
    # Ingredient colors
    INGREDIENT_BERRY, INGREDIENT_HERB, INGREDIENT_MUSHROOM,
    INGREDIENT_HONEY, INGREDIENT_MEAT, INGREDIENT_FISH,
    # Terrain colors
    GRASS_GREEN, FOREST_GREEN, TERRAIN_DIRT, TERRAIN_STONE, TERRAIN_SAND,
    TERRAIN_FLOWER_RED, TERRAIN_FLOWER_YELLOW, TERRAIN_FLOWER_BLUE,
    WATER_BLUE, SKY_BLUE,
    # UI colors
    UI_BG, UI_PANEL, UI_BORDER, UI_HIGHLIGHT, UI_TEXT, UI_TEXT_DIM,
    # Status colors
    HEALTH_GREEN, STAMINA_YELLOW, HUNGER_ORANGE, HAPPINESS_PINK,
    # Basic
    BLACK, WHITE, GRAY, DARK_GRAY, LIGHT_GRAY,
    CAFE_WARM, CAFE_WOOD, CAFE_CREAM
)


class SpriteGenerator:
    """
    Generates and caches all game sprites procedurally.

    Usage:
        sprites = SpriteGenerator()
        dragon_sprite = sprites.get_dragon('egg', color_shift=(0, 0, 0))
        button_sprite = sprites.get_button(200, 50, 'normal')
    """

    def __init__(self):
        """Initialize the sprite generator with empty cache."""
        self._cache = {}

    def _cache_key(self, *args):
        """Generate a cache key from arguments."""
        return str(args)

    def _get_cached(self, key):
        """Get a cached sprite if it exists."""
        return self._cache.get(key)

    def _set_cached(self, key, surface):
        """Cache a sprite for reuse."""
        self._cache[key] = surface
        return surface

    def clear_cache(self):
        """Clear the sprite cache."""
        self._cache.clear()

    # =========================================================================
    # DRAGON SPRITES
    # =========================================================================

    def get_dragon(self, stage, color_shift=(0, 0, 0), size=64):
        """
        Get a dragon sprite for the given life stage.

        Args:
            stage: 'egg', 'hatchling', or 'juvenile'
            color_shift: RGB tuple to shift base color by
            size: Base size in pixels

        Returns:
            pygame.Surface with the dragon sprite
        """
        key = self._cache_key('dragon', stage, color_shift, size)
        cached = self._get_cached(key)
        if cached:
            return cached

        if stage == 'egg':
            surface = self._draw_dragon_egg(size, color_shift)
        elif stage == 'hatchling':
            surface = self._draw_dragon_hatchling(size, color_shift)
        elif stage == 'juvenile':
            surface = self._draw_dragon_juvenile(size, color_shift)
        else:
            surface = self._draw_dragon_egg(size, color_shift)

        return self._set_cached(key, surface)

    def _shift_color(self, base_color, shift):
        """Apply a color shift to a base color."""
        return tuple(max(0, min(255, base_color[i] + shift[i])) for i in range(3))

    def _draw_dragon_egg(self, size, color_shift):
        """Draw a dragon egg sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        # Main egg shape (oval)
        egg_color = self._shift_color(DRAGON_EGG_SHELL, color_shift)
        egg_rect = pygame.Rect(size // 4, size // 6, size // 2, size * 2 // 3)
        pygame.draw.ellipse(surface, egg_color, egg_rect)

        # Spots on egg
        spot_color = self._shift_color(DRAGON_EGG_SPOT, color_shift)
        pygame.draw.circle(surface, spot_color, (cx - 5, cy - 5), 4)
        pygame.draw.circle(surface, spot_color, (cx + 6, cy + 2), 3)
        pygame.draw.circle(surface, spot_color, (cx - 2, cy + 8), 5)

        # Highlight
        highlight = tuple(min(255, c + 40) for c in egg_color)
        pygame.draw.ellipse(surface, highlight,
                          pygame.Rect(size // 3, size // 4, size // 6, size // 6))

        return surface

    def _draw_dragon_hatchling(self, size, color_shift):
        """Draw a baby dragon sprite (small, cute)."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        body_color = self._shift_color(DRAGON_HATCHLING, color_shift)
        belly_color = self._shift_color(DRAGON_BELLY, color_shift)

        # Body (round)
        pygame.draw.circle(surface, body_color, (cx, cy + 5), size // 3)

        # Belly
        pygame.draw.ellipse(surface, belly_color,
                          pygame.Rect(cx - size // 5, cy, size * 2 // 5, size // 4))

        # Head (large compared to body - cute proportions)
        pygame.draw.circle(surface, body_color, (cx, cy - 8), size // 4)

        # Eyes (large and cute)
        eye_color = DRAGON_EYE
        pygame.draw.circle(surface, WHITE, (cx - 6, cy - 10), 5)
        pygame.draw.circle(surface, WHITE, (cx + 6, cy - 10), 5)
        pygame.draw.circle(surface, eye_color, (cx - 5, cy - 10), 3)
        pygame.draw.circle(surface, eye_color, (cx + 7, cy - 10), 3)

        # Small wings (stubs)
        wing_color = self._shift_color(DRAGON_WING, color_shift)
        pygame.draw.ellipse(surface, wing_color,
                          pygame.Rect(cx - size // 2, cy - 2, size // 4, size // 5))
        pygame.draw.ellipse(surface, wing_color,
                          pygame.Rect(cx + size // 4, cy - 2, size // 4, size // 5))

        # Tiny horns
        pygame.draw.polygon(surface, body_color, [
            (cx - 8, cy - 18), (cx - 10, cy - 26), (cx - 6, cy - 20)
        ])
        pygame.draw.polygon(surface, body_color, [
            (cx + 8, cy - 18), (cx + 10, cy - 26), (cx + 6, cy - 20)
        ])

        # Small tail
        pygame.draw.arc(surface, body_color,
                       pygame.Rect(cx + 5, cy + 10, 20, 15),
                       -0.5, 1.5, 3)

        return surface

    def _draw_dragon_juvenile(self, size, color_shift):
        """Draw a juvenile dragon sprite (larger, more detailed)."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        body_color = self._shift_color(DRAGON_JUVENILE, color_shift)
        belly_color = self._shift_color(DRAGON_BELLY, color_shift)
        wing_color = self._shift_color(DRAGON_WING, color_shift)

        # Wings (behind body)
        wing_points_left = [
            (cx - 8, cy - 5),
            (cx - size // 2 - 5, cy - 15),
            (cx - size // 2, cy + 5),
            (cx - 10, cy + 5)
        ]
        wing_points_right = [
            (cx + 8, cy - 5),
            (cx + size // 2 + 5, cy - 15),
            (cx + size // 2, cy + 5),
            (cx + 10, cy + 5)
        ]
        pygame.draw.polygon(surface, wing_color, wing_points_left)
        pygame.draw.polygon(surface, wing_color, wing_points_right)

        # Body (elongated)
        pygame.draw.ellipse(surface, body_color,
                          pygame.Rect(cx - size // 4, cy - 5, size // 2, size // 2))

        # Belly
        pygame.draw.ellipse(surface, belly_color,
                          pygame.Rect(cx - size // 6, cy + 2, size // 3, size // 4))

        # Neck
        pygame.draw.ellipse(surface, body_color,
                          pygame.Rect(cx - 6, cy - 18, 12, 20))

        # Head
        pygame.draw.ellipse(surface, body_color,
                          pygame.Rect(cx - 10, cy - 28, 20, 16))

        # Snout
        pygame.draw.ellipse(surface, body_color,
                          pygame.Rect(cx - 4, cy - 32, 8, 8))

        # Eyes
        pygame.draw.circle(surface, WHITE, (cx - 5, cy - 22), 4)
        pygame.draw.circle(surface, WHITE, (cx + 5, cy - 22), 4)
        pygame.draw.circle(surface, DRAGON_EYE, (cx - 4, cy - 22), 2)
        pygame.draw.circle(surface, DRAGON_EYE, (cx + 6, cy - 22), 2)

        # Horns
        pygame.draw.polygon(surface, DARK_GRAY, [
            (cx - 8, cy - 26), (cx - 12, cy - 38), (cx - 5, cy - 28)
        ])
        pygame.draw.polygon(surface, DARK_GRAY, [
            (cx + 8, cy - 26), (cx + 12, cy - 38), (cx + 5, cy - 28)
        ])

        # Legs
        leg_width = 6
        # Front legs
        pygame.draw.rect(surface, body_color,
                        pygame.Rect(cx - 12, cy + 15, leg_width, 12))
        pygame.draw.rect(surface, body_color,
                        pygame.Rect(cx + 6, cy + 15, leg_width, 12))

        # Tail
        tail_points = [
            (cx + 10, cy + 10),
            (cx + 25, cy + 15),
            (cx + 30, cy + 10),
            (cx + 25, cy + 5),
            (cx + 10, cy + 5)
        ]
        pygame.draw.polygon(surface, body_color, tail_points)

        return surface

    # =========================================================================
    # UI ELEMENTS
    # =========================================================================

    def get_button(self, width, height, state='normal', text='', corner_radius=8):
        """
        Generate a button sprite.

        Args:
            width: Button width in pixels
            height: Button height in pixels
            state: 'normal', 'hover', 'pressed', or 'disabled'
            text: Optional text to render on button
            corner_radius: Rounded corner radius

        Returns:
            pygame.Surface with the button
        """
        key = self._cache_key('button', width, height, state, text, corner_radius)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Colors based on state
        colors = {
            'normal': (UI_PANEL, UI_BORDER, UI_TEXT),
            'hover': (UI_HIGHLIGHT, UI_TEXT, WHITE),
            'pressed': (UI_BG, UI_BORDER, UI_TEXT_DIM),
            'disabled': (DARK_GRAY, GRAY, LIGHT_GRAY)
        }
        bg_color, border_color, text_color = colors.get(state, colors['normal'])

        # Draw rounded rectangle background
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(surface, bg_color, rect, border_radius=corner_radius)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=corner_radius)

        # Draw text if provided
        if text:
            font = pygame.font.Font(None, height // 2)
            text_surf = font.render(text, True, text_color)
            text_rect = text_surf.get_rect(center=(width // 2, height // 2))
            surface.blit(text_surf, text_rect)

        return self._set_cached(key, surface)

    def get_panel(self, width, height, style='default'):
        """
        Generate a UI panel sprite.

        Args:
            width: Panel width
            height: Panel height
            style: 'default', 'dark', 'light', or 'wood'

        Returns:
            pygame.Surface with the panel
        """
        key = self._cache_key('panel', width, height, style)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        styles = {
            'default': (UI_PANEL, UI_BORDER),
            'dark': (UI_BG, DARK_GRAY),
            'light': (CAFE_CREAM, CAFE_WARM),
            'wood': (CAFE_WOOD, DARK_GRAY)
        }
        bg_color, border_color = styles.get(style, styles['default'])

        # Main panel
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(surface, bg_color, rect, border_radius=4)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=4)

        # Inner highlight
        highlight = pygame.Rect(2, 2, width - 4, 3)
        highlight_color = tuple(min(255, c + 20) for c in bg_color)
        pygame.draw.rect(surface, highlight_color, highlight)

        return self._set_cached(key, surface)

    def get_progress_bar(self, width, height, fill_ratio, bar_type='health'):
        """
        Generate a progress/status bar.

        Args:
            width: Bar width
            height: Bar height
            fill_ratio: 0.0 to 1.0 fill amount
            bar_type: 'health', 'stamina', 'hunger', or 'happiness'

        Returns:
            pygame.Surface with the bar
        """
        key = self._cache_key('progress_bar', width, height, fill_ratio, bar_type)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Bar colors
        colors = {
            'health': HEALTH_GREEN,
            'stamina': STAMINA_YELLOW,
            'hunger': HUNGER_ORANGE,
            'happiness': HAPPINESS_PINK
        }
        fill_color = colors.get(bar_type, HEALTH_GREEN)

        # Background
        pygame.draw.rect(surface, DARK_GRAY, pygame.Rect(0, 0, width, height),
                        border_radius=height // 2)

        # Fill
        fill_width = int((width - 4) * max(0, min(1, fill_ratio)))
        if fill_width > 0:
            pygame.draw.rect(surface, fill_color,
                           pygame.Rect(2, 2, fill_width, height - 4),
                           border_radius=max(1, (height - 4) // 2))

        # Border
        pygame.draw.rect(surface, UI_BORDER, pygame.Rect(0, 0, width, height),
                        2, border_radius=height // 2)

        return self._set_cached(key, surface)

    def get_icon(self, icon_type, size=32):
        """
        Generate a small icon sprite.

        Args:
            icon_type: Type of icon (e.g., 'heart', 'coin', 'star', 'clock')
            size: Icon size in pixels

        Returns:
            pygame.Surface with the icon
        """
        key = self._cache_key('icon', icon_type, size)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        if icon_type == 'heart':
            # Heart shape
            color = HAPPINESS_PINK
            pygame.draw.circle(surface, color, (cx - size // 6, cy - 2), size // 4)
            pygame.draw.circle(surface, color, (cx + size // 6, cy - 2), size // 4)
            pygame.draw.polygon(surface, color, [
                (cx - size // 3, cy), (cx, cy + size // 3), (cx + size // 3, cy)
            ])

        elif icon_type == 'coin':
            # Gold coin
            pygame.draw.circle(surface, STAMINA_YELLOW, (cx, cy), size // 3)
            pygame.draw.circle(surface, DARK_GRAY, (cx, cy), size // 3, 2)
            pygame.draw.circle(surface, (200, 160, 40), (cx, cy), size // 5)

        elif icon_type == 'star':
            # Star shape
            points = []
            for i in range(5):
                angle = math.radians(i * 72 - 90)
                points.append((cx + int(size // 3 * math.cos(angle)),
                             cy + int(size // 3 * math.sin(angle))))
                angle = math.radians(i * 72 - 90 + 36)
                points.append((cx + int(size // 6 * math.cos(angle)),
                             cy + int(size // 6 * math.sin(angle))))
            pygame.draw.polygon(surface, STAMINA_YELLOW, points)

        elif icon_type == 'clock':
            # Clock face
            pygame.draw.circle(surface, CAFE_CREAM, (cx, cy), size // 3)
            pygame.draw.circle(surface, DARK_GRAY, (cx, cy), size // 3, 2)
            # Hands
            pygame.draw.line(surface, DARK_GRAY, (cx, cy), (cx, cy - size // 5), 2)
            pygame.draw.line(surface, DARK_GRAY, (cx, cy), (cx + size // 6, cy), 2)

        return self._set_cached(key, surface)

    # =========================================================================
    # ITEM/INGREDIENT SPRITES
    # =========================================================================

    def get_ingredient(self, ingredient_type, size=32):
        """
        Generate an ingredient sprite.

        Args:
            ingredient_type: Type of ingredient
            size: Sprite size

        Returns:
            pygame.Surface with the ingredient
        """
        key = self._cache_key('ingredient', ingredient_type, size)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        if ingredient_type == 'berry':
            # Cluster of berries
            pygame.draw.circle(surface, INGREDIENT_BERRY, (cx - 4, cy), size // 5)
            pygame.draw.circle(surface, INGREDIENT_BERRY, (cx + 4, cy), size // 5)
            pygame.draw.circle(surface, INGREDIENT_BERRY, (cx, cy - 4), size // 5)
            # Stem
            pygame.draw.line(surface, FOREST_GREEN, (cx, cy - 8), (cx, cy - 14), 2)
            pygame.draw.ellipse(surface, FOREST_GREEN,
                              pygame.Rect(cx - 4, cy - 16, 8, 4))

        elif ingredient_type == 'herb':
            # Leafy herb
            for i in range(3):
                leaf_x = cx + (i - 1) * 6
                pygame.draw.ellipse(surface, INGREDIENT_HERB,
                                  pygame.Rect(leaf_x - 4, cy - 8, 8, 16))
            pygame.draw.rect(surface, FOREST_GREEN,
                           pygame.Rect(cx - 1, cy + 4, 2, 8))

        elif ingredient_type == 'mushroom':
            # Mushroom cap and stem
            pygame.draw.ellipse(surface, INGREDIENT_MUSHROOM,
                              pygame.Rect(cx - 10, cy - 8, 20, 12))
            pygame.draw.rect(surface, CAFE_CREAM,
                           pygame.Rect(cx - 4, cy, 8, 12))
            # Spots
            pygame.draw.circle(surface, CAFE_CREAM, (cx - 4, cy - 4), 2)
            pygame.draw.circle(surface, CAFE_CREAM, (cx + 5, cy - 3), 2)

        elif ingredient_type == 'honey':
            # Honey jar
            pygame.draw.rect(surface, INGREDIENT_HONEY,
                           pygame.Rect(cx - 8, cy - 6, 16, 16), border_radius=2)
            pygame.draw.rect(surface, CAFE_WOOD,
                           pygame.Rect(cx - 6, cy - 10, 12, 6))
            # Drip
            pygame.draw.circle(surface, INGREDIENT_HONEY, (cx + 4, cy + 12), 3)

        elif ingredient_type == 'meat':
            # Meat cut
            pygame.draw.ellipse(surface, INGREDIENT_MEAT,
                              pygame.Rect(cx - 10, cy - 6, 20, 14))
            pygame.draw.ellipse(surface, (200, 120, 100),
                              pygame.Rect(cx - 6, cy - 3, 12, 8))
            # Bone
            pygame.draw.circle(surface, CAFE_CREAM, (cx - 10, cy), 3)

        elif ingredient_type == 'fish':
            # Fish shape
            # Body
            pygame.draw.ellipse(surface, INGREDIENT_FISH,
                              pygame.Rect(cx - 12, cy - 5, 20, 10))
            # Tail
            pygame.draw.polygon(surface, INGREDIENT_FISH, [
                (cx + 6, cy), (cx + 14, cy - 6), (cx + 14, cy + 6)
            ])
            # Eye
            pygame.draw.circle(surface, BLACK, (cx - 6, cy - 1), 2)

        else:
            # Generic item (circle)
            pygame.draw.circle(surface, GRAY, (cx, cy), size // 3)

        return self._set_cached(key, surface)

    # =========================================================================
    # CHARACTER SPRITES
    # =========================================================================

    def get_character(self, char_type, size=64, hair_color=None):
        """
        Generate a character sprite.

        Args:
            char_type: 'player', 'customer', or 'staff'
            size: Sprite size
            hair_color: Override hair color (default varies by type)

        Returns:
            pygame.Surface with the character
        """
        key = self._cache_key('character', char_type, size, hair_color)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        # Default hair colors by type
        hair_colors = {
            'player': CHAR_HAIR_BROWN,
            'customer': CHAR_HAIR_BLACK,
            'staff': CHAR_HAIR_BLONDE
        }
        hair = hair_color or hair_colors.get(char_type, CHAR_HAIR_BROWN)

        # Body/clothes
        if char_type == 'staff':
            clothes_color = CHAR_APRON
        else:
            clothes_color = CHAR_CLOTHES

        # Draw body
        pygame.draw.ellipse(surface, clothes_color,
                          pygame.Rect(cx - 12, cy + 5, 24, 30))

        # Arms
        pygame.draw.ellipse(surface, CHAR_SKIN,
                          pygame.Rect(cx - 18, cy + 8, 10, 20))
        pygame.draw.ellipse(surface, CHAR_SKIN,
                          pygame.Rect(cx + 8, cy + 8, 10, 20))

        # Head
        pygame.draw.circle(surface, CHAR_SKIN, (cx, cy - 5), 14)

        # Hair
        pygame.draw.ellipse(surface, hair,
                          pygame.Rect(cx - 12, cy - 20, 24, 16))

        # Eyes
        pygame.draw.circle(surface, WHITE, (cx - 5, cy - 6), 4)
        pygame.draw.circle(surface, WHITE, (cx + 5, cy - 6), 4)
        pygame.draw.circle(surface, BLACK, (cx - 4, cy - 6), 2)
        pygame.draw.circle(surface, BLACK, (cx + 6, cy - 6), 2)

        # Mouth (simple smile)
        pygame.draw.arc(surface, BLACK,
                       pygame.Rect(cx - 5, cy - 2, 10, 8),
                       3.14, 6.28, 1)

        # Apron for staff
        if char_type == 'staff':
            pygame.draw.rect(surface, CHAR_APRON,
                           pygame.Rect(cx - 10, cy + 10, 20, 20))
            pygame.draw.rect(surface, DARK_GRAY,
                           pygame.Rect(cx - 10, cy + 10, 20, 20), 1)

        return self._set_cached(key, surface)

    # =========================================================================
    # TILE/TERRAIN SPRITES
    # =========================================================================

    def get_tile(self, tile_type, size=32):
        """
        Generate a terrain tile sprite.

        Args:
            tile_type: Type of tile
            size: Tile size (square)

        Returns:
            pygame.Surface with the tile
        """
        key = self._cache_key('tile', tile_type, size)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((size, size))

        if tile_type == 'grass':
            surface.fill(GRASS_GREEN)
            # Add grass texture
            for i in range(8):
                x = (i * 7 + 3) % size
                y = (i * 5 + 2) % size
                darker = tuple(max(0, c - 20) for c in GRASS_GREEN)
                pygame.draw.line(surface, darker, (x, y), (x + 2, y - 4), 1)

        elif tile_type == 'forest':
            surface.fill(FOREST_GREEN)
            # Darker patches
            for i in range(4):
                x = (i * 11 + 5) % size
                y = (i * 9 + 3) % size
                pygame.draw.circle(surface,
                                 tuple(max(0, c - 15) for c in FOREST_GREEN),
                                 (x, y), 5)

        elif tile_type == 'dirt':
            surface.fill(TERRAIN_DIRT)
            # Add some texture
            for i in range(5):
                x = (i * 9 + 2) % size
                y = (i * 7 + 4) % size
                pygame.draw.circle(surface,
                                 tuple(max(0, c - 15) for c in TERRAIN_DIRT),
                                 (x, y), 3)

        elif tile_type == 'stone':
            surface.fill(TERRAIN_STONE)
            # Stone texture
            pygame.draw.rect(surface, tuple(c + 10 for c in TERRAIN_STONE),
                           pygame.Rect(2, 2, size // 2 - 2, size // 2 - 2))
            pygame.draw.rect(surface, tuple(max(0, c - 10) for c in TERRAIN_STONE),
                           pygame.Rect(size // 2, size // 2, size // 2 - 2, size // 2 - 2))

        elif tile_type == 'water':
            surface.fill(WATER_BLUE)
            # Wave effect
            lighter = tuple(min(255, c + 30) for c in WATER_BLUE)
            pygame.draw.arc(surface, lighter,
                          pygame.Rect(0, size // 4, size, size // 2),
                          0, 3.14, 2)

        elif tile_type == 'sand':
            surface.fill(TERRAIN_SAND)
            # Dots for texture
            for i in range(6):
                x = (i * 8 + 3) % size
                y = (i * 6 + 5) % size
                pygame.draw.circle(surface,
                                 tuple(max(0, c - 10) for c in TERRAIN_SAND),
                                 (x, y), 1)

        elif tile_type == 'cafe_floor':
            surface.fill(CAFE_WOOD)
            # Wood grain
            for i in range(4):
                y = i * (size // 4) + size // 8
                pygame.draw.line(surface,
                               tuple(max(0, c - 20) for c in CAFE_WOOD),
                               (0, y), (size, y), 1)

        else:
            surface.fill(GRAY)

        return self._set_cached(key, surface)

    def get_decoration(self, deco_type, size=32):
        """
        Generate a decoration sprite (flowers, rocks, etc.).

        Args:
            deco_type: Type of decoration
            size: Sprite size

        Returns:
            pygame.Surface with the decoration
        """
        key = self._cache_key('decoration', deco_type, size)
        cached = self._get_cached(key)
        if cached:
            return cached

        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        if deco_type == 'flower_red':
            # Flower with petals
            pygame.draw.line(surface, FOREST_GREEN,
                           (cx, cy + 8), (cx, cy - 2), 2)
            for i in range(5):
                angle = math.radians(i * 72)
                px = cx + int(6 * math.cos(angle))
                py = cy - 5 + int(6 * math.sin(angle))
                pygame.draw.circle(surface, TERRAIN_FLOWER_RED, (px, py), 4)
            pygame.draw.circle(surface, STAMINA_YELLOW, (cx, cy - 5), 3)

        elif deco_type == 'flower_yellow':
            pygame.draw.line(surface, FOREST_GREEN,
                           (cx, cy + 8), (cx, cy - 2), 2)
            for i in range(6):
                angle = math.radians(i * 60)
                px = cx + int(6 * math.cos(angle))
                py = cy - 5 + int(6 * math.sin(angle))
                pygame.draw.circle(surface, TERRAIN_FLOWER_YELLOW, (px, py), 3)
            pygame.draw.circle(surface, CAFE_WOOD, (cx, cy - 5), 2)

        elif deco_type == 'flower_blue':
            pygame.draw.line(surface, FOREST_GREEN,
                           (cx, cy + 8), (cx, cy - 2), 2)
            for i in range(4):
                angle = math.radians(i * 90 + 45)
                px = cx + int(5 * math.cos(angle))
                py = cy - 5 + int(5 * math.sin(angle))
                pygame.draw.ellipse(surface, TERRAIN_FLOWER_BLUE,
                                  pygame.Rect(px - 3, py - 5, 6, 10))
            pygame.draw.circle(surface, WHITE, (cx, cy - 5), 2)

        elif deco_type == 'rock':
            pygame.draw.ellipse(surface, TERRAIN_STONE,
                              pygame.Rect(cx - 10, cy - 4, 20, 14))
            # Highlight
            pygame.draw.ellipse(surface, LIGHT_GRAY,
                              pygame.Rect(cx - 6, cy - 3, 8, 4))

        elif deco_type == 'bush':
            pygame.draw.circle(surface, FOREST_GREEN, (cx - 5, cy), 8)
            pygame.draw.circle(surface, FOREST_GREEN, (cx + 5, cy), 8)
            pygame.draw.circle(surface, FOREST_GREEN, (cx, cy - 5), 8)
            # Highlights
            lighter = tuple(min(255, c + 30) for c in FOREST_GREEN)
            pygame.draw.circle(surface, lighter, (cx - 3, cy - 6), 3)

        elif deco_type == 'tree':
            # Trunk
            pygame.draw.rect(surface, CAFE_WOOD,
                           pygame.Rect(cx - 3, cy, 6, 14))
            # Foliage
            pygame.draw.circle(surface, FOREST_GREEN, (cx, cy - 8), 12)
            pygame.draw.circle(surface, FOREST_GREEN, (cx - 8, cy - 2), 8)
            pygame.draw.circle(surface, FOREST_GREEN, (cx + 8, cy - 2), 8)

        return self._set_cached(key, surface)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_sprite_generator = None


def get_sprite_generator():
    """Get the global sprite generator instance."""
    global _sprite_generator
    if _sprite_generator is None:
        _sprite_generator = SpriteGenerator()
    return _sprite_generator
