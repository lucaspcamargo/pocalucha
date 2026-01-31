from __future__ import annotations
from typing import Any, Dict, Optional
import abc

class Scene(abc.ABC):
    """
    Base class for a game scene.

    Usage:
      - subclass and implement update()
      - override init() / teardown() to allocate / free resources
      - optionally override handle_event() and render()
    """

    def __init__(self, name: Optional[str] = None, manager: Any = None) -> None:
        self.name = name or self.__class__.__name__
        self.manager = manager  # optional scene manager / game reference
        self.active = False
        self.paused = False
        self.resources: Dict[str, Any] = {}
        self.width = manager.width
        self.height = manager.height
        self.entities = []

    def init(self) -> None:
        """
        Called when the scene is started/activated.
        Override to allocate resources, start music, spawn entities, etc.
        """
        self.active = True

    def teardown(self) -> None:
        """
        Called when the scene is stopped/removed.
        Override to free resources, stop sounds, cancel timers, etc.
        Default implementation clears stored resources.
        """
        self.active = False
        self.resources.clear()

    @abc.abstractmethod
    def update(self, dt: float) -> None:
        """
        Advance scene logic. Must be implemented by subclasses.

        Args:
            dt: time delta in seconds since last update call.
        """
        raise NotImplementedError

    def handle_event(self, event: Any) -> None:
        """
        Optional: handle an input/event (e.g. pygame.Event).
        Override as needed.
        """
        pass

    def render(self, surface: Any) -> None:
        """
        Optional: draw the scene to the provided surface (e.g. pygame.Surface).
        Override as needed.
        """
        pass

    def pause(self) -> None:
        """Pause the scene's updates (update should typically early-return when paused)."""
        self.paused = True

    def resume(self) -> None:
        """Resume updates."""
        self.paused = False