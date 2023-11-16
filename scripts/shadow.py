import nova_engine as nova

class Shadow(nova.Object):
    def __init__(self, game, object):
        super().__init__(game, z_pos=0.5) 
        self.image = game.get_assets()["player_shadow"]
        self.object = object
    def update(self):
        self.pos = [self.object.pos[0] - 10 + self.object.velocity[0], self.object.pos[1] + self.object.velocity[1] - 1]
    def render(self):
        self.game.render(self.image, self.pos)