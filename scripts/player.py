import nova_engine as nova, pygame
from scripts.shadow import *

class Player(nova.Entity, nova.Animated):
    def __init__(self, game, pos):
        nova.Entity.__init__(self, game, pos, [24, 16], [10, 24])
        nova.Animated.__init__(self, game.get_assets()["player_walk_sprite"])
        self.is_player = True
        self.animate(1)
        self.game = game
        self.tags = ["player"]
        self.z_pos = 2
        self.speed = 2.75
        self.dir = "left"
        self.flip = False
        self.set_animation_speed(0.18)
    
    def scene_init(self):
        self.game.scene.attach(Shadow(self.game, self))

    def update(self):
        self.z_pos = (0.4/(self.game.scene.get_size()[1]*self.game.scene.get_tile_size()))*self.rect().bottom + 1.8
        nova.Entity.update(self)
        self.stop = False
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) or (keys[pygame.K_UP] and keys[pygame.K_DOWN]):
            self.stop = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_LEFT]:
            self.set_animation(1)
            self.dir = "left"
            self.flip = False
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_RIGHT]:
            self.set_animation(1)
            self.dir = "right"
            self.flip = True
        elif keys[pygame.K_UP]:
            self.dir = "up"
            self.set_animation(0)
        elif keys[pygame.K_DOWN]:
            self.dir = "down"
            self.set_animation(2)
        elif keys[pygame.K_LEFT]:
            self.dir = "left"
            self.set_animation(1)
            self.flip = False
        elif keys[pygame.K_RIGHT]:
            self.dir = "right"
            self.set_animation(1)
            self.flip = True
       
        self.velocity = [(int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))*self.speed,(int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))*self.speed]
        if self.stop : self.velocity = [0, 0]
        if abs(self.velocity[0]) == abs(self.velocity[1]) != 0:
            self.velocity[0] *= (1/1.4)
            self.velocity[1] *= (1/1.4)
        if (keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]) and not self.stop:
            self.animate(self.game.get_dt())
        else:
            self.set_animation_cursor(2)
        
    def render(self):
        self.flip_image(self.flip, False)
        if self.game.DEBUG:
            self.debug_rect((255,0,0))
        super().render()

def player_switch_scene(game, scene, dir):
    transition_data = [scene]
    if dir == "left":
        transition_data.append([game.scenes[scene].get_map_size()[0] * game.scene.get_tile_size() - game.player.rect().w, game.player.pos[1]])
    if dir == "right":
        transition_data.append([-game.player.rect().w, game.player.pos[1]])
    if dir == "down":
        transition_data.append([game.player.pos[0], -game.player.rect().h])
    if dir == "up":
        transition_data.append([game.player.pos[0], game.scenes[scene].get_map_size()[1] * game.scene.get_tile_size() - 2*game.player.rect().h])
    game.scene.transition_data = transition_data
    game.scene.transition_timer = 0.01


