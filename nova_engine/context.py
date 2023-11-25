import pygame, time, os, moderngl, array, nova_engine as nova

from nova_engine.scene import *
from nova_engine.events import *
from nova_engine.utils import *

pygame.init()

class GameContext:
    def __init__(self, resolution, flags=0, vsync=False, z_pos_refresh=True):
        self.fullscreen = False      
        self.screen = pygame.display.set_mode(resolution, flags, vsync=vsync)

        pygame.display.set_caption(" nova engine project", f"{__file__[:-10]}icon.png")
        pygame.display.set_icon(pygame.image.load(f"{__file__[:-10]}icon.png"))

        self.dt = 1
        self.lt = time.perf_counter()
        self.clock = pygame.time.Clock()
        self.fps = 1000
        self.camera = [0, 0]
        self.scroll_ = [0, 0]
        self.z_pos_refresh = z_pos_refresh

        self.fonts = {}

        self.load_sysfont("Arial", 5)
        self.load_sysfont("Arial", 10)
        self.load_sysfont("Arial", 15)
        self.load_sysfont("Arial", 20)
        self.load_sysfont("Arial", 30)
        self.load_sysfont("Arial", 40)
        self.load_sysfont("Arial", 50)
        self.load_sysfont("Arial", 60)

        s = self.render_text("Chargement", 'Arial20', (255,255,255), (0, 0), antialias=True)
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect((0,0),self.screen.get_size()))
        rect = pygame.Rect(0, 0, s.get_size()[0], s.get_size()[1])
        rect.center = (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2)
        self.render_text("Chargement", 'Arial20', (255,255,255), rect.topleft, antialias=True)
        pygame.display.flip()

        self.load_font(__file__[:-10]+"nova.otf", "nova", 40)

        self.scrollx = True
        self.scrolly = True

        self.fps_count = 0
        self.frames = 0
        self.debug = False
        self.clock_time = 0

        self.freeze = False

    def run(self, game_loop):
        while True:
            self.fps_average(10)
            self.delta_time()  
            self.clock_time += self.dt/60
            game_loop()
            pygame.display.flip()
            self.clock.tick(self.fps)
    
    def z_render(self, image, pos, z_pos):
        self.scene.attach(nova.VolativeObject(self, image, pos, z_pos, "render"))
    
    def z_draw(self, image, pos, z_pos):
        self.scene.attach(nova.VolativeObject(self, image, pos, z_pos, "draw"))

    def cam_follow(self, pos):
        self.camera = [pos[0] + self.screen.get_size()[0]/2, pos[1] + self.screen.get_size()[1]/2]

    def render(self, image, position):
        self.screen.blit(image, (position[0] - self.camera[0], position[1] - self.camera[1]))
    
    def draw(self, image, position):
        self.screen.blit(image, position)
    
    def delta_time(self):
        self.dt = time.perf_counter() - self.lt
        self.dt *= 60
        self.lt = time.perf_counter()

    def fps_average(self, reset_delay):
        self.frames += 1
        self.fps_count += self.clock.get_fps()
        if self.clock_time > reset_delay:
            self.frames = 1
            self.fps_count = 0
            self.clock_time = 0

    def scroll(self, position, force_scroll, scroll_speed, x_switch = 2, y_switch = 2):
        self.scroll_in_x(position[0], force_scroll, scroll_speed, x_switch)
        self.scroll_in_y(position[1], force_scroll, scroll_speed, y_switch)

    def scroll_in_x(self, position, force_scroll, scroll_speed, x_switch = 2):
        if force_scroll:
            self.scroll_[0] += (position - self.screen.get_width() / 2 - self.scroll_[0]) / scroll_speed
            self.camera = [int(self.scroll_[0]), self.camera[1]]
        else:
            if self.camera[0] + self.screen.get_width() + 3 > self.scene.tile_size * self.scene.size[0]:
                self.scrollx = -1
            if self.camera[0] < 3:
                self.scrollx = 1

            if self.player.pos[0] + self.screen.get_width() / x_switch < self.scene.tile_size * self.scene.size[0] and self.scrollx == -1:
                self.scrollx = 0
            if self.player.pos[0] > self.screen.get_width() / x_switch and self.scrollx == 1:
                self.scrollx = 0
            
            if self.scrollx == 0:
                self.scroll_[0] += ((position - self.screen.get_width() / 2 - self.scroll_[0]) / scroll_speed) * self.dt

            self.camera = [int(self.scroll_[0]), self.camera[1]]
            if self.camera[0] < 0:
                self.camera[0] = 0
            if self.camera[0] + self.screen.get_size()[0] > self.scene.tile_size * self.scene.size[0]:
                self.camera[0] = self.scene.tile_size * self.scene.size[0] - self.screen.get_size()[0]
    
    def scroll_in_y(self, position, force_scroll, scroll_speed, y_switch = 2):
        if force_scroll:
            self.scroll_[1] += (position - self.screen.get_height() / 2 - self.scroll_[1]) / scroll_speed
            self.camera = [self.camera[0], int(self.scroll_[1])]
        else:
            if self.camera[1] + self.screen.get_height() + 3 > self.scene.tile_size * self.scene.size[1]:
                self.scrolly = -1
            if self.camera[1] < 3:
                self.scrolly = 1

            if self.player.pos[1] + self.screen.get_height() / y_switch < self.scene.tile_size * self.scene.size[1] and self.scrolly == -1:
                self.scrolly = 0
            if self.player.pos[1] > self.screen.get_height() / y_switch and self.scrolly == 1:
                self.scrolly = 0
            
            if self.scrolly == 0:
                self.scroll_[1] += ((position - self.screen.get_height() / 2 - self.scroll_[1]) / scroll_speed) * self.dt

            self.camera = [self.camera[0], int(self.scroll_[1])]
            if self.camera[1] < 0:
                self.camera[1] = 0
            if self.camera[1] + self.screen.get_size()[1] > self.scene.tile_size * self.scene.size[1]:
                self.camera[1] = self.scene.tile_size * self.scene.size[1] - self.screen.get_size()[1]
    
    def load_scenes(self, scenes_data):
        self.scenes = Scenes(self, scenes_data)

    def switch_scene(self, scene):
        self.scenes.switch_scene(scene)

    def render_scene(self):
        self.scenes.render()

    def get_scenes(self):
        return self.scenes

    def load_assets(self, images_dictionary):
        self.assets = images_dictionary

    def get_assets(self):
        return self.assets

    def get_fps(self):
        return self.clock.get_fps()
    
    def get_dt(self):
        return self.dt

    def set_caption(self, text):
        pygame.display.set_caption(text)

    def get_event(self, event):
        if event == "SCENESWITCH":
            return SCENESWITCH

    def quit(self):
        pygame.quit()
        os._exit(os.EX_OK)

    def toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()
        self.fullscreen = not self.fullscreen
    
    def load_font(self, file, name, size): 
        txt = name
        txt += str(size)
        self.fonts[txt] = pygame.font.Font(file, size)

    def load_sysfont(self, sysfont, size):
        txt = sysfont
        txt += str(size)
        self.fonts[txt] = pygame.font.SysFont(sysfont, size)

    def render_text(self, text, font, color=(0,0,0), position=(15, 15), antialias=True):
        font = self.fonts[font]
        self.screen.blit(font.render(text, antialias, color), position)
        return font.render(text, antialias, color)

