from functools import lru_cache
from pydantic import BaseModel
import os


class Configuracion(BaseModel):
    url_base_datos: str = os.getenv(
        "DATABASE_URL", "sqlite:///./chinook_local.db"
    )


@lru_cache
def obtener_configuracion() -> Configuracion:
    return Configuracion()
