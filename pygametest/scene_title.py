from pygametest.scene_gameplay import SceneGameplay
from . import scene_base
from . import music
from .resload import get_resource
import math

import pygame
from typing import Any

BGM_VOL = 0.2

class SceneTitle(scene_base.Scene):
    """
    Gameplay scene:
    """
    def __init__(self, manager: Any = None):
        super().__init__("gameplay", manager)
        self.bg_color = pygame.Color("darkslateblue")
        self.time = 0


    def enter(self, *args, **kwargs):
        self.bg_image = get_resource("title/bg.png")
        self.main_image = get_resource("title/main.png")
        #self.entities.append()
        music.play("bgm.ogg")
        music.set_bgm_volume(BGM_VOL)

    def exit(self):
        music.fadeout(1000)

    def pause(self):
        super().pause()

    def resume(self):
        super().resume()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                # stop/fade title music
                music.fadeout(200)

                self.manager.next_scene = SceneGameplay(self.manager)

    def update(self, dt: float):
        super().update(dt)
        self.time += dt
        if self.paused:
            return
        pass

    def render(self, surface: pygame.Surface):
        surface.fill(self.bg_color)
        surface.blit(self.bg_image, (0, 0))
        sw, sh = surface.get_size()
        iw, ih = self.main_image.get_size()
        surface.blit(self.main_image, ((sw - iw) // 2, (sh - ih) // 2 - 180 + math.sin(self.time) * 20))
        title_prov = self.manager.dbg_font.render("POCA LUCHA ------- Press enter to start", None, pygame.Color("green"), pygame.Color("black"))
        surface.blit(title_prov, (40, 40))