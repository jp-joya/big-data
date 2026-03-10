import React, { useState } from "react";

export default function BuscadorCanciones({ alBuscar }) {
  const [filtros, setFiltros] = useState({ termino: "", artista: "", genero: "" });

  function manejar_cambio(evento) {
    const { name, value } = evento.target;
    setFiltros((previo) => ({ ...previo, [name]: value }));
  }

  function manejar_envio(evento) {
    evento.preventDefault();
    alBuscar(filtros);
  }

  return (
    <form onSubmit={manejar_envio} className="tarjeta" aria-label="formulario-busqueda">
      <h2>Buscar canciones</h2>
      <label>
        Cancion
        <input
          name="termino"
          value={filtros.termino}
          onChange={manejar_cambio}
          placeholder="Ej: Thunder"
        />
      </label>
      <label>
        Artista
        <input name="artista" value={filtros.artista} onChange={manejar_cambio} />
      </label>
      <label>
        Genero
        <input name="genero" value={filtros.genero} onChange={manejar_cambio} />
      </label>
      <button type="submit">Buscar</button>
    </form>
  );
}
