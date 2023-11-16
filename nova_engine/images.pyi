"""
Module pour le traitement des images (découpage, organisation en animations, dessin des contours, etc.).
"""

from typing import List, Tuple
import pygame

def IMG_PATH(path: str) -> None:
    """
    Définit le chemin d'accès global pour les images.
    """

def load_image(path: str) -> pygame.Surface:
    """
    Charge une image depuis le chemin spécifié.
    """

def load_images(path: str) -> List[pygame.Surface]:
    """
    Charge plusieurs images depuis un dossier.
    """

def set_alpha(image: pygame.Surface, alpha: int) -> pygame.Surface:
    """
    Modifie la transparence d'une image.
    """

def scale_image_list(images: List[pygame.Surface], scaling: Tuple[int, int]) -> List[pygame.Surface]:
    """
    Redimensionne une liste d'images.
    """

def scale_animations(animations: List[List[pygame.Surface]], scaling: Tuple[int, int]) -> List[List[pygame.Surface]]:
    """
    Redimensionne une liste d'animations.
    """

def get_outline(image: pygame.Surface, color: Tuple[int, int, int] = (0, 0, 0)) -> pygame.Surface:
    """
    Crée une image de contour à partir de l'image spécifiée.
    """

def convert_PIL_pygame(img) -> pygame.Surface:
    """
    Convertit une image PIL (Pillow) en surface pygame.
    """

def load_sprite(path: str, slicing: Tuple[int, int]) -> List[pygame.Surface]:
    """
    Charge un sprite découpé en tranches depuis un fichier image.
    """

def load_animation(path: str, slicing: Tuple[int, int], frames: int) -> List[List[pygame.Surface]]:
    """
    Charge une animation découpée en tranches depuis un fichier image.
    """
