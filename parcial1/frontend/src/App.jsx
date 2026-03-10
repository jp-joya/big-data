import React, { useEffect, useState } from "react";
import BuscadorCanciones from "./components/BuscadorCanciones";
import FormularioCompra from "./components/FormularioCompra";
import { buscar_canciones, comprar_cancion, obtener_clientes } from "./services/api";

export default function App() {
  const [clientes, setClientes] = useState([]);
  const [canciones, setCanciones] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");
  const [cargandoCompra, setCargandoCompra] = useState(false);

  useEffect(() => {
    cargar_clientes();
    ejecutar_busqueda({});
  }, []);

  async function cargar_clientes() {
    try {
      setError("");
      const data = await obtener_clientes();
      setClientes(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function ejecutar_busqueda(filtros) {
    try {
      setError("");
      const data = await buscar_canciones(filtros);
      setCanciones(data);
      if (data.length === 0) {
        setMensaje("No se encontraron canciones para ese filtro");
      } else {
        setMensaje("");
      }
    } catch (err) {
      setError(err.message);
    }
  }

  async function ejecutar_compra(payload) {
    try {
      setCargandoCompra(true);
      setError("");
      const data = await comprar_cancion(payload);
      setMensaje(`Compra exitosa. Factura #${data.id_factura} por ${data.total}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargandoCompra(false);
    }
  }

  return (
    <main className="contenedor">
      <header>
        <h1>Parcial 1</h1>
        <p>Busca canciones y registra compras en linea.</p>
      </header>

      {mensaje ? <p className="alerta exito">{mensaje}</p> : null}
      {error ? <p className="alerta error">{error}</p> : null}

      <section className="grid-principal">
        <BuscadorCanciones alBuscar={ejecutar_busqueda} />
        <FormularioCompra
          clientes={clientes}
          canciones={canciones}
          alComprar={ejecutar_compra}
          cargando={cargandoCompra}
        />
      </section>

      <section className="tarjeta">
        <h2>Resultados</h2>
        <div className="tabla-scroll">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Cancion</th>
                <th>Artista</th>
                <th>Genero</th>
                <th>Precio</th>
              </tr>
            </thead>
            <tbody>
              {canciones.map((cancion) => (
                <tr key={cancion.id_cancion}>
                  <td>{cancion.id_cancion}</td>
                  <td>{cancion.nombre}</td>
                  <td>{cancion.artista}</td>
                  <td>{cancion.genero}</td>
                  <td>{cancion.precio_unitario}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
