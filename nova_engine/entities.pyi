"""
Module permettant la création d'entités interagissant avec la scène dans laquelle ils sont.
"""

import pygame, random
from typing import List, Tuple

class Animated:
    """
    Classe qui se doit d'être héritée par un élément pour lui permettre de s'animer.
    """
    def __init__(self, animations: List[List[pygame.Surface]], animation_speed: float = 0.2):
        """
        Initialise un objet Animated avec une liste d'animations et une vitesse d'animation donnée.
        """
        pass
        
    def animate(self, dt: float):
        """
        Anime l'objet en fonction du temps écoulé depuis la dernière frame.
        """
        pass
    
    def set_animation(self, animation: int):
        """
        Définit l'index de l'animation en cours.
        """
        pass
    
    def set_animation_speed(self, animation_speed: float):
        """
        Définit la vitesse d'animation.
        """
        pass
    
    def set_animation_cursor(self, animation_cursor: float):
        """
        Définit le curseur d'animation, permettant de contrôler le point de départ de l'animation.
        """
        pass

class Entity:
    """
    Classe regroupant toutes les fonctionnalités relatives aux entités ayant des propriétés physiques (position, vitesse).
    """
    def __init__(self, game, pos: Tuple[int, int], size: Tuple[int, int], offset: Tuple[int, int] = (0, 0), solid: bool = False):
        """
        Initialise une entité avec un jeu parent, une position, une taille, un décalage optionnel et une propriété de solidité.
        """
        pass
    
    def rect(self) -> pygame.Rect:
        """
        Méthode pour récupérer le rectangle englobant de l'entité.
        """
        pass

    def debug_rect(self, color: Tuple[int, int, int]):
        """
        Affiche un rectangle coloré représentant la boîte de collision de l'entité.
        """
        pass

    def debug_circle(self, color: Tuple[int, int, int]):
        """
        Affiche un cercle coloré représentant la boîte de collision de l'entité.
        """
        pass

    def update(self):
        """
        Méthode qui s'exécute chaque frame pour mettre à jour la position et détecter les collisions.
        """
        pass
    
    def render(self):
        """
        Méthode pour afficher l'entité sur l'écran.
        """
        pass
