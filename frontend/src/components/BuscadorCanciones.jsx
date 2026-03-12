import React from "react";

export default function BuscadorCanciones({ filtros, alCambiarFiltros, alBuscar, alLimpiar, cargando }) {
  function manejar_cambio(evento) {
    const { name, value } = evento.target;
    alCambiarFiltros((previo) => ({ ...previo, [name]: value }));
  }

  function manejar_envio(evento) {
    evento.preventDefault();
    alBuscar();
  }

  return (
    <form onSubmit={manejar_envio} className="tarjeta" aria-label="formulario-busqueda">
      <div className="cabecera-tarjeta">
        <h2>Buscador inteligente</h2>
        <span>Filtra por uno o varios campos</span>
      </div>

      <label>
        Cancion
        <input
          name="termino"
          value={filtros.termino}
          onChange={manejar_cambio}
          placeholder="Ej: Thunder"
          autoComplete="off"
        />
      </label>

      <label>
        Artista
        <input
          name="artista"
          value={filtros.artista}
          onChange={manejar_cambio}
          placeholder="Ej: AC/DC"
          autoComplete="off"
        />
      </label>

      <label>
        Genero
        <input
          name="genero"
          value={filtros.genero}
          onChange={manejar_cambio}
          placeholder="Ej: Rock"
          autoComplete="off"
        />
      </label>

      <div className="acciones-formulario">
        <button type="submit" disabled={cargando}>
          {cargando ? "Buscando..." : "Buscar"}
        </button>
        <button type="button" className="boton-secundario" onClick={alLimpiar}>
          Limpiar
        </button>
      </div>
    </form>
  );
}
