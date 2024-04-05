CREATE TABLE tracks
(
    id          INTEGER,
    name        VARCHAR(256),
    album_id    INT,
    duration_ms INTEGER,
    explicit    BOOLEAN,
    PRIMARY KEY(id)
)