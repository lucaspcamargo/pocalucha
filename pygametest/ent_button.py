from typing import Callable, Optional, Tuple
import pygame
from .entity import Entity

# ent_button.py



class Button(Entity):
    """
    A simple clickable button Entity.
    - rect: pygame.Rect or (x, y, w, h)
    - text: label text
    - callback: function(button: Button) called on click
    """

    def __init__(
        self,
        rect: pygame.Rect,
        text: str = "",
        callback: Optional[Callable[["Button"], None]] = None,
        font: Optional[pygame.font.Font] = None,
        colors: Optional[dict] = None,
        border_radius: int = 6,
        enabled: bool = True,
        visible: bool = True,
    ):
        # Attempt to call parent initializer if available
        try:
            super().__init__()
        except TypeError:
            # If Entity requires different signature, it's okay to continue;
            # keep Button lightweight and self-contained.
            pass

        if not isinstance(rect, pygame.Rect):
            rect = pygame.Rect(rect)

        self.rect = rect
        self.text = text
        self.callback = callback

        pygame.font.init()
        self.font = font or pygame.font.SysFont(None, 20)

        # color scheme: normal, hover, pressed, disabled, text
        default_colors = {
            "bg": (200, 200, 200),
            "hover": (170, 170, 170),
            "pressed": (140, 140, 140),
            "disabled": (120, 120, 120),
            "border": (60, 60, 60),
            "text": (10, 10, 10),
        }
        if colors:
            default_colors.update(colors)
        self.colors = default_colors

        self.border_radius = border_radius
        self.enabled = enabled
        self.visible = visible

        # internal state
        self.hover = False
        self.pressed = False
        self._mouse_down_inside = False

    def update(self, dt: float = 0):
        self.time += dt

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events. Returns True if the event was consumed.
        """
        if not self.visible or not self.enabled:
            # still track hover for visual consistency on motion if visible
            if event.type == pygame.MOUSEMOTION and self.visible:
                self.hover = self.rect.collidepoint(event.pos)
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                self._mouse_down_inside = True
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed:
                self.pressed = False
                consumed = False
                if self._mouse_down_inside and self.rect.collidepoint(event.pos):
                    consumed = True
                    if self.callback:
                        try:
                            self.callback(self)
                        except Exception:
                            # swallow exceptions; callers should handle logging if desired
                            pass
                self._mouse_down_inside = False
                return consumed

        return False

    def draw(self, surface: pygame.Surface):
        """
        Draw the button onto the provided surface.
        """
        if not self.visible:
            return

        # choose background color based on state
        if not self.enabled:
            bg = self.colors["disabled"]
        elif self.pressed:
            bg = self.colors["pressed"]
        elif self.hover:
            bg = self.colors["hover"]
        else:
            bg = self.colors["bg"]

        pygame.draw.rect(surface, bg, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.colors["border"], self.rect, width=1, border_radius=self.border_radius)

        if self.text:
            text_surf = self.font.render(self.text, True, self.colors["text"])
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    # convenience setters/getters
    def set_callback(self, cb: Optional[Callable[["Button"], None]]):
        self.callback = cb

    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        if not enabled:
            self.hover = False
            self.pressed = False

    def set_visible(self, visible: bool):
        self.visible = visible

    def is_hovered(self) -> bool:
        return self.hover

    def is_pressed(self) -> bool:
        return self.pressed