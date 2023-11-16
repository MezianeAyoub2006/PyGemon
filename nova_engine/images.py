import os, pygame
from PIL import Image

PATH = ''

def IMG_PATH(path):
    global PATH
    PATH = path

def load_image(path):
    img = pygame.image.load(f'{PATH}{path}').convert_alpha()
    return img

def load_images(path):
    images = []
    for image_name in os.listdir(f'{PATH}/{path}'):
        images.append(load_image(f'{path}/{image_name}'))
    return images

def set_alpha(image, alpha):
    img = image
    img.set_alpha(alpha)
    return img

def scale_image_list(images, scaling):
    return [pygame.transform.scale(image, scaling) for image in images]

def scale_animations(animations, scaling):
    return [scale_image_list(images, scaling) for images in animations]

def get_outline(image, color=(0,0,0)):
    mask = pygame.mask.from_surface(image, 127)
    outline_image = pygame.Surface(image.get_size()).convert_alpha()
    outline_image.fill((0,0,0,0))
    for point in mask.outline():
        outline_image.set_at(point,color)
    return outline_image

def convert_PIL_pygame(img):
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pygame.image.fromstring(data, size, mode)

def load_sprite(path, slicing):
    sprite = Sprite(PATH + path)
    sprite.slice_(slicing[0], slicing[1])
    return [convert_PIL_pygame(image).convert_alpha() for image in sprite.slices]

def load_animation(path, slicing, frames):
    sprite = Sprite(PATH + path)
    sprite.slice_(slicing[0], slicing[1])
    sprite.organise(frames)
    return sprite.slices
    
class Sprite:

    def __init__(self, img):
        self.img = Image.open(img)

    def slice_(self, x, y):    
            width, height = self.img.size
            slices = []
            for i in range(0, height, y):
                for j in range(0, width, x):
                    box = (j, i, j+x, i+y)
                    slices.append(self.img.crop(box))
            self.slices = slices

    def organise(self, y):
        m=[]
        for i in range(len(self.slices)//y):
            m.append(self.slices[i*y: (i+1)*y])
        for i in m:
            ni = [image for image in i if not all(p[3] == 0 for p in image.getdata())]
            i[:] = ni
        for i in range(len(m)):
            for j in range(len(m[i])):
                m[i][j] = convert_PIL_pygame(m[i][j]).convert_alpha()
        self.slices = m