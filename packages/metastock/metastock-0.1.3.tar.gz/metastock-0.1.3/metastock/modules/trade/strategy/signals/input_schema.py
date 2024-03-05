SIGNAL_INPUT_SCHEMA_V1_NAME = '@signal/input/v1'
SIGNAL_INPUT_SCHEMA_V1 = {
        "type": "object",
        "properties": {
                "api": {
                        "type": "string",
                        "pattern": "^@signal/input/v.*$",
                        "description": "API endpoint"
                },
                "input": {}
        },
        "required": ["api", "input"]
}
