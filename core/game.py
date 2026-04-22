import pygame
from .Input import PYGAME_TO_KEYS, Mouse, Keys
from collections.abc import Callable
from .Entity import *
from ..api import EntityKeys

class Game:
    """Class which handels the game loop."""

    def __init__(self, 
                 size: tuple[int, int] = (500, 500),
                 title: str = "Comblue Engine",
                 background: str|tuple[int, int, int]|pygame.Surface = "black",
                 first_scene: list[dict[str, object]] = [],
                 tasks: list[Callable] = [],
                 FPS: int|float = 60,
                 debug_mode: bool = False,
                 debug_frames_to_update: int|float = 1) -> None:
        """Initialises the game instance."""
        if not isinstance(size, tuple):
            raise TypeError("size must be of type tuble")
        if not all(isinstance(element, int) for element in size):
            raise TypeError("all element in size must be of type int")
        if not len(size) == 2:
            raise ValueError("size must be 2 elements long")
        if not isinstance(title, str):
            raise TypeError("title must be of type str")
        if not isinstance(background, (str, pygame.Surface)):
            if isinstance(background, tuple):
                if not all(isinstance(element, int) for element in background):
                    raise TypeError("all elements of background as a tuple must be of type int")
                if not len(background) == 3:
                    raise ValueError("background as a tuple must be 3 elements long")
            else:
                raise TypeError("background must be of type str, tuple or pygame.Surface")
        if not isinstance(first_scene, list):
            raise TypeError("first_scene must be of type list")
        if not all(isinstance(entity, dict) for entity in first_scene):
            raise TypeError("all elements of first_scene must be of type Entity")
        if not isinstance(FPS, (int, float)):
            raise TypeError("FPS must be of type int or float")
        if not isinstance(debug_mode, bool):
            raise TypeError("debug_mode must be of type bool")
        if not isinstance(debug_frames_to_update, (int, float)):
            raise TypeError("debug_frames_to_update must be of type int or float")
        
        self.size = size
        self.title = title
        self.background = background
        self.FPS = int(FPS)
        self.debug_mode = debug_mode
        self.debug_frames_to_update = int(debug_frames_to_update)
        self.running = False
        self.current_scene = first_scene
        self.tasks = tasks
        self.chace = {}

        self._keys: dict[str, bool] = {k: False for k in PYGAME_TO_KEYS.values()}
        self._keys_pressed: dict[str, bool] = {k: False for k in PYGAME_TO_KEYS.values()}
        self._mouse: dict[str, bool] = {Mouse.left: False, Mouse.right: False, Mouse.middle: False}
        self._mouse_pressed: dict[str, bool] = {Mouse.left: False, Mouse.right: False, Mouse.middle: False}
        self.input_down = {**self._keys, **self._mouse}
        self.input_pressed = {**self._keys_pressed, **self._mouse_pressed}

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.engine_font = pygame.font.Font(None, size=25)
        self._frame_since_last_debug = 0
        self.debug_overlay_entitys = {(self.size[0] - 75, 10): lambda: self.engine_font.render(f"FPS: {int(self.clock.get_fps())}", False, (255, 255, 255))}

    def start(self) -> None:
        """Starts the game by starting the game loop."""
        self.running = True

        while self.running:
            self.input()
            self.update()
            self.update_render_data()
            if (self._frame_since_last_debug == self.debug_frames_to_update) and (self.debug_mode):
                self._frame_since_last_debug = 0
                self.debug_systems()
            else:
                self._frame_since_last_debug += 1
            self.render()
            self.time()

    def input(self) -> None:
        """Gets current user input and makes it possible to use for everything in the engine."""
        pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        for pygame_key, keys_key in PYGAME_TO_KEYS.items():
            self._keys[keys_key] = pressed[pygame_key]
        
        for i, mouse_key in enumerate([Mouse.left, Mouse.middle, Mouse.right]):
            self._mouse[mouse_key] = mouse_pressed[i]
        
        for key in self._keys_pressed.keys():
            self._keys_pressed[key] = False
        for key in self._mouse_pressed.keys():
            self._mouse_pressed[key] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key in PYGAME_TO_KEYS.keys():
                    self._keys_pressed[PYGAME_TO_KEYS[event.key]] = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._mouse_pressed[Mouse.left] = True
                elif event.button == 2:
                    self._mouse_pressed[Mouse.middle] = True
                elif event.button == 3:
                    self._mouse_pressed[Mouse.right] = True
        
        self.input_down = {**self._keys, **self._mouse}
        self.input_pressed = {**self._keys_pressed, **self._mouse_pressed}
    
    def update(self) -> None:
        """Updates every entity in the game."""
        for task in self.tasks:
            task()

    def debug_systems(self) -> None:
        """Updates every debug system."""
        for pos in self.debug_overlay_entitys.keys():
            self.screen.blit(self.debug_overlay_entitys[pos](), pos)

    def update_render_data(self) -> None:
        """Prepares the screen for updating so every entity is updated."""
        if isinstance(self.background, (pygame.Surface)):
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.background)
        
        for entity in self.current_scene:
            if EntityKeys.SPRITE in entity.keys():
                pos = (entity[EntityKeys.TRANSFORM].position.x, entity[EntityKeys.TRANSFORM].position.y) if entity[EntityKeys.PARENT] == None else (entity[EntityKeys.PARENT][EntityKeys.TRANSFORM].position.x - entity[EntityKeys.TRANSFORM].position.x * -1 ,
                                                                                                                             entity[EntityKeys.PARENT][EntityKeys.TRANSFORM].position.y - entity[EntityKeys.TRANSFORM].position.y * -1)
                self.screen.blit(self.chace[entity[EntityKeys.SPRITE].id], pos)

    def render(self) -> None:
        """Updates the display."""
        pygame.display.flip()

    def time(self) -> None:
        """Makes sure that movment can stay independent by mutlipling with delta time."""
        self.dt = self.clock.tick(self.FPS) / 1000
    
    def change_scene(self, new_scene: list[dict[str, object]]) -> None:
        """Changes the scene and inits it."""
        if not isinstance(new_scene, list):
            raise TypeError("entitys must be of type list")
        if not all(isinstance(entity, dict) for entity in new_scene):
            raise TypeError("all entitys must be of type dict")
        self.current_scene = new_scene
        self.init_scene()

    def is_colliding(self, entity1, entity2) -> bool:
        self.chace[entity1[EntityKeys.BOX].id].topleft = self.get_entity_relativ_pos(entity1)
        self.chace[entity2[EntityKeys.BOX].id].topleft = self.get_entity_relativ_pos(entity2)
        print(self.chace[entity1[EntityKeys.BOX].id].topleft)
        print(self.chace[entity2[EntityKeys.BOX].id].topleft)
        if self.chace[entity1[EntityKeys.BOX].id].colliderect(self.chace[entity2[EntityKeys.BOX].id]):
            return True
        return False
    
    def get_entity_relativ_pos(self, entity) -> tuple:
        return (entity[EntityKeys.TRANSFORM].position.x, entity[EntityKeys.TRANSFORM].position.y) if entity[EntityKeys.PARENT] == None else (entity[EntityKeys.PARENT][EntityKeys.TRANSFORM].position.x - entity[EntityKeys.TRANSFORM].position.x * -1 ,
                                                                                                                             entity[EntityKeys.PARENT][EntityKeys.TRANSFORM].position.y - entity[EntityKeys.TRANSFORM].position.y * -1)