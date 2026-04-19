#!/usr/bin/env bash
#
# Automated setup for sudu_django on a fresh Ubuntu 24.04 Digital Ocean droplet.
# Run as root: bash /opt/sudu_django/deploy/setup-droplet.sh
#
set -euo pipefail

PROJECT_DIR="/opt/sudu_django"
COMPOSE_FILE="docker-compose.prod.yml"

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root." >&2
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Project directory $PROJECT_DIR does not exist." >&2
    echo "Clone the repo first: git clone <repo> $PROJECT_DIR" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# 1. System updates
# ---------------------------------------------------------------------------
info "Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq

# ---------------------------------------------------------------------------
# 2. Install Docker (official repo)
# https://docs.docker.com/engine/install/ubuntu/
# ---------------------------------------------------------------------------
if command -v docker &> /dev/null; then
    info "Docker already installed: $(docker --version)"
else
    info "Installing Docker..."
    apt-get install -y -qq ca-certificates curl

    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
      https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
      > /etc/apt/sources.list.d/docker.list

    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin

    systemctl enable docker
    systemctl start docker
    info "Docker installed: $(docker --version)"
fi

# ---------------------------------------------------------------------------
# 3. Firewall (UFW)
# ---------------------------------------------------------------------------
info "Configuring firewall..."
apt-get install -y -qq ufw

ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

info "Firewall enabled. Allowed: SSH, HTTP, HTTPS"

# ---------------------------------------------------------------------------
# 4. fail2ban
# ---------------------------------------------------------------------------
info "Installing fail2ban..."
apt-get install -y -qq fail2ban
systemctl enable fail2ban
systemctl start fail2ban
info "fail2ban active"

# ---------------------------------------------------------------------------
# 5. Generate environment files (if they don't exist)
# ---------------------------------------------------------------------------
cd "$PROJECT_DIR"

if [ -f .env.prod ]; then
    warn ".env.prod already exists, skipping generation"
else
    info "Generating .env.prod..."

    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")

    # Prompt for the domain/IP
    read -rp "Enter your domain or droplet IP (e.g. sudu.film or 134.209.x.x): " DOMAIN
    DOMAIN=${DOMAIN:-localhost}

    cat > .env.prod << EOF
DEBUG=0
SECRET_KEY=${SECRET_KEY}
DJANGO_ALLOWED_HOSTS=${DOMAIN},localhost
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=sudu_django_prod
SQL_USER=sudu_django
SQL_PASSWORD=${DB_PASSWORD}
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
EOF

    cat > .env.prod.db << EOF
POSTGRES_USER=sudu_django
POSTGRES_PASSWORD=${DB_PASSWORD}
POSTGRES_DB=sudu_django_prod
EOF

    chmod 600 .env.prod .env.prod.db
    info "Environment files created with random secrets"
fi

# ---------------------------------------------------------------------------
# 6. Build and start containers
# ---------------------------------------------------------------------------
info "Building and starting containers (this may take a few minutes)..."
docker compose -f "$COMPOSE_FILE" up -d --build

# Wait for web container to be healthy
info "Waiting for containers to be ready..."
sleep 5

# ---------------------------------------------------------------------------
# 7. Run migrations (also handled by entrypoint, but explicit is safer)
# ---------------------------------------------------------------------------
info "Running migrations..."
docker compose -f "$COMPOSE_FILE" exec web python manage.py migrate --noinput

# ---------------------------------------------------------------------------
# 8. Collect static files
# ---------------------------------------------------------------------------
info "Collecting static files..."
docker compose -f "$COMPOSE_FILE" exec web python manage.py collectstatic --noinput

# ---------------------------------------------------------------------------
# 9. Create superuser (interactive)
# ---------------------------------------------------------------------------
info "Creating admin superuser..."
docker compose -f "$COMPOSE_FILE" exec web python manage.py createsuperuser

# ---------------------------------------------------------------------------
# 10. Summary
# ---------------------------------------------------------------------------
DROPLET_IP=$(curl -s -4 ifconfig.me || echo "<unknown>")

echo ""
echo "============================================"
echo "  sudu_django deployment complete!"
echo "============================================"
echo ""
echo "  Admin:    http://${DROPLET_IP}/admin/"
echo "  Reports:  http://${DROPLET_IP}/cinema/reports/"
echo ""
echo "  Containers:  docker compose -f $COMPOSE_FILE ps"
echo "  Logs:        docker compose -f $COMPOSE_FILE logs -f"
echo "  Restart:     docker compose -f $COMPOSE_FILE restart"
echo "  Rebuild:     docker compose -f $COMPOSE_FILE up -d --build"
echo ""
echo "  Firewall:    ufw status"
echo "  fail2ban:    systemctl status fail2ban"
echo ""
if [ "${DOMAIN:-}" != "localhost" ] && [ -n "${DOMAIN:-}" ]; then
    echo "  Remember to point DNS for ${DOMAIN} to ${DROPLET_IP}"
    echo ""
fi
echo "============================================"
