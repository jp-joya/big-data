import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.main import salud, api_buscar_canciones, api_comprar, api_clientes
from app.esquemas import CompraEntrada


def test_salud():
    respuesta = salud()

    assert respuesta["estado"] == "ok"


def test_api_clientes(sesion_prueba: Session):
    respuesta = api_clientes(limite=10, sesion=sesion_prueba)

    assert len(respuesta) == 1
    assert respuesta[0].nombre_completo == "Ana Lopez"


def test_api_busqueda_canciones(sesion_prueba: Session):
    respuesta = api_buscar_canciones(termino="Thunder", artista=None, genero=None, sesion=sesion_prueba)

    assert len(respuesta) == 1
    assert respuesta[0].nombre == "Thunderstruck"


def test_api_compra_cliente_no_existe(sesion_prueba: Session):
    with pytest.raises(HTTPException) as error:
        api_comprar(CompraEntrada(id_cliente=999, id_cancion=1), sesion=sesion_prueba)

    assert error.value.status_code == 404
