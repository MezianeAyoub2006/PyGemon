"""
Nova Engine est un Framework python construit sur la base de pygame 
et qui simplifie la création de jeux vidéos perfomants et complexes.
Il agit en surcouche de pygame et nécéssite une bonne conaissance de
celui-ci.
"""

import sys, io
sys.stdout = io.StringIO()
from .object import *
from .context import *
from .entities import *
from .events import *
from .images import *
from .utils import *
from .scene import *
from .transitions import *
from .parallaxe import *
sys.stdout = sys.__stdout__
print("Welcome to Nova Engine v0.1")