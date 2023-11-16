from typing import Tuple, List, Any
import pygame, nova_engine

def distance(first_position:Tuple[int, int], second_position:Tuple[int, int]) -> float: 
    """
    Fonction qui calcule la distance entre deux points.
    """ 

def json_open(file:str) -> Any:
    """
    Ouvre un ficher json et retourne l'objet qui en résulte.
    """

def draw_alpha_rect(screen:pygame.Surface, position:Tuple[int, int], size:Tuple[int, int], color:Tuple[int, int, int], transparency:int) -> None:
    """
    Dessine un rectangle transparent.
    """

def outline(image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (0, 0, 0)) -> pygame.Surface:
    ...


class ShaderScreen(pygame.Surface):
    def update(self) -> None:
        """
        Rafraichit le contexte graphique.
        """
    def toggle_shaders(self, game:nova_engine.GameContext) -> None:
        """
        Active / Désactive le mode shader.
        """