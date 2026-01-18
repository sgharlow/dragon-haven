"""
Table and Seating UI Components for Dragon Haven Cafe.
Visual representation of cafe tables and seated customers.
"""

import pygame
from typing import Optional, List, Tuple, Dict, Any
from dataclasses import dataclass, field
from constants import (
    UI_PANEL, UI_BORDER, UI_TEXT, UI_TEXT_DIM,
    CAFE_WOOD, CAFE_CREAM, CAFE_WARM,
    CUSTOMER_STATE_SEATED, CUSTOMER_STATE_WAITING_FOOD,
    CUSTOMER_STATE_EATING, CUSTOMER_STATE_LEAVING,
)
from ui.order_bubble import OrderBubble, PatienceMeter


@dataclass
class TableSeat:
    """A seat at a table."""
    seat_id: int
    x: int  # Position relative to table
    y: int
    customer_id: Optional[str] = None
    is_occupied: bool = False


class Table:
    """
    A cafe table with seats for customers.

    Usage:
        table = Table(1, 200, 300, capacity=2)
        table.seat_customer(customer_id, seat=0)
        table.draw(surface)
    """

    def __init__(self, table_id: int, x: int, y: int, capacity: int = 2):
        """
        Initialize a table.

        Args:
            table_id: Unique table identifier
            x, y: Center position of table
            capacity: Number of seats (1-4)
        """
        self.table_id = table_id
        self.x = x
        self.y = y
        self.capacity = min(4, max(1, capacity))

        # Table dimensions
        self.width = 50 + capacity * 10
        self.height = 35

        # Create seats around the table
        self.seats: List[TableSeat] = []
        self._create_seats()

        # Visual state
        self._hover = False
        self._selected = False

        # Rect for click detection
        self.rect = pygame.Rect(
            x - self.width // 2 - 20, y - 30,
            self.width + 40, self.height + 50
        )

    def _create_seats(self):
        """Create seats around the table."""
        if self.capacity == 1:
            # Single seat in front
            self.seats.append(TableSeat(0, 0, 25))
        elif self.capacity == 2:
            # Two seats on sides
            self.seats.append(TableSeat(0, -30, 0))
            self.seats.append(TableSeat(1, 30, 0))
        elif self.capacity == 3:
            # Three seats
            self.seats.append(TableSeat(0, -30, 0))
            self.seats.append(TableSeat(1, 30, 0))
            self.seats.append(TableSeat(2, 0, 25))
        else:
            # Four seats
            self.seats.append(TableSeat(0, -35, 0))
            self.seats.append(TableSeat(1, 35, 0))
            self.seats.append(TableSeat(2, -15, 25))
            self.seats.append(TableSeat(3, 15, 25))

    def seat_customer(self, customer_id: str, seat_index: int = -1) -> int:
        """
        Seat a customer at this table.

        Args:
            customer_id: Customer ID
            seat_index: Specific seat (-1 for first available)

        Returns:
            Seat index where customer was seated, or -1 if failed
        """
        if seat_index >= 0:
            # Specific seat
            if seat_index < len(self.seats) and not self.seats[seat_index].is_occupied:
                self.seats[seat_index].customer_id = customer_id
                self.seats[seat_index].is_occupied = True
                return seat_index
            return -1

        # First available seat
        for i, seat in enumerate(self.seats):
            if not seat.is_occupied:
                seat.customer_id = customer_id
                seat.is_occupied = True
                return i

        return -1  # No seats available

    def remove_customer(self, customer_id: str = None, seat_index: int = -1) -> bool:
        """
        Remove a customer from the table.

        Args:
            customer_id: Customer ID to remove (optional)
            seat_index: Seat index to clear (optional)

        Returns:
            True if customer was removed
        """
        if seat_index >= 0 and seat_index < len(self.seats):
            self.seats[seat_index].customer_id = None
            self.seats[seat_index].is_occupied = False
            return True

        if customer_id:
            for seat in self.seats:
                if seat.customer_id == customer_id:
                    seat.customer_id = None
                    seat.is_occupied = False
                    return True

        return False

    def get_customer_seat(self, customer_id: str) -> int:
        """Get the seat index of a customer, or -1 if not found."""
        for i, seat in enumerate(self.seats):
            if seat.customer_id == customer_id:
                return i
        return -1

    def has_available_seat(self) -> bool:
        """Check if table has available seats."""
        return any(not seat.is_occupied for seat in self.seats)

    def get_customer_count(self) -> int:
        """Get number of customers at table."""
        return sum(1 for seat in self.seats if seat.is_occupied)

    def is_empty(self) -> bool:
        """Check if table is empty."""
        return all(not seat.is_occupied for seat in self.seats)

    def get_seat_position(self, seat_index: int) -> Tuple[int, int]:
        """Get the screen position of a seat."""
        if 0 <= seat_index < len(self.seats):
            seat = self.seats[seat_index]
            return (self.x + seat.x, self.y + seat.y)
        return (self.x, self.y)

    def contains_point(self, pos: Tuple[int, int]) -> bool:
        """Check if point is within table area."""
        return self.rect.collidepoint(pos)

    def set_hover(self, hover: bool):
        """Set hover state."""
        self._hover = hover

    def set_selected(self, selected: bool):
        """Set selected state."""
        self._selected = selected

    def draw(self, surface: pygame.Surface):
        """Draw the table."""
        # Draw table shadow
        shadow_rect = pygame.Rect(
            self.x - self.width // 2 + 3, self.y - 15 + 3,
            self.width, self.height
        )
        pygame.draw.rect(surface, (30, 25, 35), shadow_rect, border_radius=4)

        # Draw table top
        table_rect = pygame.Rect(
            self.x - self.width // 2, self.y - 15,
            self.width, self.height
        )

        if self._selected:
            table_color = (150, 120, 80)
        elif self._hover:
            table_color = (140, 100, 70)
        else:
            table_color = CAFE_WOOD

        pygame.draw.rect(surface, table_color, table_rect, border_radius=4)
        pygame.draw.rect(surface, (80, 55, 35), table_rect, 2, border_radius=4)

        # Draw table number
        font = pygame.font.Font(None, 18)
        num_surface = font.render(str(self.table_id), True, CAFE_CREAM)
        num_rect = num_surface.get_rect(center=table_rect.center)
        surface.blit(num_surface, num_rect)

        # Draw seats
        for seat in self.seats:
            self._draw_seat(surface, seat)

    def _draw_seat(self, surface: pygame.Surface, seat: TableSeat):
        """Draw a seat."""
        seat_x = self.x + seat.x
        seat_y = self.y + seat.y

        # Chair/seat
        if seat.is_occupied:
            # Don't draw seat under customer
            pass
        else:
            # Empty seat indicator
            pygame.draw.circle(surface, (70, 60, 80), (seat_x, seat_y), 12)
            pygame.draw.circle(surface, (50, 45, 60), (seat_x, seat_y), 12, 2)


