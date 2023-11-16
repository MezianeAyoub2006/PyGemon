from typing import Tuple
import nova_engine as nova
import pygame
import random
import math

def my_circle_transition(game, transition_timer, transition_ceil):
    game.camera_can_scroll = False
    if nova.centered_circle_transition(game, transition_timer, transition_ceil) == 1:
        for i in range(10):
            game.scroll(game.player.rect().center, False, 5)
        for object_ in game.scene.attached_objects:
            object_.update()

def my_fade_transition(game, transition_timer, transition_ceil):
    game.camera_can_scroll = False
    if nova.fade_transition(game, transition_timer, transition_ceil) == 1:
        for i in range(10):
            game.scroll(game.player.rect().center, False, 5)
        for object_ in game.scene.attached_objects:
            object_.update()

SCENES = [
    {
        "scene_name" : "menu",
        "tile_size" : 64,
        "player" : 0,
        "background_color" : [220, 220, 220],
        "size" : [300, 30]
    },

    {
        "scene_name" : "level",
        "tile_size" : 64,
        "player" : 1,
        "background_color" : [190, 240, 255],
        "world_limits" : ["left", "right"],
        "map_filepath" : "data/map.json",
        "tileset" : "tileset",
        "physical_layers" : ["Level"],
        "invisible_layers" : ["Invisible"],
        "layers_z" : {"Level" : -3, "NoCollisions" : -3.1} 
    }
]

class Flag(nova.Entity, nova.Animated):
    def __init__(self, pos):
        nova.Entity.__init__(self, game, pos, [32*4, 32*4], [30, 64])
        nova.Animated.__init__(self, game.assets["flag_sprite"])
        self.animate(1)
        self.set_animation_speed(0.3)
        self.game = game
        self.z_pos = 0

    def update(self):
        super().update()   
        self.apply_gravity(1, max=20)
        self.animate(self.game.get_dt())

    def render(self):
        super().render()

class Player(nova.Entity, nova.Animated):
    def __init__(self, game, pos, size, offset):
        nova.Entity.__init__(self, game, pos, size, offset)
        nova.Animated.__init__(self, game.assets["player_sprite"])
        self.animate(1)
        self.is_player = True
        self.game = game
        self.z_pos = 3

    def update(self):
        super().update()    
        game.camera_can_scroll = True
        for tile in self.collisions['down']:
            if tile.id == 177:
                self.pos = [8*64, 35*64]
                ennemy.pos = [7*64, 35*64]
                self.velocity = [0, 0]
                game.scene.transition_into('level')

        for tile in self.collisions['up']:
            if tile.id == 215:
                tile.remove()

        if  self.pos[1] > self.game.scene.size[1] * self.game.scene.tile_size and ennemy.pos[1] > self.game.scene.size[1] * self.game.scene.tile_size:
            self.pos = [8*64, 35*64]
            ennemy.pos = [7*64, 35*64]
            self.velocity = [0, 0]
            game.scene.transition_into('level')

        if self.velocity[1] > 1 and self.collisions['down'] == []:
            self.set_animation(4)
        elif self.velocity[1] < 0:
            self.set_animation(3)
        elif abs(self.velocity[0]) > 1:
            self.set_animation(1)
            self.set_animation_speed(0.3)
        else:
            self.set_animation(0)
            self.set_animation_speed(0.3)
 
        self.apply_gravity(1, max=20)
        keys = pygame.key.get_pressed()
        if self.collisions["down"] != [] and keys[pygame.K_UP]:
            self.velocity[1] = -23
        if keys[pygame.K_LEFT]:
            if self.velocity[0] > 0: self.velocity[0] -= 2
            if self.velocity[0] > -9: self.velocity[0] -= 1
        if keys[pygame.K_RIGHT]:
            if self.velocity[0] < 0: self.velocity[0] += 2
            if self.velocity[0] < 9: self.velocity[0] += 1
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.velocity[0] *= 0.9
  
        self.animate(self.game.get_dt())
    
    def render(self):
        self.image = pygame.transform.flip(self.game.assets["player_sprite"][self.animation][int(self.animation_cursor)-1], self.velocity[0] < 0, False)
        super().render()

class Rope(nova.Entity):
    def __init__(self):
        super().__init__(game, [0,0], [0,0], [0,0])
        self.z_pos = 1
    def render(self):
        try: d = int(3000/nova.distance(game.player.rect().center, ennemy.rect().center))
        except: d = 60
        if d > 60: d = 60
        if d == 0: d = 1
        pygame.draw.line(game.screen, (50,25,0), (game.player.rect().centerx - game.camera[0], game.player.rect().centery - game.camera[1]), (ennemy.rect().centerx - game.camera[0], ennemy.rect().centery - game.camera[1]), d) 

class Gate(nova.Tile):
    def __init__(self, pos, id):
        super().__init__(pos, id)
        self.collisions["up"] = False
        self.collisions["left"] = False
        self.collisions["right"] = False

