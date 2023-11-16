import nova_engine as nova

class BattelHandler(nova.object):
    def __init__(self, game, main_trainer, ennemy):
        nova.object.__init__(game)
        self.main_trainer = main_trainer
        self.ennemy = ennemy
