from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import modelos
from app.servicios import buscar_canciones, comprar_cancion, listar_clientes


def test_buscar_canciones_por_termino(sesion_prueba: Session):
    canciones = buscar_canciones(sesion_prueba, termino="Thunder")

    assert len(canciones) == 1
    assert canciones[0].nombre == "Thunderstruck"
    assert canciones[0].artista == "AC/DC"


def test_listar_clientes(sesion_prueba: Session):
    clientes = listar_clientes(sesion_prueba, limite=5)

    assert len(clientes) == 1
    assert clientes[0].nombre_completo == "Ana Lopez"


def test_comprar_cancion_crea_factura(sesion_prueba: Session):
    respuesta = comprar_cancion(sesion_prueba, id_cliente=1, id_cancion=1)

    assert respuesta.total == Decimal("0.99")

    factura = sesion_prueba.execute(select(modelos.Factura)).scalar_one()
    assert factura.id_cliente == 1

    linea = sesion_prueba.execute(select(modelos.LineaFactura)).scalar_one()
    assert linea.id_cancion == 1


def test_comprar_cliente_invalido(sesion_prueba: Session):
    with pytest.raises(ValueError, match="cliente"):
        comprar_cancion(sesion_prueba, id_cliente=999, id_cancion=1)
