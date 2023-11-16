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
        self.flip = False
        self.set_animation_speed(0.18)
    
    def scene_init(self):
        self.game.scene.attach(Shadow(self.game, self))

    def update(self):
        nova.Entity.update(self)
        self.stop = False
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) or (keys[pygame.K_UP] and keys[pygame.K_DOWN]):
            pass
            self.stop = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_LEFT]:
            self.set_animation(1)
            self.flip = False
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_RIGHT]:
            self.set_animation(1)
            self.flip = True
        elif keys[pygame.K_UP]:
            self.set_animation(0)
        elif keys[pygame.K_DOWN]:
            self.set_animation(2)
        elif keys[pygame.K_LEFT]:
            self.set_animation(1)
            self.flip = False
        elif keys[pygame.K_RIGHT]:
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
        super().render()

