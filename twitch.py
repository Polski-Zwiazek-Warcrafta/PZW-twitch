import asyncio
import websockets
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus
from db import join_lobby
from db import leave_lobby
from db import clear_lobby
from schema import lobby_schema

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")  # https://dev.twitch.tv/console/apps
OAUTH_TOKEN = os.getenv(
    "TWITCH_OAUTH_TOKEN")  # https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=CLIENT_ID&redirect_uri=http://localhost&scope=chat:read+chat:edit&state=JAKIS_TAM_STATE
USERNAME = os.getenv("TWITCH_USERNAME")  # App name from dev.twitch.tv/console/apps
CHANNEL = os.getenv("TWITCH_CHANNEL")  # "KroLu_"

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = quote_plus(os.getenv("DB_PASS"))
DB_HOST = os.getenv("DB_HOST")

MONGO_URI = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    if "lobby" not in db.list_collection_names():
        db.create_collection("lobby", validator=lobby_schema)
    print("✅ Successfully connected to the MongoDB database!")

except:
    print("❌ Failed to connect to MongoDB:")

if "lobby" not in db.list_collection_names():
    db.create_collection("lobby", validator=lobby_schema)


async def connect_to_twitch():
    uri = "wss://irc-ws.chat.twitch.tv:443"

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(f"PASS oauth:{OAUTH_TOKEN}")
            await websocket.send(f"NICK {USERNAME}")
            await websocket.send(f"JOIN #{CHANNEL}")

            print(f"Joined channel #{CHANNEL}...")

            while True:
                message = await websocket.recv()
                if "PRIVMSG" in message:  # We check the PRIVMSG in the message to make sure that we have just received a public message from the user, and not some other type of message. For example, an IRC server may also send other messages, such as error information, notifications that users have joined the channel, or system notifications.
                    parts = message.split(" :")
                    user_message = parts[1] if len(parts) > 1 else ""
                    username = message.split("!")[0][1:]

                    # COMMANDS
                    if user_message.lower().strip() == "!join":
                        joined = await join_lobby(db, username)  # add to db
                        if joined:
                            await send_message(websocket, f"Added {username} to lobby!")
                            print(f"Command '!join' triggered by {username}.")
                    if user_message.lower().strip() == "!leave":
                        left = await leave_lobby(db, username)  # remove from db
                        if left:
                            print(f"Command '!leave' triggered by {username}.")
                    if user_message.lower().strip() == "!clear" and username.lower() == CHANNEL.lower():
                        cleared = await clear_lobby(db)  # clear db
                        if cleared > 0:
                            print(f"Command '!clear' triggered by {username} cleared {cleared}.")
                else:
                    print(f"Received message: {message}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
        print("Attempting to reconnect...")
        await asyncio.sleep(5)
        await connect_to_twitch()


async def send_message(websocket, message):
    await websocket.send(f"PRIVMSG #{CHANNEL} :{message}")


if __name__ == "__main__":
    if not CLIENT_ID:
        print("TWITCH_CLIENT_ID is missing.")
    if not OAUTH_TOKEN:
        print("TWITCH_OAUTH_TOKEN is missing.")
    if not USERNAME:
        print("TWITCH_USERNAME is missing.")
    if not CHANNEL:
        print("TWITCH_CHANNEL is missing.")
    if not DB_NAME:
        print("DB_NAME is missing.")
    if not DB_HOST:
        print("DB_HOST is missing.")
    if not DB_PASS:
        print("DB_PASS is missing.")
    if not DB_USER:
        print("DB_USER is missing.")
    else:
        asyncio.run(connect_to_twitch())
