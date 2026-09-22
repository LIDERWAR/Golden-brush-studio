#!/bin/bash
set -e

# ==============================================================================
# Production Deployment & Update Script for GB STUDIO
# ==============================================================================

echo "=========================================="
echo "  GB STUDIO - Production Deployment Tool  "
echo "=========================================="

# 1. Check for .env file
if [ ! -f .env ]; then
    echo "[!] .env file not found."
    if [ -f .env.example ]; then
        echo "[+] Copying .env.example to .env..."
        cp .env.example .env
        echo "[!] Please edit .env with your domain and database credentials before continuing."
        exit 1
    else
        echo "[ERROR] Neither .env nor .env.example was found."
        exit 1
    fi
fi

# Load variables
export $(grep -v '^#' .env | xargs)

DOMAIN=${DOMAIN_NAME:-localhost}
echo "[+] Target Domain / Host: $DOMAIN"

# 2. Check and prepare SSL certificates directory
CERT_DIR="./certbot/conf/live/$DOMAIN"
if [ ! -f "$CERT_DIR/fullchain.pem" ]; then
    echo "[+] SSL certificate not found for $DOMAIN. Generating temporary certificate..."
    mkdir -p "$CERT_DIR"
    mkdir -p "./certbot/www"
    
    # Generate temporary self-signed cert so Nginx can start up without failing
    openssl req -x509 -nodes -newkey rsa:2048 -days 30 \
        -keyout "$CERT_DIR/privkey.pem" \
        -out "$CERT_DIR/fullchain.pem" \
        -subj "/CN=$DOMAIN" > /dev/null 2>&1 || true
    echo "[+] Temporary certificate generated."
fi

# 3. Pull latest changes if in git repository
if [ -d .git ]; then
    echo "[+] Checking for git updates..."
    git pull --no-rebase || true
fi

# 4. Build and start containers
echo "[+] Building and starting Docker containers..."
docker compose build --pull
docker compose up -d

echo "[+] Waiting for web service to be healthy..."
sleep 5

# 5. Check database and apply migrations
echo "[+] Running migrations..."
docker compose exec -T web python manage.py migrate --noinput

echo "[+] Collecting static files..."
docker compose exec -T web python manage.py collectstatic --noinput

# 6. Check if seed data should be populated
if [ "$AUTO_SEED_DB" = "true" ] || [ "$AUTO_SEED_DB" = "1" ]; then
    echo "[+] Seeding initial data..."
    docker compose exec -T web python seed_db.py || true
fi

echo "=========================================="
echo " Deployment completed successfully!"
echo " Web site is live at: http://$DOMAIN or https://$DOMAIN"
echo ""
echo " Next steps:"
echo " 1. To issue trusted Let's Encrypt SSL certificate:"
echo "    chmod +x init-ssl.sh && ./init-ssl.sh"
echo " 2. To populate demo data and superuser manually:"
echo "    docker compose exec web python seed_db.py"
echo " 3. To view application logs:"
echo "    docker compose logs -f web"
echo "=========================================="
