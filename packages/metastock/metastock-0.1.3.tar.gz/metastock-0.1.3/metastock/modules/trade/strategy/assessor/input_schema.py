ACCESSOR_INPUT_SCHEMA_V1_NAME = "@accessor/input/v1"

ACCESSOR_INPUT_SCHEMA_V1 = {
    "type": "object",
    "properties": {
        "api": {
            "type": "string",
            "pattern": "^@accessor/input/v.*$",
            "description": "",
        },
        "input": {
            "type": "object",
        },
    },
    "required": ["api", "input"],
}
