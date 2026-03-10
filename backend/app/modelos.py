from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base


class Artista(Base):
    __tablename__ = "Artist"

    id_artista: Mapped[int] = mapped_column("ArtistId", Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column("Name", String(120), nullable=False)

    albumes: Mapped[list["Album"]] = relationship(back_populates="artista")


class Album(Base):
    __tablename__ = "Album"

    id_album: Mapped[int] = mapped_column("AlbumId", Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column("Title", String(160), nullable=False)
    id_artista: Mapped[int] = mapped_column(
        "ArtistId", ForeignKey("Artist.ArtistId"), nullable=False
    )

    artista: Mapped[Artista] = relationship(back_populates="albumes")
    canciones: Mapped[list["Cancion"]] = relationship(back_populates="album")


class Genero(Base):
    __tablename__ = "Genre"

    id_genero: Mapped[int] = mapped_column("GenreId", Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column("Name", String(120), nullable=False)

    canciones: Mapped[list["Cancion"]] = relationship(back_populates="genero")


class TipoMedia(Base):
    __tablename__ = "MediaType"

    id_tipo_media: Mapped[int] = mapped_column("MediaTypeId", Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column("Name", String(120), nullable=False)

    canciones: Mapped[list["Cancion"]] = relationship(back_populates="tipo_media")


class Cancion(Base):
    __tablename__ = "Track"

    id_cancion: Mapped[int] = mapped_column("TrackId", Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column("Name", String(200), nullable=False)
    id_album: Mapped[int] = mapped_column("AlbumId", ForeignKey("Album.AlbumId"), nullable=False)
    id_tipo_media: Mapped[int] = mapped_column(
        "MediaTypeId", ForeignKey("MediaType.MediaTypeId"), nullable=False
    )
    id_genero: Mapped[int | None] = mapped_column(
        "GenreId", ForeignKey("Genre.GenreId"), nullable=True
    )
    compositor: Mapped[str | None] = mapped_column("Composer", String(220), nullable=True)
    milisegundos: Mapped[int] = mapped_column("Milliseconds", Integer, nullable=False)
    bytes: Mapped[int | None] = mapped_column("Bytes", Integer, nullable=True)
    precio_unitario: Mapped[Decimal] = mapped_column(
        "UnitPrice", Numeric(10, 2), nullable=False
    )

    album: Mapped[Album] = relationship(back_populates="canciones")
    genero: Mapped[Genero | None] = relationship(back_populates="canciones")
    tipo_media: Mapped[TipoMedia] = relationship(back_populates="canciones")


class Cliente(Base):
    __tablename__ = "Customer"

    id_cliente: Mapped[int] = mapped_column("CustomerId", Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column("FirstName", String(40), nullable=False)
    apellido: Mapped[str] = mapped_column("LastName", String(20), nullable=False)
    ciudad: Mapped[str | None] = mapped_column("City", String(40), nullable=True)
    pais: Mapped[str | None] = mapped_column("Country", String(40), nullable=True)
    correo: Mapped[str | None] = mapped_column("Email", String(60), nullable=True)

    facturas: Mapped[list["Factura"]] = relationship(back_populates="cliente")


class Factura(Base):
    __tablename__ = "Invoice"

    id_factura: Mapped[int] = mapped_column("InvoiceId", Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(
        "CustomerId", ForeignKey("Customer.CustomerId"), nullable=False
    )
    fecha_factura: Mapped[datetime] = mapped_column(
        "InvoiceDate", DateTime, default=datetime.utcnow, nullable=False
    )
    direccion: Mapped[str | None] = mapped_column("BillingAddress", String(70), nullable=True)
    ciudad: Mapped[str | None] = mapped_column("BillingCity", String(40), nullable=True)
    pais: Mapped[str | None] = mapped_column("BillingCountry", String(40), nullable=True)
    total: Mapped[Decimal] = mapped_column("Total", Numeric(10, 2), nullable=False)

    cliente: Mapped[Cliente] = relationship(back_populates="facturas")
    lineas: Mapped[list["LineaFactura"]] = relationship(back_populates="factura")


class LineaFactura(Base):
    __tablename__ = "InvoiceLine"

    id_linea_factura: Mapped[int] = mapped_column(
        "InvoiceLineId", Integer, primary_key=True
    )
    id_factura: Mapped[int] = mapped_column(
        "InvoiceId", ForeignKey("Invoice.InvoiceId"), nullable=False
    )
    id_cancion: Mapped[int] = mapped_column(
        "TrackId", ForeignKey("Track.TrackId"), nullable=False
    )
    precio_unitario: Mapped[Decimal] = mapped_column(
        "UnitPrice", Numeric(10, 2), nullable=False
    )
    cantidad: Mapped[int] = mapped_column("Quantity", Integer, nullable=False)

    factura: Mapped[Factura] = relationship(back_populates="lineas")
