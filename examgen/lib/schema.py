import json
import jsonschema

chapter = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "vspace": {"type": "integer"},
        "main": {
            "type": "object",
            "properties": {
                "description": {"type": ["string", "null"]},
                "parts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "eq": {"type": "string"},
                            "vspace": {"type": ["integer", "null"]}
                        }
                    }
                }
            }
        },
        "footer": {"type": ["object", "null"]}
    }
}
