from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import modelos


def poblar_datos_minimos(sesion: Session) -> None:
    existe_artista = sesion.execute(select(modelos.Artista.id_artista).limit(1)).first()
    if existe_artista:
        return

    artista = modelos.Artista(nombre="AC/DC")
    album = modelos.Album(titulo="For Those About To Rock", artista=artista)
    genero = modelos.Genero(nombre="Rock")
    tipo_media = modelos.TipoMedia(nombre="MPEG audio file")
    cancion = modelos.Cancion(
        nombre="For Those About To Rock (We Salute You)",
        album=album,
        tipo_media=tipo_media,
        genero=genero,
        compositor="Angus Young",
        milisegundos=343719,
        bytes=11170334,
        precio_unitario=Decimal("0.99"),
    )
    cliente = modelos.Cliente(
        nombre="Luis",
        apellido="Gonzalez",
        ciudad="Bogota",
        pais="Colombia",
        correo="luis@example.com",
    )

    sesion.add_all([artista, album, genero, tipo_media, cancion, cliente])
    sesion.commit()
