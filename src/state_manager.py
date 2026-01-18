"""
State Manager for Dragon Haven Cafe.
Handles registration and transitions between game states.
"""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class StateManager:
    """
    Manages game states and transitions between them.

    The StateManager maintains a registry of states and handles
    transitioning between them, including optional fade effects.
    """

    def __init__(self):
        """Initialize the state manager."""
        self.states = {}  # name -> state instance
        self.current_state = None
        self.current_state_name = None
        self.previous_state_name = None

        # Transition handling
        self.transitioning = False
        self.transition_target = None
        self.transition_fade_alpha = 0
        self.transition_fade_speed = 500
        self.transition_phase = None  # 'fade_out', 'switch', 'fade_in'

    def register(self, name, state):
        """
        Register a state.

        Args:
            name: Unique string identifier for the state
            state: BaseState instance
        """
        self.states[name] = state

    def get_state(self, name):
        """
        Get a state by name.

        Args:
            name: State name

        Returns:
            State instance or None
        """
        return self.states.get(name)

    def set_state(self, name, with_transition=False):
        """
        Switch to a state immediately or with fade transition.

        Args:
            name: Name of state to switch to
            with_transition: If True, fade out then in
        """
        if name not in self.states:
            print(f"Warning: State '{name}' not registered")
            return

        if with_transition:
            self.start_transition(name)
        else:
            self._switch_state(name)

    def start_transition(self, target_name):
        """
        Start a fade transition to another state.

        Args:
            target_name: Name of state to transition to
        """
        if target_name not in self.states:
            print(f"Warning: State '{target_name}' not registered")
            return

        self.transitioning = True
        self.transition_target = target_name
        self.transition_phase = 'fade_out'
        self.transition_fade_alpha = 0

    def _switch_state(self, name):
        """
        Immediately switch to a state.

        Args:
            name: Name of state to switch to
        """
        # Exit current state
        if self.current_state:
            self.current_state.exit()

        # Update tracking
        self.previous_state_name = self.current_state_name
        self.current_state_name = name
        self.current_state = self.states[name]

        # Enter new state
        self.current_state.enter(self.previous_state_name)

    def handle_event(self, event):
        """
        Pass event to current state.

        Args:
            event: pygame event
        """
        if self.current_state and not self.transitioning:
            self.current_state.handle_event(event)

    def update(self, dt):
        """
        Update current state and handle transitions.

        Args:
            dt: Delta time in seconds

        Returns:
            True to continue, False to quit
        """
        # Handle transition animation
        if self.transitioning:
            return self._update_transition(dt)

        # Update current state
        if self.current_state:
            result = self.current_state.update(dt)

            # Check if state wants to transition
            if self.current_state.next_state:
                next_state = self.current_state.next_state
                self.current_state.next_state = None
                self.set_state(next_state, with_transition=True)

            return result

        return True

    def _update_transition(self, dt):
        """
        Update transition animation.

        Args:
            dt: Delta time

        Returns:
            True to continue
        """
        if self.transition_phase == 'fade_out':
            self.transition_fade_alpha += self.transition_fade_speed * dt
            if self.transition_fade_alpha >= 255:
                self.transition_fade_alpha = 255
                self.transition_phase = 'switch'

        elif self.transition_phase == 'switch':
            self._switch_state(self.transition_target)
            self.transition_phase = 'fade_in'

        elif self.transition_phase == 'fade_in':
            self.transition_fade_alpha -= self.transition_fade_speed * dt
            if self.transition_fade_alpha <= 0:
                self.transition_fade_alpha = 0
                self.transitioning = False
                self.transition_phase = None
                self.transition_target = None

        return True

    def draw(self, screen):
        """
        Draw current state and transition overlay.

        Args:
            screen: pygame surface
        """
        # Draw current state
        if self.current_state:
            self.current_state.draw(screen)

        # Draw transition fade overlay
        if self.transitioning and self.transition_fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.transition_fade_alpha))
            screen.blit(fade_surface, (0, 0))
