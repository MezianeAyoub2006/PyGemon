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
        "scene_name" : "route_102",
        "world_limits" : ["left", "right", "up", "down"],
        "tile_size" : 32,
        "player" : 1,
        "background_color" : [0, 0, 0],
        "right_transition" : {"scene" : "bourg_en_vol"},
        "map_filepath" : "data/maps/routes/r102.json",
        "tileset" : "main_tileset",
        "invisible_layers" : ["inv"],
        "physical_layers" : ["collision", "inv"],
        "layers_z" : {"upper" : 3, "collision" : 1, "background" : 0, '_': 0.3, "__" : 1.3, "inv" : 10} 
    },

    {
        "scene_name" : "route_103",
        "world_limits" : ["left", "right", "up", "down"],
        "tile_size" : 32,
        "player" : 1,
        "background_color" : [0, 0, 0],
        "map_filepath" : "data/maps/routes/r103.json",
        "tileset" : "main_tileset",
        "physical_layers" : ["collision", "inv"],
        "layers_z" : {"upper" : 3, "collision" : 1, "background" : 0, '_': 0.3, "__" : 1.3, "inv" : 10,  "_upper" : 4} 
    },

    {
        "scene_name" : "bourg_en_vol",
        "world_limits" : ["left", "right", "up", "down"],
        "tile_size" : 32,
        "player" : 1,
        "background_color" : [0, 0, 0],
        "map_filepath" : "data/maps/villes/bourg-en-vol.json",
        "tileset" : "main_tileset",
        "left_transition" : {"scene" : "route_102"},
        "physical_layers" : ["collision", "inv"],
        "layers_z" : {"upper" : 3, "collision" : 1, "background" : 0, '_': 0.3, "__" : 1.3, "inv" : 10,  "_upper" : 4, "._":0.25} 
    },
]
