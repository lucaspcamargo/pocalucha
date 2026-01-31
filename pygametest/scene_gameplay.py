from . import scene_base
from . import music
from .resload import get_resource

import pygame
from typing import Any

BGM_VOL = 0.2

class SceneGameplay(scene_base.Scene):
    """
    Gameplay scene:
    """
    def __init__(self, manager: Any = None):
        super().__init__("gameplay", manager)
        self.player = pygame.Rect(self.width // 2 - 25, self.height // 2 - 25, 50, 50)
        self.player_color = pygame.Color("blue")
        self.bg_color = pygame.Color("black")
        self.player_speed = 300 

    def enter(self, *args, **kwargs):
        self.test_bg = get_resource("parallax_mountain_pack/layers/parallax-mountain-bg.png")
        music.play("bgm.ogg")
        music.set_bgm_volume(BGM_VOL)

    def exit(self):
        music.fadeout(1000)

    def pause(self):
        super().pause()

    def resume(self):
        super().resume()

    def handle_event(self, event: pygame.event.Event):
        if self.player:
            self.player.handle_event(event)

    def update(self, dt: float):
        if self.paused:
            return
        
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # normalize diagonal movement
        if dx != 0 and dy != 0:
            diag = 2 ** 0.5
            dx /= diag
            dy /= diag

        self.player.x += int(dx * self.speed * dt)
        self.player.y += int(dy * self.speed * dt)

        # clamp to window
        self.player.clamp_ip(pygame.Rect(0, 0, self.manager.width, self.manager.height))

    def render(self, surface: pygame.Surface):
        surface.fill(self.bg_color)
        surface.blit(self.test_bg, (0, 0))
        pygame.draw.rect(surface, self.player_color, self.player)