class CustomerSprite:
    """
    Visual representation of a customer at a table.
    """

    def __init__(self, customer_id: str, name: str):
        """
        Initialize customer sprite.

        Args:
            customer_id: Customer ID
            name: Customer name
        """
        self.customer_id = customer_id
        self.name = name

        self.x = 0
        self.y = 0

        # Visual state
        self._state = CUSTOMER_STATE_SEATED
        self._mood = 'neutral'
        self._patience = 1.0

        # Order bubble
        self.order_bubble = OrderBubble(0, 0)
        self.patience_meter = PatienceMeter(0, 0)

        # Animation
        self._eating_timer = 0.0

        # Font
        self.font = pygame.font.Font(None, 16)

    def set_position(self, x: int, y: int):
        """Set sprite position."""
        self.x = x
        self.y = y
        self.order_bubble.set_position(x, y - 35)
        self.patience_meter.set_position(x, y - 45)

    def set_state(self, state: str):
        """Set customer state."""
        self._state = state

    def set_mood(self, mood: str):
        """Set customer mood."""
        self._mood = mood

    def set_patience(self, patience: float):
        """Set patience level."""
        self._patience = patience
        self.patience_meter.set_patience(patience)

    def set_order(self, category: str, recipe_id: str = None, recipe_name: str = None):
        """Set order to display."""
        self.order_bubble.set_order(category, recipe_id, recipe_name)

    def clear_order(self):
        """Clear order bubble."""
        self.order_bubble.clear()

    def update(self, dt: float):
        """Update animations."""
        self.order_bubble.update(dt)

        if self._state == CUSTOMER_STATE_EATING:
            self._eating_timer += dt
        else:
            self._eating_timer = 0

    def draw(self, surface: pygame.Surface):
        """Draw the customer sprite."""
        # Customer body (simple circle for now)
        body_color = self._get_mood_color()

        # Body
        pygame.draw.circle(surface, body_color, (self.x, self.y - 10), 15)
        pygame.draw.circle(surface, (50, 45, 60), (self.x, self.y - 10), 15, 2)

        # Head
        pygame.draw.circle(surface, (220, 190, 160), (self.x, self.y - 28), 10)
        pygame.draw.circle(surface, (180, 150, 120), (self.x, self.y - 28), 10, 1)

        # Face based on mood
        self._draw_face(surface, self.x, self.y - 28)

        # Eating animation
        if self._state == CUSTOMER_STATE_EATING:
            # Show eating indicator
            import math
            bob = math.sin(self._eating_timer * 5) * 2
            pygame.draw.circle(surface, CAFE_WARM, (self.x + 12, int(self.y - 15 + bob)), 5)

        # Draw patience meter if waiting
        if self._state in [CUSTOMER_STATE_SEATED, CUSTOMER_STATE_WAITING_FOOD]:
            self.patience_meter.draw(surface)

        # Draw order bubble
        self.order_bubble.draw(surface)

    def _get_mood_color(self) -> Tuple[int, int, int]:
        """Get body color based on mood."""
        if self._mood == 'happy':
            return (100, 160, 140)
        elif self._mood == 'neutral':
            return (140, 140, 160)
        else:  # unhappy/angry
            return (160, 100, 100)

    def _draw_face(self, surface: pygame.Surface, x: int, y: int):
        """Draw simple face based on mood."""
        # Eyes
        pygame.draw.circle(surface, (60, 50, 40), (x - 4, y - 2), 2)
        pygame.draw.circle(surface, (60, 50, 40), (x + 4, y - 2), 2)

        # Mouth based on mood
        if self._mood == 'happy':
            # Smile
            pygame.draw.arc(surface, (60, 50, 40),
                           pygame.Rect(x - 5, y, 10, 6), 3.14, 6.28, 2)
        elif self._mood == 'unhappy' or self._mood == 'angry':
            # Frown
            pygame.draw.arc(surface, (60, 50, 40),
                           pygame.Rect(x - 5, y + 3, 10, 6), 0, 3.14, 2)
        else:
            # Neutral
            pygame.draw.line(surface, (60, 50, 40), (x - 4, y + 4), (x + 4, y + 4), 2)


