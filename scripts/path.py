import nova_engine as nova

class Path(nova.Tile):
    def __init__(self, pos, id):
        nova.Tile.__init__(self, pos, id)
        self.solid = False