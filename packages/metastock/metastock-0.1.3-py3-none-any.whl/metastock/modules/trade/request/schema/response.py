GET_STRATEGY_PROCESS_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "input": {
            "type": "object",
            "properties": {
                "range": {
                    "type": "object",
                    "properties": {"to": {}, "from": {}, "type": {"type": "string"}},
                    "required": ["from", "type"],
                },
                "action": {"type": "object", "properties": {"buy": {}, "sell": {}}},
                "filter": {},
                "signal": {},
            },
        },
        "from": {"type": "string"},
        "to": {"type": "string"},
        "hash": {"type": "string"},
        "meta": {"type": ["object", "null"]},
        "state": {"type": "integer"},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
        "trading_strategy_process": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "meta": {"type": ["object", "null"]},
                    "state": {"type": "integer"},
                    "created_at": {"type": "string"},
                    "updated_at": {"type": "string"},
                },
                "required": ["symbol", "state", "created_at", "updated_at"],
            },
        },
    },
    "required": [
        "name",
        "input",
        "from",
        "to",
        "hash",
        "state",
        "created_at",
        "updated_at",
        "trading_strategy_process",
    ],
}
