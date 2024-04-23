from get_spotify import *
from db_loader import *


# get token for API requests
TOKEN = get_token()

# get album releases for previous day. you can set every other date
df_albums_releases = get_albums_releases(
    token=TOKEN,
    dt_from=datetime.strptime('2023-01-01', '%Y-%m-%d')
)

# get albums data
df_albums = get_several_albums(
    token=TOKEN,
    ids=list(df_albums_releases["id"])
)

# rename column id to spotify_id
df_albums["spotify_id"] = df_albums["id"]
df_albums = df_albums[["spotify_id", "name", "release_date", "genres", "label"]]

# load albums data to db
merge_values(
    df=df_albums,
    join_field="spotify_id",
    table="albums"
)
