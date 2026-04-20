#!/usr/bin/env bash
#
# Update sudu_django on an existing Digital Ocean droplet.
# Assumes code is already up to date (git pull done separately).
# Run as root from the project directory: bash deploy/update-droplet.sh
#
set -euo pipefail

PROJECT_DIR="/opt/sudu_django"
COMPOSE_FILE="docker-compose.prod.yml"

GREEN='\033[0;32m'
NC='\033[0m'
info() { echo -e "${GREEN}[INFO]${NC} $1"; }

cd "$PROJECT_DIR"

info "Rebuilding images..."
docker compose -f "$COMPOSE_FILE" build

info "Restarting via systemd..."
systemctl restart sudu-django

info "Waiting for containers to be ready..."
sleep 5

info "Running migrations..."
docker compose -f "$COMPOSE_FILE" exec web python manage.py migrate --noinput

info "Collecting static files..."
docker compose -f "$COMPOSE_FILE" exec web python manage.py collectstatic --noinput

info "Done. Service status:"
systemctl status sudu-django --no-pager
echo ""
docker compose -f "$COMPOSE_FILE" ps
