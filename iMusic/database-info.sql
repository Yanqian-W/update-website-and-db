.headers on
.mode column

# 275 terms
CREATE TABLE [Artist]
(
    [ArtistId] INTEGER  NOT NULL,
    [Name] NVARCHAR(120),
    CONSTRAINT [PK_Artist] PRIMARY KEY  ([ArtistId])
);

# 25 terms
CREATE TABLE [Genre]
(
    [GenreId] INTEGER  NOT NULL,
    [Name] NVARCHAR(120),
    CONSTRAINT [PK_Genre] PRIMARY KEY  ([GenreId])
);

# 347 terms
CREATE TABLE IF NOT EXISTS "Album"
(
        [AlbumId] INTEGER  NOT NULL,
        [Title] NVARCHAR(160)  NOT NULL,
        [ArtistId] INTEGER  NOT NULL,
        CONSTRAINT [PK_Album] PRIMARY KEY  ([AlbumId]),
        FOREIGN KEY ([ArtistId]) REFERENCES [Artist] ([ArtistId])
                ON DELETE CASCADE ON UPDATE NO ACTION
);

# 3503 terms
CREATE TABLE IF NOT EXISTS "Track"
(
        [TrackId] INTEGER  NOT NULL,
        [Name] NVARCHAR(200)  NOT NULL,
        [AlbumId] INTEGER,
        [GenreId] INTEGER,
        [Composer] NVARCHAR(220),
        [Milliseconds] INTEGER  NOT NULL,
        [UnitPrice] NUMERIC(10,2)  NOT NULL,
        CONSTRAINT [PK_Track] PRIMARY KEY  ([TrackId]),
        FOREIGN KEY ([AlbumId]) REFERENCES [Album] ([AlbumId])
                ON DELETE CASCADE ON UPDATE NO ACTION,
        FOREIGN KEY ([GenreId]) REFERENCES [Genre] ([GenreId])
                ON DELETE CASCADE ON UPDATE NO ACTION
);


csv文件row：
{'genre_id': '1', 'genre_name': 'Rock'}
{'genre_id': '2', 'genre_name': 'Jazz'}
{'genre_id': '3', 'genre_name': 'Metal'}
{'genre_id': '4', 'genre_name': 'Alternative & Punk'}
{'genre_id': '5', 'genre_name': 'Rock And Roll'}
{'genre_id': '6', 'genre_name': 'Blues'}
{'genre_id': '7', 'genre_name': 'Latin'}
{'genre_id': '8', 'genre_name': 'Reggae'}
{'genre_id': '9', 'genre_name': 'Pop'}
{'genre_id': '10', 'genre_name': 'Soundtrack'}
{'genre_id': '11', 'genre_name': 'Bossa Nova'}
{'genre_id': '12', 'genre_name': 'Easy Listening'}
{'genre_id': '13', 'genre_name': 'Heavy Metal'}
{'genre_id': '14', 'genre_name': 'R&B/Soul'}
{'genre_id': '15', 'genre_name': 'Electronica/Dance'}
{'genre_id': '16', 'genre_name': 'World'}
{'genre_id': '17', 'genre_name': 'Hip Hop/Rap'}
{'genre_id': '18', 'genre_name': 'Science Fiction'}
{'genre_id': '19', 'genre_name': 'TV Shows'}
{'genre_id': '20', 'genre_name': 'Sci Fi & Fantasy'}
{'genre_id': '21', 'genre_name': 'Drama'}
{'genre_id': '22', 'genre_name': 'Comedy'}
{'genre_id': '23', 'genre_name': 'Alternative'}
{'genre_id': '24', 'genre_name': 'Classical'}
{'genre_id': '25', 'genre_name': 'Opera'}