import warnings
from get_token import *
from get_albums_releases import *
from get_several_albums import *
from get_several_artists import *
from get_several_tracks import *

warnings.filterwarnings('ignore')

def main():
    token = get_token()
    
    # релизы
    released_albums_ids = get_albums_releases(token)
    
    # альбомы
    df_albums = get_several_albums(token, released_albums_ids)
    
    # артисты
    artists_ids = []
    for alist in df_albums['artists_ids']:
        artists_ids = artists_ids + alist
    df_artists = get_several_artists(token, artists_ids)
    
    print(df_artists.head())
    
    # треки
    tracks_ids = []
    for tlist in df_albums['tracks_ids']:
        tracks_ids = tracks_ids + tlist
    df_tracks = get_several_tracks(token, tracks_ids)
    
    print(df_tracks.head())

if __name__ == "__main__":
    main()