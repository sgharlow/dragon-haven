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
    ZONE_COASTAL_SHORE, ZONE_MOUNTAIN_PASS, ZONE_ANCIENT_RUINS, ZONE_SKY_ISLANDS,
    SPAWN_RARITY_COMMON, SPAWN_RARITY_UNCOMMON, SPAWN_RARITY_RARE,
    SEASON_COLORS, SEASON_OVERLAY,
)
from systems.world import TileType, Zone
from systems.time_system import get_time_manager


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
        # Coastal tiles
        TileType.SAND: TERRAIN_SAND,
        TileType.SHALLOW_WATER: (100, 180, 220),
        TileType.SEAWEED: (40, 100, 60),
        TileType.TIDAL_POOL: (80, 140, 180),
        # Mountain tiles
        TileType.ROCK: (100, 95, 90),
        TileType.SNOW: (240, 245, 250),
        TileType.ALPINE_FLOWER: (200, 150, 220),
        TileType.HOT_SPRING: (100, 160, 200),
        # Ancient Ruins tiles
        TileType.RUIN_FLOOR: (140, 130, 120),
        TileType.RUIN_WALL: (90, 85, 80),
        TileType.CRYSTAL_CLUSTER: (140, 180, 200),
        TileType.OVERGROWN: (80, 100, 70),
        TileType.ANCIENT_PATH: (160, 150, 130),
        # Sky Islands tiles
        TileType.CLOUD: (240, 245, 255),
        TileType.SKY_CRYSTAL: (180, 200, 255),
        TileType.FLOATING_GRASS: (140, 200, 160),
        TileType.STARLIGHT_POOL: (200, 180, 240),
        TileType.WIND_STREAM: (220, 235, 255),
        TileType.VOID: (20, 30, 60),
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
        ZONE_COASTAL_SHORE: {
            'grass': (160, 190, 130),  # Sandy dune grass
            'accent': (220, 200, 150),  # Sand accent
            'tree': (70, 100, 60),  # Coastal scrub
            'sand': (220, 200, 150),  # Beach sand
            'water': (80, 160, 200),  # Ocean blue
        },
        ZONE_MOUNTAIN_PASS: {
            'grass': (100, 140, 90),  # Alpine grass
            'accent': (180, 160, 140),  # Rocky accent
            'tree': (50, 80, 45),  # Mountain pine
            'rock': (120, 115, 110),  # Mountain rock
            'snow': (240, 245, 250),  # Snow patches
        },
        ZONE_ANCIENT_RUINS: {
            'grass': (70, 90, 60),  # Moss-covered grass
            'accent': (150, 140, 130),  # Aged stone accent
            'tree': (50, 70, 45),  # Old overgrown trees
            'ruin': (130, 120, 110),  # Ruin stone
            'crystal': (120, 160, 190),  # Crystal formations
            'moss': (60, 80, 55),  # Ancient moss
        },
        ZONE_SKY_ISLANDS: {
            'grass': (140, 200, 160),  # Ethereal floating grass
            'accent': (220, 200, 255),  # Celestial accent
            'tree': (80, 140, 100),  # Floating island trees
            'cloud': (240, 245, 255),  # Cloud platforms
            'crystal': (180, 200, 255),  # Sky crystals
            'void': (20, 30, 60),  # Void between islands
            'starlight': (200, 180, 240),  # Starlight pools
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

        # Season tracking (updated from time system)
        self._current_season: str = 'spring'
        self._season_colors: Dict[str, Tuple[int, int, int]] = SEASON_COLORS.get('spring', {})

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

        # Add small decorations based on tile type
        for y in range(self._zone.height):
            for x in range(self._zone.width):
                tile = self._zone.get_tile(x, y)

                if tile == TileType.GRASS:
                    if random.random() < 0.15:
                        dec_type = random.choice(['flower', 'grass_tuft', 'pebble'])
                        self._decorations.append({
                            'type': dec_type,
                            'x': x * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'y': y * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'color_var': random.randint(-20, 20),
                        })

                # Coastal decorations
                elif tile == TileType.SAND:
                    if random.random() < 0.1:
                        dec_type = random.choice(['shell', 'driftwood', 'beach_pebble'])
                        self._decorations.append({
                            'type': dec_type,
                            'x': x * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'y': y * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'color_var': random.randint(-15, 15),
                        })

                # Mountain decorations
                elif tile == TileType.ROCK:
                    if random.random() < 0.08:
                        dec_type = random.choice(['small_rock', 'lichen', 'crystal_shard'])
                        self._decorations.append({
                            'type': dec_type,
                            'x': x * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'y': y * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'color_var': random.randint(-10, 10),
                        })

                # Sky Islands decorations
                elif tile == TileType.FLOATING_GRASS:
                    if random.random() < 0.12:
                        dec_type = random.choice(['sky_flower', 'cloud_wisp', 'starlight_mote'])
                        self._decorations.append({
                            'type': dec_type,
                            'x': x * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'y': y * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'color_var': random.randint(-15, 15),
                        })

                elif tile == TileType.CLOUD:
                    if random.random() < 0.06:
                        dec_type = random.choice(['cloud_wisp', 'starlight_mote'])
                        self._decorations.append({
                            'type': dec_type,
                            'x': x * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'y': y * TILE_SIZE + random.randint(4, TILE_SIZE - 4),
                            'color_var': random.randint(-10, 10),
                        })

    def update(self, dt: float):
        """Update animation timer and check for season changes."""
        self._anim_timer += dt

        # Check if season changed
        time_mgr = get_time_manager()
        current_season = time_mgr.get_current_season()
        if current_season != self._current_season:
            self._current_season = current_season
            self._season_colors = SEASON_COLORS.get(current_season, SEASON_COLORS.get('spring', {}))
            self._needs_redraw = True

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

        # Apply seasonal overlay
        self._draw_seasonal_overlay(surface)

    def _draw_seasonal_overlay(self, surface: pygame.Surface):
        """Apply a subtle seasonal tint overlay."""
        overlay_data = SEASON_OVERLAY.get(self._current_season)
        if overlay_data and overlay_data[3] > 0:  # If alpha > 0
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(overlay_data)
            surface.blit(overlay, (0, 0))

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
            # Grass with seasonal and slight variation
            # Blend zone theme with seasonal colors
            base_color = theme.get('grass', GRASS_GREEN)
            seasonal_grass = self._season_colors.get('grass', base_color)
            # Blend 60% zone theme, 40% seasonal
            color = (
                int(base_color[0] * 0.6 + seasonal_grass[0] * 0.4),
                int(base_color[1] * 0.6 + seasonal_grass[1] * 0.4),
                int(base_color[2] * 0.6 + seasonal_grass[2] * 0.4),
            )
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
            # Tree trunk and foliage with seasonal colors
            base_tree = theme.get('tree', FOREST_GREEN)
            seasonal_leaves = self._season_colors.get('leaves', base_tree)
            # Blend zone theme with seasonal
            base_color = (
                int(base_tree[0] * 0.5 + seasonal_leaves[0] * 0.5),
                int(base_tree[1] * 0.5 + seasonal_leaves[1] * 0.5),
                int(base_tree[2] * 0.5 + seasonal_leaves[2] * 0.5),
            )

            # Draw grass background with seasonal color
            grass_base = theme.get('grass', GRASS_GREEN)
            seasonal_grass = self._season_colors.get('grass', grass_base)
            grass_color = (
                int(grass_base[0] * 0.6 + seasonal_grass[0] * 0.4),
                int(grass_base[1] * 0.6 + seasonal_grass[1] * 0.4),
                int(grass_base[2] * 0.6 + seasonal_grass[2] * 0.4),
            )
            pygame.draw.rect(surface, grass_color, rect)

            # Trunk
            trunk_rect = pygame.Rect(x + TILE_SIZE // 2 - 4, y + TILE_SIZE // 2,
                                    8, TILE_SIZE // 2)
            pygame.draw.rect(surface, CAFE_WOOD, trunk_rect)

            # Foliage with seasonal variation
            foliage_color = (
                min(255, base_color[0] + ((tile_x + tile_y) % 3) * 10),
                min(255, base_color[1] + ((tile_x + tile_y) % 3) * 10),
                base_color[2]
            )
            pygame.draw.circle(surface, foliage_color,
                             (x + TILE_SIZE // 2, y + TILE_SIZE // 3), 14)
            pygame.draw.circle(surface, foliage_color,
                             (x + TILE_SIZE // 3, y + TILE_SIZE // 2), 10)
            pygame.draw.circle(surface, foliage_color,
                             (x + 2 * TILE_SIZE // 3, y + TILE_SIZE // 2), 10)

        elif tile_type == TileType.BUSH:
            # Bush with seasonal grass background
            grass_base = theme.get('grass', GRASS_GREEN)
            seasonal_grass = self._season_colors.get('grass', grass_base)
            grass_color = (
                int(grass_base[0] * 0.6 + seasonal_grass[0] * 0.4),
                int(grass_base[1] * 0.6 + seasonal_grass[1] * 0.4),
                int(grass_base[2] * 0.6 + seasonal_grass[2] * 0.4),
            )
            pygame.draw.rect(surface, grass_color, rect)

            # Bush with seasonal leaf color
            seasonal_leaves = self._season_colors.get('leaves', (80, 140, 70))
            bush_color = (
                int(80 * 0.5 + seasonal_leaves[0] * 0.5),
                int(140 * 0.5 + seasonal_leaves[1] * 0.5),
                int(70 * 0.5 + seasonal_leaves[2] * 0.5),
            )
            bush_dark = (max(0, bush_color[0] - 20), max(0, bush_color[1] - 20), max(0, bush_color[2] - 20))
            pygame.draw.ellipse(surface, bush_color,
                              (x + 4, y + 8, TILE_SIZE - 8, TILE_SIZE - 12))
            pygame.draw.ellipse(surface, bush_dark,
                              (x + 8, y + 12, TILE_SIZE - 16, TILE_SIZE - 18))

        elif tile_type == TileType.FLOWER:
            # Grass background with seasonal color
            grass_base = theme.get('grass', GRASS_GREEN)
            seasonal_grass = self._season_colors.get('grass', grass_base)
            grass_color = (
                int(grass_base[0] * 0.6 + seasonal_grass[0] * 0.4),
                int(grass_base[1] * 0.6 + seasonal_grass[1] * 0.4),
                int(grass_base[2] * 0.6 + seasonal_grass[2] * 0.4),
            )
            pygame.draw.rect(surface, grass_color, rect)

            # Flower patches with seasonal accent colors
            seasonal_accent = self._season_colors.get('accent', TERRAIN_FLOWER_YELLOW)
            colors = [TERRAIN_FLOWER_RED, seasonal_accent, TERRAIN_FLOWER_BLUE]
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

        # Coastal tiles
        elif tile_type == TileType.SAND:
            sand_color = theme.get('sand', TERRAIN_SAND)
            pygame.draw.rect(surface, sand_color, rect)
            # Sand texture dots
            for i in range(4):
                px = x + (tile_x * 7 + i * 9) % (TILE_SIZE - 4) + 2
                py = y + (tile_y * 5 + i * 11) % (TILE_SIZE - 4) + 2
                pygame.draw.circle(surface, tuple(max(0, c - 15) for c in sand_color), (px, py), 1)

        elif tile_type == TileType.SHALLOW_WATER:
            water_color = theme.get('water', (100, 180, 220))
            pygame.draw.rect(surface, water_color, rect)
            # Animated ripples
            wave_offset = math.sin(self._anim_timer * 1.5 + tile_x + tile_y) * 8
            lighter = tuple(min(255, c + 30) for c in water_color)
            pygame.draw.arc(surface, lighter, pygame.Rect(x, y + TILE_SIZE // 3 + wave_offset // 2,
                          TILE_SIZE, TILE_SIZE // 3), 0, 3.14, 1)

        elif tile_type == TileType.SEAWEED:
            # Sandy base
            sand_color = theme.get('sand', TERRAIN_SAND)
            pygame.draw.rect(surface, sand_color, rect)
            # Green seaweed strands
            seaweed_color = (40, 100, 60)
            for i in range(3):
                sx = x + 6 + i * 10
                wave = math.sin(self._anim_timer * 2 + i) * 2
                pygame.draw.line(surface, seaweed_color, (sx, y + TILE_SIZE),
                               (sx + wave, y + TILE_SIZE // 2), 2)

        elif tile_type == TileType.TIDAL_POOL:
            sand_color = theme.get('sand', TERRAIN_SAND)
            pygame.draw.rect(surface, sand_color, rect)
            # Water pool
            pool_color = (80, 140, 180)
            pygame.draw.ellipse(surface, pool_color, (x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8))
            pygame.draw.ellipse(surface, (100, 160, 200), (x + 6, y + 6, TILE_SIZE - 14, TILE_SIZE - 14))

        # Mountain tiles
        elif tile_type == TileType.ROCK:
            rock_color = theme.get('rock', (100, 95, 90))
            pygame.draw.rect(surface, rock_color, rect)
            # Rock texture
            lighter = tuple(min(255, c + 15) for c in rock_color)
            darker = tuple(max(0, c - 15) for c in rock_color)
            pygame.draw.polygon(surface, lighter, [(x, y + TILE_SIZE), (x + TILE_SIZE // 3, y + TILE_SIZE // 2),
                              (x, y + TILE_SIZE // 3)])
            pygame.draw.polygon(surface, darker, [(x + TILE_SIZE, y), (x + TILE_SIZE * 2 // 3, y + TILE_SIZE // 2),
                              (x + TILE_SIZE, y + TILE_SIZE * 2 // 3)])

        elif tile_type == TileType.SNOW:
            snow_color = theme.get('snow', (240, 245, 250))
            pygame.draw.rect(surface, snow_color, rect)
            # Snow sparkle
            for i in range(3):
                px = x + (tile_x * 9 + i * 11) % (TILE_SIZE - 4) + 2
                py = y + (tile_y * 7 + i * 9) % (TILE_SIZE - 4) + 2
                pygame.draw.circle(surface, (255, 255, 255), (px, py), 1)

        elif tile_type == TileType.ALPINE_FLOWER:
            # Grass base with seasonal color
            grass_color = theme.get('grass', (100, 140, 90))
            pygame.draw.rect(surface, grass_color, rect)
            # Alpine flowers (pink/purple)
            flower_colors = [(220, 120, 180), (180, 100, 200), (200, 150, 220)]
            for i in range(3):
                fx = x + (tile_x * 5 + i * 9) % (TILE_SIZE - 8) + 4
                fy = y + (tile_y * 7 + i * 7) % (TILE_SIZE - 8) + 4
                pygame.draw.circle(surface, flower_colors[i % 3], (fx, fy), 3)
                pygame.draw.circle(surface, (255, 220, 100), (fx, fy), 1)

        elif tile_type == TileType.HOT_SPRING:
            spring_color = (100, 160, 200)
            pygame.draw.rect(surface, spring_color, rect)
            # Steam bubbles animation
            bubble_offset = math.sin(self._anim_timer * 3 + tile_x) * 3
            for i in range(3):
                bx = x + 8 + (i * 10)
                by = y + 8 + bubble_offset - i * 2
                pygame.draw.circle(surface, (200, 220, 240), (int(bx), int(by)), 2)
            # Warm glow edge
            pygame.draw.rect(surface, (180, 140, 120), rect, 2, border_radius=4)

        # Sky Islands tiles
        elif tile_type == TileType.CLOUD:
            cloud_color = theme.get('cloud', (240, 245, 255))
            pygame.draw.rect(surface, cloud_color, rect)
            # Fluffy cloud texture
            lighter = tuple(min(255, c + 10) for c in cloud_color)
            pygame.draw.ellipse(surface, lighter, (x + 2, y + 4, TILE_SIZE - 4, TILE_SIZE - 8))
            pygame.draw.ellipse(surface, lighter, (x + 6, y + 2, TILE_SIZE - 12, TILE_SIZE - 6))

        elif tile_type == TileType.SKY_CRYSTAL:
            crystal_color = theme.get('crystal', (180, 200, 255))
            # Dark base
            pygame.draw.rect(surface, (40, 50, 80), rect)
            # Crystal formation
            pygame.draw.polygon(surface, crystal_color, [
                (x + TILE_SIZE // 2, y + 2),
                (x + TILE_SIZE - 4, y + TILE_SIZE - 4),
                (x + 4, y + TILE_SIZE - 4)
            ])
            # Shimmer
            shimmer = math.sin(self._anim_timer * 4 + tile_x + tile_y) * 20 + 235
            pygame.draw.line(surface, (int(shimmer), int(shimmer), 255),
                           (x + TILE_SIZE // 2, y + 4), (x + TILE_SIZE // 2 - 3, y + TILE_SIZE // 2), 2)

        elif tile_type == TileType.FLOATING_GRASS:
            grass_color = theme.get('grass', (140, 200, 160))
            pygame.draw.rect(surface, grass_color, rect)
            # Glowing grass blades
            for i in range(4):
                gx = x + 4 + i * 8
                glow = abs(math.sin(self._anim_timer * 2 + i)) * 30
                blade_color = tuple(min(255, int(c + glow)) for c in grass_color)
                pygame.draw.line(surface, blade_color, (gx, y + TILE_SIZE - 2),
                               (gx + 2, y + TILE_SIZE // 2), 1)

        elif tile_type == TileType.STARLIGHT_POOL:
            starlight_color = theme.get('starlight', (200, 180, 240))
            pygame.draw.rect(surface, (60, 50, 100), rect)  # Dark base
            pygame.draw.ellipse(surface, starlight_color, (x + 3, y + 3, TILE_SIZE - 6, TILE_SIZE - 6))
            # Animated stars
            for i in range(3):
                star_x = x + (tile_x * 7 + i * 11) % (TILE_SIZE - 8) + 4
                star_y = y + (tile_y * 9 + i * 7) % (TILE_SIZE - 8) + 4
                twinkle = abs(math.sin(self._anim_timer * 3 + i)) * 255
                pygame.draw.circle(surface, (int(twinkle), int(twinkle), 255), (star_x, star_y), 1)

        elif tile_type == TileType.WIND_STREAM:
            # Transparent wind effect
            pygame.draw.rect(surface, (180, 200, 240), rect)
            # Animated wind lines
            for i in range(3):
                wind_offset = (self._anim_timer * 50 + i * 20) % TILE_SIZE
                alpha_color = (220, 235, 255)
                pygame.draw.line(surface, alpha_color,
                               (x + wind_offset, y + 4 + i * 10),
                               (x + wind_offset + 12, y + 4 + i * 10), 2)

        elif tile_type == TileType.VOID:
            void_color = theme.get('void', (20, 30, 60))
            pygame.draw.rect(surface, void_color, rect)
            # Distant stars
            for i in range(2):
                sx = x + (tile_x * 11 + i * 17) % (TILE_SIZE - 4) + 2
                sy = y + (tile_y * 13 + i * 19) % (TILE_SIZE - 4) + 2
                twinkle = abs(math.sin(self._anim_timer * 2 + tile_x + tile_y + i)) * 100 + 50
                pygame.draw.circle(surface, (int(twinkle), int(twinkle), int(twinkle + 50)), (sx, sy), 1)

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
                # Use seasonal accent color for variety
                seasonal_accent = self._season_colors.get('accent', (240, 200, 100))
                colors = [
                    (220 + var, 100, 120),
                    (seasonal_accent[0], seasonal_accent[1] + var, seasonal_accent[2]),
                    (100, 180 + var, 220)
                ]
                color = colors[abs(var) % 3]
                pygame.draw.circle(surface, color, (screen_x, screen_y), 3)
                pygame.draw.circle(surface, (255, 255, 200), (screen_x, screen_y), 1)

            elif dec['type'] == 'grass_tuft':
                # Use seasonal grass color for tufts
                seasonal_grass = self._season_colors.get('grass', (100, 180, 80))
                color = (
                    max(0, min(255, seasonal_grass[0] - 20 + var)),
                    max(0, min(255, seasonal_grass[1] - 40 + var)),
                    max(0, min(255, seasonal_grass[2] - 20))
                )
                pygame.draw.line(surface, color, (screen_x, screen_y),
                               (screen_x - 2, screen_y - 5), 1)
                pygame.draw.line(surface, color, (screen_x, screen_y),
                               (screen_x + 1, screen_y - 6), 1)
                pygame.draw.line(surface, color, (screen_x, screen_y),
                               (screen_x + 3, screen_y - 4), 1)

            elif dec['type'] == 'pebble':
                color = (140 + var, 140 + var, 140 + var)
                pygame.draw.circle(surface, color, (screen_x, screen_y), 2)

            # Coastal decorations
            elif dec['type'] == 'shell':
                # Small seashell
                shell_color = (240 + var, 220 + var, 200)
                pygame.draw.ellipse(surface, shell_color, (screen_x - 3, screen_y - 2, 6, 4))
                pygame.draw.arc(surface, (200 + var, 180 + var, 160), (screen_x - 3, screen_y - 2, 6, 4), 0, 3.14, 1)

            elif dec['type'] == 'driftwood':
                # Small piece of driftwood
                wood_color = (140 + var, 120 + var, 100)
                pygame.draw.line(surface, wood_color, (screen_x - 4, screen_y), (screen_x + 4, screen_y - 1), 2)

            elif dec['type'] == 'beach_pebble':
                # Smooth beach pebble
                pebble_color = (180 + var, 175 + var, 165)
                pygame.draw.ellipse(surface, pebble_color, (screen_x - 2, screen_y - 1, 4, 3))

            # Mountain decorations
            elif dec['type'] == 'small_rock':
                # Angular small rock
                rock_color = (100 + var, 95 + var, 90)
                pygame.draw.polygon(surface, rock_color, [
                    (screen_x, screen_y - 2), (screen_x + 3, screen_y), (screen_x + 2, screen_y + 2),
                    (screen_x - 2, screen_y + 2), (screen_x - 3, screen_y)
                ])

            elif dec['type'] == 'lichen':
                # Greenish-gray lichen patch
                lichen_color = (100 + var, 120 + var, 90)
                pygame.draw.circle(surface, lichen_color, (screen_x, screen_y), 3)
                pygame.draw.circle(surface, (90 + var, 110 + var, 80), (screen_x + 1, screen_y - 1), 2)

            elif dec['type'] == 'crystal_shard':
                # Small crystal shard
                crystal_color = (180 + var, 200 + var, 220)
                pygame.draw.polygon(surface, crystal_color, [
                    (screen_x, screen_y - 4), (screen_x + 2, screen_y + 1), (screen_x - 2, screen_y + 1)
                ])
                pygame.draw.polygon(surface, (200 + var, 220 + var, 240), [
                    (screen_x - 1, screen_y - 2), (screen_x + 1, screen_y), (screen_x - 1, screen_y)
                ])

            # Sky Islands decorations
            elif dec['type'] == 'sky_flower':
                # Ethereal floating flower
                flower_color = (200 + var, 180, 240)
                pygame.draw.circle(surface, flower_color, (screen_x, screen_y), 3)
                pygame.draw.circle(surface, (255, 240, 255), (screen_x, screen_y), 1)
                # Petals
                for angle in range(0, 360, 72):
                    import math
                    px = screen_x + int(math.cos(math.radians(angle)) * 4)
                    py = screen_y + int(math.sin(math.radians(angle)) * 4)
                    pygame.draw.circle(surface, (220 + var, 200, 255), (px, py), 2)

            elif dec['type'] == 'cloud_wisp':
                # Small wispy cloud
                wisp_color = (240 + var, 245, 255)
                pygame.draw.ellipse(surface, wisp_color, (screen_x - 4, screen_y - 2, 8, 4))
                pygame.draw.ellipse(surface, wisp_color, (screen_x - 2, screen_y - 3, 5, 3))

            elif dec['type'] == 'starlight_mote':
                # Glowing starlight particle
                glow = abs(var) % 40 + 200
                pygame.draw.circle(surface, (glow, glow, 255), (screen_x, screen_y), 2)
                pygame.draw.circle(surface, (255, 255, 255), (screen_x, screen_y), 1)

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
