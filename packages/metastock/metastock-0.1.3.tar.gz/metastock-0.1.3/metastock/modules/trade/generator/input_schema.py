PRE_DEFINED_INPUT_SCHEMA_V1 = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
                "api": {"type": "string"},
                "strategy": {
                        "type": "object",
                        "properties": {
                                "name": {"type": "string"},
                                "input": {
                                        "type": "object",
                                        "properties": {
                                                "type": {
                                                        "type": "string",
                                                        "enum": ["files"]
                                                },
                                                "data": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                }
                                        },
                                        "required": ["type", "data"]
                                }
                        },
                        "required": ["name", "input"]
                }
        },
        "required": ["strategy"]
}
