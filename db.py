from datetime import datetime

async def join_lobby(db, username):
    lobby_collection = db["lobby"]
    lobby_user_data = {
        "username": username,
        "is_playing": False,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    lobby_collection.insert_one(lobby_user_data)
    return True

async def leave_lobby(db, username):
    lobby_collection = db["lobby"]
    result = lobby_collection.update_one(
        {"username": username},  # filter: find user by name
        {
            "$set": {
                "is_playing": False,
                "updatedAt": datetime.utcnow(),
                "deletedAt": datetime.utcnow()
            }
        }
    )
    return result.modified_count > 0  # returns true if something modified

async def clear_lobby(db):
    lobby_collection = db["lobby"]
    result = lobby_collection.delete_many({})
    return result.deleted_count