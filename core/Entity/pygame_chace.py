from pygame import Surface, Rect

def add_entry_to_chace(chace: dict[object, Surface|Rect], key_id: int, value: Surface|Rect) -> None:
     chace[key_id] = value

def remove_entry_from_chace(chace: dict[object, Surface|Rect], key_id: int) -> None:
     del chace[key_id]