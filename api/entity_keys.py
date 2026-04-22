from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class EntityKeys:
    ID = "id"
    PARENT = "parent"
    CHILDS = "childs"
    TRANSFORM = "transform"
    SPRITE = "sprite"
    BOX = "box"