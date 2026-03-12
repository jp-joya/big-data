import React from "react";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../App";

function mockRespuesta(data, ok = true, status = 200) {
  return Promise.resolve({
    ok,
    status,
    json: async () => data
  });
}

describe("App", () => {
  beforeEach(() => {
    global.fetch = vi
      .fn()
      .mockImplementationOnce(() => mockRespuesta([{ id_cliente: 1, nombre_completo: "Ana Lopez" }]))
      .mockImplementationOnce(() =>
        mockRespuesta([
          {
            id_cancion: 1,
            nombre: "Thunderstruck",
            artista: "AC/DC",
            genero: "Rock",
            precio_unitario: "0.99"
          }
        ])
      );
  });

  it("muestra resultados iniciales", async () => {
    render(<App />);

    expect(screen.getByText("Tienda Chinook")).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText("Thunderstruck")).toBeInTheDocument();
    });
  });

  it("agrega cancion al carrito y valida cliente antes de comprar", async () => {
    const usuario = userEvent.setup();
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Thunderstruck")).toBeInTheDocument();
    });

    await usuario.click(screen.getByRole("button", { name: "Agregar" }));

    const panelCarrito = screen.getByLabelText("panel-carrito");
    expect(within(panelCarrito).getByText("Thunderstruck")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Comprar carrito" }));
    expect(screen.getByText("Selecciona un cliente para comprar.")).toBeInTheDocument();
  });
});
