from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.configuracion import obtener_configuracion


configuracion = obtener_configuracion()
es_sqlite = configuracion.url_base_datos.startswith("sqlite")

argumentos_motor = {"check_same_thread": False} if es_sqlite else {}

motor = create_engine(configuracion.url_base_datos, connect_args=argumentos_motor)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)


def obtener_sesion() -> Generator[Session, None, None]:
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
