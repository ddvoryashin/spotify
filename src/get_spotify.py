import logging
import requests
import pandas as pd
from credentials import *
from datetime import datetime, date, timedelta


# TODO: fix logging
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


def get_albums_releases(
    token: str,
    dt_from: datetime = datetime.today() - timedelta(days = 1),
    limit: int = 50
) -> pd.DataFrame:
    """
    Get latest releases. Spotify can't give more than 100 latest albums
    """
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "country": "US",
        "limit": limit,
        "offset": 0,
    }
    # add try-except so it would load maximum amount of albums that Spotify can give
    # currently it's 100
    try:
        i = 0
        df_albums = pd.DataFrame()
        print("Requesting albums released lately...")
        # max 100 iterations because maximum 50*10=500 releases seems like enough
        while i < 10:
            params["offset"] = max(limit * i, 0)
            response = requests.get(
                "https://api.spotify.com/v1/browse/new-releases",
                headers=headers,
                params=params
            )
            df_response = pd.json_normalize(response.json()["albums"]["items"])
            df_albums = pd.concat(
                [
                    df_albums,
                    df_response[
                        (pd.to_datetime(df_response["release_date"]).dt.date >= dt_from.date())
                    ][["id", "release_date"]]
                ]
            )
            i+=1
    except Exception as e:
        print(e)

    print(f"Received {len(df_albums)} lately released albums")
    return df_albums


def get_several_albums(token: str, ids: list) -> pd.DataFrame:
    """
    Get albums data
    """
    
    df_albums = pd.DataFrame()
    print("Requesting data on albums released lately...")
    # 20 albums max can be requested at a time
    for i in range(int(len(ids) / 20) + 1):
        print(f"iteration {i}; {len(ids[i*20:(i+1)*20])} ids requested")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "ids": ",".join(ids[i*20:(i+1)*20])
        }
        response = requests.get(
            "https://api.spotify.com/v1/albums",
            headers=headers,
            params=params
        )
        
        try:
            df_response = pd.json_normalize(response.json()["albums"])
            df_append = df_response.loc[:, ["id", "name", "release_date", "genres", "label"]]
            df_append["artists_ids"] = df_response.loc[:, "artists"].apply(
                lambda artists_data: [artist["id"] for artist in artists_data]
            )
            df_append["tracks_ids"] = df_response.loc[:, "tracks.items"].apply(
                lambda tracks_data: [track["id"] for track in tracks_data]
            )
            df_albums = pd.concat([df_albums, df_append])
        except KeyError as e:
            print(e)
    print("Data on albums received")
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
