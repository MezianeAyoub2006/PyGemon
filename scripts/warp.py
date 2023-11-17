import nova_engine as nova, pygame

#Object qui s'active quand le joueur marche dessus et appuye sur espace (utile par ex pour les panneaux)
class Warp(nova.Object):
    def __init__(self, game, pos, size, action):
        nova.Object.__init__(self, game)
        self._pos = pos
        self.z_pos = 1.7
        self._size = size
        self.action = action

    def update(self):
        rect = pygame.Rect([self._pos[0] * self.game.scene.get_tile_size(), self._pos[1] * self.game.scene.get_tile_size()], [self._size[0] * self.game.scene.get_tile_size(), self._size[1] * self.game.scene.get_tile_size()])
        if rect.colliderect(self.game.player.rect()):
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.action()
        if self.game.DEBUG:
            pygame.draw.rect(self.game.screen, (0,255,50), pygame.Rect((rect.left - self.game.camera[0]), (rect.top - self.game.camera[1]), (rect.w), (rect.h)))

