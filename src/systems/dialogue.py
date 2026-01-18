"""
Dialogue System for Dragon Haven Cafe.
Manages conversations, branching dialogue, and character interactions.
"""

import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DialogueChoice:
    """
    A choice option within a dialogue.

    Attributes:
        text: The choice text shown to player
        next_id: ID of the dialogue node to go to
        condition: Optional flag condition to show this choice
        set_flags: Flags to set when this choice is selected
    """
    text: str
    next_id: str
    condition: Optional[str] = None
    set_flags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'next_id': self.next_id,
            'condition': self.condition,
            'set_flags': self.set_flags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogueChoice':
        return cls(
            text=data['text'],
            next_id=data.get('next_id', ''),
            condition=data.get('condition'),
            set_flags=data.get('set_flags', []),
        )


@dataclass
class DialogueNode:
    """
    A single node in a dialogue tree.

    Attributes:
        id: Unique identifier for this node
        speaker: Name of the character speaking
        portrait: ID of the portrait to show
        text: The dialogue text
        choices: List of choices (if any)
        next_id: Next node ID (if no choices)
        set_flags: Flags to set when this node is shown
        trigger_event: Event to trigger when shown
    """
    id: str
    speaker: str
    portrait: str
    text: str
    choices: List[DialogueChoice] = field(default_factory=list)
    next_id: Optional[str] = None
    set_flags: List[str] = field(default_factory=list)
    trigger_event: Optional[str] = None

    def has_choices(self) -> bool:
        """Check if this node has choices."""
        return len(self.choices) > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'speaker': self.speaker,
            'portrait': self.portrait,
            'text': self.text,
            'choices': [c.to_dict() for c in self.choices],
            'next_id': self.next_id,
            'set_flags': self.set_flags,
            'trigger_event': self.trigger_event,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogueNode':
        return cls(
            id=data['id'],
            speaker=data.get('speaker', ''),
            portrait=data.get('portrait', ''),
            text=data.get('text', ''),
            choices=[DialogueChoice.from_dict(c) for c in data.get('choices', [])],
            next_id=data.get('next_id'),
            set_flags=data.get('set_flags', []),
            trigger_event=data.get('trigger_event'),
        )


