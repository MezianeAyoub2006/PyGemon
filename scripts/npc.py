import nova_engine as nova, random, pygame

from scripts.shadow import *

#Classe représentant les Pnjs
class Npc(nova.Entity, nova.Animated):
    def __init__(self, game, pos, sprite, config):
        nova.Entity.__init__(self, game, pos, [24, 16], [2, 15])
        nova.Animated.__init__(self, game.get_assets()[sprite])
        self.moving = False
        self.dir = "up"
        self.set_animation(3)
        self.animate(1)
        self.z_pos = 2
        self.spawn = self.pos.copy()
        if self.tags == []:
            self.tags.append("npc")

    def scene_init(self):
        self.game.scene.attach(Shadow(self.game, self, offset=[-8, -10]))
    
    def update(self):
        self.z_pos = (0.4/(self.game.scene.get_size()[1]*self.game.scene.get_tile_size()))*self.rect().bottom + 1.8
        nova.Entity.update(self)
        if self.dir == "left" or self.dir == "up-left" or self.dir == "down-left":
            self.set_animation(1)
        elif  self.dir == "right" or self.dir == "up-right" or self.dir == "down-right":
            self.set_animation(2)
        elif self.dir == "up":
            self.set_animation(3)
        elif self.dir == "down":
            self.set_animation(0)
        
        self.animate(self.game.get_dt())

        if not self.moving:
            self.set_animation_cursor(0)

        self.basic_ai(2.5, 200, 100, 50)

    #Mouvement des pnjs
    def basic_ai(self, speed, moving_prb, turning_prb, stopping_prb):
        if random.randint(0, int(moving_prb*self.game.get_dt())) == 1:
            self.moving = not self.moving
        if random.randint(0, int(turning_prb*self.game.get_dt())) == 1:
            self.dir = ['right', "up", "left", "down", "up-left", "up-right", "down-right", "up-left", "down-left"][random.randint(0, 7)]
        if random.randint(0, int(stopping_prb*self.game.get_dt())) == 1:
            self.moving = False
        if self.collisions['left'] != []:
            self.dir = ["right", "down-right", "up-right"][random.randint(0,2)]
        if self.collisions['right'] != []:
            self.dir = ["left", "down-left", "up-left"][random.randint(0,2)]
        if self.collisions["up"] != []:
            self.dir = ["down", "down-left", "down-right"][random.randint(0,2)]
        if self.collisions["down"] != []:
            self.dir =  ["up", "up-left", "up-right"][random.randint(0,2)]
        if self.moving:
            self.velocity = {"up" : [0, -speed], "down" : [0, speed], "left" : [-speed, 0], "right" : [speed, 0], "up-left" : [-speed/1.4, -speed/1.4], "up-right" : [speed/1.4, -speed/1.4], "down-left" : [-speed/1.4, speed/1.4], "down-right" : [speed/1.4, speed/1.4]}[self.dir]
        else:
            self.velocity = [0, 0]

    def render(self):
        if self.game.DEBUG:
            self.debug_rect((0,255,255))
        super().render()
