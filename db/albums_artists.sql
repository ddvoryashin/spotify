CREATE TABLE albums_artists
(
    album_id    INTEGER,
    artist_id   INTEGER,
    CONSTRAINT fk_albums_artists_albums
      FOREIGN KEY(album_id) 
        REFERENCES albums(id),
    CONSTRAINT fk_albums_artists_artist
      FOREIGN KEY(artist_id) 
        REFERENCES artists(id)
)