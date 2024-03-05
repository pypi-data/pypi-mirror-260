from metastock.modules.trade.strategy.actions.input_schema import ACTION_INPUT_SCHEMA_V1
from metastock.modules.trade.strategy.filters.input_schema import FILTER_INPUT_SCHEMA_V1
from metastock.modules.trade.strategy.signals.input_schema import SIGNAL_INPUT_SCHEMA_V1

STRATEGY_INPUT_SCHEMA_V1_NAME = "@predefined_input/strategy/v1"

STRATEGY_INPUT_SCHEMA_V1 = {
    "type": "object",
    "properties": {
        "api": {
            "type": "string",
            "pattern": "^@predefined_input/strategy/v.*$",
            "description": "API endpoint",
        },
        "name": {"type": "string", "description": "Strategy Input name"},
        "input": {
            "type": "object",
            "properties": {
                "range": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["relative", "absolute"]},
                        "from": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "modify": {"type": "string", "enum": ["shift"]},
                                        "amount": {"type": ["string", "number"]},
                                        "amount_type": {
                                            "type": "string",
                                            "enum": ["years", "months"],
                                        },
                                    },
                                    "required": ["modify", "amount", "amount_type"],
                                },
                                {"type": "string"},
                            ]
                        },
                        "to": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "modify": {"type": "string", "enum": ["shift"]},
                                        "amount": {"type": ["string", "number"]},
                                        "amount_type": {
                                            "type": "string",
                                            "enum": ["years", "months"],
                                        },
                                    },
                                    "required": ["modify", "amount", "amount_type"],
                                },
                                {"type": "string"},
                            ]
                        },
                    },
                    "required": ["type", "from"],
                },
                "filter": {
                    "type": "object",
                    "properties": {
                        "filters": {"type": "array", "items": {"type": "string"}},
                        "input": FILTER_INPUT_SCHEMA_V1,
                    },
                },
                "signal": {
                    "type": "object",
                    "properties": {
                        "signals": {"type": "array", "items": {"type": "string"}},
                        "input": SIGNAL_INPUT_SCHEMA_V1,
                    },
                },
                "action": {
                    "type": "object",
                    "properties": {
                        "actions": {"type": "array", "items": {"type": "string"}},
                        "input": ACTION_INPUT_SCHEMA_V1,
                    },
                },
            },
            "required": ["range", "filter", "signal", "action"],
        },
    },
    "required": ["api", "name", "input"],
}
