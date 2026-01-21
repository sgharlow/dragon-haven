"""
Achievement System for Dragon Haven Cafe.
Tracks player accomplishments and provides rewards.
"""

from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from constants import (
    ACHIEVEMENTS, ACHIEVEMENT_COUNT,
    ACHIEVEMENT_CAT_DRAGON, ACHIEVEMENT_CAT_CAFE,
    ACHIEVEMENT_CAT_EXPLORATION, ACHIEVEMENT_CAT_STORY,
)


@dataclass
class AchievementNotification:
    """Notification for a newly unlocked achievement."""
    achievement_id: str
    name: str
    description: str
    reward: Dict[str, Any]
    timestamp: float = 0.0


class AchievementManager:
    """
    Manages achievements and tracks player progress.

    Usage:
        manager = get_achievement_manager()

        # Check achievement conditions
        manager.check_dragon_stage(dragon.stage)
        manager.check_reputation(cafe.reputation)

        # Get unlocked achievements
        unlocked = manager.get_unlocked_achievements()

        # Get pending notifications
        notifications = manager.get_pending_notifications()
    """

    def __init__(self):
        """Initialize achievement manager."""
        self._unlocked: Set[str] = set()
        self._pending_notifications: List[AchievementNotification] = []
        self._on_unlock_callbacks: List[Callable[[str, Dict], None]] = []

        # Progress tracking for cumulative achievements
        self._service_count: int = 0
        self._ingredients_gathered: int = 0
        self._rare_found: int = 0
        self._zones_visited: Set[str] = set()

    # =========================================================================
    # ACHIEVEMENT CHECKS
    # =========================================================================

    def check_dragon_stage(self, stage: str) -> Optional[str]:
        """
        Check dragon stage achievements.

        Args:
            stage: Current dragon stage

        Returns:
            Unlocked achievement ID or None
        """
        stage_achievements = {
            'hatchling': 'dragon_first_steps',
            'juvenile': 'dragon_growing_up',
            'adolescent': 'dragon_coming_of_age',
            'adult': 'dragon_full_grown',
        }

        if stage in stage_achievements:
            return self._try_unlock(stage_achievements[stage])
        return None

    def check_dragon_bond(self, bond: int) -> Optional[str]:
        """Check dragon bond achievements."""
        if bond >= 100:
            return self._try_unlock('dragon_best_friends')
        return None

    def check_reputation(self, reputation: int) -> List[str]:
        """
        Check reputation achievements.

        Returns:
            List of newly unlocked achievement IDs
        """
        unlocked = []

        rep_achievements = [
            (100, 'cafe_rising_star'),
            (200, 'cafe_expert_chef'),
            (350, 'cafe_master_chef'),
            (500, 'cafe_legendary'),
        ]

        for threshold, achievement_id in rep_achievements:
            if reputation >= threshold:
                result = self._try_unlock(achievement_id)
                if result:
                    unlocked.append(result)

        return unlocked

    def check_service_complete(self) -> Optional[str]:
        """Check service completion achievements."""
        self._service_count += 1

        if self._service_count >= 1:
            return self._try_unlock('cafe_grand_opening')
        return None

    def check_recipes_unlocked(self, count: int) -> Optional[str]:
        """Check recipe collection achievements."""
        if count >= 50:
            return self._try_unlock('cafe_recipe_collector')
        return None

    def check_zone_visited(self, zone_id: str) -> Optional[str]:
        """Check exploration achievements."""
        self._zones_visited.add(zone_id)

        if len(self._zones_visited) >= 7:
            return self._try_unlock('explore_all_zones')
        return None

    def check_ingredient_gathered(self, is_rare: bool = False) -> List[str]:
        """Check gathering achievements."""
        unlocked = []

        self._ingredients_gathered += 1
        if is_rare:
            self._rare_found += 1

        if self._ingredients_gathered >= 100:
            result = self._try_unlock('explore_gatherer')
            if result:
                unlocked.append(result)

        if self._rare_found >= 10:
            result = self._try_unlock('explore_treasure_hunter')
            if result:
                unlocked.append(result)

        return unlocked

    def check_abilities_unlocked(self, count: int) -> Optional[str]:
        """Check dragon ability achievements."""
        if count >= 10:
            return self._try_unlock('explore_dragon_master')
        return None

    def check_chapter_complete(self, chapter: int) -> Optional[str]:
        """Check story chapter achievements."""
        chapter_achievements = {
            1: 'story_chapter_1',
            2: 'story_chapter_2',
            3: 'story_chapter_3',
            4: 'story_chapter_4',
            5: 'story_chapter_5',
            6: 'story_chapter_6',
            7: 'story_chapter_7',
            8: 'story_chapter_8',
        }

        if chapter in chapter_achievements:
            return self._try_unlock(chapter_achievements[chapter])
        return None

    def check_max_affinity(self, has_max_affinity: bool) -> Optional[str]:
        """Check affinity achievements."""
        if has_max_affinity:
            return self._try_unlock('story_true_friend')
        return None

    # =========================================================================
    # CORE UNLOCK LOGIC
    # =========================================================================

    def _try_unlock(self, achievement_id: str) -> Optional[str]:
        """
        Try to unlock an achievement.

        Args:
            achievement_id: Achievement to unlock

        Returns:
            Achievement ID if newly unlocked, None if already unlocked
        """
        if achievement_id in self._unlocked:
            return None

        if achievement_id not in ACHIEVEMENTS:
            return None

        # Unlock the achievement
        self._unlocked.add(achievement_id)

        achievement = ACHIEVEMENTS[achievement_id]
        notification = AchievementNotification(
            achievement_id=achievement_id,
            name=achievement['name'],
            description=achievement['description'],
            reward=achievement.get('reward', {})
        )
        self._pending_notifications.append(notification)

        # Fire callbacks
        for callback in self._on_unlock_callbacks:
            callback(achievement_id, achievement)

        return achievement_id

    def force_unlock(self, achievement_id: str) -> bool:
        """
        Force unlock an achievement (for save loading).

        Args:
            achievement_id: Achievement to unlock

        Returns:
            True if valid achievement
        """
        if achievement_id in ACHIEVEMENTS:
            self._unlocked.add(achievement_id)
            return True
        return False

    # =========================================================================
    # QUERIES
    # =========================================================================

    def is_unlocked(self, achievement_id: str) -> bool:
        """Check if an achievement is unlocked."""
        return achievement_id in self._unlocked

    def get_unlocked_achievements(self) -> List[str]:
        """Get list of unlocked achievement IDs."""
        return list(self._unlocked)

    def get_unlocked_count(self) -> int:
        """Get count of unlocked achievements."""
        return len(self._unlocked)

    def get_total_count(self) -> int:
        """Get total achievement count."""
        return ACHIEVEMENT_COUNT

    def get_progress_percent(self) -> float:
        """Get achievement completion percentage."""
        if ACHIEVEMENT_COUNT == 0:
            return 100.0
        return (len(self._unlocked) / ACHIEVEMENT_COUNT) * 100

    def get_achievements_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all achievements in a category with unlock status.

        Args:
            category: Category name

        Returns:
            List of achievement dicts with 'unlocked' field
        """
        results = []
        for aid, data in ACHIEVEMENTS.items():
            if data['category'] == category:
                results.append({
                    'id': aid,
                    'name': data['name'],
                    'description': data['description'],
                    'reward': data.get('reward', {}),
                    'unlocked': aid in self._unlocked
                })
        return results

    def get_all_achievements(self) -> List[Dict[str, Any]]:
        """Get all achievements with unlock status."""
        results = []
        for aid, data in ACHIEVEMENTS.items():
            results.append({
                'id': aid,
                'name': data['name'],
                'description': data['description'],
                'category': data['category'],
                'reward': data.get('reward', {}),
                'unlocked': aid in self._unlocked
            })
        return results

    # =========================================================================
    # NOTIFICATIONS
    # =========================================================================

    def get_pending_notifications(self) -> List[AchievementNotification]:
        """Get pending achievement notifications (clears the list)."""
        notifications = self._pending_notifications.copy()
        self._pending_notifications.clear()
        return notifications

    def has_pending_notifications(self) -> bool:
        """Check if there are pending notifications."""
        return len(self._pending_notifications) > 0

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def on_unlock(self, callback: Callable[[str, Dict], None]):
        """Register callback for achievement unlocks."""
        self._on_unlock_callbacks.append(callback)

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_save_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'unlocked': list(self._unlocked),
            'service_count': self._service_count,
            'ingredients_gathered': self._ingredients_gathered,
            'rare_found': self._rare_found,
            'zones_visited': list(self._zones_visited),
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._unlocked = set(state.get('unlocked', []))
        self._service_count = state.get('service_count', 0)
        self._ingredients_gathered = state.get('ingredients_gathered', 0)
        self._rare_found = state.get('rare_found', 0)
        self._zones_visited = set(state.get('zones_visited', []))
        self._pending_notifications.clear()

    def reset(self):
        """Reset all achievement progress."""
        self._unlocked.clear()
        self._pending_notifications.clear()
        self._service_count = 0
        self._ingredients_gathered = 0
        self._rare_found = 0
        self._zones_visited.clear()


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_achievement_manager: Optional[AchievementManager] = None


def get_achievement_manager() -> AchievementManager:
    """Get the global achievement manager instance."""
    global _achievement_manager
    if _achievement_manager is None:
        _achievement_manager = AchievementManager()
    return _achievement_manager


def reset_achievement_manager():
    """Reset the achievement manager (for new game)."""
    global _achievement_manager
    _achievement_manager = AchievementManager()
