"""
Fichier principal du jeu.
"""

import nova_engine as nova, pygame, sys

from scripts.scenes import *
from scripts.player import *
from scripts.shadow import *
from scripts.npc import *
from scripts.text import *
from scripts.warp import *
from scripts.objects import *

game = nova.GameContext((480, 360), vsync=True, flags = pygame.SCALED | pygame.RESIZABLE)
game.DEBUG = False
c = ""

def scene_links():
    game.scene.attach(game.player)
    link_defined_objects(game)

from scripts.res import *

def init():
    game.load_assets(TILESETS | PLAYER_SPRITES)
    game.load_scenes(SCENES)

    game.player = Player(game, [10, 10])

    game.load_font("data/fonts/main.ttf", "main", 30)
    game.load_font("data/fonts/main.ttf", "main", 32)
    game.load_font("data/fonts/main.ttf", "main", 40)

    game.switch_scene('route_101')
    scene_links()
    for i in range(150): game.scroll(game.player.rect().center, game.DEBUG, 15)

def events():
    global tr, c
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            c += event.unicode
            if event.key == pygame.K_F11:
                game.toggle_fullscreen()
            if event.key == pygame.K_LSHIFT:
                if c == "debugmode":
                    game.DEBUG = not game.DEBUG
                elif c.split(" ")[0] == "tp":
                    game.player.pos = [float(c.split(" ")[1]) * game.scene.get_tile_size(), float(c.split(" ")[2]) * game.scene.get_tile_size()]
                c = ""
        if event.type == nova.SCENESWITCH:
            for object in game.scenes[event.scene].attached_objects:
                if "npc" in object.tags:
                    object.pos = object.spawn.copy()

def debug_mode():
    game.render_text(str(round(game.get_fps())), "main30", (30,30,30), (5,-2), True)
    game.render_text("DEBUG MODE", "main30", (30,30,30), (5,335), True)
    game.render_text(f'{round(game.player.rect().center[0] / game.scene.get_tile_size(), 1)} | {round(game.player.rect().center[1] / game.scene.get_tile_size(), 1)}', "main30", (30,30,30), (490,-2), True)

def loop():
    global tr
    events()
    game.scene.set_transition_mode(nova.fade_transition, time=1)
    game.scene.render()
    game.set_caption("PyGamon Emerald")
    game
    game.scroll(game.player.rect().center, game.DEBUG, 15)
    game.render_text("", "main30", (0,0,0), (195, 303))
    if game.DEBUG:
        debug_mode()

init()
game.run(loop)


