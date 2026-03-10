# Parcial 1 - Big Data 2026-1

Implementacion full-stack para compra de canciones basada en Chinook, con backend en FastAPI, frontend React, infraestructura completa en AWS CDK y CI/CD en GitHub Actions.


## Estructura

- `backend/`: API FastAPI + SQLAlchemy + pruebas PyTest.
- `frontend/`: SPA React (Vite) + pruebas Vitest.
- `infra/`: CDK (Python) para RDS privada y EC2 frontend/backend.
- `scripts/`: utilidades operativas (carga de esquema Chinook).
- `.github/workflows/`: CI/CD de aplicacion y despliegue de infraestructura.

## Requisitos implementados

- RDS PostgreSQL no publica (`publicly_accessible=False`) en subredes privadas.
- Busqueda por cancion/artista/genero.
- Compra de cancion para cliente (crea factura + linea de factura).
- Validaciones en frontend y backend.
- Alertas de exito/error en UI.
- Pruebas unitarias backend y frontend.
- Pipeline CI/CD para instalar dependencias, ejecutar pruebas y desplegar en EC2.

## Ejecucion local

### 1) Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

API: `http://localhost:8000`

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

Para apuntar a otra API:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

## Cargar esquema Chinook en RDS

```bash
./scripts/cargar_chinook_rds.sh "postgresql://usuario:clave@host:5432/chinook"
```

Esto ejecuta:

- `backend/sql/chinook_postgres.sql`
- `backend/sql/chinook_datos_minimos.sql`

## Despliegue de infraestructura (CDK)

```bash
cd infra
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy
```

Notas:

- Por defecto CDK crea VPC nueva con subredes publicas y privadas aisladas en 2 AZ.
- Region default: `us-east-1`.
- Si quieres reutilizar una VPC: `-c crearVpc=false -c vpcId=vpc-xxxx`.
- Si quieres customizar red: `-c vpcCidr=10.60.0.0/16 -c maxAzs=2 -c natGateways=0`.
- Default `natGateways=0` evita errores de cuota cuando la cuenta ya alcanzo el limite de NAT Gateway.
- Si quieres cambiar version de PostgreSQL: `-c rdsVersionFull=15.10 -c rdsVersionMajor=15`.
- Si quieres usar key pair: `-c keyName=tu-keypair`.
- Si quieres usar roles existentes: `-c ec2RoleArn=arn:...` o `-c backendRoleArn=arn:... -c frontendRoleArn=arn:...`.
- Todos los nombres usan prefijo `bnd-test-`.

## Secrets requeridos en GitHub Actions

Para `.github/workflows/ci-cd-app.yml`:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `DEPLOY_GITHUB_TOKEN` (token con permiso de lectura del repo)
- `BND_TEST_BACKEND_INSTANCE_ID`
- `BND_TEST_FRONTEND_INSTANCE_ID`
- `BACKEND_DATABASE_URL`
- `FRONTEND_API_URL` (ejemplo: `http://<IP_BACKEND>:8000`)

## Comandos de pruebas

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm test
```
