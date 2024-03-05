class DecideInfo:
    def __init__(
        self,
        open_pos: bool,
        message: str,
        min_open_pos: float = None,
        max_open_pos: float = None,
        priority: int = 1,
        code: str = "",
        meta=None,
    ):
        if meta is None:
            meta = {}
        self.max_open_pos = max_open_pos
        self.min_open_pos = min_open_pos
        self.open_pos = open_pos
        self.message = message
        self.priority = priority
        self.code = code
        self.meta = meta
