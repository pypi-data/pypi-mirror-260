ACTION_INPUT_SCHEMA_V1_NAME = '@action/input/v1'

ACTION_INPUT_SCHEMA_V1 = {
        "type": "object",
        "properties": {
                "api": {
                        "type": "string",
                        "pattern": "^@action/input/v.*$",
                        "description": "API endpoint"
                },
                "input": {
                        "type": "object",
                        "properties": {
                                "buy": {},
                                "sell": {},
                                "alert": {}
                        }
                }
        },
        "required": ["api", "input"]
}
