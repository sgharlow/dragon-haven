"""
Exploration Mode State for Dragon Haven Cafe.
Handles zone exploration, resource gathering, and dragon interactions.
"""

import pygame
import math
from typing import Optional, Dict, Any, List, Tuple
from states.base_state import BaseScreen
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    TILE_SIZE, ZONE_WIDTH, ZONE_HEIGHT,
    ZONE_CAFE_GROUNDS, ZONE_MEADOW_FIELDS, ZONE_FOREST_DEPTHS,
    HUD_MODE_EXPLORATION, NOTIFICATION_SUCCESS, NOTIFICATION_INFO, NOTIFICATION_WARNING,
    DRAGON_STAGE_EGG, DRAGON_STAGE_HATCHLING, DRAGON_STAGE_JUVENILE,
    CAFE_CREAM, UI_TEXT, UI_TEXT_DIM, UI_BG, UI_PANEL,
)
from entities.player import Player
from entities.dragon import Dragon
from systems.world import get_world_manager, Zone
from systems.resources import get_resource_manager
from systems.time_system import get_time_manager
from systems.inventory import get_inventory
from ui.zone_renderer import ZoneRenderer
from ui.hud import HUD


class DragonCompanion:
    """
    Visual representation of the dragon companion that follows the player.
    """

    def __init__(self):
        """Initialize the dragon companion."""
        self.pixel_x = 0.0
        self.pixel_y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0

        # Animation
        self._anim_timer = 0.0
        self._bob_offset = 0.0
        self._facing = 'down'

        # Dragon reference
        self._dragon: Optional[Dragon] = None

        # Follow settings
        self.follow_distance = 40.0  # Pixels behind player
        self.follow_speed = 3.0  # Pixels per frame

    def set_dragon(self, dragon: Dragon):
        """Set the dragon reference for stats/appearance."""
        self._dragon = dragon

    def set_target(self, x: float, y: float, facing: str):
        """Set target position to follow."""
        # Offset based on player facing
        offset_x, offset_y = 0, 0
        if facing == 'up':
            offset_y = self.follow_distance
        elif facing == 'down':
            offset_y = -self.follow_distance
        elif facing == 'left':
            offset_x = self.follow_distance
        elif facing == 'right':
            offset_x = -self.follow_distance

        self.target_x = x + offset_x
        self.target_y = y + offset_y
        self._facing = facing

    def update(self, dt: float):
        """Update companion position and animation."""
        # Move towards target
        dx = self.target_x - self.pixel_x
        dy = self.target_y - self.pixel_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 5:
            speed = min(self.follow_speed, dist * 0.1) * 60 * dt
            self.pixel_x += (dx / dist) * speed
            self.pixel_y += (dy / dist) * speed

        # Animation
        self._anim_timer += dt
        self._bob_offset = math.sin(self._anim_timer * 3) * 3

    def draw(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """Draw the dragon companion."""
        if not self._dragon:
            return

        screen_x = int(self.pixel_x - camera_x)
        screen_y = int(self.pixel_y - camera_y) + int(self._bob_offset)

        stage = self._dragon.get_stage()
        color_shift = self._dragon.get_color_shift()

        # Draw based on stage
        if stage == DRAGON_STAGE_EGG:
            self._draw_egg(surface, screen_x, screen_y, color_shift)
        elif stage == DRAGON_STAGE_HATCHLING:
            self._draw_hatchling(surface, screen_x, screen_y, color_shift)
        else:  # Juvenile
            self._draw_juvenile(surface, screen_x, screen_y, color_shift)

    def _draw_egg(self, surface: pygame.Surface, x: int, y: int, color_shift: Tuple[int, int, int]):
        """Draw egg stage."""
        base_color = (220, 210, 190)
        color = tuple(max(0, min(255, base_color[i] + color_shift[i])) for i in range(3))

        # Egg shape
        pygame.draw.ellipse(surface, color, (x - 10, y - 15, 20, 28))
        # Spots
        pygame.draw.circle(surface, (180, 160, 130), (x - 4, y - 8), 3)
        pygame.draw.circle(surface, (180, 160, 130), (x + 5, y - 2), 4)
        pygame.draw.circle(surface, (180, 160, 130), (x - 2, y + 5), 3)

    def _draw_hatchling(self, surface: pygame.Surface, x: int, y: int, color_shift: Tuple[int, int, int]):
        """Draw hatchling stage (small dragon)."""
        base_color = (140, 200, 160)
        color = tuple(max(0, min(255, base_color[i] + color_shift[i])) for i in range(3))
        belly_color = (200, 220, 190)

        # Body
        pygame.draw.ellipse(surface, color, (x - 12, y - 8, 24, 20))
        # Belly
        pygame.draw.ellipse(surface, belly_color, (x - 8, y - 2, 16, 14))
        # Head
        pygame.draw.circle(surface, color, (x, y - 12), 10)
        # Eyes
        pygame.draw.circle(surface, (60, 40, 30), (x - 4, y - 14), 3)
        pygame.draw.circle(surface, (60, 40, 30), (x + 4, y - 14), 3)
        pygame.draw.circle(surface, (255, 255, 255), (x - 5, y - 15), 1)
        pygame.draw.circle(surface, (255, 255, 255), (x + 3, y - 15), 1)
        # Small wings
        wing_color = (80, 150, 110)
        pygame.draw.ellipse(surface, wing_color, (x - 18, y - 6, 10, 8))
        pygame.draw.ellipse(surface, wing_color, (x + 8, y - 6, 10, 8))
        # Tail
        pygame.draw.polygon(surface, color, [
            (x + 10, y + 6), (x + 18, y + 10), (x + 12, y + 12)
        ])

    def _draw_juvenile(self, surface: pygame.Surface, x: int, y: int, color_shift: Tuple[int, int, int]):
        """Draw juvenile stage (larger dragon)."""
        base_color = (100, 180, 130)
        color = tuple(max(0, min(255, base_color[i] + color_shift[i])) for i in range(3))
        belly_color = (200, 220, 190)
        wing_color = (80, 150, 110)

        # Shadow
        shadow_surface = pygame.Surface((36, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 40), shadow_surface.get_rect())
        surface.blit(shadow_surface, (x - 18, y + 14))

        # Body
        pygame.draw.ellipse(surface, color, (x - 16, y - 10, 32, 28))
        # Belly
        pygame.draw.ellipse(surface, belly_color, (x - 10, y, 20, 18))
        # Head
        pygame.draw.circle(surface, color, (x, y - 16), 14)
        # Snout
        pygame.draw.ellipse(surface, color, (x - 4, y - 18, 8, 6))
        # Eyes
        pygame.draw.circle(surface, (60, 40, 30), (x - 6, y - 18), 4)
        pygame.draw.circle(surface, (60, 40, 30), (x + 6, y - 18), 4)
        pygame.draw.circle(surface, (255, 255, 255), (x - 7, y - 19), 2)
        pygame.draw.circle(surface, (255, 255, 255), (x + 5, y - 19), 2)
        # Wings
        wing_points_left = [(x - 14, y - 6), (x - 28, y - 16), (x - 30, y + 2), (x - 18, y + 4)]
        wing_points_right = [(x + 14, y - 6), (x + 28, y - 16), (x + 30, y + 2), (x + 18, y + 4)]
        pygame.draw.polygon(surface, wing_color, wing_points_left)
        pygame.draw.polygon(surface, wing_color, wing_points_right)
        # Tail
        pygame.draw.polygon(surface, color, [
            (x + 14, y + 8), (x + 30, y + 12), (x + 24, y + 18), (x + 16, y + 14)
        ])
        # Horns
        pygame.draw.polygon(surface, (80, 60, 50), [
            (x - 8, y - 28), (x - 10, y - 20), (x - 6, y - 22)
        ])
        pygame.draw.polygon(surface, (80, 60, 50), [
            (x + 8, y - 28), (x + 10, y - 20), (x + 6, y - 22)
        ])


class ExplorationModeState(BaseScreen):
    """
    Exploration mode where players explore zones, gather resources,
    and interact with their dragon.

    Usage:
        state = ExplorationModeState(game)
        game.state_manager.push_state(state)
    """

    def __init__(self, game):
        """Initialize exploration mode."""
        super().__init__(game)
        self.title = ""  # No title in exploration mode
        self.background_color = (60, 80, 60)

        # Get system managers
        self.world = get_world_manager()
        self.resources = get_resource_manager()
        self.time_mgr = get_time_manager()
        self.inventory = get_inventory()

        # Initialize if needed
        self.world.initialize()
        self.resources.initialize()

        # Player
        self.player = Player(ZONE_WIDTH // 2, ZONE_HEIGHT // 2)

        # Dragon companion
        self.dragon_companion = DragonCompanion()
        self._dragon: Optional[Dragon] = None

        # Zone renderer
        self.zone_renderer = ZoneRenderer()

        # HUD
        self.hud = HUD()
        self.hud.set_mode(HUD_MODE_EXPLORATION)

        # Camera
        self.camera_x = 0
        self.camera_y = 0

        # Interaction state
        self._interaction_text = ""
        self._interaction_timer = 0.0
        self._gathering = False
        self._gather_progress = 0.0
        self._gather_target = None

        # Zone transition
        self._transitioning = False
        self._transition_target = None

        # Ability use
        self._ability_effects: List[Dict[str, Any]] = []

        # Fonts
        self.prompt_font = pygame.font.Font(None, 24)
        self.info_font = pygame.font.Font(None, 20)

    def set_dragon(self, dragon: Dragon):
        """Set the player's dragon."""
        self._dragon = dragon
        self.dragon_companion.set_dragon(dragon)

    def enter(self, previous_state=None):
        """Enter exploration mode."""
        super().enter(previous_state)

        # Load current zone
        zone = self.world.get_current_zone()
        if zone:
            self.zone_renderer.set_zone(zone, self.world.get_current_zone_id())

        # Set player position from world manager
        px, py = self.world.get_player_position()
        self.player.set_tile_position(px, py)

        # Initialize dragon companion position
        player_pos = self.player.get_pixel_position()
        self.dragon_companion.pixel_x = player_pos[0]
        self.dragon_companion.pixel_y = player_pos[1] + 40

        # Update HUD
        self._update_hud()

        # Add notification
        zone_name = zone.name if zone else "Unknown"
        self.hud.add_notification(f"Entered {zone_name}", NOTIFICATION_INFO, 3.0)

    def exit(self):
        """Exit exploration mode."""
        super().exit()
        # Save player position
        tx, ty = self.player.get_tile_position()
        self.world.set_player_position(tx, ty)

    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        # Let HUD handle events first
        if self.hud.handle_event(event):
            return

        if event.type == pygame.KEYDOWN:
            # Escape to exit to menu
            if event.key == pygame.K_ESCAPE:
                self.fade_to_state('main_menu')
                return

            # P to pet dragon
            if event.key == pygame.K_p:
                self._pet_dragon()
                return

            # C to open cafe (if in cafe grounds)
            if event.key == pygame.K_c:
                if self.world.get_current_zone_id() == ZONE_CAFE_GROUNDS:
                    self.fade_to_state('cafe_mode')
                    return

    def update(self, dt: float) -> bool:
        """Update exploration state."""
        super().update(dt)

        if self._transitioning:
            return True

        # Get keyboard state
        keys = pygame.key.get_pressed()

        # Handle player input and movement
        self.player.handle_input(keys)
        self.player.update(dt, self._check_collision)

        # Update dragon companion
        player_pos = self.player.get_pixel_position()
        self.dragon_companion.set_target(player_pos[0], player_pos[1], self.player._facing)
        self.dragon_companion.update(dt)

        # Update dragon stats if we have one
        if self._dragon:
            self._dragon.update(dt)

        # Update camera
        self._update_camera()

        # Update zone renderer
        self.zone_renderer.update(dt)

        # Handle interactions
        self._handle_interactions(keys, dt)

        # Update HUD
        self._update_hud()
        self.hud.update(dt)

        # Update interaction text timer
        if self._interaction_timer > 0:
            self._interaction_timer -= dt
            if self._interaction_timer <= 0:
                self._interaction_text = ""

        # Update ability effects
        self._update_ability_effects(dt)

        # Check zone transitions
        self._check_zone_exits()

        return True

    def _check_collision(self, tile_x: int, tile_y: int) -> bool:
        """Check if a tile position has collision."""
        zone = self.world.get_current_zone()
        if not zone:
            return True
        return not zone.is_walkable(tile_x, tile_y)

    def _update_camera(self):
        """Update camera to follow player."""
        # Target camera position (centered on player)
        player_pos = self.player.get_pixel_position()
        target_x = player_pos[0] - SCREEN_WIDTH // 2
        target_y = player_pos[1] - SCREEN_HEIGHT // 2

        # Smooth camera follow
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1

        # Clamp camera to zone bounds
        max_x = ZONE_WIDTH * TILE_SIZE - SCREEN_WIDTH
        max_y = ZONE_HEIGHT * TILE_SIZE - SCREEN_HEIGHT
        self.camera_x = max(0, min(max_x, self.camera_x))
        self.camera_y = max(0, min(max_y, self.camera_y))

    def _handle_interactions(self, keys, dt: float):
        """Handle player interactions with the world."""
        # Check for interact key press
        if self.player.is_interact_pressed(keys):
            if self.player.try_interact():
                self._try_interact()

        # Check for ability key press
        ability_idx = self.player.is_ability_pressed(keys)
        if ability_idx is not None and self._dragon:
            self._try_use_ability(ability_idx)

        # Update gathering progress
        if self._gathering:
            self._gather_progress += dt
            if self._gather_progress >= 1.0:
                self._complete_gathering()

    def _try_interact(self):
        """Try to interact with something at player position."""
        tx, ty = self.player.get_facing_tile()
        zone_id = self.world.get_current_zone_id()

        # Check for resource at position
        sp = self.resources.get_spawn_at_position(zone_id, tx, ty)
        if sp:
            # Check if can gather
            dragon_abilities = self._dragon.get_available_abilities() if self._dragon else []
            if sp.can_gather(dragon_abilities):
                self._start_gathering(sp)
            elif sp.requires_ability:
                self._show_interaction_text(f"Requires: {sp.requires_ability.replace('_', ' ').title()}")
            else:
                self._show_interaction_text("Nothing to gather here")
            return

        # Check for zone exit
        self._check_zone_transition_at(tx, ty)

    def _start_gathering(self, spawn_point):
        """Start gathering from a spawn point."""
        self._gathering = True
        self._gather_progress = 0.0
        self._gather_target = spawn_point
        self._show_interaction_text(f"Gathering {spawn_point.name}...")

    def _complete_gathering(self):
        """Complete the gathering action."""
        self._gathering = False

        if self._gather_target:
            dragon_abilities = self._dragon.get_available_abilities() if self._dragon else []
            item = self.resources.gather(self._gather_target.id, dragon_abilities)

            if item:
                self.hud.add_notification(
                    f"Gathered {item.name} (★{'★' * (self._gather_target.current_quality - 1)})",
                    NOTIFICATION_SUCCESS, 3.0
                )
            else:
                self.hud.add_notification("Inventory full!", NOTIFICATION_WARNING, 3.0)

        self._gather_target = None

    def _try_use_ability(self, ability_idx: int):
        """Try to use a dragon ability."""
        if not self._dragon:
            return

        abilities = self._dragon.get_available_abilities()
        if ability_idx >= len(abilities):
            self._show_interaction_text("Ability not unlocked")
            return

        ability_name = abilities[ability_idx]
        if self._dragon.use_ability(ability_name):
            self._show_interaction_text(f"Used {ability_name.replace('_', ' ').title()}!")
            self._trigger_ability_effect(ability_name)
        else:
            self._show_interaction_text("Not enough stamina!")

    def _trigger_ability_effect(self, ability_name: str):
        """Trigger visual effect for ability."""
        player_pos = self.player.get_pixel_position()
        self._ability_effects.append({
            'type': ability_name,
            'x': player_pos[0],
            'y': player_pos[1],
            'timer': 1.0,
            'progress': 0.0,
        })

    def _update_ability_effects(self, dt: float):
        """Update ability visual effects."""
        expired = []
        for effect in self._ability_effects:
            effect['progress'] += dt / effect['timer']
            if effect['progress'] >= 1.0:
                expired.append(effect)

        for effect in expired:
            self._ability_effects.remove(effect)

    def _pet_dragon(self):
        """Pet the dragon."""
        if not self._dragon:
            return

        if self._dragon.pet():
            self.hud.add_notification("You pet the dragon! ♥", NOTIFICATION_SUCCESS, 2.0)
        else:
            self.hud.add_notification("Can't pet an egg!", NOTIFICATION_INFO, 2.0)

    def _check_zone_exits(self):
        """Check if player is near zone exit."""
        tx, ty = self.player.get_tile_position()

        # Check if at edge of zone
        zone = self.world.get_current_zone()
        if not zone:
            return

        # Near left edge
        if tx <= 1:
            self._show_zone_exit_prompt('west')
        # Near right edge
        elif tx >= ZONE_WIDTH - 2:
            self._show_zone_exit_prompt('east')
        # Near top edge
        elif ty <= 1:
            self._show_zone_exit_prompt('north')
        # Near bottom edge
        elif ty >= ZONE_HEIGHT - 2:
            self._show_zone_exit_prompt('south')

    def _show_zone_exit_prompt(self, direction: str):
        """Show zone exit prompt."""
        connections = self.world.get_connected_zones()
        if not connections:
            return

        # For simplicity, use first connection
        target_zone = connections[0]
        zone = self.world.get_zone(target_zone)
        if zone:
            self._interaction_text = f"Press E to go to {zone.name}"
            self._interaction_timer = 0.5

    def _check_zone_transition_at(self, tx: int, ty: int):
        """Check for zone transition at position."""
        # Check if at zone edge
        if tx <= 0 or tx >= ZONE_WIDTH - 1 or ty <= 0 or ty >= ZONE_HEIGHT - 1:
            connections = self.world.get_connected_zones()
            if connections:
                target_zone = connections[0]
                dragon_stage = self._dragon.get_stage() if self._dragon else DRAGON_STAGE_EGG

                if self.world.can_enter_zone(target_zone, dragon_stage):
                    self._start_zone_transition(target_zone)
                else:
                    zone = self.world.get_zone(target_zone)
                    req = zone.unlock_requirement if zone else "Unknown"
                    self._show_interaction_text(f"Requires dragon stage: {req}")

    def _start_zone_transition(self, zone_id: str):
        """Start transition to another zone."""
        self._transitioning = True
        self._transition_target = zone_id

        def on_fade_complete():
            self._complete_zone_transition()

        self.start_fade_out(on_fade_complete)

    def _complete_zone_transition(self):
        """Complete the zone transition."""
        if self._transition_target:
            dragon_stage = self._dragon.get_stage() if self._dragon else None
            self.world.set_zone(self._transition_target, dragon_stage)

            # Update renderer
            zone = self.world.get_current_zone()
            if zone:
                self.zone_renderer.set_zone(zone, self._transition_target)

            # Reset player position
            self.player.set_tile_position(ZONE_WIDTH // 2, ZONE_HEIGHT // 2)

            # Notification
            self.hud.add_notification(f"Entered {zone.name}", NOTIFICATION_INFO, 3.0)

        self._transitioning = False
        self._transition_target = None
        self.start_fade_in()

    def _show_interaction_text(self, text: str):
        """Show interaction text."""
        self._interaction_text = text
        self._interaction_timer = 2.0

    def _update_hud(self):
        """Update HUD data."""
        # Player info
        gold = self.inventory.get_gold()
        zone = self.world.get_current_zone()
        location = zone.name if zone else "Unknown"
        self.hud.set_player_info(gold, location)

        # Time info
        time_str = self.time_mgr.get_time_string()
        day = self.time_mgr.get_day()
        season = self.time_mgr.get_season()
        weather = self.world.get_weather()
        self.hud.set_time_info(time_str, day, season, weather)

        # Dragon stats
        if self._dragon:
            stats = self._dragon.get_stat_percentages()
            self.hud.set_dragon_stats(
                stats['hunger'] * 100,
                stats['stamina'] * 100,
                stats['happiness'] * 100,
                self._dragon.name,
                self._dragon.get_mood()
            )

    def draw(self, screen: pygame.Surface):
        """Draw exploration mode."""
        # Draw zone background
        self.zone_renderer.draw(screen, int(self.camera_x), int(self.camera_y))

        # Draw resource indicators
        zone_id = self.world.get_current_zone_id()
        dragon_abilities = self._dragon.get_available_abilities() if self._dragon else []
        indicators = self.resources.get_zone_indicators(zone_id, dragon_abilities)
        self.zone_renderer.draw_resource_indicators(screen, indicators,
                                                     int(self.camera_x), int(self.camera_y))

        # Draw dragon companion
        self.dragon_companion.draw(screen, int(self.camera_x), int(self.camera_y))

        # Draw player
        self.player.draw(screen, int(self.camera_x), int(self.camera_y))

        # Draw ability effects
        self._draw_ability_effects(screen)

        # Draw gathering progress
        if self._gathering:
            self._draw_gather_progress(screen)

        # Draw interaction text
        if self._interaction_text:
            self._draw_interaction_text(screen)

        # Draw HUD
        self.hud.draw(screen)

        # Draw controls hint
        self._draw_controls_hint(screen)

        # Draw fade overlay
        self.draw_fade_overlay(screen)

    def _draw_ability_effects(self, screen: pygame.Surface):
        """Draw ability visual effects."""
        for effect in self._ability_effects:
            x = int(effect['x'] - self.camera_x)
            y = int(effect['y'] - self.camera_y)
            progress = effect['progress']

            if effect['type'] == 'burrow_fetch':
                # Expanding circle with dirt particles
                radius = int(30 * progress)
                alpha = int(255 * (1 - progress))
                color = (140, 100, 70, alpha)
                surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, (radius, radius), radius, 3)
                screen.blit(surf, (x - radius, y - radius))

            elif effect['type'] == 'sniff_track':
                # Pulsing wave
                radius = int(50 * progress)
                alpha = int(200 * (1 - progress))
                color = (100, 180, 255, alpha)
                surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, (radius, radius), radius, 2)
                screen.blit(surf, (x - radius, y - radius))

            elif effect['type'] == 'rock_smash':
                # Expanding cracks
                radius = int(40 * progress)
                alpha = int(255 * (1 - progress))
                for angle in [0, 60, 120, 180, 240, 300]:
                    rad = math.radians(angle)
                    end_x = x + int(math.cos(rad) * radius)
                    end_y = y + int(math.sin(rad) * radius)
                    pygame.draw.line(screen, (140, 140, 140, alpha), (x, y), (end_x, end_y), 2)

    def _draw_gather_progress(self, screen: pygame.Surface):
        """Draw gathering progress bar."""
        bar_width = 60
        bar_height = 8
        x = SCREEN_WIDTH // 2 - bar_width // 2
        y = SCREEN_HEIGHT // 2 + 40

        # Background
        pygame.draw.rect(screen, UI_BG, (x - 2, y - 2, bar_width + 4, bar_height + 4), border_radius=4)

        # Progress fill
        fill_width = int(bar_width * self._gather_progress)
        pygame.draw.rect(screen, (100, 200, 100), (x, y, fill_width, bar_height), border_radius=2)

        # Border
        pygame.draw.rect(screen, UI_PANEL, (x - 2, y - 2, bar_width + 4, bar_height + 4), 1, border_radius=4)

    def _draw_interaction_text(self, screen: pygame.Surface):
        """Draw interaction text prompt."""
        text_surface = self.prompt_font.render(self._interaction_text, True, CAFE_CREAM)
        text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 100)

        # Background
        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (30, 28, 40, 200), bg_surface.get_rect(), border_radius=6)
        screen.blit(bg_surface, bg_rect)

        screen.blit(text_surface, text_rect)

    def _draw_controls_hint(self, screen: pygame.Surface):
        """Draw controls hint at bottom."""
        hints = [
            "WASD: Move",
            "E/Space: Interact",
            "1-3: Abilities",
            "P: Pet Dragon",
            "C: Open Cafe",
        ]

        hint_text = "  |  ".join(hints)
        text_surface = self.info_font.render(hint_text, True, UI_TEXT_DIM)
        text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 25)
        screen.blit(text_surface, text_rect)
