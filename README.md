# comblue-engine
Small python game engine based on pygame for creating 2D arcade games. It is in an early state (version 0.1).
Note: The english in this README is really bad and the documentation is not the best. I will make a new and better one in the next version (probatly using HTML).

## Features
Here are all the features impimented into the engine to this point.

### Game
An instance of the Game class is the core of your game. It manages input, switches scenes, updates every entity in the current scene and renders everything on the screen.
The arguments you can use to change how the instance operates should be easy enough to understand so I don't have to explain them all here. The only method you need to start a game after initialising a instance of the Game class is "start" which just starts the game.

### Entitys
Every object in a scene must be an instance of the Entity class.
If you initialise an instance of this class, you have to give it the game instance, a surface (object in pygame which can be rendered on the screen) and a position (a simple tuple out of two ints). If you use None as an argument for surface the entity will not be rendered on screen. This is usefull if you e.g. want to have Hit- and Hurtboxes.
It has following methods:
-ready: Gets called if the scene, the entity is in, gets initialised in the game scene.
-update: Gets called every frame if the current scene in the game is the scene the entity is in.
-collides_with: Checks for a collision with another entity.
-is_clicked: Checks if the entity gets clicked with the left mouse button.

### Input
If you want to check for input it depends on what you want to check:
-Key input: If you just want to check if a key is pressed in this frame you use the game instance: ´game.keys[key]´. Instead of "key" you have to insert the key you want to check where you have to use the key classes from pygame (pygame.K_w, pygame.K_1, pygame.K_e, etc.). This returns a bool.
-Mouse input: If you want to check for mouse input you have to use the game instance again: ´game.mouse_input´. In this attribute is a tuple with 3 elements where index 0 is the left mouse button, index 1 is the middle mouse button and index 2 is the right mouse button. All elements of mouse_input are boolean.
-Key just pressed input: With this method you can check if a key was pressed, but it stays false after the key was pressed until it is released again. Like always you have to use the game instance to use this method: ´game.keys_just_pressd[key]´. Like with "normal" key input you have to insert the key you want to check instead of "key" as a key class in pygame. Accidantly I have spelled pressed wrong which I will correct in the next version. You also have to register these keys before you can use them in this way with ´game.register_just_pressed_key(key)´. This also returns a bool.

### Scenes
There is no real class for scenes yet, instead they are just lists of all entitys which should be in the scene. So to create a scene you just have to create a list and insert all entitys you want to have in the scene as an element of this list. To switch to a scene you have to call ´game.change_scene(new_scene)´. To set a scene which the game should start with you have to change the attribute ´game.current_scene´ of the game instance.

### Audio
To add audio to your game using a engine you have to use following methods:
-For Sounds: Create a sound by using ´Sound(path)´ and assaining it to a variable. If you want to play it use ´Audio.play_sound(sound)´ and if you want to set its volumne use ´sound.set_volume(volumne)´ while volumne has to be a float or int between 0.0 and 1.0. You can play as much sounds as you want at the same play, also when you currently playing background music.
-For music: You can just play one background music at the same time. To set your background use ´Audio.load_background(path)´, play it with ´Audio.play_background(loop)´ (-1 for a infinite loop), pause it with ´Audio.pause_background()´ and unpause it with ´Audio.unpause_background()´. You can find the current state of the background music in ´Audio.background_state´. Possible states are "None", "Loaded", "Playing" and "Paused".

### Images
To load an image use ´ImageLoader.load_sprite(path)´. If you want to scale the image use ´ImageLoader.load_sprite(path, scale_by)´ where scale_by is an int which must be bigger than 0 and is the factor the image gets scaled with. By defauled it is 1.

### GUI
As of right now there are just two GUI objects you can use in your game:
-Label: A label is object which is used to create text. You create on by using ´Label(game)´. To customize it use ´Label(game, text, font, size, color)´. Font must be an instance of pygame.font.Font. You can change it values by changing the attributes of the label instance you want to change and then call ´label.update_label()´ to uptade it.
-Button: You create a button by using ´Button(game)´. To customize it use ´Button(game, label, size, color)´. "Label" must be an instance of the class Label but should not be in the scene with the button because this gets handeld automatically. A button has to methods which you have to change if you want to change its functionality:
-on_click(): Gets triggered every frame the button is clicked.
-on_pressed(): Gets triggered just one frame if the button is clicked and must get released and pressed again to trigger again.

## Example
Here is a simple example you can use to try out the engine (you need 3 assats):
```
from engine import Game, Entity, ImageLoader, Audio, Sound
import pygame

class Player(Entity):

    def __init__(self, game: Game) -> None:
        super().__init__(game, ImageLoader.load_sprite("character.png", scale_by=3), (400,400))
        self.SPEED = 400
        self.say_sound = Sound("pistol.wav")
    
    def update(self) -> None:
        super().update()
        game: Game = self.game
        if game.keys[pygame.K_a]:
            self.physics.x -= self.SPEED * game.dt
        if game.keys[pygame.K_d]:
            self.physics.x += self.SPEED * game.dt
        if game.keys[pygame.K_s]:
            self.physics.y += self.SPEED * game.dt
        if game.keys[pygame.K_w]:
            self.physics.y -= self.SPEED * game.dt
        self.physics.x = self.physics.x % game.size[0]
        self.physics.y = self.physics.y % game.size[1]

        if game.keys_just_pressd[pygame.K_e]:
            Audio.play_sound(self.say_sound)

game = Game(title="Simple example", size=(800,800), background="green")

game.current_scene = [Player(game)]

game.register_just_pressed_key(pygame.K_e)

Audio.load_background("awesomeness.wav")
Audio.play_background(-1)

game.start()
```

## Notes
-Make sure to have pygame installed
-This is an very early version (v1.0) I made in 2 days which will definetly improve in the future