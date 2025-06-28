# PZW-twitch

Create virtual env
```
python -m venv ./venv
```

Use new virtual env
```
source venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```


Create .env file, insert values:
```
DB_NAME=
DB_USER=
DB_PASS=
DB_HOST=
TWITCH_USERNAME=
TWITCH_CLIENT_ID=
TWITCH_OAUTH_TOKEN=
TWITCH_CHANNEL=
TWITCH_LOBBY_REFRESH=
```
where
TWITCH_CLIENT_ID get from https://dev.twitch.tv/console/apps
TWITCH_OAUTH_TOKEN get from https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=CLIENT_ID&redirect_uri=http://localhost&scope=chat:read+chat:edit&state=JAKIS_TAM_STATE
TWITCH_USERNAME get from app name from dev.twitch.tv/console/apps
TWITCH_CHANNEL get from twitch channel name, example: KroLu_
DB values get from DB settings
