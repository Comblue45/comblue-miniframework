from .vector import Vector2D
from dataclasses import dataclass

@dataclass
class Sprite:
    id: int
    path: str
    scale_by: Vector2D