class Ennemy(nova.Entity, nova.Animated):
    def __init__(self, game, pos, size, offset):
        nova.Entity.__init__(self, game, pos, size, offset)
        nova.Animated.__init__(self, game.assets["ennemy_sprite"])
        self.animate(1)
        self.game = game
        self.jump = False
        self.left = False
        self.right = False
        self.z_pos = 2
        self.can_jump = False
        
    def update(self):
        super().update()    

        for tile in self.collisions['down']:
            if tile.id == 177:
                game.player.pos = [8*64, 35*64]
                self.pos = [7*64, 35*64]
                self.velocity = [0, 0]
                game.scene.transition_into('level')

        for tile in self.collisions['up']:
            if tile.id == 215:
                tile.remove()

        if self.pos[1] > self.game.scene.size[1] * self.game.scene.tile_size and game.player.pos[1] > self.game.scene.size[1] * self.game.scene.tile_size:
            self.pos = [7*64, 35*64]
            game.player.pos = [8*64, 35*64]
            self.velocity = [0, 0]
            game.scene.transition_into('level')

        if self.velocity[1] > 1 and self.collisions['down'] == []:
            self.set_animation(2)
        elif self.velocity[1] < 0:
            self.set_animation(2)
        elif abs(self.velocity[0]) > 1:
            self.set_animation(1)
            self.set_animation_speed(0.3)
        else:
            self.set_animation(0)
            self.set_animation_speed(0.3)
 
        self.apply_gravity(1, max=20)
        self.animate(self.game.get_dt())
        self.ai()

    def ai(self):
        self.right = self.pos[0] < self.game.player.pos[0]
        self.left = self.pos[0] > self.game.player.pos[0]
        if self.collisions["down"] != []:
            self.can_jump = True
        if (self.velocity[1] > 3 or (abs(game.player.pos[1] - self.pos[1]) > 150 and game.player.pos[1] < self.pos[1] and (game.player.velocity[1] < -15)) and game.player.collisions['down'] == []) and self.can_jump and game.player.pos[1] < self.pos[1]:
            self.velocity[1] = -math.sqrt(abs(game.player.rect().centery - self.rect().centery)) * 1.4
            self.can_jump = False
        if abs(self.pos[0] - self.game.player.pos[0]) < 80:
            self.left = False
            self.right = False
        if self.left:
            if self.velocity[0] > 0: self.velocity[0] -= 2
            if self.velocity[0] > -abs(game.player.rect().centerx - self.rect().centerx) / 20: self.velocity[0] -= 1
        if self.right:
            if self.velocity[0] < 0: self.velocity[0] += 2
            if self.velocity[0] < abs(game.player.rect().centerx - self.rect().centerx) / 20: self.velocity[0] += 1
        if not (self.left or self.right):
            self.velocity[0] *= 0.9
    
    def render(self):
        self.image = pygame.transform.flip(self.game.assets["ennemy_sprite"][self.animation][int(self.animation_cursor)-1], self.velocity[0] < 0, False)
        super().render()

nova.IMG_PATH('data/')

game = nova.GameContext((1280, 720), vsync=True, flags=pygame.SCALED)
game.camera_can_scroll = True

game.load_images({
    "tileset" : nova.scale_image_list(nova.load_sprite('tileset.png', (16,16)), (64,64)),
    "player_sprite" : nova.scale_animations(nova.load_animation("player_sprite.png", (32, 32), 12), (128,128)),
    "ennemy_sprite" : nova.scale_animations(nova.load_animation("ennemy_sprite.png", (32, 32), 12), (128,128)),
    "flag_sprite" : nova.scale_animations(nova.load_animation("checkpoint.png", (16*4, 16*4), 10), (64*4, 64*4)),
    "mountain" : pygame.transform.scale(nova.load_image("glacial_mountains.png"), (1280, 720)),
    "clouds" : pygame.transform.scale(nova.load_image("clouds_bg.png"), (1280, 720)),
    "clouds2" : pygame.transform.scale(nova.load_image("clouds_mg_1.png"), (1280, 720))
})

game.load_scenes(SCENES)
game.player = Player(game, [10, 35], [55, 90], [20, 18])
ennemy = Ennemy(game,  [7, 35], [70, 90], [16, 18])


game.scenes['level'].attach(game.player)
game.scenes['level'].attach(ennemy)
game.scenes['level'].attach(Rope())
game.scenes['level'].attach(Flag([94,10]))
game.scenes['level'].attach(nova.ParallaxeLayers(game, { (0.02, -10) : "clouds", (0.08, -9) : "mountain"}))

game.scenes['level'].change_tile_type(Gate, 47)
game.scenes['level'].change_tile_type(Gate, 48)
game.scenes['level'].change_tile_type(Gate, 46)


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()
        if event.type == 768:
            if event.key == pygame.K_F11: 
                game.toggle_fullscreen()

def loop():
    if game.scenes.index == "menu" and pygame.key.get_pressed()[pygame.K_SPACE]:
        game.switch_scene("level")
    events()
    game.scene.set_transition_mode(my_fade_transition, time=1)
    game.set_caption(f'Jeu Nova Engine, FPS : {round(game.get_fps())}')
    game.scene.render()
    game.scene.handle_transitions()
    if game.camera_can_scroll:
        game.scroll(game.player.rect().center, False, 15)

game.run(loop)