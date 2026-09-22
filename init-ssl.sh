#!/bin/bash
set -e

# ==============================================================================
# SSL Certificate Initialization Script using Let's Encrypt & Docker Compose
# ==============================================================================

if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Please create .env from .env.example first."
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

if [ -z "$DOMAIN_NAME" ]; then
    echo "ERROR: DOMAIN_NAME is not set in .env"
    exit 1
fi

if [ -z "$CERTBOT_EMAIL" ]; then
    echo "ERROR: CERTBOT_EMAIL is not set in .env"
    exit 1
fi

domains=($DOMAIN_NAME www.$DOMAIN_NAME)
rsa_key_size=4096
data_path="./certbot"
email="$CERTBOT_EMAIL"
staging=0 # Set to 1 if you're testing your setup to avoid hitting Let's Encrypt rate limits

echo "### Starting SSL initialization for ${domains[*]}..."

if [ -d "$data_path/conf/live/$DOMAIN_NAME" ]; then
    read -p "Existing data found for $DOMAIN_NAME. Continue and replace existing certificate? (y/N) " decision
    if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
        exit 0
    fi
fi

echo "### 1. Downloading recommended TLS parameters..."
mkdir -p "$data_path/conf"
if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
fi

echo "### 2. Creating dummy certificate for $DOMAIN_NAME to allow Nginx startup..."
path="/etc/letsencrypt/live/$DOMAIN_NAME"
mkdir -p "$data_path/conf/live/$DOMAIN_NAME"
docker compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot

echo "### 3. Starting Nginx..."
docker compose up --force-recreate -d nginx

echo "### 4. Deleting dummy certificate for $DOMAIN_NAME..."
docker compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$DOMAIN_NAME && \
  rm -Rf /etc/letsencrypt/archive/$DOMAIN_NAME && \
  rm -Rf /etc/letsencrypt/renewal/$DOMAIN_NAME.conf" certbot

echo "### 5. Requesting Let's Encrypt certificate for ${domains[*]}..."
# Join $domains to -d args
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Select appropriate email arg
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot

echo "### 6. Reloading Nginx with new certificate..."
docker compose exec nginx nginx -s reload

echo "=== SSL Certificate successfully initialized for $DOMAIN_NAME! ==="
