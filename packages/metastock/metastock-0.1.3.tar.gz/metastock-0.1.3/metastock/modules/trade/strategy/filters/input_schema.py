FILTER_INPUT_SCHEMA_V1_NAME = '@filter/input/v1'

FILTER_INPUT_SCHEMA_V1 = {
        "type": "object",
        "properties": {
                "api": {
                        "type": "string",
                        "pattern": "^@filter/input/v.*$",
                        "description": "API endpoint"
                },
                "input": {
                        "type": "object",
                }
        },
        "required": ["api", "input"]
}
