-- Datos minimos para probar busqueda y compra.
INSERT INTO "Artist" ("ArtistId", "Name") OVERRIDING SYSTEM VALUE
VALUES (1, 'AC/DC')
ON CONFLICT ("ArtistId") DO NOTHING;

INSERT INTO "Album" ("AlbumId", "Title", "ArtistId") OVERRIDING SYSTEM VALUE
VALUES (1, 'For Those About To Rock', 1)
ON CONFLICT ("AlbumId") DO NOTHING;

INSERT INTO "Genre" ("GenreId", "Name") OVERRIDING SYSTEM VALUE
VALUES (1, 'Rock')
ON CONFLICT ("GenreId") DO NOTHING;

INSERT INTO "MediaType" ("MediaTypeId", "Name") OVERRIDING SYSTEM VALUE
VALUES (1, 'MPEG audio file')
ON CONFLICT ("MediaTypeId") DO NOTHING;

INSERT INTO "Track" (
  "TrackId", "Name", "AlbumId", "MediaTypeId", "GenreId", "Composer", "Milliseconds", "Bytes", "UnitPrice"
) OVERRIDING SYSTEM VALUE
VALUES (
  1, 'For Those About To Rock (We Salute You)', 1, 1, 1, 'Angus Young', 343719, 11170334, 0.99
)
ON CONFLICT ("TrackId") DO NOTHING;

INSERT INTO "Customer" (
  "CustomerId", "FirstName", "LastName", "City", "Country", "Email"
) OVERRIDING SYSTEM VALUE
VALUES (
  1, 'Luis', 'Gonzalez', 'Bogota', 'Colombia', 'luis@example.com'
)
ON CONFLICT ("CustomerId") DO NOTHING;
