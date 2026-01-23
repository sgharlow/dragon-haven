"""
Inventory System for Dragon Haven Cafe.
Manages items, storage, spoilage, and the recipe book.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from constants import (
    ITEM_CATEGORIES, ITEM_VEGETABLE, ITEM_FRUIT, ITEM_SPECIAL,
    INVENTORY_CARRIED_SLOTS, INVENTORY_STORAGE_SLOTS, INVENTORY_FRIDGE_SLOTS,
    ITEM_DEFAULT_STACK_SIZE, ITEM_DEFAULT_SPOIL_DAYS,
    STARTING_GOLD
)


@dataclass
class Item:
    """
    Represents an item/ingredient in the game.

    Items can be stacked, have quality levels, and may spoil over time.
    """
    id: str                          # Unique identifier (e.g., 'tomato', 'sugar')
    name: str                        # Display name
    category: str                    # One of ITEM_CATEGORIES
    quality: float = 1.0             # 0.5 (low) to 1.5 (high)
    stack_size: int = ITEM_DEFAULT_STACK_SIZE
    spoil_days: int = ITEM_DEFAULT_SPOIL_DAYS  # 0 = never spoils
    description: str = ""
    base_price: int = 10             # Base sell/buy price
    color_influence: Tuple[float, float, float] = (0.5, 0.5, 0.5)  # For dragon feeding

    def get_sell_price(self) -> int:
        """Get the selling price based on quality."""
        return int(self.base_price * self.quality * 0.7)

    def get_buy_price(self) -> int:
        """Get the buying price."""
        return int(self.base_price * 1.2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'quality': self.quality,
            'stack_size': self.stack_size,
            'spoil_days': self.spoil_days,
            'description': self.description,
            'base_price': self.base_price,
            'color_influence': self.color_influence
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        return cls(
            id=data['id'],
            name=data['name'],
            category=data.get('category', ITEM_VEGETABLE),
            quality=data.get('quality', 1.0),
            stack_size=data.get('stack_size', ITEM_DEFAULT_STACK_SIZE),
            spoil_days=data.get('spoil_days', ITEM_DEFAULT_SPOIL_DAYS),
            description=data.get('description', ''),
            base_price=data.get('base_price', 10),
            color_influence=tuple(data.get('color_influence', (0.5, 0.5, 0.5)))
        )


@dataclass
class ItemStack:
    """
    A stack of identical items in an inventory slot.
    """
    item: Item
    quantity: int
    days_until_spoil: int = -1  # -1 = not started, 0 = spoiled

    def __post_init__(self):
        if self.days_until_spoil == -1 and self.item.spoil_days > 0:
            self.days_until_spoil = self.item.spoil_days

    def is_spoiled(self) -> bool:
        """Check if this stack has spoiled."""
        return self.item.spoil_days > 0 and self.days_until_spoil <= 0

    def advance_day(self, in_fridge: bool = False):
        """Advance spoilage by one day (unless in fridge)."""
        if self.item.spoil_days > 0 and not in_fridge:
            self.days_until_spoil -= 1

    def can_merge(self, other: 'ItemStack') -> bool:
        """Check if another stack can merge into this one."""
        return (self.item.id == other.item.id and
                self.quantity < self.item.stack_size)

    def merge(self, other: 'ItemStack') -> int:
        """
        Merge another stack into this one.

        Returns:
            Number of items that couldn't fit (overflow)
        """
        if not self.can_merge(other):
            return other.quantity

        space = self.item.stack_size - self.quantity
        to_add = min(space, other.quantity)
        self.quantity += to_add
        return other.quantity - to_add

    def split(self, amount: int) -> Optional['ItemStack']:
        """
        Split off a portion of this stack.

        Returns:
            New ItemStack with the split portion, or None if invalid
        """
        if amount <= 0 or amount >= self.quantity:
            return None

        new_stack = ItemStack(
            item=self.item,
            quantity=amount,
            days_until_spoil=self.days_until_spoil
        )
        self.quantity -= amount
        return new_stack

    def to_dict(self) -> Dict[str, Any]:
        return {
            'item': self.item.to_dict(),
            'quantity': self.quantity,
            'days_until_spoil': self.days_until_spoil
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ItemStack':
        return cls(
            item=Item.from_dict(data['item']),
            quantity=data['quantity'],
            days_until_spoil=data.get('days_until_spoil', -1)
        )


class InventoryContainer:
    """
    A container for ItemStacks with limited slots.
    """

    def __init__(self, max_slots: int, prevents_spoilage: bool = False):
        """
        Initialize the container.

        Args:
            max_slots: Maximum number of item stacks
            prevents_spoilage: If True, items don't spoil in this container
        """
        self.max_slots = max_slots
        self.prevents_spoilage = prevents_spoilage
        self.slots: List[Optional[ItemStack]] = [None] * max_slots

    def add_item(self, item: Item, quantity: int = 1) -> int:
        """
        Add items to the container.

        Args:
            item: Item to add
            quantity: How many to add

        Returns:
            Number of items that couldn't fit (overflow)
        """
        remaining = quantity

        # First, try to merge with existing stacks
        for i, slot in enumerate(self.slots):
            if slot and slot.item.id == item.id and slot.quantity < item.stack_size:
                space = item.stack_size - slot.quantity
                to_add = min(space, remaining)
                slot.quantity += to_add
                remaining -= to_add
                if remaining == 0:
                    return 0

        # Then, fill empty slots
        for i, slot in enumerate(self.slots):
            if slot is None:
                to_add = min(item.stack_size, remaining)
                self.slots[i] = ItemStack(item=item, quantity=to_add)
                remaining -= to_add
                if remaining == 0:
                    return 0

        return remaining  # Overflow

    def remove_item(self, item_id: str, quantity: int = 1) -> int:
        """
        Remove items from the container.

        Args:
            item_id: ID of item to remove
            quantity: How many to remove

        Returns:
            Number actually removed
        """
        remaining = quantity
        removed = 0

        for i, slot in enumerate(self.slots):
            if slot and slot.item.id == item_id:
                to_remove = min(slot.quantity, remaining)
                slot.quantity -= to_remove
                remaining -= to_remove
                removed += to_remove

                if slot.quantity == 0:
                    self.slots[i] = None

                if remaining == 0:
                    break

        return removed

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if the container has at least the specified quantity."""
        return self.get_count(item_id) >= quantity

    def get_count(self, item_id: str) -> int:
        """Get total count of an item in the container."""
        total = 0
        for slot in self.slots:
            if slot and slot.item.id == item_id:
                total += slot.quantity
        return total

    def get_all_items(self) -> List[Tuple[str, int]]:
        """Get list of (item_id, quantity) for all items."""
        items = {}
        for slot in self.slots:
            if slot:
                items[slot.item.id] = items.get(slot.item.id, 0) + slot.quantity
        return list(items.items())

    def get_slot(self, index: int) -> Optional[ItemStack]:
        """Get the stack at a specific slot index."""
        if 0 <= index < self.max_slots:
            return self.slots[index]
        return None

    def get_used_slots(self) -> int:
        """Get number of used slots."""
        return sum(1 for slot in self.slots if slot is not None)

    def get_free_slots(self) -> int:
        """Get number of free slots."""
        return self.max_slots - self.get_used_slots()

    def is_full(self) -> bool:
        """Check if all slots are used."""
        return self.get_free_slots() == 0

    def advance_day(self):
        """Advance spoilage for all items (unless this prevents spoilage)."""
        if self.prevents_spoilage:
            return

        spoiled_items = []
        for i, slot in enumerate(self.slots):
            if slot:
                slot.advance_day()
                if slot.is_spoiled():
                    spoiled_items.append(i)

        # Remove spoiled items
        for i in spoiled_items:
            self.slots[i] = None

    def sort_by_category(self):
        """
        Sort items by category then by name (Phase 4 QoL).
        Compacts items and moves empty slots to the end.
        """
        # Extract non-empty slots
        items = [slot for slot in self.slots if slot is not None]

        # Sort by category, then by name
        category_order = {
            ITEM_VEGETABLE: 0,
            ITEM_FRUIT: 1,
            ITEM_SPECIAL: 2,
        }
        items.sort(key=lambda s: (
            category_order.get(s.item.category, 99),
            s.item.name
        ))

        # Rebuild slots with sorted items and trailing Nones
        self.slots = items + [None] * (self.max_slots - len(items))

    def to_dict(self) -> Dict[str, Any]:
        return {
            'max_slots': self.max_slots,
            'prevents_spoilage': self.prevents_spoilage,
            'slots': [slot.to_dict() if slot else None for slot in self.slots]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryContainer':
        container = cls(
            max_slots=data['max_slots'],
            prevents_spoilage=data.get('prevents_spoilage', False)
        )
        container.slots = [
            ItemStack.from_dict(slot) if slot else None
            for slot in data.get('slots', [])
        ]
        # Pad with None if needed
        while len(container.slots) < container.max_slots:
            container.slots.append(None)
        return container


class Inventory:
    """
    Main inventory manager handling all player storage.

    Includes:
    - Carried inventory (for exploration)
    - Cafe storage (general)
    - Fridge (prevents spoilage)
    - Gold tracking
    - Recipe book
    """

    def __init__(self):
        """Initialize the inventory system."""
        # Storage containers
        self.carried = InventoryContainer(INVENTORY_CARRIED_SLOTS)
        self.storage = InventoryContainer(INVENTORY_STORAGE_SLOTS)
        self.fridge = InventoryContainer(INVENTORY_FRIDGE_SLOTS, prevents_spoilage=True)

        # Currency
        self.gold = STARTING_GOLD

        # Recipe book
        self.unlocked_recipes: List[str] = []
        self.mastered_recipes: List[str] = []  # Recipes made multiple times

        # QoL Features (Phase 4)
        self.favorite_recipes: List[str] = []  # Pinned recipes for quick access
        self.auto_sort_enabled: bool = True  # Auto-sort on pickup

    # =========================================================================
    # ITEM MANAGEMENT
    # =========================================================================

    def add_item(self, item: Item, quantity: int = 1, to_carried: bool = True) -> int:
        """
        Add items to inventory.

        Args:
            item: Item to add
            quantity: How many to add
            to_carried: If True, add to carried; else add to storage

        Returns:
            Number of items that couldn't fit
        """
        if to_carried:
            return self.carried.add_item(item, quantity)
        else:
            return self.storage.add_item(item, quantity)

    def remove_item(self, item_id: str, quantity: int = 1, from_carried: bool = True) -> int:
        """
        Remove items from inventory.

        Returns:
            Number actually removed
        """
        if from_carried:
            return self.carried.remove_item(item_id, quantity)
        else:
            return self.storage.remove_item(item_id, quantity)

    def has_item(self, item_id: str, quantity: int = 1, check_all: bool = True) -> bool:
        """
        Check if player has enough of an item.

        Args:
            item_id: Item to check
            quantity: Required quantity
            check_all: If True, check all storage; else just carried
        """
        if check_all:
            total = (self.carried.get_count(item_id) +
                    self.storage.get_count(item_id) +
                    self.fridge.get_count(item_id))
            return total >= quantity
        else:
            return self.carried.has_item(item_id, quantity)

    def get_count(self, item_id: str, check_all: bool = True) -> int:
        """Get total count of an item across inventories."""
        if check_all:
            return (self.carried.get_count(item_id) +
                   self.storage.get_count(item_id) +
                   self.fridge.get_count(item_id))
        else:
            return self.carried.get_count(item_id)

    # =========================================================================
    # TRANSFER BETWEEN CONTAINERS
    # =========================================================================

    def transfer_to_storage(self, item_id: str, quantity: int = 1, to_fridge: bool = False) -> int:
        """
        Transfer items from carried to storage or fridge.

        Returns:
            Number actually transferred
        """
        # Check how many we have
        available = self.carried.get_count(item_id)
        to_transfer = min(available, quantity)

        if to_transfer == 0:
            return 0

        # Get the item info from a slot
        item = None
        for slot in self.carried.slots:
            if slot and slot.item.id == item_id:
                item = slot.item
                break

        if not item:
            return 0

        # Try to add to destination
        dest = self.fridge if to_fridge else self.storage
        overflow = dest.add_item(item, to_transfer)
        actually_transferred = to_transfer - overflow

        # Remove from carried
        if actually_transferred > 0:
            self.carried.remove_item(item_id, actually_transferred)

        return actually_transferred

    def transfer_from_storage(self, item_id: str, quantity: int = 1, from_fridge: bool = False) -> int:
        """
        Transfer items from storage or fridge to carried.

        Returns:
            Number actually transferred
        """
        source = self.fridge if from_fridge else self.storage
        available = source.get_count(item_id)
        to_transfer = min(available, quantity)

        if to_transfer == 0:
            return 0

        # Get the item info
        item = None
        for slot in source.slots:
            if slot and slot.item.id == item_id:
                item = slot.item
                break

        if not item:
            return 0

        # Try to add to carried
        overflow = self.carried.add_item(item, to_transfer)
        actually_transferred = to_transfer - overflow

        # Remove from source
        if actually_transferred > 0:
            source.remove_item(item_id, actually_transferred)

        return actually_transferred

    # =========================================================================
    # GOLD MANAGEMENT
    # =========================================================================

    def add_gold(self, amount: int):
        """Add gold."""
        self.gold += amount

    def spend_gold(self, amount: int) -> bool:
        """
        Spend gold if available.

        Returns:
            True if successful, False if not enough gold
        """
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def can_afford(self, amount: int) -> bool:
        """Check if player can afford an amount."""
        return self.gold >= amount

    # =========================================================================
    # RECIPE BOOK
    # =========================================================================

    def unlock_recipe(self, recipe_id: str) -> bool:
        """
        Unlock a new recipe.

        Returns:
            True if newly unlocked, False if already known
        """
        if recipe_id not in self.unlocked_recipes:
            self.unlocked_recipes.append(recipe_id)
            return True
        return False

    def has_recipe(self, recipe_id: str) -> bool:
        """Check if a recipe is unlocked."""
        return recipe_id in self.unlocked_recipes

    def master_recipe(self, recipe_id: str) -> bool:
        """
        Mark a recipe as mastered.

        Returns:
            True if newly mastered
        """
        if recipe_id not in self.mastered_recipes:
            self.mastered_recipes.append(recipe_id)
            return True
        return False

    def is_recipe_mastered(self, recipe_id: str) -> bool:
        """Check if a recipe is mastered."""
        return recipe_id in self.mastered_recipes

    # =========================================================================
    # QoL FEATURES (Phase 4)
    # =========================================================================

    def toggle_favorite_recipe(self, recipe_id: str) -> bool:
        """
        Toggle a recipe's favorite status.

        Args:
            recipe_id: Recipe to toggle

        Returns:
            True if recipe is now favorited, False if unfavorited
        """
        if recipe_id in self.favorite_recipes:
            self.favorite_recipes.remove(recipe_id)
            return False
        else:
            self.favorite_recipes.append(recipe_id)
            return True

    def is_recipe_favorite(self, recipe_id: str) -> bool:
        """Check if a recipe is favorited."""
        return recipe_id in self.favorite_recipes

    def get_favorite_recipes(self) -> List[str]:
        """Get list of favorited recipe IDs."""
        return self.favorite_recipes.copy()

    def sort_inventory(self, container_name: str = 'storage'):
        """
        Sort an inventory container by category then by name.

        Args:
            container_name: 'carried', 'storage', or 'fridge'
        """
        container = getattr(self, container_name, None)
        if container:
            container.sort_by_category()

    def sort_all_inventories(self):
        """Sort all inventory containers."""
        self.carried.sort_by_category()
        self.storage.sort_by_category()
        self.fridge.sort_by_category()

    def set_auto_sort(self, enabled: bool):
        """Enable or disable auto-sorting on item pickup."""
        self.auto_sort_enabled = enabled

    # =========================================================================
    # TIME UPDATES
    # =========================================================================

    def advance_day(self):
        """Called at the start of a new day to handle spoilage."""
        self.carried.advance_day()
        self.storage.advance_day()
        # Fridge doesn't spoil items

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get complete state for saving."""
        return {
            'carried': self.carried.to_dict(),
            'storage': self.storage.to_dict(),
            'fridge': self.fridge.to_dict(),
            'gold': self.gold,
            'unlocked_recipes': self.unlocked_recipes.copy(),
            'mastered_recipes': self.mastered_recipes.copy(),
            # QoL data (Phase 4)
            'favorite_recipes': self.favorite_recipes.copy(),
            'auto_sort_enabled': self.auto_sort_enabled,
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        if 'carried' in state:
            self.carried = InventoryContainer.from_dict(state['carried'])
        if 'storage' in state:
            self.storage = InventoryContainer.from_dict(state['storage'])
        if 'fridge' in state:
            self.fridge = InventoryContainer.from_dict(state['fridge'])

        self.gold = state.get('gold', STARTING_GOLD)
        self.unlocked_recipes = state.get('unlocked_recipes', [])
        self.mastered_recipes = state.get('mastered_recipes', [])
        # QoL data (Phase 4)
        self.favorite_recipes = state.get('favorite_recipes', [])
        self.auto_sort_enabled = state.get('auto_sort_enabled', True)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_inventory = None


def get_inventory() -> Inventory:
    """Get the global inventory instance."""
    global _inventory
    if _inventory is None:
        _inventory = Inventory()
    return _inventory


def reset_inventory():
    """Reset the inventory (for new game)."""
    global _inventory
    _inventory = Inventory()
