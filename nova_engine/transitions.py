import pygame
import nova_engine as nova

def circle_transition(game, transition_timer, transition_ceil):
    if transition_timer < transition_ceil/2: 
        pygame.draw.circle(game.screen, (0,0,0), (game.player.rect().centerx - game.camera[0], game.player.rect().centery - game.camera[1]), transition_timer * (2/transition_ceil) * game.screen.get_size()[0] * 1.15)
        return 0
    else: 
        pygame.draw.circle(game.screen, (0,0,0), (game.player.rect().centerx - game.camera[0], game.player.rect().centery - game.camera[1]), (transition_ceil-transition_timer) * (2/transition_ceil) * game.screen.get_size()[0] * 1.15)
        return 1
    
def centered_circle_transition(game, transition_timer, transition_ceil):
    if transition_timer < transition_ceil/2: 
        pygame.draw.circle(game.screen, (0,0,0), (game.screen.get_size()[0]/2, game.screen.get_size()[1]/2), transition_timer * (2/transition_ceil) * game.screen.get_size()[0] * 1.15)
        return 0
    else: 
        pygame.draw.circle(game.screen, (0,0,0), (game.screen.get_size()[0]/2, game.screen.get_size()[1]/2), (transition_ceil-transition_timer) * (2/transition_ceil) * game.screen.get_size()[0] * 1.15)
        return 1

def fade_transition(game, transition_timer, transition_ceil):
    surf = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
    surf.fill((0,0,0))
    if transition_timer < transition_ceil/2: 
        surf.set_alpha(transition_timer * (2/transition_ceil) * 255)
        game.screen.blit(surf, (0,0))
        return 0
    else: 
        surf.set_alpha((transition_ceil-transition_timer) * (2/transition_ceil) * 255)
        game.screen.blit(surf, (0,0))
        return 1
    
def blank_transition(game, transition_timer, transition_ceil):
    if transition_timer < transition_ceil/2:
        return 0
    else:
        return 1
    


    