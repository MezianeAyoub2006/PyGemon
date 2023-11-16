"""
Module permettant la gestion des scènes
qui sont des espaces dans lesquels divers
objets statiques ou dynamiques peuvent
intéragir
"""
import pygame
from typing import List, Dict, Union, Tuple, Any

SceneData = Dict[str, Union[str, List[int], Dict[str, Union[str, int, List[str]]]]]

def list_to_matrix(list_: List[int], xcount: int) -> List[List[int]]:
    """
    Convertit une liste en matrice bidimensionnelle ayant pour abcisse 'xcount'.
    """

def animated_tile(sequence: List[int], animation_speed: float, **arguments) -> type:
    """
    Crée et retourne une classe de tuile animée basée sur la séquence d'images et la vitesse d'animation spécifiées.
    """

def load_map(path: str) -> List[Union[List[Dict[str, int]], List[int], Dict[int, str]]]:
    """
    Charge une carte à partir du fichier spécifié et retourne les données de la carte.
    """

class Tile:
    def __init__(self, pos: Tuple[int, int], id: int) -> None:
        """
        Initialise un objet Tile avec une position et un identifiant.
        """

class AnimatedTile(Tile):
    def __init__(self, pos: Tuple[int, int], id: int) -> None:
        """
        Initialise un objet AnimatedTile avec une position et un identifiant.
        """

class Scene:
    def __init__(self, game: Any, tile_size: int) -> None:
        """
        Initialise un objet Scene avec un jeu et une taille de tuile.
        """
    
    def render(self) -> None:
        """
        Affiche la scène et actualise ses éléments.
        """

    def tiles_around(self, pos: Tuple[int, int], layer: int) -> List[Tile]:
        """
        Récupère toutes les tuiles autour d'une position donnée dans une couche spécifique.
        """

    def physics_tiles_around(self, pos: Tuple[int, int]) -> List[List[Union[pygame.Rect, List[Union[Tuple[int, int], int]]]]]:
        """
        Récupère toutes les tuiles solides autour d'une position donnée pour la gestion des collisions.
        """

    def handle_transitions(self, scroll_power: int = 1000) -> None:
        """
        Fait transitionner le joueur entre plusieurs scènes si cela est spécifié dans les paramètres de la scène.
        """
    
    def change_tile_type(self, tile_class: type, id: Union[int, List[int]]) -> None:
        """
        Change le type de tuile pour les identifiants spécifiés dans la couche courante.
        """

    def attach(self, object: Any) -> None:
        """
        Attache un objet à la scène.
        """

class Scenes:
    def __init__(self, game: Any, scenes_data: List[SceneData]) -> None:
        """
        Initialise un objet Scenes avec un jeu et les données des scènes.
        """
        self.index:str
        """
        Scène actuelle.
        """
    
    def __getitem__(self, scene: str) -> Scene:
        """
        Récupère la scène spécifiée.
        """
    
    def __iter__(self) -> 'Scenes':
        """
        Itère sur les scènes.
        """
    
    def __next__(self) -> Scene:
        """
        Récupère la prochaine scène lors de l'itération.
        """
    
    def switch_scene(self, scene: Union[str, int]) -> None:
        """
        Change la scène courante du jeu.
        """
    
    def render(self) -> None:
        """
        Affiche la scène courante.
        """
    
    def attach(self, scene: str, obj: Any) -> None:
        """
        Attache un objet à la scène spécifiée.
        """
