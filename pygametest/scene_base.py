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
        # TODO update entities
        pass

    def handle_event(self, event: Any) -> None:
        for ent in self.entities:
            if ent is None:
                continue
            # prefer custom handle_event(event)
            handle_fn = getattr(ent, "handle_event", None)
            if callable(handle_fn):
                try:
                    handle_fn(event)
                except Exception:
                    continue

    def render(self, surface: Any) -> None:
        """Render entities. Entities may implement render(surface), draw(surface), or have image/rect."""
        # render in order of z attribute if present
        entities = sorted(self.entities, key=lambda e: getattr(e, "z", 0))
        for ent in entities:
            if ent is None:
                continue
            # prefer custom render(surface)
            render_fn = getattr(ent, "render", None)
            if callable(render_fn):
                try:
                    render_fn(surface)
                except TypeError:
                    # some renderers may not accept surface
                    try:
                        render_fn()
                    except Exception:
                        continue
                except Exception:
                    continue
            else:
                draw_fn = getattr(ent, "draw", None)
                if callable(draw_fn):
                    try:
                        draw_fn(surface)
                    except Exception:
                        continue
                elif hasattr(ent, "image") and hasattr(ent, "rect"):
                    try:
                        surface.blit(ent.image, ent.rect)
                    except Exception:
                        continue

    def pause(self) -> None:
        """Pause the scene's updates (update should typically early-return when paused)."""
        self.paused = True

    def resume(self) -> None:
        """Resume updates."""
        self.paused = False