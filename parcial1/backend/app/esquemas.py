from decimal import Decimal
from pydantic import BaseModel, Field


class CancionRespuesta(BaseModel):
    id_cancion: int
    nombre: str
    artista: str
    genero: str
    precio_unitario: Decimal


class CompraEntrada(BaseModel):
    id_cliente: int = Field(gt=0)
    id_cancion: int = Field(gt=0)


class CompraRespuesta(BaseModel):
    id_factura: int
    id_cliente: int
    id_cancion: int
    total: Decimal
    mensaje: str


class ClienteRespuesta(BaseModel):
    id_cliente: int
    nombre_completo: str
