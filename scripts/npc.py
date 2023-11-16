import nova_engine as nova

class Npc(nova.Entity, nova.Animated):
    def __init__(self, game, pos, sprite, config):
        nova.Entity.__init__(self, game, pos, [24, 16])
        nova.Animated.__init__(self, game.get_assets()[sprite])
    
    def update(self):
        self.z_pos = 2.1 if self.rect().bottom < self.game.player.rect().bottom else 1.9