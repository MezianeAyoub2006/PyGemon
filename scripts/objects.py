import nova_engine as nova, pygame

from scripts.warp import *
from scripts.npc import *

def find(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]

def get_property(properties, property):
    if len(find(properties, lambda x : x["name"] == property)) >= 1:
        return properties[find(properties, lambda x : x["name"] == property)[0]]["value"]
    else:
        return []

def link_defined_objects(game : nova.GameContext):
    for scene in game.scenes:
        if hasattr(scene, "objects"):
            for object in scene.objects:
                try:
                    properties = object["properties"]
                    if get_property(properties, "type") == "warp":
                        scene.attach(Warp(game, [float(object["x"]) / scene.get_tile_size(), float(object["y"]) / scene.get_tile_size()], [float(object["width"]) / scene.get_tile_size(), float(object["height"]) / scene.get_tile_size()], f'lambda self : {get_property(properties, "action")}', f'lambda self : {get_property(properties, "condition")}', bool(get_property(properties, "direct")), bool(get_property(properties, "volatile"))))
                    if get_property(properties, "type") == "textwarp":
                        scene.attach(Warp(game, [float(object["x"]) / scene.get_tile_size(), float(object["y"]) / scene.get_tile_size()], [float(object["width"]) / scene.get_tile_size(), float(object["height"]) / scene.get_tile_size()], f'lambda self : self.game.scene.attach(TextBox("{get_property(properties, "text")}", self.game))', f'lambda self : {get_property(properties, "condition")}', bool(get_property(properties, "direct")), bool(get_property(properties, "volatile"))))
                    if get_property(properties, "type") == "textbox":
                        scene.attach(Warp(game, [float(object["x"]) / scene.get_tile_size(), float(object["y"]) / scene.get_tile_size()], [float(object["width"]) / scene.get_tile_size(), float(object["height"]) / scene.get_tile_size()], f'lambda self : self.game.scene.attach(TextBox("{get_property(properties, "text")}", self.game))', f'lambda self : {get_property(properties, "condition")}', False, False))
                    if get_property(properties, "type") == "npc":
                        npc_attach(game, scene.name, int(get_property(properties, 'id')), [float(object["x"]) / scene.get_tile_size(), float(object["y"]) / scene.get_tile_size()])
                except:
                    pass
        