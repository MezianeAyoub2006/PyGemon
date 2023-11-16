class Object:
    def __init__(self, game, pos=[0, 0], is_player=False, z_pos=0, erased=False):
        self.game = game
        self.pos = pos
        self.is_player = is_player
        self.z_pos = z_pos
        self.erased = erased
        self.tags = []
    def update(self):
        pass
    def render(self):
        pass
    def scene_init(self):
        pass

class VolativeObject(Object):
    def __init__(self, game, image, pos, z_pos, flag):
        super().__init__(game, pos=pos, z_pos=z_pos)
        self.rendered = False
        self.image = image
        self.flag = flag
    
    def render(self):
        if self.rendered == False:
            if self.flag == "render":
                self.game.render(self.image, self.pos)
            if self.flag == "draw":
                self.game.draw(self.image, self.pos)
            self.rendered = True
            self.erased = True