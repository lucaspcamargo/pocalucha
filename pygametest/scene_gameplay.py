from pygametest.ent_bar import Bar
from . import scene_base
from . import music
from .resload import get_resource
from .entity import Entity
from .ent_guy import LittleGuy

import pygame
from typing import Any

BGM_VOL = 0.2

MAX_HEALTH = 100
MAX_STAMINA = 20


class SceneGameplay(scene_base.Scene):
    """
    Gameplay scene:
    """
    def __init__(self, manager: Any = None):
        super().__init__("gameplay", manager)

        self.bg_color = pygame.Color("#222222")

        self.bg_group = pygame.sprite.Group()
        self.hud_group = pygame.sprite.Group()


    def enter(self, *args, **kwargs):
        music.play("bgm.ogg")
        music.set_bgm_volume(BGM_VOL)

        self.entities.append(Entity((0, 0), get_resource("bgs/basic.png"), group=self.bg_group))

        self.ent_p1 = LittleGuy(0, False, (200, 1000-LittleGuy.DIM_Y,))
        self.ent_p2 = LittleGuy(0, True, (1920-200-LittleGuy.DIM_X, 1000-LittleGuy.DIM_Y,))
        self.entities.append(self.ent_p1)
        self.entities.append(self.ent_p2)

        self.ent_p1l = Bar((100, 100), (400, 20), max_value=MAX_HEALTH, current_value=MAX_HEALTH, group=self.hud_group)
        self.ent_p1s = Bar((100, 130), (400, 20), max_value=MAX_STAMINA, current_value=MAX_STAMINA, color=pygame.Color("yellow"), group=self.hud_group)
        self.ent_p2l = Bar((1420, 100), (400, 20), max_value=MAX_HEALTH, current_value=MAX_HEALTH, group=self.hud_group)
        self.ent_p2s = Bar((1420, 130), (400, 20), max_value=MAX_STAMINA, current_value=MAX_STAMINA, color=pygame.Color("yellow"), group=self.hud_group)
        self.entities.append(self.ent_p1l)
        self.entities.append(self.ent_p1s)
        self.entities.append(self.ent_p2l)
        self.entities.append(self.ent_p2s)
        

    def exit(self):
        music.fadeout(1000)

    def pause(self):
        super().pause()

    def resume(self):
        super().resume()

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        if self.paused:
            return
        super().update(dt)

    def render(self, surface: pygame.Surface):
        surface.fill(self.bg_color)
        super().render(surface)