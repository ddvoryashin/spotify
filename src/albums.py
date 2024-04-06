from get_spotify import *
from db_loader import *


# get token for further API requests
TOKEN = get_token()

# get album releases for previous day
df_albums_releases = get_albums_releases(
    token=TOKEN,
    delta_days=300
)

# TODO: write cycle in case there are more than 20 albums
# get albums data
df_albums = get_several_albums(
    token=TOKEN,
    ids=list(df_albums_releases)[:20]
)

# rename column id to spotify_id
df_albums["spotify_id"] = df_albums["id"]
df_albums = df_albums[["spotify_id", "name", "release_date", "genres", "label"]]

# TODO: check double data
# load albums data to db
insert_values(
    df=df_albums,
    table="albums"
)
