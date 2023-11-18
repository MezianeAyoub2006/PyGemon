import pygame, json, random
from nova_engine.events import SCENESWITCH, TRANSITIONEND

NEIGHBOORS_OFFSET = [(0,0), (0,1), (0,-1), (1,0), (1,-1), (1,1), (-1,0), (-1,1), (-1,-1)]

class Tile:
    def __init__(self, pos, id):
        self.pos = pos
        self.id = id
        self.solid = True
        self.kill = False
        self.collisions = {"up" : True, "down" : True, "left" : True, "right" : True}
    
    def __repr__(self):
        return f"<Tile(id={self.id}, pos={self.pos})>"

    def remove(self):
        self.kill = True

    def update(self, tilemap):
        pass

    def render(self, tilemap):
        tilemap.game.render(tilemap.tileset[self.id], [self.pos[0] * tilemap.tile_size, self.pos[1] * tilemap.tile_size])

    def rect(self, rect, tile_size):
        return pygame.Rect(self.pos[0] * tile_size + rect.x, self.pos[1] * tile_size + rect.y,  rect.w, rect.h)
    
class AnimatedTile(Tile):
    def __init__(self, pos, id):
        self.pos = pos
        self.id = id
        self.animation_cursor = 0

    def animate(self, dt, sequence, animation_speed):
        self.animation_cursor += animation_speed * dt
        try: self.id = sequence[int(self.animation_cursor)]
        except:
            self.animation_cursor = 0
            self.id = sequence[0]

