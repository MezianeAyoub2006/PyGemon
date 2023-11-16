"""
Fichier principal du jeu.
"""

import nova_engine as nova, pygame, sys
from scripts.scenes import *
from scripts.player import *
from scripts.shadow import *

game = nova.GameContext((640, 360), vsync=True, flags = pygame.SCALED | pygame.RESIZABLE)

def scene_links():
    game.scene.attach(game.player)


from scripts.res import *

def init():
    global tr
    game.load_assets(TILESETS | PLAYER_SPRITES)
    game.load_scenes(SCENES)
    game.player = Player(game, [5, 5])
    game.switch_scene('test')
    scene_links()
    tr = nova.circle_transition
    game.scene.set_transition_mode(tr, time=1.5)

def events():
    global tr
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                game.toggle_fullscreen()
        if event.type == nova.TRANSITIONEND:
            if tr == nova.circle_transition:
                tr = nova.fade_transition
                game.scene.set_transition_mode(tr, time=1)
            elif tr == nova.fade_transition:
                tr = nova.circle_transition
                game.scene.set_transition_mode(tr, time=1.5)

def loop():
    global tr
    events()
    game.scene.render()
    game.set_caption("PyGamon Emerald")
    game.scroll(game.player.rect().center, False, 15)
    game.render_text(str(round(game.get_fps())), "nova40", (255,255,100), (5,-7), True)
    
    game.scene.handle_transitions()

init()
game.run(loop)


