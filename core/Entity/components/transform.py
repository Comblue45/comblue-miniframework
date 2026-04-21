from .vector import Vector2D
from dataclasses import dataclass

@dataclass(slots=True)
class Transform2D:
    id: int
    position: Vector2D
    rotation: Vector2D
    scale: Vector2D