import json
import jsonschema

chapter = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "main": {
            "type": "object",
            "properties": {
                "description": {"type": ["string", "null"]},
                "equations": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "footer": {"type": ["object", "null"]}
    }
}

jsonschema.validate(
    instance={
        "title": "asdf",
        "main": {
            "description": "i am a description",
            "problems": ["a", "b", "c"]
        },
        "footer": None
    },
    schema=chapter
)
