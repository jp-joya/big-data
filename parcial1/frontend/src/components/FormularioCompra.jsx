import React, { useMemo, useState } from "react";

function validar_compra(id_cliente, id_cancion) {
  if (!id_cliente) return "Debes seleccionar un cliente";
  if (!id_cancion) return "Debes seleccionar una cancion";
  return null;
}

export default function FormularioCompra({ clientes, canciones, alComprar, cargando }) {
  const [idCliente, setIdCliente] = useState("");
  const [idCancion, setIdCancion] = useState("");
  const [errorLocal, setErrorLocal] = useState("");

  const botonDeshabilitado = useMemo(() => cargando, [cargando]);

  async function enviar_compra(evento) {
    evento.preventDefault();
    const error = validar_compra(idCliente, idCancion);
    if (error) {
      setErrorLocal(error);
      return;
    }

    setErrorLocal("");
    await alComprar({ id_cliente: Number(idCliente), id_cancion: Number(idCancion) });
  }

  return (
    <form onSubmit={enviar_compra} className="tarjeta" aria-label="formulario-compra">
      <h2>Comprar cancion</h2>
      <label>
        Cliente
        <select value={idCliente} onChange={(e) => setIdCliente(e.target.value)}>
          <option value="">Seleccione cliente</option>
          {clientes.map((cliente) => (
            <option key={cliente.id_cliente} value={cliente.id_cliente}>
              {cliente.nombre_completo}
            </option>
          ))}
        </select>
      </label>
      <label>
        Cancion
        <select value={idCancion} onChange={(e) => setIdCancion(e.target.value)}>
          <option value="">Seleccione cancion</option>
          {canciones.map((cancion) => (
            <option key={cancion.id_cancion} value={cancion.id_cancion}>
              {cancion.nombre} - {cancion.artista}
            </option>
          ))}
        </select>
      </label>
      {errorLocal ? <p className="alerta error">{errorLocal}</p> : null}
      <button type="submit" disabled={botonDeshabilitado}>
        {cargando ? "Procesando..." : "Comprar"}
      </button>
    </form>
  );
}
