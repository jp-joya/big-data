#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <DATABASE_URL>"
  echo "Ejemplo: $0 postgresql://usuario:clave@host:5432/chinook"
  exit 1
fi

DATABASE_URL="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

psql "${DATABASE_URL}" -f "${ROOT_DIR}/backend/sql/chinook_postgres.sql"
psql "${DATABASE_URL}" -f "${ROOT_DIR}/backend/sql/chinook_datos_minimos.sql"

echo "Esquema y datos minimos cargados correctamente."
