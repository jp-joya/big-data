import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
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
    global.fetch = vi.fn()
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

    expect(screen.getByText("Parcial 1")).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText("Thunderstruck")).toBeInTheDocument();
    });
  });

  it("valida formulario de compra en frontend", async () => {
    const usuario = userEvent.setup();
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Thunderstruck")).toBeInTheDocument();
    });

    await usuario.click(screen.getByRole("button", { name: "Comprar" }));
    expect(screen.getByText("Debes seleccionar un cliente")).toBeInTheDocument();
  });
});
