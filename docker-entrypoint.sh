#!/bin/bash
set -e

# Espera pelo PostgreSQL
until psql "$DATABASE_URL" -c '\q'; do
  echo "PostgreSQL ainda não está disponível - aguardando..."
  sleep 1
done

echo "PostgreSQL está disponível - continuando..."

# Executa as migrações
alembic upgrade head

# Executa o comando passado para o container
exec "$@" 