import pygame, random

class Animated:
    def __init__(self, animations, animation_speed=0.2):
        self.animation = 0
        self.animations = animations
        self.animation_speed = animation_speed
        self.animation_cursor = 0

    def animate(self, dt):
        if int(self.animation_cursor) + self.animation_speed * dt < len(self.animations[self.animation]): self.animation_cursor += self.animation_speed * dt
        else: self.animation_cursor = 0
        try: self.image = self.animations[self.animation][int(self.animation_cursor)]
        except: self.image = self.animations[self.animation][0]
    
    def set_animation(self, animation):
        self.animation = animation
    
    def set_animation_speed(self, animation_speed):
        self.animation_speed = animation_speed
    
    def set_animation_cursor(self, animation_cursor):
        self.animation_cursor = animation_cursor

    def flip_image(self, x_flip, y_flip):
        self.image = pygame.transform.flip(self.animations[self.animation][int(self.animation_cursor)-1], x_flip, y_flip)

class Entity:
    def __init__(self, game, pos, size, offset=(0,0)):
        self.game = game
        self.pos = [pos[0] * self.game.scene.tile_size, pos[1] * self.game.scene.tile_size]
        self.size = size
        self.offset = offset
        self.image = pygame.Surface((0,0))
        self.velocity = [0, 0]
        self.is_player = False
        self.updated = False
        self.z_pos = 1
        self.erased = False
        self.tags = []
        self.collisions = {'up': [], 'down': [], 'right': [], 'left': []}
    
    def rect(self):
        return pygame.Rect(self.pos[0] + self.offset[0], self.pos[1] + self.offset[1], self.size[0], self.size[1])
    
    def scene_init(self):
        pass

    def debug_rect(self, color):
        image = pygame.Surface((self.size[0], self.size[1]))
        image.fill(color)
        self.game.render(image, [self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]])

    def debug_circle(self, color):
        pygame.draw.circle(self.game.screen, color, (self.rect().centerx + self.offset[0] - self.game.camera[0], self.rect().centery + self.offset[1] - self.game.camera[1]), self.size[0]/2)

    def update(self):
        self.collisions = {'up': [], 'down': [], 'right': [], 'left': []}

        self.pos[0] += self.velocity[0] * self.game.dt
        entity_rect = self.rect()

        for rect in self.game.scene.physics_tiles_around(self.rect().center):
            if entity_rect.colliderect(rect[0]):
                if self.velocity[0] > 0:
                    if rect[1].collisions['right']:
                        entity_rect.right = rect[0].left
                        self.collisions['right'].append(rect[1])
                if self.velocity[0] < 0:
                    if rect[1].collisions['left']:
                        entity_rect.left = rect[0].right
                        self.collisions['left'].append(rect[1])
                self.pos[0] = entity_rect.x - self.offset[0]

        if self.game.scene.world_limit != []:
            if entity_rect.left < 0 and len(self.game.scene.left) == 0 and "left" in self.game.scene.world_limit : entity_rect.left = 0 ; self.pos[0] = entity_rect.x - self.offset[0]
            if entity_rect.right > self.game.scene.tile_size * self.game.scene.size[0] and "right" in self.game.scene.world_limit and len(self.game.scene.right) == 0  : entity_rect.right = self.game.scene.tile_size * self.game.scene.size[0] ; self.pos[0] = entity_rect.x - self.offset[0]
        
        self.pos[1] += self.velocity[1] * self.game.dt
        entity_rect = self.rect()

        for rect in self.game.scene.physics_tiles_around(self.rect().center):
            if entity_rect.colliderect(rect[0]):
                if self.velocity[1] > 0:
                    if rect[1].collisions['down']:
                        entity_rect.bottom = rect[0].top
                        self.collisions['down'].append(rect[1])
                if self.velocity[1] < 0:
                    if rect[1].collisions['up']:
                        entity_rect.top = rect[0].bottom
                        self.collisions['up'].append(rect[1])
                self.pos[1] = entity_rect.y - self.offset[1]

        if  self.game.scene.world_limit != []:
            if entity_rect.top < 0 and len(self.game.scene.up) == 0 and "up" in self.game.scene.world_limit : entity_rect.top = 0 ; self.pos[1] = entity_rect.y - self.offset[1]
            if entity_rect.bottom > self.game.scene.tile_size * self.game.scene.size[1] and "down" in self.game.scene.world_limit and len(self.game.scene.down) == 0: entity_rect.bottom = self.game.scene.tile_size * self.game.scene.size[1] ; self.pos[1] = entity_rect.y - self.offset[1]

    def apply_gravity(self, gravity_force, max=None):
        if max == None:
            self.velocity[1] += gravity_force
        else:
            if max < 0:
                if self.velocity[1] > max:
                    self.velocity[1] += gravity_force
            elif max > 0:
                if self.velocity[1] < max:
                    self.velocity[1] += gravity_force 
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self):
        self.game.render(self.image, (self.pos[0] - self.offset[0], self.pos[1] - self.offset[1]))
