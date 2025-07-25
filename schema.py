# schema.py

# Schema for players in the lobby
lobby_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "Twitch username, required"
            },
            "is_playing": {
                "bsonType": "bool",
                "description": "Indicates if the user has been selected to be playing, defaults to false"
            },
            "createdAt": {
                "bsonType": ["date", "null"],
                "description": "Timestamp of creation"
            },
            "updatedAt": {
                "bsonType": ["date", "null"],
                "description": "Timestamp of last update"
            },
            "deletedAt": {
                "bsonType": ["date", "null"],
                "description": "Timestamp of deletion (nullable)"
            }
        }
    }
}

# Schema for lobby configuration
lobby_config_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "properties": {
            "is_open": {
                "bsonType": "bool",
                "description": "Indicates if the lobby is open"
            }
        }
    }
}
