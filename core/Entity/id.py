class IDSystem:
    _current_id = 0

    @classmethod
    def next_id(cls) -> int:
        return_id = cls._current_id
        cls._current_id += 1
        return return_id