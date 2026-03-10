# Checklist Requerimientos Parcial

## Funcionales

- [x] Conectar a base Chinook en motor relacional PostgreSQL.
- [x] RDS no publica.
- [x] Implementar estructura Chinook (script SQL).
- [x] Compra de canciones por cliente.
- [x] Busqueda por cancion, artista y genero.
- [x] Validaciones frontend y backend.
- [x] Alertas de exito/error en operaciones.
- [ ] Registro/login y roles (opcional, no obligatorio).

## Tecnicos

- [x] Frontend con React.
- [x] Backend con FastAPI.

## Pruebas

- [x] Pruebas unitarias de servicios backend.
- [x] Pruebas unitarias de endpoints backend.
- [x] Pruebas unitarias de componentes frontend.
- [x] Pruebas unitarias de consumo API frontend.

## CI/CD

- [x] Instala dependencias automaticamente.
- [x] Ejecuta pruebas al hacer push.
- [x] Si pasan pruebas, despliega backend en EC2.
- [x] Si pasan pruebas, despliega frontend en EC2.
- [x] Reinicia servicios luego del despliegue.

## Infraestructura con prefijo

- [x] CDK con prefijo `bnd-test-`.
- [x] Crea VPC completa (publica/privada) por defecto.
- [x] Crea EC2 frontend/backend.
- [x] Crea RDS PostgreSQL privada.
