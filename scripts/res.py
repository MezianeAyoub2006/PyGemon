"""
Fichier servant à charger les ressources audio et graphiques
du jeu.
"""

import nova_engine as nova, pygame
nova.IMG_PATH('data/images/')

TILESETS = {
    'main_tileset' : nova.load_sprite('tilesets/main.png', (32, 32))
}

PLAYER_SPRITES = {
    'player_walk_sprite' : nova.scale_animations(nova.load_animation('player/walk_sprite.png', (32, 32), 3), (64, 64)),
    'player_shadow' : pygame.transform.scale(nova.load_image('player/shadow.png'), (64, 64)),
    'bird_keeper_sprite' : nova.scale_animations(nova.load_animation('npcs/bird_keeper.png', (16, 24), 4), (32, 48)),
    'textbox' : nova.load_image('interface/textbox.png')
}