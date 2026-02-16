import pygame
from .entity import Entity

class Game:
    """Class which handels the game loop."""

    def __init__(self, 
                 size: tuple[int, int] = (500, 500),
                 title: str = "Comblue Engine",
                 background: str|tuple[int, int, int]|pygame.Surface = "black",
                 first_scene: list[Entity] = [],
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
        if not all(isinstance(entity, Entity) for entity in first_scene):
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
        self.keys: pygame.key.ScancodeWrapper
        self.keys_just_pressd = {}
        self.mouse_input = ()

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
        self.init_scene()

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
        self.keys = pygame.key.get_pressed()
        self.mouse_input = pygame.mouse.get_pressed()

        for key in self.keys_just_pressd:
            self.keys_just_pressd[key] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in self.keys_just_pressd:
                    self.keys_just_pressd[event.key] = True
    
    def update(self) -> None:
        """Updates every entity in the game."""
        for entity in self.current_scene:
            entity.update()

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
            self.screen.blit(entity.surface, entity.physics)

    def render(self) -> None:
        """Updates the display."""
        pygame.display.flip()

    def time(self) -> None:
        """Makes sure that movment can stay independent by mutlipling with delta time."""
        self.dt = self.clock.tick(self.FPS) / 1000

    def init_scene(self) -> None:
        """Initialises the current scene."""
        for entity in self.current_scene:
            entity.ready()
    
    def change_scene(self, new_scene: list[Entity]) -> None:
        """Changes the scene and inits it."""
        if not isinstance(new_scene, list):
            raise TypeError("entitys must be of type list")
        if not all(isinstance(entity, Entity) for entity in new_scene):
            raise TypeError("all elements of entitys must be of type Entity")
        self.current_scene = new_scene
        self.init_scene()

    def register_just_pressed_key(self, key) -> None:
        """Appends a key to the keys_just_pressd dict so it can be checked for a just-pressed event every frame."""
        self.keys_just_pressd[key] = False