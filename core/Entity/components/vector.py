from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Vector2D:
    x: int
    y: int