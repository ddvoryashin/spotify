CREATE TABLE albums
(
	id              SERIAL,
    spotify_id      VARCHAR(22),
    name            VARCHAR(256),
    release_date    DATE,
    genres          VARCHAR(256),
    label           VARCHAR(128),
    PRIMARY KEY(id)
);