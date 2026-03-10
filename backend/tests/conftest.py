from collections.abc import Generator
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.base import Base
from app import modelos


@pytest.fixture()
def engine_prueba():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    SesionPrueba = sessionmaker(bind=engine)
    with SesionPrueba() as sesion:
        sesion.add_all(
            [
                modelos.Artista(nombre="AC/DC"),
                modelos.Genero(nombre="Rock"),
                modelos.TipoMedia(nombre="MP3"),
            ]
        )
        sesion.flush()

        album = modelos.Album(titulo="Album", id_artista=1)
        sesion.add(album)
        sesion.flush()

        sesion.add(
            modelos.Cancion(
                nombre="Thunderstruck",
                id_album=album.id_album,
                id_tipo_media=1,
                id_genero=1,
                compositor="AC/DC",
                milisegundos=1000,
                bytes=1200,
                precio_unitario=Decimal("0.99"),
            )
        )

        sesion.add(
            modelos.Cliente(
                nombre="Ana",
                apellido="Lopez",
                ciudad="Bogota",
                pais="Colombia",
                correo="ana@example.com",
            )
        )
        sesion.commit()

    yield engine
    engine.dispose()


@pytest.fixture()
def sesion_prueba(engine_prueba) -> Generator[Session, None, None]:
    SesionPrueba = sessionmaker(bind=engine_prueba)
    sesion = SesionPrueba()
    try:
        yield sesion
    finally:
        sesion.close()
