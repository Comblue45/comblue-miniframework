from .vector import Vector2D
from .transform import Transform2D
from dataclasses import dataclass

@dataclass(slots=True)
class Box2D:
    id: int
    transform: Transform2D