import React, { useEffect, useMemo, useState } from "react";
import BuscadorCanciones from "./components/BuscadorCanciones";
import FormularioCompra from "./components/FormularioCompra";
import { buscar_canciones, comprar_cancion, obtener_clientes } from "./services/api";

function normalizar_precio(valor) {
  const numero = Number(valor);
  if (Number.isNaN(numero)) return 0;
  return numero;
}

function formato_precio(valor) {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2
  }).format(valor);
}

export default function App() {
  const [clientes, setClientes] = useState([]);
  const [canciones, setCanciones] = useState([]);
  const [filtros, setFiltros] = useState({ termino: "", artista: "", genero: "" });
  const [carrito, setCarrito] = useState([]);
  const [idClienteSeleccionado, setIdClienteSeleccionado] = useState("");
  const [notificacion, setNotificacion] = useState(null);
  const [cargandoBusqueda, setCargandoBusqueda] = useState(false);
  const [cargandoCompra, setCargandoCompra] = useState(false);

  useEffect(() => {
    cargar_clientes();
    ejecutar_busqueda({});
  }, []);

  const totalCarrito = useMemo(
    () => carrito.reduce((acum, item) => acum + item.precio_unitario * item.cantidad, 0),
    [carrito]
  );

  const totalItems = useMemo(
    () => carrito.reduce((acum, item) => acum + item.cantidad, 0),
    [carrito]
  );

  function mostrar_exito(texto) {
    setNotificacion({ tipo: "exito", texto });
  }

  function mostrar_error(texto) {
    setNotificacion({ tipo: "error", texto });
  }

  async function cargar_clientes() {
    try {
      const data = await obtener_clientes();
      setClientes(data);
    } catch (err) {
      mostrar_error(err.message);
    }
  }

  async function ejecutar_busqueda(filtrosBusqueda) {
    try {
      setCargandoBusqueda(true);
      const data = await buscar_canciones(filtrosBusqueda);
      setCanciones(data);
      if (data.length === 0) {
        mostrar_error("No encontramos canciones para esos filtros. Prueba otra combinacion.");
      } else {
        setNotificacion(null);
      }
    } catch (err) {
      mostrar_error(err.message);
    } finally {
      setCargandoBusqueda(false);
    }
  }

  function manejar_busqueda() {
    ejecutar_busqueda(filtros);
  }

  function limpiar_filtros() {
    const vacio = { termino: "", artista: "", genero: "" };
    setFiltros(vacio);
    ejecutar_busqueda(vacio);
  }

  function agregar_al_carrito(cancion) {
    setCarrito((previo) => {
      const indice = previo.findIndex((item) => item.id_cancion === cancion.id_cancion);
      if (indice >= 0) {
        return previo.map((item, i) =>
          i === indice ? { ...item, cantidad: item.cantidad + 1 } : item
        );
      }

      return [
        ...previo,
        {
          id_cancion: cancion.id_cancion,
          nombre: cancion.nombre,
          artista: cancion.artista,
          precio_unitario: normalizar_precio(cancion.precio_unitario),
          cantidad: 1
        }
      ];
    });

    mostrar_exito(`Agregaste "${cancion.nombre}" al carrito.`);
  }

  function cambiar_cantidad(idCancion, cambio) {
    setCarrito((previo) =>
      previo
        .map((item) =>
          item.id_cancion === idCancion
            ? { ...item, cantidad: Math.max(0, item.cantidad + cambio) }
            : item
        )
        .filter((item) => item.cantidad > 0)
    );
  }

  function quitar_del_carrito(idCancion) {
    setCarrito((previo) => previo.filter((item) => item.id_cancion !== idCancion));
  }

  function vaciar_carrito() {
    setCarrito([]);
    mostrar_exito("Carrito vaciado.");
  }

  async function comprar_carrito() {
    if (!idClienteSeleccionado) {
      mostrar_error("Selecciona un cliente para comprar.");
      return;
    }

    if (carrito.length === 0) {
      mostrar_error("El carrito esta vacio. Agrega al menos una cancion.");
      return;
    }

    try {
      setCargandoCompra(true);
      const idCliente = Number(idClienteSeleccionado);
      const facturas = [];

      // La API actual registra una compra por cancion.
      for (const item of carrito) {
        for (let i = 0; i < item.cantidad; i += 1) {
          const resultado = await comprar_cancion({
            id_cliente: idCliente,
            id_cancion: item.id_cancion
          });
          facturas.push(resultado.id_factura);
        }
      }

      setCarrito([]);
      mostrar_exito(
        `Compra confirmada: ${facturas.length} item(s). Facturas generadas: ${facturas.join(", ")}.`
      );
    } catch (err) {
      mostrar_error(err.message);
    } finally {
      setCargandoCompra(false);
    }
  }

  return (
    <main className="contenedor">
      <header className="encabezado">
        <div>
          <p className="etiqueta">Panel musical</p>
          <h1>Tienda Chinook</h1>
          <p className="subtitulo">Busca por artista/genero, arma tu carrito y confirma la compra.</p>
        </div>
        <div className="resumen-flotante" aria-label="resumen-carrito">
          <span>{totalItems} item(s)</span>
          <strong>{formato_precio(totalCarrito)}</strong>
        </div>
      </header>

      {notificacion ? (
        <div className={`alerta ${notificacion.tipo}`} role="status">
          <span>{notificacion.texto}</span>
          <button type="button" className="boton-alerta" onClick={() => setNotificacion(null)}>
            Cerrar
          </button>
        </div>
      ) : null}

      <section className="grid-principal">
        <BuscadorCanciones
          filtros={filtros}
          cargando={cargandoBusqueda}
          alCambiarFiltros={setFiltros}
          alBuscar={manejar_busqueda}
          alLimpiar={limpiar_filtros}
        />

        <FormularioCompra
          clientes={clientes}
          carrito={carrito}
          idClienteSeleccionado={idClienteSeleccionado}
          cargando={cargandoCompra}
          total={totalCarrito}
          onCambiarCliente={setIdClienteSeleccionado}
          onCambiarCantidad={cambiar_cantidad}
          onQuitarDelCarrito={quitar_del_carrito}
          onVaciarCarrito={vaciar_carrito}
          onComprarCarrito={comprar_carrito}
          formatoPrecio={formato_precio}
        />
      </section>

      <section className="tarjeta resultados">
        <div className="resultados-encabezado">
          <h2>Canciones disponibles</h2>
          <span>{canciones.length} resultado(s)</span>
        </div>
        <div className="tabla-scroll">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Cancion</th>
                <th>Artista</th>
                <th>Genero</th>
                <th>Precio</th>
                <th>Accion</th>
              </tr>
            </thead>
            <tbody>
              {canciones.map((cancion) => (
                <tr key={cancion.id_cancion}>
                  <td>{cancion.id_cancion}</td>
                  <td>{cancion.nombre}</td>
                  <td>{cancion.artista}</td>
                  <td>{cancion.genero}</td>
                  <td>{formato_precio(normalizar_precio(cancion.precio_unitario))}</td>
                  <td>
                    <button
                      type="button"
                      className="boton-secundario"
                      onClick={() => agregar_al_carrito(cancion)}
                    >
                      Agregar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
