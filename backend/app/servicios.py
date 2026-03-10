from __future__ import annotations
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import modelos
from app.esquemas import CancionRespuesta, ClienteRespuesta, CompraRespuesta


def buscar_canciones(
    sesion: Session,
    termino: str | None = None,
    artista: str | None = None,
    genero: str | None = None,
) -> list[CancionRespuesta]:
    consulta = (
        select(modelos.Cancion, modelos.Artista, modelos.Genero)
        .join(modelos.Album, modelos.Cancion.id_album == modelos.Album.id_album)
        .join(modelos.Artista, modelos.Album.id_artista == modelos.Artista.id_artista)
        .join(modelos.Genero, modelos.Cancion.id_genero == modelos.Genero.id_genero)
    )

    if termino:
        consulta = consulta.where(modelos.Cancion.nombre.ilike(f"%{termino.strip()}%"))
    if artista:
        consulta = consulta.where(modelos.Artista.nombre.ilike(f"%{artista.strip()}%"))
    if genero:
        consulta = consulta.where(modelos.Genero.nombre.ilike(f"%{genero.strip()}%"))

    filas = sesion.execute(consulta.order_by(modelos.Cancion.nombre.asc())).all()
    return [
        CancionRespuesta(
            id_cancion=cancion.id_cancion,
            nombre=cancion.nombre,
            artista=artista_modelo.nombre,
            genero=genero_modelo.nombre,
            precio_unitario=cancion.precio_unitario,
        )
        for cancion, artista_modelo, genero_modelo in filas
    ]


def listar_clientes(sesion: Session, limite: int = 20) -> list[ClienteRespuesta]:
    clientes = (
        sesion.execute(select(modelos.Cliente).order_by(modelos.Cliente.id_cliente).limit(limite))
        .scalars()
        .all()
    )
    return [
        ClienteRespuesta(
            id_cliente=cliente.id_cliente,
            nombre_completo=f"{cliente.nombre} {cliente.apellido}",
        )
        for cliente in clientes
    ]


def comprar_cancion(
    sesion: Session,
    id_cliente: int,
    id_cancion: int,
) -> CompraRespuesta:
    cliente = sesion.get(modelos.Cliente, id_cliente)
    if not cliente:
        raise ValueError("El cliente no existe")

    cancion = sesion.get(modelos.Cancion, id_cancion)
    if not cancion:
        raise ValueError("La cancion no existe")

    factura = modelos.Factura(
        id_cliente=id_cliente,
        direccion=cliente.ciudad or "Sin direccion",
        ciudad=cliente.ciudad,
        pais=cliente.pais,
        total=Decimal(cancion.precio_unitario),
    )
    sesion.add(factura)
    sesion.flush()

    linea = modelos.LineaFactura(
        id_factura=factura.id_factura,
        id_cancion=id_cancion,
        precio_unitario=Decimal(cancion.precio_unitario),
        cantidad=1,
    )
    sesion.add(linea)
    sesion.commit()
    sesion.refresh(factura)

    return CompraRespuesta(
        id_factura=factura.id_factura,
        id_cliente=id_cliente,
        id_cancion=id_cancion,
        total=factura.total,
        mensaje="Compra registrada correctamente",
    )
