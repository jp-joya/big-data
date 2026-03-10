from __future__ import annotations
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.base import Base
from app.base_datos import motor, obtener_sesion, SesionLocal
from app.esquemas import CancionRespuesta, ClienteRespuesta, CompraEntrada, CompraRespuesta
from app.semilla import poblar_datos_minimos
from app.servicios import buscar_canciones, comprar_cancion, listar_clientes

app = FastAPI(title="bnd-test-chinook-api", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def al_iniciar() -> None:
    # Crea tablas al iniciar para facilitar la prueba local y en EC2.
    Base.metadata.create_all(bind=motor)
    with SesionLocal() as sesion:
        poblar_datos_minimos(sesion)


@app.get("/api/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}


@app.get("/api/clientes", response_model=list[ClienteRespuesta])
def api_clientes(
    limite: int = Query(default=20, ge=1, le=100),
    sesion: Session = Depends(obtener_sesion),
) -> list[ClienteRespuesta]:
    return listar_clientes(sesion, limite=limite)


@app.get("/api/canciones", response_model=list[CancionRespuesta])
def api_buscar_canciones(
    termino: Optional[str] = Query(default=None, min_length=1),
    artista: Optional[str] = Query(default=None, min_length=1),
    genero: Optional[str] = Query(default=None, min_length=1),
    sesion: Session = Depends(obtener_sesion),
) -> list[CancionRespuesta]:
    return buscar_canciones(sesion, termino=termino, artista=artista, genero=genero)


@app.post("/api/compras", response_model=CompraRespuesta)
def api_comprar(
    datos: CompraEntrada,
    sesion: Session = Depends(obtener_sesion),
) -> CompraRespuesta:
    try:
        return comprar_cancion(
            sesion,
            id_cliente=datos.id_cliente,
            id_cancion=datos.id_cancion,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
