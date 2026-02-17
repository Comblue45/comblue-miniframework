import pygame
from .Input import Keys, Mouse

class Entity:
    """Base class for every entity in the game."""

    def __init__(self, 
                 game,
                 surface: pygame.Surface, 
                 position: tuple[int, int] = (0, 0)) -> None:
        """Initialises a instance of the Entity class."""
        if not isinstance(surface, pygame.Surface):
            raise TypeError("surface must be of type pygame.Surface")
        if not isinstance(position, tuple):
            raise TypeError("postion must be of type tuple")
        if not all(isinstance(element, int) for element in position):
            raise TypeError("all elements in position must be of type int")
        if not len(position) == 2:
            raise ValueError("position must be two elements long")

        self.game = game
        self.surface = surface
        self.physics = self.surface.get_rect()
        self.physics.topleft = position

    def ready(self) -> None:
        """Method gets called when the scene, it is in, gets loaded into the game."""
        pass

    def update(self) -> None:
        """Method gets called every frame, when the entity is in the current scene of the game."""
        pass

    def collides_with(self, other_entity) -> bool:
        """Method for checking for a collision with another entity easily."""
        if not isinstance(other_entity, Entity):
            raise TypeError("other_entity must be of type Entity")
        if self.physics.colliderect(other_entity.physics):
            return True
        else:
            return False
    
    def is_clicked(self) -> None:
        """Checks if the entity is clicked with the mouse."""
        if self.physics.collidepoint(pygame.mouse.get_pos()) and self.game.input_down[Mouse.left]:
            return True
        else:
            return False