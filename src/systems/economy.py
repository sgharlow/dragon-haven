"""
Economy System for Dragon Haven Cafe.
Manages gold, pricing, tips, and upgrades.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple

from constants import (
    STARTING_GOLD,
    QUALITY_PRICE_MULTIPLIERS,
    REPUTATION_PRICE_BONUS,
    TIP_BASE_PERCENT, TIP_SATISFACTION_BONUS, TIP_MAX_PERCENT,
    UPGRADE_CARRIED_SLOTS, UPGRADE_STORAGE_SLOTS, UPGRADE_FRIDGE_SLOTS,
    UPGRADES
)
from systems.inventory import get_inventory


@dataclass
class Transaction:
    """Record of a financial transaction."""
    amount: int
    transaction_type: str  # 'sale', 'tip', 'expense', 'upgrade'
    description: str
    day: int = 0
    timestamp: float = 0.0


class EconomyManager:
    """
    Manages the game's economy including gold, prices, tips, and upgrades.

    Usage:
        economy = get_economy()

        # Sell a dish
        price = economy.calculate_dish_price(base_price=50, quality=4, reputation=150)
        economy.add_gold(price, 'sale', 'Sold Berry Tart')

        # Purchase an upgrade
        if economy.purchase_upgrade('upgrade_carried'):
            print('Backpack expanded!')
    """

    def __init__(self):
        """Initialize the economy manager."""
        # Gold is stored in Inventory, but we track transactions
        self._transactions: List[Transaction] = []
        self._daily_income: int = 0
        self._daily_expenses: int = 0
        self._total_earned: int = 0
        self._total_spent: int = 0

        # Track upgrade purchases
        self._upgrade_counts: Dict[str, int] = {
            UPGRADE_CARRIED_SLOTS: 0,
            UPGRADE_STORAGE_SLOTS: 0,
            UPGRADE_FRIDGE_SLOTS: 0,
        }

        # Current day for transaction tracking
        self._current_day: int = 1

    # =========================================================================
    # GOLD MANAGEMENT (delegates to Inventory)
    # =========================================================================

    def get_gold(self) -> int:
        """Get current gold amount."""
        return get_inventory().gold

    def add_gold(self, amount: int, transaction_type: str = 'income',
                 description: str = '') -> int:
        """
        Add gold and record the transaction.

        Args:
            amount: Gold to add
            transaction_type: Type of transaction ('sale', 'tip', etc.)
            description: Description for transaction log

        Returns:
            New gold total
        """
        if amount <= 0:
            return self.get_gold()

        get_inventory().add_gold(amount)

        # Track transaction
        self._transactions.append(Transaction(
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            day=self._current_day
        ))
        self._daily_income += amount
        self._total_earned += amount

        return self.get_gold()

    def spend_gold(self, amount: int, transaction_type: str = 'expense',
                   description: str = '') -> bool:
        """
        Spend gold if available.

        Args:
            amount: Gold to spend
            transaction_type: Type of transaction ('upgrade', 'expense', etc.)
            description: Description for transaction log

        Returns:
            True if successful
        """
        if amount <= 0:
            return True

        if not get_inventory().spend_gold(amount):
            return False

        # Track transaction
        self._transactions.append(Transaction(
            amount=-amount,
            transaction_type=transaction_type,
            description=description,
            day=self._current_day
        ))
        self._daily_expenses += amount
        self._total_spent += amount

        return True

    def can_afford(self, amount: int) -> bool:
        """Check if player can afford an amount."""
        return get_inventory().can_afford(amount)

    # =========================================================================
    # PRICE CALCULATION
    # =========================================================================

    def calculate_dish_price(self, base_price: int, quality: int = 3,
                             reputation: int = 0) -> int:
        """
        Calculate the selling price for a dish.

        Args:
            base_price: Base recipe price
            quality: Dish quality (1-5 stars)
            reputation: Current reputation points

        Returns:
            Final selling price
        """
        # Quality multiplier
        quality = max(1, min(5, quality))
        quality_mult = QUALITY_PRICE_MULTIPLIERS.get(quality, 1.0)

        # Reputation bonus (per 100 reputation)
        rep_tiers = reputation // 100
        rep_bonus = 1.0 + (rep_tiers * REPUTATION_PRICE_BONUS)

        final_price = int(base_price * quality_mult * rep_bonus)
        return max(1, final_price)

    def calculate_ingredient_price(self, base_price: int, quality: float = 1.0) -> int:
        """
        Calculate price for selling an ingredient.

        Args:
            base_price: Base item price
            quality: Item quality multiplier (0.7-1.3)

        Returns:
            Selling price (70% of value)
        """
        return max(1, int(base_price * quality * 0.7))

    # =========================================================================
    # TIP CALCULATION
    # =========================================================================

    def calculate_tip(self, dish_price: int, satisfaction: int = 3) -> int:
        """
        Calculate tip based on customer satisfaction.

        Args:
            dish_price: Price of the dish
            satisfaction: Customer satisfaction (1-5)

        Returns:
            Tip amount
        """
        # Base tip percentage
        tip_percent = TIP_BASE_PERCENT

        # Satisfaction bonus (for satisfaction > 3)
        if satisfaction > 3:
            tip_percent += (satisfaction - 3) * TIP_SATISFACTION_BONUS

        # Cap at max tip
        tip_percent = min(tip_percent, TIP_MAX_PERCENT)

        # No tip for very unsatisfied customers
        if satisfaction <= 1:
            return 0

        return max(0, int(dish_price * tip_percent))

    # =========================================================================
    # UPGRADE SYSTEM
    # =========================================================================

    def get_upgrade_info(self, upgrade_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an upgrade."""
        if upgrade_id not in UPGRADES:
            return None

        upgrade = UPGRADES[upgrade_id].copy()
        upgrade['times_purchased'] = self._upgrade_counts.get(upgrade_id, 0)
        upgrade['can_purchase'] = self.is_upgrade_available(upgrade_id)
        upgrade['can_afford'] = self.can_afford(upgrade['cost'])
        return upgrade

    def get_all_upgrades(self) -> List[Dict[str, Any]]:
        """Get information about all upgrades."""
        return [self.get_upgrade_info(uid) for uid in UPGRADES.keys()]

    def get_upgrade_cost(self, upgrade_id: str) -> int:
        """Get the cost of an upgrade."""
        if upgrade_id not in UPGRADES:
            return 0
        return UPGRADES[upgrade_id]['cost']

    def is_upgrade_available(self, upgrade_id: str) -> bool:
        """Check if an upgrade can be purchased (not maxed out)."""
        if upgrade_id not in UPGRADES:
            return False

        max_purchases = UPGRADES[upgrade_id]['max_purchases']
        current = self._upgrade_counts.get(upgrade_id, 0)
        return current < max_purchases

    def purchase_upgrade(self, upgrade_id: str) -> bool:
        """
        Purchase an upgrade.

        Returns:
            True if successful
        """
        if not self.is_upgrade_available(upgrade_id):
            return False

        cost = self.get_upgrade_cost(upgrade_id)
        if not self.can_afford(cost):
            return False

        # Spend the gold
        upgrade_name = UPGRADES[upgrade_id]['name']
        if not self.spend_gold(cost, 'upgrade', f'Purchased {upgrade_name}'):
            return False

        # Apply the upgrade
        self._apply_upgrade(upgrade_id)
        self._upgrade_counts[upgrade_id] = self._upgrade_counts.get(upgrade_id, 0) + 1

        return True

    def _apply_upgrade(self, upgrade_id: str):
        """Apply an upgrade's effect."""
        inventory = get_inventory()
        amount = UPGRADES[upgrade_id]['amount']

        if upgrade_id == UPGRADE_CARRIED_SLOTS:
            # Expand carried inventory
            new_max = inventory.carried.max_slots + amount
            inventory.carried.max_slots = new_max
            # Add None slots
            while len(inventory.carried.slots) < new_max:
                inventory.carried.slots.append(None)

        elif upgrade_id == UPGRADE_STORAGE_SLOTS:
            # Expand storage
            new_max = inventory.storage.max_slots + amount
            inventory.storage.max_slots = new_max
            while len(inventory.storage.slots) < new_max:
                inventory.storage.slots.append(None)

        elif upgrade_id == UPGRADE_FRIDGE_SLOTS:
            # Expand fridge
            new_max = inventory.fridge.max_slots + amount
            inventory.fridge.max_slots = new_max
            while len(inventory.fridge.slots) < new_max:
                inventory.fridge.slots.append(None)

    # =========================================================================
    # DAILY TRACKING
    # =========================================================================

    def advance_day(self):
        """Called at the start of a new day."""
        self._current_day += 1
        self._daily_income = 0
        self._daily_expenses = 0

    def get_daily_summary(self) -> Dict[str, int]:
        """Get financial summary for the current day."""
        return {
            'day': self._current_day,
            'income': self._daily_income,
            'expenses': self._daily_expenses,
            'net': self._daily_income - self._daily_expenses,
            'current_gold': self.get_gold()
        }

    def get_total_summary(self) -> Dict[str, int]:
        """Get overall financial summary."""
        return {
            'total_earned': self._total_earned,
            'total_spent': self._total_spent,
            'current_gold': self.get_gold()
        }

    def get_recent_transactions(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent transactions."""
        recent = self._transactions[-count:] if count > 0 else self._transactions
        return [
            {
                'amount': t.amount,
                'type': t.transaction_type,
                'description': t.description,
                'day': t.day
            }
            for t in reversed(recent)
        ]

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'current_day': self._current_day,
            'daily_income': self._daily_income,
            'daily_expenses': self._daily_expenses,
            'total_earned': self._total_earned,
            'total_spent': self._total_spent,
            'upgrade_counts': self._upgrade_counts.copy(),
            'transactions': [
                {
                    'amount': t.amount,
                    'type': t.transaction_type,
                    'description': t.description,
                    'day': t.day
                }
                for t in self._transactions[-50:]  # Keep last 50 transactions
            ]
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._current_day = state.get('current_day', 1)
        self._daily_income = state.get('daily_income', 0)
        self._daily_expenses = state.get('daily_expenses', 0)
        self._total_earned = state.get('total_earned', 0)
        self._total_spent = state.get('total_spent', 0)
        self._upgrade_counts = state.get('upgrade_counts', {
            UPGRADE_CARRIED_SLOTS: 0,
            UPGRADE_STORAGE_SLOTS: 0,
            UPGRADE_FRIDGE_SLOTS: 0,
        })

        # Load transactions
        self._transactions = []
        for t_data in state.get('transactions', []):
            self._transactions.append(Transaction(
                amount=t_data['amount'],
                transaction_type=t_data['type'],
                description=t_data['description'],
                day=t_data['day']
            ))


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_economy_manager = None


def get_economy() -> EconomyManager:
    """Get the global economy manager instance."""
    global _economy_manager
    if _economy_manager is None:
        _economy_manager = EconomyManager()
    return _economy_manager


def reset_economy():
    """Reset the economy manager (for new game)."""
    global _economy_manager
    _economy_manager = EconomyManager()
