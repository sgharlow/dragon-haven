"""
Cafe Mode State for Dragon Haven Cafe.
The main cafe operations screen where players manage service.
"""

import pygame
from typing import Optional, Dict, List, Any
from states.base_state import BaseScreen
from ui.hud import HUD
from ui.table import CafeFloor, CustomerSprite
from ui.order_bubble import OrderBubble
from ui.cooking_minigame import CookingMinigame
from systems.cafe import get_cafe_manager, ServiceStats
from systems.time_system import get_time_manager
from systems.economy import get_economy
from entities.staff import get_staff_manager, Staff
from entities.customer import get_customer_manager, Customer
from sound_manager import get_sound_manager
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    CAFE_STATE_CLOSED, CAFE_STATE_PREP, CAFE_STATE_SERVICE, CAFE_STATE_CLEANUP,
    CAFE_WARM, CAFE_CREAM, CAFE_WOOD,
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM, WHITE,
    HUD_MODE_CAFE,
    CUSTOMER_STATE_SEATED, CUSTOMER_STATE_WAITING_FOOD, CUSTOMER_STATE_EATING,
    REAL_SECONDS_PER_GAME_HOUR,
    RECIPES, DEFAULT_UNLOCKED_RECIPES,
)


class CafeModeState(BaseScreen):
    """
    Main cafe operations state.

    Manages:
    - Kitchen area (left side) for cooking
    - Serving area (right side) with tables and customers
    - Staff management
    - Service flow
    """

    def __init__(self, game):
        """Initialize cafe mode state."""
        super().__init__(game)
        self.title = "Cafe Mode"

        # Managers
        self.cafe = get_cafe_manager()
        self.time = get_time_manager()
        self.economy = get_economy()
        self.staff_mgr = get_staff_manager()
        self.customer_mgr = get_customer_manager()
        self.sound = get_sound_manager()

        # UI Areas
        self.kitchen_area = pygame.Rect(0, 80, 400, SCREEN_HEIGHT - 80)
        self.serving_area = pygame.Rect(400, 80, SCREEN_WIDTH - 400, SCREEN_HEIGHT - 80)

        # Cafe floor (tables and customers)
        self.cafe_floor = CafeFloor(self.serving_area)

        # HUD
        self.hud = HUD()
        self.hud.set_mode(HUD_MODE_CAFE)

        # Cooking minigame
        self.cooking_minigame = CookingMinigame()
        self._cooking_active = False
        self._cooking_customer_id: Optional[str] = None

        # Selection state
        self._selected_customer: Optional[str] = None
        self._selected_staff: Optional[str] = None
        self._ready_dish: Optional[Dict[str, Any]] = None  # Cooked dish waiting to serve

        # Service state
        self._service_summary: Optional[ServiceStats] = None
        self._showing_summary = False

        # Menu management
        self._menu_open = False
        self._available_recipes = list(DEFAULT_UNLOCKED_RECIPES)

        # Staff sprites (simple positions)
        self._staff_positions = {
            'melody': {'x': 600, 'y': 500},  # Server in serving area
            'bruno': {'x': 200, 'y': 300},   # Chef in kitchen
            'sage': {'x': 500, 'y': 400},    # Busser
        }

        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

        # Buttons
        self._kitchen_buttons: List[Dict[str, Any]] = []
        self._create_kitchen_buttons()

    def _create_kitchen_buttons(self):
        """Create kitchen area buttons."""
        btn_y = 150
        btn_height = 40
        btn_spacing = 50

        self._kitchen_buttons = [
            {
                'rect': pygame.Rect(50, btn_y, 150, btn_height),
                'text': 'Cook',
                'action': 'cook',
                'enabled': True,
            },
            {
                'rect': pygame.Rect(220, btn_y, 150, btn_height),
                'text': 'Menu',
                'action': 'menu',
                'enabled': True,
            },
        ]

    def enter(self, previous_state=None):
        """Initialize when entering cafe mode."""
        super().enter(previous_state)

        # Initialize staff
        self.staff_mgr.initialize()

        # Reset customer manager for fresh service
        self.customer_mgr.clear_all()

        # Setup cafe floor with default layout
        self.cafe_floor = CafeFloor(self.serving_area)
        self.cafe_floor.create_default_layout()

        # Reset state
        self._cooking_active = False
        self._showing_summary = False
        self._ready_dish = None

        # Setup callbacks
        self.cafe.on_service_end(self._on_service_end)

    def exit(self):
        """Cleanup when leaving cafe mode."""
        super().exit()

    def _on_service_end(self, stats: ServiceStats):
        """Handle end of service."""
        self._service_summary = stats
        self._showing_summary = True

    # =========================================================================
    # EVENT HANDLING
    # =========================================================================

    def handle_event(self, event):
        """Handle input events."""
        if self._cooking_active:
            # Pass to cooking minigame
            result = self.cooking_minigame.handle_input(event)
            if result:
                self._on_cooking_complete(result)
            return

        if self._showing_summary:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self._showing_summary = False
                self.fade_to_state('main_menu')
            return

        if self._menu_open:
            self._handle_menu_event(event)
            return

        # HUD events
        if self.hud.handle_event(event):
            return

        if event.type == pygame.KEYDOWN:
            # Escape to open pause menu
            if event.key == pygame.K_ESCAPE:
                self.transition_to('pause_menu')
                return

            # I to open inventory
            if event.key == pygame.K_i:
                self.transition_to('inventory')
                return

            # R to open recipe book
            if event.key == pygame.K_r:
                self.transition_to('recipe_book')
                return

            # D to open dragon status
            if event.key == pygame.K_d:
                self.transition_to('dragon_status')
                return

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._handle_click(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            self.cafe_floor.handle_hover(event.pos)

    def _handle_click(self, pos):
        """Handle mouse click."""
        # Check kitchen buttons
        for btn in self._kitchen_buttons:
            if btn['rect'].collidepoint(pos) and btn['enabled']:
                self._handle_button_action(btn['action'])
                return

        # Check serving area
        if self.serving_area.collidepoint(pos):
            click_result = self.cafe_floor.handle_click(pos)

            if click_result['type'] == 'customer':
                self._on_customer_clicked(click_result['customer_id'])
            elif click_result['type'] == 'table':
                self._on_table_clicked(click_result['table_id'])

        # Check kitchen area for staff
        if self.kitchen_area.collidepoint(pos):
            self._check_staff_click(pos)

    def _handle_button_action(self, action: str):
        """Handle kitchen button action."""
        if action == 'cook':
            self._start_cooking()
        elif action == 'menu':
            self._menu_open = True

        self.sound.play('ui_click')

    def _handle_menu_event(self, event):
        """Handle menu popup events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._menu_open = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Simple close on click outside
            menu_rect = pygame.Rect(200, 150, 400, 400)
            if not menu_rect.collidepoint(event.pos):
                self._menu_open = False

    def _on_customer_clicked(self, customer_id: str):
        """Handle customer click."""
        customer = self.customer_mgr.get_customer(customer_id)
        if not customer:
            return

        # If we have a ready dish, serve it
        if self._ready_dish:
            self._serve_dish_to_customer(customer)
            return

        # Take order if customer is seated
        if customer.state == CUSTOMER_STATE_SEATED:
            order = customer.take_order(self.cafe.get_menu())
            sprite = self.cafe_floor.get_customer_sprite(customer_id)
            if sprite and order:
                sprite.set_order(order.category, order.recipe_id)
                sprite.set_state(CUSTOMER_STATE_WAITING_FOOD)
            self.sound.play('ui_confirm')

        self._selected_customer = customer_id

    def _on_table_clicked(self, table_id: int):
        """Handle table click."""
        # Could be used for seating new customers
        pass

    def _check_staff_click(self, pos):
        """Check if a staff member was clicked."""
        for staff_id, staff_pos in self._staff_positions.items():
            if staff_id == 'melody':
                continue  # Melody is in serving area

            dist_sq = (pos[0] - staff_pos['x']) ** 2 + (pos[1] - staff_pos['y']) ** 2
            if dist_sq < 30 ** 2:
                self._talk_to_staff(staff_id)
                return

    def _talk_to_staff(self, staff_id: str):
        """Talk to a staff member."""
        staff = self.staff_mgr.get_staff(staff_id)
        if staff:
            result = staff.talk_to()
            if result['success']:
                self.hud.add_notification(result['message'], 'success')
                self.sound.play('ui_confirm')
            else:
                self.hud.add_notification(result['message'], 'warning')

    def _start_cooking(self):
        """Start the cooking minigame."""
        # Get a recipe from menu
        menu = self.cafe.get_menu()
        if not menu:
            menu = self._available_recipes

        if not menu:
            self.hud.add_notification("No recipes available!", 'warning')
            return

        recipe_id = menu[0]  # Use first recipe for simplicity
        recipe_data = RECIPES.get(recipe_id)
        if not recipe_data:
            return

        self.cooking_minigame.setup(
            recipe_id=recipe_id,
            difficulty=recipe_data.get('difficulty', 2),
            ingredient_quality=3  # Average quality
        )
        self.cooking_minigame.start()
        self._cooking_active = True
        self.sound.play('ui_confirm')

    def _on_cooking_complete(self, result):
        """Handle cooking minigame completion."""
        self._cooking_active = False

        if result.completed:
            self._ready_dish = {
                'recipe_id': result.recipe_id,
                'quality': result.quality,
            }
            self.hud.add_notification(
                f"Cooked {result.recipe_id}! Quality: {result.quality} stars",
                'success'
            )
            self.sound.play('ui_confirm')
        else:
            self.hud.add_notification("Cooking cancelled", 'warning')

    def _serve_dish_to_customer(self, customer: Customer):
        """Serve the ready dish to a customer."""
        if not self._ready_dish:
            return

        result = customer.serve_dish(
            self._ready_dish['recipe_id'],
            self._ready_dish['quality']
        )

        if result.get('success'):
            # Update sprite
            sprite = self.cafe_floor.get_customer_sprite(customer.id)
            if sprite:
                sprite.clear_order()
                sprite.set_state(CUSTOMER_STATE_EATING)
                sprite.set_mood(result['mood'])

            # Record sale
            recipe_data = RECIPES.get(self._ready_dish['recipe_id'], {})
            price = recipe_data.get('base_price', 50)
            self.cafe.record_sale(
                self._ready_dish['recipe_id'],
                price,
                satisfaction=result['satisfaction']
            )

            self.hud.add_notification(f"Served to {customer.name}!", 'success')
            self.sound.play('ui_confirm')

            self._ready_dish = None

    # =========================================================================
    # UPDATE
    # =========================================================================

    def update(self, dt):
        """Update cafe mode."""
        super().update(dt)

        if self._cooking_active:
            result = self.cooking_minigame.update(dt)
            if result:
                self._on_cooking_complete(result)
            return True

        if self._showing_summary:
            return True

        # Update time
        game_hours = dt / REAL_SECONDS_PER_GAME_HOUR

        # Update cafe state
        self.cafe.update(self.time.get_current_hour())

        # Update customers
        if self.cafe.is_open():
            # Spawn customers
            if self.customer_mgr.should_spawn(self.cafe.get_reputation(), game_hours):
                self._spawn_customer()

            # Update existing customers
            events = self.customer_mgr.update(game_hours)
            for event in events:
                self._handle_customer_event(event)

        # Update staff
        self.staff_mgr.decay_all_morale(game_hours)
        staff_events = self.staff_mgr.update(game_hours)
        for event in staff_events:
            if event.get('mistake'):
                self.hud.add_notification(event['mistake_message'], 'warning')

        # Update UI
        self.cafe_floor.update(dt)
        self.hud.update(dt)

        # Update HUD info
        self.hud.set_player_info(self.economy.get_gold(), "Cafe")
        self.hud.set_time_info(
            self.time.get_formatted_time(),
            self.time.get_current_day(),
            self.time.get_current_season(),
            'sunny'  # Placeholder
        )

        return True

    def _spawn_customer(self):
        """Spawn a new customer."""
        # Check for available table
        table = self.cafe_floor.get_available_table()
        if not table:
            return  # No seats

        # Create customer
        customer = self.customer_mgr.spawn_customer(self.cafe.get_reputation())

        # Seat at table
        table_id, seat_id = self.cafe_floor.seat_customer(
            customer.id, customer.name, table.table_id
        )

        if table_id >= 0:
            customer.seat_at_table(table_id, seat_id)
            sprite = self.cafe_floor.get_customer_sprite(customer.id)
            if sprite:
                sprite.set_patience(1.0)
                sprite.set_state(CUSTOMER_STATE_SEATED)

            self.hud.add_notification(f"{customer.name} arrived!", 'info')

    def _handle_customer_event(self, event: Dict[str, Any]):
        """Handle customer update events."""
        customer_id = event.get('customer_id')

        if event.get('patience_depleted'):
            # Customer left angry
            leave_result = event.get('leave_result', {})
            self.cafe.add_reputation(leave_result.get('reputation_change', 0))
            self.hud.add_notification(leave_result.get('feedback', 'Customer left!'), 'error')
            self.cafe_floor.remove_customer(customer_id)

        elif event.get('finished_eating'):
            # Customer finished and left happy
            leave_result = event.get('leave_result', {})
            tip = leave_result.get('tip', 0)
            if tip > 0:
                self.economy.add_gold(tip, 'tip', f"Tip from {event.get('customer_name')}")

            self.cafe.add_reputation(leave_result.get('reputation_change', 0))
            self.cafe.record_customer_served()
            self.hud.add_notification(leave_result.get('feedback', ''), 'success')
            self.cafe_floor.remove_customer(customer_id)

    # =========================================================================
    # DRAWING
    # =========================================================================

    def draw(self, screen):
        """Draw cafe mode."""
        # Background
        screen.fill(self.background_color)

        # Draw areas
        self._draw_kitchen(screen)
        self.cafe_floor.draw(screen)

        # Draw staff
        self._draw_staff(screen)

        # Draw top bar
        self._draw_top_bar(screen)

        # Draw HUD
        self.hud.draw(screen)

        # Draw cooking minigame overlay
        if self._cooking_active:
            self.cooking_minigame.draw(screen)

        # Draw menu popup
        if self._menu_open:
            self._draw_menu_popup(screen)

        # Draw service summary
        if self._showing_summary:
            self._draw_service_summary(screen)

        # Draw ready dish indicator
        if self._ready_dish:
            self._draw_ready_dish(screen)

        # Fade overlay
        self.draw_fade_overlay(screen)

    def _draw_top_bar(self, screen):
        """Draw the top status bar."""
        bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 80)
        pygame.draw.rect(screen, UI_PANEL, bar_rect)
        pygame.draw.line(screen, UI_BORDER, (0, 80), (SCREEN_WIDTH, 80), 2)

        # Title
        title_surface = self.title_font.render("Dragon Haven Cafe", True, CAFE_CREAM)
        screen.blit(title_surface, (20, 20))

        # Cafe state
        state_colors = {
            CAFE_STATE_CLOSED: (150, 100, 100),
            CAFE_STATE_PREP: (180, 180, 100),
            CAFE_STATE_SERVICE: (100, 180, 100),
            CAFE_STATE_CLEANUP: (100, 150, 180),
        }
        state_text = self.cafe.get_state().replace('_', ' ').title()
        state_color = state_colors.get(self.cafe.get_state(), UI_TEXT)
        state_surface = self.text_font.render(f"Status: {state_text}", True, state_color)
        screen.blit(state_surface, (20, 50))

        # Today's stats
        stats = self.cafe.get_today_stats()
        stats_text = f"Served: {stats.customers_served}  Revenue: {stats.revenue}g  Tips: {stats.tips}g"
        stats_surface = self.small_font.render(stats_text, True, UI_TEXT_DIM)
        screen.blit(stats_surface, (SCREEN_WIDTH - stats_surface.get_width() - 20, 55))

        # Reputation
        rep = self.cafe.get_reputation()
        rep_name = self.cafe.get_reputation_level_name()
        rep_surface = self.text_font.render(f"Reputation: {rep} ({rep_name})", True, CAFE_WARM)
        screen.blit(rep_surface, (SCREEN_WIDTH - rep_surface.get_width() - 20, 25))

    def _draw_kitchen(self, screen):
        """Draw the kitchen area."""
        # Background
        pygame.draw.rect(screen, (50, 45, 60), self.kitchen_area)

        # Title
        title = self.text_font.render("Kitchen", True, CAFE_CREAM)
        screen.blit(title, (self.kitchen_area.x + 20, self.kitchen_area.y + 20))

        # Buttons
        for btn in self._kitchen_buttons:
            color = CAFE_WARM if btn['enabled'] else (100, 100, 100)
            pygame.draw.rect(screen, color, btn['rect'], border_radius=6)
            pygame.draw.rect(screen, UI_BORDER, btn['rect'], 2, border_radius=6)

            text_surface = self.text_font.render(btn['text'], True, WHITE)
            text_rect = text_surface.get_rect(center=btn['rect'].center)
            screen.blit(text_surface, text_rect)

        # Counter/workspace
        counter_rect = pygame.Rect(50, 220, 300, 150)
        pygame.draw.rect(screen, CAFE_WOOD, counter_rect, border_radius=4)
        pygame.draw.rect(screen, (80, 55, 35), counter_rect, 2, border_radius=4)

        # Instructions
        instructions = [
            "1. Click 'Cook' to prepare dishes",
            "2. Click customers to take orders",
            "3. Serve dishes to waiting customers",
            "4. Click staff to boost morale",
        ]
        y = 400
        for line in instructions:
            text = self.small_font.render(line, True, UI_TEXT_DIM)
            screen.blit(text, (60, y))
            y += 25

    def _draw_staff(self, screen):
        """Draw staff members."""
        for staff_id, pos in self._staff_positions.items():
            staff = self.staff_mgr.get_staff(staff_id)
            if not staff:
                continue

            x, y = pos['x'], pos['y']

            # Only draw Bruno in kitchen area
            if staff_id == 'bruno' and not self.kitchen_area.collidepoint(x, y):
                continue
            # Melody and Sage in serving area
            if staff_id in ['melody', 'sage'] and not self.serving_area.collidepoint(x, y):
                continue

            # Body
            mood_colors = {
                'happy': (100, 160, 140),
                'neutral': (140, 140, 160),
                'unhappy': (160, 100, 100),
            }
            color = mood_colors.get(staff.get_mood(), (140, 140, 140))
            pygame.draw.circle(screen, color, (x, y), 20)
            pygame.draw.circle(screen, UI_BORDER, (x, y), 20, 2)

            # Head
            pygame.draw.circle(screen, (220, 190, 160), (x, y - 25), 12)

            # Name
            name_surface = self.small_font.render(staff.name, True, UI_TEXT)
            name_rect = name_surface.get_rect(centerx=x, y=y + 25)
            screen.blit(name_surface, name_rect)

            # Morale bar
            bar_width = 40
            bar_rect = pygame.Rect(x - bar_width // 2, y + 40, bar_width, 6)
            pygame.draw.rect(screen, (40, 35, 50), bar_rect, border_radius=2)

            fill_width = int((staff.morale / 100) * (bar_width - 2))
            if fill_width > 0:
                fill_color = (80, 180, 100) if staff.morale > 50 else (220, 180, 60)
                fill_rect = pygame.Rect(x - bar_width // 2 + 1, y + 41, fill_width, 4)
                pygame.draw.rect(screen, fill_color, fill_rect, border_radius=1)

    def _draw_menu_popup(self, screen):
        """Draw menu management popup."""
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Menu panel
        panel_rect = pygame.Rect(200, 150, 400, 400)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Title
        title = self.title_font.render("Today's Menu", True, CAFE_CREAM)
        screen.blit(title, (panel_rect.x + 20, panel_rect.y + 20))

        # Menu items
        menu = self.cafe.get_menu()
        y = panel_rect.y + 70
        for recipe_id in menu:
            recipe = RECIPES.get(recipe_id, {})
            name = recipe.get('name', recipe_id)
            price = recipe.get('base_price', 0)

            text = f"- {name} ({price}g)"
            text_surface = self.text_font.render(text, True, UI_TEXT)
            screen.blit(text_surface, (panel_rect.x + 30, y))
            y += 30

        if not menu:
            text = "No items on menu!"
            text_surface = self.text_font.render(text, True, UI_TEXT_DIM)
            screen.blit(text_surface, (panel_rect.x + 30, y))

        # Close hint
        hint = self.small_font.render("Press ESC or click outside to close", True, UI_TEXT_DIM)
        screen.blit(hint, (panel_rect.x + 20, panel_rect.y + panel_rect.height - 30))

    def _draw_service_summary(self, screen):
        """Draw end of service summary."""
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Summary panel
        panel_rect = pygame.Rect(300, 150, 400, 350)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=8)

        # Title
        title = self.title_font.render("Service Complete!", True, CAFE_CREAM)
        title_rect = title.get_rect(centerx=panel_rect.centerx, y=panel_rect.y + 20)
        screen.blit(title, title_rect)

        # Stats
        if self._service_summary:
            stats = self._service_summary
            lines = [
                f"Customers Served: {stats.customers_served}",
                f"Dishes Sold: {stats.dishes_sold}",
                f"Revenue: {stats.revenue}g",
                f"Tips: {stats.tips}g",
                f"Total: {stats.revenue + stats.tips}g",
                f"Avg Satisfaction: {stats.average_satisfaction:.1f}/5",
            ]

            y = panel_rect.y + 80
            for line in lines:
                text = self.text_font.render(line, True, UI_TEXT)
                screen.blit(text, (panel_rect.x + 40, y))
                y += 35

        # Continue prompt
        prompt = self.text_font.render("Click or press any key to continue", True, CAFE_WARM)
        prompt_rect = prompt.get_rect(centerx=panel_rect.centerx, y=panel_rect.y + panel_rect.height - 40)
        screen.blit(prompt, prompt_rect)

    def _draw_ready_dish(self, screen):
        """Draw indicator for ready dish."""
        if not self._ready_dish:
            return

        # Indicator in kitchen area
        recipe_id = self._ready_dish['recipe_id']
        recipe = RECIPES.get(recipe_id, {})
        name = recipe.get('name', recipe_id)
        quality = self._ready_dish['quality']

        indicator_rect = pygame.Rect(50, 380, 300, 40)
        pygame.draw.rect(screen, (80, 120, 80), indicator_rect, border_radius=6)
        pygame.draw.rect(screen, (60, 100, 60), indicator_rect, 2, border_radius=6)

        text = f"Ready: {name} ({quality} stars) - Click customer to serve"
        text_surface = self.small_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=indicator_rect.center)
        screen.blit(text_surface, text_rect)
