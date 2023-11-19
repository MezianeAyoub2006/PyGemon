import nova_engine as nova

#Object concernant l'ombre en dessous du joueur et des pnjs
class Shadow(nova.Object):
    def __init__(self, game, object, offset=[0,0]):
        super().__init__(game, z_pos=0.5) 
        self.image = game.get_assets()["player_shadow"]
        self.object = object
        self.offset_ = offset
    def update(self):
        self.pos = [self.object.pos[0] - 10 + self.object.velocity[0] + self.offset_[0], self.object.pos[1] + self.object.velocity[1] - 1 + self.offset_[1]]
    def render(self):
        self.game.render(self.image, self.pos)