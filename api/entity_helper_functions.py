from ..core import IDSystem, Vector2D, Transform2D, Sprite, add_entry_to_chace, Game, Box2D
from .entity_keys import EntityKeys
from pygame.image import load

def create_entity(parent: dict[str, object]|None, childs: list[dict[str, object]]) -> dict[str, object]:
    return {EntityKeys.ID: IDSystem.next_id(),
            EntityKeys.PARENT: parent,
            EntityKeys.CHILDS: childs}

def create_2d_entity(parent: dict[str, object], childs: list[dict[str, object]], position: Vector2D) -> dict[str, object]:
    return create_entity(parent, childs) | {EntityKeys.TRANSFORM: Transform2D(IDSystem.next_id(), position, Vector2D(0,0), Vector2D(0,0))}

def create_sprite_entity(parent: dict[str, object], childs: list[dict[str, object]], position: Vector2D, image_path: str, game: Game) -> dict[str, object]:
    new_entity = create_2d_entity(parent, childs, position) | {EntityKeys.SPRITE: Sprite(IDSystem.next_id(), image_path, Vector2D(1,1))}
    add_entry_to_chace(game.chace, new_entity[EntityKeys.SPRITE].id, load(new_entity[EntityKeys.SPRITE].path))
    return new_entity

def create_collision_entity(parent: dict[str, object], childs: list[dict[str, object]], position: Vector2D, collision_shape_sprite: Sprite, game: Game) -> dict[str, object]:
    new_entity = create_2d_entity(parent, childs, position) | {EntityKeys.BOX: Box2D(IDSystem.next_id(), Transform2D(IDSystem.next_id(), Vector2D(100,100), Vector2D(0,0), Vector2D(1,1)))}
    add_entry_to_chace(game.chace, new_entity[EntityKeys.BOX].id, game.chace[collision_shape_sprite.id].get_rect())
    return new_entity