class ShaderScreen(pygame.Surface):
    def __init__(self, size, shaders):
        super().__init__(size)
        self.size = size
        self.display = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
        self.hud = pygame.Surface(self.size, pygame.SRCALPHA)
        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array.array('f', [-1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, 0.0, 1.0, 1.0, -1.0, 1.0, 1.0]))
        self.program = self.ctx.program(vertex_shader=open(f"{os.getcwd()}\\shaders\\vertex.glsl").read(), fragment_shader=open(f"{os.getcwd()}\\shaders\\fragment.glsl").read())
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        self.shaders = shaders
        self.program['tex'] = 0
        self.program['hud'] = 1
    
    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
    
    def update(self):
        self.display.blit(self, (0,0))
        if self.shaders:
            self.frame_tex = self.surf_to_texture(self.display)
            self.frame_tex.use(0)
            self.hud_tex = self.surf_to_texture(self.hud)
            self.hud_tex.use(1)
            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        else: self.display.blit(self.hud, (0,0))
        self.hud.fill((0,0,0,0))
       
    def toggle_shaders(self, game):
        self.shaders = not self.shaders
        if self.shaders: self.__init__(self.size, self.shaders)
        else: self.display = pygame.display.set_mode(self.size) ; self.hud = pygame.Surface(self.size, pygame.SRCALPHA)
        game.hud = self.hud
        if game.fullscreen: pygame.display.toggle_fullscreen()
        
    
            