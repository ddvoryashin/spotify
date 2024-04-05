CREATE TABLE tracks_artists
(
    track_id    INTEGER,
    artist_id   INTEGER,
    CONSTRAINT fk_tracks_artists_albums
      FOREIGN KEY(track_id) 
        REFERENCES tracks(id),
    CONSTRAINT fk_tracks_artists_artists
      FOREIGN KEY(artist_id) 
        REFERENCES artists(id)
)