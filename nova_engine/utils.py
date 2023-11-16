import math, pygame, json

def distance(first_position, second_position):
    return math.sqrt((first_position[0] - second_position[0])**2 + (first_position[1] - second_position[1])**2)

def json_open(file):
    with open(file, 'r') as f:
        return json.load(f)
    
def draw_alpha_rect(screen, postion, size, color, transparency):
    srf = pygame.Surface(size)
    srf.fill(color)
    srf.set_alpha(transparency)
    screen.blit(srf, postion)

def middle(first_position, second_position):
    return ((first_position[0] + second_position[0])/2, (first_position[1] + second_position[1])/2)

def outline(image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (0, 0, 0)) -> pygame.Surface:
    mask = pygame.mask.from_surface(image)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))

    new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
    new_img.fill(color_key)
    new_img.set_colorkey(color_key)

    for i in -thickness, thickness:
        new_img.blit(mask_surf, (i + thickness, thickness))
        new_img.blit(mask_surf, (thickness, i + thickness))
    new_img.blit(image, (thickness, thickness))

    return new_img