class CafeFloor:
    """
    Manager for all tables and customers in the cafe serving area.
    """

    def __init__(self, area_rect: pygame.Rect):
        """
        Initialize cafe floor.

        Args:
            area_rect: Rectangle defining the serving area
        """
        self.area = area_rect
        self.tables: Dict[int, Table] = {}
        self.customer_sprites: Dict[str, CustomerSprite] = {}

        self._selected_table: Optional[int] = None
        self._selected_customer: Optional[str] = None

    def add_table(self, table_id: int, x: int, y: int, capacity: int = 2) -> Table:
        """Add a table to the floor."""
        table = Table(table_id, x, y, capacity)
        self.tables[table_id] = table
        return table

    def create_default_layout(self):
        """Create a default table layout."""
        # Two-seater tables on left
        self.add_table(1, self.area.x + 80, self.area.y + 100, 2)
        self.add_table(2, self.area.x + 80, self.area.y + 220, 2)

        # Four-seater in center
        self.add_table(3, self.area.x + 200, self.area.y + 160, 4)

        # Two-seater tables on right
        self.add_table(4, self.area.x + 320, self.area.y + 100, 2)
        self.add_table(5, self.area.x + 320, self.area.y + 220, 2)

    def seat_customer(self, customer_id: str, name: str,
                      table_id: int = -1) -> Tuple[int, int]:
        """
        Seat a customer at a table.

        Args:
            customer_id: Customer ID
            name: Customer name
            table_id: Specific table (-1 for any available)

        Returns:
            (table_id, seat_id) or (-1, -1) if no seat available
        """
        # Find table
        if table_id >= 0:
            if table_id in self.tables and self.tables[table_id].has_available_seat():
                table = self.tables[table_id]
            else:
                return (-1, -1)
        else:
            # Find any table with space
            table = None
            for t in self.tables.values():
                if t.has_available_seat():
                    table = t
                    break
            if not table:
                return (-1, -1)

        # Seat customer
        seat_index = table.seat_customer(customer_id)
        if seat_index < 0:
            return (-1, -1)

        # Create sprite
        sprite = CustomerSprite(customer_id, name)
        seat_pos = table.get_seat_position(seat_index)
        sprite.set_position(seat_pos[0], seat_pos[1])
        self.customer_sprites[customer_id] = sprite

        return (table.table_id, seat_index)

    def remove_customer(self, customer_id: str):
        """Remove a customer from the floor."""
        # Find and remove from table
        for table in self.tables.values():
            if table.remove_customer(customer_id):
                break

        # Remove sprite
        if customer_id in self.customer_sprites:
            del self.customer_sprites[customer_id]

    def get_customer_sprite(self, customer_id: str) -> Optional[CustomerSprite]:
        """Get a customer sprite."""
        return self.customer_sprites.get(customer_id)

    def get_available_table(self) -> Optional[Table]:
        """Get first table with available seats."""
        for table in self.tables.values():
            if table.has_available_seat():
                return table
        return None

    def handle_click(self, pos: Tuple[int, int]) -> Dict[str, Any]:
        """
        Handle click on the floor.

        Returns:
            Dict with 'type' (table/customer/none) and relevant data
        """
        # Check customers first (they're on top)
        for cid, sprite in self.customer_sprites.items():
            # Simple hit test
            dist_sq = (pos[0] - sprite.x) ** 2 + (pos[1] - sprite.y) ** 2
            if dist_sq < 25 ** 2:  # 25 pixel radius
                self._selected_customer = cid
                return {'type': 'customer', 'customer_id': cid, 'name': sprite.name}

        # Check tables
        for table in self.tables.values():
            if table.contains_point(pos):
                self._selected_table = table.table_id
                return {'type': 'table', 'table_id': table.table_id, 'table': table}

        self._selected_table = None
        self._selected_customer = None
        return {'type': 'none'}

    def handle_hover(self, pos: Tuple[int, int]):
        """Handle mouse hover."""
        for table in self.tables.values():
            table.set_hover(table.contains_point(pos))

    def update(self, dt: float):
        """Update all sprites."""
        for sprite in self.customer_sprites.values():
            sprite.update(dt)

    def draw(self, surface: pygame.Surface):
        """Draw the cafe floor."""
        # Draw floor background
        pygame.draw.rect(surface, (60, 55, 70), self.area)

        # Draw floor pattern
        for i in range(0, self.area.width, 40):
            for j in range(0, self.area.height, 40):
                rect = pygame.Rect(self.area.x + i, self.area.y + j, 38, 38)
                color = (55, 50, 65) if (i + j) // 40 % 2 == 0 else (65, 60, 75)
                pygame.draw.rect(surface, color, rect)

        # Draw tables
        for table in self.tables.values():
            table.set_selected(table.table_id == self._selected_table)
            table.draw(surface)

        # Draw customer sprites
        for sprite in self.customer_sprites.values():
            sprite.draw(surface)
