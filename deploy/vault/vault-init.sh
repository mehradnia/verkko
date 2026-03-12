#!/bin/sh
# Waits for Vault and PostgreSQL, then configures dynamic database secrets.
# Requires: VAULT_ADDR, VAULT_TOKEN, DB_HOST, DB_PORT, DB_NAME, DB_ADMIN_USER, DB_ADMIN_PASS

set -e

# Wait for Vault
until vault status > /dev/null 2>&1; do
  echo "Waiting for Vault..."
  sleep 1
done

# Wait for PostgreSQL
until nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done
sleep 2

# Enable database secrets engine
vault secrets enable database 2>/dev/null || true

# Configure PostgreSQL connection
vault write database/config/verkko-db \
  plugin_name=postgresql-database-plugin \
  allowed_roles="verkko-service" \
  connection_url="postgresql://{{username}}:{{password}}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=${DB_SSLMODE:-require}" \
  username="$DB_ADMIN_USER" \
  password="$DB_ADMIN_PASS"

# Create role for the app (1h TTL, max 24h)
vault write database/roles/verkko-service \
  db_name=verkko-db \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT CREATE ON SCHEMA public TO \"{{name}}\"; GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\"; GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO \"{{name}}\";" \
  revocation_statements="DROP ROLE IF EXISTS \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

echo "Vault database secrets engine configured."
