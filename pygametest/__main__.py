#!/usr/bin/env python3

import sys
import pygame

from .resload import load_resources_init, load_resource

from .scene_gameplay import SceneGameplay


WIDTH, HEIGHT = 854, 480
TITLE = "pygame Test"
RES_DIR = "./res/"
FULLSCREEN = (sys.argv.count("--fullscreen") + sys.argv.count("-f")> 0)


class Game:
    def __init__(self, width: int = WIDTH, height: int = HEIGHT):
        pygame.init()
        self.width = width
        self.height = height
        flags = pygame.SCALED | pygame.RESIZABLE
        if FULLSCREEN:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((self.width, self.height), flags, vsync=1)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.dbg_font = pygame.font.Font(None, 18)
        self.bg_color = pygame.Color("black")

        self.scene = None
        self.next_scene = SceneGameplay(self)

    def run(self):
        self.resource_load()


        while self.running:
            dt = self.clock.tick() / 1000.0  # delta time in seconds
            if self.next_scene:
                if self.scene:
                    self.scene.exit()
                self.scene = self.next_scene
                self.scene.enter()
                self.next_scene = None
            if self.scene:
                self.scene.update(dt)
                self.scene.render(self.screen)

            self.handle_events()
            self.update(dt)
            self.draw()

    def resource_load(self):
        load_color = pygame.Color("yellow")
        load_bg_color = pygame.Color("#222222")
        files = load_resources_init(RES_DIR)
        total = len(files)
        done = 0
        last_frame = pygame.time.get_ticks()
        for p in files:
            load_resource(p, RES_DIR)
            done += 1
            print(f"Loaded {done}/{total}: {p}")
            if pygame.time.get_ticks() - last_frame > 50:
                last_frame = pygame.time.get_ticks()
                self.screen.fill(self.bg_color)
                pygame.draw.rect(self.screen, load_bg_color, pygame.Rect(50, self.height // 2 - 15, self.width - 100, 30))
                pygame.draw.rect(self.screen, load_color, pygame.Rect(50, self.height // 2 - 15, int((done / total) * (self.width - 100)), 30))
                pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt: float):
        pass

    def draw(self):
        # FPS counter
        fps_text = self.dbg_font.render(f"FPS: {self.clock.get_fps():.1f}", False, pygame.Color("green"), pygame.Color("black"))
        rect = fps_text.get_rect()
        sw, sh = self.screen.get_size()
        self.screen.blit(fps_text, (sw - 80, sh - rect.height - 8))  # fixed x pos for FPS display

        pygame.display.flip()


def main():
    try:
        game = Game()
        game.run()
    except:
        import traceback as tb
        tb.print_exc
        raise
    finally:
        pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()