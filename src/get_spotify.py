import logging
import requests
import pandas as pd
from credentials import *
from datetime import datetime, timedelta


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
    logging.info("Token received")
    return token


def get_albums_releases(token: str, delta_days: int = 1, limit: int = 50) -> pd.DataFrame:

    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "country": "US",
        "limit": limit,
        "offset": 0,
    }
    response = requests.get(
        "https://api.spotify.com/v1/browse/new-releases",
        headers=headers,
        params=params
    )
    df_albums = pd.json_normalize(response.json()["albums"]["items"])
    df_albums = df_albums[
        (pd.to_datetime(df_albums["release_date"]).dt.date >= datetime.now().date() - timedelta(days=delta_days))
    ]["id"]

    logging.info(f"Received {len(df_albums)} lately released albums")
    return df_albums


def get_several_albums(token: str, ids: list) -> pd.DataFrame:

    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "ids": ",".join(ids)
    }
    response = requests.get(
        "https://api.spotify.com/v1/albums",
        headers=headers,
        params=params
    )
    
    df = pd.json_normalize(response.json()["albums"])
    
    df_albums = df[["id", "name", "release_date", "genres", "label"]]
    df_albums["artists_ids"] = df["artists"].apply(lambda artists_data: [artist["id"] for artist in artists_data])
    df_albums["tracks_ids"] = df["tracks.items"].apply(lambda tracks_data: [track["id"] for track in tracks_data])
    
    logging.info(f"Received data on {len(df_albums)} albums")
    return df_albums


def get_several_artists(token: str, ids: list) -> pd.DataFrame:

    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "ids": ','.join(ids)
    }
    response = requests.get(
        "https://api.spotify.com/v1/artists",
        headers=headers,
        params=params
    )
    
    df = pd.json_normalize(response.json()["artists"])
    df_artists = df[['id', 'name', 'genres', 'popularity']]
    
    return df_artists


def get_several_tracks(token: str, ids: list) -> pd.DataFrame:

    counter_from = 0
    counter_to = min(49, len(ids))

    df = pd.DataFrame()
    for i in range(int(len(ids) / counter_to) + 1):
        # print(f'{counter_from}:{counter_to}')
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "ids": ','.join(ids[counter_from:counter_to])
        }
        response = requests.get(
            "https://api.spotify.com/v1/tracks",
            headers=headers,
            params=params
        )
        
        df_iter = pd.json_normalize(response.json()["tracks"])
        df = pd.concat([df, df_iter], ignore_index=True)
        
        counter_from += 50
        counter_to += min(50, len(ids) - counter_to)

    df_tracks = df[["id", "name", "album.id", "duration_ms", "explicit", "popularity"]]
    df_tracks["artists_ids"] = df["artists"].apply(lambda artists_data: [artist["id"] for artist in artists_data])
    
    return df_tracks
