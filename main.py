"""
Fichier principal du jeu.
"""

import nova_engine as nova, pygame, sys

from scripts.scenes import *
from scripts.player import *
from scripts.shadow import *
from scripts.npc import *

game = nova.GameContext((640, 360), vsync=True, flags = pygame.SCALED | pygame.RESIZABLE)
DEBUG = True

def scene_links():
    game.scene.attach(game.player)
    game.scene.attach(Npc(game, [5, 5], 'bird_keeper_sprite', {}))

from scripts.res import *

def init():
    global tr
    game.load_assets(TILESETS | PLAYER_SPRITES)
    game.load_scenes(SCENES)
    game.player = Player(game, [5, 5])
    game.switch_scene('test')
    game.load_font("data/fonts/main.ttf", "main", 30)
    scene_links()
    tr = nova.fade_transition
    game.scene.set_transition_mode(tr, time=1)

def events():
    global tr
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                game.toggle_fullscreen()
        if event.type == nova.SCENESWITCH:
            for object in game.scenes[event.scene].attached_objects:
                if "npc" in object.tags:
                    object.pos = object.spawn.copy()

def debug_mode():
    game.render_text(str(round(game.get_fps())), "nova40", (30,30,30), (5,-7), True)

def loop():
    global tr
    events()
    game.scene.render()
    game.set_caption("PyGamon Emerald")
    game.scroll(game.player.rect().center, False, 15)
    game.scene.handle_transitions()
    game.draw(game.get_assets()["textbox"], (70,283))
    game.render_text("Hello, je suis de ton coté Coulalali. Pourquoi", "main30", (0,0,0), (78, 288))
    game.render_text("Oulala", "main30", (0,0,0), (78, 315))
    game.render_text("", "main30", (0,0,0), (195, 303))
    if DEBUG:
        debug_mode()

init()
game.run(loop)


