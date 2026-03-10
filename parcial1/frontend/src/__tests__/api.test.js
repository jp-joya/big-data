import { buscar_canciones, comprar_cancion } from "../services/api";

function respuesta(data, ok = true) {
  return Promise.resolve({ ok, json: async () => data });
}

describe("servicio api", () => {
  it("arma query de busqueda", async () => {
    global.fetch = vi.fn().mockImplementationOnce(() => respuesta([]));

    await buscar_canciones({ termino: "rock", artista: "acdc", genero: "rock" });

    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch.mock.calls[0][0]).toContain("termino=rock");
    expect(global.fetch.mock.calls[0][0]).toContain("artista=acdc");
    expect(global.fetch.mock.calls[0][0]).toContain("genero=rock");
  });

  it("propaga error de backend en compra", async () => {
    global.fetch = vi.fn().mockImplementationOnce(() =>
      respuesta({ detail: "El cliente no existe" }, false)
    );

    await expect(comprar_cancion({ id_cliente: 1, id_cancion: 2 })).rejects.toThrow(
      "El cliente no existe"
    );
  });
});