def list_to_matrix(list, xcount):
    matrix=[]
    for i in range(len(list)//xcount):
        matrix.append(list[i*xcount: (i+1)*xcount])
    return matrix

def animated_tile(sequence, animation_speed, **arguments):
    id = 'animated'+str(random.randint(0,10000000))
    n_class = type(id, (AnimatedTile,), {})
    for attribute in dict(arguments):
        setattr(n_class, attribute, dict(arguments)[attribute])
    def update_(tile, tilemap):
        tile.animate(tilemap.game.get_dt(), sequence, animation_speed)
    n_class.update = update_
    return n_class

def load_map(path):
    map_ = []
    layers = []
    objects = []
    with open(path, 'r') as f:
        data = json.load(f)
        for layer in range(len(data['layers'])):
            if 'data' in data['layers'][layer]:
                layers.append(data['layers'][layer]['name'])
                layer_matrix = list_to_matrix(data['layers'][layer]['data'], data['width'])
                map_.append({str(x)+';'+str(y) : Tile((x, y),layer_matrix[y][x]-1) for x in range(len(layer_matrix[0])) for y in range(len(layer_matrix)) if layer_matrix[y][x] != 0})
            elif 'objects' in data['layers'][layer]:
                for object in data['layers'][layer]['objects']:
                    objects.append(object)
    return [map_, [data['width'], data['height']], {i:j for i,j in enumerate(layers)}, objects] 

def generate_screen_positions(tile_size, camera, screen_size):
    for x in range(int(camera[0] // tile_size), int((camera[0] + screen_size[0]) // tile_size + 1)):
        for y in range(int(camera[1] // tile_size), int((camera[1] + screen_size[1]) // tile_size + 1)):
            yield str(x) + ';' + str(y)

class Scene:
    def __init__(self, game, tile_size):
        self.game = game
        self.z_positions = set({})
        self.layers_z_pos = dict({})
        self.tile_size = tile_size
        self.color = [0, 0, 0]
        self.attached_objects = []
        self.PHYSICS_LAYERS, self.NORMAL_LAYERS, self.UPPER_LAYERS = [], [], []
        self.left, self.right, self.up, self.down = [], [], [], []
        self.transition_timer = 0
        self.transition_ceil = 2
        self.transition = None
        self.transition_data = None
        self.entity_block = False
        

    def render(self):          
        if self.transition_timer > 0:
            self.transition_timer += self.game.get_dt()/60
        if self.transition_timer > self.transition_ceil:
            self.transition_timer = 0
            pygame.event.post(pygame.event.Event(TRANSITIONEND))

        if self.game.z_pos_refresh:
            self.z_positions = sorted(set(map(lambda x: x.z_pos, self.attached_objects)).union(set(self.layers_z_pos.keys())))

        self.game.screen.fill(tuple(self.color))
        for object in self.attached_objects:
            object.updated = False

        for z_pos_ in self.z_positions:
            flt = filter(lambda x: x.z_pos == z_pos_, self.attached_objects)
            
            if z_pos_ in map(lambda x: x.z_pos, self.attached_objects):
                for object in flt:
                    if not self.game.freeze and self.transition_timer == 0 : 
                        object.update()
                    object.render()
                    object.updated = True
            else:
                layer = self.layers_z_pos[z_pos_]
                for loc in generate_screen_positions(int(self.tile_size), (int(self.game.camera[0]), int(self.game.camera[1])), self.game.screen.get_size()):
                    if loc in self.layers[self._layer_names[layer]]:
                        tile = self.layers[self._layer_names[layer]][loc]
                        tile.render(self)
                        if not self.game.freeze:
                            tile.update(self)
        
        for i in range(len(self.layers)):
            self.layers[i] = dict(filter(lambda item: not item[1].kill, self.layers[i].items()))

        self.attached_objects = list(filter(lambda x: not x.erased, self.attached_objects))
    
        
        
    
    def tiles_around(self, pos, layer):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOORS_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.layers[self._layer_names[layer]]:
                tiles.append(self.layers[self._layer_names[layer]][check_loc])
        return tiles
    
    def set_transition_mode(self, transition, time=0, entity_block=False):
        self.transition_ceil = time
        self.transition = transition
        self.entity_block = entity_block
    
    def physics_tiles_around(self, pos):
        rects = []
        for i in self.PHYSICS_LAYERS:
            for tile in self.tiles_around(pos, i):
                try:
                    img = self.tileset[tile.id]
                    rect = img.get_bounding_rect()
                    if tile.solid:
                        rects.append([tile.rect(rect, self.tile_size), tile])
                except:
                    pass
        return rects
    
    def handle_transitions(self, scroll_power=100):
        for object in self.attached_objects:
            if object.is_player:
                player = object

        if self.transition != None:
            if self.transition_timer > 0:
                if self.transition(self.game, self.transition_timer, self.transition_ceil) == 1:
                    if self.transition_data != None:
                        self.game.scenes.switch_scene(self.transition_data[0])
                        player.pos = self.transition_data[1]
                        for i in range(scroll_power): self.game.scroll(player.rect().center, False, 15)
                        pl = False
                        for object in self.game.scenes[self.transition_data[0]].attached_objects:
                            if object.is_player:
                                pl = True
                        if not pl:
                            self.game.scenes.attach(self.transition_data[0], player)
                        self.transition_data = None


        if self.transition_data != None and self.transition == None:
            self.transition_timer = 0.01
            self.game.scenes.switch_scene(self.transition_data[0])
            player.pos = self.transition_data[1]
            for i in range(scroll_power): self.game.scroll(player.rect().center, False, 15)
            pl = False
            for object in self.game.scenes[self.transition_data[0]].attached_objects:
                if object.is_player:
                    pl = True
            if not pl:
                self.game.scenes.attach(self.transition_data[0], player)
            self.transition_data = None

        if len(self.left) != 0:
            if player.rect().right < 0:
                if len(self.left) == 3:
                    self.transition_data = [self.left['scene'], [self.game.scenes[self.left['scene']].size[0] * self.tile_size - player.offset[1], self.left['location'] * self.tile_size - player.offset[0]]]
                else:
                    self.transition_data = [self.left['scene'], [self.game.scenes[self.left['scene']].size[0] * self.tile_size - player.offset[1], player.pos[1]]]     
                if self.transition_timer == 0:
                    self.transition_timer = 0.01
                
                    
        if len(self.right) != 0:
            if player.rect().left > self.size[0] * self.tile_size:
                if len(self.right) == 3:
                    self.transition_data = [self.right['scene'], [player.rect().w - player.offset[1], self.right['location'] * self.tile_size  - player.offset[0]]]
                else:
                    self.transition_data = [self.right['scene'], [player.rect().w - player.offset[1], player.pos[1]]]    
                if self.transition_timer == 0:
                    self.transition_timer = 0.01
                   
        if len(self.up) != 0:
            if player.rect().bottom < 0:
                if len(self.up) == 3:
                    self.transition_data = [self.up['scene'], [self.up['location'] * self.tile_size  - player.offset[0], self.game.scenes[self.up['scene']].size[1] * self.tile_size - player.offset[1]]]
                else:
                    self.transition_data = [self.up['scene'], [player.pos[0],  self.game.scenes[self.up['scene']].size[1] * self.tile_size - player.offset[1]]] 
                if self.transition_timer == 0:
                    self.transition_timer = 0.01
                 
        if len(self.down) != 0:
            if player.rect().top > self.size[1] * self.tile_size:
                if len(self.down) == 3:
                    self.transition_data = [self.down['scene'], [self.down['location'] * self.tile_size - player.offset[0], -player.rect().h - player.offset[1]]]
                else:
                    self.transition_data = [self.down['scene'], [player.pos[0],  -player.rect().h - player.offset[1]]] 
                if self.transition_timer == 0:
                    self.transition_timer = 0.01
    
    def transition_into(self, scene):
        self.transition_data = [scene, self.game.player.pos]
        self.transition_timer = 0.01
        return self.transition(self.game, self.transition_timer, self.transition_ceil)

    def change_tile_type(self, tile_class, id):
        if isinstance(id, int):
            for i in range(len(self.layers)):
                for tile in self.layers[i]:
                    if self.layers[i][tile].id == id:
                        self.layers[i][tile] = tile_class(self.layers[i][tile].pos, self.layers[i][tile].id)
        elif isinstance(id, list) or isinstance(id, set) or isinstance(id, tuple):
            for d in id:
                for i in range(len(self.layers)):
                    for tile in self.layers[i]:
                        if self.layers[i][tile].id == d:
                            self.layers[i][tile] = tile_class(self.layers[i][tile].pos, self.layers[i][tile].id)

    def attach(self, object):
        self.attached_objects.append(object)
        self.z_positions = sorted(set(map(lambda x: x.z_pos, self.attached_objects)).union(set(self.layers_z_pos.keys())))
        object.scene_init()

    def get_size(self):
        return self.size
       
    def get_tile_size(self):
        return self.tile_size

class Scenes:
    def __init__(self, game, scenes_data):
        self.scenes = {}
        self.numeric_scenes = []

        for scene_data in scenes_data:
            scene_name = scene_data['scene_name']
            self.numeric_scenes.append(scene_name)
            self.scenes[scene_name] = Scene(game, scene_data['tile_size'])
            if 'background_color' in scene_data:
                self.scenes[scene_name].color = scene_data['background_color']
            if 'map_filepath' in scene_data:
                map = load_map(scene_data['map_filepath'])
                self.scenes[scene_name].is_map = True
                self.scenes[scene_name].layers = map[0]
                self.scenes[scene_name].size = map[1]
                self.scenes[scene_name].objects = map[3]
                self.scenes[scene_name].layer_names = map[2]
                self.scenes[scene_name]._layer_names = {j: i for i, j in map[2].items()}
                self.scenes[scene_name].tileset = game.assets[scene_data['tileset']]
                self.scenes[scene_name].NORMAL_LAYERS = [i for i in map[2].values()]
                self.scenes[scene_name].layers_z_pos = {value : key for key, value in scene_data['layers_z'].items()}
                self.scenes[scene_name].z_positions = self.scenes[scene_name].z_positions.union(self.scenes[scene_name].layers_z_pos)
            else:
                self.scenes[scene_name].is_map = False
                self.scenes[scene_name].size = scene_data['size']
                self.scenes[scene_name].layers = []
            if 'physical_layers' in scene_data:
                self.scenes[scene_name].PHYSICS_LAYERS = scene_data['physical_layers']
                for i in scene_data['physical_layers']:
                    if i in self.scenes[scene_name].NORMAL_LAYERS:
                        self.scenes[scene_name].NORMAL_LAYERS.remove(i)
            if 'world_limits' in scene_data:
                self.scenes[scene_name].world_limit = scene_data['world_limits']
            if 'left_transition' in scene_data:
                self.scenes[scene_name].left = scene_data['left_transition'] 
            if "right_transition" in scene_data:
                self.scenes[scene_name].right = scene_data["right_transition"]      
            if 'up_transition' in scene_data:
                self.scenes[scene_name].up = scene_data['up_transition']    
            if 'down_transition' in scene_data:
                self.scenes[scene_name].down = scene_data['down_transition']
            self.scenes[scene_name]._player = scene_data['player']
        self.game = game
        self.index = scenes_data[0]['scene_name']
        self.game.scene = self.scenes[self.index]
        self.numeric_index = 0

    def __getitem__(self, scene):
        return self.scenes[scene]
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.numeric_index >= len(self.numeric_scenes):
            self.numeric_index = 0
            raise StopIteration
        scene_name = self.numeric_scenes[self.numeric_index]
        self.numeric_index += 1
        return self.scenes[scene_name]
        
    def switch_scene(self, scene):
        source = self.index
        if isinstance(scene, str):
            self.index = scene
            self.game.scene = self.scenes[self.index]
            pygame.event.post(pygame.event.Event(SCENESWITCH, scene=self.index, source=source))
        elif isinstance(scene, int):
            self.index = self.numeric_scenes[self.numeric_index]
            self.game.scene = self.scenes[self.index]
            pygame.event.post(pygame.event.Event(SCENESWITCH, scene=self.index, source=source))
        self.game.scrollx = 0
        self.game.scrolly = 0
        self.game.scroll_ = self.game.camera.copy()

    def render(self):
        self.scenes[self.index].render()

    def attach(self, scene, obj):
        self.scenes[scene].attach(obj)




    


    


"""
if len(self.left) == 3:
    player.pos[1] = self.left['location'] * self.tile_size - player.offset[0]
    player.pos[0] = self.game.scenes[self.left['scene']].size[0] * self.tile_size - player.offset[1]
    for i in range(scroll_power): self.game.scroll(player.rect().center, False, 15)
    pl = False
    for object in self.game.scenes[self.left['scene']].attached_objects:
        if object.is_player:
            pl = True
    if not pl:
        self.game.scenes.attach(self.left['scene'], player)
"""