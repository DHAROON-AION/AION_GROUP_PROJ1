#!/bin/bash
set -euo pipefail

host="${POSTGRES_HOST:-postgres}"
port="${POSTGRES_PORT:-5432}"
user="${POSTGRES_USER:-aion_admin}"
db="${POSTGRES_DB:-aion_banking}"

echo "Waiting for PostgreSQL at ${host}:${port}..."
until pg_isready -h "$host" -p "$port" -U "$user" -d "$db" > /dev/null 2>&1; do
  sleep 2
done
echo "PostgreSQL is ready."

exec "$@"
