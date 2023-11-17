"""
Fichier définissant les propriétées de toutes les scènes
du jeu.
"""

SCENES = [
    {
        "scene_name" : "battle",
        "tile_size" : 32,
        "player" : 0,
        "background_color" : [255, 0, 0],
        "size" : [300, 300]
    },

    {
        "scene_name" : "test",
        "world_limits" : ["left", "right", "up", "down"],
        "tile_size" : 32,
        "player" : 0,
        "up_transition" : {"scene" : "test"},
        "down_transition" : {"scene" : "test"},
        "background_color" : [0, 0, 0],
        "map_filepath" : "data/maps/test.json",
        "tileset" : "main_tileset",
        "invisible_layers" : ["inv"],
        "physical_layers" : ["physic", "inv"],
        "layers_z" : {"upper" : 3, "physic" : 1, "background" : 0, "inv" : -10, '_': 0.3} 
    },

    {
        "scene_name" : "test_",
        "world_limits" : ["left", "right", "up", "down"],
        "tile_size" : 32,
        "player" : 0,
        "up_transition" : {"scene" : "test"},
        "down_transition" : {"scene" : "test"},
        "background_color" : [0, 0, 0],
        "map_filepath" : "data/maps/test.json",
        "tileset" : "main_tileset",
        "invisible_layers" : ["inv"],
        "physical_layers" : ["physic", "inv"],
        "layers_z" : {"upper" : 3, "physic" : 1, "background" : 0, "inv" : -10, '_': 0.3} 
    }
]
