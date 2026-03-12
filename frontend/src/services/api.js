const URL_API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function manejar_respuesta(respuesta) {
  let data = {};

  try {
    data = await respuesta.json();
  } catch {
    data = {};
  }

  if (!respuesta.ok) {
    throw new Error(data.detail ?? "Error inesperado en API");
  }

  return data;
}

export async function obtener_clientes() {
  const respuesta = await fetch(`${URL_API}/api/clientes`);
  return manejar_respuesta(respuesta);
}

export async function buscar_canciones(filtros) {
  const parametros = new URLSearchParams();

  if (filtros.termino) parametros.set("termino", filtros.termino);
  if (filtros.artista) parametros.set("artista", filtros.artista);
  if (filtros.genero) parametros.set("genero", filtros.genero);

  const respuesta = await fetch(`${URL_API}/api/canciones?${parametros.toString()}`);
  return manejar_respuesta(respuesta);
}

export async function comprar_cancion(payload) {
  const respuesta = await fetch(`${URL_API}/api/compras`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return manejar_respuesta(respuesta);
}
