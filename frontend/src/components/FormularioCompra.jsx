import React from "react";

export default function FormularioCompra({
  clientes,
  carrito,
  idClienteSeleccionado,
  total,
  cargando,
  onCambiarCliente,
  onCambiarCantidad,
  onQuitarDelCarrito,
  onVaciarCarrito,
  onComprarCarrito,
  formatoPrecio
}) {
  return (
    <section className="tarjeta" aria-label="panel-carrito">
      <div className="cabecera-tarjeta">
        <h2>Carrito de compra</h2>
        <span>{carrito.length} cancion(es) distinta(s)</span>
      </div>

      <label>
        Cliente para facturar
        <select value={idClienteSeleccionado} onChange={(e) => onCambiarCliente(e.target.value)}>
          <option value="">Seleccione cliente</option>
          {clientes.map((cliente) => (
            <option key={cliente.id_cliente} value={cliente.id_cliente}>
              {cliente.nombre_completo}
            </option>
          ))}
        </select>
      </label>

      <div className="lista-carrito" aria-live="polite">
        {carrito.length === 0 ? (
          <p className="carrito-vacio">Aun no has agregado canciones.</p>
        ) : (
          carrito.map((item) => (
            <article key={item.id_cancion} className="item-carrito">
              <div>
                <strong>{item.nombre}</strong>
                <p>{item.artista}</p>
              </div>

              <div className="controles-cantidad">
                <button
                  type="button"
                  className="boton-icono"
                  onClick={() => onCambiarCantidad(item.id_cancion, -1)}
                  aria-label={`Disminuir cantidad de ${item.nombre}`}
                >
                  -
                </button>
                <span>{item.cantidad}</span>
                <button
                  type="button"
                  className="boton-icono"
                  onClick={() => onCambiarCantidad(item.id_cancion, 1)}
                  aria-label={`Aumentar cantidad de ${item.nombre}`}
                >
                  +
                </button>
              </div>

              <div className="item-total">
                <strong>{formatoPrecio(item.precio_unitario * item.cantidad)}</strong>
                <button
                  type="button"
                  className="boton-texto"
                  onClick={() => onQuitarDelCarrito(item.id_cancion)}
                >
                  Quitar
                </button>
              </div>
            </article>
          ))
        )}
      </div>

      <footer className="resumen-carrito">
        <div>
          <span>Total</span>
          <strong>{formatoPrecio(total)}</strong>
        </div>
        <div className="acciones-formulario">
          <button type="button" className="boton-secundario" onClick={onVaciarCarrito}>
            Vaciar
          </button>
          <button type="button" onClick={onComprarCarrito} disabled={cargando}>
            {cargando ? "Confirmando..." : "Comprar carrito"}
          </button>
        </div>
      </footer>
    </section>
  );
}
