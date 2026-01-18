"""
Zone Renderer for Dragon Haven Cafe.
Renders zone backgrounds and tile maps for exploration mode.
"""

import pygame
import math
from typing import Dict, Any, Optional, Tuple, List
from constants import (
    TILE_SIZE, ZONE_WIDTH, ZONE_HEIGHT,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GRASS_GREEN, FOREST_GREEN, WATER_BLUE, SKY_BLUE,
    TERRAIN_DIRT, TERRAIN_STONE, TERRAIN_SAND,
    TERRAIN_FLOWER_RED, TERRAIN_FLOWER_YELLOW, TERRAIN_FLOWER_BLUE,
    CAFE_WOOD, CAFE_WARM, CAFE_CREAM,
    ZONE_CAFE_GROUNDS, ZONE_MEADOW_FIELDS, ZONE_FOREST_DEPTHS,
    SPAWN_RARITY_COMMON, SPAWN_RARITY_UNCOMMON, SPAWN_RARITY_RARE,
)
from systems.world import TileType, Zone


class ZoneRenderer:
    """
    Renders zone tile maps and decorations.

    Usage:
        renderer = ZoneRenderer()
        renderer.set_zone(zone)
        renderer.draw(surface, camera_x, camera_y)
    """

    # Tile colors by type
    TILE_COLORS = {
        TileType.GRASS: GRASS_GREEN,
        TileType.DIRT: TERRAIN_DIRT,
        TileType.WATER: WATER_BLUE,
        TileType.STONE: TERRAIN_STONE,
        TileType.TREE: FOREST_GREEN,
        TileType.BUSH: (80, 140, 70),
        TileType.FLOWER: (140, 180, 100),
        TileType.BUILDING: CAFE_WOOD,
    }

    # Zone-specific color themes
    ZONE_THEMES = {
        ZONE_CAFE_GROUNDS: {
            'grass': (120, 170, 90),
            'accent': CAFE_CREAM,
            'tree': (60, 100, 50),
        },
        ZONE_MEADOW_FIELDS: {
            'grass': (140, 190, 100),
            'accent': (220, 200, 80),
            'tree': (70, 110, 50),
        },
        ZONE_FOREST_DEPTHS: {
            'grass': (80, 120, 60),
            'accent': (100, 80, 60),
            'tree': (40, 70, 35),
        },
    }

    # Spawn point indicator colors by rarity
    RARITY_COLORS = {
        SPAWN_RARITY_COMMON: (100, 200, 100),
        SPAWN_RARITY_UNCOMMON: (100, 140, 220),
        SPAWN_RARITY_RARE: (220, 180, 60),
    }

    def __init__(self):
        """Initialize the zone renderer."""
        self._zone: Optional[Zone] = None
        self._zone_id: str = ""
        self._cached_surface: Optional[pygame.Surface] = None
        self._needs_redraw = True

        # Decoration positions (generated per zone)
        self._decorations: List[Dict[str, Any]] = []

        # Animation timer
        self._anim_timer = 0.0

    def set_zone(self, zone: Zone, zone_id: str = ""):
        """
        Set the zone to render.

        Args:
            zone: Zone object to render
            zone_id: Zone ID for theming
        """
        self._zone = zone
        self._zone_id = zone_id
        self._needs_redraw = True
        self._generate_decorations()

    def _generate_decorations(self):
        """Generate random decorations for the zone."""
        import random
        self._decorations = []

        if not self._zone:
            return

        # Add small decorations to grass tiles
        for y in range(self._zone.height):
            for x in range(self._zone.width):
                tile = self._zone.get_tile(x, y)
                if tile == TileType.GRASS:
                    if random.random() < 0.15:
                        # Add a small decoration
                        dec_type = random.choice(['flower', 'grass_tuft', 'pebble'])
                        self._decorations.append({
                            'type': dec_type,
                            'x': x * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'y': y * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'color_var': random.randint(-20, 20),
                        })

    def update(self, dt: float):
        """Update animation timer."""
        self._anim_timer += dt

    def draw(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """
        Draw the zone.

        Args:
            surface: Surface to draw on
            camera_x, camera_y: Camera offset
        """
        if not self._zone:
            return

        # Draw tiles
        self._draw_tiles(surface, camera_x, camera_y)

        # Draw decorations
        self._draw_decorations(surface, camera_x, camera_y)

    def _draw_tiles(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """Draw all visible tiles."""
        if not self._zone:
            return

        # Get zone theme
        theme = self.ZONE_THEMES.get(self._zone_id, self.ZONE_THEMES[ZONE_CAFE_GROUNDS])

        # Calculate visible tile range
        start_x = max(0, camera_x // TILE_SIZE)
        start_y = max(0, camera_y // TILE_SIZE)
        end_x = min(self._zone.width, (camera_x + SCREEN_WIDTH) // TILE_SIZE + 2)
        end_y = min(self._zone.height, (camera_y + SCREEN_HEIGHT) // TILE_SIZE + 2)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self._zone.get_tile(x, y)
                if tile is None:
                    continue

                screen_x = x * TILE_SIZE - camera_x
                screen_y = y * TILE_SIZE - camera_y

                # Draw tile based on type
                self._draw_tile(surface, tile, screen_x, screen_y, theme, x, y)

    def _draw_tile(self, surface: pygame.Surface, tile_type: str, x: int, y: int,
                   theme: Dict[str, Any], tile_x: int, tile_y: int):
        """Draw a single tile."""
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        if tile_type == TileType.GRASS:
            # Grass with slight variation
            color = theme.get('grass', GRASS_GREEN)
            var = ((tile_x * 7 + tile_y * 13) % 3) * 5
            color = (
                min(255, color[0] + var),
                min(255, color[1] + var),
                min(255, color[2] - var)
            )
            pygame.draw.rect(surface, color, rect)

        elif tile_type == TileType.DIRT:
            pygame.draw.rect(surface, TERRAIN_DIRT, rect)
            # Add texture
            for i in range(3):
                px = x + (tile_x * 5 + i * 11) % (TILE_SIZE - 4) + 2
                py = y + (tile_y * 7 + i * 9) % (TILE_SIZE - 4) + 2
                pygame.draw.circle(surface, (120, 85, 60), (px, py), 2)

        elif tile_type == TileType.WATER:
            pygame.draw.rect(surface, WATER_BLUE, rect)
            # Animated water ripple
            wave_offset = math.sin(self._anim_timer * 2 + tile_x + tile_y) * 10
            highlight_color = (100, 160, 220)
            pygame.draw.line(surface, highlight_color,
                           (x + 4 + wave_offset, y + TILE_SIZE // 2),
                           (x + TILE_SIZE - 4 + wave_offset, y + TILE_SIZE // 2), 1)

        elif tile_type == TileType.STONE:
            pygame.draw.rect(surface, TERRAIN_STONE, rect)
            # Add stone texture
            pygame.draw.rect(surface, (120, 120, 120),
                           (x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8), border_radius=4)

        elif tile_type == TileType.TREE:
            # Tree trunk and foliage
            base_color = theme.get('tree', FOREST_GREEN)
            pygame.draw.rect(surface, theme.get('grass', GRASS_GREEN), rect)

            # Trunk
            trunk_rect = pygame.Rect(x + TILE_SIZE // 2 - 4, y + TILE_SIZE // 2,
                                    8, TILE_SIZE // 2)
            pygame.draw.rect(surface, CAFE_WOOD, trunk_rect)

            # Foliage
            foliage_color = (
                base_color[0] + ((tile_x + tile_y) % 3) * 10,
                base_color[1] + ((tile_x + tile_y) % 3) * 10,
                base_color[2]
            )
            pygame.draw.circle(surface, foliage_color,
                             (x + TILE_SIZE // 2, y + TILE_SIZE // 3), 14)
            pygame.draw.circle(surface, foliage_color,
                             (x + TILE_SIZE // 3, y + TILE_SIZE // 2), 10)
            pygame.draw.circle(surface, foliage_color,
                             (x + 2 * TILE_SIZE // 3, y + TILE_SIZE // 2), 10)

        elif tile_type == TileType.BUSH:
            pygame.draw.rect(surface, theme.get('grass', GRASS_GREEN), rect)
            # Bush shape
            pygame.draw.ellipse(surface, (80, 140, 70),
                              (x + 4, y + 8, TILE_SIZE - 8, TILE_SIZE - 12))
            pygame.draw.ellipse(surface, (60, 120, 50),
                              (x + 8, y + 12, TILE_SIZE - 16, TILE_SIZE - 18))

        elif tile_type == TileType.FLOWER:
            pygame.draw.rect(surface, theme.get('grass', GRASS_GREEN), rect)
            # Flower patches
            colors = [TERRAIN_FLOWER_RED, TERRAIN_FLOWER_YELLOW, TERRAIN_FLOWER_BLUE]
            for i in range(3):
                fx = x + (tile_x * 3 + i * 7) % (TILE_SIZE - 8) + 4
                fy = y + (tile_y * 5 + i * 11) % (TILE_SIZE - 8) + 4
                pygame.draw.circle(surface, colors[i % 3], (fx, fy), 4)
                pygame.draw.circle(surface, (255, 255, 200), (fx, fy), 2)

        elif tile_type == TileType.BUILDING:
            pygame.draw.rect(surface, CAFE_WOOD, rect)
            # Building detail
            pygame.draw.rect(surface, (100, 65, 40),
                           (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4), 2, border_radius=2)

        else:
            # Default
            color = self.TILE_COLORS.get(tile_type, (100, 100, 100))
            pygame.draw.rect(surface, color, rect)

    def _draw_decorations(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """Draw small decorations."""
        for dec in self._decorations:
            screen_x = dec['x'] - camera_x
            screen_y = dec['y'] - camera_y

            # Skip if off screen
            if screen_x < -10 or screen_x > SCREEN_WIDTH + 10:
                continue
            if screen_y < -10 or screen_y > SCREEN_HEIGHT + 10:
                continue

            var = dec['color_var']

            if dec['type'] == 'flower':
                colors = [(220 + var, 100, 120), (100, 180 + var, 220), (240, 200 + var, 100)]
                color = colors[abs(var) % 3]
                pygame.draw.circle(surface, color, (screen_x, screen_y), 3)
                pygame.draw.circle(surface, (255, 255, 200), (screen_x, screen_y), 1)

            elif dec['type'] == 'grass_tuft':
                color = (80 + var, 140 + var, 60)
                pygame.draw.line(surface, color, (screen_x, screen_y),
                               (screen_x - 2, screen_y - 5), 1)
                pygame.draw.line(surface, color, (screen_x, screen_y),
                               (screen_x + 1, screen_y - 6), 1)
                pygame.draw.line(surface, color, (screen_x, screen_y),
                               (screen_x + 3, screen_y - 4), 1)

            elif dec['type'] == 'pebble':
                color = (140 + var, 140 + var, 140 + var)
                pygame.draw.circle(surface, color, (screen_x, screen_y), 2)

    def draw_resource_indicators(self, surface: pygame.Surface,
                                  indicators: List[Dict[str, Any]],
                                  camera_x: int = 0, camera_y: int = 0):
        """
        Draw resource spawn point indicators.

        Args:
            surface: Surface to draw on
            indicators: List of indicator data from ResourceManager.get_zone_indicators()
            camera_x, camera_y: Camera offset
        """
        for ind in indicators:
            if not ind.get('visible', False):
                continue

            x = ind['x'] * TILE_SIZE + TILE_SIZE // 2 - camera_x
            y = ind['y'] * TILE_SIZE + TILE_SIZE // 2 - camera_y

            # Skip if off screen
            if x < -20 or x > SCREEN_WIDTH + 20:
                continue
            if y < -20 or y > SCREEN_HEIGHT + 20:
                continue

            # Get color based on rarity and availability
            if ind.get('available', False):
                base_color = self.RARITY_COLORS.get(ind.get('rarity', SPAWN_RARITY_COMMON),
                                                     (100, 200, 100))
                # Pulsing animation
                pulse = abs(math.sin(self._anim_timer * 3)) * 0.3 + 0.7
                color = tuple(int(c * pulse) for c in base_color)
            else:
                color = (80, 80, 80)  # Depleted - gray

            # Draw indicator
            self._draw_resource_indicator(surface, x, y, ind, color)

    def _draw_resource_indicator(self, surface: pygame.Surface, x: int, y: int,
                                  indicator: Dict[str, Any], color: Tuple[int, int, int]):
        """Draw a single resource indicator."""
        available = indicator.get('available', False)
        locked = indicator.get('locked', False)
        can_gather = indicator.get('can_gather', False)

        # Outer glow
        if available and can_gather:
            glow_surface = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*color, 60), (12, 12), 12)
            surface.blit(glow_surface, (x - 12, y - 12))

        # Main indicator circle
        pygame.draw.circle(surface, color, (x, y), 8)

        # Inner highlight
        if available:
            highlight = tuple(min(255, c + 60) for c in color)
            pygame.draw.circle(surface, highlight, (x - 2, y - 2), 3)

        # Lock icon if ability required
        if locked and not can_gather:
            pygame.draw.rect(surface, (60, 60, 60), (x - 3, y - 2, 6, 5), border_radius=1)
            pygame.draw.rect(surface, (80, 80, 80), (x - 2, y - 5, 4, 4), 1, border_radius=1)

        # Quality stars if available
        if available:
            quality = indicator.get('quality', 1)
            star_y = y + 12
            for i in range(quality):
                star_x = x - (quality * 3) + i * 6 + 3
                pygame.draw.polygon(surface, (255, 220, 60), [
                    (star_x, star_y - 3),
                    (star_x + 2, star_y),
                    (star_x + 4, star_y - 3),
                    (star_x + 3, star_y + 1),
                    (star_x + 4, star_y + 3),
                    (star_x, star_y + 1),
                    (star_x - 4, star_y + 3),
                    (star_x - 3, star_y + 1),
                    (star_x - 4, star_y - 3),
                    (star_x - 2, star_y),
                ])

    def draw_zone_exit(self, surface: pygame.Surface, x: int, y: int,
                       direction: str, zone_name: str,
                       camera_x: int = 0, camera_y: int = 0):
        """
        Draw a zone exit indicator.

        Args:
            surface: Surface to draw on
            x, y: Tile position of exit
            direction: Exit direction ('north', 'south', 'east', 'west')
            zone_name: Name of destination zone
            camera_x, camera_y: Camera offset
        """
        screen_x = x * TILE_SIZE + TILE_SIZE // 2 - camera_x
        screen_y = y * TILE_SIZE + TILE_SIZE // 2 - camera_y

        # Skip if off screen
        if screen_x < -40 or screen_x > SCREEN_WIDTH + 40:
            return
        if screen_y < -40 or screen_y > SCREEN_HEIGHT + 40:
            return

        # Draw arrow based on direction
        arrow_color = (200, 180, 100)
        pulse = abs(math.sin(self._anim_timer * 2)) * 0.3 + 0.7

        points = []
        if direction == 'north':
            points = [(screen_x, screen_y - 10), (screen_x - 8, screen_y + 5),
                     (screen_x + 8, screen_y + 5)]
        elif direction == 'south':
            points = [(screen_x, screen_y + 10), (screen_x - 8, screen_y - 5),
                     (screen_x + 8, screen_y - 5)]
        elif direction == 'east':
            points = [(screen_x + 10, screen_y), (screen_x - 5, screen_y - 8),
                     (screen_x - 5, screen_y + 8)]
        elif direction == 'west':
            points = [(screen_x - 10, screen_y), (screen_x + 5, screen_y - 8),
                     (screen_x + 5, screen_y + 8)]

        if points:
            color = tuple(int(c * pulse) for c in arrow_color)
            pygame.draw.polygon(surface, color, points)

        # Draw zone name
        font = pygame.font.Font(None, 20)
        text_surface = font.render(f"→ {zone_name}", True, (240, 230, 200))
        text_y = screen_y + 20 if direction in ['north', 'east', 'west'] else screen_y - 30
        text_rect = text_surface.get_rect(centerx=screen_x, y=text_y)
        surface.blit(text_surface, text_rect)