@dataclass
class Dialogue:
    """
    A complete dialogue conversation.

    Attributes:
        id: Unique identifier for this dialogue
        name: Display name for the dialogue
        nodes: Dict of node ID to DialogueNode
        start_id: ID of the starting node
    """
    id: str
    name: str
    nodes: Dict[str, DialogueNode]
    start_id: str

    def get_node(self, node_id: str) -> Optional[DialogueNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_start_node(self) -> Optional[DialogueNode]:
        """Get the starting node."""
        return self.nodes.get(self.start_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'nodes': {k: v.to_dict() for k, v in self.nodes.items()},
            'start_id': self.start_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dialogue':
        nodes = {}
        for node_id, node_data in data.get('nodes', {}).items():
            node_data['id'] = node_id  # Ensure ID is set
            nodes[node_id] = DialogueNode.from_dict(node_data)
        return cls(
            id=data['id'],
            name=data.get('name', ''),
            nodes=nodes,
            start_id=data.get('start_id', 'start'),
        )


class DialogueManager:
    """
    Manages dialogue loading, playback, and state.

    Usage:
        manager = DialogueManager()
        manager.load_dialogue_file('data/dialogues/intro.json')
        manager.start_dialogue('intro')
        node = manager.get_current_node()
        manager.advance()  # or manager.select_choice(0)
    """

    def __init__(self):
        """Initialize the dialogue manager."""
        # Loaded dialogues
        self._dialogues: Dict[str, Dialogue] = {}

        # Current playback state
        self._current_dialogue: Optional[Dialogue] = None
        self._current_node: Optional[DialogueNode] = None
        self._is_active = False

        # Dialogue flags (persistent state)
        self._flags: Dict[str, bool] = {}

        # Event callbacks
        self._event_callbacks: Dict[str, Callable] = {}

        # Callbacks for dialogue events
        self._on_dialogue_start: Optional[Callable] = None
        self._on_dialogue_end: Optional[Callable] = None
        self._on_node_change: Optional[Callable] = None

    # =========================================================================
    # DIALOGUE LOADING
    # =========================================================================

    def load_dialogue(self, dialogue: Dialogue):
        """Load a dialogue into the manager."""
        self._dialogues[dialogue.id] = dialogue

    def load_dialogue_dict(self, data: Dict[str, Any]):
        """Load a dialogue from dict data."""
        dialogue = Dialogue.from_dict(data)
        self.load_dialogue(dialogue)

    def load_dialogue_file(self, filepath: str) -> bool:
        """
        Load a dialogue from a JSON file.

        Args:
            filepath: Path to the JSON file

        Returns:
            True if loaded successfully
        """
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Dialogue file not found: {filepath}")
                return False

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.load_dialogue_dict(data)
            return True
        except Exception as e:
            print(f"Error loading dialogue: {e}")
            return False

    def load_dialogues_from_directory(self, directory: str) -> int:
        """
        Load all dialogue files from a directory.

        Args:
            directory: Path to directory containing JSON files

        Returns:
            Number of dialogues loaded
        """
        count = 0
        path = Path(directory)
        if not path.exists():
            return 0

        for file in path.glob('*.json'):
            if self.load_dialogue_file(str(file)):
                count += 1

        return count

    def get_dialogue(self, dialogue_id: str) -> Optional[Dialogue]:
        """Get a dialogue by ID."""
        return self._dialogues.get(dialogue_id)

    # =========================================================================
    # DIALOGUE PLAYBACK
    # =========================================================================

    def start_dialogue(self, dialogue_id: str) -> bool:
        """
        Start playing a dialogue.

        Args:
            dialogue_id: ID of the dialogue to start

        Returns:
            True if dialogue started successfully
        """
        dialogue = self._dialogues.get(dialogue_id)
        if not dialogue:
            print(f"Dialogue not found: {dialogue_id}")
            return False

        self._current_dialogue = dialogue
        self._current_node = dialogue.get_start_node()
        self._is_active = True

        # Process start node
        if self._current_node:
            self._process_node(self._current_node)

        # Trigger callback
        if self._on_dialogue_start:
            self._on_dialogue_start(dialogue_id)

        return True

    def advance(self) -> bool:
        """
        Advance to the next node (for nodes without choices).

        Returns:
            True if advanced, False if dialogue ended or has choices
        """
        if not self._is_active or not self._current_node:
            return False

        # Can't advance if there are choices
        if self._current_node.has_choices():
            return False

        # Get next node
        next_id = self._current_node.next_id
        if not next_id or not self._current_dialogue:
            self.end_dialogue()
            return False

        next_node = self._current_dialogue.get_node(next_id)
        if not next_node:
            self.end_dialogue()
            return False

        self._current_node = next_node
        self._process_node(self._current_node)

        # Trigger callback
        if self._on_node_change:
            self._on_node_change(self._current_node)

        return True

    def select_choice(self, choice_index: int) -> bool:
        """
        Select a choice and advance to its target node.

        Args:
            choice_index: Index of the choice to select

        Returns:
            True if choice was valid and selected
        """
        if not self._is_active or not self._current_node:
            return False

        if not self._current_node.has_choices():
            return False

        # Get available choices (filtered by conditions)
        available = self.get_available_choices()
        if choice_index < 0 or choice_index >= len(available):
            return False

        choice = available[choice_index]

        # Set any flags from the choice
        for flag in choice.set_flags:
            self.set_flag(flag)

        # Get next node
        if not choice.next_id or not self._current_dialogue:
            self.end_dialogue()
            return False

        next_node = self._current_dialogue.get_node(choice.next_id)
        if not next_node:
            self.end_dialogue()
            return False

        self._current_node = next_node
        self._process_node(self._current_node)

        # Trigger callback
        if self._on_node_change:
            self._on_node_change(self._current_node)

        return True

    def end_dialogue(self):
        """End the current dialogue."""
        dialogue_id = self._current_dialogue.id if self._current_dialogue else None

        self._current_dialogue = None
        self._current_node = None
        self._is_active = False

        # Trigger callback
        if self._on_dialogue_end:
            self._on_dialogue_end(dialogue_id)

    def _process_node(self, node: DialogueNode):
        """Process a node when it becomes current."""
        # Set any flags
        for flag in node.set_flags:
            self.set_flag(flag)

        # Trigger any event
        if node.trigger_event and node.trigger_event in self._event_callbacks:
            try:
                self._event_callbacks[node.trigger_event]()
            except Exception as e:
                print(f"Error in dialogue event callback: {e}")

    # =========================================================================
    # STATE ACCESS
    # =========================================================================

    def is_active(self) -> bool:
        """Check if a dialogue is currently active."""
        return self._is_active

    def get_current_node(self) -> Optional[DialogueNode]:
        """Get the current dialogue node."""
        return self._current_node

    def get_current_speaker(self) -> str:
        """Get the current speaker name."""
        return self._current_node.speaker if self._current_node else ""

    def get_current_text(self) -> str:
        """Get the current dialogue text."""
        return self._current_node.text if self._current_node else ""

    def get_current_portrait(self) -> str:
        """Get the current portrait ID."""
        return self._current_node.portrait if self._current_node else ""

    def has_choices(self) -> bool:
        """Check if current node has choices."""
        return self._current_node.has_choices() if self._current_node else False

    def get_available_choices(self) -> List[DialogueChoice]:
        """Get choices available at current node (filtered by conditions)."""
        if not self._current_node:
            return []

        available = []
        for choice in self._current_node.choices:
            if choice.condition:
                # Check if condition flag is set
                if not self.has_flag(choice.condition):
                    continue
            available.append(choice)

        return available

    # =========================================================================
    # FLAGS
    # =========================================================================

    def set_flag(self, flag: str, value: bool = True):
        """Set a dialogue flag."""
        self._flags[flag] = value

    def clear_flag(self, flag: str):
        """Clear a dialogue flag."""
        self._flags.pop(flag, None)

    def has_flag(self, flag: str) -> bool:
        """Check if a flag is set."""
        return self._flags.get(flag, False)

    def get_all_flags(self) -> Dict[str, bool]:
        """Get all flags."""
        return self._flags.copy()

    def clear_all_flags(self):
        """Clear all flags."""
        self._flags.clear()

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def register_event(self, event_name: str, callback: Callable):
        """Register a callback for a dialogue event."""
        self._event_callbacks[event_name] = callback

    def on_dialogue_start(self, callback: Callable):
        """Set callback for dialogue start."""
        self._on_dialogue_start = callback

    def on_dialogue_end(self, callback: Callable):
        """Set callback for dialogue end."""
        self._on_dialogue_end = callback

    def on_node_change(self, callback: Callable):
        """Set callback for node change."""
        self._on_node_change = callback

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'flags': self._flags.copy(),
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._flags = state.get('flags', {})


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_dialogue_manager: Optional[DialogueManager] = None


def get_dialogue_manager() -> DialogueManager:
    """Get the global dialogue manager instance."""
    global _dialogue_manager
    if _dialogue_manager is None:
        _dialogue_manager = DialogueManager()
    return _dialogue_manager


def reset_dialogue_manager():
    """Reset the dialogue manager (for new game)."""
    global _dialogue_manager
    _dialogue_manager = DialogueManager()
