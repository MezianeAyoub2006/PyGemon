import pygame
import nova_engine
from typing import *

class GameContext:
    def render(self, image, position) -> None: 
        """
        Permet d'afficher une surface dans un contexte de jeu par rapport à la position de la camera.
        """
        ...
    
    def __init__(self, resolution, flags=0, vsync=False) -> None:
        """
        Contexte de jeu Nova Engine.
        """
        ...
    
    def run(self, game_loop) -> None:
        self.scene:nova_engine.Scene
        self.scenes:nova_engine.Scenes
        self.player:nova_engine.Entity
        """
        Permet de mettre en route la boucle d'exécution du jeu.
        """
        ...

    def scroll(self, position, force_scroll, scroll_speed, x_switch=2, y_switch=2) -> None:
        """
        Permet de faire défiler l'écran en fonction de la position donnée.
        """
        ...

    def load_scenes(self, scenes_data) -> None:
        """
        Charge les scènes à partir des données spécifiées.
        """
        ...

    def switch_scene(self, scene) -> None:
        """
        Permet de changer de scène.
        """
        ...

    def render_scene(self) -> None:
        """
        Rend la scène actuelle.
        """
        ...

    def get_scenes(self):
        """
        Récupère les scènes actuelles.
        """
        ...

    def load_images(self, images_dictionary) -> None:
        """
        Charge les images à partir du dictionnaire spécifié.
        """
        ...

    def get_fps(self):
        """
        Récupère les images par seconde (FPS) actuelles.
        """
        ...

    def get_dt(self):
        """
        Récupère le temps écoulé depuis la dernière frame (delta time).
        """
        ...

    def set_caption(self, text) -> None:
        """
        Définit le texte de la barre de titre de la fenêtre du jeu.
        """
        ...

    def get_event(self, event):
        """
        Récupère un événement spécifique.
        """
        ...

    def quit(self) -> None:
        """
        Quitte le jeu.
        """
        ...

    def toggle_fullscreen(self) -> None:
        """
        Active/désactive le mode plein écran.
        """
        ...
    def render_text(self, text:str, font:str, color:Tuple[int, int, int], position:Tuple[int, int], antialias:bool) -> None:
        """
        Affiche un texte.
        """
        ...
