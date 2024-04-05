import requests
from credentials import *

def get_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "scope": "user-top-read",
    }
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        params=params
    )
    token = response.json()['access_token']
    return token